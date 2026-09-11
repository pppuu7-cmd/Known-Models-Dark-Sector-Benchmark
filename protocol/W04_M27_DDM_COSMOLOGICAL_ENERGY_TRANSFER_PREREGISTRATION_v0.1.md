# W04 M27 DDM cosmological energy-transfer solver preregistration v0.1

## Trigger

The nine-branch theory-level distributed-decay geometry benchmark passed for all `(delta,y)` rays and demonstrated non-degenerate lifetime distributions and non-single-exponential survival. The next layer tests the same ensemble inside an expanding cosmological background with explicit energy transfer from decaying pressureless DDM components into free-streaming/background dark radiation.

This remains a background/energy-conservation benchmark, not a perturbation or observational likelihood calculation.

## Frozen ensemble construction

Retain the M27 scaling family:

- `N=64`
- `m_0=1`
- `Delta_m=0.25`
- `m_n = 1 + 0.25 n^delta`
- `Gamma_n = Gamma_0 m_n^y`
- `gamma=-y`
- normalized initial parent weights `w_n propto m_n^gamma`.

Independent benchmark axes:

- `delta in {0.5,1,2}`
- `y in {1,2,3}`
- `Gamma_0/H_* in {0.03,0.3,3.0}`

The resulting 27 branches SHOULD run concurrently subject to runner availability.

## Frozen background normalization

Use dimensionless fiducial present-day critical-density units with `H_*=1` and initial scale factor `a_i=1e-5`.

Fiducial stable components:

- `Omega_b,* = 0.05`
- `Omega_r,* = 9e-5`
- `Omega_Lambda,* = 0.69`
- initial comoving DDM normalization corresponding to `Omega_DDM,* = 0.26` in the no-decay reference.

At scale factor `a`, surviving parent densities are evaluated exactly along the numerical cosmic-time trajectory:

`rho_n(a,t) = Omega_DDM,* w_n a^-3 exp(-Gamma_n t)`.

Define daughter-radiation comoving energy `D=a^4 rho_dr`. Integrate in `x=ln a`:

`dt/dx = 1/H`

`dD/dx = a^4/H sum_n Gamma_n rho_n`

with

`H^2 = Omega_r,* a^-4 + Omega_b,* a^-3 + Omega_Lambda,* + sum_n rho_n + D a^-4`.

Initial conditions at `a_i`: `t=0`, `D=0`.

Integrate to `a=1` with SciPy `solve_ivp`, DOP853, `rtol=1e-10`, `atol=1e-12`, and evaluate on 4001 log-spaced scale-factor points.

## Independent N=1 reference control

For the same `Gamma_0/H_*`, solve an independent direct single-species DCDM system for `[t,rho_parent,rho_dr]`:

`dt/dx=1/H`

`drho_parent/dx=-3 rho_parent-(Gamma_0/H)rho_parent`

`drho_dr/dx=-4 rho_dr+(Gamma_0/H)rho_parent`.

Compare this direct system against the exact-survival representation specialized to N=1. Require p95 symmetric relative residuals <=1e-7 in `H(a)`, `rho_parent(a)`, and `rho_dr(a)` over numerically supported points.

## Ensemble conservation/positivity gates

For every 64-component branch require:

1. integration success and finite values;
2. `H>0`, parent density >=0 and daughter-radiation density >=0;
3. surviving parent comoving density `a^3 sum rho_n` is non-increasing;
4. daughter comoving radiation `D=a^4 rho_dr` is non-decreasing;
5. initial D=0 and final D>0;
6. numerical quadrature of `a^4 source/H` over x agrees with integrated D at a=1 to relative 1e-4.

## Distributed-response comparator

Construct a unique moment-matched single-decay comparator with

`Gamma_eff,0 = sum_n w_n Gamma_n`

and the same initial total parent abundance. Record, but do not use as a post-hoc tuning parameter:

- p95 relative difference in H(a);
- maximum relative difference in surviving parent density;
- maximum relative difference in daughter-radiation density on supported points.

## Classification

Per branch: `M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_PASS_WITH_SCOPE` iff the N=1 reference and all ensemble conservation/positivity gates pass.

Aggregate: `M27_DDM_27_BRANCH_ENERGY_TRANSFER_PASS_WITH_SCOPE` iff all 27 branches pass.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`. Perturbation/source-closure and observation-space gates remain open.
