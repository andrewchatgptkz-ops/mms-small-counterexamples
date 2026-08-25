from itertools import product
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix

m=11
rows=[{0,1,2},{3,4,5},{6,7},{8,9,10}]
cols=[{0,6,8},{1,3,7},{4,9},{2,5,10}]
R=np.array([11,15,16,12,10,20,28,14,1,40,1],dtype=int)
C=np.array([7,14,18,14,4,22,34,14,1,38,2],dtype=int)
T=42

def collect(R,C,T):
    badR=set();badC=set();
    for ass in product(range(4),repeat=m):
        masks=[0,0,0,0];vals=[0,0,0,0]
        for g,a in enumerate(ass):masks[a]|=1<<g;vals[a]+=R[g] if a<2 else C[g]
        losers=[a for a in range(4) if vals[a]<T]
        if not losers: raise RuntimeError('not counterexample')
        # Maximize relative deficit; then prefer smaller mask.
        a=min(losers,key=lambda x:(vals[x]-T,masks[x].bit_count(),x))
        (badR if a<2 else badC).add(masks[a])
    return badR,badC

def solve(badR,badC,Tub):
    tid=2*m;n=tid+1;nr=8+len(badR)+len(badC)
    A=lil_matrix((nr,n));lo=np.full(nr,-np.inf);hi=np.full(nr,np.inf);r=0
    for b in rows:
        for g in b:A[r,g]=1
        A[r,tid]=-1;lo[r]=hi[r]=0;r+=1
    for b in cols:
        for g in b:A[r,m+g]=1
        A[r,tid]=-1;lo[r]=hi[r]=0;r+=1
    for mask in badR:
        for g in range(m):
            if mask>>g&1:A[r,g]=1
        A[r,tid]=-1;hi[r]=-1;r+=1
    for mask in badC:
        for g in range(m):
            if mask>>g&1:A[r,m+g]=1
        A[r,tid]=-1;hi[r]=-1;r+=1
    c=np.zeros(n);c[tid]=1;c[:tid]=1e-5
    lb=np.zeros(n);lb[tid]=1;ub=np.full(n,Tub)
    z=milp(c,integrality=np.ones(n,dtype=np.int8),bounds=Bounds(lb,ub),constraints=LinearConstraint(csr_matrix(A),lo,hi),options={'mip_rel_gap':0.0,'time_limit':60})
    if z.x is None:return None
    x=np.rint(z.x).astype(int);return x[:m],x[m:2*m],x[tid]

for it in range(8):
    print('ITER',it,'T',T,'R',R.tolist(),'C',C.tolist(),flush=True)
    br,bc=collect(R,C,T);print('bad',len(br),len(bc),flush=True)
    sol=solve(br,bc,T)
    if sol is None: print('infeasible');break
    R2,C2,T2=sol;print('sol',T2,R2.tolist(),C2.tolist(),flush=True)
    if T2==T and np.array_equal(R2,R) and np.array_equal(C2,C):break
    R,C,T=R2,C2,int(T2)
