#include <bits/stdc++.h>
using namespace std; typedef unsigned long long u64;
int main(){ int cm[7]; vector<array<int,7>> perms; array<int,7> p; iota(p.begin(),p.end(),0); do perms.push_back(p); while(next_permutation(p.begin(),p.end()));
  while(scanf("%d %d %d %d %d %d %d",&cm[0],&cm[1],&cm[2],&cm[3],&cm[4],&cm[5],&cm[6])==7){ u64 best=~0ULL; for(auto&q:perms){ int c[7]; for(int j=0;j<7;j++){int v=0; for(int i=0;i<7;i++) if(cm[j]>>q[i]&1) v|=1<<i; c[j]=v;} sort(c,c+7); u64 k=0; for(int j=0;j<7;j++) k=(k<<8)|c[j]; if(k<best)best=k;} printf("%016llx\n",best);} }
