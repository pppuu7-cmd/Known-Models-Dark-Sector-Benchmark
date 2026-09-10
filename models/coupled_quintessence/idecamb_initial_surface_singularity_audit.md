# M14 IDECAMB coupled-quintessence initial-surface singularity audit

Updated: 2026-09-10
Status: `FIXED_AMIN_BETA_LIMIT_NONUNIFORM_CANDIDATE`
Scientific interpretation: **current upstream K4 angular failure is not yet a physical local-response result.**

## Evidence entering this audit

The source-scaled beta grid `{0,5e-8,1e-7}` gives a small tangent-norm mismatch but an approximately 8 degree angular failure. High-precision serialization leaves the angle unchanged. Replacing the pinned source's nonstandard Broyden inverse-Jacobian update with the standard rank-one good-Broyden formula also leaves the angle unchanged (`8.04154 deg` vs `8.04172 deg`), while all three shooting solutions terminate after one iteration with residual norm about `1.79e-7`.

Therefore the Broyden-update defect exists in source but is not causal for this particular local-grid failure.

## Relevant pinned source structure

Provider: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`.

For coupled quintessence with power-law potential and exponential coupling:

- the background integration starts at the hard-coded `amin = 1e-12`;
- the initial tracker field is

`phi_i proportional to a_i^(4/(2+alpha))`;

- the initial-condition formula contains `alpha`, the potential normalization, and radiation normalization, but **no beta coupling correction**;
- the scalar equation contains

`d(a^2 phi')/da proportional to [-a^2 dU/dphi + Q/phi']`,

and for the exponential coupling

`Q/phi' = beta * rho_c` in the source normalization.

Thus the coupling force becomes increasingly important towards the hard-coded initial surface even for small nonzero beta.

## Scaling of the crossover

Define the local crossover beta by equality of the magnitudes of the potential and coupling terms,

`beta_star(a) = a^2 |dU/dphi| / rho_c(a)`.

For the source tracker initial condition with `U proportional to phi^(-alpha)`, `phi proportional to a^(4/(2+alpha))`, and `rho_c(source) proportional to a^-1`, one obtains

`beta_star(a) proportional to a^[(2-alpha)/(2+alpha)]`.

At the frozen M14 anchor `alpha=0.02`,

`(2-alpha)/(2+alpha) = 0.9801980198...`.

The previous source-force audit measured

`beta_star(1e-4) = 7.813256771938583e-7`.

Scaling that same source tracker to the actual integration surface gives

`beta_star(1e-12) ~= 1.12525e-14`.

Hence the smallest executed nonzero beta,

`beta = 5e-8`,

is not below the crossover at the true start surface; it is approximately

`4.44e6 * beta_star(1e-12)`.

The previous `a=1e-4` source-scaled criterion therefore did not place the numerical trajectory in a uniformly weak-coupling regime over the full integration history.

For orientation, the same tracker scaling predicts approximately:

- `beta_star(1e-8) = 9.38e-11`  -> beta=5e-8 is ~533 times larger;
- `beta_star(1e-6) = 8.56e-9`   -> beta=5e-8 is ~5.84 times larger;
- `beta_star(1e-5) = 8.18e-8`   -> beta=5e-8 is ~0.61 times the crossover;
- `beta_star(1e-4) = 7.81e-7`   -> beta=5e-8 is ~0.064 times the crossover.

## Why this creates a nonuniform beta -> 0 limit

At every fixed scale factor `a>0`, the coupling force vanishes as beta -> 0. But the integration domain extends to a fixed extremely early `amin`, where `rho_c` is much larger. The weak-coupling condition required for the uncoupled tracker to be an asymptotically uniform initial approximation is therefore much stronger than the condition evaluated at the first exported diagnostic point (`a=1e-4`).

This means that finite differences around beta=0 can mix two effects:

1. the desired local response to the physical coupling parameter;
2. sensitivity to using an uncoupled tracker initial condition in a regime where the coupling term already dominates the scalar-force balance.

That is a classic singular/nonuniform perturbation risk. It can rotate a finite-difference response direction even while the response norm appears converged.

## M14 interpretation after this audit

Current status should be read as

`K4 = BLOCKED_BY_INITIAL_ASYMPTOTIC_UNIFORMITY_AUDIT`

not as physical failure of coupled quintessence differentiability.

The source Broyden defect remains documented separately, but the corrected-control run shows it is dormant for this beta grid because the root solve needs only one iteration.

## Next preregistered diagnostic direction

Do **not** continue shrinking beta blindly below `1e-14`, because CMB/output differences would approach numerical precision and could create a false convergence result.

Instead use a diagnostic start-surface ladder that deliberately straddles the predicted crossover for the already frozen beta grid, while keeping all physical equations and the response definition fixed. Suggested diagnostic surfaces are

`amin = {1e-8, 1e-6, 1e-5}`

with the upstream `1e-12` result retained as baseline.

The purpose is not to promote a late-start model as physical. The purpose is to test the causal prediction:

**if the ~8 degree rotation is produced by the nonuniform uncoupled initial asymptotic, the K4 direction should change sharply as amin crosses the region where beta/beta_star(amin) falls from >>1 to <=1.**

If this transition is observed, M14 needs a coupled asymptotic initial-condition derivation or an independent provider before scientific scoring. If no material start-surface dependence is observed, the next audit should target another source of response rotation (perturbation initialization / output operator / finite precision).

No observational claim and no family falsification are authorized by this audit.
