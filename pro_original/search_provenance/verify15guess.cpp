#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
using namespace std;
constexpr int N=4,M=11; using Row=array<int,M>;
long long cnt; int best; array<int,M> bestlab;
void rec(const Row&v,int p,int used,array<int,4>&s,array<int,M>&lab){if(p==M){if(used==4){cnt++;int x=*min_element(s.begin(),s.end());if(x>best){best=x;bestlab=lab;}}return;}if(M-p<4-used)return;for(int b=0;b<used;b++){lab[p]=b;s[b]+=v[p];rec(v,p+1,used,s,lab);s[b]-=v[p];}if(used<4){lab[p]=used;s[used]=v[p];rec(v,p+1,used+1,s,lab);s[used]=0;}}
int mms(const Row&v){cnt=0;best=-1;array<int,4>s{};array<int,M>l{};rec(v,0,0,s,l);return best;}
int main(){Row R={3,6,6,4,3,8,10,5,1,13,1};Row C={3,5,7,5,2,7,11,5,1,13,1};array<Row,4>V={R,R,C,C};array<int,4>mu;for(int a=0;a<4;a++){mu[a]=mms(V[a]);cout<<mu[a]<<" partitions "<<cnt<<"\n";}uint64_t total=1ULL<<(2*M),ok=0;int opt=-1;for(uint64_t code=0;code<total;code++){uint64_t x=code;array<int,4>s{};for(int g=0;g<M;g++){int a=x&3;x>>=2;s[a]+=V[a][g];}bool good=1;int mn=s[0];for(int a=0;a<4;a++){good&=s[a]>=mu[a];mn=min(mn,s[a]);}ok+=good;opt=max(opt,mn);}cout<<"ok "<<ok<<" opt "<<opt<<"\n";return !(mu==array<int,4>{15,15,15,15}&&ok==0&&opt==14);}
