# Two-branch weight certificates ("one disjunction + two weightings")

Fix the branching good g*. Case R (g* with an R-agent): every set S with R(S) ≥ T has w(S) ≥ α; every set S with C(S) ≥ T and g* ∉ S has w(S) ≥ β; a·α + b·β > Σw. Case C: symmetric (R-sets avoiding g*). Each condition is equivalent to a knapsack bound, e.g. "max R(S) over w(S) ≤ α − 1 equals T − 1". All rows below are verified by `verify/verify_certificate.py` (brute force over all 2^m subsets).

| Instance | g* | Case R: w; α, β; Σw < aα+bβ | Case C: w; α, β; Σw < aα+bβ |
|---|---|---|---|
| 4×11, T=30 (2+2) | g2 | 7 10 13 9 6 15 22 9 2 25 3; 30, 31; 121 < 122 | 4 6 7 6 4 10 13 7 2 16 2; 20, 19; 77 < 78 |
| 5×13, T=29 (2+3) | g1 | 2 6 3 4 1 6 3 9 3 2 6 9 3; 11, 12; 57 < 58 | 10 19 9 16 3 23 9 33 15 4 23 34 8; 42, 41; 206 < 207 |
| 6×15, T=28 (3+3) | g1 | 5 11 6 7 3 12 6 17 7 3 12 17 6 11 11; 22, 23; 134 < 135 | 8 17 8 14 3 20 8 29 14 3 20 30 7 17 20; 37, 36; 218 < 219 |
| 4×12, T=60 (2+2) | g3 | 16 7 3 15 4 12 1 8 1 5 6 11; 22, 23; 89 < 90 | 20 10 5 18 4 16 1 12 1 8 8 14; 30, 29; 117 < 118 |
| 7×17, T=27 (3+4) | g1 | 5 11 6 7 3 12 6 17 7 3 12 17 6 11 11 17 6; 22, 23; 157 < 158 | 17 30 14 24 6 36 14 52 24 6 36 53 13 30 36 51 15; 66, 65; 457 < 458 |

Chain certificates (one vector for n = 5, 6, 7, first m entries):
- case R: 5 11 6 7 3 12 6 17 7 3 12 17 6 11 11 17 6 with α = 22, β = 23 (sums 112 < 113, 134 < 135, 157 < 158);
- case C: 45 80 38 64 16 96 38 138 64 16 96 141 35 80 96 137 39 with α = 176 and β = 172, 172, 173.

Knapsack view (6×15, case R): max R-value at weight ≤ 21 is 27; max C-value avoiding g1 at weight ≤ 22 is 27. Case C: max R-value avoiding g1 at weight ≤ 36 is 27; max C-value at weight ≤ 35 is 27. Control: at threshold T − 1 no such certificate exists for any branching good (an allocation with minimum T − 1 exists).

## Depth-2 certificate: 8×19, T = 104 (4+4), branch on (g1, g2)

Leaf XY: g1 goes to a type-X agent, g2 to a type-Y agent; R-sets may not contain a good given to C, C-sets may not contain a good given to R. Verified by `verify/verify_certificate.py` (brute force over all 2^19 subsets, every minimum equals the quota exactly).

| Leaf | w | α, β | Σw < 4α+4β |
|---|---|---|---|
| RR | 6 11 6 7 3 13 6 18 7 3 13 18 6 11 12 18 6 11 12 | 23, 24 | 187 < 188 |
| RC | 2 4 2 3 1 5 2 7 3 1 5 7 2 4 5 7 2 4 5 | 9, 9 | 71 < 72 |
| CR | 17 31 15 25 6 37 14 54 25 6 37 55 13 31 37 53 15 31 37 | 68, 67 | 539 < 540 |
| CC | 15 26 13 22 5 33 12 48 22 5 33 49 11 27 33 47 13 27 33 | 60, 59 | 474 < 476 |

Best allocation (minimum 103): R-agents get rows {4,5,6}, {9,10,11}, {14,15}, {18,19}; C-agents get {3,8}, {12,13}, {7,16}, {1,2,17} with utilities 116, 108, 104, 103.
