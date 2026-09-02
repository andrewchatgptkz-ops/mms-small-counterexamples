// Exact verifier by dynamic programming over subsets (no allocation enumeration).
// Input: whitespace matrix, first line "N M", then N rows of M integers (the .txt form).
// 1. MMS of each agent: DP with one valuation, best[k][S] = max_T min(sum(T), best[k-1][S\T]).
// 2. Exact max_A min_i v_i(A_i) over ALL labeled allocations: F_N(S)=v_N(S),
//    F_i(S) = max_{B subset of S} min(v_i(B), F_{i+1}(S\B)); F_1(full) is the answer.
//    Allocations are exactly ordered partitions into labeled possibly-empty bundles.
// Cost O(N * 3^M); m=16 runs in seconds. Independent of, and different in method from,
// verify_exhaustive.{py,cpp} which enumerate allocations literally.
// Usage: g++ -O2 -o verify_dp verify_dp.cpp && ./verify_dp < instances/5x13_T29.txt
#include <bits/stdc++.h>
using namespace std;
int main(){
  int N,M; if(!(cin>>N>>M)) return 1;
  vector<vector<long long>> V(N, vector<long long>(M));
  for(auto&r:V) for(auto&x:r) cin>>x;
  int F=1<<M;
  vector<vector<long long>> ss(N, vector<long long>(F,0));
  for(int i=0;i<N;i++) for(int S=1;S<F;S++){ int b=S&(-S); ss[i][S]=ss[i][S^b]+V[i][__builtin_ctz(b)]; }
  // MMS per agent
  for(int a=0;a<N;a++){
    vector<long long> p(F), q(F);
    for(int S=0;S<F;S++) p[S]=ss[a][S];
    for(int k=2;k<=N;k++){
      for(int S=0;S<F;S++){ long long best=LLONG_MIN;
        for(int B=S;;B=(B-1)&S){ best=max(best,min(ss[a][B],p[S^B])); if(!B)break; }
        q[S]=best; }
      swap(p,q);
    }
    printf("MMS[agent %d] = %lld\n", a+1, p[F-1]);
  }
  // exact max-min over all allocations
  vector<long long> nxt(F), cur(F);
  for(int S=0;S<F;S++) nxt[S]=ss[N-1][S];
  for(int i=N-2;i>=0;i--){
    for(int S=0;S<F;S++){ long long best=LLONG_MIN;
      for(int B=S;;B=(B-1)&S){ best=max(best,min(ss[i][B],nxt[S^B])); if(!B)break; }
      cur[S]=best; }
    swap(cur,nxt);
  }
  printf("max_A min_i v_i(A_i) over all %d^%d allocations (by DP) = %lld\n", N, M, nxt[F-1]);
  return 0;
}
