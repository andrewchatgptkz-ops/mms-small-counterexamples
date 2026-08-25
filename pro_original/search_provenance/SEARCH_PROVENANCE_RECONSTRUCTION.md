# Provenance of the sparse 4×4 incidence search

## Bottom line

The original exploratory source cell/script and its run log were **not retained**. I could not recover them from the first archive, the surviving work files, temporary/history locations, or the retained conversation transcript. Therefore the following historical fields are unknown and must not be filled in by inference:

- original pseudorandom generator and seed, if a seeded generator was used;
- exact order in which incidence patterns were visited;
- whether row/column-isomorphic patterns were collapsed before the search;
- any degree or connectivity prefilter used in the historical run;
- the exact scalar objective or acceptance schedule used between exact feasibility tests;
- number of patterns visited before the first 11-good hit;
- elapsed time from search start to that hit.

The only surviving top-level timing is `35m 18s` for the entire original task. It includes literature work, several earlier approaches, synthesis, simplification, and verification, so it is **not** a timing for the incidence search and is not reported as one.

This directory now contains a clearly marked reconstruction, not a falsely back-filled “original” log.

## Status labels used below

- **RECOVERED**: literally present in surviving files or uniquely forced by them.
- **DERIVED**: recomputed exactly from recovered vectors or constraints.
- **RECONSTRUCTED**: a plausible implementation choice needed to make a runnable search driver, but not historical evidence.

## What is recovered

### Search normal form — RECOVERED

There are two valuation types, each repeated twice. A good is an edge of a simple bipartite graph with four row vertices and four column vertices. For a target `T`:

- the row-type valuation sums to exactly `T` on the incident goods of each row vertex;
- the column-type valuation sums to exactly `T` on the incident goods of each column vertex;
- all item values are positive integers in the reported hits.

Each valuation row therefore totals `4T`, while its four designated witness bundles each have value `T`. Hence its exact MMS is `T`.

### Exact zero/nonzero feasibility criterion — RECOVERED

For a valuation vector `v`, let `M(v,T)` be the inclusion-minimal subsets of goods with value at least `T`. Let

- `P_R` be the unordered pairs of disjoint bundles from `M(R,T)`;
- `P_C` be the unordered pairs of disjoint bundles from `M(C,T)`.

The exact score used in the reconstruction is

```text
score(R,C,T)
  = number of (p_R,p_C) in P_R × P_C
    such that union(p_R) is disjoint from union(p_C).
```

The zero test itself is exact, independently of how a stochastic search chooses to minimize it:

1. Every bundle of value at least `T` contains an inclusion-minimal such bundle, because values are nonnegative.
2. Thus any allocation giving two row agents and two column agents value at least `T` contains four mutually disjoint minimal threshold bundles, two of each type.
3. Conversely, any such four mutually disjoint bundles can be extended to a complete allocation by assigning leftover goods arbitrarily.

Therefore an MMS allocation exists exactly when `score > 0`; a search hit is exactly `score == 0`.

The scorer in `reconstructed_incidence_search.cpp` computes this count without a quadratic cross-product. It tabulates column-pair unions, applies a subset-zeta transform, and queries how many column-pair unions fit in the complement of each row-pair union.

### Initial 11-good hit — RECOVERED

```text
R11 = 15 22 23 16 13 31 39 21  1 55  4
C11 =  9 21 25 19  4 33 50 20  1 56  2
T   = 60
```

The witness groups literally retained in both simplification scripts are

```text
rows: {g1,g2,g3} | {g4,g5,g6} | {g7,g8} | {g9,g10,g11}
cols: {g1,g7,g9} | {g2,g4,g8} | {g5,g10} | {g3,g6,g11}
```

With that retained row/column labeling, the good coordinates are

```text
g1=(1,1)  g2=(1,2)  g3=(1,4)
g4=(2,2)  g5=(2,3)  g6=(2,4)
g7=(3,1)  g8=(3,2)
g9=(4,1)  g10=(4,3) g11=(4,4)
```

The row-major 16-bit pattern mask is `0xd3eb`; its canonical mask under independent row and column permutations is `0x37de`. Row and column labels themselves have no mathematical significance.

Exact replay gives

