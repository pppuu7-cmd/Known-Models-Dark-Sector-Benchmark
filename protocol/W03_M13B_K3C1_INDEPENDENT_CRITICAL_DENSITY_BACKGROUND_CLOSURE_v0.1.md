# W03 M13b K3C1 independent critical-density background closure v0.1

Date frozen: 2026-09-13  
Target: F13/M13b two-field quintom  
Scope: independently normalized cosmology-scale **background** bridge after K3C0 unit-binding blocker  
Author-model reproduction: **NO**

## Purpose

K3C0 proves that the public reduced-Planck numerical labels cannot be inserted literally into an ordinary physical cosmology with the simultaneously quoted H0/Omega values. Public-source reconnaissance found no authoritative code normalization map.

This gate therefore constructs a fully independent dimensionless FRW benchmark. Its normalization is not obtained by multiplying the published `V0` by the diagnostic K3C0 scale. Instead, the potential amplitude is determined by one explicit cosmological boundary condition: a flat no-Lambda model must satisfy `H(a=1)=H0` after evolving from a frozen-field state at `z=5`.

The benchmark tests whether the public tanh **shape mechanism**, when given a transparent critical-density normalization, admits a finite phantom-to-quintessence background crossing on a cosmological interval. It is not a fit and makes no claim to reproduce Goh–Taylor tables, chains, figures or hidden CLASS variables.

## Frozen variables and normalization

Use `N=ln a` and define

- `x = phi/M_P`;
- `y = psi/M_P`;
- `p = dx/dN`;
- `q = dy/dN`;
- `E = H/H0`;
- `U = V/rho_crit,0`, where `rho_crit,0=3 M_P^2 H0^2`.

No separate cosmological constant is present.

Frozen reference densities:

- `Omega_m0 = 0.3114`;
- `Omega_r0 = 9.23e-5`.

These define only the independent benchmark background.

## Frozen potential shape

Use the public 2025 tanh shape in dimensionless field coordinates:

`U(x)=U0 [tanh(s_hat(1-x))+1]`

with `s_hat=29`.

Derivative:

`U_x = -U0 s_hat sech^2[s_hat(1-x)]`.

The shape seed at the start of the independent benchmark is

- `z_start=5`, hence `N_start=-ln 6`;
- `x_start=0.92`;
- `y_start=1.02`;
- `p_start=q_start=0`.

The field positions and shape parameter are used only as a public mechanism-shape seed. The exact `p=q=0` start is the independent implementation of the published qualitative statement that the fields remain frozen until approximately `z>5`; it is not claimed to reproduce the authors' hidden numerical state at `z=5`.

## Frozen FRW equations

Let `D=p^2-q^2` and

`B(N)=Omega_m0 exp(-3N)+Omega_r0 exp(-4N)`.

The algebraic Friedmann relation is

`E^2 = [B + U(x)+U(y)] / [1-D/6]`.

Raychaudhuri in the same variables is

`dlnE/dN = -0.5 * [(3 Omega_m0 exp(-3N)+4 Omega_r0 exp(-4N))/E^2 + D]`.

Field evolution is

- `x_N = p`;
- `p_N = -(3+dlnE/dN)p - 3 U_x/E^2`;
- `y_N = q`;
- `q_N = -(3+dlnE/dN)q + 3 U_y/E^2`.

The effective dark-energy crossing coordinate is `D=p^2-q^2`; `D<0` is phantom dominated and `D>0` is quintessence dominated.

## Frozen amplitude boundary condition

`U0` is not imported from the public `V0` label.

At each numerical resolution, determine `U0` independently by bisection so that the evolved model satisfies

`E(N=0)=1`.

Prospectively frozen bracket:

`U0 in [1e-4, 2]`.

The bracket itself must straddle the target: `E0(U_low)<1<E0(U_high)`. If it does not, the gate is blocked/fails exactly as frozen; the bracket may not be changed post hoc.

Bisection uses at most 64 iterations and stops only when either `|E0-1|<=1e-11` or the bracket width is <=`1e-12`.

This is a boundary/closure solve, not an observational likelihood fit. No other parameter is varied.

## Frozen numerics

Deterministic fixed-step classical RK4, IEEE-754 binary64.

Two independent resolution lanes:

- coarse: `4000` steps from `N_start` to `0`;
- fine: `8000` steps.

Each lane solves its own `U0` from the same frozen bracket and boundary condition.

## Frozen gates

All are mandatory.

1. **Bracket**: both coarse and fine lanes satisfy `E0(U_low)<1<E0(U_high)` with finite endpoints.
2. **Closure root**: both lanes find positive finite `U0` within the frozen bracket and `|E0-1|<=1e-10`.
3. **Flat scalar closure**: at the final point, the scalar contribution `Omega_DE = E^2 D/6 + U(x)+U(y)` satisfies `|Omega_DE-(1-Omega_m0-Omega_r0)|<=2e-10`.
4. **Finite physical background**: throughout both lanes `E^2>0`, `1-D/6>0.5`, and all state/derived values are finite.
5. **Phantom phase develops**: after the exactly frozen start, fine-lane `D` reaches below `-1e-6` before the crossing.
6. **True later crossing**: exactly one resolved transition from `D<-1e-6` to `D>+1e-6` occurs on the fine lane for `0<z<5`.
7. **Quintessence phase survives**: fine-lane final `D>1e-4`.
8. **Amplitude convergence**: coarse/fine symmetric relative difference in solved `U0` is <=`1e-6`.
9. **Crossing convergence**: coarse/fine crossing redshifts differ by <=`1e-3`.
10. **Endpoint convergence**: coarse/fine symmetric relative difference at `N=0` for each of `x,p,y,q,E` is <=`1e-6`, using denominator `max(|fine|,|coarse|,1e-12)`.
11. **No public-amplitude reassignment**: report the implied `V0/M_P^4 = (rho_crit,0/M_P^4) U0` and its ratio to the public `0.91e-8` label, but explicitly set `author_normalization_map_claimed=false` and `published_V0_reproduced=false`.
12. **No promotion leakage**: `K3` remains at most `PARTIAL`; `K4_promoted=false`; `K5_promoted=false`; `physical_falsification=false`.

## Frozen classifications

If all gates pass:

`M13B_K3C1_INDEPENDENT_CRITICAL_DENSITY_BACKGROUND_CLOSURE_PASS_WITH_SCOPE`

Meaning: the tanh two-field mechanism admits a numerically converged, flat-FRW, independently normalized background trajectory from a frozen `z=5` state to today, with a resolved phantom-to-quintessence crossing. This supplies a transparent cosmology-scale normalization bridge for a later independent perturbation test.

It does **not** resolve the K3C0 author-unit blocker and does **not** reproduce the published model parameters.

If the model is finite but any frozen closure/crossing/convergence gate fails:

`M13B_K3C1_INDEPENDENT_BACKGROUND_CLOSURE_NOT_ESTABLISHED`.

If the frozen bracket does not straddle the boundary or execution becomes nonfinite:

`M13B_K3C1_INDEPENDENT_BACKGROUND_IMPLEMENTATION_BLOCKED`.

## Next gate

Only a PASS authorizes preregistration of an independent cosmology-scale perturbation bridge (`K3C2`) on this exact internally normalized background. K3C2 must carry K3C0's prohibition against calling the construction an author-code/Table reproduction.
