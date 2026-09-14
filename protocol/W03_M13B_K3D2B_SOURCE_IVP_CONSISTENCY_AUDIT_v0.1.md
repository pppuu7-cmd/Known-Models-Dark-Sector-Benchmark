# W03 M13b K3D2-B source / IVP consistency audit v0.1

Frozen: 2026-09-14 after terminal parent full run `34790860872` and terminal artifact-only phantom-sign diagnostic `34791327872`, before execution of this confirmatory audit.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Parent full artifact: `10327756907` (`sha256:4efbd193e5ab0943af4715fd262f9e695b5f65a1800bc971b6d48853727b4f9f`).
Parent B3 verdict: `M13B_K3D2B_CERTIFIED_DEFAULT_FULL_B123_GAP`.
Parent diagnostic: `M13B_K3D2B_PHANTOM_DELTA_Y_SIGN_DIAGNOSTIC_NUMERICAL_AMBIGUITY`.

## Purpose

Localize whether the surviving B3 phantom `delta_y` sign gap is caused by:

1. a source-equation/sign inconsistency in the independent CLASS qcf+qpf adapter; or
2. a mismatch between the frozen K3C2 **Newtonian-gauge** initial surface and the adapter's **synchronous-gauge** direct-field initial surface.

This audit is diagnostic only. It MUST NOT rerun the cosmology solver, flip a sign, change the seam, retune a threshold, change a potential, change the K3C2 target, or alter the historical parent B3 verdict.

## Frozen authorities

K3C2 starts at `z=5` in Newtonian gauge with

- `delta_x_N = r_N = delta_y_N = t_N = 0`;
- `Phi_i=1e-5`, `W_i=0`.

The K3D2-B frozen gauge transforms are

- `delta_x_N = delta_x_S + alpha*phi'`;
- `delta_x_prime_N = delta_x_prime_S + (-2*aH*alpha*phi' - a^2*V_phi*alpha + phi'*alpha')`;
- `delta_y_N = delta_y_S + alpha*psi'`;
- `delta_y_prime_N = delta_y_prime_S + (-2*aH*alpha*psi' + a^2*V_psi*alpha + psi'*alpha')`.

At the exact K3C1 handoff, the frozen background IVP has `phi'=psi'=0` before post-handoff evolution. Therefore a Newtonian zero-derivative seed requires, at the exact boundary,

- `delta_x_prime_S = +a^2*V_phi*alpha`;
- `delta_y_prime_S = -a^2*V_psi*alpha`;

when `phi'=psi'=0`; the general formulas retain the displayed `phi'`, `psi'`, and `alpha'` terms.

The current adapter source is known to freeze both synchronous direct fields and their synchronous derivatives to zero before the handoff. This audit tests whether that source choice is gauge-equivalent to K3C2, not whether another choice gives a preferred late-time sign.

## Lane A — source equation and stress-energy audit

Apply only the frozen K3D2 adapter to the exact provider pin and inspect generated source. Require all of:

1. canonical qcf perturbation mass term is `k^2 + a^2 V_phi_phi`;
2. phantom qpf perturbation mass term is `k^2 - a^2 V_psi_psi`;
3. qcf and qpf synchronous metric-continuity terms have the same kinetic-source sign;
4. phantom background equation is equivalent to `psi'' + 2 a H psi' - a^2 V_psi = 0`;
5. qpf `delta_rho`, `delta_p`, and momentum-source signs equal the frozen K3D2-A preregistration;
6. no combined qcf+qpf `rho+p`, `D`, or effective `theta_DE` denominator is introduced.

If any required source sign fails, classify the source lane `SOURCE_EQUATION_SIGN_INCONSISTENCY`.

## Lane B — initial-surface identity and immutable-artifact witness

Use only immutable parent artifact `10327756907` plus the frozen canonical K3C2 result. Do not execute CLASS.

For each frozen mode, inspect the first output row at the certified `z=5` handoff and reconstruct the already frozen Newtonian transform. Record:

