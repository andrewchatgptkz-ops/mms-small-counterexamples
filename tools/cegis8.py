"""n=8 constructor: case R enforced by the fixed chain weights (linear knapsack cuts, lazily),
case C (g1 with a C-agent) enforced by CEGIS with a packing oracle (subset-DP with R-agents valuing g1 at 0)
and disjunctive cuts: for each found allocation, at least one of its 8 bundles must fall below T."""
import sys, json, time, subprocess
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import construct8 as c8

T, m = c8.T, c8.m
edge = int(sys.argv[1]) - 1; x = int(sys.argv[2]); A_R = int(sys.argv[3]) if len(sys.argv)>3 else 4; B_C = 8 - A_R; QUOTA = 22 if A_R == 4 else 23
rows, cols = c8.pattern(edge)
wR = c8.wR7 + [x, QUOTA - x]

def oracle(Rv, Cv):
    """allocation with all >= T where g1 is NOT useful to R-agents (R value of g1 zeroed) -> covers case C."""
    R0 = Rv[:]; R0[0] = 0
    vals = [R0]*A_R + [Cv]*B_C
    inp = f"8 {m} {T}\n" + "\n".join(' '.join(map(str, v)) for v in vals) + "\n"
    out = subprocess.run(['./dp_alloc'], input=inp, capture_output=True, text=True).stdout.strip()
    if out == 'none': return None
    masks = [int(t) for t in out.split()]
    return masks

def build_and_solve(kcuts, pcuts):
    # variables: R(19), C(19), d(34) L1 aux, z (one per bundle per packing cut)
    nz = sum(len(p) for p in pcuts)
    nv = 2*m + 34 + nz
    cost = np.zeros(nv); cost[2*m:2*m+34] = 1
    A = []; lo = []; hi = []
    def row(vec, l, h): A.append(vec); lo.append(l); hi.append(h)
    for r in rows:
        v = np.zeros(nv); v[[g for g in r]] = 1; row(v, T, T)
    for c in cols:
        v = np.zeros(nv); v[[m+g for g in c]] = 1; row(v, T, T)
    for g in range(17):
        v = np.zeros(nv); v[g] = 1; v[2*m+g] = -1; row(v, -np.inf, c8.R7[g])
        v = np.zeros(nv); v[g] = 1; v[2*m+g] = 1; row(v, c8.R7[g], np.inf)
        v = np.zeros(nv); v[m+g] = 1; v[2*m+17+g] = -1; row(v, -np.inf, c8.C7[g])
        v = np.zeros(nv); v[m+g] = 1; v[2*m+17+g] = 1; row(v, c8.C7[g], np.inf)
    for kind, mask in kcuts:
        v = np.zeros(nv)
        for g in range(m):
            if mask >> g & 1: v[(0 if kind == 0 else m) + g] = 1
        row(v, -np.inf, T-1)
    zi = 2*m + 34
    for p in pcuts:  # p: list of (kind, mask)
        v = np.zeros(nv); v[zi:zi+len(p)] = 1; row(v, 1, np.inf)
        for j, (kind, mask) in enumerate(p):
            v = np.zeros(nv); size = 0
            for g in range(m):
                if mask >> g & 1: v[(0 if kind == 0 else m) + g] = 1; size += 1
            M = (T-1) * size  # value <= T-1 + M*(1-z)  <=>  value + M*z <= T-1+M
            v[zi+j] = M; row(v, -np.inf, T-1+M)
        zi += len(p)
    lb = np.zeros(nv); lb[:2*m] = 1; ub = np.full(nv, T-1.0); ub[2*m:2*m+34] = 100; ub[2*m+34:] = 1
    res = milp(cost, constraints=LinearConstraint(np.array(A), lo, hi), integrality=np.ones(nv), bounds=Bounds(lb, ub))
    if not res.success: return None, None
    return [int(round(v)) for v in res.x[:m]], [int(round(v)) for v in res.x[m:2*m]]

kcuts = []; kseen = set(); pcuts = []
t0 = time.time()
for it in range(400):
    sol = build_and_solve(kcuts, pcuts)
    if sol[0] is None:
        print(f'edge g{edge+1} x={x}: INFEASIBLE at iter {it} (kcuts {len(kcuts)}, pcuts {len(pcuts)})'); break
    Rv, Cv = sol
    viol = c8.violated(Rv, Cv, wR, None, False)
    newk = 0
    for k, arr in zip([0, 1], viol):
        for s in sorted(arr.tolist(), key=lambda s: bin(s).count('1'))[:400]:
            if (k, s) not in kseen: kseen.add((k, s)); kcuts.append((k, s)); newk += 1
    if newk:
        print(f'iter {it}: +{newk} knapsack cuts (total {len(kcuts)}) [{time.time()-t0:.0f}s]', flush=True); continue
    masks = oracle(Rv, Cv)
    if masks is None:
        print(f'HIT edge g{edge+1} x={x} iter {it}: R={Rv} C={Cv} kcuts={len(kcuts)} pcuts={len(pcuts)} [{time.time()-t0:.0f}s]')
        json.dump(dict(edge=edge+1, x=x, R=Rv, C=Cv, rows=rows, cols=cols, wR=wR), open(f'hit8_g{edge+1}_x{x}_a{A_R}.json', 'w'))
        break
    p = [(0, mk) for mk in masks[:A_R]] + [(1, mk) for mk in masks[A_R:]]
    pcuts.append(p)
    print(f'iter {it}: packing cut #{len(pcuts)} bundles={[bin(mk).count("1") for mk in masks]} [{time.time()-t0:.0f}s]', flush=True)
