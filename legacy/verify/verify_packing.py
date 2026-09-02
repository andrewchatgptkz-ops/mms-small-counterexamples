#!/usr/bin/env python3
"""Compact certificate for two-type instances (a agents of type X, b of type Y), standard library only.
An allocation giving every agent >= q exists  iff  there are a pairwise-disjoint sets with X-value >= q
and b pairwise-disjoint sets with Y-value >= q, all a+b mutually disjoint (leftover goods can be added
to any bundle since valuations are positive). It suffices to look at inclusion-minimal sets.
Usage: python3 verify_packing.py instances/5x13_T29.json          (checks q = T and q = T-1)
"""
import json, sys
from itertools import combinations

def minimal_sets(v, q, m):
    good = [S for S in range(1, 1 << m) if sum(v[j] for j in range(m) if S >> j & 1) >= q]
    gs = set(good)
    return [S for S in good if all((S ^ (1 << j)) not in gs for j in range(m) if S >> j & 1)]

def tuples_disjoint(sets_list, k):
    out = [(S, S) for S in [0]]  # (union, ) seeds handled below
    res = [((), 0)]
    for _ in range(k):
        res = [(t + (S,), u | S) for (t, u) in res for S in sets_list if S & u == 0 and (not t or S > t[-1])]
    return res

def check(inst, q):
    m = inst["goods"]; V = inst["valuations"]
    types = []
    for row in V:
        if not types or row != types[-1][0]: types.append([row, 1])
        else: types[-1][1] += 1
    assert len(types) == 2, "certificate applies to two-type instances only"
    (X, a), (Y, b) = types
    MX = minimal_sets(X, q, m); MY = minimal_sets(Y, q, m)
    xa = tuples_disjoint(MX, a); packs = 0
    yb = tuples_disjoint(MY, b)
    for (_, ux) in xa:
        for (_, uy) in yb:
            if ux & uy == 0: packs += 1
    print(f"q={q}: minimal type-1 sets {len(MX)}, minimal type-2 sets {len(MY)}, "
          f"disjoint {a}-tuples {len(xa)}, disjoint {b}-tuples {len(yb)}, compatible packings {packs}")
    return packs

inst = json.load(open(sys.argv[1]))
T = inst["T"]
pT = check(inst, T)
pT1 = check(inst, T - 1)
print("no allocation reaches MMS everywhere" if pT == 0 else "!! MMS allocation exists")
print(f"threshold {T-1} achievable: {'yes' if pT1 > 0 else 'NO'}")
