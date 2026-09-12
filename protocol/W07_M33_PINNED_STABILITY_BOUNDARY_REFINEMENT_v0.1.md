# W07 M33 pinned-provider stability-boundary refinement v0.1

Date: 2026-09-12
Model: M33 cubic Galileon in pinned `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
Purpose: refine the already-observed empirical provider/config transition bracket between `Omega_smg=0.001` (scalar ghost-stability veto) and `Omega_smg=0.01` (executable finite CMB/P(k)).

## Frozen grid
Run the parser-compliant `gravity_models/galileon_3.ini` route at exactly:
`Omega_smg = {0.0015, 0.002, 0.003, 0.004, 0.006, 0.008}`.

For each point remove `Omega_Lambda` and `Omega_fld` exactly as in the successful parser-compliant recovery. Do not adaptively add points after seeing results.

## Classification
A point is `valid` only if provider exit=0 and finite CMB and P(k) tables are produced. A nonzero provider exit with the pinned scalar-stability ghost diagnostic is `provider_stability_veto`, not infrastructure failure and not family falsification. Other nonzero exits are separately `provider_or_harness_failure` and cannot define the stability boundary.

If the frozen grid contains at least one valid point and one provider-stability-veto point with an ordered transition, report the tightest adjacent tested bracket `[largest vetoed Omega_smg, smallest valid Omega_smg]`. Do not interpolate a universal theoretical critical value.

Always set `K1_promoted=false`, `physical_falsification=false`, `family_wide_stability_claim=false`. The result is scoped to the exact pinned provider/config and frozen grid.