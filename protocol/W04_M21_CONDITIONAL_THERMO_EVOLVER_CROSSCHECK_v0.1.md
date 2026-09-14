# W04 M21 conditional thermodynamics-evolver crosscheck v0.1

Frozen: 2026-09-14 while the seven-point thermodynamics-tolerance direction audit is non-terminal and before any cross-evolver execution.

Status: **CONDITIONAL / NOT AUTHORIZED TO EXECUTE YET**.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Source motivation fixed prospectively

Exact source establishes two independent evolver controls. The M21 common precision baseline contains `evolver=0` for the generic/perturbation evolver, but thermodynamics uses the distinct `thermo_evolver`, whose exact default is `ndf15`. Current stage-3 and tolerance-direction lanes do not override `thermo_evolver`.

Exact `source/thermodynamics.c` passes `tol_thermo_integration` to whichever thermodynamics evolver is selected. Exact `tools/evolver_ndf15.c` consumes it as `rtol` in adaptive step/order/Newton/error control. RK also consumes the same tolerance argument through its own adaptive Cash–Karp error control, but it is not the current thermodynamics solver.

This gate is designed only as a successor if the NDF15 tolerance-direction result is path-specific or nonmonotone.

## Activation condition

Execution is authorized iff the terminal result of `W04 M21 conditional thermo-tolerance direction audit v0.1` has classification exactly one of:

- `M21_THERMO_TOL_REFERENCE_VALUE_PATH_SPECIFIC`;
- `M21_THERMO_TOL_NONMONOTONE_DIRECTIONAL_RESPONSE`.

It remains unexecuted if the parent is blocked or if tightening preserves removal/sufficiency. No alternative activation criterion may be chosen after the parent result.

## Frozen object

Same exact CLASS pin, same M21 `ref/f2/f3/f4` physical INIs, same `cl_permille.pre + m21_ncdm_tight.pre` numerical baseline, and same generic `evolver=0` setting used in the current M21 chain.

The only new dimension is the thermodynamics solver identity, `thermo_evolver`, evaluated at three prospectively frozen tolerances.

## Frozen 2 x 3 matrix

Mandatory six independent lanes:

NDF15:
- `NDF_T1E5`: `thermo_evolver=ndf15`, `tol_thermo_integration=1e-5`
- `NDF_T1E6`: `thermo_evolver=ndf15`, `tol_thermo_integration=1e-6`
- `NDF_T1E7`: `thermo_evolver=ndf15`, `tol_thermo_integration=1e-7`

RK:
- `RK_T1E5`: `thermo_evolver=rk`, `tol_thermo_integration=1e-5`
- `RK_T1E6`: `thermo_evolver=rk`, `tol_thermo_integration=1e-6`
- `RK_T1E7`: `thermo_evolver=rk`, `tol_thermo_integration=1e-7`

No tolerance may be inserted, removed, or changed after the parent outcome.

## Execution

Six independent jobs may run in parallel. Each executes immutable `ref/f2/f3/f4` sequentially, with hard timeout and branch-level artifact checkpointing. No lane may inspect another lane before execution.

## Frozen metrics

Use the unchanged M21 response profile and CMB excursion metric:

`Emax = max(E_TT,E_EE,E_TE)`.

Per lane: `REMOVES`, `REDUCES`, `INSUFFICIENT`, or `BLOCKED` under the same thresholds already frozen in stage-3/tolerance-direction work.

For each tolerance also report direct RK-vs-NDF15 TT/EE/TE normalized differences for `ref/f2/f3/f4`; these are diagnostics and do not introduce a new threshold.

## Frozen classification

If any lane is blocked -> `M21_THERMO_EVOLVER_CROSSCHECK_BLOCKED`.

Otherwise define the ordered class sequence at each solver over `1e-5 -> 1e-6 -> 1e-7` and report Emax values.

- If NDF15 is path-specific/nonmonotone while RK is sufficient at both `1e-6` and `1e-7` -> `M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED`.
- If both solvers are sufficient at both `1e-6` and `1e-7` -> `M21_THERMO_SOLVER_INDEPENDENT_TIGHT_LIMIT_SUPPORTED_WITH_SCOPE`.
- If both solvers remain insufficient at `1e-6` and `1e-7` -> `M21_THERMO_TOLERANCE_EFFECT_NOT_SUPPORTED_AT_TIGHT_LIMIT`.
- Otherwise -> `M21_THERMO_EVOLVER_DEPENDENCE_MIXED`.

These labels are numerical solver diagnostics only.

## Controls / forbidden changes

Exact provider pin and physical INI hashes must match across all six lanes. Only `thermo_evolver` and `tol_thermo_integration` may differ. Generic `evolver=0`, ncdm controls, transfer controls, cosmology, gauge, outputs, k/l ranges and all scientific thresholds stay fixed. No provider source patch or post-hoc solver rescue.

## Interpretation ceiling

This gate can distinguish solver-specific from cross-solver thermodynamics numerical sensitivity. It cannot establish a CLASS bug, global convergence, a production tuning recommendation, K1/K3/K4 status, or any physical property of mixed cold+warm dark matter.
