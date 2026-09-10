# W04 M21 integrator-branch diagnostic preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT
Date: 2026-09-11
Family: F21 / M21 mixed cold+warm DM

## Motivation
The previous M21 precision diagnostic established that the deterministic CMB excursion at warm fraction f_w=0.003 survives both `cl_permille.pre` and a source-bound tight ncdm profile. The anomaly is also present in normalized whole-vector L2 metrics, so it is not merely a p95/support artifact.

The remaining clean numerical hypothesis is an ODE-integrator branch effect. CLASS exposes two independent evolvers: enum value 0 is Runge-Kutta (`rk`) and the default is the stiff `ndf15` integrator. This diagnostic changes only that numerical integrator while preserving the physical model and the already frozen P2 precision profile.

## Provider
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Frozen physical cases
Reuse `verification/m21/mixed_cold_warm_k1_reference.py prepare` without edits.
Only these cases are run:
- `ref` (pure CDM)
- `f2`: f_w=0.01
- `f3`: f_w=0.003
- `f4`: f_w=0.001

All physical inputs, m_ncdm=3000 eV, T_ncdm=0.71611, total omega_dm=0.12 and abundance normalization are unchanged.

## Frozen precision profile
Both integrator branches use the exact P2 profile from the prior diagnostic:
- untouched pinned `cl_permille.pre`;
- concatenated source-bound `verification/m21/m21_ncdm_tight.pre`.

The RK branch adds only `evolver = 0` to that P2 file. No other precision or physics parameter is changed.

Branches:
- NDF: default `ndf15` (no explicit evolver override)
- RK: explicit `evolver = 0`

## Metrics
For TT, EE and TE, use the exact common ell grid and normalized whole-vector L2 residual to that branch's own reference:
`R2(f) = ||C_l(f)-C_l(ref)||_2 / max(||C_l(ref)||_2,1e-300)`.

For P(k), compare on positive common k support after log-k interpolation if necessary and use normalized L2. For H(z), canonicalize coordinate ordering before interpolation and use normalized L2.

For each branch/channel define the f_w=0.003 excursion factor:
`E = R2(0.003) / max(R2(0.01),R2(0.001),1e-300)`.

Also measure direct RK-vs-NDF normalized L2 differences for each physical case in TT/EE/TE/P(k). These direct differences are diagnostic only.

## Prospectively frozen classifications
Let `Emax_RK = max(E_RK_TT,E_RK_EE,E_RK_TE)` and `Emax_NDF` analogously.

- `M21_INTEGRATOR_BRANCH_LOCALIZED_TO_NDF15` if all three RK CMB excursion factors are <=3 while at least one NDF factor is >9.
- `M21_INTEGRATOR_BRANCH_REDUCES_EXCURSION` if not localized and `Emax_RK <= Emax_NDF/3`.
- `M21_INTEGRATOR_BRANCH_EXCURSION_PERSISTS` otherwise.
- `M21_INTEGRATOR_BRANCH_EXECUTION_BLOCKED` if any required run/product is missing or nonfinite.

No classification in this diagnostic promotes K1. `K1_promoted=false` is mandatory.

## Interpretation boundaries
- Localization to NDF15 would identify the anomaly as a solver-branch artifact and authorize a separately preregistered K1 recovery using the independent RK branch.
- Persistence in both integrators would rule out a simple single-integrator artifact and require a deeper source/phase-space-discretization audit before any K1 recovery.
- A large direct RK/NDF discrepancy is numerical evidence, not a physical mixed-WDM falsification.
- No K3-K9 promotion is allowed here.
