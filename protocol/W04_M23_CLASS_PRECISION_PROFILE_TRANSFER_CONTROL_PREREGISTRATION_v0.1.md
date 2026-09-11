# W04 M23 shared-CLASS precision-profile transfer control — preregistration v0.1

Frozen before execution: 2026-09-11
Status: PROSPECTIVE
Purpose: localize the already-recorded M23 K4 precision-ladder nonmonotonicity without changing M23 physics, thresholds, or its preserved K4 result.

## Preserved parent evidence

Parent scientific result is immutable:
- run `34596841563`;
- canonical result commit `605d97039eedee0d779b8a2d518667a92a32250e`;
- aggregate artifact `10262840156`, digest `sha256:d36dc8134fe4d4066a0de635093610263915262c072d67152f335ffc86f7a1b4`;
- K3 common-observable cross-gauge PASS_WITH_SCOPE;
- K4 `M23_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED`.

Analysis-only localization at `waves/wave_04_dark_matter/M23_K4_PRECISION_LADDER_LOCALIZATION_RESULT.json` records that TT, EE and P(k) are nonmonotone in all 14 M23 case×gauge branches under the frozen `default -> cl_permille.pre -> repaired cl_ref.pre` ladder, while TE is stable. This control MUST NOT overwrite, weaken, or relabel that result.

## Question

Does the same default -> cl_permille -> cl_ref precision-profile nonmonotonicity occur in a pure LambdaCDM control under the same pinned CLASS build, output support, cosmological anchor, gauges and metric definition?

This is a provider/numerical-layer diagnostic only. It is not a new M23 physical gate and cannot produce a physical falsification.

## Provider pin

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

No source modification is permitted.

## Frozen control cosmology

Use the same M23 anchor where applicable, but remove IDM/IDR-specific content entirely:

- `h = 0.675`
- `omega_b = 0.0222`
- `omega_cdm = 0.1197`
- `A_s = 2.196e-9`
- `n_s = 0.9655`
- `tau_reio = 0.06`
- `N_ur = 3.046`
- no `f_idm`
- no `N_idr`
- no `Gamma_0_nadm`
- output `tCl,pCl,mPk`
- lensing `no`
- nonlinear `none`
- `P_k_max_h/Mpc = 20`
- `z_pk = 0`
- `l_max_scalars = 2500`

Run independently in `synchronous` and `newtonian` gauge.

## Frozen precision profiles

For each gauge run exactly:
1. `default`: no `.pre` file;
2. `permille`: stock pinned `cl_permille.pre`;
3. `reference`: stock pinned `cl_ref.pre`.

Because the control has no IDR sector, do NOT add the M23 IDR-trigger compatibility repair to the LambdaCDM control. The purpose is to test the stock provider precision profiles themselves.

## Frozen observables and metric

Use exactly the M23 K4 aggregate metric implementation and channel support:
- TT column 1 for ell >= 2;
- EE column 2;
- TE column 4;
- linear P(k) on the common positive-k support, log-k interpolation;
- normalized L2 residual `R(a,b)=||a-b||_2/max(||b||_2,1e-300)`.

For each gauge and each block define:
- `R_coarse = R(default, permille)`;
- `R_fine = R(permille, reference)`.

Retain the parent K4 numerical rule unchanged for diagnostic comparison only:
- absolute fine bound `R_fine <= 1e-4`;
- contraction `R_fine <= 0.5*R_coarse`, with the existing floor exception when `R_coarse <= 1e-8` and `R_fine <= 1e-8`.

Also record `nonmonotone = (R_fine > R_coarse)` independently of pass/fail.

## Prospectively frozen classification

After both gauges finish:

- `GENERAL_CLASS_PRECISION_PROFILE_NONNESTED_CONTROL` iff at least one of TT/EE/P(k) is nonmonotone in BOTH gauges. This establishes transfer of the failure mode to a pure LambdaCDM control and therefore supports a shared CLASS precision-profile interpretation. It does NOT establish that every CLASS model has the same floor.

- `M23_OR_IDR_SPECIFIC_PRECISION_NONMONOTONICITY` iff no TT/EE/P(k) block is nonmonotone in both gauges and all six provider executions succeed. This localizes the parent anomaly away from a generic pure-LambdaCDM stock-profile effect but does not identify its exact IDM/IDR cause.

- `CONTROL_MIXED_OR_INCONCLUSIVE` otherwise, including transfer in only one gauge or mixed blocks.

- `CONTROL_PROVIDER_BLOCKED` if any required provider execution fails or a required TT/TE/EE/P(k) product is missing.

No classification from this diagnostic changes M23 K3/K4, any other family's K-status, or physical viability.

## Parallelization and barrier

The synchronous and Newtonian controls are independent and MUST run as parallel jobs with `fail-fast:false`. Classification waits for an explicit barrier on both jobs. Green CI alone is not scientific PASS.

## Continuation rule

If `GENERAL_CLASS_PRECISION_PROFILE_NONNESTED_CONTROL`, preserve M23 K4 as NOT_ESTABLISHED and treat this ladder as unsuitable for model-specific K4 promotion until a separately preregistered nested numerical-tolerance sequence is source-justified. Do not tune a new sequence after inspecting model outputs.

If `M23_OR_IDR_SPECIFIC_PRECISION_NONMONOTONICITY`, the next diagnostic must localize IDM/IDR-specific precision controls prospectively; no physical retuning is allowed.

If BLOCKED or INCONCLUSIVE, diagnose the first causal infrastructure/provider issue only; do not reinterpret M23 physics.
