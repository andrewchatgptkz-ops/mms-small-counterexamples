"""Search for the simplest certificates: for each branching good, minimal sum(w) and minimal max(w)."""
from inst import get, check
from analyze import sets_ge
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import sys

def cert_opt(d, X, Y, objective='sum', maxw=60):
    R,C,T,n,a = d['R'],d['C'],d['T'],d['n'],d['a']; b=n-a; m=len(R)
    full=(1<<m)-1
    _, minR, svR = sets_ge(R, m, T)
    _, minC, svC = sets_ge(C, m, T)
    SR = [S for S in minR if S & Y == 0]
    SC = [S for S in minC if S & X == 0]
    nv = m+3  # w, alpha, beta, z(max)
    cost = np.zeros(nv)
    if objective=='sum': cost[:m]=1
    else: cost[m+2]=1
    rows=[]; lo=[]; hi=[]
    for S in SR:
        r=np.zeros(nv);
        for g in range(m):
            if S>>g&1: r[g]=1
        r[m]=-1; rows.append(r); lo.append(0); hi.append(np.inf)
    for S in SC:
        r=np.zeros(nv)
        for g in range(m):
            if S>>g&1: r[g]=1
        r[m+1]=-1; rows.append(r); lo.append(0); hi.append(np.inf)
    r=np.zeros(nv); r[:m]=-1; r[m]=a; r[m+1]=b; rows.append(r); lo.append(1); hi.append(np.inf)
    for g in range(m):
        r=np.zeros(nv); r[g]=-1; r[m+2]=1; rows.append(r); lo.append(0); hi.append(np.inf)
    cons=LinearConstraint(np.array(rows),lo,hi)
    res=milp(cost,constraints=cons,integrality=np.ones(nv),bounds=Bounds(np.zeros(nv),np.full(nv,maxw)))
    if not res.success: return None
    w=[int(round(x)) for x in res.x[:m]]; al=int(round(res.x[m])); be=int(round(res.x[m+1]))
    return w,al,be

if __name__=='__main__':
    name = sys.argv[1] if len(sys.argv)>1 else '6x15'
    d=get(name); check(d); m=len(d['R'])
    for g in range(m):
        out=[]
        for X,Y in [(1<<g,0),(0,1<<g)]:
            r=cert_opt(d,X,Y,'max')
            out.append(r)
        if all(r is not None for r in out):
            print(f'g{g+1}: R-case w={out[0][0]} a={out[0][1]} b={out[0][2]} max={max(out[0][0])} | C-case w={out[1][0]} a={out[1][1]} b={out[1][2]} max={max(out[1][0])}')
