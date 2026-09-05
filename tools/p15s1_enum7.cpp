// Independent enumeration of 7x7 rank-5 patterns (P15S1 acceptance).
// A pattern: 7x7 0/1 matrix, 18 ones, row sums (3,3,3,3,2,2,2), column sums a
// permutation of the same multiset, up to row and column permutations.
// Mode "enum": enumerate all, classify (connected? suppressed core simple? which
// cubic skeleton? row-side core vertices?), print one line per class.
// Mode "canon": read lines of 7 column masks (bits = rows) and print canonical keys.
// Mode "cubic": count labelled / unlabelled connected cubic graphs on 8 vertices.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;

static const int RT[7]={3,3,3,3,2,2,2};
static vector<array<int,7>> rowperms; // degree-preserving row permutations (144)

static void build_rowperms(){
  int a[4]={0,1,2,3}; int b[3]={4,5,6};
  do{ int bb[3]={4,5,6};
    do{ array<int,7> p; for(int i=0;i<4;i++)p[i]=a[i]; for(int i=0;i<3;i++)p[4+i]=bb[i]; rowperms.push_back(p);}
    while(next_permutation(bb,bb+3));
  }while(next_permutation(a,a+4));
}
// canonical key of a matrix given as 7 column masks (bit i = row i has a one)
static u64 canon(const int cm[7]){
  u64 best=~0ULL;
  for(auto&p:rowperms){
    int c[7];
    for(int j=0;j<7;j++){int v=0; for(int i=0;i<7;i++) if(cm[j]>>p[i]&1) v|=1<<i; c[j]=v;}
    sort(c,c+7);
    u64 k=0; for(int j=0;j<7;j++) k=(k<<8)|c[j];
    if(k<best)best=k;
  }
  return best;
}
static void unpack(u64 k,int cm[7]){ for(int j=6;j>=0;j--){cm[j]=k&255;k>>=8;} }

// skeletons from data/skeletons_final.json (P15S1), labelled 0..7
static const int SK[5][12][2]={
 {{0,5},{0,6},{0,7},{1,4},{1,6},{1,7},{2,4},{2,5},{2,7},{3,4},{3,5},{3,6}},
 {{0,5},{0,6},{0,7},{1,4},{1,6},{1,7},{2,3},{2,6},{2,7},{3,4},{3,5},{4,5}},
 {{0,5},{0,6},{0,7},{1,4},{1,6},{1,7},{2,3},{2,5},{2,7},{3,4},{3,6},{4,5}},
 {{0,5},{0,6},{0,7},{1,3},{1,6},{1,7},{2,4},{2,5},{2,7},{3,4},{3,6},{4,5}},
 {{0,1},{0,6},{0,7},{1,6},{1,7},{2,4},{2,5},{2,7},{3,4},{3,5},{3,6},{4,5}}};
static int skadj[5][8];
static void build_sk(){ for(int s=0;s<5;s++){ for(int v=0;v<8;v++)skadj[s][v]=0; for(int e=0;e<12;e++){int a=SK[s][e][0],b=SK[s][e][1]; skadj[s][a]|=1<<b; skadj[s][b]|=1<<a;} } }

// find isomorphism phi: my core (adj[8]) -> skeleton s; returns true and phi
static bool iso_rec(const int adj[8],const int sadj[8],int v,int* phi,int used){
  if(v==8) return true;
  for(int w=0;w<8;w++) if(!(used>>w&1)){
    bool ok=true;
    for(int u=0;u<v&&ok;u++){ bool e1=adj[v]>>u&1, e2=sadj[w]>>phi[u]&1; if(e1!=e2) ok=false; }
    if(!ok) continue;
    phi[v]=w; if(iso_rec(adj,sadj,v+1,phi,used|1<<w)) return true;
  }
  return false;
}

struct Info{ bool connected; bool simplecore; int skel; int rcore; int d33; bool survives; u64 tkey; int ncols3; };

