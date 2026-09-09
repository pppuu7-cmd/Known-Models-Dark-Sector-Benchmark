# M07 small-lambda response-order audit — preregistration

Date frozen: 2026-09-09  
Status: **FROZEN BEFORE SMALL-LAMBDA OUTPUTS**

## Motivation

The quotient-aware field-reflection audit established that the signed covering branches

`(+lambda,+phi) <-> (-lambda,-phi)`

are physically redundant in the frozen M07 pure-exponential model. The physical representative may therefore be taken as `lambda>=0`.

Existing production points suggested approximately `||r_Delta|| proportional to lambda^2`, but those values are not sufficient to freeze the local order after the fact. This audit uses new smaller lambda values that have not been inspected.

## Frozen branch and numerics

- solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`;
- `V=(1+A)exp(-lambda phi)`;
- `alpha=0`, `B=0`;
- `phi_ini=1`, `phi_prime_ini=0`;
- `Omega_scf_target=0.682686955086854`;
- `scf_tuning_index=2`;
- scale-aware `A_seed`;
- `tol_shooting_deltax_rel=1e-13`;
- frozen response block: 7 z x 5 low-k `r_Delta(k,z)` plus 7-node `lnH` diagnostic.

## New hold-in characterization points

These are **not B8 holdouts**. They are local-geometry calibration points:

`lambda = {0.005,0.010,0.020,0.040}`.

A lambda-zero scalar replacement and pure LambdaCDM reference remain mandatory controls.

## Hard numerical gates

1. all runs exit successfully;
2. every scalar case satisfies `abs(Omega_scf(today)-target)<=1e-6`;
3. lambda-zero reference satisfies existing production reference tolerances;
4. every nonzero low-k response norm exceeds `100 x` the lambda-zero scalar-reference response norm, so the order fit is not solver-floor dominated.

## Frozen order test

Let

`n(lambda)=||r_Delta(lambda)||_2`.

Fit

`ln n = a + p ln lambda`

by ordinary least squares over all four frozen nonzero points.

The **quadratic-order hypothesis passes** only if

`1.8 <= p <= 2.2`.

This range is frozen before the outputs and represents a +/-10% tolerance around the analytically expected leading even order `p=2` after field-reflection quotienting.

## Frozen convergence-direction test

Define

`q(lambda)=r_Delta(lambda)/lambda^2`.

For adjacent descending scales `(0.04,0.02)`, `(0.02,0.01)`, `(0.01,0.005)`, compute:
- angle between q-vectors;
- relative vector difference using the smaller-lambda q-vector as denominator.

The convergence test passes only if both diagnostics are non-increasing toward smaller lambda:

`angle(0.01,0.005) <= angle(0.02,0.01) <= angle(0.04,0.02)`

and

`reldiff(0.01,0.005) <= reldiff(0.02,0.01) <= reldiff(0.04,0.02)`.

No absolute post-hoc angle threshold is allowed.

## Interpretation rules

- If numerical gates fail: `BLOCKED_NUMERICAL`; do not infer response order.
- If numerical gates pass but fitted `p` fails `[1.8,2.2]`: reject the quadratic-order hypothesis in this scale range.
- If `p` passes but convergence monotonicity fails: report `INCONCLUSIVE` for the asymptotic coordinate; do not freeze `q=lambda^2` yet.
- Only if both order and convergence tests pass may W03 freeze `q=lambda^2` as the local M07 response coordinate in this scoped low-k theory-response block.
- This is local geometry, not observational identifiability and not B8 evidence.
