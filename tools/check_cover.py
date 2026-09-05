import json, itertools, os
R0=[8,15,4,9,1,17,4,23,9,1,17,24,3,11,16,22,5]; C0=[9,11,6,9,1,16,4,24,9,1,16,25,3,11,15,23,6]
base=os.environ.get("P16S1_RESULTS")
if not base:
    raise SystemExit("set P16S1_RESULTS to the results/ directory of the unpacked P16S1_final.tar.gz "
                     "(sha256 643e59ac...; see PROVENANCE.md)")
base=base.rstrip("/")+"/"
c=json.load(open(base+'decrement_cover/certificate.json'))
v=json.load(open(base+'decrement/variant_choices_zero_based.json'))
packs=[p['packing'] for p in c['packings']]
assert all(sum(p)==(1<<17)-1 and len(p)==7 for p in packs)
def val(vec,mask): return sum(vec[g] for g in range(17) if mask>>g&1)
combos=list(itertools.combinations(range(7),3))
covered=0; uncovered=[]
for ri,rch in enumerate(v['R']):
    R=R0[:]; 
    for g in rch: R[g]-=1
    assert min(R)>=1 and len(rch)==7
    pr=[[val(R,b) for b in p] for p in packs]
    for ci,cch in enumerate(v['C']):
        C=C0[:]
        for g in cch: C[g]-=1
        assert min(C)>=1
        ok=False
        for pi,p in enumerate(packs):
            pc=[val(C,b) for b in p]
            for tr in combos:
                if all(pr[pi][i]>=26 for i in tr) and all(pc[i]>=26 for i in range(7) if i not in tr):
                    ok=True; break
            if ok: break
        if ok: covered+=1
        else: uncovered.append((ri,ci))
print('pairs',len(v['R'])*len(v['C']),'covered by the 20 packings',covered,'uncovered',len(uncovered), uncovered[:5])
# also sanity: rows sum to 26 under R and columns under C for every variant
rows=[[1,2,3],[4,5,6],[7,8],[9,10,11],[12,13],[14,15],[16,17]]; cols=[[1,4,9],[5,10,12],[2,11],[3,15,17],[8,13],[6,14],[7,16]]
bad=0
for rch in v['R']:
    R=R0[:]; 
    for g in rch: R[g]-=1
    bad+=any(sum(R[g-1] for g in r)!=26 for r in rows)
for cch in v['C']:
    C=C0[:]
    for g in cch: C[g]-=1
    bad+=any(sum(C[g-1] for g in cc)!=26 for cc in cols)
print('variants with wrong sums',bad)