static Info classify(const int cm[7]){
  Info I{}; 
  int rm[7]={0}; for(int j=0;j<7;j++) for(int i=0;i<7;i++) if(cm[j]>>i&1) rm[i]|=1<<j;
  // vertices 0..6 rows, 7..13 cols; adjacency as 14-bit masks
  int adj[14]; for(int i=0;i<7;i++) adj[i]=rm[i]<<7; for(int j=0;j<7;j++) adj[7+j]=cm[j];
  // connectivity
  int seen=1, frontier=1; while(frontier){ int nf=0; for(int v=0;v<14;v++) if(frontier>>v&1) nf|=adj[v]; nf&=~seen; seen|=nf; frontier=nf; }
  I.connected = (seen==(1<<14)-1);
  // survives: no 3 rows whose neighbourhood union has <=3 columns  (<=> 3 rows x 4 cols zero submatrix)
  I.survives=true;
  for(int a=0;a<7;a++)for(int b=a+1;b<7;b++)for(int c=b+1;c<7;c++){ int u=rm[a]|rm[b]|rm[c]; if(__builtin_popcount(u)<=3) I.survives=false; }
  // d33
  I.d33=0; for(int i=0;i<7;i++) for(int j=0;j<7;j++) if(rm[i]>>j&1) if(__builtin_popcount(rm[i])==3 && __builtin_popcount(cm[j])==3) I.d33++;
  // transpose key
  int tm[7]; // transpose: columns of the transpose = rows of original; but need row sums (3,3,3,3,2,2,2) order -> rows of transpose = columns sorted by degree desc
  { int idx[7]; iota(idx,idx+7,0); stable_sort(idx,idx+7,[&](int x,int y){return __builtin_popcount(cm[x])>__builtin_popcount(cm[y]);});
    for(int i=0;i<7;i++){ int v=0; for(int k=0;k<7;k++) if(rm[i]>>idx[k]&1) v|=1<<k; tm[i]=v; } I.tkey=canon(tm); }
  // core: degree-3 vertices
  int deg[14]; for(int v=0;v<14;v++) deg[v]=__builtin_popcount(adj[v]);
  int coreid[14]; int nc=0; for(int v=0;v<14;v++) coreid[v]=(deg[v]==3)?nc++:-1;
  I.simplecore=true; I.skel=-1; I.rcore=0;
  if(nc!=8){ I.simplecore=false; return I; }
  int cadj[8]={0}; int emult[8][8]={{0}};
  for(int v=0;v<14;v++) if(deg[v]==3){
    for(int u=0;u<14;u++) if(adj[v]>>u&1){
      int prev=v,cur=u; while(deg[cur]==2){ int nx=adj[cur]&~(1<<prev); int n=__builtin_ctz(nx); prev=cur; cur=n; }
      int w=cur; if(w==v){ I.simplecore=false; } else { emult[coreid[v]][coreid[w]]++; cadj[coreid[v]]|=1<<coreid[w]; }
    }
  }
  for(int a=0;a<8;a++)for(int b=0;b<8;b++) if(emult[a][b]>1) I.simplecore=false;
  if(!I.simplecore) return I;
  for(int s=0;s<5;s++){ int phi[8]; if(iso_rec(cadj,skadj[s],0,phi,0)){ I.skel=s; for(int v=0;v<7;v++) if(deg[v]==3) I.rcore|=1<<phi[coreid[v]]; break; } }
  return I;
}

static set<u64> classes;
static long long nmat=0;
static int cmask[7]; static int rowsum[7];
static vector<int> masks;
static void dfs(int j,int minidx,int n3,int n2){
  if(j==7){ for(int i=0;i<7;i++) if(rowsum[i]!=RT[i]) return; nmat++; classes.insert(canon(cmask)); return; }
  for(size_t t=minidx;t<masks.size();t++){
    int m=masks[t]; int pc=__builtin_popcount(m);
    if(pc==3&&n3==4) continue; if(pc==2&&n2==3) continue;
    bool ok=true; for(int i=0;i<7;i++) if(m>>i&1){ if(rowsum[i]+1>RT[i]){ok=false;break;} }
    if(!ok) continue;
    for(int i=0;i<7;i++) if(m>>i&1) rowsum[i]++;
    cmask[j]=m; dfs(j+1,t,n3+(pc==3),n2+(pc==2));
    for(int i=0;i<7;i++) if(m>>i&1) rowsum[i]--;
  }
}

