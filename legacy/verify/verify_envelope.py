#!/usr/bin/env python3
"""Compact certificate for two-type instances (agents 1,2 share row A; agents 3,4 share row B).
Usage: python3 verify_envelope.py instances/4x11_T30.json [--list]

Argument. Let W(g) = max(A(g), B(g)). In any MMS allocation each of the four bundles is worth
>= T to its recipient, hence >= T under W. So it suffices to enumerate UNLABELED partitions of the
goods into four bundles, keep those whose four W-sums are all >= T ("survivors"), and check for each
survivor whether two bundles can go to the A-agents and the other two to the B-agents with every
assigned bundle worth >= T to its recipient. If no survivor admits such a 2+2 assignment, no MMS
allocation exists. The survivor list is short enough to check by hand (114 rows for 4x11_T30).
The MMS values themselves (=T) are certified separately by the witness partitions in the README.
"""
import json, sys
from itertools import combinations

def main(path, show):
    inst = json.load(open(path)); V=inst["valuations"]; T=inst["T"]; N=4; M=inst["goods"]
    assert V[0]==V[1] and V[2]==V[3], "envelope certificate requires the 2+2 two-type structure"
    A,B=V[0],V[2]; W=[max(a,b) for a,b in zip(A,B)]
    lab=[0]*M; s=[0]*N; s[0]=W[0]; count=[0]; surv=[]
    def rec(j,ml):
        if j==M:
            if ml!=N-1: return
            count[0]+=1
            if min(s)>=T: surv.append(tuple(lab))
            return
        for b in range(min(ml+1,N-1)+1):
            lab[j]=b; s[b]+=W[j]; rec(j+1,max(ml,b)); s[b]-=W[j]
    rec(1,0)
    feasible=0
    for lab_ in surv:
        bs=[[j for j in range(M) if lab_[j]==k] for k in range(N)]
        va=[sum(A[j] for j in b) for b in bs]; vb=[sum(B[j] for j in b) for b in bs]
        ok=any(all(va[k]>=T for k in aa) and all(vb[k]>=T for k in range(N) if k not in aa)
               for aa in combinations(range(N),2))
        feasible+=ok
        if show:
            print(" | ".join(f"{tuple(j+1 for j in b)} A={va[k]} B={vb[k]}" for k,b in enumerate(bs)), "FEASIBLE" if ok else "")
    print(f"instance: {inst['name']}  T={T}")
    print(f"unlabeled 4-partitions enumerated: {count[0]}")
    print(f"survivors (all four W-sums >= T): {len(surv)}")
    print(f"survivors admitting a 2+2 assignment: {feasible}")
    print("VERDICT:", "NO MMS ALLOCATION (given MMS=T for all agents)" if feasible==0 else "INCONCLUSIVE")

if __name__=="__main__":
    main(sys.argv[1], "--list" in sys.argv)
