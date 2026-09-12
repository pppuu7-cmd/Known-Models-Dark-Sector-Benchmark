# W07 M33 cubic-tracker finer tangent localization v0.1

Date: 2026-09-12
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

## Motivation
The preregistered local-tangent run `34708771934` at base `Omega_smg=0.005` used central steps `h=0.001` and `h=0.0005`. All five provider arms executed, and symmetric displacement scales contracted, but the coarse/fine concatenated tangent failed the unchanged convergence gate (signed cosine -0.8871, principal angle 27.49 deg, norm mismatch 0.5036). This new diagnostic does not alter the threshold and does not erase that result.

## Frozen profile and stencil
Use the same exact pinned cubic tracker, `D_safe_smg=1e-100`, `a_min_stability_test_smg=0`, base `Omega_smg=0.005`, and same closure handling.

New same-build symmetric stencil:
- coarse: `Omega_smg=0.0045, 0.0055` (`h=0.0005`);
- fine: `Omega_smg=0.00475, 0.00525` (`h=0.00025`).

## Frozen response and criteria
Use the same global CMB+P(k) support and base-L2 block normalization as the parent tangent protocol. Combined central tangent convergence retains exactly:
- signed cosine >=0.995;
- principal angle <=5 deg;
- relative norm mismatch <=0.25;
- all displacements nonzero;
- fine symmetric displacement scale < coarse separately in CMB and P(k).

For localization only, compute the same signed cosine / principal angle / relative norm mismatch separately for the CMB derivative block and P(k) derivative block. These block diagnostics do not introduce new pass thresholds and cannot rescue a failed combined tangent.

## Interpretation
Combined pass -> `M33_CUBIC_TRACKER_FINER_LOCAL_TANGENT_CONVERGED_K2_SYNTHESIS_ELIGIBLE`.
Combined fail -> `M33_CUBIC_TRACKER_FINER_LOCAL_TANGENT_NOT_CONVERGED` with block-localization diagnostics retained.
Provider/control failure remains separate.

Always `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`, `all_Galileon_variants_claim=false`. Any K2 change requires a later synthesis that preserves both the larger-step negative result and this finer result.