# Independent brute-force check of a depth-2 (two branching goods, four leaves) certificate.
import json, itertools, sys
d=json.load(open(sys.argv[1]))
R,C,T,m,a,b=d['R'],d['C'],d['T'],d['goods'],d['a'],d['b']
p,q=[g-1 for g in d['branch_goods']]
assert sum(R)==8*T==sum(C)
for row in d['rows_R_sum_T']: assert sum(R[g-1] for g in row)==T
for col in d['cols_C_sum_T']: assert sum(C[g-1] for g in col)==T
assert sorted(g for r in d['rows_R_sum_T'] for g in r)==list(range(1,m+1))
assert sorted(g for c in d['cols_C_sum_T'] for g in c)==list(range(1,m+1))
assert max(R)<T and max(C)<T and min(R)>=1 and min(C)>=1
print("witness partitions OK; MMS = T =",T,"for all; max good <T; all positive")
# precompute set values
N=1<<m
Rv=[0]*N; Cv=[0]*N; 
for S in range(1,N):
    low=S&-S; i=low.bit_length()-1
    Rv[S]=Rv[S^low]+R[i]; Cv[S]=Cv[S^low]+C[i]
ok=True
for leaf,cert in d['certificates'].items():
    w=cert['w']; al=cert['alpha']; be=cert['beta']
    # leaf 'XY': X = type receiving p, Y = type receiving q
    # R-bundles may not contain a good given to C; C-bundles may not contain a good given to R
    forbR=sum(1<<g for g,t in zip((p,q),leaf) if t=='C')
    forbC=sum(1<<g for g,t in zip((p,q),leaf) if t=='R')
    wv=[0]*N
    for S in range(1,N):
        low=S&-S; wv[S]=wv[S^low]+w[low.bit_length()-1]
    minR=min(wv[S] for S in range(N) if Rv[S]>=T and not S&forbR)
    minC=min(wv[S] for S in range(N) if Cv[S]>=T and not S&forbC)
    tot=sum(w); need=a*al+b*be
    good=minR>=al and minC>=be and need>tot
    ok&=good
    print(f"leaf {leaf}: minR={minR} (alpha {al}) minC={minC} (beta {be}) sum w={tot} < a*alpha+b*beta={need} -> {'OK' if good else 'FAIL'}")
print("DEPTH-2 CERTIFICATE VALID" if ok else "CERTIFICATE INVALID")
# best allocation check
A=d['best_allocation_1based']; assert sorted(g for B in A for g in B)==list(range(1,m+1))
u=[sum((R if i<a else C)[g-1] for g in B) for i,B in enumerate(A)]
print("allocation utilities",u,"min",min(u))
