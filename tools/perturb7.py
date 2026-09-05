# Rational-perturbation search around 7x17: direction (hR,hC) with zero row/column sums such that
# the perturbed instance has a depth-d certificate at threshold 26 (=T-1).  Then MMS stays 27 and
# best-min < 26  =>  ratio < 26/27.
import sys, numpy as np, itertools, json
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix
R=[8,15,4,9,1,17,4,23,9,1,17,24,3,11,16,22,5]; C=[9,11,6,9,1,16,4,24,9,1,16,25,3,11,15,23,6]
rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13],[14,15],[16,17]]
cols=[[1,4,9],[5,10,12],[2,11],[3,15,17],[8,13],[6,14],[7,16]]
a,b,T,m=3,4,27,17; q=T-1
branch=[int(x) for x in sys.argv[1].split(',')] if len(sys.argv)>1 else [1]   # branching goods (1-based)
D=float(sys.argv[2]) if len(sys.argv)>2 else 3; W=200; NOH=(len(sys.argv)>4 and sys.argv[4]=='noh'); CONT=(len(sys.argv)>4 and sys.argv[4]=='cont')
N=1<<m
def vals(v):
    val=[0]*N
    for S in range(1,N):
        low=S&-S; val[S]=val[S^low]+v[low.bit_length()-1]
    return val
VR,VC=vals(R),vals(C)
def minimal(val,thr):
    isw=[x>=thr for x in val]
    return [S for S in range(N) if isw[S] and all(not isw[S^(1<<g)] for g in range(m) if S>>g&1)]
minR,minC=minimal(VR,T),minimal(VC,T)
tieR=[S for S in range(N) if VR[S]==q]; tieC=[S for S in range(N) if VC[S]==q]
ties=[('R',S) for S in tieR]+[('C',S) for S in tieC]
leaves=[''.join(p) for p in itertools.product('RC',repeat=len(branch))]
# variables: hR(17) hC(17) | z(len ties) | per leaf: w(17), alpha, beta
nh=2*m; nz=len(ties); off=nh+nz; L=m+2; NV=off+len(leaves)*L
lo=np.zeros(NV); hi=np.zeros(NV)
lo[:nh]=-D; hi[:nh]=D; hi[nh:off]=1; hi[off:]=W
integ=np.zeros(NV,int); integ[:nh]=0 if (CONT or NOH) else 1; integ[nh:off]=1
A=lil_matrix((0,NV)); cl=[]; cu=[]; rowsA=[]
def add(co,l,u):
    rowsA.append((co,l,u))
# zero row/col sums
RHO=float(sys.argv[5]) if len(sys.argv)>5 else 0.0
for r in rows: add({g-1:1 for g in r},-RHO,-RHO)
for c in cols: add({m+g-1:1 for g in c},-RHO,-RHO)
zid={t:nh+i for i,t in enumerate(ties)}
# z=1 -> h_t(S) <= -1 :  h(S) + M z <= M-1  with M = D*|S|+1
for (t,S) in ties:
    if NOH: break
    base=0 if t=='R' else m; js=[g for g in range(m) if S>>g&1]; M=D*len(js)+1
    need=1.0 if RHO==0 else RHO*26/27+0.01
    co={base+g:1 for g in js}; co[zid[(t,S)]]=M; add(co,-np.inf,M-need)
def allowed(S,t,leaf):
    # in leaf, good branch[i] goes to type leaf[i]; a t-set may not contain goods given to the other type
    return not any((S>>(g-1))&1 and leaf[i]!=t for i,g in enumerate(branch))
for li,leaf in enumerate(leaves):
    st=off+li*L; ia,ib=st+m,st+m+1
    co={st+g:1 for g in range(m)}; co[ia]=-a; co[ib]=-b; add(co,-np.inf,-1)      # sum w <= a*alpha+b*beta-1
    for t,mins,tie in (('R',minR,tieR),('C',minC,tieC)):
        quota=ia if t=='R' else ib
        for S in mins:
            if allowed(S,t,leaf):
                co={st+g:1 for g in range(m) if S>>g&1}; co[quota]=-1; add(co,0,np.inf)
        for S in tie:
            if allowed(S,t,leaf):
                co={st+g:1 for g in range(m) if S>>g&1}; co[quota]=-1; co[zid[(t,S)]]=W*m; add(co,0,np.inf)  # w(S) >= quota - M z
A=lil_matrix((len(rowsA),NV))
for i,(co,l,u) in enumerate(rowsA):
    for j,v in co.items(): A[i,j]=v
    cl.append(l); cu.append(u)
obj=np.zeros(NV); obj[nh:off]=1   # minimise number of ties turned losing (keeps h small)
print(f'branch {branch} D={D}: leaves {len(leaves)}, ties {nz}, minimal winners {len(minR)}/{len(minC)}, rows {len(rowsA)}, vars {NV}',flush=True)
res=milp(obj,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A.tocsr(),np.array(cl),np.array(cu)),options={'disp':False,'time_limit':float(sys.argv[3]) if len(sys.argv)>3 else 600})
print('status',res.status,res.message)
if res.x is not None and res.status==0:
    x=res.x; hR=[int(round(v)) for v in x[:m]]; hC=[int(round(v)) for v in x[m:2*m]]
    zs=[(t,S) for (t,S) in ties if x[zid[(t,S)]]>0.5]
    print('hR',hR); print('hC',hC); print('ties turned losing',len(zs))
    out={'hR':hR,'hC':hC,'losing_ties':[(t,[g+1 for g in range(m) if S>>g&1]) for t,S in zs],'leaves':{}}
    for li,leaf in enumerate(leaves):
        st=off+li*L; out['leaves'][leaf]={'w':[float(v) for v in x[st:st+m]],'alpha':float(x[st+m]),'beta':float(x[st+m+1])}
    json.dump(out,open(f'perturb7_{"_".join(map(str,branch))}_D{D}.json','w'),indent=1)
