# W03 M13b K3D2-B perturbation interval-boundary audit v0.1

Frozen: 2026-09-14 after default full CLASS run 34788012803 failed inside `perturbations_solve` and before any perturbation-seam patch.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Parent background recovery: U1 from `protocol/W03_M13B_K3D2B_POST_HANDOFF_ULP_SEAM_RECOVERY_v0.1.md`.

## Observed blocker

With background U1 recovery active, full CLASS reaches perturbations and fails before B1/B2/B3 evaluation:

`perturbations_solve -> generic_evolver(perturbations_derivs, interval_limit[index_interval], interval_limit[index_interval+1], ...) -> evolver_ndf15: Step size too small`, with the reported interval `[558.061, 13984.9]`.

This is an implementation/numerical blocker. It is not a frozen B1/B2/B3 failure and not physical falsification.

## Audit question

Determine from exact-pin source whether CLASS already represents perturbation evolution as multiple integration intervals with mutable `interval_limit[]`, and whether a model-specific conformal-time boundary can be inserted without altering:

- perturbation equations on open intervals;
- approximation definitions or switching conditions;
- photon/polarization/neutrino hierarchy equations;
- Einstein source equations;
- tolerances or solver family;
- primordial initial conditions.

The target model boundary is the same frozen physical event `a=1/6` (`z=5`). Its conformal time must be obtained through the existing exact background mapping, not a fitted numerical constant.

## Source-audit PASS requirements

PASS requires all of the following in `perturbations_solve` or its directly called interval-construction helpers:

1. perturbations are integrated by `generic_evolver` over consecutive `interval_limit[index_interval] -> interval_limit[index_interval+1]` ranges;
2. interval limits are stored in a mutable allocated array and an explicit interval count exists;
3. integration state is carried in `ppw->pv->y` between intervals;
4. the source/output sampling array is global across those intervals rather than redefined per model boundary;
5. CLASS exposes an exact background redshift/scale-factor to conformal-time mapping usable to obtain tau at z=5;
6. an extra boundary can be inserted as an integration split while leaving approximation flags on either side determined by existing CLASS logic;
7. no change to the perturbation RHS is required merely to split the interval.

PASS classification:

`M13B_K3D2B_PERTURBATION_NATIVE_INTERVAL_SPLIT_STRUCTURALLY_AUTHORIZED_WITH_SCOPE`.

PASS authorizes only a separately frozen implementation probe with disabled-adapter null regression and enabled qcf+qpf execution. It does not authorize B1/B2/B3 promotion.

FAIL classification:

`M13B_K3D2B_PERTURBATION_NATIVE_INTERVAL_SPLIT_NOT_ESTABLISHED`.

On FAIL, do not patch `interval_limit` heuristically; inspect an alternative native restart route.
