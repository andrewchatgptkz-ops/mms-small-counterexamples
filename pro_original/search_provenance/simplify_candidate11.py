from itertools import product
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix

R0=np.array([15,22,23,16,13,31,39,21,1,55,4],dtype=int)
C0=np.array([9,21,25,19,4,33,50,20,1,56,2],dtype=int)
m=11
rows=[{0,1,2},{3,4,5},{6,7},{8,9,10}]
cols=[{0,6,8},{1,3,7},{4,9},{2,5,10}]

badR=set();badC=set(); counts=[0,0,0,0]
for ass in product(range(4),repeat=m):
    masks=[0,0,0,0]
    vals=[0,0,0,0]
    for g,a in enumerate(ass):
        masks[a]|=1<<g
        vals[a]+= (R0[g] if a<2 else C0[g])
    losers=[a for a in range(4) if vals[a]<=59]
    assert losers
    # Pick the most strongly losing current bundle.
    a=min(losers,key=lambda x:(vals[x]-60, masks[x].bit_count(),x))
    counts[a]+=1
    (badR if a<2 else badC).add(masks[a])
print('badR',len(badR),'badC',len(badC),'counts',counts, flush=True)

Tidx=2*m;nvar=2*m+1
ncon=8+len(badR)+len(badC)
A=lil_matrix((ncon,nvar),dtype=float);lo=np.full(ncon,-np.inf);hi=np.full(ncon,np.inf)
r=0
for b in rows:
    for g in b:A[r,g]=1
    A[r,Tidx]=-1;lo[r]=hi[r]=0;r+=1
for b in cols:
    for g in b:A[r,m+g]=1
    A[r,Tidx]=-1;lo[r]=hi[r]=0;r+=1
for mask in sorted(badR):
    for g in range(m):
        if mask>>g&1:A[r,g]=1
    A[r,Tidx]=-1;hi[r]=-1;r+=1
for mask in sorted(badC):
    for g in range(m):
        if mask>>g&1:A[r,m+g]=1
    A[r,Tidx]=-1;hi[r]=-1;r+=1
assert r==ncon
c=np.zeros(nvar);c[Tidx]=1;c[:2*m]=1e-4
integrality=np.ones(nvar,dtype=np.int8)
lb=np.zeros(nvar);ub=np.full(nvar,60.0);lb[Tidx]=1
res=milp(c,integrality=integrality,bounds=Bounds(lb,ub),constraints=LinearConstraint(csr_matrix(A),lo,hi),options={'time_limit':120,'mip_rel_gap':0.0,'disp':True})
print(res.status,res.message,res.fun)
if res.x is not None:
    x=np.rint(res.x).astype(int)
    print('T',x[Tidx]);print('R',x[:m].tolist());print('C',x[m:2*m].tolist())
