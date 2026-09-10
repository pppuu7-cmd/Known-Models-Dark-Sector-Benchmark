# W03 M13b SimpleMC author-slice crossing preregistration v0.1

Date: 2026-09-10
Target: M13b true two-field quintom / phantom-divide crossing
Purpose: determine whether the pinned SimpleMC `QuintomCosmology` actually realizes a robust `w=-1` crossing on parameter slices explicitly used by the author's own plotting code, without post-hoc parameter tuning.

## Frozen provider/runtime

- provider: `ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0`
- Python 3.8
- numpy 1.24.4
- scipy 1.10.1
- scikit-learn 1.1.3
- pandas 1.5.3
- matplotlib 3.7.5
- numdifftools 0.9.41

This historical runtime is an infrastructure compatibility choice only. It does not edit provider physics.

## Source identity

The provider defines two scalar degrees of freedom with quadratic/interacting potential

`V = 0.5 (mquin phi)^2 + 0.5 (mphan psi)^2 + beta (phi psi)^2`

and opposite-sign kinetic contributions in `rho`/`w`. Thus a genuine background phantom-divide crossing requires the kinetic difference to change sign, not merely a point numerically equal to `w=-1`.

The provider source explicitly comments `Still figuring out initial conditions for two fields.` Therefore even a successful crossing is only scoped provider evidence; it cannot by itself close M13b K3/K5.

## Frozen parameter slices

No free search or optimizer is allowed. Reproduce the author's own `simplemc/plots/plot_Quintom_DR12.py` uncoupled slices:

1. `Quintom_mquin`: `mphan=1.2`, `beta=0`, scan `mquin` using the author's `steps=9`, `min=0.1`, `max=2.5`, i.e. Python `np.arange(0.1,2.5,(2.5-0.1)/9)`.
2. `Quintom_mphan`: `mquin=1.2`, `beta=0`, scan `mphan` over the identical author grid.

The provider-declared parameter ranges in `paramDefs.py` are `mquin in [0,4]` and `mphan in [0,3]`; the author plotting slices lie inside them.

## Frozen evaluation domains

For every point:

- execute the provider's own `updateParams`/`call_functions` route;
- require finite solution, finite H and finite w;
- record provider `phi_ini` status;
- evaluate `w(a)` on the native 500-point `lna in [-10,0]` grid;
- separately evaluate the author plot domain `z in [0,3)` using the exact plot grid `np.arange(0,3,0.05)`.

## Frozen crossing definition

A point has a **robust strict crossing** on a domain only if both conditions occur on that same domain:

- `min(w+1) < -1e-6`, and
- `max(w+1) > +1e-6`.

The `1e-6` dead zone is fixed before execution to prevent an initial/rest point numerically equal to `w=-1` from being misclassified as a crossing. Also report raw sign-change counts with no dead zone for diagnostics, but they do not control classification.

Points with `phi_ini in {0,-1}` are not accepted as an executable two-field crossing representative: `0` is provider no-solution and `-1` is provider's LCDM-like fallback.

## Predeclared classification

- `M13B_SIMPLEMC_AUTHOR_SLICE_CROSSING_FOUND_WITH_SCOPE` if at least one author-slice point has a valid nonfallback solution and robust strict crossing in the author's `z<3` plot domain.
- `M13B_SIMPLEMC_CROSSING_ONLY_OUTSIDE_AUTHOR_PLOT_DOMAIN` if no valid point crosses at `z<3` but at least one valid point robustly crosses on the full native `lna` domain.
- `M13B_SIMPLEMC_AUTHOR_SLICES_NO_ROBUST_CROSSING` if no valid author-slice point robustly crosses even on the full native domain.
- `M13B_SIMPLEMC_AUTHOR_SLICE_SCAN_BLOCKED` if the historical provider cannot execute the frozen scan reproducibly.

A crossing-found result only establishes background representability with scope. It does not validate perturbation closure, initial-condition correctness, stability, K4 convergence, K5 multichannel response or observational discrimination.

No M13b family falsification is authorized by a no-crossing result from these limited author slices.