# Checkpoint log

## 1. Literature and starting construction

The starting point was Feige-Sapir-Tauber's four-agent construction. For four agents it uses thirteen goods, with two identical row agents and two identical column agents, each with MMS 68. Hummel's later existence theorem covers four agents with at most ten goods. Thus eleven and twelve were the unresolved sizes under the premise of the task.

The 13-good FST valuation types extracted from the paper were:

```text
R13 = 32 32  4 24 16 28 24 16 28 19 19 19 11
C13 = 32 32  3 24 16 27 24 16 27 20 20 20 11
```

## 2. Direct coarsening of FST

All exact MMS partitions at value 68 were enumerated.

- row type: 14 exact-68 subsets and 4 exact MMS partitions;
- column type: 16 exact-68 subsets and 12 exact MMS partitions.

No pair of goods is together in some MMS partition of both types. There was also no compatible triple and no compatible pair of disjoint pair-merges that preserved the original witness value 68 for both types.

A broader exact search then tested 3,458 descendants of the FST instance:

- 12 goods: all 78 one-pair merges and all 13 one-good deletions;
- 11 goods: every triple merge, every two-disjoint-pair merge, every two-good deletion, and every delete-one-plus-merge-two operation.

For each descendant, MMS was recomputed exactly and allocation feasibility was checked exactly. None was a counterexample.

## 3. Normal form and search constraints

For a fixed agent and a chosen MMS partition, excess value can be reduced inside each witness bundle until every witness bundle has value exactly `T`. Reducing values cannot create a previously absent threshold-`T` allocation. Hence it is natural to search in the normal form:

- four witness bundles, each summing to `T`;
- total value exactly `4T`, which forces MMS to equal `T`.

The search used two identical row agents and two identical column agents. Goods were edges of a sparse 4-by-4 row/column incidence matrix. The row valuation summed to `T` on each row; the column valuation summed to `T` on each column.

For this two-type profile, an MMS allocation exists exactly when one can choose two disjoint row-good bundles and two disjoint column-good bundles, all four mutually disjoint. Inclusion-minimal threshold bundles were enumerated by bit mask, and this condition supplied an exact zero/nonzero search score.

## 4. First positive result: twelve goods

A stochastic integer search over all simple 12-edge incidence patterns found a positive-integer instance with `T=60`:

```text
R12 = 44 16  8 42 10 34  1 24  1 14 14 32
C12 = 46 19 11 40  6 37  1 20  1 12 13 34
```

Two independent exhaustive checks gave MMS `(60,60,60,60)`, zero MMS allocations, and optimum common value 59.

## 5. Eleven goods

The same search over simple 11-edge patterns found:

```text
R11(initial) = 15 22 23 16 13 31 39 21  1 55  4
C11(initial) =  9 21 25 19  4 33 50 20  1 56  2
T = 60
```

Exact verification gave zero MMS allocations and optimum common value 59.

The integers were then simplified. For every complete allocation, one currently losing agent was selected. Keeping those loser choices fixed turns nonexistence into integer linear inequalities of the form

```text
value_of_selected_bundle <= T - 1,
```

along with the eight row/column witness equalities. Iterating this policy and re-verifying after every reduction produced the final profile:

```text
R =  7 12 11  8  6 16 21  9  1 28  1
C =  6 10 13 10  4 15 23 10  1 26  2
T = 30
```

## 6. Final exact verification

Two independent programs were run on the final profile.

C++:

- `145,750` unordered four-partitions per agent;
- `4,194,304` complete allocations;
- MMS vector `(30,30,30,30)`;
- MMS allocations: `0`;
- best possible minimum utility: `29`.

Python, using a separate restricted-growth-string generator and `itertools.product`, returned the same counts and conclusions.

## What was and was not established

Established exactly:

- the displayed 11-good positive-integer additive instance has no MMS allocation;
- each MMS is exactly 30;
- every complete allocation gives some agent value at most 29;
- therefore a four-agent counterexample exists already at eleven goods.

Not established in this run:

- a human case-by-case proof replacing exhaustive allocation enumeration;
- a proof-assistant certificate;
- publication priority or the absence of an unpublished simultaneous discovery;
- optimality of the displayed integer magnitudes or uniqueness of the incidence pattern.


## 7. Independent structural check

Because there are two identical row-type agents and two identical column-type agents, feasibility can also be checked without enumerating owner labels for all allocations. Every value-at-least-30 bundle contains an inclusion-minimal value-at-least-30 subbundle. Exact subset enumeration found:

- 54 minimal row-type threshold bundles;
- 54 minimal column-type threshold bundles;
- 448 disjoint pairs of row-type minimal bundles;
- 436 disjoint pairs of column-type minimal bundles;
- zero choices consisting of one row pair and one column pair whose four bundles are mutually disjoint.

This is implemented independently in `verify_two_type_structure.py`.
