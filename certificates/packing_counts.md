# Packing certificates (two-type instances)

An allocation with all agents ≥ q exists iff a pairwise-disjoint R-sets of R-value ≥ q and b pairwise-disjoint C-sets of C-value ≥ q exist, all mutually disjoint (leftover goods can be added anywhere). Counting inclusion-minimal sets and disjoint tuples, "compatible pairs" = pairs (R-tuple, C-tuple) with disjoint unions (`verify/packing.cpp`) or pairs of distinct union masks (`verify/packing_pairs.cpp`). Zero at q = T proves non-existence; positive at q = T − 1 shows the best minimum is T − 1 (together with the DP).

| Instance | q | minimal R-sets | minimal C-sets | disjoint R-tuples | disjoint C-tuples | union masks R / C | compatible tuple pairs |
|---|---|---|---|---|---|---|---|
| 4×11 | 30 | 54 | 54 | 448 | 436 | 294 / 260 | 0 |
| 4×11 | 29 | 56 | 48 | 529 | 400 | 344 / 239 | 181 |
| 4×12 T=60 | 60 | 64 | 65 | 624 | 669 | 326 / 435 | 0 |
| 5×13 | 29 | 99 | 90 | 1746 | 6145 | 1034 / 1224 | 0 |
| 5×13 | 28 | 91 | 102 | 1587 | 9833 | 1013 / 1907 | 1072 |
| 6×15 | 28 | 145 | 147 | 38 473 | 42 520 | 8066 / 7967 | 0 |
| 6×15 | 27 | 118 | 145 | 27 273 | 46 807 | 7221 / 9266 | 9796 |
| 7×17 | 27 | 230 | 247 | 174 099 | 1 117 997 | 34 965 / 29 833 | 0 |
| 7×17 | 26 | 202 | 220 | 136 802 | 1 118 787 | 32 753 / 36 113 | 102 508 |

(5×13 C-tuples are triples; 7×17 C-tuples are quadruples. The 5×13 pair count 1520 quoted in earlier notes referred to C-pairs, not triples.) All numbers were obtained by two independent implementations (GPT-5.6 Pro's verifiers and `verify/packing.cpp`) and agree.
