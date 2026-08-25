# Search provenance

These are retained exploratory files from the integer-simplification stage.

- `simplify_candidate11.py` takes the initial `T=60` 11-good candidate, selects a losing agent for every one of the `4^11` allocations, and solves the resulting integer linear system to reduce the coefficients.
- `policy_simplify.py` repeats that loser-selection / integer-optimization step, producing the final `T=30` profile after intermediate `T=42` and `T=33` profiles.
- `verify15guess.cpp`, `verify42.cpp`, and `verify30.cpp` are small exact checkers for intermediate scaling/simplification experiments.
- The two output files record the solver results.

The original stochastic incidence-pattern search was exploratory notebook code and was not retained as a clean standalone driver. Its tested families and results are recorded in `../checkpoints.md`. The final mathematical claim does not depend on reproducing that search: the independent exhaustive verifiers in the parent directory certify the displayed instance from scratch.
