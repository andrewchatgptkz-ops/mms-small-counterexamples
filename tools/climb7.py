import random, subprocess, sys
R=[8,15,4,9,1,17,4,23,9,1,17,24,3,11,16,22,5]; C=[9,11,6,9,1,16,4,24,9,1,16,25,3,11,15,23,6]
rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13],[14,15],[16,17]]
cols=[[1,4,9],[5,10,12],[2,11],[3,15,17],[8,13],[6,14],[7,16]]
def pairs(Rv,Cv,q):
    inp=f"17 3 4 {q}\n{' '.join(map(str,Rv))}\n{' '.join(map(str,Cv))}\n"
    out=subprocess.run(["./packing_masks"],input=inp,capture_output=True,text=True).stdout
    return int(out.strip().split("pairs=")[-1])
random.seed(int(sys.argv[1])); K=int(sys.argv[2]); D=int(sys.argv[3]); iters=int(sys.argv[4])
hR=[0]*17; hC=[0]*17
def score(hR,hC):
    Rv=[K*r+x for r,x in zip(R,hR)]; Cv=[K*c+x for c,x in zip(C,hC)]
    if min(Rv)<1 or min(Cv)<1: return 10**9
    return pairs(Rv,Cv,26*K)
cur=score(hR,hC); print('start',cur,flush=True)
for it in range(iters):
    # move: pick a row (R) or column (C), transfer 1 unit between two of its goods (keeps sums)
    if random.random()<0.5:
        g=random.choice(rows); h=hR
    else:
        g=random.choice(cols); h=hC
    i,j=random.sample(g,2); i-=1; j-=1
    if h[i]+1>D or h[j]-1<-D: continue
    h[i]+=1; h[j]-=1
    s=score(hR,hC)
    if s<=cur:
        if s<cur: print(it,'pairs',s,'hR',hR,'hC',hC,flush=True)
        cur=s
        if s==0: print('HIT K',K,'R',[K*r+x for r,x in zip(R,hR)],'C',[K*c+x for c,x in zip(C,hC)],flush=True); break
    else:
        h[i]-=1; h[j]+=1
print('done',cur)
