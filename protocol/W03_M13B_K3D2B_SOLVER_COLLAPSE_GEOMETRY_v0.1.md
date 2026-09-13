# W03 M13b K3D2-B solver-collapse geometry v0.1

Date: 2026-09-14

## Purpose

Resolve the numerical mechanism behind the solver-dependent K3D2-B perturbation failure sets without modifying any numerical decision or physical equation.

Frozen upstream evidence:

- exact provider `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`;
- remap/source audit PASS;
- minimal right-owned perturbation point = 12 local tau ULP;
- previous A1 first RHS is already right-owned;
- default NDF15: exactly 36 low-k post-handoff modes pass and exactly 80 contiguous high-k modes fail, with frontier between `k=0.014267228152127612` and `k=0.01796125219837715` 1/Mpc;
- reference RK: all 133 internal k modes fail;
- frozen K1/K10 fail in RK but not in default NDF15;
- direct comparison classification: `M13B_K3D2B_SOLVER_DEPENDENT_FAILING_SET`;
- B1/B2/B3 remain unevaluated.

## Diagnostic-only source changes

Only enrich existing failure strings. Do not change conditions, branches, steps, tolerances, Jacobians, state vectors, equations, provider pin, output request, or precision files.

### NDF15

At each of the two existing `absh <= hmin` exits record:

- failure reason: `newton` or `error_control`;
- current conformal time `t`;
- `absh`, `hmin`;
- current BDF order;
- successful/failed step counts;
- function/Jacobian/LU/linear-solve counters;
- for error-control failure, `err` and `rtol`.

### Reference RK

At the existing `fabs(hnext/x1) <= hmin` exit record:

- current conformal time `x`;
- normalized next-step ratio;
- minimum variation;
- accepted `hdid` and proposed `hnext`;
- step index;
- interval endpoints.

The direct worker tracer must print a flattened *copy* of the complete error chain, leaving the original CLASS error buffer unchanged.

## Parallel lanes

Run three independent jobs:

1. source-only guard of the diagnostic patches;
2. default NDF15 full unchanged A1 lane;
3. `cl_ref.pre` reference RK full unchanged A1 lane.

After both compute lanes complete, an analysis-only job summarizes collapse-time and mechanism distributions.

## Interpretation

- NDF15 failures dominated by `newton` identify nonlinear/Jacobian stiffness; failures dominated by `error_control` identify truncation/error-control stiffness.
- A narrow common collapse-time band across high-k NDF15 modes would localize a later physical/numerical transition; collapse immediately at the handoff would instead implicate the seam/IVP.
- RK collapse times distributed over the interval versus concentrated near the seam distinguish global explicit-solver stiffness from a localized discontinuity.
- No outcome authorizes tolerance changes, solver substitution, smoothing, B1/B2/B3 evaluation, or K3/K4/K5 promotion.

All outcomes preserve `physical_falsification=false`, `K3_state_ceiling=PARTIAL`, `K4_promoted=false`, and `K5_promoted=false`.