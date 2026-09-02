// Packing certificate for two-type instance: a disjoint R-sets >= q and b disjoint C-sets >= q, all disjoint.
// input: m a b q, R row, C row. Output counts: minimal sets, disjoint a-tuples/b-tuples, distinct union masks, compatible pairs.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long ull;
int m;
vector<int> minimal_sets(const vector<int>& v, int q){
    int full=(1<<m)-1; vector<int> sv(1<<m,0);
    for(int S=1;S<=full;S++){int low=S&-S; sv[S]=sv[S^low]+v[__builtin_ctz(S)];}
    vector<int> out;
    for(int S=1;S<=full;S++) if(sv[S]>=q){ bool mn=true; for(int x=S;x;x&=x-1){int low=x&-x; if(sv[S^low]>=q){mn=false;break;}} if(mn) out.push_back(S);}
    return out;
}
// enumerate disjoint k-tuples (unordered) of sets from list; return multiset of union masks as counts map
void tuples(const vector<int>& sets, int k, int start, int mask, int depth, unordered_map<int,ull>& cnt, ull& total){
    if(depth==k){cnt[mask]++; total++; return;}
    for(int i=start;i<(int)sets.size();i++) if(!(sets[i]&mask)) tuples(sets,k,i+1,mask|sets[i],depth+1,cnt,total);
}
int main(){
    int a,b,q; scanf("%d %d %d %d",&m,&a,&b,&q);
    vector<int> R(m),C(m); for(auto&x:R)scanf("%d",&x); for(auto&x:C)scanf("%d",&x);
    auto mR=minimal_sets(R,q), mC=minimal_sets(C,q);
    unordered_map<int,ull> cR,cC; ull tR=0,tC=0;
    tuples(mR,a,0,0,0,cR,tR); tuples(mC,b,0,0,0,cC,tC);
    // zeta: f[V] = number of C-tuples with union subset of V
    int full=(1<<m)-1; vector<ull> f(1<<m,0);
    for(auto&p:cC) f[p.first]+=p.second;
    for(int i=0;i<m;i++) for(int V=0;V<=full;V++) if(V>>i&1) f[V]+=f[V^(1<<i)];
    ull compat=0; for(auto&p:cR) compat+=p.second*f[full^p.first];
    printf("q=%d minimal R-sets=%zu C-sets=%zu | disjoint R-%d-tuples=%llu C-%d-tuples=%llu | distinct union masks R=%zu C=%zu | compatible unordered pairs=%llu\n",
           q,mR.size(),mC.size(),a,tR,b,tC,cR.size(),cC.size(),compat);
}
