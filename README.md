# Four-agent MMS counterexamples with 11 and 12 goods

**Claim.** There is an instance of fair division with 4 agents, 11 indivisible goods, additive positive integer valuations, in which no allocation gives every agent her maximin share (MMS). Since Hummel (IJCAI 2023, arXiv:2302.00264) proves that MMS allocations exist for n = 4 agents whenever m ≤ 10, eleven is the minimum number of goods for a four-agent counterexample. The instance also gives the upper bound α₄ ≤ 29/30 on the best guaranteed MMS approximation for four agents, improving the 67/68 obtained from the 13-good construction of Feige, Sapir and Tauber (WINE 2021, arXiv:2104.04977, Theorem 4).

**Status: COMPUTED.** Established by exhaustive enumeration, reproduced by three independent programs, plus a compact certificate that can be checked by hand. No human-written proof, no proof-assistant formalization, no claim of publication priority beyond the literature search described in `PROVENANCE.md`.

## The instance (`instances/4x11_T30.json`)

Agents 1 and 2 share valuation R; agents 3 and 4 share valuation C.

```
good:  g1  g2  g3  g4  g5  g6  g7  g8  g9  g10 g11
R:      7  12  11   8   6  16  21   9   1   28   1     (agents 1, 2)
C:      6  10  13  10   4  15  23  10   1   26   2     (agents 3, 4)
```

Each row sums to 120, so every MMS is at most 30. Witness partitions into four bundles worth exactly 30:

```
R:  {g1,g2,g3} | {g4,g5,g6} | {g7,g8}     | {g9,g10,g11}
C:  {g1,g7,g9} | {g2,g4,g8} | {g3,g6,g11} | {g5,g10}
```

Hence MMS = (30, 30, 30, 30). Exhaustive enumeration of all 4¹¹ = 4,194,304 allocations finds none giving every agent ≥ 30; the best achievable value of min_i v_i(A_i) is 29, e.g. agent 1 ← {g9,g10,g11} (30), agent 2 ← {g7,g8} (30), agent 3 ← {g4,g5,g6} (29), agent 4 ← {g1,g2,g3} (29).

## Other instances in `instances/`

| file | goods | T = MMS | max-min | origin |
|---|---|---|---|---|
| `4x11_T30` | 11 | 30 | 29 | main result |
| `4x12_T60` | 12 | 60 | 59 | same search, all-positive 12-good instance (m = 12 is also closed without a zero-valued good) |
| `4x12_T68_a`, `4x12_T68_b` | 12 | 68 | 67 | intermediate: FST's 13-good instance with one good deleted and valuations re-solved by MILP |

All four share the "two types of agents" structure (2 + 2). Note that with 3 agents a two-type profile is 2 + 1, and "all but one agent identical" always admits an MMS allocation (Feige–Norkin, arXiv:2205.05363), so this skeleton is specific to n ≥ 4.

## Verification (`verify/`, outputs in `results/`)

1. `verify_exhaustive.py` — standard-library Python. Computes each agent's MMS by enumerating all unordered partitions into 4 nonempty bundles (S(11,4) = 145,750 per agent), then enumerates all 4ᵐ complete allocations. ~1 minute for m = 11.
2. `verify_exhaustive.cpp` — the same in C++; seconds for m = 12. Input is the `.txt` form of each instance.
3. `verify_envelope.py` — compact certificate for the two-type structure. Let W(g) = max(R(g), C(g)). Any bundle worth ≥ T to its recipient is worth ≥ T under W, so only unlabeled partitions whose four W-sums are all ≥ T can host an MMS allocation. For `4x11_T30` exactly **114** of the 145,750 partitions survive; for each, one checks that no two bundles are worth ≥ 30 to R while the other two are worth ≥ 30 to C. The full survivor list with R- and C-values is in `results/4x11_T30_envelope_survivors.txt` (114 rows, four number pairs each). Together with the two witness partitions above, this is a proof a reader can check without trusting the enumeration.

To reproduce everything:

```
python3 verify/verify_exhaustive.py instances/4x11_T30.json
g++ -O2 -o ve verify/verify_exhaustive.cpp && ./ve < instances/4x11_T30.txt
python3 verify/verify_envelope.py instances/4x11_T30.json --list
```

`pro_original/` contains the verification package as produced in the original search session (its own two verifiers, a structural checker via inclusion-minimal bundles, checkpoint log, and the integer-simplification scripts). Its outputs agree with `results/`.

## What the reader must take on faith

Nothing beyond running the scripts, or reading the 114-row certificate. The only external inputs are (a) Hummel's theorem for the minimality claim and (b) FST's 67/68 for the comparison; neither affects the counterexample itself.

## What is NOT established here

- Optimality of T = 30: whether some 11-good four-agent instance forces an agent below 29/30 of her MMS is open.
- Uniqueness or a classification of 11-good counterexamples.
- Any improvement to the general upper bound: 29/30 ≈ 0.967 is weaker than the three-agent 39/40 = 0.975 from FST, so the best known bound over all n is unchanged.
- A human-readable structural proof of nonexistence (as FST give for 3 × 9); the certificate here is a finite check, not an argument.

## How it was found

Search by GPT-5.6 Pro (OpenAI) in a single session on 25–26 August 2026, directed and verified by the author with Claude Fable 5 (Anthropic) doing independent re-verification. Chronology and method in `PROVENANCE.md`.

## Citation

Andrey Alexandrov, *Four-agent MMS counterexamples with 11 and 12 goods*, GitHub repository, August 2026. Contact: alexandrov.home@gmail.com
