# Small two-type counterexamples for maximin-share (MMS) fair division

**Status: COMPUTED (computer-found, independently re-verified), not peer-reviewed. Priority not established.**

This repository contains explicit instances of fair division of indivisible goods with additive valuations in which no allocation gives every agent her maximin share (MMS), together with exact verifiers and human-auditable certificates.

## Main claim

The general MMS approximation constant α (the largest ratio such that every instance admits an allocation giving each agent at least α times her MMS) satisfies

**α ≤ 26/27 ≈ 0.96296** (7 agents, 17 goods, T = 27, best achievable minimum 26).

Before this work the best known upper bound was 39/40 (Feige, Sapir, Tauber, WINE 2021, 3 agents and 9 goods). Known lower bounds: 10/13 (Heidari, Kaviani, Seddighin, Shahrezaei, SODA 2026) and 7/9 (Huang and Zhou, preprint arXiv:2511.13056). See `PROVENANCE.md` for dates; the literature moves fast, check before citing.

## The series

| n | m | T | best min | ratio | n-specific bound before | goods bound f(n) |
|---|---|---|---|---|---|---|
| 3 | 9 | 40 | 39 | 39/40 | (FST 2021) | — |
| 4 | 11 | 30 | 29 | 29/30 | 67/68 (FST) | f(4) = 10 exactly (with Hummel's n+6 theorem) |
| 5 | 13 | 29 | 28 | 28/29 | 1 − 1/5⁴ (FST) | f(5) ≤ 12 |
| 6 | 15 | 28 | 27 | 27/28 | 1 − 1/6⁴ | f(6) ≤ 14 |
| 7 | 17 | 27 | 26 | 26/27 | 1 − 1/7⁴ | f(7) ≤ 16 |

All four new instances follow the two-type row/column paradigm of Feige–Sapir–Tauber's general construction (two agent types with valuations R and C, goods as cells of a sparse n×n grid, every row summing to T under R and every column to T under C, so MMS = T for everyone by construction), but on a much sparser skeleton with far fewer goods. The incidence graphs (rows and columns as vertices, goods as edges) are subdivisions of the triangular prism; each instance for n = 5, 6, 7 is obtained from the previous one by subdividing one edge and adjusting values (m = 2n + 3, T = 34 − n for n = 4…7). Details in `FAMILY.md`. The recursion is a set of four data points, not a proven construction for all n; at n = 8 the naive step fails and the existence of an 8-agent instance with ratio 25/26 is open.

## Contents

- `instances/*.json` — the instances (values, row/column pattern, best allocation) for 4×11, 5×13, 6×15, 7×17, and an all-positive 4×12 with T = 60.
- `verify/` — independent verifiers (standard library only):
  - `dp.cpp` — subset DP: exact MMS and exact max over allocations of the minimum utility (`./dp max < input`).
  - `packing.cpp`, `packing_pairs.cpp` — packing certificate for two-type instances: an allocation with all agents ≥ q exists iff there are a pairwise-disjoint R-sets ≥ q and b pairwise-disjoint C-sets ≥ q, all disjoint; the programs count inclusion-minimal sets, disjoint tuples and compatible pairs (tuple pairs / distinct union-mask pairs). Zero compatible pairs at q = T is the certificate.
  - `verify_certificate.py` — the human-auditable "one disjunction + two weightings" certificates (see `certificates/`), checked by brute force over all 2^m subsets.
  - `verify_subsetdp.cpp` — literal enumeration of all n^m allocations (for the small instances; 6^15 ≈ 4.7·10¹¹ was done in shards, see `PROVENANCE.md`).
  - `run_all.sh` — runs everything (about 10 seconds).
- `certificates/` — packing counts and weight certificates, with the verification recipe.
- `FAMILY.md` — the structure of the family, the chain certificate, the rigidity facts, and the status of n = 8.
- `PROVENANCE.md` — who found what and when, archive hashes, what was lost, what is not established.
- `pro_original*/` — the unmodified search archives of the GPT-5.6 Pro sessions (4×11 package; 5×13, 6×15, 7×17 `.tar.zst` with SHA-256).
- `kit/` — everything a model session needs to continue the work (dossier, environment lessons, fetch instructions, packing oracle).
- `results/`, `legacy/` — material from releases v1.0–v1.2, kept for reference: the run logs of the older verifiers, their instance files in the older JSON schema (including the two intermediate 4×12 instances with T = 68 that the family above does not contain), and the verifiers themselves.

## How the certificates work

For each instance fix one good g* (a good of the "soft" column, the only column with no heavy good). In any allocation g* goes to an R-agent or to a C-agent. **Case R**: integer weights w ≥ 0 such that every set with R-value ≥ T weighs ≥ α, every set with C-value ≥ T not containing g* weighs ≥ β, and a·α + b·β > Σw. Since the bundles of an allocation are disjoint, an allocation with all agents ≥ T would carry weight ≥ a·α + b·β > Σw — contradiction. **Case C** is symmetric. Each condition is a knapsack statement ("maximum R-value at weight ≤ α − 1 is T − 1") that can be checked by hand with a small table. A single weighting without the disjunction is impossible: the fractional packing (half of every row plus half of every column) has value exactly 1.

For n = 5, 6, 7 one weight vector serves all three instances (first m entries): case R with w = 5 11 6 7 3 12 6 17 7 3 12 17 6 11 11 17 6, α = 22, β = 23; the margin is exactly 1 each time. This "chain certificate" does not extend to n = 8 (proved), see `FAMILY.md`.

## What is not established

T-minimality and m-minimality of each instance; whether an 8-agent instance with ratio below 26/27 exists; a construction for all n; priority (no systematic prior-art search beyond the sources listed in `PROVENANCE.md`).

## Method and provenance, honestly

The instances were found by GPT-5.6 Pro (OpenAI) in searches designed and audited by the author with Claude (Anthropic); every claim was re-verified with separately written code before being trusted (subset DP, packing certificates, literal enumeration where feasible, weight certificates by brute force). The search code for 4×11 was lost in a container reset and is present only as a marked reconstruction; for 5×13, 6×15 and 7×17 the producing scripts, seeds, logs and shell invocations are archived (hashes in `PROVENANCE.md`). The certificates in this repository do not depend on any search code.

Author: Andrey Alexandrov (journalist, not a mathematician). Corrections and prior-art pointers are welcome.
