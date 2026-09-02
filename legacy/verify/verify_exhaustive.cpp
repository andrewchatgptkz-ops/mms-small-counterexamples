// Exact verifier in C++ (fast). Reads a whitespace matrix: first line "N M", then N rows of M integers.
// Usage: g++ -O2 -o verify_exhaustive verify_exhaustive.cpp && ./verify_exhaustive < instances/4x11_T30.txt
#include <bits/stdc++.h>
using namespace std;
int main(){
  int N,M; if(!(cin>>N>>M)) return 1;
  vector<vector<int>> V(N,vector<int>(M)); for(auto&r:V)for(auto&x:r)cin>>x;
  // MMS: enumerate labelings with restricted growth (unordered partitions), require all N bundles nonempty
  vector<int> mms(N,-1);
  for(int a=0;a<N;a++){
    vector<int> lab(M,0), s(N,0); int best=-1;
    function<void(int,int)> rec=[&](int g,int used){
      if(g==M){ if(used==N) best=max(best,*min_element(s.begin(),s.end())); return; }
      if(M-g<N-used) return;
      for(int b=0;b<used;b++){ s[b]+=V[a][g]; rec(g+1,used); s[b]-=V[a][g]; }
      if(used<N){ s[used]+=V[a][g]; rec(g+1,used+1); s[used]-=V[a][g]; }
    };
    rec(0,0); mms[a]=best;
  }
  long long total=1; for(int i=0;i<M;i++) total*=N;
  long long cnt=0; int bestmin=-1;
  vector<int> u(N), a(M,0);
  for(long long code=0; code<total; code++){
    long long x=code; fill(u.begin(),u.end(),0);
    for(int g=0;g<M;g++){ int o=x%N; x/=N; u[o]+=V[o][g]; }
    bool ok=true; int mn=INT_MAX;
    for(int i=0;i<N;i++){ if(u[i]<mms[i]) ok=false; mn=min(mn,u[i]); }
    if(ok) cnt++; bestmin=max(bestmin,mn);
  }
  printf("MMS:"); for(int x:mms) printf(" %d",x); printf("\n");
  printf("allocations enumerated: %lld\nMMS allocations: %lld\nmax-min: %d\nVERDICT: %s\n",
         total,cnt,bestmin, cnt==0?"NO MMS ALLOCATION":"MMS ALLOCATION EXISTS");
}
