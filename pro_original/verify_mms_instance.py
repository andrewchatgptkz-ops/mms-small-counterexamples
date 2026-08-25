#!/usr/bin/env python3
"""Independent exact verifier; standard library only.

It enumerates every unordered partition into four nonempty bundles to compute
MMS, then every one of the 4^11 complete allocations. All arithmetic is integer.
"""
from itertools import product

VALUES = [
    [7, 12, 11, 8, 6, 16, 21, 9, 1, 28, 1],
    [7, 12, 11, 8, 6, 16, 21, 9, 1, 28, 1],
    [6, 10, 13, 10, 4, 15, 23, 10, 1, 26, 2],
    [6, 10, 13, 10, 4, 15, 23, 10, 1, 26, 2],
]


def unordered_partitions(m, n):
    """Restricted-growth strings; each set partition appears exactly once."""
    labels = [0] * m

    def rec(pos, used):
        if pos == m:
            if used == n:
                bundles = [[] for _ in range(n)]
                for good, bundle in enumerate(labels):
                    bundles[bundle].append(good)
                yield tuple(tuple(bundle) for bundle in bundles)
            return
        if m - pos < n - used:
            return
        for bundle in range(used):
            labels[pos] = bundle
            yield from rec(pos + 1, used)
        if used < n:
            labels[pos] = used
            yield from rec(pos + 1, used + 1)

    yield from rec(0, 0)


def exact_mms(row, n):
    best = -1
    witness = None
    count = 0
    for partition in unordered_partitions(len(row), n):
        count += 1
        minimum = min(sum(row[g] for g in bundle) for bundle in partition)
        if minimum > best:
            best = minimum
            witness = partition
    return best, witness, count


def main():
    n = len(VALUES)
    m = len(VALUES[0])
    mms = []
    print("Exact MMS calculation by all unordered 4-partitions")
    for agent, row in enumerate(VALUES, 1):
        value, witness, count = exact_mms(row, n)
        mms.append(value)
        human = tuple(tuple(g + 1 for g in bundle) for bundle in witness)
        print(f"agent {agent}: MMS={value}, partitions checked={count}, witness={human}")

    mms_allocations = 0
    best_common = -1
    best_assignment = None
    best_utilities = None
    checked = 0

    for assignment in product(range(n), repeat=m):
        checked += 1
        utilities = [0] * n
        for good, owner in enumerate(assignment):
            utilities[owner] += VALUES[owner][good]
        if all(utilities[a] >= mms[a] for a in range(n)):
            mms_allocations += 1
        minimum = min(utilities)
        if minimum > best_common:
            best_common = minimum
            best_assignment = assignment
            best_utilities = tuple(utilities)

    print("\nComplete-allocation enumeration")
    print(f"allocations checked={checked} (=4^11)")
    print(f"MMS allocations={mms_allocations}")
    print(f"maximum over allocations of min_i v_i(A_i)={best_common}")
    print(f"one maximizing assignment={best_assignment}")
    print(f"utilities there={best_utilities}")

    assert mms == [30, 30, 30, 30]
    assert checked == 4**11
    assert mms_allocations == 0
    assert best_common == 29
    print("\nVERIFIED: MMS=(30,30,30,30), and no MMS allocation exists.")


if __name__ == "__main__":
    main()
