// subset-DP: exists allocation with min_i v_i(A_i) >= q ?  and exact max-min.
// input: n m q, then n lines of m ints (valuations). Output: maxmin.
// mode: "feas" prints 1/0 for >= q; "max" prints exact max-min.
#include <bits/stdc++.h>
using namespace std;
int main(int argc, char** argv){
    string mode = argc>1 ? argv[1] : "max";
    int n,m,q;
    while (scanf("%d %d %d",&n,&m,&q)==3){
        vector<vector<int>> v(n, vector<int>(m));
        for(int i=0;i<n;i++) for(int g=0;g<m;g++) scanf("%d",&v[i][g]);
        int full=(1<<m)-1;
        vector<vector<int>> sv(n, vector<int>(1<<m,0));
        for(int i=0;i<n;i++) for(int S=1;S<=full;S++){ int low=S&-S; int g=__builtin_ctz(S); sv[i][S]=sv[i][S^low]+v[i][g]; }
        if (mode=="feas"){
            // F_i(S) bool: agents i..n-1 can each get >= q from S
            vector<char> F(1<<m), G(1<<m);
            for(int S=0;S<=full;S++) F[S] = sv[n-1][S]>=q;
            for(int i=n-2;i>=0;i--){
                for(int S=0;S<=full;S++){
                    char ok=0;
                    if (F[S]) { // quick: if superset works for later agents, need B with sv>=q and F[S^B]
                    }
                    for(int B=S; B; B=(B-1)&S){ if (sv[i][B]>=q && F[S^B]) {ok=1;break;} }
                    G[S]=ok;
                }
                swap(F,G);
            }
            printf("%d\n", (int)F[full]);
        } else {
            vector<int> F(1<<m), G(1<<m);
            for(int S=0;S<=full;S++) F[S]=sv[n-1][S];
            for(int i=n-2;i>=0;i--){
                for(int S=0;S<=full;S++){
                    int best=0;
                    for(int B=S; ; B=(B-1)&S){ int val=min(sv[i][B],F[S^B]); if(val>best)best=val; if(B==0)break; }
                    G[S]=best;
                }
                swap(F,G);
            }
            printf("%d\n", F[full]);
        }
        fflush(stdout);
    }
}
