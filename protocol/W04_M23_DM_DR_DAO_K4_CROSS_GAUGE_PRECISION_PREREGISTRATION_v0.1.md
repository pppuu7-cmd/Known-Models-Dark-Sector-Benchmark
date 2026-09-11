# W04 M23 DM-dark-radiation / DAO K4 cross-gauge + precision preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT
Date: 2026-09-11
Family: F23 / M23 NADM-like DM-dark-radiation scattering

## Purpose
Test numerical robustness (K4) and close the numerical part of the K3 cross-gauge check without changing M23 physics. This gate does not test K5-K9 and cannot by itself establish observational discrimination.

## Provider
Exact solver pin: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

The physical configuration and interaction coordinate are inherited unchanged from `protocol/W04_M23_DM_DR_DAO_K1_REFERENCE_PREREGISTRATION_v0.1.md` and its validated result `waves/wave_04_dark_matter/M23_K1_REFERENCE_RESULT.json`.

## Frozen physics
Common cosmology and species content are unchanged from M23 K1:
- h = 0.675
- omega_b = 0.0222
- omega_cdm = 0.1197 before conversion by f_idm=1
- A_s = 2.196e-9
- n_s = 0.9655
- tau_reio = 0.06
- N_ur = 3.046
- f_idm = 1
- N_idr = 0.4290
- nindex_idm_dr = 0
- idr_nature = fluid
- b_idr = 0
- output = tCl,pCl,mPk
- lensing = no
- non linear = none
- P_k_max_h/Mpc = 20
- z_pk = 0
- l_max_scalars = 2500

No physical parameter may be retuned after seeing this result.

## Frozen cases
Seven K1 cases are reused exactly:
- `ref`: Gamma key omitted, while nindex and idr_nature stay explicit;
- `zero`: Gamma_0_nadm = 0;
- `g0`: 2.371e-8 Mpc^-1;
- `g1`: 7.113e-9 Mpc^-1;
- `g2`: 2.371e-9 Mpc^-1;
- `g3`: 7.113e-10 Mpc^-1;
- `g4`: 2.371e-10 Mpc^-1.

Each case is run independently in `synchronous` and `newtonian` gauge. Raw gauge-dependent perturbation variables are NOT compared across gauges.

## Frozen precision ladder
For every case and gauge, run the same physical input with exactly three provider-defined numerical profiles:
1. `default`: no external `.pre` precision file;
2. `permille`: provider `cl_permille.pre`;
3. `reference`: provider `cl_ref.pre`.

Only numerical precision changes across this ladder. If `cl_ref.pre` is not executable for an otherwise executable case, classify the affected branch as numerical/provider blocked; do not substitute a post-hoc precision file in this gate.

## Common observables and metrics
Mandatory blocks: TT, TE, EE and linear P(k,z=0).

- CMB is compared only on exact common ell support.
- P(k) is compared only on common positive-k support with log-k interpolation.
- Undefined or absent blocks are masked and cause that mandatory branch to be NOT ESTABLISHED; they are never zero-imputed.
- For arrays x and y use normalized L2 residual `R2 = ||x-y||_2 / max(||y||_2,1e-300)`.

For each case+gauge+block define:
- `R_coarse = R2(default, permille)`;
- `R_fine = R2(permille, reference)`.

For each case+block define the cross-gauge residual at the reference precision:
- `R_gauge = R2(synchronous_reference, newtonian_reference)`.

## Frozen K4 gate
A case+gauge+block passes precision convergence only if all runs execute and:
- `R_fine <= 1e-4`, AND
- either `R_fine <= 0.5 * R_coarse` OR `R_coarse <= 1e-8` and `R_fine <= 1e-8`.

K4 may be promoted only if every mandatory block passes for all 7 cases in both gauges.

The 1e-4 observable-level normalized-L2 ceiling is frozen prospectively as a conservative KMDSB numerical-robustness requirement; it is not an observational likelihood threshold.

## Frozen cross-gauge gate
The numerical cross-gauge part of K3 passes only if every mandatory block for all 7 cases has:
- `R_gauge <= 1e-4` at provider reference precision.

This compares gauge-invariant/common observables only. It does not claim equality of gauge-dependent perturbation coordinates.

## Fail-closed classification
- If all precision gates pass: `M23_K4_PASS_WITH_SCOPE_PROVIDER_PRECISION_LADDER_BOTH_GAUGES`.
- Otherwise: `M23_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED`.
- If all cross-gauge observable gates pass: `M23_K3_CROSS_GAUGE_NUMERICAL_PASS_WITH_COMMON_OBSERVABLE_SCOPE`.
- Otherwise: `M23_K3_CROSS_GAUGE_NUMERICAL_NOT_ESTABLISHED`.
- Build/configuration/profile execution failure: `M23_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED` for the affected branch.

All outcomes retain `physical_falsification=false`. No failure here is a physical falsification of interacting-DM / dark-radiation models.

## Parallelization and barrier
The 14 independent case×gauge branches may run in parallel with `fail-fast:false`. Each branch runs its three precision levels serially to keep build/input identity local. Aggregate classification is forbidden until all 14 branch artifacts reach the explicit barrier.
