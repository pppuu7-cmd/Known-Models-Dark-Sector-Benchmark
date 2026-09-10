# M17 OHDE finite-background attack against CPL — preregistration

Date: 2026-09-10
Status: FROZEN BEFORE NUMERICAL RESULT

This gate is deliberately **background-only**.  It cannot close K3 perturbation closure, K5 multichannel rank, K7 observational whitening, or mechanism-level novelty.

## Physical model
Original flat noninteracting future-event-horizon HDE:

- `Omega_m0 = 0.30`;
- `Omega_de0 = 0.70`;
- constant HDE parameter points `c = {0.60, 0.80, 1.00, 1.20}`;
- evolution variable `x = ln a`;
- ODE

\[
\frac{d\Omega_{de}}{dx}=\Omega_{de}(1-\Omega_{de})\left(1+\frac{2\sqrt{\Omega_{de}}}{c}\right).
\]

For this scoped late-time background control radiation is omitted consistently from HDE, LambdaCDM and CPL comparators.  The HDE expansion rate is reconstructed from flat matter+HDE closure,

\[
E^2(a)=\frac{\Omega_{m0}a^{-3}}{1-\Omega_{de}(a)}.
\]

Reference for residual reporting is flat LambdaCDM with the same `Omega_m0` and `H0`; this is an external comparator, **not** a native HDE parameter limit.

Frozen redshift nodes are the standard seven DSIR late-time nodes:
`{0.295, 0.51, 0.706, 0.934, 1.317, 1.491, 2.33}`.

## Comparator
Full finite two-parameter CPL background manifold,

\[
w(a)=w_0+w_a(1-a),
\]

with the same `Omega_m0/H0`.  Fit bounds are frozen as

- `-2.0 <= w0 <= 0.0`;
- `-3.0 <= wa <= 3.0`.

The fit minimizes the unweighted L2 norm of the seven-component **residual difference**

`r_HDE - r_CPL`, where `r = ln(H/H_LCDM)`.

No family-specific rescaling after the CPL fit is allowed.

## Machine controls
- ODE integration tolerance: `rtol=1e-11`, `atol=1e-13`.
- Repeat each HDE point at `rtol=3e-12`, `atol=3e-14`.
- Numerical HDE convergence requires relative response-norm mismatch <= `1e-4` and direction angle <= `0.02 deg` whenever the response norm is nonzero.
- CPL optimizer must terminate successfully from at least three frozen starts: `(-1,0)`, `(-0.8,-0.5)`, `(-1.2,0.5)`; retain the best objective but record all starts.

## Classification thresholds
For each HDE point define

\[
R_H=\frac{\|r_{HDE}-r_{CPL,best}\|_2}{\|r_{HDE}\|_2}.
\]

- `R_H <= 0.10`: `BACKGROUND_ABSORBED_BY_CPL_WITH_SCOPE`;
- `R_H >= 0.30`: `BACKGROUND_SEPARATED_FROM_CPL_WITH_SCOPE`;
- otherwise: `BACKGROUND_INCONCLUSIVE`.

The family-level result is not promoted above background scope regardless of `R_H` because K3 is still open/provider-blocked.

## Anti-overclaim
A large background residual does not imply observational distinguishability or physical falsification of CPL. A small background residual does not establish equivalence of HDE and CPL perturbations.  No result from this gate changes the previously recorded fact that native OHDE has no LambdaCDM intersection in constant `c`.