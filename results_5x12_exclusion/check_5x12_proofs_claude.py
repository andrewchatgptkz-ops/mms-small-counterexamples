# Independent re-implementation of the 5x12 exclusion proof checker (Claude, 2026-09-05).
# Trusts only: Fractions, subset tests, disjointness. Reads proofs.json.gz from the P16S2 archive.
import gzip, json, sys
from fractions import Fraction as F
from itertools import combinations
b=json.load(gzip.open(sys.argv[1],'rt'))
pats, states = b['patterns'], b['states']
M=12
def sub(m,big): return m & big == m
def implied(assume, need):   # every needed losing (t,m) is a subset of some assumed losing set of the same type
    return all(any(t==u and sub(m,big) for u,big in assume) for t,m in need)
def apply(perm,m): return sum(1<<perm[j] for j in range(M) if m>>j&1)
tot_nodes=0; tot_duals=0; tot_branch=0
for p in pats:
    rows, cols = p['rows'], p['cols']
    assert sorted(g for g in rows)==sorted(rows) and sum(rows)==4095 and sum(cols)==4095
    assert all(not (rows[i]&rows[j]) for i in range(5) for j in range(i+1,5))
    assert all(not (cols[i]&cols[j]) for i in range(5) for j in range(i+1,5))
    if p['direct_packings']:
        ok=False
        for w in p['direct_packings']:
            R2,C3=w['R'],w['C']; ms=R2+C3
            assert len(R2)==2 and len(C3)==3 and all(not(ms[i]&ms[j]) for i in range(5) for j in range(i+1,5))
            if all(any(sub(g,m) for g in rows) for m in R2) and all(any(sub(g,m) for g in cols) for m in C3): ok=True
        assert ok, p['id']; continue
    st=states[p['id']]; nodes=st['nodes']; done={}; stack=set()
    def leaf_ok(n):
        # combination: sum lam_i * (ineq_i) + sum mu_k * (eq_k) ; prove k*delta <= c, c<=0
        coef=[F(0)]*M*2; kd=F(0); rhs=F(0)
        for idx,s in n['dual']['lambda']:
            q=F(s); assert q>=0
            if idx<2*M:            # v_{t,g} >= delta  <=>  delta - v <= 0
                coef[idx]-=q; kd+=q
            else:                  # v_t(S) + delta <= 1 for losing (t,S)
                t,m=n['losing'][idx-2*M]
                for j in range(M):
                    if m>>j&1: coef[t*M+j]+=q
                kd+=q; rhs+=q
        for idx,s in n['dual']['mu']:  # witness equality v_t(group)=1, free multiplier
            q=F(s); t=idx//5; g=(rows if t==0 else cols)[idx%5]
            for j in range(M):
                if g>>j&1: coef[t*M+j]+=q
            rhs+=q
        assert all(c==0 for c in coef) and kd>0 and rhs<=0, ('bad dual', p['id'], n['id'])
        return [tuple(n['losing'][idx-2*M]) for idx,s in n['dual']['lambda'] if idx>=2*M and F(s)>0]
    def walk(i):
        if i in done: return done[i]
        assert i not in stack; stack.add(i)
        n=nodes[i]; loss=[tuple(x) for x in n['losing']]; kind=n['kind']
        global tot_nodes,tot_duals,tot_branch
        tot_nodes+=1
        if kind=='dual':
            supp=leaf_ok(n); tot_duals+=1
        elif kind=='core':
            ref=nodes[n['ref']]; assert ref['kind']=='dual'; supp_ref=walk(n['ref'])
            img=[(t,apply(n['perm'],m)) for t,m in loss] if 'perm' in n else loss
            if 'perm' in n:
                pr=n['perm']; assert sorted(pr)==list(range(M))
                assert sorted(apply(pr,g) for g in rows)==sorted(rows) and sorted(apply(pr,g) for g in cols)==sorted(cols)
            assert implied(img, supp_ref); supp=None
        elif kind=='symmetry':
            pr=n['perm']; assert sorted(pr)==list(range(M))
            assert sorted(apply(pr,g) for g in rows)==sorted(rows) and sorted(apply(pr,g) for g in cols)==sorted(cols)
            assert implied([(t,apply(pr,m)) for t,m in loss], [tuple(x) for x in nodes[n['ref']]['losing']]); walk(n['ref']); supp=None
        elif kind=='branch':
            tot_branch+=1
            R2,C3=n['packing']['R'],n['packing']['C']; ms=R2+C3
            assert len(R2)==2 and len(C3)==3 and all(0<m<4096 for m in ms) and all(not(ms[i]&ms[j]) for i in range(5) for j in range(i+1,5))
            # bundles that can lose: those not containing a full own-type witness
            can=[(0,m) for m in R2 if not any(sub(g,m) for g in rows)]+[(1,m) for m in C3 if not any(sub(g,m) for g in cols)]
            assert sorted(can)==sorted(tuple(x) for x in n['choices']) and len(can)==len(n['children'])
            for ch,child in zip(n['choices'],n['children']):
                assert implied(loss+[tuple(ch)], [tuple(x) for x in nodes[child]['losing']]); walk(child)
            supp=None
        else: raise AssertionError(kind)
        stack.remove(i); done[i]=supp; return supp
    roots=st['roots']; assert len(roots)==50
    seen=set()
    for r in roots:
        hc=r['hard_column_allowed']; hr=tuple(r['hard_rows_allowed']); seen.add((hc,hr))
        forced=[(0,cols[k]) for k in range(5) if k!=hc]+[(1,rows[k]) for k in range(5) if k not in hr]
        assert implied(forced,[tuple(x) for x in nodes[r['node']]['losing']]); walk(r['node'])
    assert seen=={(hc,hr) for hc in range(5) for hr in combinations(range(5),2)}
print('patterns',len(pats),'direct',sum(1 for p in pats if p['direct_packings']),'proved',sum(1 for p in pats if not p['direct_packings']),
      'nodes checked',tot_nodes,'dual leaves',tot_duals,'branch nodes',tot_branch)
print('ALL 37 EXCLUSIONS RE-VERIFIED (independent checker)')
