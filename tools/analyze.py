import sys
from inst import get, check
import numpy as np
from scipy.optimize import linprog

def graph(d):
    m = len(d['R'])
    rowof = {g:i for i,r in enumerate(d['rows']) for g in r}
    colof = {g:j for j,c in enumerate(d['cols']) for g in c}
    edges = [(rowof[g], colof[g]) for g in range(m)]
    degr = [len(r) for r in d['rows']]; degc = [len(c) for c in d['cols']]
    return edges, degr, degc

def sets_ge(v, m, T):
    """all subsets with value >= T, and inclusion-minimal ones"""
    sv = [0]*(1<<m)
    for S in range(1,1<<m):
        low = S & -S; g = low.bit_length()-1
        sv[S] = sv[S^low] + v[g]
    ok = [S for S in range(1<<m) if sv[S] >= T]
    okset = set(ok)
    minimal = []
    for S in ok:
        mn = True
        x = S
        while x:
            low = x & -x
            if (S ^ low) in okset: mn = False; break
            x ^= low
        if mn: minimal.append(S)
    return ok, minimal, sv

def frac_packing(d, q=None, minimal_only=True):
    """LP: max sum x_S, S over R-sets (>=q under R) and C-sets, s.t. each good covered <= 1,
    sum over R-sets x = a exactly? We want: can we fractionally pack a R-sets and b C-sets.
    Do: maximize t s.t. sum_R x >= a t, sum_C y >= b t, coverage <= 1. If t<1 -> weight certificate exists."""
    R, C, T, n, a = d['R'], d['C'], d['T'], d['n'], d['a']
    b = n - a
    if q is None: q = T
    m = len(R)
    _, minR, _ = sets_ge(R, m, q)
    _, minC, _ = sets_ge(C, m, q)
    setsR = minR; setsC = minC
    nv = len(setsR) + len(setsC) + 1  # + t
    # variables: x_S (R), y_S (C), t ; maximize t -> minimize -t
    c = np.zeros(nv); c[-1] = -1
    A_ub = []; b_ub = []
    for g in range(m):
        row = np.zeros(nv)
        for i,S in enumerate(setsR):
            if S>>g & 1: row[i] = 1
        for j,S in enumerate(setsC):
            if S>>g & 1: row[len(setsR)+j] = 1
        A_ub.append(row); b_ub.append(1)
    row = np.zeros(nv); row[:len(setsR)] = -1; row[-1] = a; A_ub.append(row); b_ub.append(0)
    row = np.zeros(nv); row[len(setsR):len(setsR)+len(setsC)] = -1; row[-1] = b; A_ub.append(row); b_ub.append(0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=[(0,None)]*nv, method='highs')
    return res, setsR, setsC

if __name__ == '__main__':
    for name in ['4x11','5x13','6x15']:
        d = get(name); check(d)
        edges, degr, degc = graph(d)
        print(f"== {name}: n={d['n']} a={d['a']} T={d['T']} m={len(d['R'])}")
        print('  edges (row,col):', [(r+1,c+1) for r,c in edges])
        print('  row degrees', degr, 'col degrees', degc)
        m = len(d['R'])
        okR, minR, svR = sets_ge(d['R'], m, d['T'])
        okC, minC, svC = sets_ge(d['C'], m, d['T'])
        print('  R-sets >=T:', len(okR), 'minimal', len(minR), '| C-sets >=T:', len(okC), 'minimal', len(minC))
        res, sR, sC = frac_packing(d)
        print('  fractional packing t* =', -res.fun)
        res2, _, _ = frac_packing(d, q=d['T']-1)
        print('  at q=T-1: t* =', -res2.fun)
