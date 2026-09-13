# W03 M13b K3C2 independent cosmology-scale perturbation bridge v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Scope: independent Newtonian-gauge scalar + metric + ideal matter/radiation perturbation bridge on the exact K3C1 background  
Full Boltzmann reproduction: **NO**  
Original Goh–Taylor provider reproduction: **NO**

## Trigger

K3C1 established a converged, independently critical-density-normalized FRW trajectory from `z=5` to today with a unique phantom-to-quintessence crossing and exact flat closure. The public author normalization/source map remains blocked by K3C0.

This gate asks a narrower but stronger question than K3C1:

> On exactly the K3C1 background, can the canonical and phantom field perturbations be coupled to a standard Newtonian-gauge metric plus pressureless matter and perfect radiation while preserving independent Einstein constraints through the cosmological crossing?

This is still not a full CLASS/Boltzmann implementation: baryons, photons and neutrinos are not split into their complete hierarchies, radiation anisotropic stress is set to zero, recombination is absent, and no transfer spectrum or observation operator is claimed.

## Frozen background authority

Read the canonical K3C1 result:

`waves/wave_03_expanded_dark_energy/M13B_K3C1_INDEPENDENT_BACKGROUND_CLOSURE_RESULT.json`.

The perturbation bridge MUST use exactly the canonical fine-lane amplitude `U0` from that result and the same equations/shape/start:

- `Omega_m0=0.3114`;
- `Omega_r0=9.23e-5`;
- `N_start=-ln 6` (`z=5`);
- `x=phi/M_P=0.92`, `p=dx/dN=0`;
- `y=psi/M_P=1.02`, `q=dy/dN=0`;
- `s_hat=29`;
- `U(x)=U0[tanh(s_hat(1-x))+1]`;
- no Lambda.

K3C2 may not re-solve, retune or modify `U0`.

## Frozen perturbation variables

Conformal Newtonian gauge with zero anisotropic stress:

`ds^2=a^2[(1+2 Phi)d tau^2-(1-2 Phi)dx^i dx_i]`.

Use `N=ln a` and evolve directly:

- scalar fields: `delta_x=delta_phi/M_P`, `r=d(delta_x)/dN`, `delta_y=delta_psi/M_P`, `t=d(delta_y)/dN`;
- metric: `Phi`, `W=dPhi/dN`;
- pressureless matter: density contrast `delta_m`, dimensionless velocity divergence `Theta_m=theta_m/Hc`;
- perfect radiation: `delta_r`, `Theta_r=theta_r/Hc`.

No effective dark-energy `theta_DE` is evolved.

## Frozen modes

Two dimensionless comoving modes are mandatory:

- `k_hat=1`;
- `k_hat=10`;

where `k_hat=k/H0` in `c=1` units. At each time define

`K2=(k/Hc)^2 = k_hat^2/(a^2 E^2)`.

These are mechanism-consistency probes, not an observational k-grid.

## Frozen background relations

With `D=p^2-q^2`:

`E^2=[Omega_m0 a^-3 + Omega_r0 a^-4 + U(x)+U(y)]/[1-D/6]`.

`dlnE/dN = -0.5[(3 Omega_m0 a^-3 +4 Omega_r0 a^-4)/E^2 + D]`.

The background field equations are exactly K3C1.

## Frozen scalar perturbation equations

Let `U_x=dU/dx`, `U_xx=d^2U/dx^2` and similarly for `y`.

Canonical field:

`delta_x_N = r`

`r_N = -(3+dlnE/dN)r -(K2+3 U_xx/E^2)delta_x +4 p W -6 U_x Phi/E^2`.

Phantom field:

`delta_y_N = t`

`t_N = -(3+dlnE/dN)t -(K2-3 U_yy/E^2)delta_y +4 q W +6 U_y Phi/E^2`.

These are the independent covariant standard-GR equations fixed by K3B1, not the literal printed author equations.

## Frozen fluid equations

Pressureless matter:

`delta_m_N = -Theta_m +3 W`

`Theta_m_N = -(2+dlnE/dN)Theta_m +K2 Phi`.

Perfect radiation with zero anisotropic stress:

`delta_r_N = -(4/3)Theta_r +4 W`

`Theta_r_N = -(1+dlnE/dN)Theta_r +K2(delta_r/4+Phi)`.

## Frozen pressure source and metric evolution

Normalize perturbations to `rho_crit,0`.

Canonical scalar pressure:

`dP_phi = E^2(p r-p^2 Phi)/3 - U_x delta_x`.

Phantom scalar pressure:

`dP_psi = -E^2(q t-q^2 Phi)/3 - U_y delta_y`.

Radiation pressure:

`dP_r = Omega_r0 a^-4 delta_r/3`.

The metric is evolved with the standard spatial-trace Einstein equation:

`Phi_N=W`

`W_N=-(4+dlnE/dN)W -(3+2 dlnE/dN)Phi +(3/(2E^2))(dP_phi+dP_psi+dP_r)`.

The `00` and `0i` Einstein equations are independent residuals and are not used after initialization.

