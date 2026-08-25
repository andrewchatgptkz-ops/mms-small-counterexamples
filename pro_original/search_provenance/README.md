# Search provenance

This directory now separates **retained original files** from a **marked reconstruction** of the missing sparse-incidence search.

## Historical limitation

The original exploratory source cell/script for the stochastic 4×4 incidence search and its run log were not retained. They could not be recovered from the first archive, surviving work files, temporary/history locations, or the retained conversation transcript. In particular, the following historical facts are unknown:

- random-number generator and seed, if any;
- labelled-pattern order and whether isomorphic patterns were collapsed;
- degree/connectivity prefilters;
- exact stochastic move/acceptance schedule;
- number of patterns visited before the first 11-good hit;
- elapsed time to that hit.

The surviving `35m 18s` duration covers the entire original task, not this search stage, and therefore is not used as a search timing.

See `SEARCH_PROVENANCE_RECONSTRUCTION.md` and `original_run_metadata.json` for the complete recovered/derived/reconstructed split.

## Reconstructed incidence-search files

- `reconstructed_incidence_search.cpp` — C++17 reconstruction, prominently labeled **RECONSTRUCTION, NOT THE ORIGINAL SEARCH SOURCE**. It contains:
  - exact enumeration of simple 11- and 12-edge subgraphs of a labelled 4×4 incidence matrix;
  - optional canonicalization under independent row and column permutations;
  - positive integer initialization respecting the four row/column witness sums;
  - the exact minimal-threshold-bundle pair-of-pairs score;
  - a plausible local-transfer/simulated-annealing driver with mandatory explicit seed;
  - JSON-lines logging for reconstructed runs.
- `pattern_inventory.txt` — deterministic counts of labelled patterns and row/column-isomorphism orbits.
- `reconstructed_replay_output.txt` — deterministic C++ replay of the retained `T=60` vectors.
- `replay_initial_candidates.py` — independent standard-library replay deriving exact `T`-partitions, incidence assignments, and scores.
- `replay_initial_candidates_output.txt` — captured Python replay. It shows that the 11-good incidence is uniquely recoverable up to row/column labels, whereas the 12-good incidence is not.
- `original_run_metadata.json` — machine-readable record of which historical fields are unknown and which facts are recovered.

No new stochastic search was run to prepare this supplement. Only deterministic compilation, inventory, replay, and verification were performed.

## Retained original simplification files

- `simplify_candidate11.py` — takes the initial `T=60` 11-good candidate, selects a losing agent for every one of the `4^11` allocations, and solves the resulting integer linear system to reduce the coefficients.
- `policy_simplify.py` — repeats that loser-selection/integer-optimization step, producing the final `T=30` profile after intermediate `T=42` and `T=33` profiles.
- `verify15guess.cpp`, `verify42.cpp`, and `verify30.cpp` — exact checkers for intermediate scaling/simplification experiments.
- `simplify_candidate11_output.txt` and `policy_simplify_output.txt` — captured solver output.

The final mathematical claim does not depend on reproducing the lost stochastic search: the independent exhaustive verifiers in the parent directory certify the displayed instance from scratch.
