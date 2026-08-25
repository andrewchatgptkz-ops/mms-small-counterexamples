// RECONSTRUCTION, NOT THE ORIGINAL SEARCH SOURCE.
//
// The original exploratory incidence-pattern search was not retained. This
// standalone C++17 program reconstructs the parts that are recoverable from the
// checkpoint and verification files:
//   * simple m-edge subgraphs of a labelled 4 x 4 row/column incidence matrix;
//   * positive integer row/column valuations whose four row/column witness
//     bundles each sum to T;
//   * the exact score based on two disjoint inclusion-minimal row bundles and
//     two disjoint inclusion-minimal column bundles.
//
// The local-move and simulated-annealing policy below is a faithful plausible
// reconstruction, but its exact move schedule, seeds, and pattern order were not
// preserved. Do not cite those reconstructed choices as historical run data.
//
// Build:
//   g++ -O3 -std=c++17 reconstructed_incidence_search.cpp -o reconstructed_search
//
// Safe provenance/replay modes (do not launch a search):
//   ./reconstructed_search --mode inventory
//   ./reconstructed_search --mode replay
//
// Reconstructed search mode:
//   ./reconstructed_search --mode search --m 11 --target 60
//       --seed 2026082611 --min-degree 1 --restarts 16 --steps 20000
//       --shuffle-patterns 1 --log run11.jsonl
//
// The seed in this example is newly chosen for the reconstruction. It is NOT a
// recovered seed from the historical run.

#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint16_t;
using Count = std::uint64_t;

constexpr int SIDE = 4;
constexpr int CELLS = 16;

struct Pattern {
    Mask mask = 0;
    std::vector<std::pair<int,int>> cells;  // good index -> (row,column)
    std::array<std::vector<int>, SIDE> rows;
    std::array<std::vector<int>, SIDE> cols;
};

struct PackingStats {
    int minimal_row_bundles = 0;
    int minimal_col_bundles = 0;
    int disjoint_row_pairs = 0;
    int disjoint_col_pairs = 0;
    int row_pairs_with_compatible_col_pair = 0;
    Count compatible_pair_pairs = 0;  // the exact search score
};

struct Candidate {
    std::vector<int> row_values;
    std::vector<int> col_values;
    PackingStats stats;
};

struct Options {
    std::string mode = "replay";
    int m = 11;
    int target = 60;
    std::uint64_t seed = 0;
    bool seed_explicit = false;
    int restarts = 16;
    int steps = 20000;
    int min_degree = 1;
    bool symmetry_reduce = false;
    bool shuffle_patterns = false;
    std::string log_path;
};

int popcount(Mask x) {
#if defined(__GNUG__)
    return __builtin_popcount(static_cast<unsigned>(x));
#else
    int out = 0;
    while (x) { x &= static_cast<Mask>(x - 1); ++out; }
    return out;
#endif
}

Pattern make_pattern(Mask mask) {
    Pattern p;
    p.mask = mask;
    for (int cell = 0; cell < CELLS; ++cell) {
        if (!(mask & static_cast<Mask>(Mask{1} << cell))) continue;
        const int r = cell / SIDE;
        const int c = cell % SIDE;
        const int g = static_cast<int>(p.cells.size());
        p.cells.emplace_back(r,c);
        p.rows[r].push_back(g);
        p.cols[c].push_back(g);
    }
    return p;
}

Pattern make_pattern_from_good_coordinates(
    const std::vector<std::pair<int,int>>& coords
) {
    Pattern p;
    p.cells = coords;
    for (int g = 0; g < static_cast<int>(coords.size()); ++g) {
        const auto [r,c] = coords[g];
        if (r < 0 || r >= SIDE || c < 0 || c >= SIDE) {
            throw std::runtime_error("bad incidence coordinate");
        }
        const Mask bit = static_cast<Mask>(Mask{1} << (SIDE*r+c));
        if (p.mask & bit) throw std::runtime_error("incidence pattern is not simple");
        p.mask = static_cast<Mask>(p.mask | bit);
        p.rows[r].push_back(g);
        p.cols[c].push_back(g);
    }
    return p;
}

