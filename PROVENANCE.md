# Provenance

## Who, when, how
- 4×11 (T = 30, 29/30) and the 4×12 instances: found by GPT-5.6 Pro on 2026-08-25/26 (single session, 35 min) from a free-form prompt; two-type skeleton after FST, pattern enumeration + annealing + "fix the loser" tightening on scipy/HiGHS. The original search code was lost in a container reset; the archive contains a reconstruction explicitly marked `RECONSTRUCTION, NOT THE ORIGINAL SEARCH SOURCE`. The result does not depend on it.
- 5×13 (T = 29, 28/29): GPT-5.6 Pro, 2026-09-01. Stochastic search (master seed 202609020013, pattern 0x123e16d) + CEGIS on HiGHS (seed 202609051329, 83 cuts). Archive `mms5_5x13_T29_ratio28of29_20260901T132943Z.tar.zst`, sha256 129aaab7323a3f17cf01042154b6323d38be24f96b63e4d2c2853a5af5407afc.
- 6×15 (T = 28, 27/28): GPT-5.6 Pro, 2026-09-01, deterministic construction from 5×13 (no seeds). Archive `mms6_6x15_T28_ratio27of28_20260901T163946Z.tar.zst`, sha256 de3c90501b577b8105dd4526e6e621199f00cd99f8c81995a695cfb86429cbed (1655 files, 45 shell-invocation records, 1296 shards of the literal 6^15 enumeration with per-shard SHA-256).
- 7×17 (T = 27, 26/27): GPT-5.6 Pro, 2026-09-01, subdivision of 6×15 + CEGIS repair (580 cuts, bitwise replay). Archive `mms7_7x17_T27_ratio26of27_20260901T190531Z.tar.zst`, sha256 03241e04a4176e36a33c4662d201e1bd5b7af024831ac7ad625dffc60d637e38 (1337 files, 68 invocation records, Git bundle; contains the 6×15 archive verbatim).
- Certificates, chain certificate, rigidity and hard-row facts, n = 8 negative results: Claude (Anthropic) in Cowork sessions 2026-09-01/02, with independent code; the n = 8 CEGIS stages were run by GPT-5.6 Pro on prompts designed by Claude.

The Pro archives are distributed separately (they are large); their hashes above pin them.

## Independent verification (all by separately written code)
- 4×11: literal 4^11 enumeration (Python and C++), envelope certificate (114 surviving 4-partitions, no 2+2 hand-out), reproduced on the author's machine.
- 5×13: literal 5^13 (7 s, C++), subset DP, packing certificate 99/90/1746/1520/0.
- 6×15: subset DP, packing certificate 145/147/38473/42520/8066/7967/0 (9796 at q = 27), literal 6^15 = 470 184 984 576 allocations in 36 shards (about 25 min on 2 cores; visited count exactly 6^15).
- 7×17: two subset DPs (C++ and Python/Numba by Pro; C++ by Claude), packing certificate 230/247/174099/1117997/34965/29833/0 (102508 at q = 26), weight certificate by brute force over 2^17 subsets. No literal 7^17 enumeration (2.3·10^14).
- All weight certificates and chain certificates: brute force over all 2^m subsets (`verify/verify_certificate.py`, seconds).
- 2026-09-02, on the author's own machine (Claude Code, Opus 5, separate code from the Cowork sessions): all five instances re-checked end to end — grid structure (rows and columns really partition the goods and sum to T, no good worth T or more), subset DP (MMS = T for both types, max-min = T − 1), the packing counts of `certificates/packing_counts.md` recomputed by a different algorithm (union masks of the disjoint tuples plus a subset-sum transform instead of pairing tuples), the weight certificates re-checked with the weights parsed from the table in `certificates/weight_certificates.md` rather than from the script, and the structural claims of `FAMILY.md` (prism subdivision after suppressing the degree-2 vertices; hard rows and columns at the b − 1 / a − 1 limit; the row and column weights of the chain vector). All numbers agree. The 6×15 case was additionally re-run by literal enumeration with a separately written sharded program (six shards by the owner of good 1, about 26 minutes on two cores): exactly 470 184 984 576 = 6^15 allocations visited, none with minimum ≥ 28, best minimum 27.

## Literature checked (2026-08-26, non-systematic)
arXiv full text (cs.GT, math.CO), Google Scholar "cited by" of arXiv:2104.04977 sorted by date, homepages of Feige, Sapir, Tauber, Hummel, Zenodo web index, GitHub repository search, Wikipedia "Maximin share". No prior instance below 39/40 was found. Not checked: Semantic Scholar, OpenAIRE, GitHub code search. A targeted check for the specific fractions 29/30, 28/29, 27/28, 26/27 has not been run.

## Sources
- U. Feige, A. Sapir, L. Tauber. A tight negative example for MMS fair allocations. WINE 2021, arXiv:2104.04977.
- H. Hummel. Maximin shares under cardinality constraints / on the existence of MMS allocations for n+6 goods. IJCAI 2023, arXiv:2302.00264.
- H.-L. Hsu. Ordinal maximin share / existence for n+5 goods, arXiv:2209.06330.
- U. Feige, A. Norkin. Improved maximin fair allocation of indivisible items to three agents, arXiv:2205.05363.
- Heidari, Kaviani, Seddighin, Shahrezaei, SODA 2026 (10/13 lower bound); Huang, Zhou, arXiv:2511.13056 (7/9, preprint).

## Not established
T-minimality and m-minimality; existence of an 8-agent instance below 26/27; a construction for all n; priority.
