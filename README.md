# Small MMS counterexamples: 5 agents / 13 goods and 4 agents / 11 goods

**Main claim.** There are instances of fair division with additive positive integer valuations in which no allocation gives every agent her maximin share (MMS), and in which the best achievable value of min_i v_i(A_i)/MMS_i is small:

- **5 agents, 13 goods: ratio exactly 28/29** (`instances/5x13_T29.json`), giving the upper bound **α ≤ 28/29 ≈ 0.9655** on the largest α for which α-MMS allocations always exist (any number of agents, any valuations), and α₅ ≤ 28/29 for five agents (previous: 1 − 1/5⁴ = 624/625 from the general construction of Feige, Sapir and Tauber).
- **4 agents, 11 goods: ratio exactly 29/30** (`instances/4x11_T30.json`), giving α₄ ≤ 29/30 (previous: 67/68, FST Theorem 4). Since Hummel (IJCAI 2023, arXiv:2302.00264) proves MMS allocations exist for 4 agents whenever m ≤ 10, eleven goods is the minimum for a four-agent counterexample.

Before these instances the best upper bound over all n was **39/40**, from the three-agent, nine-good instance of Feige, Sapir and Tauber (WINE 2021, arXiv:2104.04977), unimproved since 2021. The known series is now:

| n | goods | T = MMS | max-min | ratio |
|---|---|---|---|---|
| 3 | 9  | 40 | 39 | 39/40 (FST 2021) |
| 4 | 11 | 30 | 29 | 29/30 (this repository) |
| 5 | 13 | 29 | 28 | **28/29 (this repository)** |

Best known bounds over all n: 10/13 ≤ α ≤ 28/29 (lower bound: Heidari–Kaviani–Seddighin–Shahrezaei, SODA 2026; 7/9 claimed in the preprint arXiv:2511.13056).

**Status: COMPUTED.** Each upper bound follows directly from its instance and an exhaustive check of all allocations; no further argument is needed. Established by exhaustive enumeration, reproduced by independent programs of different design (literal enumeration and subset dynamic programming), plus per-instance compact certificates checkable by hand. No human-written proof, no proof-assistant formalization, no claim of publication priority beyond the literature search described in `PROVENANCE.md`.

## The 5 × 13 instance (`instances/5x13_T29.json`)

Agents 1–2 share valuation R; agents 3–5 share valuation C (two types, 2 + 3). Goods are cells of a sparse 5 × 5 grid.

```
good:  g1  g2  g3  g4  g5  g6  g7  g8  g9  g10 g11 g12 g13
R:      8  16   5  10   1  18   5  24   9   2  18  25   4     (agents 1, 2)
C:      9  12   7  10   1  15   7  26  10   1  17  27   3     (agents 3, 4, 5)
```

Witness partitions worth exactly 29 per bundle — the grid rows for R, the grid columns for C:

```
R (rows):     {g1,g2,g3} | {g4,g5,g6} | {g7,g8}  | {g9,g10,g11} | {g12,g13}
C (columns):  {g1,g4,g9} | {g5,g10,g12} | {g2,g11} | {g3,g6,g7}  | {g8,g13}
```

Each valuation sums to 145 = 5·29, so no partition into five bundles can have minimum above the average 29; the witnesses reach 29; hence MMS = (29, 29, 29, 29, 29) with no computation. Exhaustive enumeration of all 5¹³ = 1,220,703,125 allocations finds none giving every agent ≥ 29; the best achievable minimum is 28, e.g. agent 1 ← {g12,g13} (29), agent 2 ← {g4,g11} (28), agent 3 ← {g5,g8,g10} (28), agent 4 ← {g6,g7,g9} (32), agent 5 ← {g1,g2,g3} (28). Thus the ratio is exactly 28/29.

## The 4 × 11 instance (`instances/4x11_T30.json`)

Agents 1 and 2 share valuation R; agents 3 and 4 share valuation C (two types, 2 + 2).

```
good:  g1  g2  g3  g4  g5  g6  g7  g8  g9  g10 g11
R:      7  12  11   8   6  16  21   9   1   28   1     (agents 1, 2)
C:      6  10  13  10   4  15  23  10   1   26   2     (agents 3, 4)
```

Witness partitions worth exactly 30 per bundle:

```
R:  {g1,g2,g3} | {g4,g5,g6} | {g7,g8}     | {g9,g10,g11}
C:  {g1,g7,g9} | {g2,g4,g8} | {g3,g6,g11} | {g5,g10}
```

Rows sum to 120 = 4·30, so MMS = (30, 30, 30, 30) by the same average argument. All 4¹¹ = 4,194,304 allocations: none gives every agent ≥ 30; best minimum 29 — ratio exactly 29/30.

