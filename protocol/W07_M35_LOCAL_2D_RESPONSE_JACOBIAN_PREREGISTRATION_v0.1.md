# W07 M35 local 2D response-Jacobian audit — preregistration v0.1

## Purpose

Test whether the pinned CLASS_LVDM implementation exhibits two locally independent observable-response directions when the gravity Lorentz-violation ray and the dark-matter Lorentz-violation coordinate `Y_dm` are perturbed about the same executable base point.

This is a local response-rank/coverage diagnostic. It does **not** close the full K2 physical geometry or quotient, does not validate the full Einstein–Aether scalar/vector/tensor theory space, and cannot physically falsify the family.

## Immutable provider

- repository: `Michalychforever/CLASS_LVDM`
- branch: `LVDM`
- commit: `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`

## Frozen base point

Parameterize the already-tested gravity ray by `q`:

- `alpha = 0.05 q`
- `beta = 0.25 q`
- `lambda = -0.10 q`

Base point:

- `q0 = 0.1`, hence `(alpha,beta,lambda)=(0.005,0.025,-0.010)`
- `Y_dm = 0`

## Frozen finite-difference arms

Gravity direction, holding `Y_dm=0`:

- coarse: `q = 0.102` (`dq = 0.002`)
- fine: `q = 0.101` (`dq = 0.001`)

Dark-matter direction, holding `q=0.1`:

- coarse: `Y_dm = 0.002`
- fine: `Y_dm = 0.001`

No parameter values may be changed after seeing the outputs.

## Frozen observable response vectors

Use the finite common numerical support of:

1. all common numerical CMB `C_l` columns on matched multipoles;
2. matter `P(k)` interpolated only onto the base-point k grid inside common support.

For each block, form `(arm - base) / step`, and normalize the block by the L2 norm of the corresponding base observable. The combined response vector is the concatenation of the normalized CMB and P(k) derivative blocks.

## Frozen diagnostics

For each coordinate direction:

- derivative convergence angle between coarse and fine response vectors;
- relative derivative-norm mismatch between coarse and fine response vectors.

Between the two fine-step coordinate derivatives:

- absolute cosine and principal angle in degrees;
- `sin(angle)` as a dimensionless rank-separation diagnostic.

## Frozen decision labels

- `M35_LOCAL_2D_RESPONSE_RANK_EVIDENCE`: all five executions are finite; for both coordinate directions the coarse/fine derivative angle is <= 5 degrees and norm mismatch <= 0.25; and the fine gravity-vs-Y principal angle is >= 10 degrees.
- `M35_LOCAL_2D_RESPONSE_DERIVATIVE_NOT_CONVERGED`: executions are finite but either coordinate fails its convergence rule.
- `M35_LOCAL_2D_RESPONSE_NEAR_COLLINEAR`: both derivatives converge but their principal angle is < 10 degrees.
- `M35_LOCAL_2D_RESPONSE_PROVIDER_BLOCKED`: base succeeds but one or more perturbation arms fail.
- `M35_LOCAL_2D_RESPONSE_CONTROL_BLOCKED`: base fails.

Regardless of label:

- `K2_promoted = false`
- `physical_falsification = false`
- `full_Einstein_Aether_SVT_claim = false`

A positive rank-evidence result means only that the tested implementation has at least two locally distinguishable observable-response directions near this base point.