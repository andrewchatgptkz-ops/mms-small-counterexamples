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
  q=Fraction(s);assert q>=0
  if idx<24:co[idx]-=q;co[24]+=q
  else:
   t,m=n['losing'][idx-24]
   for j in bits(m):co[t*12+j]+=q
   co[24]+=q;rhs+=q
 for idx,s in n['dual']['mu']:
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

# Independently enumerate ALL simple, connected, minimum-degree-two patterns.
# Uses only the Python standard library, not the producer's enumerator.
import gzip
from itertools import combinations_with_replacement,permutations
start=time.monotonic()
allowed=[x for x in range(32) if x.bit_count()>=2]
perms=list(permutations(range(5)))
permuted=[[sum(1<<p[j] for j in range(5) if x>>j&1) for x in range(32)] for p in perms]
def canonical(key):return min(tuple(sorted(mp[x] for x in key)) for mp in permuted)
def connected(key):
 seen={0};todo=[0]
 while todo:
  v=todo.pop()
  ns=([5+j for j in range(5) if key[v]>>j&1] if v<5 else [j for j in range(5) if key[j]>>(v-5)&1])
  for w in ns:
   if w not in seen:seen.add(w);todo.append(w)
 return len(seen)==10
expected=set();raw=degreeok=connok=0
for key in combinations_with_replacement(allowed,5):
 if sum(x.bit_count() for x in key)!=12:continue
 raw+=1
 if min(sum(bool(x>>j&1) for x in key) for j in range(5))<2:continue
 degreeok+=1
 if not connected(key):continue
 connok+=1;expected.add(canonical(key))
with gzip.open(ROOT/'proofs.json.gz','rt') as f:bundle=json.load(f)
patterns=bundle['patterns'];states=bundle['states']
assert [tuple(p['row_masks']) for p in patterns]==sorted(expected)
results=[]
for i,p in enumerate(patterns):
 assert p['id']==f'P{i:02d}'
 coords=[(r,c) for r in range(5) for c in range(5) if p['row_masks'][r]>>c&1]
 assert coords==list(map(tuple,p['coordinates'])) and len(coords)==12
 assert p['rows']==[sum(1<<g for g,(r,c) in enumerate(coords) if r==k) for k in range(5)]
 assert p['cols']==[sum(1<<g for g,(r,c) in enumerate(coords) if c==k) for k in range(5)]
 if p['direct_packings']:
  for w in p['direct_packings']:assert pack(w,p)==[]
  results.append({'pattern':p['id'],'result':'VERIFIED_VALUE_INDEPENDENT_EXCLUSION'})
 else:results.append(check(p,states[p['id']]))
assert len(results)==37
report={'status':'ALL 37 EXACT EXCLUSIONS VERIFIED','enumeration':{'raw_row_multisets':raw,'both_side_degree_ok':degreeok,'connected_row_multisets':connok,'oriented_patterns':len(expected)},'results':results,'seconds':time.monotonic()-start}
print(json.dumps(report,indent=2))
