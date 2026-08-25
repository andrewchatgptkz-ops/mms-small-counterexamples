#!/usr/bin/env python3
"""Exact replay of the recoverable T=60 search facts.

This is not the missing stochastic search.  It independently derives the exact
T-partitions, incidence candidates, and set-packing score of the two T=60
profiles recorded in checkpoints.md.  It uses only the Python standard library.
"""
from __future__ import annotations

from itertools import permutations
from typing import Iterable, Sequence

SIDE = 4

R11 = [15, 22, 23, 16, 13, 31, 39, 21, 1, 55, 4]
C11 = [9, 21, 25, 19, 4, 33, 50, 20, 1, 56, 2]
R12 = [44, 16, 8, 42, 10, 34, 1, 24, 1, 14, 14, 32]
C12 = [46, 19, 11, 40, 6, 37, 1, 20, 1, 12, 13, 34]
T = 60


def subset_sums(values: Sequence[int]) -> list[int]:
    sums = [0] * (1 << len(values))
    for mask in range(1, 1 << len(values)):
        bit = mask & -mask
        j = bit.bit_length() - 1
        sums[mask] = sums[mask ^ bit] + values[j]
    return sums


def exact_four_partitions(values: Sequence[int], target: int) -> list[tuple[int, ...]]:
    """Every unordered partition into four target-valued nonempty bundles."""
    m = len(values)
    full = (1 << m) - 1
    sums = subset_sums(values)
    exact = [mask for mask in range(1, 1 << m) if sums[mask] == target]
    by_good: list[list[int]] = [[] for _ in range(m)]
    for mask in exact:
        for g in range(m):
            if mask & (1 << g):
                by_good[g].append(mask)

    out: list[tuple[int, ...]] = []

    def rec(remaining: int, blocks: tuple[int, ...]) -> None:
        if remaining == 0:
            if len(blocks) == 4:
                out.append(blocks)
            return
        if len(blocks) >= 4:
            return
        first = (remaining & -remaining).bit_length() - 1
        for block in by_good[first]:
            if block & remaining == block:
                rec(remaining ^ block, blocks + (block,))

    rec(full, ())
    return out


def goods(mask: int, m: int) -> tuple[int, ...]:
    return tuple(g + 1 for g in range(m) if mask & (1 << g))


def partition_text(partition: Sequence[int], m: int) -> str:
    return " | ".join("{" + ",".join(f"g{g}" for g in goods(mask, m)) + "}" for mask in partition)


def minimal_threshold_bundles(values: Sequence[int], target: int) -> list[int]:
    m = len(values)
    sums = subset_sums(values)
    out = []
    for mask in range(1, 1 << m):
        if sums[mask] < target:
            continue
        if all(sums[mask ^ (1 << g)] < target for g in range(m) if mask & (1 << g)):
            out.append(mask)
    return out


def disjoint_pair_unions(bundles: Sequence[int]) -> list[int]:
    out: list[int] = []
    for i, left in enumerate(bundles):
        for right in bundles[i + 1 :]:
            if left & right == 0:
                out.append(left | right)
    return out


def exact_score(row_values: Sequence[int], col_values: Sequence[int], target: int) -> dict[str, int]:
    """Count compatible pairs of disjoint row bundles and column bundles.

    The score is the number of ordered-by-type pair-of-pairs (P_R, P_C), where
    P_R is an unordered pair of disjoint inclusion-minimal row bundles, P_C is
    the analogous column pair, and the two unions are disjoint.  A profile has
    an MMS allocation iff this score is positive.
    """
    m = len(row_values)
    full = (1 << m) - 1
    min_row = minimal_threshold_bundles(row_values, target)
    min_col = minimal_threshold_bundles(col_values, target)
    row_pairs = disjoint_pair_unions(min_row)
    col_pairs = disjoint_pair_unions(min_col)

    contained = [0] * (1 << m)
    for union in col_pairs:
        contained[union] += 1
    for bit in range(m):
        flag = 1 << bit
        for mask in range(1 << m):
            if mask & flag:
                contained[mask] += contained[mask ^ flag]

    compatible_row_pairs = 0
    score = 0
    for union in row_pairs:
        count = contained[full ^ union]
        compatible_row_pairs += int(count > 0)
        score += count

    return {
        "minimal_row": len(min_row),
        "minimal_col": len(min_col),
        "row_pairs": len(row_pairs),
        "col_pairs": len(col_pairs),
        "compatible_row_pairs": compatible_row_pairs,
        "score": score,
    }


