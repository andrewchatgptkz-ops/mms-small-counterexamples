#!/usr/bin/env python3
"""Exact verifier, standard library only.
Usage: python3 verify_exhaustive.py instances/4x11_T30.json
1. MMS of every agent by enumerating all unordered partitions of the goods into n nonempty bundles.
2. All n^m complete allocations; counts those giving every agent >= her MMS; reports max_A min_i v_i(A_i).
"""
import json, sys
from itertools import product

def partitions(M, N):
    lab = [0]*M
    def rec(g, used):
        if g == M:
            if used == N: yield tuple(lab)
            return
        if M-g < N-used: return
        for b in range(used):
            lab[g] = b; yield from rec(g+1, used)
        if used < N:
            lab[g] = used; yield from rec(g+1, used+1)
    yield from rec(0, 0)

def mms(row, N):
    best, count = -1, 0
    for p in partitions(len(row), N):
        count += 1
        s = [0]*N
        for g, b in enumerate(p): s[b] += row[g]
        best = max(best, min(s))
    return best, count

def main(path):
    inst = json.load(open(path))
    V, N, M = inst["valuations"], inst["agents"], inst["goods"]
    assert len(V) == N and all(len(r) == M for r in V)
    print("instance:", inst["name"])
    m = []
    for i, r in enumerate(V):
        b, c = mms(r, N); m.append(b)
        print(f"agent {i+1}: sum={sum(r)} MMS={b} (partitions enumerated: {c})")
    ok, best = 0, -1
    for a in product(range(N), repeat=M):
        u = [0]*N
        for g, o in enumerate(a): u[o] += V[o][g]
        if all(u[i] >= m[i] for i in range(N)): ok += 1
        best = max(best, min(u))
    print(f"allocations enumerated: {N**M}")
    print(f"MMS allocations: {ok}")
    print(f"max over allocations of min_i v_i(A_i): {best}")
    print("VERDICT:", "NO MMS ALLOCATION" if ok == 0 else "MMS ALLOCATION EXISTS")

if __name__ == "__main__":
    main(sys.argv[1])
