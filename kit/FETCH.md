# How a model session gets everything it needs from this repository

This repository is the single source of truth for the project. Nothing needs to be attached by hand.

## Fetch (first action of every session)
    cd /mnt/data && git clone --depth 1 https://github.com/andrewchatgptkz-ops/mms-small-counterexamples.git repo
    cd repo && sha256sum -c pro_original_5x13/SHA256SUMS pro_original_6x15/SHA256SUMS pro_original_7x17/SHA256SUMS
    python3 verify/verify_certificate.py        # must end with: ALL CERTIFICATES VALID / CHAIN CERTIFICATES VALID
If `git` cannot reach GitHub from the sandbox, try `curl -L https://github.com/andrewchatgptkz-ops/mms-small-counterexamples/archive/refs/heads/main.zip -o /mnt/data/repo.zip`; if that fails too, say so in the first message and stop — the operator will attach a copy.

## What is where
- `kit/MMS_DOSSIER.md` — project state, results, structure, open questions, and §8 environment lessons (read §8 before computing anything).
- `kit/REVIEW_GPT6_2026-09-04.md` — the outside review (in Russian) and the resulting plan.
- `instances/`, `certificates/`, `verify/` — accepted instances, certificates, independent verifiers (`verify/run_all.sh`, ~10 s).
- `kit/dp_alloc.cpp` — subset DP that outputs an allocation with min ≥ q (packing oracle: zero the R-value of the branching good to model "g* with a C-agent").
- `pro_original_5x13/` — the 5×13 search machine (pattern enumeration for 5×5 grids, stochastic search with exact packing score, CEGIS on HiGHS), archive `.tar.zst`; unpack with `zstd -d` or Python `zstandard`.
- `pro_original_6x15/`, `pro_original_7x17/` — the 6×15 and 7×17 archives (the 7×17 one contains the packing-oracle CEGIS with indicator formulation, invocation-record tooling, and the 6×15 archive verbatim).
- `pro_original/` — the 4×11 package (search code reconstructed, verifiers original).
- `results_5x12_exclusion/` — proof bundle + two checkers for "no two-type 5×12 on simple connected grids".
- `pro_original_8x19_theory/` — the GPT-6 Pro theory session snapshot (gadget signatures, depth-2 certificate synthesis, the 8×19 T = 104 instance, invariants).

## Rules that apply to every computation (from §8 of the dossier)
Snapshot the working tree to /mnt/data after every stage; one prompt = one stage; the newest snapshot is always a complete deliverable (REPORT.md, REPRODUCE.md, MANIFEST.sha256, invocation records); size-based guards, not time; every producing script on disk verbatim with seeds, logs and the shell invocation recorded before the worker starts; independent verification (two subset DPs, packing certificate, sanity checks) before any instance is reported.