def incidence_from_partitions(
    row_partition: Sequence[int], col_partition: Sequence[int], m: int
) -> tuple[list[tuple[int, int]], int] | None:
    row_of = [-1] * m
    col_of = [-1] * m
    for row, block in enumerate(row_partition):
        for g in range(m):
            if block & (1 << g):
                row_of[g] = row
    for col, block in enumerate(col_partition):
        for g in range(m):
            if block & (1 << g):
                col_of[g] = col
    coords = list(zip(row_of, col_of))
    if any(r < 0 or c < 0 for r, c in coords) or len(set(coords)) != m:
        return None
    mask = sum(1 << (SIDE * r + c) for r, c in coords)
    return coords, mask


PERMS = list(permutations(range(SIDE)))


def permute_pattern(mask: int, row_perm: Sequence[int], col_perm: Sequence[int]) -> int:
    out = 0
    for row in range(SIDE):
        for col in range(SIDE):
            if mask & (1 << (SIDE * row + col)):
                out |= 1 << (SIDE * row_perm[row] + col_perm[col])
    return out


def canonical_pattern(mask: int) -> int:
    return min(permute_pattern(mask, rp, cp) for rp in PERMS for cp in PERMS)


def print_candidate(name: str, row_values: Sequence[int], col_values: Sequence[int]) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    row_parts = exact_four_partitions(row_values, T)
    col_parts = exact_four_partitions(col_values, T)
    print(name)
    print(f"  goods={len(row_values)} target={T} totals=({sum(row_values)},{sum(col_values)})")
    print(f"  exact row T-partitions={len(row_parts)}")
    for part in row_parts:
        print("    " + partition_text(part, len(row_values)))
    print(f"  exact column T-partitions={len(col_parts)}")
    for part in col_parts:
        print("    " + partition_text(part, len(col_values)))
    print(f"  packing_stats={exact_score(row_values, col_values, T)}")
    return row_parts, col_parts


def main() -> None:
    row11, col11 = print_candidate("11-good initial T=60", R11, C11)
    assert len(row11) == len(col11) == 1
    # Preserve the row/column order literally retained in both simplification scripts.
    retained_rows11 = tuple(sum(1 << (g - 1) for g in block) for block in ((1,2,3),(4,5,6),(7,8),(9,10,11)))
    retained_cols11 = tuple(sum(1 << (g - 1) for g in block) for block in ((1,7,9),(2,4,8),(5,10),(3,6,11)))
    assert set(retained_rows11) == set(row11[0])
    assert set(retained_cols11) == set(col11[0])
    inc11 = incidence_from_partitions(retained_rows11, retained_cols11, len(R11))
    assert inc11 is not None
    coords11, mask11 = inc11
    print("  incidence_status=RECOVERED EXACTLY UP TO ROW/COLUMN LABEL PERMUTATIONS")
    print("  The displayed labels below are the literal order retained in the simplification scripts.")
    print("  good_coordinates=" + str([(f"g{i+1}", r + 1, c + 1) for i, (r, c) in enumerate(coords11)]))
    print(f"  pattern_mask=0x{mask11:04x} canonical_mask=0x{canonical_pattern(mask11):04x}")
    print()

    row12, col12 = print_candidate("12-good initial T=60", R12, C12)
    assert len(row12) == 1 and len(col12) == 4
    print("  incidence_status=NOT UNIQUELY RECOVERABLE")
    print("  Every pairing below is a simple 4x4 incidence assignment consistent with the retained vectors.")
    seen_orbits: set[int] = set()
    for index, col_part in enumerate(col12, 1):
        incidence = incidence_from_partitions(row12[0], col_part, len(R12))
        assert incidence is not None
        coords, mask = incidence
        canon = canonical_pattern(mask)
        seen_orbits.add(canon)
        print(f"    option={index} pattern_mask=0x{mask:04x} canonical_mask=0x{canon:04x}")
        print("      column_partition=" + partition_text(col_part, len(C12)))
        print("      good_coordinates=" + str([(f"g{i+1}", r + 1, c + 1) for i, (r, c) in enumerate(coords)]))
    print(f"  compatible assignments=4 distinct row/column orbits={len(seen_orbits)}")
    print("  Therefore the original 12-edge incidence orbit cannot be selected from retained data alone.")

    assert exact_score(R11, C11, T)["score"] == 0
    assert exact_score(R12, C12, T)["score"] == 0
    assert len(seen_orbits) == 2
    print("REPLAY PASSED")


if __name__ == "__main__":
    main()
