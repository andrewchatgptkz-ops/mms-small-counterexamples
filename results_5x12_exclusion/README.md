# Exact certificate: the requested two-type 5-agent / 12-good grid class

## Claim
For every connected simple 5-by-5 incidence grid with exactly twelve goods and every row and column of degree at least two, any positive valuations R,C with every R-row summing to 1 and every C-column summing to 1 admit an allocation to two R agents and three C agents in which everyone obtains at least 1.

This covers all positive rational valuations, with no denominator or T bound. In fact the proof applies to positive real valuations as well. It does not assert the corresponding result for unrestricted three-type or five-type instances, the 1+4 multiplicity split, or arbitrary witness structures. The equivalent 3+2 split is covered by transposing the grid and exchanging type names.

## Check
Run `python3 verify.py` in this directory, or pass its full path. Only Python's standard library is needed. Expected status: `ALL 37 EXACT EXCLUSIONS VERIFIED`.

The verifier independently enumerates all eligible grids, checks that their oriented canonical list equals the 37 certificate patterns, verifies the grid-to-good labelling, and checks every proof. It uses no optimizer, no floating-point arithmetic for proof inequalities, and no packing oracle. `proofs.json.gz` is the complete compact proof bundle; search logs are not needed to establish the claim.

## Why these proofs imply the claim
The five R-rows form a partition, and the five C-columns form a partition. If three rows were each worth at least 1 to C, give those rows to the three C agents and the other two rows to R. Thus a counterexample has at most two such rows. Similarly, it has at most one column worth at least 1 to R. Every counterexample therefore belongs to at least one of 5 * binomial(5,2) = 50 cases: choose the one allowed hard R-column and the two allowed hard C-rows, and declare all the other cross-valued witness bundles strictly losing.

At a node, the assumptions are that certain typed subsets are losing, meaning their value is strictly below 1. Any particular positive counterexample satisfying these assumptions admits a positive common margin delta: choose delta at most every individual value and every assumed strict losing gap. The LP relaxation writes v_g >= delta, every witness sum = 1, and v(S) + delta <= 1 for each assumed losing subset. Delta is not bounded below in the computational relaxation; the proof only needs the impossibility of delta > 0.

A terminal dual node supplies nonnegative rational multipliers for inequalities and arbitrary rational multipliers for witness equalities. Their exact sum cancels all value variables, leaving k * delta <= c with k > 0 and c <= 0. This rules out the positive common margin.

A branching node supplies an explicit disjoint allocation of two R bundles and three C bundles. At least one of these must lose in a counterexample. A bundle containing a complete witness for its own type cannot lose; all other alternatives are explored. Leftover goods do not affect this argument because values are positive and can be assigned arbitrarily. Every resulting branch is checked.

Losing sets are downward closed: a subset of a losing set is losing. The checker verifies every use of that implication. Core-reuse nodes use only the inequalities whose multipliers in a previously checked dual proof are positive. Symmetry-reuse nodes include an explicit permutation of the twelve goods, checked to preserve each type's witness partition; the losing assumptions and proof references are transformed accordingly.

All 50 cases are checked in each of the 26 surviving patterns. The remaining 11 patterns have explicit value-independent allocations consisting of two whole R-rows and three whole C-columns, pairwise disjoint.

## Depth and completeness
These are finite, exhaustive disjunctive allocation proofs, not one-good or two-good weighting certificates. No depth-1/depth-2 certificate restriction is present. The separate weighting-certificate synthesis engine was not needed and was not run.
