# W04 M27 DDM perturbation-source closure preregistration v0.1

## Motivation and scope

The 27-branch background energy-transfer grid has passed with the independently frozen D04 N=1 reference recovery. The next open layer is perturbation/source closure.

For pressureless decaying matter in the synchronous gauge comoving with the decaying species, the standard DCDM perturbation equation is `delta_dcdm' = -h'/2`, while the daughter-radiation continuity/Euler source terms are proportional to `a Gamma rho_dcdm / rho_dr`. For an adiabatic DDM ensemble whose cold parent components share the same comoving velocity/gauge, each fractional parent perturbation follows the same metric-forced equation; the ensemble decay perturbation source must therefore equal the component sum and reduce exactly to ordinary DCDM at N=1.

This preregistration tests that source structure and a low-order daughter fluid response. It is NOT a full free-streaming dark-radiation Boltzmann hierarchy and cannot by itself promote full K3 or K4.

## Frozen grid

Reuse the exact M27 background construction:

- N=64;
- delta in {0.5,1,2};
- y in {1,2,3};
- Gamma0/H* in {0.03,0.3,3};
- same mass spacing, abundance weights, cosmology and D04 support definition as the completed background campaign.

All 27 `(delta,y,Gamma0)` rays are independent jobs and shall run in parallel with `fail-fast:false`.

Within each job probe `k/H* = {0.1,1,10}`.

## Frozen metric forcing and fluid-source probe

On the D04 support use a deterministic small metric forcing

`h(x)=A_h [sin(2 pi u)+0.35 sin(5 pi u)]`, `x=ln a`, `u=(x-x_min)/(0-x_min)`.

Use amplitudes `A_h={1e-5,2e-5}` for a linearity check.

Parent perturbation is fixed by the synchronous-comoving pressureless relation `delta_p=-h/2`.

For the daughter source probe integrate the sigma=0 monopole/dipole fluid truncation

`d delta_dr/dx = -(4/3) theta/(a H) -(2/3) dh/dx + [Q/(H rho_dr)](delta_p-delta_dr)`

`d theta/dx = [k^2/(4 a H)] delta_dr - [Q/(H rho_dr)] theta`

with `Q=sum_i Gamma_i rho_i`. Initial conditions at the D04 support boundary are `delta_dr=delta_p`, `theta=0`.

The sigma=0 truncation is deliberately scoped as a source/continuity probe; a later hierarchy gate remains mandatory.

## Frozen gates

For every ray:

1. `component_source_identity`: component-wise `sum_i Gamma_i rho_i delta_i` vs `Q delta_p` amplitude-normalized maximum residual <= 1e-12.
2. `N1_reference`: compare the N=1 ensemble formulation with an independently integrated single-DCDM background/source formulation on their common D04 support. For each k, amplitude-normalized max residual <=1e-5 in both `delta_dr` and `theta`.
3. `linearity`: response at `A_h=2e-5` vs exactly twice the response at `A_h=1e-5`; amplitude-normalized max residual <=1e-7 for `delta_dr` and `theta` at every k.
4. all solutions finite.

A ray is `M27_DDM_PERTURBATION_SOURCE_CLOSURE_PASS_WITH_FLUID_SCOPE` iff all four gates pass. Provider/numerical failure remains blocked, never a physical falsification.

## Comparator measurement

For the N=64 ensemble, also run a moment-matched single-lifetime comparator with `Gamma_eff=sum w_i Gamma_i` and record normalized L2 residuals in `delta_dr` and `theta` for each k. This is descriptive response-geometry evidence only; no comparator threshold is used for pass/fail in this gate.

## Promotion policy

Even aggregate 27/27 pass means only a scoped perturbation-source/continuity closure result. Dark-radiation shear and higher multipoles, gauge robustness, numerical convergence, full observable response and likelihood remain open.

`K1_promoted=false`, `K3_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
