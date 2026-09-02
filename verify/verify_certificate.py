#!/usr/bin/env python3
"""
Human-auditable non-existence certificates for the two-type grid MMS counterexamples
(4 agents x 11 goods, 5 x 13, 6 x 15).  Standard library only.

Setting.  a agents value goods by R, b agents by C (n = a+b).  Rows of the grid sum to T under R,
columns sum to T under C, so MMS = T for everyone.  An allocation giving everyone >= T exists iff
there are a pairwise-disjoint sets S with R(S) >= T and b pairwise-disjoint sets S with C(S) >= T,
all mutually disjoint ("packing").

Certificate (one disjunction + two weightings).  Fix a good g*.  In any allocation g* goes to an
R-agent or to a C-agent.
  Case R (g* with an R-agent): no C-bundle contains g*.  Weights w >= 0 on goods such that
      every S with R(S) >= T has w(S) >= alpha,
      every S with C(S) >= T and g* not in S has w(S) >= beta,
      a*alpha + b*beta > sum(w).
    Then the a R-bundles and b C-bundles, being disjoint, would carry weight >= a*alpha + b*beta
    > sum(w): contradiction.
  Case C (g* with a C-agent): symmetric, with R-sets avoiding g*.
This script checks the three conditions of each case by brute force over ALL 2^m subsets.
"""
import sys

INSTANCES = {
  '4x11': dict(a=2, b=2, T=30,
      R=[7,12,11,8,6,16,21,9,1,28,1],
      C=[6,10,13,10,4,15,23,10,1,26,2],
      gstar=2,
      caseR=dict(w=[7,10,13,9,6,15,22,9,2,25,3], alpha=30, beta=31),
      caseC=dict(w=[4,6,7,6,4,10,13,7,2,16,2], alpha=20, beta=19)),
  '5x13': dict(a=2, b=3, T=29,
      R=[8,16,5,10,1,18,5,24,9,2,18,25,4],
      C=[9,12,7,10,1,15,7,26,10,1,17,27,3],
      gstar=1,
      caseR=dict(w=[2,6,3,4,1,6,3,9,3,2,6,9,3], alpha=11, beta=12),
      caseC=dict(w=[10,19,9,16,3,23,9,33,15,4,23,34,8], alpha=42, beta=41)),
  '6x15': dict(a=3, b=3, T=28,
      R=[7,16,5,9,1,18,4,24,9,1,18,25,3,11,17],
      C=[8,12,6,10,1,16,7,25,10,1,16,26,3,12,15],
      gstar=1,
      caseR=dict(w=[5,11,6,7,3,12,6,17,7,3,12,17,6,11,11], alpha=22, beta=23),
      caseC=dict(w=[8,17,8,14,3,20,8,29,14,3,20,30,7,17,20], alpha=37, beta=36)),
  '6x15-pre-decrement-T29': dict(a=3, b=3, T=29,
      R=[8,16,5,10,1,18,5,24,9,2,18,25,4,12,17],
      C=[9,12,7,10,1,17,7,26,10,1,17,27,3,12,15],
      gstar=1,
      caseR=dict(w=[4,9,5,6,2,10,5,14,5,3,10,14,5,9,9], alpha=18, beta=19),
      caseC=dict(w=[11,21,10,17,4,25,10,36,17,4,25,37,9,21,25], alpha=46, beta=45)),
  '7x17': dict(a=3, b=4, T=27,
      R=[8,15,4,9,1,17,4,23,9,1,17,24,3,11,16,22,5],
      C=[9,11,6,9,1,16,4,24,9,1,16,25,3,11,15,23,6],
      gstar=1,
      caseR=dict(w=[5,11,6,7,3,12,6,17,7,3,12,17,6,11,11,17,6], alpha=22, beta=23),
      caseC=dict(w=[17,30,14,24,6,36,14,52,24,6,36,53,13,30,36,51,15], alpha=66, beta=65)),
}

# Chain ("universal") certificates: ONE weight vector serves n = 5, 6, 7 (first m entries), same branching good g1.
# Case R: w_R with alpha = 22, beta = 23 for all three; sum grows by exactly beta per step (new goods 17 + 6), margin stays 1.
# Case C: w_C with alpha = 176, beta = 172 (n=5,6) / 173 (n=7).
CHAIN = dict(
    caseR=dict(w=[5,11,6,7,3,12,6,17,7,3,12,17,6,11,11,17,6], ab={'5x13':(22,23),'6x15':(22,23),'7x17':(22,23)}),
    caseC=dict(w=[45,80,38,64,16,96,38,138,64,16,96,141,35,80,96,137,39], ab={'5x13':(176,172),'6x15':(176,172),'7x17':(176,173)}),
)

def check_case(inst, case, side):
    R, C, T, a, b = inst['R'], inst['C'], inst['T'], inst['a'], inst['b']
    m = len(R); gs = inst['gstar'] - 1
    w, alpha, beta = case['w'], case['alpha'], case['beta']
    assert len(w) == m and min(w) >= 0
    minR = minC = None
    for S in range(1 << m):
        rs = cs = ws = 0; has = (S >> gs) & 1
        for g in range(m):
            if (S >> g) & 1:
                rs += R[g]; cs += C[g]; ws += w[g]
        # side 'R': g* is with an R-agent -> C-sets avoid g*.  side 'C': R-sets avoid g*.
        if rs >= T and not (side == 'C' and has):
            minR = ws if minR is None else min(minR, ws)
        if cs >= T and not (side == 'R' and has):
            minC = ws if minC is None else min(minC, ws)
    ok = (minR >= alpha) and (minC >= beta) and (a*alpha + b*beta > sum(w))
    return ok, minR, minC, sum(w), a*alpha + b*beta

if __name__ == '__main__':
    names = sys.argv[1:] or list(INSTANCES)
    allok = True
    for name in names:
        inst = INSTANCES[name]
        R, C, T, a, b = inst['R'], inst['C'], inst['T'], inst['a'], inst['b']
        assert sum(R) == (a+b)*T and sum(C) == (a+b)*T
        print(f'{name}: n={a+b} ({a}+{b}), m={len(R)}, T={T}, branching good g{inst["gstar"]}')
        for side in ('R', 'C'):
            ok, mr, mc, sw, need = check_case(inst, inst['case'+side], side)
            print(f'  case {side}: min w(R-set)={mr} (>= alpha={inst["case"+side]["alpha"]}), '
                  f'min w(C-set)={mc} (>= beta={inst["case"+side]["beta"]}), sum w={sw} < {need}: {"OK" if ok else "FAIL"}')
            allok &= ok
    print('ALL CERTIFICATES VALID' if allok else 'SOME CERTIFICATE FAILED')
    if not sys.argv[1:]:
        print('Chain certificates (one weight vector for n = 5, 6, 7):')
        for side in ('R', 'C'):
            ch = CHAIN['case'+side]
            for name, (al, be) in ch['ab'].items():
                inst = INSTANCES[name]; m = len(inst['R'])
                ok, mr, mc, sw, need = check_case(inst, dict(w=ch['w'][:m], alpha=al, beta=be), side)
                print(f'  case {side} {name}: alpha={al} beta={be} min w(R)={mr} min w(C)={mc} sum={sw} < {need}: {"OK" if ok else "FAIL"}')
                allok &= ok
        print('CHAIN CERTIFICATES VALID' if allok else 'CHAIN FAILED')
