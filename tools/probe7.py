# random probe: K*v + h with h in {-1,0,1}^17, zero row/col sums, K=2,3: any with no allocation >= 26K ?
import random, subprocess, sys
R=[8,15,4,9,1,17,4,23,9,1,17,24,3,11,16,22,5]; C=[9,11,6,9,1,16,4,24,9,1,16,25,3,11,15,23,6]
rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13],[14,15],[16,17]]
cols=[[1,4,9],[5,10,12],[2,11],[3,15,17],[8,13],[6,14],[7,16]]
def randdir(groups):
    h=[0]*17
    for g in groups:
        k=len(g)
        if k==2:
            s=random.choice([-1,0,1]); h[g[0]-1]=s; h[g[1]-1]=-s
        else:
            p=random.choice([(0,0,0),(1,-1,0),(1,0,-1),(-1,1,0),(0,1,-1),(-1,0,1),(0,-1,1)])
            for x,v in zip(g,p): h[x-1]=v
    return h
def pairs(Rv,Cv,q):
    inp=f"17 3 4 {q}\n{' '.join(map(str,Rv))}\n{' '.join(map(str,Cv))}\n"
    out=subprocess.run(["./packing_masks"],input=inp,capture_output=True,text=True).stdout
    return int(out.strip().split("pairs=")[-1])
random.seed(int(sys.argv[1])); n=int(sys.argv[2]); K=int(sys.argv[3])
best=None
for it in range(n):
    hR=randdir(rows); hC=randdir(cols)
    Rv=[K*r+x for r,x in zip(R,hR)]; Cv=[K*c+x for c,x in zip(C,hC)]
    if min(Rv)<1 or min(Cv)<1: continue
    p=pairs(Rv,Cv,26*K)
    if best is None or p<best: best=p; print(it,'pairs',p,'hR',hR,'hC',hC,flush=True)
    if p==0: print('HIT',Rv,Cv,flush=True); break
print('done best',best)
