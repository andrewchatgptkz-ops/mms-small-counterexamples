"""Subdivide edge e=(r,c) of an instance: e=(rho,gamma) -> e1=(rho, T-y) in (r,c'), e2=(x,y) in (r',c'), e3=(T-x, gamma) in (r',c).
Scan (x,y), test feasibility at q=T with split (a+1, b+1) [and optionally other splits]. Uses ./dp feas via one pipe."""
from inst import get, check
import subprocess, sys, itertools

def subdivide(d, g, x, y):
    R,C,T = d['R'][:], d['C'][:], d['T']
    rho, gamma = R[g], C[g]
    # e1 stays as good g in row r, new column c'
    R[g] = rho; C[g] = T - y
    R += [x, T - x]; C += [y, gamma]
    m = len(R)
    rows = [r[:] for r in d['rows']]; cols = [c[:] for c in d['cols']]
    ci = next(j for j,c in enumerate(cols) if g in c)
    cols[ci].remove(g); cols[ci].append(m-1)       # e3 in old column
    rows.append([m-2, m-1])                         # new row r' = {e2, e3}
    cols.append([g, m-2])                           # new column c' = {e1, e2}
    return dict(n=d['n']+2-1, a=None, T=T, R=R, C=C, rows=rows, cols=cols)

if __name__ == '__main__':
    name = sys.argv[1]; edge = int(sys.argv[2])-1  # good index (1-based)
    aR = int(sys.argv[3])  # number of R agents in subdivided instance
    d = get(name); check(d)
    n2 = d['n']+1; T=d['T']
    proc = subprocess.Popen(['./dp','feas'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    good=[]
    for x in range(1, T):
        for y in range(1, T):
            d2 = subdivide(d, edge, x, y)
            d2['n']=n2; d2['a']=aR
            check(d2)
            vals = [d2['R']]*aR + [d2['C']]*(n2-aR)
            proc.stdin.write(f"{n2} {len(d2['R'])} {T}\n" + "\n".join(' '.join(map(str,v)) for v in vals) + "\n"); proc.stdin.flush()
            f = int(proc.stdout.readline())
            if f == 0: good.append((x,y))
    print(name, 'edge g%d'%(edge+1), 'split', aR, '+', n2-aR, ': (x,y) with NO allocation at T:', len(good))
    print(good)
