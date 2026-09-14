# W04 M21 secondary thermodynamics-state branch-signature audit v0.1

Frozen: 2026-09-14 after terminal explicit-none parser recovery run `34887773207` classified `M21_CMB_BRANCH_NOT_LOCALIZED_IN_PRIMARY_THERMO_STATE_COLUMNS`, and before any secondary-column aggregate is computed.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is an **analysis-only** continuation. It MUST reuse the six immutable thermodynamics-state artifacts from run `34887773207`; no CLASS execution or physical/numerical retuning is allowed.

## Motivation

The primary state audit tested only `x_e`, `kappa'`, `exp(-kappa)`, `g`, and `Tb`. Exact provider thermodynamics tables also expose downstream thermodynamic state columns not used by that classifier:

- conformal time `[Mpc]`;
- `dTb [K]`;
- `w_b`;
- `c_b^2`;
- `kappa_b` (baryon-drag optical-depth state).

The numerical CMB branch map remains the frozen parent map:

- NDF15 1e-5: REMOVES
- NDF15 1e-6: INSUFFICIENT
- NDF15 1e-7: REMOVES
- RK 1e-5: REMOVES
- RK 1e-6: INSUFFICIENT
- RK 1e-7: INSUFFICIENT

This audit asks whether the f_w=0.003-specific branch signature is present in these additional **already-computed** state variables even though it is absent from the five primary columns.

## Frozen artifacts

Authoritative parent run: `34887773207`.

Required artifact names exactly:
- `m21-thermo-state-NDF_T1E5`
- `m21-thermo-state-NDF_T1E6`
- `m21-thermo-state-NDF_T1E7`
- `m21-thermo-state-RK_T1E5`
- `m21-thermo-state-RK_T1E6`
- `m21-thermo-state-RK_T1E7`

The parent aggregate must have classification exactly `M21_CMB_BRANCH_NOT_LOCALIZED_IN_PRIMARY_THERMO_STATE_COLUMNS`, `cross_lane_input_identity=true`, `K1_promoted=false`, and `physical_falsification=false`.

## Frozen coordinate/window/metric

Reuse the exact parent rules:
- redshift `z`, sorted ascending;
- strict overlap only, interpolation in `log1p(z)`;
- primary window `500 <= z <= 2500`;
- normalized symmetric L2 distance `||a-b|| / max(||a||,||b||,1e-300)`;
- full-overlap values are report-only.

Secondary columns are frozen to exact zero-based table indices:
- `conf_time`: 2
- `dTb`: 8
- `w_b`: 9
- `c_b2`: 10
- `kappa_b`: 11

## Frozen edges and threshold

Branch-change edges:
- `NDF_T1E5__NDF_T1E6`
- `NDF_T1E6__NDF_T1E7`
- `RK_T1E5__RK_T1E6`
- `NDF_T1E7__RK_T1E7`

Same-branch controls:
- `RK_T1E6__RK_T1E7`
- `NDF_T1E5__RK_T1E5`
- `NDF_T1E6__RK_T1E6`

For each column and edge define
`J = D_f3 / max(D_ref,D_f2,D_f4,1e-300)`.

`Jmax >= 3` is frozen as f3-specific localization evidence for that edge.

## Frozen classification

Artifact/schema/input identity failure -> `M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_BLOCKED`.

All four branch-change edges localized and zero same-branch controls localized -> `M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE`.

At least two branch-change edges localized but full pattern fails -> `M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_PARTIAL`.

Fewer than two branch-change edges localized -> `M21_CMB_BRANCH_NOT_LOCALIZED_IN_EXPOSED_THERMO_STATE_COLUMNS`.

## Consequence rule

If the final class is `...NOT_LOCALIZED_IN_EXPOSED_THERMO_STATE_COLUMNS`, no further thermodynamics-state column mining is authorized from this table. The next scientific localization must move downstream to perturbation/source/transfer quantities or remain a numerical-path blocker.

Any MATCH/PARTIAL result is only state-localization evidence and does not establish a CLASS bug, production setting, global convergence, K1/K3/K4 promotion, or physical M21 failure.
