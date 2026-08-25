#!/usr/bin/env python3
"""Exact structural verifier for the two-type 11-good construction.

Agents 1,2 have valuation R and agents 3,4 have valuation C.  An MMS
allocation exists exactly if there are two mutually disjoint R-threshold
bundles and two mutually disjoint C-threshold bundles, all four disjoint.
Every threshold bundle contains an inclusion-minimal threshold bundle, so it
suffices to enumerate minimal bundles and disjoint pairs of them.
"""

R = [7, 12, 11, 8, 6, 16, 21, 9, 1, 28, 1]
C = [6, 10, 13, 10, 4, 15, 23, 10, 1, 26, 2]
T = 30
M = len(R)


def subset_values(row):
    out = [0] * (1 << M)
    for mask in range(1, 1 << M):
        bit = mask & -mask
        good = bit.bit_length() - 1
        out[mask] = out[mask ^ bit] + row[good]
    return out


def minimal_threshold_bundles(row):
    val = subset_values(row)
    ans = []
    for mask in range(1, 1 << M):
        if val[mask] < T:
            continue
        if all(val[mask ^ (1 << g)] < T
               for g in range(M) if mask & (1 << g)):
            ans.append(mask)
    return ans


def disjoint_pairs(bundles):
    ans = []
    for i, left in enumerate(bundles):
        for right in bundles[i + 1:]:
            if not (left & right):
                ans.append((left, right, left | right))
    return ans


r_min = minimal_threshold_bundles(R)
c_min = minimal_threshold_bundles(C)
r_pairs = disjoint_pairs(r_min)
c_pairs = disjoint_pairs(c_min)

compatible = []
for r1, r2, r_union in r_pairs:
    for c1, c2, c_union in c_pairs:
        if not (r_union & c_union):
            compatible.append((r1, r2, c1, c2))

print(f"minimal R-threshold bundles: {len(r_min)}")
print(f"minimal C-threshold bundles: {len(c_min)}")
print(f"disjoint R-pairs: {len(r_pairs)}")
print(f"disjoint C-pairs: {len(c_pairs)}")
print(f"four-way compatible choices: {len(compatible)}")

assert len(r_min) == 54
assert len(c_min) == 54
assert len(r_pairs) == 448
assert len(c_pairs) == 436
assert not compatible
print("VERIFIED: no two R-threshold bundles and two C-threshold bundles can be pairwise disjoint.")