std::array<int,SIDE> row_degrees(Mask mask) {
    std::array<int,SIDE> d{};
    for (int cell = 0; cell < CELLS; ++cell) {
        if (mask & static_cast<Mask>(Mask{1} << cell)) ++d[cell/SIDE];
    }
    return d;
}

std::array<int,SIDE> col_degrees(Mask mask) {
    std::array<int,SIDE> d{};
    for (int cell = 0; cell < CELLS; ++cell) {
        if (mask & static_cast<Mask>(Mask{1} << cell)) ++d[cell%SIDE];
    }
    return d;
}

bool all_degrees_at_least(Mask mask, int minimum) {
    const auto rd = row_degrees(mask);
    const auto cd = col_degrees(mask);
    return std::all_of(rd.begin(),rd.end(),[&](int x){return x>=minimum;}) &&
           std::all_of(cd.begin(),cd.end(),[&](int x){return x>=minimum;});
}

bool connected_bipartite(Mask mask) {
    std::array<std::vector<int>,8> adj;
    for (int cell=0; cell<CELLS; ++cell) {
        if (!(mask & static_cast<Mask>(Mask{1} << cell))) continue;
        const int r=cell/SIDE, c=cell%SIDE;
        adj[r].push_back(SIDE+c);
        adj[SIDE+c].push_back(r);
    }
    std::array<bool,8> seen{};
    std::vector<int> stack{0};
    seen[0]=true;
    while(!stack.empty()) {
        const int v=stack.back(); stack.pop_back();
        for(int w:adj[v]) if(!seen[w]) { seen[w]=true; stack.push_back(w); }
    }
    return std::all_of(seen.begin(),seen.end(),[](bool x){return x;});
}

std::vector<std::array<int,SIDE>> permutations4() {
    std::array<int,SIDE> p{{0,1,2,3}};
    std::vector<std::array<int,SIDE>> out;
    do { out.push_back(p); } while(std::next_permutation(p.begin(),p.end()));
    return out;
}

Mask permute_pattern(
    Mask mask,
    const std::array<int,SIDE>& rp,
    const std::array<int,SIDE>& cp
) {
    Mask out=0;
    for(int r=0;r<SIDE;++r) for(int c=0;c<SIDE;++c) {
        const int oldcell=SIDE*r+c;
        if (mask & static_cast<Mask>(Mask{1} << oldcell)) {
            const int newcell=SIDE*rp[r]+cp[c];
            out=static_cast<Mask>(out | static_cast<Mask>(Mask{1} << newcell));
        }
    }
    return out;
}

Mask canonical_pattern(Mask mask) {
    static const auto perms=permutations4();
    Mask best=std::numeric_limits<Mask>::max();
    for(const auto& rp:perms) for(const auto& cp:perms) {
        best=std::min(best,permute_pattern(mask,rp,cp));
    }
    return best;
}

std::vector<Mask> enumerate_patterns(int m, bool symmetry_reduce, int min_degree) {
    std::vector<Mask> out;
    std::set<Mask> seen_orbits;
    for(std::uint32_t raw=0; raw < (1u<<CELLS); ++raw) {
        const Mask mask=static_cast<Mask>(raw);
        if(popcount(mask)!=m) continue;
        if(!all_degrees_at_least(mask,min_degree)) continue;
        if(symmetry_reduce) {
            const Mask canon=canonical_pattern(mask);
            if(!seen_orbits.insert(canon).second) continue;
            out.push_back(canon);
        } else {
            out.push_back(mask);
        }
    }
    return out;
}

