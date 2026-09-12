# W07 M30 / F30 Horndeski K4 — local 2D provider-precision preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT

## Purpose
Test numerical robustness of the already-established local M30 response geometry without changing physics or the K2 interpretation. The K2 synthesis is PARTIAL because the original K1 ladder was radial and a prospectively tested c_T direction supplied an independent local response direction. K4 therefore must cover both that radial neighborhood and the independent c_T neighborhood rather than only the original K1 ray.

## Provider
Exact pin: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
Base file: provider `gravity_models/propto_omega_bh.ini`.

## Frozen local physical patch
The six `parameters_smg` entries use the same coordinate map as the prior M30 K1/K2 workflows. Three independently executed physical points are frozen:
- `base`: q=0.100, c_T=0.000 -> `[0.100, 0.050, 0.020, 0.000, 0.000, 1.0]`;
- `radial`: q=0.102, c_T=0.000 -> `[0.102, 0.051, 0.0204, 0.000, 0.000, 1.0]`;
- `cT`: q=0.100, c_T=0.002 -> `[0.100, 0.050, 0.020, 0.002, 0.000, 1.0]`.
No physical parameter may be retuned after execution.

## Frozen numerical ladder
For each physical point run exactly:
1. `default`: provider input only;
2. `permille`: provider input + `cl_permille.pre`;
3. `reference`: provider input + `cl_ref.pre`.
Only the provider precision profile changes within a physical point.

## Mandatory observables and metric
Mandatory blocks: TT, EE, TE and linear P(k). CMB uses exact common ell support; P(k) uses common positive-k support with log-k interpolation. Undefined/missing blocks are fail-closed and never zero-imputed.
For arrays x,y use normalized L2 `R2=||x-y||_2/max(||y||_2,1e-300)`.
For each physical point/block define:
- `R_coarse = R2(default, permille)`;
- `R_fine = R2(permille, reference)`.

## Frozen K4 gate
Reuse the existing KMDSB provider-precision criterion already frozen for M23:
- `R_fine <= 1e-4`, AND
- either `R_fine <= 0.5*R_coarse`, OR (`R_coarse <= 1e-8` and `R_fine <= 1e-8`).
A physical point passes only if all four blocks pass. The local-2D K4 gate passes only if all three physical points pass.

## Classification
- all 3×4 gates pass -> `M30_K4_PASS_WITH_SCOPE_LOCAL_2D_PROVIDER_PRECISION_LADDER`;
- all runs execute but any gate fails -> `M30_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED_LOCAL_2D`;
- any required provider/profile execution or mandatory-output failure -> `M30_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED`.

A PASS promotes K4 only with the local M30 hi_class scope represented by these radial+c_T neighborhoods; it is not complete Horndeski-family numerical closure. Every outcome retains `physical_falsification=false` and has no bearing on K3/K5-K9.

## Parallelization/barrier
The three physical points may run in parallel (`fail-fast:false`). Their three precision profiles remain serial inside each job. Aggregate classification is forbidden until all three point artifacts cross the barrier.
