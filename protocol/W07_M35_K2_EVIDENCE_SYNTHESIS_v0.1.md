# W07 M35 K2 evidence synthesis v0.1

Date: 2026-09-12
Model: M35 Einstein–Aether / Lorentz-violating gravity in pinned CLASS_LVDM scalar-cosmology representation
Purpose: immutable bookkeeping synthesis for K2 only

## Frozen inputs
Use only these already-terminal immutable artifacts:

- K1 weak-coupling ladder: run `34657362639`, artifact `10286581994`.
- K2 path-geometry audit: run `34667748388`, artifact `10288863878`.
- orthogonal Y_dm coverage: run `34667885612`, artifact `10289609230`.
- local 2D response Jacobian: run `34668120323`, artifact `10290165068`.

All must identify provider commit `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1` where applicable.

## Frozen classification rule
Assign `M35_K2_PARTIAL_LOCAL_RESPONSE_RANK2_SOURCE_QUOTIENT_OPEN` iff all are true:

1. K1 artifact has `K1_promoted=true` and `physical_falsification=false`.
2. K2 path audit establishes that the original gravity ladder is a narrow/radial path and does not itself close K2.
3. Y_dm artifact classification is `M35_YDM_DIRECTION_EXECUTABLE_CONTRACTING` with all prospectively frozen arms executable.
4. 2D Jacobian artifact classification is `M35_LOCAL_2D_RESPONSE_RANK_EVIDENCE`, both finite-difference directions converged, cross-direction separation passed, and `K2_promoted=false`.

If any immutable prerequisite is absent/inconsistent, assign `M35_K2_SYNTHESIS_INTEGRITY_BLOCKED`.
If prerequisites are valid but the independent local rank condition did not pass, assign `M35_K2_OPEN_LOCAL_RANK_NOT_ESTABLISHED`.

## Meaning of PARTIAL
`PARTIAL` means only that the pinned scalar CLASS_LVDM representation has reproducible local evidence for at least two response-distinct parameter directions (gravity-ray and Y_dm), beyond the original one-dimensional K1 path.

It does NOT establish:
- the complete Einstein–Aether scalar/vector/tensor parameter geometry;
- the covariant quotient by field/frame/reparameterization redundancies;
- K3 conservation/gauge/frame closure;
- K4–K9;
- observational identifiability or family falsification.

Therefore this synthesis can recommend K2=`PARTIAL` but can never assign K2=`PASS`.
