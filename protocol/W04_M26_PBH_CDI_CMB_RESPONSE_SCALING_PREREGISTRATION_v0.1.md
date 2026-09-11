# W04 M26 PBH CDI CMB/PK response-scaling preregistration v0.1

## Purpose

Extend the validated M26 PBH Poisson/CDI transfer geometry from the high-k matter plateau to independent linear observables `TT`, `EE`, `TE`, and `P(k)` using the same pinned CLASS primordial CDI representation.

This is a solver/response-geometry gate. It is not an observational likelihood constraint and cannot by itself promote K4.

## Frozen mapping and provider

- CLASS: `lesgourg/class_public` at `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Poisson entropy power: `P_S = f_PBH M_PBH / rho_dm`.
- CLASS CDI amplitude: `f_cdi = sqrt(P_S k_pivot^3 / (2 pi^2 A_s))`.
- `n_cdi = 4`, `alpha_cdi = 0`, `c_ad_cdi = 0`.
- Exact/null PBH-CDI state is represented by omission of the CDI mode, as established by the provider-null recovery; an enabled zero-amplitude CDI mode is not used.

Cosmology is frozen to the preceding CDI transfer gate: `h=0.675`, `omega_b=0.0222`, `omega_cdm=0.12`, `N_ur=3.046`, `A_s=2.1e-9`, `n_s=0.965`, `k_pivot=0.05 1/Mpc`, `tau_reio=0.054`, flat geometry, linear spectra.

## Frozen grid

Independent mass branches SHOULD run concurrently:

- 100 Msun
- 1000 Msun
- 10000 Msun

Each branch contains one adiabatic reference and four finite PBH fractions:

`f = [1, 0.1, 0.01, 0.001]`.

Cases within a mass branch have independent output roots and MAY run two-at-a-time.

## Outputs

Request `tCl,pCl,mPk` with `l_max_scalars=2500`, `P_k_max_h/Mpc=100`, `z_pk=0`, no nonlinear correction and no lensing.

For each finite case compute response norms relative to the adiabatic reference:

- `R_TT = ||Delta C_l^TT||_2 / ||C_l,ref^TT||_2` over the common l support, excluding l<2;
- likewise `R_EE` and `R_TE`;
- `R_Pk = ||Delta P(k)||_2 / ||P_ref(k)||_2` on the common k support.

## Frozen gates

For every mass and every block TT/EE/TE/Pk:

1. all finite response norms must be finite and strictly positive;
2. log-log response-norm slope versus PBH fraction must be within `0.05` of 1;
3. monotonicity: each tenfold reduction in fraction must reduce the response norm.

Across masses, for each fixed fraction and each block, the log-log response-norm slope versus PBH mass must be within `0.05` of 1.

Per mass: `M26_PBH_CDI_CMB_RESPONSE_SCALING_PASS_WITH_SCOPE` iff all four block fraction gates pass.

Aggregate: `M26_PBH_CDI_MULTI_OBSERVABLE_MASS_FRACTION_SCALING_PASS_WITH_SCOPE` iff all mass branches and all cross-mass gates pass.

Provider execution failure is not physical falsification. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`; observation-likelihood validation remains open.