## Frozen independent Einstein constraints

Scalar density perturbations normalized to `rho_crit,0`:

`dR_phi = E^2(p r-p^2 Phi)/3 + U_x delta_x`

`dR_psi = -E^2(q t-q^2 Phi)/3 + U_y delta_y`.

Total:

`dR = Omega_m0 a^-3 delta_m + Omega_r0 a^-4 delta_r + dR_phi+dR_psi`.

### 00 residual

`C00 = K2 Phi +3(W+Phi) +(3/(2E^2))dR`.

### 0i residual

`C0i = W+Phi -0.5(p delta_x-q delta_y) - [3/(2E^2 K2)] [Omega_m0 a^-3 Theta_m +(4/3)Omega_r0 a^-4 Theta_r]`.

For each residual, normalize by the sum of absolute magnitudes of all displayed terms, floored at `1e-30`.

## Prospectively frozen initial perturbation seed

At `z=5`, for each mode:

- `Phi_i=1e-5`;
- `W_i=0`;
- `delta_x=r=delta_y=t=0`.

Impose a constrained adiabatic ideal-fluid seed:

- `delta_r=(4/3)delta_m`;
- `Theta_r=Theta_m=Theta`.

`delta_m` is solved algebraically from `C00=0`; `Theta` is solved algebraically from `C0i=0`. No perturbation quantity is fitted or shot to a late-time target.

The exact formulas used by the executable must be written to the result manifest.

## Frozen numerics

Fixed-step classical RK4, IEEE-754 binary64.

For each `k_hat`, execute independently:

- coarse: `4000` steps from `z=5` to `z=0`;
- fine: `8000` steps.

No adaptive solver or threshold-dependent restart is allowed.

## Frozen gates

All mandatory for both modes unless explicitly stated.

1. **Canonical background identity**: the integrated fine background endpoint and crossing must reproduce the K3C1 fine result: each endpoint `x,p,y,q,E` symmetric-relative difference <=`2e-9`, and crossing-redshift absolute difference <=`2e-5`.
2. **Initial constraints**: absolute normalized `C00` and `C0i` at the constructed seed are each <=`1e-12`.
3. **Finite linear realization**: every evolved/derived quantity is finite; `E^2>0`, `1-D/6>0.5` throughout.
4. **Linear-amplitude domain**: maximum absolute value of every perturbation/metric/fluid state (`delta_x,r,delta_y,t,Phi,W,delta_m,Theta_m,delta_r,Theta_r`) is <`0.1` on the fine lane.
5. **00 preservation**: fine maximum normalized `|C00| <=1e-7`.
6. **0i preservation**: fine maximum normalized `|C0i| <=1e-7`.
7. **Constraint refinement**: separately for C00 and C0i, either fine maximum residual <=`1e-10` or it is <=`0.5` times the coarse maximum.
8. **Perturbation trajectory convergence**: at `z=0`, for all ten perturbation/metric/fluid state variables, coarse/fine symmetric-relative difference <=`1e-5`, denominator floored at `1e-12`.
9. **Scalar perturbations are dynamically sourced**: on each fine mode, at least one of `|delta_x|` or `|delta_y|` at `z=0` exceeds `1e-8`; a permanently zero dark-energy perturbation is not accepted as a successful coupling test.
10. **Crossing retained**: the background has exactly one resolved phantom-to-quintessence crossing and ends with `D>1e-4`.
11. **Direct-field crossing discipline**: no RHS denominator contains `D`, `rho_DE+p_DE`, or an effective `theta_DE`; only direct field variables are evolved.
12. **Scope guardrail**: result explicitly states `full_Boltzmann_hierarchy=false`, `author_model_reproduced=false`, `K3_state_ceiling=PARTIAL`, `K4_promoted=false`, `K5_promoted=false`, `physical_falsification=false`.

## Frozen classification

If both modes pass every gate:

`M13B_K3C2_INDEPENDENT_COSMOLOGY_PERTURBATION_BRIDGE_PASS_WITH_SCOPE`

Meaning: on the exact independently normalized K3C1 cosmological background, a standard-GR same-realization two-field + metric + ideal matter/radiation perturbation system remains finite and preserves independent Einstein constraints through the crossing for two distinct comoving modes.

This materially strengthens K3 but remains `PARTIAL`: it is not a photon/neutrino Boltzmann hierarchy, not a transfer-function prediction, not a source-level reproduction of the unavailable author solver, and not K4/K5.

If executions remain finite but any constraint/refinement/coupling gate fails:

`M13B_K3C2_COSMOLOGY_PERTURBATION_BRIDGE_NOT_ESTABLISHED`.

If the frozen system cannot execute or initialization constraints cannot be constructed:

`M13B_K3C2_IMPLEMENTATION_BLOCKED`.

## Next gate

A PASS authorizes a separately preregistered full independent Einstein–Boltzmann provider build/adapter search using the K3C1 normalization and K3C2 equations as regression controls. No observational or K4/K5 promotion is authorized directly by K3C2.
