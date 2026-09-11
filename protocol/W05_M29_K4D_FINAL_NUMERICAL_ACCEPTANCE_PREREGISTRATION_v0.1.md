# W05 M29 Brans-Dicke K4d final numerical acceptance preregistration v0.1

Date: 2026-09-11
Provider: `hiclass-code/hi_class_public` commit `0009f51d89e6465c79e570b496c66fc90058fa77`.
Parent evidence preserved: original K4 `M29_K4_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS`; K4b `M29_K4B_GRID_DOMINATED`; K4c `M29_K4C_FULL_CORE_REQUIRED`.

## Purpose

K4d is the first post-diagnostic acceptance gate allowed to promote K4. It prospectively retests both supported Brans-Dicke points using the numerical core localized by K4b/K4c against an independently tightened numerical reference. The original failed K4 remains part of the permanent audit record.

K3 remains separately `BLOCKED_IMPLEMENTATION` by provider gauge capability regardless of K4d outcome. No K4d failure is physical falsification.

## Frozen model points

Exactly the same two points and model conventions as the original K4:

- `omega_BD=15`
- `omega_BD=1e4`
- shipped `gravity_models/brans_dicke.ini`, changing only omega and output root.

## Frozen profiles

Three profiles are run independently for each omega (`fail-fast:false`).

### A. `coarse_localized`

Diagnostic coarse comparator:

- provider `cl_permille.pre`
- `background_Nloga=40000`
- K4b-localized reference k-grid:
  - `k_min_tau0=0.002`
  - `k_max_tau0_over_l_max=3`
  - `k_step_sub=0.015`
  - `k_step_super=0.0001`
  - `k_step_super_reduction=0.1`.

### B. `production_core`

The complete K4c-localized production numerical core. Use pinned provider `cl_ref.pre` with `background_Nloga=40000`. This is the production candidate, not the acceptance reference.

### C. `super_ref`

Start from the same pinned `cl_ref.pre`, then apply only prospectively frozen monotonic numerical refinements:

- `background_Nloga=80000` (2x production grid);
- `recfast_Nz0=200000` (2x production sampling);
- `tol_thermo_integration=5e-6` (2x tighter than production);
- `k_step_sub=0.0075` (2x finer);
- `k_step_super=0.00005` (2x finer);
- `tol_perturbations_integration=5e-7` (2x tighter);
- `perturbations_sampling_stepsize=0.005` (2x finer).

All other `cl_ref.pre` settings, model parameters and provider code are identical to `production_core`. These refinements were fixed before K4d execution and are not tuned from K4d outputs.

## Frozen observables and error metric

Same observables and symmetric-relative-error metric as original K4:

- background: column 3 of `*_background.dat` against column 0 coordinate;
- TT: column 1 of `*_cl.dat` against ell column 0;
- linear P(k): column 1 of `*_pk.dat` against k column 0;
- metric `2|x-y|/(|x|+|y|+1e-300)` on common support with linear interpolation of reference values.

For each omega compute max and RMS error of `coarse_localized` and `production_core` against `super_ref`.

## Original K4 thresholds preserved exactly

`production_core` passes an observable only if:

- TT: max <= `5e-3` and RMS <= `1e-3`;
- P(k): max <= `1e-3` and RMS <= `5e-4`;
- background: max <= `1e-4` and RMS <= `5e-5`.

Also preserve the original non-increase rule in the prospectively mapped coarse->production ladder: for each observable,

`RMS(production_core vs super_ref) <= 1.2 * RMS(coarse_localized vs super_ref)`.

No threshold is changed from original K4.

## Frozen classification

K4 is promoted only if, for both omega points:

1. all six branch executions return zero and all three observable tables are finite;
2. every production absolute threshold above passes;
3. every coarse->production 20% non-increase check passes.

Then: `M29_K4D_PASS_WITH_SCOPE_NUMERICAL_ROBUSTNESS` and `K4_promoted=true`.

If executions/finite output fail: `M29_K4D_BLOCKED_IMPLEMENTATION_OR_NUMERICAL_EXECUTION`.

Otherwise: `M29_K4D_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS`.

`physical_falsification=false` in every outcome. K4d does not resolve K3 or promote K5-K9.
