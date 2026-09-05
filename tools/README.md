# tools/ — Claude's acceptance and exploration code (Cowork sessions 2026-08-26 … 09-05)

Not needed to verify anything in the repository (use `verify/`); kept so the negative results and explorations are reproducible.
- `dp.cpp` — subset DP (`./dp max < input`, input: n m q then n rows); `dp_alloc.cpp` — same, outputs an allocation; `packing_masks.cpp` — packing counts with distinct union-mask pairs (input: m a b q, R row, C row).
- `inst.py`, `analyze.py` — instances, patterns, minimal sets, fractional packing LP; `tree.py`, `nice.py`, `cert.py` — search/synthesis of one-branch weight certificates (MILP, HiGHS); `verify_depth2.py` — brute-force check of the 8×19 depth-2 certificate; `lift.py`, `subdiv_scan.py`, `dec_scan.py` — subdivision/decrement scans behind FAMILY.md; `cegis8.py` — packing-oracle CEGIS for n = 8.
- `perturb7.py` — first-order perturbation MILP around 7×17 with depth-≤2 certificates (infeasible for all branching goods/pairs); `probe7.py`, `climb7.py` — random/hill-climb probes of K·v + h; `check_cover.py` — checks the 20-packing cover of all 27 648 decrements of 7×17 against the P16S1 archive.
Python needs numpy/scipy (HiGHS) for the MILP scripts; the checkers are standard library.
