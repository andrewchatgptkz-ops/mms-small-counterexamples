"""Independent solver-free checker for rational LP branching certificates.
Only integers, fractions, set containment and explicit packings are trusted.
It does not import the producer, NumPy, SciPy, or the packing oracle.
"""
import json,sys,time
from fractions import Fraction
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def bits(x):return [j for j in range(12) if x>>j&1]
def implies(assumptions,required):
 return all(any(t==u and mask&large==mask for u,large in assumptions) for t,mask in required)
def pack(w,p):
 assert len(w['R'])==2 and len(w['C'])==3
 used=0;choice=[]
 for t,(key,groups) in enumerate([('R',p['rows']),('C',p['cols'])]):
  for m in w[key]:
   assert isinstance(m,int) and 0<m<4096 and not used&m;used|=m
   if not any(m&g==g for g in groups):choice.append((t,m))
 return sorted(choice)
def transform(loss,perm,p):
 assert sorted(perm)==list(range(12))
 def apply(mask):return sum(1<<perm[j] for j in bits(mask))
 for groups in [p['rows'],p['cols']]:assert sorted(apply(g) for g in groups)==sorted(groups)
 return [(t,apply(m)) for t,m in loss]
def dual(n,p):
 co=[Fraction(0) for _ in range(25)];rhs=Fraction(0)
 for idx,s in n['dual']['lambda']:
  assert isinstance(idx,int) and 0<=idx<24+len(n['losing'])
  q=Fraction(s);assert q>=0
  if idx<24:co[idx]-=q;co[24]+=q
  else:
   t,m=n['losing'][idx-24]
   for j in bits(m):co[t*12+j]+=q
   co[24]+=q;rhs+=q
 for idx,s in n['dual']['mu']:
  assert isinstance(idx,int) and 0<=idx<10
  q=Fraction(s);t=idx//5;g=[p['rows'],p['cols']][t][idx%5]
  for j in bits(g):co[t*12+j]+=q
  rhs+=q
 assert co[:24]==[0]*24 and co[24]>0 and rhs<=0
 assert str(co[24])==n['dual']['delta_coefficient'] and str(rhs)==n['dual']['rhs']
 return [(n['losing'][idx-24][0],n['losing'][idx-24][1]) for idx,s in n['dual']['lambda'] if idx>=24 and Fraction(s)>0]
def check(p,state):
 nodes=state['nodes'];checked=set();visiting=set();support={}
 for t,groups in enumerate([p['rows'],p['cols']]):
  assert len(groups)==5 and sum(g.bit_count() for g in groups)==12
  used=0
  for g in groups:assert not used&g;used|=g
  assert used==4095
 def rec(i):
  assert isinstance(i,int) and 0<=i<len(nodes)
  if i in checked:return
  assert i not in visiting;visiting.add(i);n=nodes[i]
  assert n['id']==i and n['closed'];loss=n['losing']
  assert all(t in [0,1] and 0<m<4096 for t,m in loss)
  if n['kind']=='dual':support[i]=dual(n,p)
  elif n['kind']=='core':
   ref=n['ref'];assert nodes[ref]['kind']=='dual';rec(ref);image=transform(loss,n['perm'],p) if 'perm' in n else loss;assert implies(image,support[ref])
  elif n['kind']=='symmetry':
   ref=n['ref'];assert implies(transform(loss,n['perm'],p),nodes[ref]['losing']);rec(ref)
  elif n['kind']=='branch':
   choices=pack(n['packing'],p);assert choices==list(map(tuple,n['choices']))
   assert len(choices)==len(n['children'])
   for ch,child in zip(choices,n['children']):
    assert implies(list(map(tuple,loss))+[ch],nodes[child]['losing']);rec(child)
  else:raise AssertionError('unclosed proof node kind '+n['kind'])
  visiting.remove(i);checked.add(i)
 expected=[(hc,hr) for hc in range(5) for hr in combinations(range(5),2)]
 assert len(state['roots'])==50 and sorted(r['index'] for r in state['roots'])==list(range(50))
 for r in state['roots']:
  hc,hr=expected[r['index']];assert hc==r['hard_column_allowed'] and list(hr)==r['hard_rows_allowed'] and r['closed']
  loss=[(0,c) for k,c in enumerate(p['cols']) if k!=hc]+[(1,g) for k,g in enumerate(p['rows']) if k not in hr]
  assert implies(loss,nodes[r['node']]['losing']);rec(r['node'])
 return {'pattern':p['id'],'result':'VERIFIED_EXACT_RATIONAL_EXCLUSION','checked_nodes':len(checked),'stored_nodes':len(nodes),'roots':50}


"""Independent stdlib enumeration for use inside the portable checker.
Row multisets of weak compositions, unlike the producer's recursive C++ search.
Degree-sorted columns reduce enumeration but do not quotient transposition.
"""
from itertools import combinations_with_replacement,product,permutations
from collections import Counter