- `alpha`, `alpha'`, background `phi'`, `psi'`, `V_phi`, `V_psi`;
- synchronous `delta_x_S`, `delta_x_prime_S`, `delta_y_S`, `delta_y_prime_S`;
- transformed Newtonian `delta_x_N`, `r_N`, `delta_y_N`, `t_N`;
- the same four quantities after the one frozen common mode normalization `S_k=1e-5/Phi_N(z=5)`.

The K3C2 target seed is exactly zero for all four direct-field variables. A transformed derivative magnitude above the existing K3C2/B3 exclusion floor `1e-12` is a resolved nonzero initial-surface mismatch; no new tolerance is introduced.

The lane passes the mismatch witness if both frozen modes satisfy all of:

1. synchronous qcf/qpf field values and derivatives at the handoff row are zero to printed artifact precision;
2. `alpha` is finite and nonzero;
3. `V_phi` and `V_psi` are finite and nonzero;
4. normalized transformed `|r_N| > 1e-12` and `|t_N| > 1e-12`;
5. the transformed phantom `t_N` has the same sign in both modes;
6. the witness is computed without endpoint fitting, per-variable rescaling, or sign rephasing.

This lane does not require the qcf mismatch to cause a late-time sign failure; it only tests whether the intended same-IVP contract was realized.

## Lane C — native-boundary implementation feasibility audit

Source-only. No solver execution.

Inspect exact-pin CLASS plus the already frozen native perturbation interval split. Determine whether the `z=5` boundary path can set qcf/qpf synchronous field states from the frozen gauge-map identities while leaving all photon, polarization, ur/ncdm, Einstein-source, thermodynamics, primordial, and nonlinear equations unchanged.

PASS requires a concrete source location and data path for:

- exact boundary detection;
- background `phi'`, `psi'`, `V_phi`, `V_psi`, `aH`;
- the synchronous metric gauge generator information needed by the frozen transform (`alpha`, and `alpha'` if nonzero background velocities are retained numerically);
- mode-local qcf/qpf state assignment before the right-owned post-handoff evolver begins;
- no new free parameter and no per-mode fitted coefficient.

If the exact gauge-map inputs are not available at the boundary without changing protected equations, classify `GAUGE_MAPPED_IVP_IMPLEMENTATION_NOT_YET_DEFINED`.

## Aggregate classification

If Lane A passes, Lane B proves a nonzero Newtonian-start mismatch, and Lane C establishes a source-clean implementation path, classify:

`M13B_K3D2B_EQUATIONS_CONSISTENT_IVP_GAUGE_MISMATCH_CONFIRMED`.

Interpretation: the historical B3 FAIL remains a valid result for the executed synchronous-zero initialization, but it is not a clean same-initial-surface test of the frozen K3C2 Newtonian IVP. This is an implementation-contract localization, not a scientific PASS and not a physical falsification.

If Lane A finds a sign/equation mismatch, classify:

`M13B_K3D2B_SOURCE_EQUATION_INCONSISTENCY_FOUND`.

If source equations pass but the initial-surface mismatch cannot be established or the evidence is malformed, classify:

`M13B_K3D2B_SOURCE_IVP_AUDIT_INCONCLUSIVE`.

In all outcomes:

- historical parent B3 verdict is not rewritten;
- `K3_state_ceiling=PARTIAL`;
- `K4_promoted=false`;
- `K5_promoted=false`;
- `physical_falsification=false`;
- no author-code or published-`V0` claim is introduced.

## Next-gate rule

Only `M13B_K3D2B_EQUATIONS_CONSISTENT_IVP_GAUGE_MISMATCH_CONFIRMED` may authorize a **new prospectively frozen successor** that initializes qcf/qpf in synchronous gauge by the exact frozen gauge map of the K3C2 Newtonian zero seed. The successor must preserve the old B3 result, all K3C1/K3C2 equations, cosmology, modes, normalization, B1/B2/B3 thresholds, and the certified numerical seam. It may not use a manual sign flip, endpoint fitting, or late-time tuning.