std::vector<int> subset_sums(const std::vector<int>& values) {
    const int m=static_cast<int>(values.size());
    std::vector<int> sums(1<<m,0);
    for(int mask=1;mask<(1<<m);++mask) {
        const int bit=mask & -mask;
#if defined(__GNUG__)
        const int j=__builtin_ctz(static_cast<unsigned>(bit));
#else
        int j=0; while((1<<j)!=bit) ++j;
#endif
        sums[mask]=sums[mask^bit]+values[j];
    }
    return sums;
}

std::vector<int> minimal_threshold_bundles(
    const std::vector<int>& values,
    int target
) {
    const int m=static_cast<int>(values.size());
    const auto sums=subset_sums(values);
    std::vector<int> out;
    for(int mask=1;mask<(1<<m);++mask) {
        if(sums[mask]<target) continue;
        bool minimal=true;
        for(int j=0;j<m;++j) if(mask&(1<<j)) {
            if(sums[mask^(1<<j)]>=target) { minimal=false; break; }
        }
        if(minimal) out.push_back(mask);
    }
    return out;
}

std::vector<int> disjoint_pair_unions(const std::vector<int>& bundles) {
    std::vector<int> out;
    for(std::size_t i=0;i<bundles.size();++i) {
        for(std::size_t j=i+1;j<bundles.size();++j) {
            if((bundles[i]&bundles[j])==0) out.push_back(bundles[i]|bundles[j]);
        }
    }
    return out;
}

PackingStats exact_packing_score(
    const std::vector<int>& row_values,
    const std::vector<int>& col_values,
    int target
) {
    if(row_values.size()!=col_values.size()) throw std::runtime_error("row/column length mismatch");
    const int m=static_cast<int>(row_values.size());
    if(m<=0 || m>15) throw std::runtime_error("mask scorer expects 1..15 goods");
    const int full=(1<<m)-1;

    const auto minr=minimal_threshold_bundles(row_values,target);
    const auto minc=minimal_threshold_bundles(col_values,target);
    const auto rpairs=disjoint_pair_unions(minr);
    const auto cpairs=disjoint_pair_unions(minc);

    std::vector<Count> contained(1<<m,0);
    for(int u:cpairs) ++contained[u];
    for(int bit=0;bit<m;++bit) {
        const int flag=1<<bit;
        for(int mask=0;mask<(1<<m);++mask) if(mask&flag) {
            contained[mask]+=contained[mask^flag];
        }
    }

    PackingStats st;
    st.minimal_row_bundles=static_cast<int>(minr.size());
    st.minimal_col_bundles=static_cast<int>(minc.size());
    st.disjoint_row_pairs=static_cast<int>(rpairs.size());
    st.disjoint_col_pairs=static_cast<int>(cpairs.size());
    for(int u:rpairs) {
        const Count n=contained[full^u];
        if(n) ++st.row_pairs_with_compatible_col_pair;
        st.compatible_pair_pairs+=n;
    }
    return st;
}

bool witness_sums_ok(
    const std::vector<int>& values,
    const std::array<std::vector<int>,SIDE>& groups,
    int target
) {
    if(values.empty()) return false;
    std::vector<int> seen(values.size(),0);
    for(const auto& group:groups) {
        int sum=0;
        for(int g:group) {
            if(g<0 || g>=static_cast<int>(values.size())) return false;
            ++seen[g]; sum+=values[g];
        }
        if(sum!=target) return false;
    }
    return std::all_of(seen.begin(),seen.end(),[](int x){return x==1;});
}

std::vector<int> positive_composition(int total, int parts, std::mt19937_64& rng) {
    if(parts<=0 || total<parts) throw std::runtime_error("positive composition impossible");
    if(parts==1) return {total};
    std::vector<int> cuts(total-1);
    std::iota(cuts.begin(),cuts.end(),1);
    std::shuffle(cuts.begin(),cuts.end(),rng);
    cuts.resize(parts-1);
    std::sort(cuts.begin(),cuts.end());
    std::vector<int> out;
    int last=0;
    for(int x:cuts) { out.push_back(x-last); last=x; }
    out.push_back(total-last);
    return out;
}

