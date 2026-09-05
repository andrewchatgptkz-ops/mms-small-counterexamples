// Find an allocation with min_i v_i(A_i) >= q, output bundle masks; or "none".
#include <bits/stdc++.h>
using namespace std;
int main(){
    int n,m,q; if(scanf("%d %d %d",&n,&m,&q)!=3) return 1;
    vector<vector<int>> v(n, vector<int>(m));
    for(int i=0;i<n;i++) for(int g=0;g<m;g++) if(scanf("%d",&v[i][g])!=1) return 1;
    int full=(1<<m)-1;
    vector<vector<int>> sv(n, vector<int>(1<<m,0));
    for(int i=0;i<n;i++) for(int S=1;S<=full;S++){ int low=S&-S; sv[i][S]=sv[i][S^low]+v[i][__builtin_ctz(S)]; }
    // F[i][S]: agents i..n-1 can each get >= q from S
    vector<vector<char>> F(n, vector<char>(1<<m,0));
    for(int S=0;S<=full;S++) F[n-1][S] = sv[n-1][S]>=q;
    for(int i=n-2;i>=0;i--){
        for(int S=0;S<=full;S++){
            char ok=0;
            for(int B=S; B; B=(B-1)&S){ if(sv[i][B]>=q && F[i+1][S^B]) {ok=1;break;} }
            F[i][S]=ok;
        }
    }
    if(!F[0][full]){ printf("none\n"); return 0; }
    int S=full;
    for(int i=0;i<n-1;i++){
        for(int B=S; B; B=(B-1)&S){ if(sv[i][B]>=q && F[i+1][S^B]) { printf("%d ", B); S^=B; break; } }
    }
    printf("%d\n", S);
}
