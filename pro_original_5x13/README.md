# Original search archive for the 5x13 instance (unmodified)

`mms5_5x13_T29_ratio28of29_20260901T132943Z.tar.zst` is the complete, unmodified archive produced
in the GPT-5.6 Pro search session of 1 September 2026 (SHA-256 in `SHA256SUMS`, matching the value
reported in the session). It contains, verbatim: the stochastic C++ search source and binary
(master seed 202609020013; hit on pattern 0x123e16d, restart 10, step 1777), the CEGIS driver on
SciPy/HiGHS (seed 202609051329, 8 iterations, 83 cuts), the full pattern enumeration for
m = 12..16, both bitwise replays, its own verifiers, checkpoints, environment manifest,
MANIFEST.sha256 and REPRODUCE.md. Unlike the 4-agent search (see ../PROVENANCE.md), the search
code for this instance is fully preserved. One known gap: the original shell command line of the
stochastic worker was not separately recorded; the source, binary, live log and seeds were, and
the deterministic replay reproduces the candidate bitwise.
