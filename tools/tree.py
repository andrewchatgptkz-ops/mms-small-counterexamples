"""Decision-tree proof search: branch on good -> R-type / C-type.
Node relaxation: fractional packing LP over minimal R-sets (within X∪U) and C-sets (within Y∪U),
coverage <= 1, sum x >= a t, sum y >= b t, maximize t. t* < 1 => node refuted (dual = weights)."""
from inst import get, check
from analyze import sets_ge
import numpy as np
from scipy.optimize import linprog
import sys, functools

name = sys.argv[1] if len(sys.argv)>1 else '6x15'
d = get(name); check(d)
R,C,T,n,a = d['R'],d['C'],d['T'],d['n'],d['a']; b=n-a; m=len(R)
full=(1<<m)-1
_, minR, svR = sets_ge(R, m, T)
_, minC, svC = sets_ge(C, m, T)

def lp(X, Y):
    """X: goods fixed to R-type, Y: fixed to C-type. Returns (t*, dual info)."""
    allowR = full ^ Y; allowC = full ^ X
    SR = [S for S in minR if S & ~allowR == 0]
    SC = [S for S in minC if S & ~allowC == 0]
    if len(SR) < 1 or len(SC) < 1: return 0.0, None, SR, SC
    nv = len(SR)+len(SC)+1
    c = np.zeros(nv); c[-1] = -1
    A=[]; bb=[]
    for g in range(m):
        row=np.zeros(nv)
        for i,S in enumerate(SR):
            if S>>g&1: row[i]=1
        for j,S in enumerate(SC):
            if S>>g&1: row[len(SR)+j]=1
        A.append(row); bb.append(1)
    row=np.zeros(nv); row[:len(SR)]=-1; row[-1]=a; A.append(row); bb.append(0)
    row=np.zeros(nv); row[len(SR):len(SR)+len(SC)]=-1; row[-1]=b; A.append(row); bb.append(0)
    res = linprog(c, A_ub=np.array(A), b_ub=np.array(bb), bounds=[(0,None)]*nv, method='highs')
    return -res.fun, res, SR, SC

def show(S): return [g+1 for g in range(m) if S>>g&1]

leaves=[]
def solve(X, Y, depth, path):
    t, res, SR, SC = lp(X, Y)
    if t < 1 - 1e-9:
        leaves.append((path, t, X, Y))
        return 1
    if depth > 6:
        leaves.append((path, None, X, Y)); return 1
    # choose branching good: minimize max(child t)
    best=None
    U = full ^ X ^ Y
    for g in range(m):
        if not (U>>g&1): continue
        t1,_,_,_ = lp(X | 1<<g, Y)
        t2,_,_,_ = lp(X, Y | 1<<g)
        score = max(t1,t2) + 0.01*(t1+t2)
        if best is None or score < best[0]: best=(score,g,t1,t2)
    _,g,t1,t2 = best
    sz = solve(X | 1<<g, Y, depth+1, path+[(g+1,'R')])
    sz += solve(X, Y | 1<<g, depth+1, path+[(g+1,'C')])
    return sz

sz = solve(0,0,0,[])
print(name, 'leaves:', sz)
for path,t,X,Y in leaves:
    print('  ', ' '.join(f'{g}{s}' for g,s in path), ' t*=', None if t is None else round(t,3))
