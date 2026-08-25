# Four agents, eleven goods, and no MMS allocation

## Instance

There are four agents and eleven indivisible goods `g1,...,g11`. Valuations are additive. Agents 1 and 2 have the first valuation type; agents 3 and 4 have the second.

```text
agent 1:  7  12  11   8   6  16  21   9   1  28   1
agent 2:  7  12  11   8   6  16  21   9   1  28   1
agent 3:  6  10  13  10   4  15  23  10   1  26   2
agent 4:  6  10  13  10   4  15  23  10   1  26   2
```

All values are positive integers.

## Exact maximin shares

Each valuation row has total value 120, so its 1-out-of-4 MMS is at most 30.

For agents 1 and 2, the following partition has value 30 in every bundle:

```text
{g1,g2,g3} | {g4,g5,g6} | {g7,g8} | {g9,g10,g11}
```

For agents 3 and 4, the following partition has value 30 in every bundle:

```text
{g1,g7,g9} | {g2,g4,g8} | {g3,g6,g11} | {g5,g10}
```

Therefore the exact MMS vector is `(30,30,30,30)`.

## Nonexistence of an MMS allocation

The two included verifiers independently enumerate every complete allocation of the eleven goods. There are

```text
4^11 = 4,194,304
```

such allocations. Both programs find zero allocations in which all agents receive value at least 30. They also find that

```text
max_A min_i v_i(A_i) = 29.
```

Thus this is an exact counterexample, not merely a failed heuristic search.

## Running the verification

C++ (fast):

```bash
g++ -O3 -std=c++17 verify_mms_instance.cpp -o verify_mms_instance
./verify_mms_instance
```

Python (independent standard-library implementation):

```bash
python verify_mms_instance.py
```

Both implementations do the two requested exhaustive checks:

1. every unordered partition of eleven goods into four nonempty bundles (`145,750` partitions per agent) to compute MMS;
2. every complete allocation (`4,194,304` allocations) to test MMS feasibility.

A third verifier, `verify_two_type_structure.py`, independently exploits the two-agent-type form. It enumerates all inclusion-minimal value-30 bundles (54 for each type), all disjoint pairs of such bundles (448 row-type pairs and 436 column-type pairs), and confirms that no row pair and column pair are mutually disjoint.

Because all values are positive and the certified MMS is positive, allowing empty bundles in the definition of a partition cannot improve the MMS; the optimum partitions are nonempty.

## Files

- `verify_mms_instance.cpp` - exact C++ verifier.
- `verify_mms_instance.py` - independent exact Python verifier.
- `verify_two_type_structure.py` - independent exact structural verifier.
- `verification_output_cpp.txt`, `verification_output_python.txt`, and `verification_output_structure.txt` - captured outputs.
- `checkpoints.md` - search provenance, intermediate failures, and the constraints used.
- `search_provenance/` - retained integer-simplification scripts, intermediate verifiers, and solver logs.
- `SHA256SUMS` - hashes of the archived text files.

## Scope of the claim

The computation establishes the mathematical claim for the displayed instance. Together with the known existence result for four agents and at most ten goods, it makes eleven the minimum number of goods for a four-agent additive counterexample.

No claim about publication priority is made here. A final literature and author check is still appropriate before presenting the instance as a new result.
