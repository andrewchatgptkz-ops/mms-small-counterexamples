"""Instances of the two-type grid family. Goods are 1-indexed in docs; here 0-indexed."""
from itertools import combinations

INST = {}

# 4x11, T=30, 2+2. Pattern reconstructed below from rows/cols (must verify sums).
INST['4x11'] = dict(
    n=4, a=2, T=30,
    R=[7,12,11,8,6,16,21,9,1,28,1],
    C=[6,10,13,10,4,15,23,10,1,26,2],
    rows=None, cols=None)

INST['5x13'] = dict(
    n=5, a=2, T=29,
    R=[8,16,5,10,1,18,5,24,9,2,18,25,4],
    C=[9,12,7,10,1,15,7,26,10,1,17,27,3],
    rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13]],
    cols=[[1,4,9],[5,10,12],[2,11],[3,6,7],[8,13]])

INST['6x15'] = dict(
    n=6, a=3, T=28,
    R=[7,16,5,9,1,18,4,24,9,1,18,25,3,11,17],
    C=[8,12,6,10,1,16,7,25,10,1,16,26,3,12,15],
    rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13],[14,15]],
    cols=[[1,4,9],[5,10,12],[2,11],[3,7,15],[8,13],[6,14]])

INST['7x17'] = dict(
    n=7, a=3, T=27,
    R=[8,15,4,9,1,17,4,23,9,1,17,24,3,11,16,22,5],
    C=[9,11,6,9,1,16,4,24,9,1,16,25,3,11,15,23,6],
    rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13],[14,15],[16,17]],
    cols=[[1,4,9],[5,10,12],[2,11],[3,15,17],[8,13],[6,14],[7,16]])

def find_pattern(R, C, T, n):
    """Find row/col partitions of goods with sums T (for 4x11 where pattern not recorded)."""
    m = len(R)
    def parts(vals, idx, k):
        # all partitions of idx into k blocks each summing to T
        if not idx:
            if k == 0: yield []
            return
        if k == 0: return
        first = idx[0]; rest = idx[1:]
        for r in range(0, len(rest)+1):
            for comb in combinations(rest, r):
                blk = (first,)+comb
                if sum(vals[g] for g in blk) == T:
                    remaining = [g for g in rest if g not in comb]
                    for p in parts(vals, remaining, k-1):
                        yield [list(blk)] + p
    rows = list(parts(R, list(range(m)), n))
    cols = list(parts(C, list(range(m)), n))
    return rows, cols

def get(name):
    d = dict(INST[name])
    if d['rows'] is None:
        rows, cols = find_pattern(d['R'], d['C'], d['T'], d['n'])
        d['row_options'] = rows; d['col_options'] = cols
        d['rows'] = rows[0]; d['cols'] = cols[0]
    else:
        d['rows'] = [[g-1 for g in r] for r in d['rows']]
        d['cols'] = [[g-1 for g in c] for c in d['cols']]
    return d

def check(d):
    R, C, T, n = d['R'], d['C'], d['T'], d['n']
    m = len(R)
    assert sum(R) == n*T and sum(C) == n*T, (sum(R), sum(C), n*T)
    assert sorted(g for r in d['rows'] for g in r) == list(range(m))
    assert sorted(g for c in d['cols'] for g in c) == list(range(m))
    for r in d['rows']: assert sum(R[g] for g in r) == T, r
    for c in d['cols']: assert sum(C[g] for g in c) == T, c
    assert max(R) < T and max(C) < T
    return True

def subset_dp_maxmin(vals_list, m):
    """max over allocations of min_i v_i(A_i). vals_list: one valuation per agent."""
    from functools import lru_cache
    n = len(vals_list)
    full = (1<<m)-1
    # precompute set values
    sv = []
    for v in vals_list:
        arr = [0]*(1<<m)
        for S in range(1, 1<<m):
            low = S & -S; g = low.bit_length()-1
            arr[S] = arr[S ^ low] + v[g]
        sv.append(arr)
    import sys
    sys.setrecursionlimit(10000)
    # F_i(S): best min for agents i..n-1 sharing set S
    F = sv[n-1][:]  # last agent takes everything
    for i in range(n-2, -1, -1):
        G = [0]*(1<<m)
        svi = sv[i]
        for S in range(1<<m):
            best = 0
            B = S
            while True:
                val = min(svi[B], F[S ^ B])
                if val > best: best = val
                if B == 0: break
                B = (B-1) & S
            G[S] = best
        F = G
    return F[full]

if __name__ == '__main__':
    for name in ['4x11','5x13','6x15']:
        d = get(name); check(d)
        print(name, 'ok; rows', [[g+1 for g in r] for r in d['rows']], 'cols', [[g+1 for g in c] for c in d['cols']])
        if 'row_options' in d:
            print('  row partitions found:', len(d['row_options']), 'col partitions:', len(d['col_options']))