std::vector<int> random_values_on_groups(
    int m,
    const std::array<std::vector<int>,SIDE>& groups,
    int target,
    std::mt19937_64& rng
) {
    std::vector<int> values(m,0);
    for(const auto& group:groups) {
        const auto comp=positive_composition(target,static_cast<int>(group.size()),rng);
        for(std::size_t k=0;k<group.size();++k) values[group[k]]=comp[k];
    }
    return values;
}

struct Move {
    int a=-1,b=-1;
    int olda=0,oldb=0;
};

Move random_transfer(
    std::vector<int>& values,
    const std::array<std::vector<int>,SIDE>& groups,
    std::mt19937_64& rng
) {
    // Choose only from witness groups on which a positive preserving transfer
    // actually exists. This avoids a spurious failure on patterns containing
    // singleton rows or columns.
    std::vector<int> movable_groups;
    for(int k=0;k<SIDE;++k) {
        if(groups[k].size()<2) continue;
        if(std::any_of(groups[k].begin(),groups[k].end(),
                       [&](int g){return values[g]>1;})) {
            movable_groups.push_back(k);
        }
    }
    if(movable_groups.empty()) {
        throw std::runtime_error("could not construct a preserving transfer move");
    }
    std::uniform_int_distribution<int> group_dist(
        0,static_cast<int>(movable_groups.size())-1);
    const auto& group=groups[movable_groups[group_dist(rng)]];

    std::vector<int> sources;
    for(int g:group) if(values[g]>1) sources.push_back(g);
    std::uniform_int_distribution<int> src_dist(0,static_cast<int>(sources.size())-1);
    const int a=sources[src_dist(rng)];

    std::vector<int> dests;
    for(int g:group) if(g!=a) dests.push_back(g);
    std::uniform_int_distribution<int> dst_dist(0,static_cast<int>(dests.size())-1);
    const int b=dests[dst_dist(rng)];

    const int max_delta=std::max(1,std::min(values[a]-1,8));
    std::uniform_int_distribution<int> delta_dist(1,max_delta);
    const int delta=delta_dist(rng);
    Move mv{a,b,values[a],values[b]};
    values[a]-=delta;
    values[b]+=delta;
    return mv;
}

void undo_transfer(std::vector<int>& values,const Move& mv) {
    values[mv.a]=mv.olda;
    values[mv.b]=mv.oldb;
}

double energy(const PackingStats& s) {
    // The historical exact criterion is score==0. Log scaling is a reconstructed
    // annealing choice so that very large count differences do not dominate.
    return std::log1p(static_cast<double>(s.compatible_pair_pairs));
}

std::string stats_json(const PackingStats& s) {
    std::ostringstream o;
    o << "{\"minimal_row\":" << s.minimal_row_bundles
      << ",\"minimal_col\":" << s.minimal_col_bundles
      << ",\"row_pairs\":" << s.disjoint_row_pairs
      << ",\"col_pairs\":" << s.disjoint_col_pairs
      << ",\"compatible_row_pairs\":" << s.row_pairs_with_compatible_col_pair
      << ",\"score\":" << s.compatible_pair_pairs << "}";
    return o.str();
}

std::string vector_json(const std::vector<int>& v) {
    std::ostringstream o; o << "[";
    for(std::size_t i=0;i<v.size();++i) { if(i) o << ","; o << v[i]; }
    o << "]"; return o.str();
}

std::string hex_mask(Mask mask) {
    std::ostringstream o; o << "0x" << std::hex << std::setw(4) << std::setfill('0')
                            << static_cast<unsigned>(mask);
    return o.str();
}

