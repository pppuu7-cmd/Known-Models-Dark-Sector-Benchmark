# W07 M30/M31 local 2D response-Jacobian preregistration v0.1

Date: 2026-09-12
Models: M30 Horndeski / M31 beyond-Horndeski (effective hi_class propto_omega_bh representation)
Gate target: K2 parameter-geometry evidence only
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`

## Frozen motivation
The validated K1 ladders for M30 and M31 scale the active alpha coefficients jointly and therefore sample only one radial path. The pinned provider documents
`parameters_smg = c_K, c_B, c_M, c_T, c_H, M*^2_ini`.
The original M30 path keeps `c_T=c_H=0`; the original M31 path keeps `c_T=0` while `c_H=0.3 q`. A K2 geometry diagnostic therefore requires at least one prospectively frozen independent coordinate.

## Frozen base points
Use the same propto_omega_bh configuration, LCDM expansion and numerical settings as the pinned provider file.

- M30 base: `q=0.1`, `(c_K,c_B,c_M,c_T,c_H,M2_ini)=(0.1,0.05,0.02,0,0,1)`.
- M31 base: `q=0.1`, `(0.1,0.05,0.02,0,0.03,1)`.

No background-expansion retuning is authorized.

## Frozen finite differences
For each model compute five arms from the same base configuration:

1. `base`: q=0.100, c_T=0.
2. `rcoarse`: q=0.102, c_T=0.
3. `rfine`: q=0.101, c_T=0.
4. `tcoarse`: q=0.100, c_T=0.002.
5. `tfine`: q=0.100, c_T=0.001.

For M30 set c_H=0 for all arms. For M31 set c_H=0.3*q for radial arms and c_H=0.03 for c_T arms. M2_ini=1 always.

## Frozen response vector
Use the concatenation of:
- all common finite numerical CMB C_l columns after exact ell matching, normalized by the base CMB vector norm;
- common-support P(k), interpolating only inside overlap onto the base k grid, normalized by the base P(k) vector norm.

Finite-difference vectors are `(response_arm-response_base)/step`.

## Frozen acceptance diagnostics
For each direction compare coarse and fine derivatives by principal angle using `abs(cosine)` and relative norm mismatch.

A direction is converged iff:
- principal angle <= 5 degrees; and
- relative norm mismatch <= 0.25.

The two fine derivatives are response-separated iff their principal angle >= 10 degrees.

Classifications:
- `LOCAL_2D_RESPONSE_RANK_EVIDENCE`: both derivatives converge and fine directions are separated.
- `LOCAL_2D_RESPONSE_NEAR_COLLINEAR`: both converge but cross angle <10 degrees.
- `LOCAL_2D_RESPONSE_DERIVATIVE_NOT_CONVERGED`: at least one derivative fails convergence.
- `LOCAL_2D_RESPONSE_PROVIDER_BLOCKED`: base succeeds but one or more perturbation arms fail.
- `LOCAL_2D_RESPONSE_CONTROL_BLOCKED`: base/provider identity fails.

## Scope guard
This diagnostic is theory-response geometry in one pinned effective hi_class representation. It does **not** by itself promote K2, does not establish a complete covariant Horndeski/GLPV/DHOST quotient, does not establish observational distinguishability, and never authorizes physical family falsification. Any K2 promotion requires a separate synthesis against source/covariant parameter geometry and all representation boundaries.
