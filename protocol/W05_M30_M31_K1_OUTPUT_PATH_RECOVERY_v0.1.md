# W05 M30/M31 K1 output-path recovery — preregistration v0.1

Frozen before corrected analysis of the parent artifacts from Actions run `34656276938`.

The M30/M31 provider builds and all five frozen hi_class executions completed with exit 0. The parent analyzer requested `${label}_cl.dat` and `${label}_pk.dat`, while the pinned hi_class configuration writes `${label}_00_cl.dat` and `${label}_00_pk.dat`; the resulting FileNotFoundError is a harness/output-path defect only.

Recovery is analysis-only: reuse immutable parent artifacts `M30-k1-reference-limit` and `M31-k1-reference-limit`; do not rebuild hi_class or rerun cosmology. Replace only the analyzer input paths with the actually emitted `_00_cl.dat` and `_00_pk.dat` files. Preserve exact provider pin, frozen s={1,0.1,0.01,0.001} ladder, same-model zero reference, normalized-L2 statistic, and all K1 thresholds from `W05_PARALLEL_M30_M31_M40_K1_PREREGISTRATION_v0.1.md`.

Classification is exactly the original frozen rule. PASS requires finest<coarsest, every adjacent finer D <=1.20 times coarser D, finest/coarsest <=0.25, and log10(s)-log10(D) Pearson >=0.90. Failure is K1 NOT_ESTABLISHED, not physical falsification. Artifact byte reuse and exact parent run provenance are mandatory.