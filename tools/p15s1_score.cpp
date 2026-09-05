// Independent packing scorer: a disjoint minimal R-bundles + b disjoint minimal C-bundles.
// stdin: m q a b, then m R-values, then m C-values.
#include <bits/stdc++.h>
using namespace std; typedef long long ll; typedef unsigned long long u64;
int m,q,a,b; vector<ll> R,C;
vector<int> minimal(const vector<ll>&v){ vector<int> out; for(int s=0;s<(1<<m);s++){ ll t=0; for(int i=0;i<m;i++) if(s>>i&1) t+=v[i]; if(t<q) continue; bool mn=true; for(int i=0;i<m&&mn;i++) if((s>>i&1)&&t-v[i]>=q) mn=false; if(mn) out.push_back(s);} return out; }
// cnt[U] = ordered k-tuples of pairwise disjoint minimal sets with union U
vector<u64> level(const vector<int>&L,int k){ vector<u64> cur(1<<m,0); for(int s:L) cur[s]=1; for(int t=1;t<k;t++){ vector<u64> nx(1<<m,0); for(int U=0;U<(1<<m);U++) if(cur[U]) for(int s:L) if(!(s&U)) nx[U|s]+=cur[U]; cur.swap(nx);} return cur; }
int main(){ scanf("%d %d %d %d",&m,&q,&a,&b); R.resize(m);C.resize(m); for(auto&x:R)scanf("%lld",&x); for(auto&x:C)scanf("%lld",&x);
  auto LR=minimal(R), LC=minimal(C); auto cr=level(LR,a), cc=level(LC,b);
  ll fa=1,fb=1; for(int i=2;i<=a;i++)fa*=i; for(int i=2;i<=b;i++)fb*=i;
  u64 ur=0,uc=0,tr=0,tc=0; for(int U=0;U<(1<<m);U++){ if(cr[U]){ur++;tr+=cr[U];} if(cc[U]){uc++;tc+=cc[U];} }
  // zeta over subsets: G[S]=sum_{V subset S} f[V]
  vector<u64> g1(1<<m),g2(1<<m); for(int U=0;U<(1<<m);U++){g1[U]=cc[U]?1:0; g2[U]=cc[U]/fb;}
  for(int i=0;i<m;i++) for(int S=0;S<(1<<m);S++) if(S>>i&1){ g1[S]+=g1[S^(1<<i)]; g2[S]+=g2[S^(1<<i)]; }
  int full=(1<<m)-1; u64 distinct=0; unsigned __int128 tuples=0; for(int U=0;U<(1<<m);U++) if(cr[U]){ distinct+=g1[full^U]; tuples+=(unsigned __int128)(cr[U]/fa)*g2[full^U]; }
  printf("q=%d minimal R=%zu C=%zu | disjoint tuples R=%llu C=%llu | union masks R=%llu C=%llu | distinct union pairs=%llu | tuple pairs=%llu\n",q,LR.size(),LC.size(),tr/fa,tc/fb,ur,uc,distinct,(u64)tuples);
}
