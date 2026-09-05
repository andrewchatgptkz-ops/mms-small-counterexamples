# GPT-6 Pro theory session (2026-09-05, prompt P17): gadget signatures, depth-2 certificates, invariant

`mms_theory_final.zip` is the model's own snapshot, verbatim (REPORT.md, REPRODUCE.md, scripts/, logs/, MANIFEST.sha256, `8x19_depth2.json`, `verify_new_certificate.py`). Contents in one line each:
- a proof that the fixed-quota (22, 23) chain certificate cannot be continued indefinitely (E = b − 1, D + z = 22 − a) and a correction to our rigidity statement (n = 5: column c4 weighs 24);
- a counterexample to locality of the subdivision gadget (6×15 with C(g2) += 2, C(g11) −= 2 admits an MMS allocation);
- the 8×19 instance with T = 104 and best minimum 103, synthesised from a depth-2 certificate, with the parametric line B(ε) = max(26 − ε, 25 + 3ε) around the T = 26 score-2 profile;
- the polyhedral reading of the chain (forbidden knapsack polytopes) and a four-term lifting rule for the knapsack envelopes at 5 → 6 and 6 → 7;
- the balanced-prism, depth-two conjecture.
Everything numerical was re-verified independently (see `PROVENANCE.md`); the instance and certificate are in `instances/8x19_T104.json` and `verify/verify_certificate.py`.
