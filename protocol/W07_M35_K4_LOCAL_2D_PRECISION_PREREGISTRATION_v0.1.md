# W07 M35 / F35 Einstein-Aether / vector-tensor K4 — local 2D provider-precision preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT

## Purpose
Test numerical robustness on the same local response patch that supports M35 K2 PARTIAL. Existing K2 evidence distinguishes the gravity Lorentz-violation ray from the dark-matter Lorentz-violation coordinate `Y_dm`; K4 therefore tests both neighborhoods rather than only the K1 gravity ray.

## Provider
Exact pin: `Michalychforever/CLASS_LVDM@d9a20bd0c7b7a6c8957410fd245ed06b30b915c1` on provider branch `LVDM`. Base physical file: `Misha.ini`. The exact provider includes `cl_permille.pre` and `cl_ref.pre`.

## Frozen local physical patch
Use the same coordinate convention as the prior M35 local 2D Jacobian. Three points:
- `base`: q=0.100, Y_dm=0.000 -> alpha=0.005, beta=0.025, lambda=-0.010;
- `gravity`: q=0.102, Y_dm=0.000 -> alpha=0.0051, beta=0.0255, lambda=-0.0102;
- `Y`: q=0.100, Y_dm=0.002 -> alpha=0.005, beta=0.025, lambda=-0.010, Y_dm=0.002.
No physical retuning is authorized.

## Frozen numerical ladder
At each point run exactly:
1. default provider input;
2. input + `cl_permille.pre`;
3. input + `cl_ref.pre`.
Only numerical precision changes within a point.

## Mandatory blocks and metric
Mandatory TT, EE, TE and linear P(k). CMB uses exact common ell; P(k) uses common positive-k support with log-k interpolation. Missing/undefined blocks fail closed and are never zero-imputed. `R2=||x-y||_2/max(||y||_2,1e-300)`.
For each point/block:
- `R_coarse=R2(default,permille)`;
- `R_fine=R2(permille,reference)`.

## Frozen K4 gate
Reuse the existing KMDSB provider-precision standard:
- `R_fine <= 1e-4`, AND
- either `R_fine <= 0.5*R_coarse`, OR (`R_coarse <= 1e-8` and `R_fine <= 1e-8`).
A point passes only if all four blocks pass; local-2D K4 passes only if all three points pass.

## Classification
- all points/blocks pass -> `M35_K4_PASS_WITH_SCOPE_LOCAL_2D_PROVIDER_PRECISION_LADDER`;
- all required runs execute but any gate fails -> `M35_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED_LOCAL_2D`;
- provider/precision/output execution failure -> `M35_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED`.

A PASS is scoped to this pinned CLASS_LVDM scalar-cosmology local gravity×Y_dm patch. It does not establish full Einstein-Aether scalar/vector/tensor numerical closure. All outcomes retain `physical_falsification=false`; K3/K5-K9 are unaffected.
