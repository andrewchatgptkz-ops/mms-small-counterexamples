# Provenance

All dates 25–26 August 2026 (UTC). The search was run by GPT-5.6 Pro in one session; the author supplied the problem statement, read the FST paper beforehand, and accepted results only after independent re-verification (Claude Fable 5, separate code, separate container).

## Chronology

1. **Starting point: FST 13-good construction for n = 4** (two row-type and two column-type agents, MMS 68, best common value 67). Its exact-68 partitions were enumerated: 4 for the row type, 12 for the column type.
2. **Pure compression fails.** 3,458 descendants of the FST instance — every one-pair merge and one-good deletion (12 goods); every triple merge, two-disjoint-pair merge, two-good deletion, deletion-plus-merge (11 goods) — were tested exactly. None is a counterexample.
3. **Compression with re-solving succeeds at 12.** Deleting one good from FST-13, redistributing its weight inside its witness bundle, and re-solving the valuations by MILP (`scan_fst_deletions.py`, using a CEGIS loop: MILP proposes valuations, exact enumeration returns an MMS allocation as a new constraint) gives 12-good counterexamples at T = 68: `4x12_T68_a` and `4x12_T68_b`. Pair-merging these to 11 goods gives nothing.
4. **Fresh search at 11.** Normal form: each witness bundle worth exactly T, total exactly 4T (so MMS = T automatically; reducing values inside a witness bundle cannot create an allocation that was absent). Goods are cells of a sparse 4 × 4 incidence pattern; row agents value rows, column agents value columns. For this profile an MMS allocation exists iff two disjoint row bundles ≥ T and two disjoint column bundles ≥ T can be chosen mutually disjoint — an exact, fast score. The search over 12-cell patterns found `4x12_T60`; over 11-cell patterns, an 11-good instance at T = 60.
5. **Integer simplification.** For every allocation, fix one currently losing agent; nonexistence becomes a system of integer inequalities `value(assigned bundle) ≤ T − 1` plus the eight witness equalities. Iterating and re-verifying after each step took T from 60 through 42 and 33 to 30 (`pro_original/search_provenance/`).
6. **Verification** by two programs in the search session, then independently here (`verify/`), plus the max-envelope certificate (114 survivors, none feasible).

## What is still missing from this record

- The CEGIS core (`cegis_two_types.py`: `solve_milp`, `find_certificates_two_types`) and the incidence-pattern scan of step 4 were not exported from the search session. They are requested; the result does not depend on them — the certificate in `verify/` is self-contained.

## Prior-art check (26 August 2026)

Searched: arXiv (full text and cs.GT/math.CO listings), Zenodo (search page), GitHub (repository search; Hummel's account), Google Scholar (papers citing FST 2021, sorted by date, through August 2026), homepages of Feige, Sapir, Tauber and Hummel, ResearchGate, Wikipedia "Maximin share" (maintained, still lists 3n+1 = 13 for even n). Not queried directly: OpenAIRE, Semantic Scholar, GitHub code search.

Nothing found claiming a four-agent counterexample below 13 goods or an upper bound for n = 4 better than 67/68. Nearest neighbours: Schwerdtfeger (arXiv:2607.18139) — ordinal 1-out-of-5 for four agents, different scale; Feldman–Fiat–Nissan–Ponitka (arXiv:2606.18921) — "two types of additive agents" as a setting where MMS may fail (citing FST) but EPMMS exists; Alkassar–Fouz–Mehlhorn (arXiv:2608.08590) — EFX existence for four agents and ≤ 9 goods, same small-instance genre, different notion.