def weak_compositions(total,n=5):
 if n==1:
  yield (total,)
 else:
  for x in range(total+1):
   for rest in weak_compositions(total-x,n-1):yield (x,)+rest

def connected_matrix(a):
 seen={0};todo=[0]
 while todo:
  v=todo.pop()
  ns=[5+j for j in range(5) if a[v][j]] if v<5 else [j for j in range(5) if a[j][v-5]]
  for w in ns:
   if w not in seen:seen.add(w);todo.append(w)
 return len(seen)==10

def matrix_class(a):
 return ('simple' if max(map(max,a))<=1 else 'multi')+'_'+('connected' if connected_matrix(a) else 'disconnected')

def independent_enumeration():
 rows={d:list(weak_compositions(d)) for d in [2,3,4]}
 # Each row is encoded in base five, an injective representation since entries <=4.
 def encode(row):
  z=0
  for x in row:z=5*z+x
  return z
 def decode(z):
  out=[]
  for _ in range(5):out.append(z%5);z//=5
  return tuple(reversed(out))
 permutations_by_degrees={}
 maps={}
 for deg in [(2,2,2,2,4),(2,2,2,3,3)]:
  ps=[p for p in permutations(range(5)) if tuple(deg[j] for j in p)==deg]
  permutations_by_degrees[deg]=ps
  maps[deg]=[{encode(r):encode(tuple(r[j] for j in p)) for r in sum(rows.values(),[])} for p in ps]
 expected=set();raw=degreeok=ordered=0
 for deg2_count in [4,3]:
  tails=(([r] for r in rows[4]) if deg2_count==4 else combinations_with_replacement(rows[3],2))
  # Materialize the independent Cartesian-product factor once.
  tails=list(tails)
  for head in combinations_with_replacement(rows[2],deg2_count):
   for tail in tails:
    raw+=1;a=tuple(head)+tuple(tail);cd=tuple(map(sum,zip(*a)))
    if min(cd)<2:continue
    degreeok+=1
    if cd!=tuple(sorted(cd)):continue
    ordered+=1;codes=tuple(map(encode,a))
    key=min(tuple(sorted(mp[c] for c in codes)) for mp in maps[cd])
    expected.add(key)
 result={tuple(decode(x) for x in k) for k in expected}
 stats={'raw_row_multisets':raw,'degree_ok':degreeok,'sorted_column_degrees':ordered,'oriented_total':len(result),'counts':dict(Counter(matrix_class(a) for a in result))}
 return result,stats



import gzip,argparse
ap=argparse.ArgumentParser();ap.add_argument('--allow-incomplete',action='store_true');args=ap.parse_args()
start=time.monotonic();expected,enum_stats=independent_enumeration()
# Canonicalisation for bundle matrices is independent of the producer's ordering.
PERMS=list(permutations(range(5)))
def canonical(a):
 deg=list(map(sum,zip(*a)));sd=sorted(deg)
 return min(tuple(sorted(tuple(r[j] for j in p) for r in a)) for p in PERMS if [deg[j] for j in p]==sd)
with gzip.open(ROOT/'proofs.json.gz','rt') as f:bundle=json.load(f)
patterns=bundle['patterns'];states=bundle['states'];pending=bundle.get('pending',[])
assert len(patterns)==len(expected)==462
assert len({p['id'] for p in patterns})==len(patterns)
actual=[];results=[]
assert {p['id'] for p in patterns if p['id'].startswith('P')}=={f'P{i:02d}' for i in range(37)}
for p in patterns:
 a=p['matrix'];assert len(a)==5 and all(len(r)==5 for r in a)
 assert all(isinstance(x,int) and x>=0 for r in a for x in r)
 assert sum(map(sum,a))==12 and min(map(sum,a))>=2 and min(map(sum,zip(*a)))>=2
 actual.append(canonical(a))
 assert p['class']==matrix_class(a)
 coords=[(r,c) for r in range(5) for c in range(5) for _ in range(a[r][c])]
 assert coords==list(map(tuple,p['coordinates'])) and len(coords)==12
 assert p['rows']==[sum(1<<g for g,(r,c) in enumerate(coords) if r==k) for k in range(5)]
 assert p['cols']==[sum(1<<g for g,(r,c) in enumerate(coords) if c==k) for k in range(5)]
 if p['direct_packings']:
  for w in p['direct_packings']:assert pack(w,p)==[]
  results.append({'pattern':p['id'],'class':p['class'],'result':'VERIFIED_VALUE_INDEPENDENT_EXCLUSION'})
 elif p['id'] in states:
  results.append(check(p,states[p['id']])|{'class':p['class']})
 else:
  assert sum(q['pattern']==p['id'] for q in pending)==1
  results.append({'pattern':p['id'],'class':p['class'],'result':'UNDECIDED_NOT_EXCLUDED'})
