# W03 M13b K3D2-B mapping-certified tau implementation probe v0.1

Date: 2026-09-14

## Purpose

Test the minimal perturbation evolver start that is *provably right-owned by the exact CLASS background interpolation used by `perturbations_derivs()`*, without selecting a manual epsilon or changing any physical/numerical acceptance threshold.

Provider remains exactly:

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Frozen upstream facts

1. Native z=5 perturbation interval insertion/remap audit passed.
2. The exact handoff is `tau_handoff = 6256.998662974107` for the frozen qfield realization.
3. Mapping certificate passed with the minimal right-owned point at 12 local conformal-time ULP:
   - `tau_prev = 6256.998662974117` returns `a_prev = 0.16666666666666666`;
   - `tau_cert = 6256.998662974118` returns `a_cert = 0.16666666666666670`;
   - `a_handoff = exp(log(1/6)) = 0.16666666666666669`.
4. Direct NDF15 collapse geometry corrected the earlier A1 interpretation:
   - actual A1 `evolver_start = 6256.998662974108`, only one local tau ULP above the exact interval boundary and still below `tau_cert`;
   - all 80 high-k NDF15 failures are `error_control` failures at that start with zero successful steps;
   - the earlier first traced right-owned RHS at `6256.998662974136` was a later NDF15 initial-step derivative probe, not the evolver start.
5. B1/B2/B3 remain unevaluated; K3 ceiling remains PARTIAL; K4/K5 remain unpromoted.

## Authorized implementation

Replace only the lower bound supplied to the inserted post-handoff qfield perturbation `generic_evolver` interval.

When qcf or qpf is enabled and the interval starts at the exact z=5 handoff:

1. set `tau_candidate = tau_handoff`;
2. repeatedly apply `nextafter(tau_candidate,+infinity)` one representable conformal-time value at a time;
3. after each move, evaluate the same CLASS path used by the perturbation RHS: `background_at_tau(..., normal_info, inter_normal, ...)`;
4. stop at the first candidate for which returned `a > exp(log(1/6))`;
5. require the predecessor to return `a <= exp(log(1/6))`;
6. require the exact frozen provider/realization to find the point in exactly 12 ULP, as established prospectively by the mapping-certificate run;
7. pass this `tau_cert` as the second interval's numerical lower bound while keeping `perturbations_vector_init()` at the exact native interval boundary and keeping the state vector unchanged.

The search guard is 4096 representable tau steps. This is only a fail-closed implementation bound, not a physical/numerical epsilon; the preregistered expected result is exactly 12.

No smoothing, tolerance change, solver substitution, state kick, altered initial condition, modified equation, modified mass sign, changed output request, or changed precision file is authorized.

## Parallel lanes

Run independently on separate GitHub runners:

### S — source guard

Verify that the patch:

- is conditional on qcf/qpf;
- changes only `source/perturbations.c`;
- leaves vector initialization at the exact interval boundary;
- leaves state components unchanged;
- uses `background_at_tau` to certify the actual RHS ownership;
- requires predecessor-left/current-right ownership and exactly 12 ULP;
- changes no equation, tolerance, solver family, Einstein source, or Boltzmann hierarchy equation.

### N — strict disabled null

Build exact upstream CLASS and the fully recovered adapter containing the mapping-certified seam. Run identical qfield-disabled LambdaCDM controls. Require:

- both providers return zero;
- same finite positive P(k) grid;
- normalized L2 P(k) difference <= `1e-10`;
- identical H0 to <= `1e-12` relative.

### D — enabled default NDF15

Run the unchanged frozen enabled qcf+qpf `mPk,dTk` probe and require:

- provider rc=0;
- no minimum-step/underflow diagnostic;
- finite positive P(k);
- exactly two requested direct perturbation trajectories;
- finite qcf/qpf trajectory columns and dynamically nonzero qcf/qpf values.

### R — enabled `cl_ref.pre` RK

Apply the same requirements independently using the unchanged reference precision file.

## Classification

- S+N+D+R all pass -> `M13B_K3D2B_MAPPING_CERTIFIED_TAU_IMPLEMENTATION_PASS_WITH_SCOPE`.
- S/N pass but either enabled lane still fails -> `M13B_K3D2B_MAPPING_CERTIFIED_TAU_IMPLEMENTATION_NOT_ESTABLISHED` with solver-specific diagnostics preserved.
- Null failure -> implementation route is rejected regardless of enabled behavior.

A PASS only authorizes a new full frozen B1/B2/B3 regression using the same certified seam. It does **not** itself evaluate B1/B2/B3 or promote K3/K4/K5.

All outcomes preserve `physical_falsification=false`.