```text
minimal row bundles       52
minimal column bundles    38
disjoint row pairs       409
disjoint column pairs    257
compatible row pairs       0
score                       0
```

The row and column exact-60 partitions are each unique as unordered partitions, which independently recovers the same incidence pattern up to row/column relabeling.

### Initial 12-good hit — vectors RECOVERED, incidence not uniquely recoverable

```text
R12 = 44 16  8 42 10 34  1 24  1 14 14 32
C12 = 46 19 11 40  6 37  1 20  1 12 13 34
T   = 60
```

Exact replay gives

```text
minimal row bundles       64
minimal column bundles    65
disjoint row pairs       624
disjoint column pairs    669
compatible row pairs       0
score                       0
```

The row vector has one exact-60 four-partition:

```text
{g1,g2} | {g3,g4,g5} | {g6,g7,g8,g9} | {g10,g11,g12}.
```

The column vector has four exact-60 four-partitions. All four combine with the row partition to form a simple 4×4 incidence assignment, and they occupy **two different row/column-isomorphism orbits**, with canonical masks `0x3def` and `0x37df`. No surviving file says which orbit was used by the original stochastic search. `replay_initial_candidates.py` prints all four assignments. Consequently the 12-good incidence pattern must be reported as unresolved, not guessed.

## Exact incidence-pattern inventory — DERIVED

`reconstructed_incidence_search.cpp --mode inventory` enumerates all `m`-edge subsets of the sixteen cells and independently canonicalizes them under `S4 × S4`.

```text
m   all labelled   no empty row/col   min degree >=2   all orbits   nonempty orbits   min-degree-2 orbits
11       4,368            4,272              2,304          21             19                  8
12       1,820            1,812              1,428          16             14                 10
```

For these edge counts, every pattern with no empty row or column is connected; the program also checks this directly.

These numbers describe the possible search universes. They do **not** reveal which universe the historical code chose or how many patterns it reached before the hit.

## Runnable reconstruction — RECONSTRUCTED

`reconstructed_incidence_search.cpp` contains three modes:

```bash
# Exact inventory only
g++ -O3 -std=c++17 reconstructed_incidence_search.cpp -o reconstructed_search
./reconstructed_search --mode inventory

# Exact replay of the retained T=60 vectors; no stochastic search
./reconstructed_search --mode replay

# Optional reconstructed search driver
./reconstructed_search --mode search --m 11 --target 60 \
  --seed 2026082611 --min-degree 1 --restarts 16 --steps 20000 \
  --shuffle-patterns 1 --log reconstructed_run11.jsonl
```

Search mode requires an explicit seed so that no default can be mistaken for a recovered historical seed. The example seed `2026082611` is newly chosen for the reconstruction.

The following mechanics are **RECONSTRUCTED**:

1. Enumerate simple 4×4 patterns, optionally modulo row/column symmetry.
2. For each pattern, initialize the row values by a random positive composition of `T` independently on each row, and initialize column values analogously on each column.
3. Make local moves by transferring a positive integer amount between two goods in one witness row or column. This preserves positivity and all four witness sums.
4. Recompute the exact pair-of-pairs score after each move.
5. Use `log(1 + score)` as an annealing energy and a geometric temperature schedule from `1.5` to `0.01`.
6. Stop only at exact score zero, and write per-pattern JSON-lines records if `--log` is supplied.

Those choices reproduce the documented search idea and exact stopping test, but the move size, temperature schedule, restarts, pattern prefilter, ordering, and seed are not claimed to match the lost code.

## Files in this provenance supplement

- `reconstructed_incidence_search.cpp` — runnable C++17 reconstruction, prominently marked as non-original.
- `pattern_inventory.txt` — captured deterministic inventory output.
- `reconstructed_replay_output.txt` — captured C++ replay of the two T=60 vectors.
- `replay_initial_candidates.py` — independent standard-library derivation of partitions, incidence possibilities, and exact scores.
- `replay_initial_candidates_output.txt` — captured Python replay, including all four 12-good incidence assignments.
- `original_run_metadata.json` — machine-readable unknown/recovered/reconstructed fields.

No new stochastic search was run while preparing this supplement. Only deterministic inventory, replay, compilation, and verification were performed.