## Other instances in `instances/`

| file | n | goods | T = MMS | max-min | origin |
|---|---|---|---|---|---|
| `5x13_T29` | 5 | 13 | 29 | 28 | main result |
| `4x11_T30` | 4 | 11 | 30 | 29 | main result |
| `4x12_T60` | 4 | 12 | 60 | 59 | same search, all-positive 12-good instance (m = 12 closed without a zero-valued good) |
| `4x12_T68_a`, `4x12_T68_b` | 4 | 12 | 68 | 67 | intermediate: FST's 13-good instance with one good deleted, valuations re-solved by MILP |

All instances share the "two types of agents" skeleton. With 3 agents a two-type profile is 2 + 1, and "all but one agent identical" always admits an MMS allocation (Feige–Norkin, arXiv:2205.05363), so this skeleton is specific to n ≥ 4.

## Verification (`verify/`, outputs in `results/`)

Four independent programs, two of them of different algorithmic design:

1. `verify_exhaustive.py` — standard-library Python. MMS by enumerating all unordered partitions into n nonempty bundles, then all nᵐ allocations. ~1 minute for 4 × 11 (use the C++ version for 5 × 13).
2. `verify_exhaustive.cpp` — the same, literal, in C++. Seconds for m = 12; about a minute for all 5¹³ allocations. Input is the `.txt` form of each instance.
3. `verify_dp.cpp` — exact verification **without enumerating allocations**: subset dynamic programming F_i(S) = max_{B⊆S} min(v_i(B), F_{i+1}(S∖B)) computes the exact max-min over all allocations in O(n·3ᵐ); the same recursion with one valuation computes exact MMS. Agrees with the literal enumeration on every instance here.
4. `verify_envelope.py` (4 × 11) and `verify_packing.py` (any two-type instance) — compact certificates. For 4 × 11: with W = max(R, C), only **114** of the 145,750 unordered partitions have all four W-sums ≥ 30, and none of them splits into two R-bundles and two C-bundles worth ≥ 30 (`results/4x11_T30_envelope_survivors.txt`). For 5 × 13: an allocation giving everyone ≥ q exists iff two disjoint sets with R-value ≥ q and three disjoint sets with C-value ≥ q, all five mutually disjoint, exist (leftover goods only help, valuations being positive); at q = 29 there are **99** inclusion-minimal R-sets and **90** minimal C-sets, 1746 disjoint R-pairs and 6145 disjoint C-triples, and **zero** compatible 2+3 packings, while at q = 28 packings exist (`results/5x13_T29_packing.txt`). Together with the witness partitions these are proofs a reader can check without trusting any enumeration.

To reproduce everything:

```
g++ -O2 -o ve verify/verify_exhaustive.cpp && ./ve < instances/5x13_T29.txt
g++ -O2 -o vdp verify/verify_dp.cpp && ./vdp < instances/5x13_T29.txt
python3 verify/verify_packing.py instances/5x13_T29.json
python3 verify/verify_exhaustive.py instances/4x11_T30.json
python3 verify/verify_envelope.py instances/4x11_T30.json --list
```

`pro_original/` (4 × 11) and `pro_original_5x13/` contain the unmodified packages from the original search sessions; their outputs agree with `results/`.

## What the reader must take on faith

Nothing beyond running the scripts, or reading the certificates (114 rows for 4 × 11; 99 + 90 minimal sets for 5 × 13). External inputs: Hummel's theorem for the minimality claims and FST for the compared bounds; neither affects the counterexamples themselves.

## What is NOT established here

- Optimality of the ratios: whether 11-good 4-agent instances can force below 29/30, or 13-good 5-agent instances below 28/29, is open. T = 29 is not known to be minimal even on the found 5 × 13 pattern.
- Whether a 5-agent counterexample with 12 goods exists (Hummel gives existence for m ≤ 11; so the 12-good case is the one remaining open window for n = 5).
- Any n = 6 instance; whether the series 39/40, 29/30, 28/29 continues to decrease.
- A human-readable structural proof of nonexistence (as FST give for 3 × 9); the certificates are finite checks, not arguments.

## How it was found

Search by GPT-5.6 Pro (OpenAI): 4 × 11 on 25–26 August 2026, 5 × 13 on 1 September 2026 (two-type grid skeleton, stochastic search with exact scoring, then CEGIS-style integer tightening). Directed by the author; independent re-verification with separately written programs by Claude (Anthropic). Chronology, methods, and what was lost or preserved from the original sessions in `PROVENANCE.md`.

## Citation

Andrey Alexandrov, *Small MMS counterexamples: 5 agents / 13 goods and 4 agents / 11 goods*, GitHub repository, September 2026. Contact: alexandrov.home@gmail.com
