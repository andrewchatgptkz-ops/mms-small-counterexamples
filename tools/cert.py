"""Given fixed good assignments, find small integer weight certificate:
w_g >= 0 integer, alpha, beta integers; w(S) >= alpha for every allowed minimal R-set,
w(S) >= beta for every allowed minimal C-set; a*alpha + b*beta >= sum(w) + 1.
Then no packing of a R-sets + b C-sets (disjoint) exists in the region."""
from inst import get, check
from analyze import sets_ge
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import sys

def cert(d, X, Y, maxw=60, verbose=True):
    R,C,T,n,a = d['R'],d['C'],d['T'],d['n'],d['a']; b=n-a; m=len(R)
    full=(1<<m)-1
    _, minR, svR = sets_ge(R, m, T)
    _, minC, svC = sets_ge(C, m, T)
    allowR = full ^ Y; allowC = full ^ X
    SR = [S for S in minR if S & ~allowR == 0]
    SC = [S for S in minC if S & ~allowC == 0]
    # variables: w_0..w_{m-1}, alpha, beta
    nv = m+2
    cost = np.zeros(nv); cost[:m] = 1  # minimize total weight
    rows=[]; lo=[]; hi=[]
    for S in SR:
        r=np.zeros(nv)
        for g in range(m):
            if S>>g&1: r[g]=1
        r[m] = -1; rows.append(r); lo.append(0); hi.append(np.inf)
    for S in SC:
        r=np.zeros(nv)
        for g in range(m):
            if S>>g&1: r[g]=1
        r[m+1] = -1; rows.append(r); lo.append(0); hi.append(np.inf)
    r=np.zeros(nv); r[:m]=-1; r[m]=a; r[m+1]=b; rows.append(r); lo.append(1); hi.append(np.inf)
    cons = LinearConstraint(np.array(rows), lo, hi)
    bounds = Bounds(np.zeros(nv), np.full(nv, maxw))
    res = milp(cost, constraints=cons, integrality=np.ones(nv), bounds=bounds)
    if not res.success:
        if verbose: print('no certificate', res.message)
        return None
    w = [int(round(x)) for x in res.x[:m]]; al=int(round(res.x[m])); be=int(round(res.x[m+1]))
    if verbose:
        print(f'X={[g+1 for g in range(m) if X>>g&1]} Y={[g+1 for g in range(m) if Y>>g&1]}')
        print(f'  weights: {w}  alpha={al} beta={be}  sum(w)={sum(w)}  a*alpha+b*beta={a*al+b*be}')
        print(f'  allowed R-sets {len(SR)}, C-sets {len(SC)}')
    return w, al, be, SR, SC

if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv)>1 else '6x15'
    d = get(name); check(d)
    m=len(d['R'])
    g = int(sys.argv[2]) if len(sys.argv)>2 else 9
    cert(d, 1<<(g-1), 0)
    cert(d, 0, 1<<(g-1))
