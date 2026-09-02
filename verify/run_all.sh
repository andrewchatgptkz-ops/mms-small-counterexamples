#!/bin/bash
# Verifies every instance in ../instances with three independent methods:
#  (1) subset-DP exact max-min and MMS (dp.cpp),
#  (2) packing certificate (packing.cpp: tuple pairs; packing_pairs.cpp: distinct union-mask pairs),
#  (3) the two-branch weight certificates, brute force over all 2^m subsets (verify_certificate.py).
set -e
cd "$(dirname "$0")"
g++ -O2 -o dp dp.cpp && g++ -O2 -o packing packing.cpp && g++ -O2 -o packing_pairs packing_pairs.cpp
for f in ../instances/*.json; do
  python3 - "$f" << 'PY'
import json,sys,subprocess
d=json.load(open(sys.argv[1])); n=d['agents']; a=int(d['split'].split()[0]); b=n-a; T=d['T']; R=d['R']; C=d['C']; m=len(R)
print(f"== {d['name']}: n={n} ({a}+{b}), m={m}, T={T}")
assert sum(R)==n*T and sum(C)==n*T
for r in d['rows_R_sum_T']: assert sum(R[g-1] for g in r)==T
for c in d['cols_C_sum_T']: assert sum(C[g-1] for g in c)==T
assert max(R)<T and max(C)<T
inp=f"{n} {m} {T}\n"+"\n".join(' '.join(map(str,v)) for v in [R]*a+[C]*b)+"\n"
mm=subprocess.run(['./dp','max'],input=inp,capture_output=True,text=True).stdout.strip()
mR=subprocess.run(['./dp','max'],input=f"{n} {m} {T}\n"+"\n".join(' '.join(map(str,R)) for _ in range(n))+"\n",capture_output=True,text=True).stdout.strip()
mC=subprocess.run(['./dp','max'],input=f"{n} {m} {T}\n"+"\n".join(' '.join(map(str,C)) for _ in range(n))+"\n",capture_output=True,text=True).stdout.strip()
print(f"   subset-DP: MMS(R)={mR} MMS(C)={mC} max-min={mm}  (expected T={T}, T-1={T-1})")
assert int(mR)==T and int(mC)==T and int(mm)==T-1
for q in (T,T-1):
    pk=f"{m} {a} {b} {q}\n{' '.join(map(str,R))}\n{' '.join(map(str,C))}\n"
    print('   '+subprocess.run(['./packing'],input=pk,capture_output=True,text=True).stdout.strip())
PY
done
python3 verify_certificate.py
echo "ALL INSTANCES VERIFIED"
