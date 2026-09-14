# W04 M21 thermodynamics-state branch-signature audit v0.1

Frozen: 2026-09-14 after terminal cross-evolver recovery run `34884124030` and before any thermodynamics-state execution.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Parent authority: `M21_THERMO_EVOLVER_DEPENDENCE_MIXED`, cross-lane input identity true.

## Motivation

The terminal parent gives the following immutable CMB branch map:

- NDF15 1e-5: REMOVES
- NDF15 1e-6: INSUFFICIENT
- NDF15 1e-7: REMOVES
- RK 1e-5: REMOVES
- RK 1e-6: INSUFFICIENT
- RK 1e-7: INSUFFICIENT

Because `thermo_evolver` acts before perturbations/transfer/harmonic, the next high-information question is whether the f_w=0.003-specific numerical branch signature is already present in the thermodynamics state passed downstream.

## Frozen state execution

Reuse the exact six parent solver/tolerance pairs and exact physical cases `ref,f2,f3,f4`.

For each physical case, derive a thermodynamics-state INI from the existing M21 K1 generator by:

1. preserving every physical/cosmological/ncdm line verbatim;
2. removing only the expensive spectrum request line `output = tCl,pCl,mPk`;
3. adding `write_thermodynamics = yes`;
4. keeping the original root and background writing.

Exact source order computes background and thermodynamics before perturbations; removing requested spectra is permitted only for this state-localization diagnostic and its outputs may never substitute for K1 CMB/P(k) runs.

Precision baseline remains `cl_permille.pre + verification/m21/m21_ncdm_tight.pre + evolver=0`, plus the frozen solver/tolerance pair. No other precision key changes.

## Frozen thermodynamics columns and window

Exact output title authority fixes the primary state columns:

- `x_e`
- `kappa' [Mpc^-1]`
- `exp(-kappa)`
- `g [Mpc^-1]`
- `Tb [K]`

Use redshift `z` as coordinate, sort ascending, strict overlap only, and interpolate in `log1p(z)`.

Primary recombination window: `500 <= z <= 2500`.
Full-overlap metrics are report-only.

For each state column, lane and finite case, compute normalized L2 relative to the same-lane exact-CDM reference.

## Frozen edge signature

For any pair of numerical lanes A/B and physical case c, define direct state distance `D_c(A,B)` as normalized L2 after the same frozen z alignment/window.

Define f3-specific jump factor
`J(A,B) = D_f3(A,B) / max(D_ref(A,B), D_f2(A,B), D_f4(A,B), 1e-300)`.

For each edge report J separately for all five primary columns and define `Jmax` as their maximum.

Frozen **branch-change edges** from the terminal CMB parent:

- `NDF_T1E5__NDF_T1E6`
- `NDF_T1E6__NDF_T1E7`
- `RK_T1E5__RK_T1E6`
- `NDF_T1E7__RK_T1E7`

Frozen **same-branch control edges**:

- `RK_T1E6__RK_T1E7`
- `NDF_T1E5__RK_T1E5`
- `NDF_T1E6__RK_T1E6`

Threshold `Jmax >= 3` is frozen here as evidence of f3-specific state localization; `<3` is non-localized for that edge. Thresholds are not adjustable after execution.

## Frozen classification

Any execution, pin, state-schema or physical-input identity failure:
`M21_THERMO_STATE_BRANCH_SIGNATURE_BLOCKED`.

If all four branch-change edges have `Jmax>=3` and all three same-branch controls have `Jmax<3`:
`M21_THERMO_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE`.

If at least two branch-change edges have `Jmax>=3`, but the exact full pattern above fails:
`M21_THERMO_STATE_BRANCH_SIGNATURE_PARTIAL`.

If fewer than two branch-change edges have `Jmax>=3`:
`M21_CMB_BRANCH_NOT_LOCALIZED_IN_PRIMARY_THERMO_STATE_COLUMNS`.

## Claim ceiling

This audit may localize the numerical branch to thermodynamics state output. It cannot identify a CLASS defect, select a production tolerance, establish global convergence, authorize K1-v2, promote K1/K3/K4, or yield a physical M21 verdict.
