# Wave 03 model-construction lessons v0.1

Updated: 2026-09-09  
Status: LIVING / evidence-fed from M07 canonical quintessence

This supplement records Wave-03 lessons that directly constrain construction of a future original dark-sector model. It supplements `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md` and does not replace the frozen B0-B9 protocol.

## W03-L1 — physical parameters and solver nuisance coordinates are different objects

M07 keeps `lambda` as the physical potential slope and uses `A` only as the `Omega_scf` shooting nuisance (`scf_tuning_index=2`). A solver is not allowed to repair convergence by moving the physical theory parameter unless a new scientific branch is explicitly opened.

## W03-L2 — natural-scale initialization is required for sensitive nuisance coordinates

For the alpha-zero exponential branch

`V=(1+A) exp(-lambda phi)`

and constant-field reference,

`V_target = 3 Omega_scf H0^2`,

so a scale-aware shooting seed is

`A_seed = 3 Omega_scf H0^2 exp(lambda phi_ini) - 1`.

Starting at the naive `A=0` placed the solver many orders of magnitude from the late-time scalar density scale and generated stiff integration failure. The scale-aware seed restored successful reference execution.

## W03-L3 — solver tolerance must be defined in a physically resolved coordinate

For M07 the raw nuisance is `A approximately -1`, while the physically relevant normalization is `N=1+A << 1`. CLASS default one-dimensional shooting tolerance in raw `A` allowed large relative error in `N` and produced apparent target-density drift.

At lambda=0.30 the default branch drifted by about `1.24e-3` in `Omega_scf`, while the strict rerun (`tol_shooting_deltax_rel=1e-13`) reduced the error to about `3.0e-10`. The default and strict 35-node matter-response vectors differed by roughly 38% in relative norm.

Therefore numerical-conditioning audits are part of physical response validation; solver defaults do not define the theory manifold.

## W03-L4 — microphysical novelty can collapse onto a phenomenological response direction

On the frozen 7x5 low-k `r_Delta(k,z)` block, strict M07 responses for lambda 0.075-0.30 lie only about `6.6-6.9 deg` from the C1 smooth-w direction. Exact collinearity is rejected, but the nearest phenomenological-DE degeneracy is strong. Against the frozen minimum-resolved designer-f(R) ray the acute separation remains about `61-62 deg` over the same larger-lambda range.

Construction implication: a new microphysical model does not earn mechanism-level novelty merely by having new fields or an action. It must generate at least one response channel that survives the nearest phenomenological comparator.

## W03-L5 — quotient exact coordinate redundancies before local-geometry inference

A fixed-coordinate parity audit tested `lambda -> -lambda` while keeping `phi_ini=+1`. It failed the preregistered low-k parity gate:
- abs(lambda)=0.025: odd/even `7.47e-3`;
- abs(lambda)=0.075: odd/even `2.03e-3`;
- frozen threshold: `1e-3`.

But for `B=0` the canonical exponential sector has the exact field-reflection map

`(lambda,phi) -> (-lambda,-phi)`.

Therefore fixed-chart parity is not identical to parity on the physical quotient manifold. The correct order is:

1. identify exact parameter/field redundancies;
2. quotient them;
3. define local coordinates;
4. only then infer derivative order, tangent/Jacobian rank or statements such as `q=lambda^2`.

The dedicated field-reflection quotient audit is preregistered separately. The failed fixed-coordinate threshold remains immutable evidence and must not be loosened post hoc.

## W03-L6 — reference success and comparator success are different gates

M07 has a very clean LambdaCDM intersection (`max|lnH|~1.1e-10`, `max|lnP|~2.2e-10` in strict dark-energy-dominant lambda-zero control), yet its finite response nearly aligns with smooth-w in the matter block. Therefore a clean reference limit is necessary but provides no guarantee of identifiable novelty.

## Design-prior mapping

These lessons feed DP-0801..DP-0807 in `matrices/design_prior_ledger.csv`.

Most important for the future original model:
- do not confuse theory and fitting coordinates;
- condition every sensitive nuisance at its natural scale;
- quotient exact redundancies before rank/local-coordinate claims;
- require an orthogonal observable channel when the nearest known phenomenological model is strongly aligned;
- keep theory-space geometry separate from observational identifiability.
