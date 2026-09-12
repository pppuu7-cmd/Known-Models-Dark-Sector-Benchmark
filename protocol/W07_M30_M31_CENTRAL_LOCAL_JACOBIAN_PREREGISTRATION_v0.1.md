# W07 M30/M31 central-difference local Jacobian preregistration v0.1

Date: 2026-09-12
Models: M30 effective Horndeski and M31 effective beyond-Horndeski in pinned hi_class
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`
Purpose: localization after the prospectively frozen forward-difference audit classified both models `LOCAL_2D_RESPONSE_DERIVATIVE_NOT_CONVERGED`.

## Prior evidence retained
The failed forward-difference result is not erased:
- M30: radial coarse/fine angle 66.2443 deg, mismatch 0.59705; c_T direction converged.
- M31: radial angle 67.1273 deg; c_T angle 20.3601 deg; both failed frozen convergence rule.

This follow-up changes the finite-difference stencil, not the prior thresholds or scientific classification.

## Frozen base coordinates
Use provider file `gravity_models/propto_omega_bh.ini` unchanged except `parameters_smg` and output root.

- M30 base: q=0.100, `(c_K,c_B,c_M,c_T,c_H,M2_ini)=(q,0.5q,0.2q,0,0,1)`.
- M31 base: q=0.100, `(q,0.5q,0.2q,0,0.3q,1)`.

## Frozen symmetric arms
For each model execute:
- base;
- radial q = 0.100 ± 0.002;
- radial q = 0.100 ± 0.001;
- c_T = ±0.002 at q=0.100;
- c_T = ±0.001 at q=0.100.

For M31 radial arms keep c_H=0.3q. c_T arms keep c_H=0.03. No expansion-model, background-density, stability-check, or precision retuning is authorized.

Central derivatives:
`J_h = [R(+h)-R(-h)]/(2h)`.
Compare h=0.002 to h=0.001 separately for radial and c_T.

## Frozen common response space
Construct one finite support common to all nine arms:
- exact common ell rows and numerical C_l columns;
- P(k) on the base k grid restricted to the global overlap of all arms.
Normalize CMB and P(k) blocks by base-vector norms exactly as in the forward audit.

## Frozen decision rule
A derivative is converged iff:
- principal angle between coarse and fine central derivatives <= 5 deg, and
- relative norm mismatch <= 0.25.

If both derivatives converge, fine radial and c_T derivatives are response-separated iff principal angle >=10 deg.

Classifications:
- `*_CENTRAL_LOCAL_2D_RESPONSE_RANK_EVIDENCE`: both converge and are separated.
- `*_CENTRAL_LOCAL_2D_RESPONSE_NEAR_COLLINEAR`: both converge but cross angle <10 deg.
- `*_CENTRAL_LOCAL_DERIVATIVE_NOT_CONVERGED`: either derivative fails.
- `*_CENTRAL_LOCAL_PROVIDER_BLOCKED`: base succeeds but at least one symmetric arm does not execute.
- `*_CENTRAL_LOCAL_CONTROL_BLOCKED`: base or provider identity fails.

## Scope
This is a numerical/local theory-response diagnostic in one pinned effective representation. No K2 promotion is authorized by this workflow alone. A successful central result may support a later immutable synthesis to K2 PARTIAL only; full covariant Horndeski/GLPV/DHOST geometry and quotient closure remain open. No physical family falsification is authorized by any outcome.
