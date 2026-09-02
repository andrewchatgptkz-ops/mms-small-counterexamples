# The prism family: structure, certificates, and where it stops

## 1. Two-type grid instances
a agents with valuation R, b agents with valuation C (n = a + b). Goods are cells of a sparse n×n grid; rows sum to T under R, columns to T under C; total value nT for both types, so MMS = T for every agent (rows/columns are witness partitions; a partition into n parts has minimum ≤ average). An allocation with all agents ≥ T exists iff there is a packing: a pairwise-disjoint R-sets of R-value ≥ T and b pairwise-disjoint C-sets of C-value ≥ T, all mutually disjoint. Equivalently: a 2-colouring of goods (X to R-agents, Y to C-agents) with X splittable into a R-sets ≥ T and Y into b C-sets ≥ T.

## 2. The incidence graphs
Rows and columns as vertices, goods as edges. n = 3 (FST): K3,3. n = 4, 5, 6, 7: subdivisions of the triangular prism (two triangles joined by a perfect matching); the matching edges are never subdivided, only triangle edges. Row/column patterns:

- 4×11: rows {1,2,3}|{4,5,6}|{7,8}|{9,10,11}; columns {1,7,9}|{2,4,8}|{3,6,11}|{5,10} (unique).
- 5×13: rows {1,2,3}|{4,5,6}|{7,8}|{9,10,11}|{12,13}; columns {1,4,9}|{5,10,12}|{2,11}|{3,6,7}|{8,13}.
- 6×15: rows … |{14,15}; columns {1,4,9}|{5,10,12}|{2,11}|{3,7,15}|{8,13}|{6,14}. Obtained from 5×13 by subdividing edge g6 = (r2,c4) through new r6, c6 with the unique working parameters (12,12) at T = 29, then decrementing one good per row (R) and one per column (C) → T = 28.
- 7×17: rows … |{16,17}; columns {1,4,9}|{5,10,12}|{2,11}|{3,15,17}|{8,13}|{6,14}|{7,16}. Obtained from 6×15 by subdividing g7 = (r3,c4) through new r7, c7; here the literal "subdivide + decrement" operator fails (all 10 935 T-preserving subdivisions and all 70 087 680 subdivision/decrement pairs keep a packing) and a small CEGIS repair of the values was needed (L1 distance 6 in R and 4 in C from the best literal candidate).

Sensitivity: among all 13 edges × 28×28 subdivision parameters × three splits of 5×13, exactly one subdivision preserves non-existence at T = 29; among 46 656 decrement patterns of that instance, 21 work.

## 3. Human-auditable certificates
See README and `certificates/weight_certificates.md`. Branching good: g1 (column c1 = {g1, g4, g9}, the only column with no heavy good; on the optimal face of the fractional packing LP the goods of c1 always take a fractional share in [1/4, 3/4]). The certificates for all four instances and the chain certificate are checked by `verify/verify_certificate.py` by brute force over all 2^m subsets.

## 4. Chain certificate and rigidity
One weight vector certifies case R for n = 5, 6, 7 with α = 22, β = 23. Structural facts behind it (all verified on the instances):

- Rows are R-sets of value exactly T and columns without g* are C-sets of value exactly T, so any case-R certificate must give every row weight ≥ α and every such column weight ≥ β. In the chain weights this holds with equality: rows weigh 22 or 23, columns without g1 weigh exactly 23, column c1 weighs 19. Hence Σw = nα + (row excesses) = (n−1)β + w(c1), and a·α + b·β > Σw forces: row excesses ≤ b − 1 and w(c1) ≤ a(α − β) + β − 1 (= α − a when β = α + 1). In 7×17 both hold with equality (excesses 1+1+1 = 3 = b − 1; w(c1) = 19 = 22 − 3). With α = β no certificate can exist at all, which is why the disjunction and the asymmetry are necessary.
- Subdividing an edge of weight w_e in a column of weight W_c requires W_c + q ≥ 2β where q is the new agent's quota: with a new R-agent (q = α = 22) only column c1 qualifies; with a new C-agent (q = β = 23) any edge, but the new weights are forced (x = β − w_e). This is why the step 6 → 7 (new C-agent) lifted the weights unchanged (g7 had w = 6, the new goods got 17 and 6).
- Hard rows/columns (necessary condition for any two-type instance): if b or more rows have C-sum ≥ T the C-agents take b whole rows and an allocation exists; so at most b − 1 rows may have C-sum ≥ T and at most a − 1 columns may have R-sum ≥ T. All four instances satisfy this with equality.

## 5. Status of n = 8 (as of 2026-09-02)
- The fixed prefix chain (same weights, α = 22, β = 23, one subdivision) does not extend to n = 8: proved for split 4+4 on all 17 edges (LP-infeasible for the c1 edges, witness sums for the others) and for split 3+5 on all non-c1 edges (exact CEGIS). 
- Best known 8×19 profile (subdivision of g11, T = 26): R = 7 14 5 9 1 16 4 22 9 1 16 23 3 11 15 21 5 11 15, C = 8 12 6 9 1 15 4 23 9 1 15 24 3 11 14 22 6 11 14, with exactly two surviving packings (four whole rows to C-agents; four whole columns to C-agents). One-sided repair is UNSAT; the L1 ≤ 6 ball is empty; with the hard-row/hard-column constraints the L1 ≤ 20 box on this graph is UNSAT (exact CEGIS). Full-space CEGIS does not converge.
- Whether an 8-agent two-type instance with ratio below 26/27 exists is open.
