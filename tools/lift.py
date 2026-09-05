"""Try to lift a certificate of the base instance to the subdivided instance keeping old weights (scaled)."""
from inst import get, check
from analyze import sets_ge
from subdiv_scan import subdivide
from verify_cert import check_case
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
import sys

def cert_fixed(d, X, Y, fixed, maxw=200):
    """fixed: dict good->weight (forced). Others free. Minimize max free weight."""
    R,C,T,n,a = d['R'],d['C'],d['T'],d['n'],d['a']; b=n-a; m=len(R)
    _, minR, _ = sets_ge(R, m, T); _, minC, _ = sets_ge(C, m, T)
    SR=[S for S in minR if S & Y==0]; SC=[S for S in minC if S & X==0]
    nv=m+3
    cost=np.zeros(nv); cost[m+2]=1
    rows=[];lo=[];hi=[]
    for S in SR:
        r=np.zeros(nv)
        for g in range(m):
            if S>>g&1: r[g]=1
        r[m]=-1; rows.append(r); lo.append(0); hi.append(np.inf)
    for S in SC:
        r=np.zeros(nv)
        for g in range(m):
            if S>>g&1: r[g]=1
        r[m+1]=-1; rows.append(r); lo.append(0); hi.append(np.inf)
    r=np.zeros(nv); r[:m]=-1; r[m]=a; r[m+1]=b; rows.append(r); lo.append(1); hi.append(np.inf)
    lb=np.zeros(nv); ub=np.full(nv,maxw)
    for g,wv in fixed.items(): lb[g]=ub[g]=wv
    for g in range(m):
        if g not in fixed:
            r=np.zeros(nv); r[g]=-1; r[m+2]=1; rows.append(r); lo.append(0); hi.append(np.inf)
    res=milp(cost,constraints=LinearConstraint(np.array(rows),lo,hi),integrality=np.ones(nv),bounds=Bounds(lb,ub))
    if not res.success: return None
    w=[int(round(v)) for v in res.x[:m]]; return w,int(round(res.x[m])),int(round(res.x[m+1]))

if __name__=='__main__':
    d=get('5x13'); check(d)
    base_R = ([2,6,3,4,1,6,3,9,3,2,6,9,3], 11, 12)   # branch g1, R-case
    base_C = ([10,19,9,16,3,23,9,33,15,4,23,34,8], 42, 41)  # branch g1, C-case
    e=5  # good g6 (0-based 5)
    d2=subdivide(d,e,12,12); d2['n']=6; d2['a']=3; check(d2)
    print('subdivided instance R=',d2['R'],'C=',d2['C'])
    for lam in [1,2,3,4]:
        for tag,(w,al,be),X,Y in [('R-case',base_R,1,0),('C-case',base_C,0,1)]:
            fixed={g:lam*w[g] for g in range(13) if g!=e}
            r=cert_fixed(d2,X,Y,fixed)
            if r:
                ok,*rest=check_case(d2,r[0],r[1],r[2],X,Y)
                print(f'lambda={lam} {tag}: lifted w={r[0]} alpha={r[1]} beta={r[2]} verified={ok}  (base alpha,beta scaled: {lam*al},{lam*be})')
            else:
                print(f'lambda={lam} {tag}: no lifting with old weights fixed')
