# M21 thermodynamics adaptive-path source audit — 2026-09-14

Provider authority: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Purpose: source-mechanism audit independent of the active RK/NDF15 cross-evolver result. This note does not change any frozen numerical lane, threshold or claim ceiling.

## Solver identity

M21 generic `evolver=0` does not select the thermodynamics solver. Exact CLASS has a distinct `thermo_evolver` precision field with default `ndf15`. `source/thermodynamics.c` selects `evolver_rk` or `evolver_ndf15` from that field and passes `tol_thermo_integration` as the tolerance argument.

## NDF15 adaptive surfaces controlled by rtol

Exact `tools/evolver_ndf15.c` is a variable-order (1--5), adaptive-step stiff solver. The thermodynamics tolerance enters several separate decision surfaces:

1. **Initial step selection.** The initial rate scale contains `1/sqrt(rtol)` and a second-derivative estimate contains `sqrt(.../rtol)`, so changing rtol can alter the first accepted step.
2. **Newton convergence.** Iterative acceptance uses explicit conditions `errit <= 0.05*rtol` and `errit <= 0.5*rtol`; failure can trigger a new Jacobian/linearization or a reduced step.
3. **Step acceptance/rejection.** A step fails when estimated error `err > rtol`.
4. **Step and method-order reselection.** Recovery and subsequent step-size/order proposals contain powers of `rtol/err`, `rtol/errkm1` and related error estimates. The solver may therefore cross discrete step/order/Jacobian histories as rtol changes.

These source facts make a nonmonotone output response under a tolerance sweep mechanically possible. They do **not** establish that the observed M21 CMB nonmonotonicity is caused by any particular branch switch, and they do not imply a CLASS defect. The preregistered RK/NDF15 cross-evolver experiment remains the numerical authority for solver specificity.

## Harness serialization boundary

Exact input parsing reads `thermo_evolver` with `parser_read_int`. Exact enum order is `rk=0`, `ndf15=1`. The first cross-evolver execution serialized symbolic labels and therefore stopped in the input parser before scientific calculation. The authorized recovery changes only that textual representation to the exact integer enum values.

## Claim ceiling

Source semantics only. No solver-quality ranking, convergence claim, production setting recommendation, K1/K3/K4 promotion, or physical mixed-dark-matter conclusion.
