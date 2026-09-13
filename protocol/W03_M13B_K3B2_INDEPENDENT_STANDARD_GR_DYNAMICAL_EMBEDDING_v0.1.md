# W03 M13b K3B2 independent standard-GR two-field dynamical embedding v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Implementation provenance: **independent KMDSB standard-GR verification**  
Original Goh–Taylor provider reproduction: **NO / FORBIDDEN CLAIM**

## Trigger

K3A passed independent equation/sign/continuity closure. K3B0 and K3B1 then established that the literal printed Einstein trace and perturbed Klein–Gordon forms in the public article cannot be silently used as standard-GR numerical implementation authority. The unavailable author code therefore remains a separate provenance layer.

This gate tests whether the intended two-field mechanism itself admits a finite, self-consistent local Newtonian-gauge Einstein + canonical-field + phantom-field realization through an exact effective `w=-1` crossing when standard covariant GR equations are used.

This is not an observational fit, not a reproduction of published spectra, and not K4/K5.

## Frozen units and conventions

- `8 pi G = 1`.
- Flat FRW.
- Conformal Newtonian gauge with zero anisotropic stress and one metric potential `Phi`.
- Fourier convention `nabla^2 -> -k^2`.
- Expanding branch `Hc > 0`.
- Total potential is `V(phi)+V(psi)` with the same functional form for each field.

Potential:

`V(x) = V0 [tanh(s(1-x)) + 1]`

with exact derivatives

`V_x = -V0 s sech^2(s(1-x))`

`V_xx = -2 V0 s^2 sech^2(s(1-x)) tanh(s(1-x))`.

## Frozen background system

State variables are `a, phi, u=phi', psi, v=psi'`.

Energy density and pressure:

`rho = (u^2-v^2)/(2 a^2) + V(phi)+V(psi)`

`p   = (u^2-v^2)/(2 a^2) - V(phi)-V(psi)`.

Friedmann branch:

`Hc = a sqrt(rho/3)`.

Evolution:

- `a' = Hc a`;
- `phi' = u`;
- `u' = -2 Hc u - a^2 V_phi`;
- `psi' = v`;
- `v' = -2 Hc v + a^2 V_psi`.

For the independent trace diagnostic:

`Hc' = Hc^2 - (u^2-v^2)/2`.

The crossing coordinate is

`q = u^2-v^2 = a^2(rho+p)`.

## Frozen perturbation system

State variables are `delta_phi, delta_phi', delta_psi, delta_psi', Phi`.

Field stress-energy perturbations:

`delta_rho_phi = (u delta_phi' - u^2 Phi)/a^2 + V_phi delta_phi`

`delta_p_phi   = (u delta_phi' - u^2 Phi)/a^2 - V_phi delta_phi`

`delta_rho_psi = (-v delta_psi' + v^2 Phi)/a^2 + V_psi delta_psi`

`delta_p_psi   = (-v delta_psi' + v^2 Phi)/a^2 - V_psi delta_psi`.

Metric evolution uses the standard `0i` Einstein constraint as a first-order equation:

`Phi' + Hc Phi = (u delta_phi - v delta_psi)/2`.

Covariant field perturbation equations:

`delta_phi'' = -2 Hc delta_phi' - (k^2+a^2 V_phiphi)delta_phi + 4 u Phi' - 2 a^2 V_phi Phi`

`delta_psi'' = -2 Hc delta_psi' - (k^2-a^2 V_psipsi)delta_psi + 4 v Phi' + 2 a^2 V_psi Phi`.

## Independent Einstein residuals

Neither residual is used to evolve the state; both must remain small if the embedding is self-consistent.

### 00 constraint

`C00 = k^2 Phi + 3 Hc(Phi'+Hc Phi) + (a^2/2) delta_rho_total`.

### spatial-trace residual

Differentiate the frozen `0i` relation algebraically:

`Phi'' = -Hc' Phi - Hc Phi' + [u' delta_phi + u delta_phi' - v' delta_psi - v delta_psi']/2`.

Then

`Cij = Phi'' + 3 Hc Phi' + (2 Hc'+Hc^2)Phi - (a^2/2)delta_p_total`.

The normalization of each residual is the sum of absolute magnitudes of the terms entering that equation, floored at `1e-30`. No cancellation term may be omitted from the denominator.

