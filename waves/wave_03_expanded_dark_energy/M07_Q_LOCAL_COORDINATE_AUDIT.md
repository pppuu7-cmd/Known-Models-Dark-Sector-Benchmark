# M07 q=lambda^2 local-coordinate audit

Date: 2026-09-09  
Actions run: `34359536106`  
Artifact: `w03-m07-perturbation-precision-q-audit`  
Artifact digest: `sha256:6cd91f54d94982425cbec2055c42f7e087458ae3a4e350796f9a661623240b5d`  
Status: **PASS_WITH_SCOPE**

## Question

After exact field-reflection quotient parity established that sign(lambda) is redundant, test whether the local response is well parameterized by

`q=lambda^2`

and whether the apparent low-lambda mismatch in the matter block was a perturbation numerical floor.

## Preregistered tight-tier gate

Same strict shooting as production (`tol_shooting_deltax_rel=1e-13`) plus:
- `tol_perturbations_integration=1e-8`;
- `perturbations_sampling_stepsize=0.01`.

For q-scaled low-k matter responses at lambda=.025 and .075:
- relative difference <= `0.05`;
- angle <= `2.0 deg`.

Thresholds were frozen before the tight run.

## Results

Baseline perturbation precision:
- q-scaled relative difference: `0.2184933`;
- angle: `12.5058 deg`;
- norms: `0.1105024`, `0.1166733`.

Tight perturbation precision:
- q-scaled relative difference: **`5.51889e-4`**;
- angle: **`0.0273111 deg`**;
- norms: **`0.11748477`, `0.11745212`**.

The hard gate passes by large margins.

Background H response independently shows the same local q behavior: lambda=.025 vs .075 q-scaled relative difference about `9.98e-4` and angle about `0.0294 deg`.

## Conclusion

Within the tested canonical M07 branch and frozen response grid:

1. quotient sign redundancy is exact under `(lambda,phi)->(-lambda,-phi)`;
2. `q=lambda^2` is the correct local invariant coordinate;
3. the earlier 12.5-degree low-lambda mismatch was a perturbation numerical-precision artifact, not physical q-nonlinearity;
4. the local q response can be represented by the average of the converged q-scaled lambda=.025 and .075 vectors.

Machine-readable frozen direction:
`M07_LOCAL_Q_DIRECTION.json`.

## Local q nearest-comparator geometry

Using the frozen local q direction on the same unwhitened 35-node low-k matter block:
- vs C1 smooth-w: acute angle `6.69445 deg`, best-scalar orthogonal residual fraction `0.11657`;
- vs C5 designer f(R): acute angle `60.72848 deg`, residual fraction `0.87231`.

Thus the properly quotient-reduced local M07 direction confirms the strong smooth-w near-degeneracy already seen in finite-lambda B6 while remaining far from the frozen f(R) comparator.

## Methodological consequence

A local tangent/Jacobian must be constructed in a quotient coordinate and only after numerical convergence of that coordinate's response has been demonstrated. Raw parameter derivatives can vanish or be numerically misleading when the physical response begins at second order in an unreduced parameter.

For M07, `dr/dlambda|_0=0` is not an absence of response; the meaningful local direction is `dr/dq|_{q=0}` with `q=lambda^2`.
