// Independent verifier (Claude, 27.08.2026): MMS by subset DP; existence + max-min by LITERAL enumeration of n^m allocations.
// Use only for small instances (4x11: 4^11; 4x12: 4^12; 5x13: 5^13 ~ 1.2e9, seconds; 6x15 takes ~1 CPU-hour per shard set).
// args: n m then n rows of m ints
#include <bits/stdc++.h>
using namespace std;
int m,n; vector<vector<long long>> V;
long long sub_sum(const vector<long long>&v,int S){long long s=0;for(int i=0;i<m;i++)if(S>>i&1)s+=v[i];return s;}
long long mms(const vector<long long>& v){
  int F=1<<m; vector<long long> ss(F);
  for(int S=0;S<F;S++) ss[S]=sub_sum(v,S);
  vector<long long> prev(F),cur(F);
  for(int S=0;S<F;S++) prev[S]=ss[S];
  for(int k=2;k<=n;k++){
    for(int S=0;S<F;S++){
      long long best=LLONG_MIN;
      for(int T=S;;T=(T-1)&S){ long long val=min(ss[T],prev[S^T]); best=max(best,val); if(T==0)break; }
      cur[S]=best;
    }
    prev=cur;
  }
  return prev[F-1];
}
int main(int argc,char**argv){
  n=atoi(argv[1]); m=atoi(argv[2]);
  V.assign(n,vector<long long>(m));
  int p=3; for(int i=0;i<n;i++)for(int j=0;j<m;j++)V[i][j]=atoll(argv[p++]);
  vector<long long> M(n);
  for(int i=0;i<n;i++){M[i]=mms(V[i]); printf("MMS[%d] = %lld\n",i+1,M[i]);}
  long long total=1; for(int j=0;j<m;j++) total*=n;
  long long bestmin=LLONG_MIN; long long cnt=0; vector<int> bestA(m);
  vector<int> a(m,0);
  for(long long code=0;code<total;code++){
    long long c=code; for(int j=0;j<m;j++){a[j]=c%n;c/=n;}
    vector<long long> s(n,0);
    for(int j=0;j<m;j++) s[a[j]]+=V[a[j]][j];
    long long mn=LLONG_MAX; bool ok=true;
    for(int i=0;i<n;i++){ mn=min(mn,s[i]); if(s[i]<M[i]) ok=false; }
    if(ok) cnt++;
    if(mn>bestmin){bestmin=mn;bestA=a;}
  }
  printf("allocations enumerated: %lld\nMMS-allocations: %lld\nmax_A min_i v_i(A_i) = %lld\n",total,cnt,bestmin);
  printf("best assignment (good->agent):"); for(int j=0;j<m;j++)printf(" %d",bestA[j]+1); printf("\n");
  return 0;
}
