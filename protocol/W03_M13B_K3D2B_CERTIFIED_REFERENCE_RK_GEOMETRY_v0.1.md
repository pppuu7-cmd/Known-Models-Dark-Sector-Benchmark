# W03 M13b K3D2-B certified reference RK geometry v0.1

Date: 2026-09-14

## Purpose

Localize the residual `cl_ref.pre` explicit-RK numerical blocker after the mapping-certified 12-tau-ULP perturbation seam has already passed the source guard, strict disabled-null reduction, and default NDF15 enabled implementation gate.

Exact provider:

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Frozen upstream facts

- certified seam runtime certificate: 12 tau ULP;
- strict disabled null: P(k) normalized L2 `5.350776836980277e-16`, H0 relative difference `0`;
- certified default NDF15: provider rc=0 and enabled implementation gates PASS;
- certified `cl_ref.pre` RK: provider rc=1 with minimum-step failure in a later native interval reported as `[6257,6271]`;
- the earlier provisional-seam RK collapse band `[6256.998662974109,6256.998662974117]` was entirely before the mapping-certified right-owned point;
- B1/B2/B3 remain unevaluated by the certified full-Boltzmann scientific verifier.

## Authorized diagnostics

Apply the exact certified stack, then only diagnostic source transformations already source-guarded elsewhere:

1. enrich the existing RK minimum-step error string with current `x`, normalized next-step ratio, minimum variation, `hdid`, `hnext`, step index, and interval endpoints;
2. replace only the surrounding `class_call(generic_evolver(...))` error wrapper by a byte-argument-equivalent direct call that prints the failing worker identity and a flattened *copy* of the existing CLASS error buffer before returning `_FAILURE_`.

No solver choice, precision entry, tolerance, equation, state vector, initial condition, output request, approximation threshold, mass sign, or handoff coordinate may change.

## Parallel lanes

### S — source combination guard

Verify that the certified seam remains exactly 12 ULP and that the two diagnostic patches change only error reporting/wrapping, preserving the generic-evolver argument list and all numerical/physical choices.

### R — certified reference RK capture

Run the unchanged frozen enabled `cl_ref.pre` realization. Capture every worker that returns solver failure and, for each, record physical k and the enriched RK collapse geometry.

The run is expected to remain rc!=0 unless the diagnostic-only source changes unexpectedly alter behavior. If provider rc=0, classify the result as a provenance contradiction requiring a clean repetition; do not promote.

## Output questions

The diagnostic must determine:

- number and k-range of failing modes after the certified seam;
- whether K1 and K10 remain in the failing set;
- minimum/median/maximum collapse tau;
- minimum/median/maximum accepted `hdid` and proposed `hnext` where available;
- whether collapses remain concentrated near tau_cert or occur later throughout native intervals.

## Interpretation

- Later collapses after tau_cert indicate a residual explicit-RK stiffness/accuracy-control blocker distinct from the corrected seam ownership issue.
- A reduced failing set is evidence that the certified seam improves reference behavior but does not establish reference robustness unless every required mode completes.
- This protocol does not authorize tolerance relaxation, a solver substitution, or a new precision profile.

All outcomes preserve `physical_falsification=false`, `K3_state_ceiling=PARTIAL`, `K4_promoted=false`, `K5_promoted=false`.