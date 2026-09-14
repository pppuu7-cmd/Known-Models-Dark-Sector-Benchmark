# W03 M13b K3D2-B phantom delta_y sign diagnostic v0.1

Frozen: 2026-09-14 after terminal run 34790860872 and before this diagnostic.

Parent protocol: `protocol/W03_M13B_K3D2B_ENABLED_TWO_FIELD_COSMOLOGY_REGRESSION_v0.1.md`.
Parent scientific run: `34790860872`, immutable full artifact `10327756907` (`sha256:4efbd193e5ab0943af4715fd262f9e695b5f65a1800bc971b6d48853727b4f9f`).
Exact provider pin remains `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Trigger

The certified default full run is finite and passes frozen B1 and B2. B3 fails only because the transformed Newtonian phantom direct-field perturbation `delta_y` has the opposite sign from the independent K3C2 bridge at today in both frozen modes. `Phi`, `delta_x`, `r`, and `t` retain the frozen sign requirements; all absolute-amplitude ratios, including `delta_y`, remain within the frozen broad ratio interval.

This is therefore a localization diagnostic only. It MUST NOT change, relax, remove, reinterpret, or replace the frozen B3 sign gate.

## Allowed evidence

Use only immutable artifacts from run `34790860872` plus repository-frozen K3C2 authority. No solver rerun is authorized by this diagnostic.

For each frozen mode (`khat=1`, `khat=10`) and for samples with `0<=z<=5`, reconstruct exactly the already frozen diagnostic transformation:

- `delta_y_N = delta_y_S + alpha*psi'_qpf`;
- `delta_y_prime_N = delta_y_prime_S + (-2*aH*alpha*psi'_qpf + a^2*V_psi*alpha + psi'_qpf*alpha')`;
- `t_N = delta_y_prime_N/(aH)`.

Apply only the already frozen common mode normalization `S_k=1e-5/Phi_N(z=5)`.

Record prospectively, without changing any gate:

1. today `delta_y_S`, gauge term `alpha*psi'_qpf`, transformed `delta_y_N`, and their normalized values;
2. whether the sign mismatch is already present in the raw synchronous direct field or is introduced by the gauge term;
3. all zero crossings of normalized `delta_y_N` on `0<=z<=5`;
4. the minimum/maximum normalized `delta_y_N` and `t_N` on that interval;
5. whether the transformed `delta_y_N` sign at today is stable under interpolation using the two nearest output rows;
6. K3C2 frozen endpoint sign and value, read without modification from `M13B_K3C2_INDEPENDENT_PERTURBATION_BRIDGE_RESULT.json`.

## Classification

This diagnostic cannot produce a scientific PASS.

- If both modes show a stable same-direction sign mismatch in `delta_y_N`, while B1/B2 and the other B3 variables remain as already recorded, classify `M13B_K3D2B_PHANTOM_DELTA_Y_SIGN_GAP_LOCALIZED` and retain the parent B3 FAIL / K3 PARTIAL state.
- If the sign is interpolation-unstable or created solely by a numerically dominant gauge cancellation, classify `M13B_K3D2B_PHANTOM_DELTA_Y_SIGN_DIAGNOSTIC_NUMERICAL_AMBIGUITY`; do not change the parent result.
- Any malformed/missing prior artifact is `DIAGNOSTIC_BLOCKED_EVIDENCE`, never physical falsification.

`physical_falsification=false`, `K4_promoted=false`, `K5_promoted=false` in all outcomes.

## Next gate rule

Only after this diagnostic is terminal may a new prospectively frozen source/equation consistency audit be opened. No sign flip, variable redefinition, altered initial conditions, seam movement, tolerance change, or post-hoc rephasing is allowed to rescue B3.
