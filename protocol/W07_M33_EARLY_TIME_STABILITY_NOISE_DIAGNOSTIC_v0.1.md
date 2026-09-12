# W07 M33 early-time stability-noise diagnostic preregistration v0.1

Date: 2026-09-12
Model: pinned cubic Galileon `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
Purpose: diagnose whether the reproducible tiny negative `D_smg` vetoes at `a=1e-14` are sensitive to provider-documented numerical-noise controls. This workflow is diagnostic only and cannot convert a vetoed baseline into a physical stability pass.

## Frozen points
Use exactly the reproducibly vetoed/tested points `Omega_smg={0.001,0.0035,0.004,0.0045,0.005}`.

## Frozen profiles
For every point execute three parser-compliant otherwise-identical configs:
1. `baseline`: provider defaults, `D_safe_smg=0`, `a_min_stability_test_smg=0`;
2. `late_start`: retain `D_safe_smg=0` and set `a_min_stability_test_smg=1e-13`, one decade after the observed `a=1e-14` minima;
3. `tiny_D_safe`: retain `a_min_stability_test_smg=0` and set `D_safe_smg=1e-100`, still an extremely small dimensionless tolerance but above the observed ~1e-106 sign excursions.

These values are frozen before execution. No adaptive tolerance changes are allowed.

## Frozen classification
For each profile/point record exit, finite CMB/P(k), and any ghost diagnostic. The baseline must reproduce the prior veto pattern for the diagnostic to be interpretable.

If baseline vetoes reproduce and both diagnostic profiles remove the ghost veto with finite outputs at all frozen points, classify `M33_TINY_EARLY_D_VETO_PROVIDER_NOISE_CONTROLS_SENSITIVE`. If only one profile does so, classify the corresponding sensitivity. If baseline does not reproduce, classify integrity/reproducibility blocked.

Even a sensitivity result means only that the pinned provider's strict zero-threshold classification is controlled by the earliest-time/tiny-D numerical handling. It does NOT establish physical stability of the cubic Galileon family and does not promote K1.

Always set `K1_promoted=false`, `physical_falsification=false`, `family_wide_stability_claim=false`.