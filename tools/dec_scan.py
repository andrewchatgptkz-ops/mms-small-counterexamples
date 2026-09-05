"""Scan all decrements of the pre-decrement 6x15 (T=29): one good per row (R) and one per column (C) reduced by 1.
Which choices give NO allocation at T=28 (3+3)?"""
from inst import get, check
import subprocess, itertools, sys
base = get('6x15')
Rp = [8,16,5,10,1,18,5,24,9,2,18,25,4,12,17]
Cp = [9,12,7,10,1,17,7,26,10,1,17,27,3,12,15]
rows = base['rows']; cols = base['cols']
part = int(sys.argv[1]); nparts = int(sys.argv[2])
proc = subprocess.Popen(['./dp','feas'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
hits=[]; cnt=0
rowchoices = list(itertools.product(*rows)); colchoices = list(itertools.product(*cols))
for i,rc in enumerate(rowchoices):
    if i % nparts != part: continue
    R = Rp[:]
    for g in rc: R[g]-=1
    if min(R) < 0: continue
    for cc in colchoices:
        C = Cp[:]
        for g in cc: C[g]-=1
        if min(C) < 0: continue
        cnt+=1
        vals=[R]*3+[C]*3
        proc.stdin.write("6 15 28\n"+"\n".join(' '.join(map(str,v)) for v in vals)+"\n"); proc.stdin.flush()
        if int(proc.stdout.readline())==0:
            hits.append(([g+1 for g in rc],[g+1 for g in cc],R,C))
            print('HIT', hits[-1], flush=True)
print('part',part,'tested',cnt,'hits',len(hits))
