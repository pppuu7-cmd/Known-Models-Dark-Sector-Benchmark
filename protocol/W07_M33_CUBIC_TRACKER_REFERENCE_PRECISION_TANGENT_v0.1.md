# W07 M33 cubic-tracker reference-precision tangent diagnostic v0.1

Date: 2026-09-12
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

## Motivation
The canonical M33 K1 gate now passes with scope, while K2 remains OPEN. The same-build default-precision finer central tangent at base `Omega_smg=0.005`, `h={0.0005,0.00025}`, failed the unchanged derivative-convergence gate. The pinned provider ships `cl_ref.pre`, documented as a maximum/reference CMB precision profile. This diagnostic asks whether the *same frozen physical stencil* converges under that provider reference precision. It does not reduce the step size and does not relax any threshold.

## Frozen physical profile and stencil
Unchanged from `W07_M33_CUBIC_TRACKER_FINER_TANGENT_LOCALIZATION_v0.1`:
- cubic tracker `gravity_models/galileon_3.ini`;
- `D_safe_smg=1e-100`, `a_min_stability_test_smg=0`;
- base `Omega_smg=0.005`;
- coarse central pair `0.0045,0.0055`, `h=0.0005`;
- fine central pair `0.00475,0.00525`, `h=0.00025`;
- identical closure removal and output blocks.

The only changed numerical profile is supplying the exact provider-shipped `cl_ref.pre` as the second hi_class input file. No contents of `cl_ref.pre` are edited.

## Frozen response and criteria
Use the identical global CMB+P(k) common support and base-L2 block normalization as the default finer-tangent run. Combined tangent convergence retains exactly:
- signed cosine >=0.995;
- principal angle <=5 deg;
- relative norm mismatch <=0.25;
- all displacements nonzero;
- fine symmetric displacement scale < coarse separately in CMB and P(k).

Also retain separate CMB and P(k) block diagnostics without allowing either block to rescue a failed combined gate.

## Frozen interpretation
- all combined criteria pass -> `M33_CUBIC_TRACKER_REFERENCE_PRECISION_TANGENT_CONVERGED_SYNTHESIS_REQUIRED`;
- execution succeeds but any combined criterion fails -> `M33_CUBIC_TRACKER_REFERENCE_PRECISION_TANGENT_NONCONVERGENCE_PERSISTS`;
- provider/control/integrity problem -> `M33_CUBIC_TRACKER_REFERENCE_PRECISION_TANGENT_BLOCKED`.

Always `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`. Even a reference-precision convergence result requires a later immutable synthesis preserving both default-precision negative tangent results before any K2 status change.
