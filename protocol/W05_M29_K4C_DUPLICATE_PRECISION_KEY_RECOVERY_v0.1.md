# W05 M29 K4c duplicate-precision-key recovery v0.1

Status: prospectively frozen technical recovery before rerun.

## Trigger
Canonical K4c run 34635419961 completed its aggregate with classification `M29_K4C_DIAGNOSTIC_EXECUTION_OR_FINITE_OUTPUT_BLOCK`. The three projection-containing profiles (`projection_ref`, `thermo_projection_ref`, `full_core_ref`) exited 1 before scientific outputs because the harness concatenated `cl_permille.pre` with override fragments that repeated CLASS/hi_class precision parameter names. The parser is fail-closed on duplicate entries. Successful profiles `base_grid`, `thermo_ref`, and `full_ref` are valid immutable evidence and must not be recomputed.

## Frozen repair
For only the three failed profiles, construct the same intended merged precision profile but canonicalize duplicate parameter assignments before execution: when the same precision key appears more than once across `cl_permille.pre` and the preregistered override fragments, retain exactly the last assignment, preserving the intended override value from the existing K4c workflow. Comments/blank lines may be retained or discarded; no parameter value may otherwise change.

This is a parser/plumbing repair only. It does not change:
- hi_class pin `0009f51d89e6465c79e570b496c66fc90058fa77`;
- Brans-Dicke physics or `omega_BD=15`;
- `background_Nloga=40000`;
- any K4c grid, thermodynamics, projection, evolution, or full-reference precision value;
- observables, metrics, reduction rule, threshold, or classification logic;
- the canonical K4b/K4c scientific evidence.

## Rerun scope
Rerun only `projection_ref`, `thermo_projection_ref`, and `full_core_ref` with `fail-fast:false`. Reuse immutable successful artifacts from run 34635419961 for `base_grid`, `thermo_ref`, and `full_ref`. Aggregate only after all three recovered arms terminate.

## Fail-closed interpretation
- Any recovered-arm nonzero exit or nonfinite/missing TT result remains `M29_K4C_DIAGNOSTIC_EXECUTION_OR_FINITE_OUTPUT_BLOCK` and is not a physical failure.
- If all six profiles are executable/finite, apply the already-frozen K4c analyzer and thresholds without modification.
- Green CI is not scientific PASS. K4 promotion remains forbidden by this diagnostic itself unless the pre-existing frozen gate explicitly authorizes it.
- No physical falsification of Brans-Dicke or modified gravity can be inferred from this recovery.
