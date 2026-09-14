# W04 M21 conditional thermodynamics-tolerance direction audit v0.1

Frozen: 2026-09-14 while stage-3 run `34878158930` is non-terminal and before any tolerance-ladder execution.

Status: **CONDITIONAL / NOT AUTHORIZED UNTIL TERMINAL STAGE-3 ACTIVATION**.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Motivation fixed before stage-3 result

Outcome-independent exact-pin source audit established that among the four G1A assignments only `tol_thermo_integration` has runtime consumers. It also established that exact `cl_ref.pre` sets `tol_thermo_integration=1e-5` while the exact-pin default is `1e-6`; hence the reference value is looser, not tighter, than the default. Stage-2 G1A removed the CMB excursion, but a reference-profile path difference is not a convergence proof.

This gate asks only whether the stage-3 thermodynamics-tolerance effect, if stage-3 actually identifies it, persists directionally as the tolerance is tightened.

## Activation condition

Execution is authorized iff the terminal artifact from workflow `W04 M21 CMB precision stage3 single-parameter decomposition v0.1` satisfies all of:

1. `classification == M21_CMB_PRECISION_STAGE3_COMPLETE`;
2. `cross_lane_input_identity == true`;
3. parameter `G1A__tol_thermo_integration` has classification `PARAMETER_REMOVES_EXCURSION` or `PARAMETER_REDUCES_EXCURSION`;
4. G1A is not stage-3 blocked.

If any condition fails, this gate remains unexecuted historical preparation. No substitute parameter may be selected.

## Frozen scientific object

Same exact CLASS binary family and same M21 physical cases `ref/f2/f3/f4` as stage-3. Common baseline remains:

- exact `cl_permille.pre`;
- `verification/m21/m21_ncdm_tight.pre`;
- `evolver=0`;
- no other stage-1/2/3 reference-profile assignment.

The only varied key is `tol_thermo_integration`.

## Frozen tolerance ladder

Mandatory independent values:

- `T1E4 = 1e-4`
- `T3E5 = 3e-5`
- `T1E5 = 1e-5`  (the conditional stage-3/reference-profile value)
- `T3E6 = 3e-6`
- `T1E6 = 1e-6`  (exact-pin default)
- `T3E7 = 3e-7`
- `T1E7 = 1e-7`

All seven values are frozen before stage-3 outcome. No additional point may be inserted after results.

## Execution

Seven independent tolerance jobs may run in parallel. Each builds/uses the exact pin and executes immutable `ref/f2/f3/f4` sequentially. Each CLASS case has a hard 2700-second timeout and every job uploads return codes, logs, exact input/profile hashes, and available outputs even on failure.

## Frozen response metric

For each tolerance, use the same `integrator_branch_diagnostic.response_profile` and stage-3 CMB excursion definitions:

`Emax(tol) = max(E_TT,E_EE,E_TE)` with frozen parent scale `Emax_parent_RK=534.8355868817356`.

Per tolerance classification is unchanged from stage-3:

- `REMOVES` iff TT, EE, TE excursion factors are all <= 3;
- `REDUCES` iff removal fails but `Emax <= Emax_parent_RK/3`;
- `INSUFFICIENT` otherwise;
- failed/nonfinite/invalid provenance -> `BLOCKED`.

`SUFFICIENT = REMOVES or REDUCES`.

Additionally report, without changing the verdict, per-case TT/EE/TE symmetric normalized differences relative to the tightest `1e-7` run and adjacent-ladder differences. These are diagnostic convergence curves only.

## Frozen directional classifications

After all seven lanes are terminal and unblocked:

1. `M21_THERMO_TOL_TIGHTENING_PRESERVES_REMOVAL` iff each of `3e-6,1e-6,3e-7,1e-7` is `REMOVES`.
2. Else `M21_THERMO_TOL_TIGHTENING_PRESERVES_SUFFICIENCY` iff each of those four tighter-than-reference values is `SUFFICIENT`.
3. Else `M21_THERMO_TOL_REFERENCE_VALUE_PATH_SPECIFIC` iff `1e-5` is `SUFFICIENT` but both `3e-7` and `1e-7` are `INSUFFICIENT`.
4. Else `M21_THERMO_TOL_NONMONOTONE_DIRECTIONAL_RESPONSE`.
5. Any mandatory blocked lane -> `M21_THERMO_TOL_DIRECTION_AUDIT_BLOCKED`.

The looser `3e-5` and `1e-4` values are mandatory context/negative-direction controls but do not define the tightening classification.

## Positive controls

- exact provider commit in every lane;
- identical physical INI hashes across all seven tolerance lanes;
- identical common baseline hashes;
- exactly one varied precision key, `tol_thermo_integration`;
- all required output products finite and uniquely identified.

## Negative controls / forbidden changes

No change to dark-matter fractions, masses, temperatures, cosmology, gauge, outputs, k/l ranges, ncdm precision, transfer precision, integrator identity (`evolver=0` stays frozen), thresholds, response metric, or provider source. No post-hoc tolerance insertion/deletion. No use of partial stage-3 values.

## Interpretation ceiling

This is a numerical-direction audit only. Even `TIGHTENING_PRESERVES_REMOVAL` does not prove global convergence or a CLASS bug and does not authorize production tuning. `REFERENCE_VALUE_PATH_SPECIFIC` or `NONMONOTONE` is a numerical diagnostic, not physical M21 falsification. No K1/K3/K4 promotion is authorized by this gate.
