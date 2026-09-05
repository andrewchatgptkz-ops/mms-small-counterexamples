# From the checked incidence classes to arbitrary two-type instances

This document supplies the reductions for the unrestricted claim. The portable checker has verified all 462 main patterns and all 72 auxiliary singleton patterns; see logs/final_verify.json. No unfinished search is used as a premise.

## Proved claim
Every instance with five agents, twelve indivisible goods, positive rational additive valuations, and at most two distinct valuation functions admits an MMS allocation. There is no bound on denominators or on a scaled integer threshold T. Three or more types are not covered, so this does not determine f(5).

The only imported mathematical premise is Hummel's n+6 existence theorem for n != 3, as supplied in `input_context/MMS_DOSSIER.md`, section 1. At n=5 it guarantees an MMS allocation for eleven goods. The rest of the reductions below are proved here; the finite incidence cases have exact, independently checked proof objects.

## 1. One common type, or a 1+4 split
Choose an MMS partition of the common type into five bundles and give the exceptional agent her favourite bundle. Its value to her is at least her total value divided by five, which is at least her own MMS.
Give the four other bundles to the four identical agents; each gets at least the common MMS. The same argument works for a 1+(n-1) split for any n.

## 2. Normalise the 2+3 split without assuming total = 5 MMS
Call the minority type R and the majority type C. Choose an optimal five-bundle MMS partition for each. Let mu_t > 0 be the MMS of type t. Divide all its values by mu_t, so each bundle of its chosen partition has value at least 1.
For each chosen bundle B, divide the values of the goods in B by that bundle's current total. All resulting values remain positive and rational and are no larger than their previous normalised values. All five own-witness bundles now have value exactly 1, and the total value is exactly 5. Thus MMS is exactly 1 for each modified type, by the witness lower bound and the average upper bound.
An allocation meeting 1 for the modified values meets mu_t in the original instance. It is therefore enough to exclude counterexamples with unit witness sums. Label the R bundles as rows and the C bundles as columns. Every good is an edge of their 5-by-5 bipartite incidence multigraph. No connectedness or intersection-size assumption has been made.

## 3. Multiple goods in one intersection merge to eleven goods
If two goods g,h lie in the same row and the same column, replace them by a single good e, valued at R(g)+R(h) and C(g)+C(h). Both own-witness partitions survive the merger with unit sums, and both total values remain 5. Consequently both MMS values in the eleven-good instance are exactly 1.
Hummel's n+6 theorem gives an MMS allocation for these five agents and eleven goods. Replace e in its owner's bundle by g and h to lift the allocation to the original instance without changing any utility.
Therefore any counterexample in normal form would have a SIMPLE incidence grid. This reduction applies equally to connected and disconnected grids, and also to grids with singleton witness bundles. The requested 423 multiple-edge patterns with minimum degree two nevertheless receive explicit allocation-branching/whole-witness proofs in the main bundle, rather than being counted as solver-closed merely on the basis of this reduction.

## 4. A singleton R witness reduces to the all-but-one-identical case
Suppose a row is {g}, so R(g)=1. Give g to one of the two R agents. For either remaining type, take its five-bundle witness partition, delete the bundle containing g, and retain the other four bundles. They are disjoint, avoid g, and each is worth 1 to that type. Distribute any leftover goods arbitrarily among them. Hence the MMS of each type for four agents on the remaining goods is at least 1.
The remaining split is one R agent and three identical C agents. The argument of section 1, with n=4 and the reduced MMS values, gives each remaining agent at least 1. Thus no counterexample has a singleton R row.

## 5. Two or more singleton C witnesses give an explicit allocation
Choose two singleton C columns {g},{h}, each worth 1 to C. At least three R rows avoid both goods, because g,h belong to at most two of the five R rows. The total C value of all such untouched R rows is at most 5-C(g)-C(h)=3.
Among k >= 3 untouched R rows, the two with the smallest C values have combined C value at most 2*3/k <= 2. Give these two whole rows to the two R agents. Give g and h separately to two C agents, and all remaining goods to the third C agent. The last agent's value is at least 5-2-1-1=1. The bundles are disjoint and all five agents meet 1.

## 6. Exact finite cases remaining
After sections 3-5, a counterexample would have a simple grid, all five R rows of degree at least two, and either:
* all five C columns of degree at least two; or
* exactly one C column of degree one and the other four of degree at least two.
The first case lies in the 462-pattern main class. Its simple portion has 37 connected and two disconnected oriented patterns; all are checked in the main bundle. The second case consists of exactly 72 oriented simple patterns, independently enumerated by the portable checker; these are the auxiliary SB00-SB71 cases.
Each non-direct proof covers all 50 hard-row/hard-column root cases, with exact rational dual leaves, explicit allocation branches, downward closure and checked good permutations. There is no restriction to depth-one or depth-two weighting certificates, no fixed T, and no floating-point infeasibility accepted as a proof. All those checks pass, so both remaining cases are impossible. This establishes the stated unrestricted two-type claim, using the imported eleven-good theorem only in the merger reduction.