void print_pattern_inventory_one(int m) {
    std::size_t raw=0,nonempty=0,mindeg2=0,connected=0;
    std::set<Mask> all_orbits,nonempty_orbits,mindeg2_orbits;
    for(std::uint32_t x=0;x<(1u<<CELLS);++x) {
        const Mask mask=static_cast<Mask>(x);
        if(popcount(mask)!=m) continue;
        ++raw; all_orbits.insert(canonical_pattern(mask));
        if(all_degrees_at_least(mask,1)) {
            ++nonempty; nonempty_orbits.insert(canonical_pattern(mask));
        }
        if(all_degrees_at_least(mask,2)) {
            ++mindeg2; mindeg2_orbits.insert(canonical_pattern(mask));
        }
        if(connected_bipartite(mask)) ++connected;
    }
    std::cout << "m=" << m
              << " raw_labelled=" << raw
              << " nonempty_rows_cols=" << nonempty
              << " min_degree_2=" << mindeg2
              << " connected=" << connected
              << " row_col_orbits_all=" << all_orbits.size()
              << " row_col_orbits_nonempty=" << nonempty_orbits.size()
              << " row_col_orbits_min_degree_2=" << mindeg2_orbits.size()
              << "\n";
}

void replay_candidate(
    const std::string& name,
    const std::vector<std::pair<int,int>>& coords,
    const std::vector<int>& r,
    const std::vector<int>& c,
    int target,
    const std::string& incidence_status
) {
    const Pattern p=make_pattern_from_good_coordinates(coords);
    const auto st=exact_packing_score(r,c,target);
    const int sr=std::accumulate(r.begin(),r.end(),0);
    const int sc=std::accumulate(c.begin(),c.end(),0);
    std::cout << "candidate=" << name << "\n"
              << "  incidence_status=" << incidence_status << "\n"
              << "  goods=" << r.size() << " target=" << target
              << " pattern_mask=" << hex_mask(p.mask)
              << " canonical_mask=" << hex_mask(canonical_pattern(p.mask)) << "\n"
              << "  row_values=" << vector_json(r) << " total=" << sr << "\n"
              << "  col_values=" << vector_json(c) << " total=" << sc << "\n"
              << "  row_witness_sums_ok=" << (witness_sums_ok(r,p.rows,target)?"true":"false")
              << " col_witness_sums_ok=" << (witness_sums_ok(c,p.cols,target)?"true":"false") << "\n"
              << "  packing_stats=" << stats_json(st) << "\n";
    if(!witness_sums_ok(r,p.rows,target) || !witness_sums_ok(c,p.cols,target) ||
       sr!=4*target || sc!=4*target || st.compatible_pair_pairs!=0) {
        throw std::runtime_error("replay candidate failed");
    }
}

void run_replay() {
    // Eleven-good incidence is RECOVERED EXACTLY from simplify_candidate11.py
    // and policy_simplify.py.
    replay_candidate(
        "11-good initial T=60",
        {{0,0},{0,1},{0,3},{1,1},{1,2},{1,3},{2,0},{2,1},{3,0},{3,2},{3,3}},
        {15,22,23,16,13,31,39,21,1,55,4},
        {9,21,25,19,4,33,50,20,1,56,2},
        60,
        "recovered exactly from retained simplification scripts"
    );

    // For the twelve-good vector, the original incidence assignment was not
    // retained. The representative below is INFERRED from the unique row-type
    // exact-60 partition and the first of four compatible exact-60 column-type
    // partitions. replay_initial_candidates.py lists all four possibilities.
    replay_candidate(
        "12-good initial T=60",
        {{0,0},{0,1},{1,2},{1,1},{1,3},{2,2},{2,0},{2,3},{2,1},{3,2},{3,0},{3,3}},
        {44,16,8,42,10,34,1,24,1,14,14,32},
        {46,19,11,40,6,37,1,20,1,12,13,34},
        60,
        "inferred representative; original assignment not retained"
    );
}

