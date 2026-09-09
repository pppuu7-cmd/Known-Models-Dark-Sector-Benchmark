# W03 / M10 — CLASS_EDE axion-like scalar-field Early Dark Energy preregistration v0.1

Frozen: 2026-09-10

## Scientific authority and implementation
- DSIR methodology overlay: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@bc28acc47cc5facba046741fd09f710ae8da9689`.
- EDE implementation: `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.
- M10 is a new implementation/model branch. It is **not** a repair or continuation of blocked M09 native `class_public` EDE.

CLASS_EDE explicitly evolves the scalar-field background and perturbed Klein-Gordon equation with adiabatic scalar-field perturbation initial conditions. Its EDE potential is axion-like,

`V_EDE(phi) ∝ m^2 f^2 [1-cos(phi/f)]^n`,

with effective shooting targets `fEDE` and `log10z_c`.

## Frozen physical branch
The first M10 branch fixes:
- `n_scf = 3`;
- `thetai_scf = 2.6`;
- `log10z_c = 3.5`;
- `CC_scf = 1`;
- `attractor_ic_scf = no`;
- EDE closure: `Omega_Lambda=0`, `Omega_fld=0`, `Omega_scf=-1` so the scalar branch/tuning closes the budget;
- shooting targets `fEDE` and `log10z_c` are used together, as required by this implementation.

Physical deformation coordinate:
`f = fEDE > 0` at fixed target `log10z_c=3.5`.

No negative-fEDE point is allowed.

## Frozen reference
Reference is pure LambdaCDM run in the **same CLASS_EDE commit**, with no scalar-field/EDE parameters activated and Lambda inferred by closure.

This same-solver reference is required before comparison with any KMDSB model computed in another CLASS fork.

## Stage A grid
Frozen first grid:
`fEDE = {0.005, 0.01, 0.03, 0.05}`.

- `0.005` and `0.01` are the local one-sided convergence pair.
- `0.03` and `0.05` are finite-deformation stress points only.
- None is B8 evidence.

## Shooting verification
For every finite case, independently reconstruct achieved EDE peak fraction and peak redshift from the written background table:

`rho_EDE = [phi'^2/(2a^2) + V_e_scf]/3`,

`f_EDE(a)=rho_EDE/rho_crit`.

The achieved peak is the maximum of this table-level fraction. The achieved `z_c` is the redshift at the maximum (with optional local quadratic interpolation if numerically well-conditioned).

Frozen shooting gates:
- `|fEDE_achieved - fEDE_target| <= max(1e-4, 0.01*fEDE_target)`;
- `|log10(zc_achieved) - 3.5| <= 0.015`.

Failure is `BLOCKED_NUMERICAL_SHOOTING` or `PARTIAL`, never physical falsification.

## Frozen response blocks
### L — late-time standard block
- `ln H(z)` on z `{0.295,0.51,0.706,0.934,1.317,1.491,2.33}`;
- `ln P(k,z)` on the same z nodes and k `{0.001,0.003,0.01,0.03,0.1} h/Mpc`.

### S — broad-k amplitude-quotiented shape block
At `z=0.51`, use
`k={0.001,0.003,0.006,0.01,0.02,0.03,0.05,0.08,0.1,0.2,0.3,0.5,0.8,1.0} h/Mpc`.

Define
`r(k)=ln[P_EDE(k)/P_LCDM(k)]`,

`s(k)=r(k)-mean[r(0.001),r(0.003)]`.

S removes a common very-low-k amplitude and retains scale-dependent transfer/shape response. It is theory-response geometry only.

## Stage A convergence gates
For the two smallest points compare `r/fEDE` in P, H and S.
A non-negligible block passes locally if:
- relative L2 difference <= 0.10;
- acute angle <= 3 deg.

The relaxed gate relative to M08 is preregistered because fEDE is obtained through a nonlinear two-target shooting map and the physical scalar field undergoes transition dynamics.

Near-zero directions are explicitly `NEAR_NULL`.

## Stage B preregistered question
Stage B may begin only if Stage A has a valid reference, successful shooting and at least one stable response block.

The primary comparator is the **full 2D local CPL manifold**, implemented in the same CLASS_EDE solver/reference and evaluated on exactly the same L and S grids.

Question:
> Can a common CPL `(epsilon0,wa)` fit absorb the M10 local EDE direction simultaneously in late-time L and broad-k S, or does an amplitude-quotiented scale-dependent residual survive?

No separation from one constant-w ray is sufficient.

## Initial B0-B9
- B0 `PASS_WITH_SCOPE`
- B1 `OPEN` — same-solver Lambda reference control pending
- B2 `PARTIAL` — published scalar perturbation implementation pinned; gauge/representation promotion still separate
- B3 `OPEN` — shooting and local convergence pending
- B4 `OPEN` — L/S responses pending
- B5 `OPEN`
- B6 `OPEN` — full CPL manifold is preregistered comparator
- B7 `OPEN`
- B8 `OPEN`
- B9 `PARTIAL`

## Anti-overclaim
- M10 is the pinned CLASS_EDE axion-like scalar branch, not all EDE models.
- Successful shooting is implementation validation, not observational support.
- A broad-k S residual is not an observable detection until a common observation operator/covariance is bound.
- M09 remains an independent upstream-implementation block and must not be overwritten by M10 results.
