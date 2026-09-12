# W04 M22 annihilating-DM K4 precision-ladder localization preregistration v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Parent K1: `M22_K1_V2_REFERENCE_LIMIT_PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION`.

## Purpose
Localize numerical precision sensitivity of the already-scoped M22 energy-injection response before any canonical K4 claim. This diagnostic does not alter K1, K3, or physical interpretation.

## Frozen physics
Reuse the K1-v2 cosmology and native CLASS `DM_annihilation_efficiency` coordinate exactly. Select three preregistered K1-v2 response points spanning the ladder:
- strong: `p0 = 1.11e-23 m^3 s^-1 J^-1`;
- mid: `p3 = 3.33e-25`;
- tail: `p5 = 3.33e-26`.

For every numerical profile also run the omitted-input reference and explicit `DM_annihilation_efficiency=0` zero control.

## Frozen numerical profiles
1. `default`: provider default precision, identical to K1-v2.
2. `permille`: provider-shipped `cl_permille.pre` as the second CLASS input.
3. `reference`: provider-shipped `cl_ref.pre` as the second CLASS input.

No precision-file content is edited.

## Frozen metrics
For each profile require all five cases to execute and require zero-vs-omitted normalized-L2 <=1e-12 in TT/EE/TE/P(k).
For each p_ann point compute its TT/EE/TE/P(k) normalized-L2 response relative to that profile's own explicit-zero output.
For each of the 12 response cells compute symmetric profile discrepancy for default->permille and permille->reference:
`D=2|R_b-R_a|/(|R_b|+|R_a|+1e-30)`.
Record maximum and median D for each profile step.

## Frozen diagnostic interpretation
- all integrity checks pass, max(D_permille_to_reference)<=0.10 and max(D_permille_to_reference)<=max(D_default_to_permille): `M22_K4_PRECISION_CONVERGENCE_CANDIDATE_DIAGNOSTIC`;
- all integrity checks pass and terminal max improves but remains >0.10: `M22_K4_PRECISION_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`;
- all integrity checks pass and terminal max does not improve: `M22_K4_PRECISION_NONMONOTONE_OR_NONCONVERGED_DIAGNOSTIC`;
- execution/profile/integrity failure: `M22_K4_PRECISION_LADDER_BLOCKED`.

Always diagnostic-only: `K4_promoted=false`, `physical_falsification=false`, `scientific_fail=false`. A later synthesis is required before canonical K4 status can change.