bool search_pattern(
    const Pattern& p,
    const Options& opt,
    std::mt19937_64& rng,
    Candidate& hit,
    Count& best_score
) {
    const int m=static_cast<int>(p.cells.size());
    std::uniform_real_distribution<double> u01(0.0,1.0);
    best_score=std::numeric_limits<Count>::max();

    for(int restart=0;restart<opt.restarts;++restart) {
        Candidate cur;
        cur.row_values=random_values_on_groups(m,p.rows,opt.target,rng);
        cur.col_values=random_values_on_groups(m,p.cols,opt.target,rng);
        cur.stats=exact_packing_score(cur.row_values,cur.col_values,opt.target);
        best_score=std::min(best_score,cur.stats.compatible_pair_pairs);
        if(cur.stats.compatible_pair_pairs==0) { hit=cur; return true; }

        for(int step=0;step<opt.steps;++step) {
            const double frac=(opt.steps<=1)?1.0:static_cast<double>(step)/(opt.steps-1);
            const double temperature=std::exp((1.0-frac)*std::log(1.5)+frac*std::log(0.01));
            const bool change_row=(u01(rng)<0.5);
            auto& values=change_row?cur.row_values:cur.col_values;
            const auto& groups=change_row?p.rows:p.cols;
            const Move mv=random_transfer(values,groups,rng);
            const PackingStats next=exact_packing_score(cur.row_values,cur.col_values,opt.target);
            const double de=energy(next)-energy(cur.stats);
            const bool accept=(de<=0.0) || (u01(rng)<std::exp(-de/temperature));
            if(accept) {
                cur.stats=next;
                best_score=std::min(best_score,cur.stats.compatible_pair_pairs);
                if(cur.stats.compatible_pair_pairs==0) { hit=cur; return true; }
            } else {
                undo_transfer(values,mv);
            }
        }
    }
    return false;
}

void run_search(const Options& opt) {
    if(opt.m!=11 && opt.m!=12) throw std::runtime_error("reconstruction supports m=11 or 12");
    if(opt.target<3) throw std::runtime_error("target too small");

    // The historical prefilter is not recoverable. min_degree=1 means every
    // row and column witness is nonempty and is the broadest natural family.
    // min_degree=2 is available because it was a plausible exploratory filter.
    if(opt.min_degree<1 || opt.min_degree>2) {
        throw std::runtime_error("min-degree must be 1 or 2");
    }
    if(!opt.seed_explicit) {
        throw std::runtime_error("search mode requires an explicit --seed; no historical seed was recovered");
    }
    auto patterns=enumerate_patterns(opt.m,opt.symmetry_reduce,opt.min_degree);
    std::mt19937_64 rng(opt.seed);
    if(opt.shuffle_patterns) std::shuffle(patterns.begin(),patterns.end(),rng);

    std::ofstream log;
    if(!opt.log_path.empty()) {
        log.open(opt.log_path);
        if(!log) throw std::runtime_error("cannot open log path");
        log << "{\"record_type\":\"config\""
            << ",\"provenance\":\"RECONSTRUCTION_NOT_HISTORICAL\""
            << ",\"m\":" << opt.m
            << ",\"target\":" << opt.target
            << ",\"seed\":" << opt.seed
            << ",\"min_degree\":" << opt.min_degree
            << ",\"symmetry_reduce\":" << (opt.symmetry_reduce?"true":"false")
            << ",\"shuffle_patterns\":" << (opt.shuffle_patterns?"true":"false")
            << ",\"restarts\":" << opt.restarts
            << ",\"steps\":" << opt.steps
            << ",\"patterns_total\":" << patterns.size()
            << "}" << "\n";
        log.flush();
    }

    const auto started=std::chrono::steady_clock::now();
    std::size_t tried=0;
    for(Mask mask:patterns) {
        ++tried;
        const Pattern p=make_pattern(mask);
        Candidate hit;
        Count best=0;
        const bool ok=search_pattern(p,opt,rng,hit,best);
        const double elapsed=std::chrono::duration<double>(
            std::chrono::steady_clock::now()-started).count();
        if(log) {
            log << "{\"record_type\":\"pattern\""
                << ",\"pattern_ordinal\":" << tried
                << ",\"pattern_mask\":\"" << hex_mask(mask) << "\""
                << ",\"canonical_mask\":\"" << hex_mask(canonical_pattern(mask)) << "\""
                << ",\"best_score\":" << best
                << ",\"elapsed_seconds\":" << std::setprecision(12) << elapsed
                << ",\"hit\":" << (ok?"true":"false") << "}" << "\n";
            log.flush();
        }
        if(ok) {
            std::cout << "RECONSTRUCTED_SEARCH_HIT\n"
                      << "patterns_tried=" << tried << "\n"
                      << "elapsed_seconds=" << std::setprecision(12) << elapsed << "\n"
                      << "seed=" << opt.seed << "\n"
                      << "pattern_mask=" << hex_mask(mask) << "\n"
                      << "row_values=" << vector_json(hit.row_values) << "\n"
                      << "col_values=" << vector_json(hit.col_values) << "\n"
                      << "packing_stats=" << stats_json(hit.stats) << "\n";
            return;
        }
    }
    const double elapsed=std::chrono::duration<double>(
        std::chrono::steady_clock::now()-started).count();
    std::cout << "RECONSTRUCTED_SEARCH_NO_HIT\n"
              << "patterns_tried=" << tried << "\n"
              << "elapsed_seconds=" << std::setprecision(12) << elapsed << "\n";
}

