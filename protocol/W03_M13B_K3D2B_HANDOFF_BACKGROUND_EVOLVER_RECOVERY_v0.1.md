# W03 M13b K3D2-B hard-handoff background-evolver recovery v0.1

Frozen: 2026-09-14 after run 34785090114 failed in both default and reference lanes before any B1/B2/B3 gate evaluation.

Parent protocols:
- `protocol/W03_M13B_K3D2B_ENABLED_TWO_FIELD_COSMOLOGY_REGRESSION_v0.1.md`
- `protocol/W03_M13B_K3D2B_Z5_IVP_HANDOFF_RECOVERY_v0.1.md`

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Observed numerical failure

The static z=5 handoff audit passed completely, but both enabled CLASS lanes stopped in `background_solve` before any physical regression gate was evaluated:

`evolver_ndf15: Step size too small ... interval [-32.2362:0]`.

The failure is identical in the default and `cl_ref.pre` runs and is caused by the discontinuous derivative at the prospectively frozen hard handoff `a=1/6`: NDF15 repeatedly shrinks its implicit step while trying to straddle the exact RHS switch.

This is a numerical-integrator compatibility failure, not an enabled cosmology result.

## Frozen recovery

Use CLASS's existing explicit Runge-Kutta background integrator for the hard-handoff realization:

`background_evolver = rk`

in both the default and reference-precision enabled K3D2-B runs.

No source equation is modified by this recovery. In particular:

- the pre-handoff qcf/qpf background RHS remains exactly zero;
- the post-handoff qcf/qpf canonical/phantom KG RHS remains byte-identical to the already frozen K3D2 adapter;
- the handoff remains exactly `a=1/6` with no smoothing/ramp;
- qcf/qpf perturbation handoff semantics remain unchanged;
- all cosmological parameters, U0, field starts, mode definitions and B1/B2/B3 thresholds remain unchanged;
- `cl_ref.pre` remains otherwise unchanged.

## Required numerical cross-check

The use of RK for the handoff realization must not be treated as an unchecked solver substitution.

A separate control shall run the adapter with qcf=qpf disabled under the exact same standard LambdaCDM control using both `background_evolver=ndf15` and `background_evolver=rk`. Require:

- both return codes zero;
- common linear P(k) normalized L2 `<=1e-8`;
- H(z=0) relative difference `<=1e-10` where directly available from the background table;
- no qcf/qpf output is active in this numerical-control comparison.

This cross-check is a numerical-solver audit only; it does not replace the already passed K3D2-A exact null regression.

## Interpretation

Run 34785090114 is classified as `HARD_HANDOFF_NDF15_NUMERICAL_INCOMPATIBILITY_NO_B1_B2_B3_EVALUATION`.

Only the RK recovered run may evaluate the already frozen B1/B2/B3 gates. Thresholds may not be changed based on that output.