assert len(set(actual))==len(actual) and set(actual)==expected
assert set(states)=={p['id'] for p in patterns if not p['direct_packings'] and p['id'] not in {q['pattern'] for q in pending}}
# Independently enumerate the additional simple grids with exactly one C-singleton.
# Different representation and traversal from the multigraph C++ producer.
aux_expected=set();allowed_masks=[m for m in range(32) if m.bit_count()>=2]
for row_masks in combinations_with_replacement(allowed_masks,5):
 if sum(m.bit_count() for m in row_masks)!=12:continue
 cd=[sum((m>>c)&1 for m in row_masks) for c in range(5)]
 if min(cd)!=1 or cd.count(1)!=1:continue
 a=tuple(tuple((m>>c)&1 for c in range(5)) for m in row_masks)
 aux_expected.add(canonical(a))
assert len(aux_expected)==72
aux_patterns=bundle.get('auxiliary_patterns',[]);aux_states=bundle.get('auxiliary_states',{});aux_pending=bundle.get('auxiliary_pending',[])
assert len(aux_patterns)==72 and {canonical(p['matrix']) for p in aux_patterns}==aux_expected
assert {p['id'] for p in aux_patterns}=={f'SB{i:02d}' for i in range(72)}
aux_results=[]
for p in aux_patterns:
 a=p['matrix'];assert len(a)==5 and all(len(r)==5 for r in a)
 assert all(isinstance(x,int) and x in (0,1) for r in a for x in r)
 assert sum(map(sum,a))==12 and min(map(sum,a))>=2
 cd=list(map(sum,zip(*a)));assert min(cd)==1 and cd.count(1)==1
 coords=[(r,c) for r in range(5) for c in range(5) if a[r][c]]
 assert coords==list(map(tuple,p['coordinates']))
 assert p['rows']==[sum(1<<g for g,(r,c) in enumerate(coords) if r==k) for k in range(5)]
 assert p['cols']==[sum(1<<g for g,(r,c) in enumerate(coords) if c==k) for k in range(5)]
 if p['direct_packings']:
  for w in p['direct_packings']:assert pack(w,p)==[]
  aux_results.append({'pattern':p['id'],'result':'VERIFIED_VALUE_INDEPENDENT_EXCLUSION'})
 elif p['id'] in aux_states:aux_results.append(check(p,aux_states[p['id']]))
 else:
  assert sum(q['pattern']==p['id'] for q in aux_pending)==1
  aux_results.append({'pattern':p['id'],'result':'UNDECIDED_NOT_EXCLUDED'})
assert set(aux_states)=={p['id'] for p in aux_patterns if not p['direct_packings'] and p['id'] not in {q['pattern'] for q in aux_pending}}
if not args.allow_incomplete:
 assert not pending,'Incomplete main class: see pending list'
 assert not aux_pending,'Incomplete singleton auxiliary class: see auxiliary pending list'

counts={}
for cls in enum_stats['counts']:
 rr=[r for r in results if r['class']==cls]
 counts[cls]={'total':len(rr),'direct':sum(r['result']=='VERIFIED_VALUE_INDEPENDENT_EXCLUSION' for r in rr),'branching':sum(r['result']=='VERIFIED_EXACT_RATIONAL_EXCLUSION' for r in rr),'undecided':sum(r['result']=='UNDECIDED_NOT_EXCLUDED' for r in rr)}
report={'status':('ALL 462 EXACT EXCLUSIONS VERIFIED' if not pending else 'PARTIAL PROOFS VERIFIED; CLASS INCOMPLETE'),'enumeration':enum_stats,'class_outcomes':counts,'total_checked_nodes':sum(r.get('checked_nodes',0) for r in results),'total_dual_leaves':sum(n['kind']=='dual' for s in states.values() for n in s['nodes']),'total_roots':sum(r.get('roots',0) for r in results),'undecided':[q['pattern'] for q in pending],'results':results,'seconds':time.monotonic()-start}
report['auxiliary']={'status':'ALL 72 AUXILIARY SINGLETON CASES VERIFIED' if not aux_pending else 'AUXILIARY CLASS INCOMPLETE','patterns':72,'direct':sum(bool(p['direct_packings']) for p in aux_patterns),'branching_proofs':len(aux_states),'undecided':[q['pattern'] for q in aux_pending],'checked_nodes':sum(r.get('checked_nodes',0) for r in aux_results),'roots':sum(r.get('roots',0) for r in aux_results),'dual_leaves':sum(n['kind']=='dual' for s in aux_states.values() for n in s['nodes']),'results':aux_results}
print(json.dumps(report,indent=2))
