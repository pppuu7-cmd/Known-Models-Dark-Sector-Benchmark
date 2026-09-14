# M21 thermodynamics-tolerance evolver semantics — 2026-09-14

Provider authority: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540` (CLASS v3.3.4).

Purpose: outcome-independent source clarification while the prospectively frozen thermodynamics-tolerance direction audit is non-terminal. This note changes no numerical gate, threshold, tolerance ladder, physical case, or classifier.

## Important separation of evolver controls

The M21 precision baseline explicitly contains `evolver=0`. On the exact pin, `enum evolver_type { rk, ndf15 }`, so this value selects RK for the generic `evolver` control used elsewhere (notably perturbations).

Thermodynamics has a distinct precision field:

`thermo_evolver`, whose exact-pin default is `ndf15`.

Neither `cl_permille.pre` nor `verification/m21/m21_ncdm_tight.pre` nor the stage-3/tolerance profiles override `thermo_evolver`. Therefore all current M21 thermodynamics-tolerance lanes use the default **NDF15 thermodynamics evolver**, not RK.

Any earlier shorthand interpreting `tol_thermo_integration` as an RK thermodynamics tolerance is incorrect for this frozen M21 object. The numerical results themselves are unaffected because the executed profiles never changed `thermo_evolver`; only the verbal mechanism interpretation needed correction.

## Exact tolerance path

Exact `source/thermodynamics.c` selects the thermodynamics solver via `ppr->thermo_evolver` and passes `ppr->tol_thermo_integration` as the tolerance argument to the selected generic evolver at the thermodynamics integration calls.

With the default `thermo_evolver=ndf15`, the exact `tools/evolver_ndf15.c` receives this value as `rtol`.

The NDF15 implementation is explicitly a variable-order (1–5), adaptive-step stiff ODE solver. `rtol` controls its numerical trajectory in several direct ways, including:

- the initial-step estimates scale with `1/sqrt(rtol)`;
- Newton-iteration acceptance tests compare iteration errors with `0.05*rtol` and `0.5*rtol`;
- a step is rejected when the estimated integration error exceeds `rtol`;
- the recovered/next step size and possible order changes depend on powers of `rtol/error`.

Thus changing `tol_thermo_integration` changes the adaptive NDF15 step/order/linearization path of the thermodynamics ODE solve. Smaller values are stricter relative tolerances, but whether the M21 CMB-response anomaly converges monotonically under such tightening remains an empirical question for the already-frozen seven-point direction audit.

## Relation to current M21 gates

Stage-3 established that `tol_thermo_integration=1e-5` alone removes the localized f3 CMB excursion under the frozen benchmark. The exact default is `1e-6`, so the sufficient reference-profile value is looser by a factor of 10.

This source fact strengthens, rather than changes, the need for the prospective ladder `1e-4, 3e-5, 1e-5, 3e-6, 1e-6, 3e-7, 1e-7`: only that terminal numerical result can distinguish a broad tolerance-resolution effect from a path-specific/non-monotone NDF15 response.

## Interpretation ceiling

This note establishes solver identity and source-level tolerance semantics only. It does not predict the ladder outcome, establish convergence, identify a CLASS defect, authorize a production tolerance, promote M21 K1/K3/K4, or imply any physical property of mixed cold+warm dark matter.