// cubic graphs on 8 vertices: labelled count and isomorphism classes
static set<u64> cubic_classes; static long long cubic_lab=0, cubic_conn=0;
static u64 gkey(const int adj[8],const int* p){ u64 k=0; for(int a=0;a<8;a++)for(int b=a+1;b<8;b++){ k<<=1; if(adj[p[a]]>>p[b]&1) k|=1; } return k; }
static void cubic_dfs(int adj[8],int v){
  if(v==8){ cubic_lab++; int seen=1,fr=1; while(fr){int nf=0; for(int x=0;x<8;x++) if(fr>>x&1) nf|=adj[x]; nf&=~seen; seen|=nf; fr=nf;} if(seen!=255) return; cubic_conn++;
    int p[8]; iota(p,p+8,0); u64 best=~0ULL; do{ u64 k=gkey(adj,p); if(k<best)best=k; }while(next_permutation(p,p+8)); cubic_classes.insert(best); return; }
  int need=3-__builtin_popcount(adj[v]); if(need<0) return;
  // choose 'need' neighbours among higher vertices not yet adjacent, with remaining capacity
  vector<int> cand; for(int u=v+1;u<8;u++) if(!(adj[v]>>u&1) && __builtin_popcount(adj[u])<3) cand.push_back(u);
  int C=cand.size(); if(need>C) return;
  // iterate subsets of size need
  for(int s=0;s<(1<<C);s++){ if(__builtin_popcount(s)!=need) continue; for(int i=0;i<C;i++) if(s>>i&1){adj[v]|=1<<cand[i]; adj[cand[i]]|=1<<v;} cubic_dfs(adj,v+1); for(int i=0;i<C;i++) if(s>>i&1){adj[v]&=~(1<<cand[i]); adj[cand[i]]&=~(1<<v);} }
}

int main(int argc,char**argv){
  build_rowperms(); build_sk();
  string mode=argc>1?argv[1]:"enum";
  if(mode=="cubic"){ int adj[8]={0}; cubic_dfs(adj,0); printf("labelled cubic graphs on 8 vertices: %lld, connected: %lld, connected isomorphism classes: %zu\n",cubic_lab,cubic_conn,cubic_classes.size());
    // check the 5 given skeletons are pairwise non-isomorphic and cubic
    set<u64> sk; for(int s=0;s<5;s++){ int p[8]; iota(p,p+8,0); u64 best=~0ULL; do{u64 k=gkey(skadj[s],p); if(k<best)best=k;}while(next_permutation(p,p+8)); sk.insert(best); bool cub=true; for(int v=0;v<8;v++) if(__builtin_popcount(skadj[s][v])!=3) cub=false; printf("S%d cubic=%d key=%llx\n",s+1,(int)cub,best); }
    printf("given skeletons: %zu distinct classes; all in the enumerated set: %d\n",sk.size(),(int)includes(cubic_classes.begin(),cubic_classes.end(),sk.begin(),sk.end()));
    return 0; }
  if(mode=="canon"){ int cm[7]; while(scanf("%d %d %d %d %d %d %d",&cm[0],&cm[1],&cm[2],&cm[3],&cm[4],&cm[5],&cm[6])==7){ Info I=classify(cm); printf("%016llx %016llx %d %d %d %d %d %d\n",canon(cm),I.tkey,(int)I.connected,(int)I.simplecore,I.skel,I.rcore,I.d33,(int)I.survives);} return 0; }
  for(int m=0;m<128;m++){ int pc=__builtin_popcount(m); if(pc==2||pc==3) masks.push_back(m); }
  dfs(0,0,0,0);
  fprintf(stderr,"column-sorted matrices: %lld, canonical classes: %zu\n",nmat,classes.size());
  int cnt_conn=0,cnt_simple=0;
  for(u64 k:classes){ int cm[7]; unpack(k,cm); Info I=classify(cm); if(I.connected)cnt_conn++; if(I.connected&&I.simplecore)cnt_simple++;
    printf("%016llx %016llx %d %d %d %d %d %d\n",k,I.tkey,(int)I.connected,(int)I.simplecore,I.skel,I.rcore,I.d33,(int)I.survives); }
  fprintf(stderr,"connected: %d; connected with simple cubic core: %d\n",cnt_conn,cnt_simple);
}
