# Portable allocation-branching certificates

Run `python3 verify.py` from this directory or by absolute path. Only the Python standard library is used. No optimizer, numerical library, network or producer oracle is part of the checking path.

The checker independently enumerates all 462 oriented 5x5 integer incidence matrices with 12 edges and every row/column degree >=2. It verifies that the bundle contains exactly that class, expands every cell multiplicity into distinct goods, and checks every proof. The 37 Stage 2 simple connected patterns and proofs are retained with their original P00-P36 labels.

An auxiliary enumeration covers the 72 simple grids with all R-row degrees >=2, exactly one singleton C column, and no other singleton columns. These cases repair a scope gap between minimum-degree-two incidence enumeration and arbitrary two-type instances. See ../THEOREM.md for all reductions, including singleton minority rows, multiple singleton majority columns, and the merger-to-eleven-goods argument using the supplied Hummel theorem.

The checker maximally claims only the proof coverage actually present. During the search, `--allow-incomplete` validates existing proofs and explicitly lists unexcluded patterns; the default refuses incomplete coverage. Final expected outputs are `ALL 462 EXACT EXCLUSIONS VERIFIED` and `ALL 72 AUXILIARY SINGLETON CASES VERIFIED`.

Proof rules are the retained Stage 2 rules. A positive counterexample at any node would allow a common delta>0 bounded by every individual value and every strict losing gap. Dual leaves give exact rational identities cancelling all value variables and implying k*delta <= c, with k>0 and c<=0. Allocation branches give two R bundles and three C bundles, mutually disjoint; at least one non-witness-containing bundle must lose. All losing alternatives are checked. The verifier checks downward inclusion and every symmetry as a permutation preserving both labelled witness partitions. Every non-direct pattern has all 50 structural root cases.