void print_help() {
    std::cout
      << "Usage: reconstructed_search [options]\n"
      << "  --mode inventory|replay|search   default replay\n"
      << "  --m 11|12                        default 11\n"
      << "  --target N                       default 60\n"
      << "  --seed N                         reconstruction seed\n"
      << "  --restarts N                     per pattern\n"
      << "  --steps N                        per restart\n"
      << "  --min-degree 1|2                 default 1\n"
      << "  --symmetry-reduce 0|1            default 0 (all labelled patterns)\n"
      << "  --shuffle-patterns 0|1           default 0\n"
      << "  --log PATH                       JSON-lines log\n";
}

Options parse_options(int argc,char** argv) {
    Options o;
    for(int i=1;i<argc;++i) {
        const std::string a=argv[i];
        auto next=[&]()->std::string {
            if(i+1>=argc) throw std::runtime_error("missing value after "+a);
            return argv[++i];
        };
        if(a=="--help" || a=="-h") { print_help(); std::exit(0); }
        else if(a=="--mode") o.mode=next();
        else if(a=="--m") o.m=std::stoi(next());
        else if(a=="--target") o.target=std::stoi(next());
        else if(a=="--seed") { o.seed=std::stoull(next()); o.seed_explicit=true; }
        else if(a=="--restarts") o.restarts=std::stoi(next());
        else if(a=="--steps") o.steps=std::stoi(next());
        else if(a=="--min-degree") o.min_degree=std::stoi(next());
        else if(a=="--symmetry-reduce") o.symmetry_reduce=(std::stoi(next())!=0);
        else if(a=="--shuffle-patterns") o.shuffle_patterns=(std::stoi(next())!=0);
        else if(a=="--log") o.log_path=next();
        else throw std::runtime_error("unknown option: "+a);
    }
    return o;
}

} // namespace

int main(int argc,char** argv) {
    try {
        const Options opt=parse_options(argc,argv);
        if(opt.mode=="inventory") {
            print_pattern_inventory_one(11);
            print_pattern_inventory_one(12);
        } else if(opt.mode=="replay") {
            run_replay();
        } else if(opt.mode=="search") {
            run_search(opt);
        } else {
            throw std::runtime_error("unknown mode: "+opt.mode);
        }
        return 0;
    } catch(const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << "\n";
        return 1;
    }
}
