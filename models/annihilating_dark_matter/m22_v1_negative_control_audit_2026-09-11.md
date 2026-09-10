# M22 v1 negative-control audit — 2026-09-11

The frozen M22 K1-v1 gate is retained as `M22_K1_REFERENCE_LIMIT_NOT_ESTABLISHED` and is not relabelled after seeing the result.

## What passed
All solver cases executed. Explicit `DM_annihilation_efficiency=0` and the omitted-parameter reference are exactly identical in TT, EE, TE and P(k) (normalized L2 residual 0 in all four blocks).

TT, EE and TE all show finite, monotonic contraction toward zero across the preregistered p_ann ladder and pass their frozen tail-slope/contraction gates.

## Sole v1 failure
The v1 preregistration treated P(k) as a strict negative control and required `max R2 <= 1e-4`, based on the qualitative provider-example comment that P(k) is not affected by p_ann. The actual same-solver response is small but clearly finite:
- R2 = 9.4481e-3 at 1.11e-22;
- 4.0923e-3 at 3.33e-23;
- 1.7018e-3 at 1.11e-23;
- 5.8332e-4 at 3.33e-24;
- 2.0517e-4 at 1.11e-24.

The three-smallest-point log-log slope is approximately 0.9183, so this block is contracting toward the exact-zero reference rather than showing a non-decoupling floor.

## Interpretation
The provider's example statement is not a theorem that the matter spectrum is bitwise or sub-1e-4 invariant. A thermodynamic energy-injection modification can propagate through recombination/baryon evolution into a small matter-spectrum response even when P(k) is not the primary observable of the example.

Therefore v1 failure is classified as a preregistered negative-control assumption being too strong for K1. It is not a physical failure of annihilating DM and it does not authorize changing the v1 threshold post hoc.

## Authorized v2
A separate prospective K1-v2 may:
- preserve the exact omitted-vs-zero identity test;
- treat P(k) as a response channel whose only K1 requirement is continuous contraction to zero;
- extend the p_ann ladder to previously untested smaller values;
- require TT, EE, TE and P(k) all to pass continuity on that new tail.

No K3-K9 promotion follows from a K1-v2 pass.