## Prospectively frozen local crossing anchor

This is a dimensionless local consistency anchor, not a cosmological best fit:

- `tau0 = 0`;
- `a0 = 1`;
- `V0 = 1`;
- `s = 1`;
- `phi0 = 0.5`;
- `psi0 = 1.5`;
- `u0 = v0 = 0.1`;
- `k = 0.7`;
- `delta_phi0 = 1e-5`;
- `delta_psi0 = -5e-6`;
- `delta_phi_prime0 = 0`;
- `Phi0 = 2e-6`.

At the anchor `q0=0` exactly. `Phi_prime0` is not fitted; it is fixed by the `0i` constraint. `delta_psi_prime0` is not fitted; it is solved algebraically from `C00=0` after all preceding quantities are frozen.

No shooting, parameter scan, root search over physical parameters, or post-hoc anchor change is authorized.

The chosen symmetric field positions imply equal finite potential slopes and a nonzero prospectively predicted crossing derivative

`q'_0 = -2 u0 a0^2 [V_phi(phi0)+V_psi(psi0)]`.

The run must report this value and its sign before integrating.

## Frozen numerical method

Deterministic fixed-step classical RK4, no adaptive solver.

Integrate independently forward and backward from `tau0` over `T=0.05`.

Two resolutions:

- coarse: `N=500` steps per half-interval;
- fine: `N=1000` steps per half-interval.

The same exact anchor is reconstructed independently at each resolution. Floating-point type: IEEE-754 binary64.

## Frozen gates

All are mandatory.

1. **Anchor algebra**: `|q0| <= 1e-15`; algebraically solved initial `|C00| <= 1e-13` in absolute units.
2. **Transverse crossing prediction**: `q'_0 > 0` and finite.
3. **Executed crossing**: on the fine run, backward endpoint has `q<0` and forward endpoint has `q>0`; neither endpoint may be zero within `1e-12`.
4. **Finite realization**: every state and every derived `rho,Hc,delta_rho,delta_p,C00,Cij` is finite at every stored fine-grid point; `rho>0` and `Hc>0` throughout.
5. **00 constraint**: fine-run maximum normalized `|C00| <= 1e-7`.
6. **ij trace**: fine-run maximum normalized `|Cij| <= 1e-7`.
7. **Resolution stability of physical trajectory**: at both forward and backward endpoints, the fine-vs-coarse symmetric relative difference for each of `a,phi,u,psi,v,Phi,delta_phi,delta_psi` must be `<=1e-7`, with denominator `max(|x_f|,|x_c|,1e-12)`.
8. **Constraint refinement**: for each residual separately, either fine maximum normalized residual is `<=1e-10`, or it must be `<=0.5` times the coarse maximum normalized residual.
9. **Direct crossing variables**: no denominator in the evolution RHS may contain `q`, `rho+p`, `u^2-v^2`, or an effective-fluid `theta_DE` quantity. The executable must enforce this by construction and record the direct-variable manifest.
10. **No promotion leakage**: result must state `original_provider_reproduced=false`, `K4_promoted=false`, `K5_promoted=false`, `physical_falsification=false`.

## Frozen classifications

If all gates pass:

`M13B_K3B2_INDEPENDENT_STANDARD_GR_DYNAMICAL_EMBEDDING_PASS_WITH_SCOPE`

Interpretation: an independent same-realization local Einstein + canonical + phantom perturbation solution exists through an exact transverse effective-`w=-1` crossing, with preserved independent Einstein constraints in the stated local dimensionless scope. This advances K3 evidence but **does not** reproduce the unavailable author implementation and does **not** make K3 globally PASS.

If execution is finite but any constraint/crossing/refinement gate fails:

`M13B_K3B2_DYNAMICAL_EMBEDDING_NOT_ESTABLISHED`

If the frozen system cannot execute:

`M13B_K3B2_IMPLEMENTATION_BLOCKED`.

All outcomes retain canonical F13 K3 at `PARTIAL` at most. K4/K5 remain closed.

## Post-K3B2 authorization

A PASS authorizes a separate preregistration for a cosmology-scale Einstein–Boltzmann embedding/benchmark against response channels. It does not authorize observational claims, a family-wide stability claim, or reinterpretation of the Goh–Taylor code provenance.
