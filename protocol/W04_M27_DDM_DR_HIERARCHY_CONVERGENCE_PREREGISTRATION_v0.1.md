# W04 M27 DDM dark-radiation hierarchy convergence preregistration v0.1

## Trigger and scope

The 27-way normalized sigma=0 perturbation-source layer passes with independent solver verification. The remaining mandatory source-level physics is free-streaming daughter radiation shear and higher multipoles.

Pinned CLASS DCDM->DR evolves the comoving daughter brightness moments `F_l`: F0 and F1 receive the decay source/metric terms; F2 contains shear, l>=3 follows the collisionless hierarchy, and the final multipole uses the standard cotK closure. The pinned provider default is `l_max_dr=17` and requires at least l=4.

This gate reproduces those flat-space hierarchy equations for the DDM ensemble under the same prospectively prescribed synchronous-comoving metric forcing used in the source-closure campaign. It tests hierarchy truncation convergence and N=1 reduction. It is not yet a self-consistent Einstein-Boltzmann observable calculation because the metric is prescribed rather than solved from the perturbed stress-energy.

## Frozen background/grid

All 27 ensemble rays run independently:

- delta={0.5,1,2};
- y={1,2,3};
- Gamma0/H*={0.03,0.3,3};
- N=64;
- k/H*={0.1,1,10};
- support starts at D04, i.e. daughter comoving energy D > 1e-4 of final D;
- normalized metric forcing `hhat=sin(2 pi u)+0.35 sin(5 pi u)`;
- synchronous-comoving parent: delta_p=-hhat/2, theta_p=0;
- flat K=0; prescribed metric_euler=metric_shear=0; metric_continuity=h'/2.

The conformal time used in the CLASS closure is reconstructed from the accepted background via `d tau/d ln a = 1/(a H)`, with the radiation-era initial approximation `tau(a_i)=a_i/sqrt(Omega_r)` at a_i=1e-5.

## Frozen hierarchy

With f=D=a^4 rho_dr (irrelevant constant normalization suppressed) and `fprime_tau=a^5 Q`, integrate the pinned CLASS flat hierarchy transformed to x=ln a:

- F0_x = `-k F1/(aH) - (2/3) hhat_x f + D_x delta_p`;
- F1_x = `k(F0-2F2)/(3aH)`;
- F2_x = `2 k F1/(5aH) - 3 k F3/(5aH)`;
- for 3<=l<L: `F_l,x = k[l F_{l-1}-(l+1)F_{l+1}]/[(2l+1)aH]`;
- at L: `F_L,x = k F_{L-1}/(aH) - (L+1)F_L/(aH tau)`.

Initial F_l=0 at D04 (the prescribed forcing also has hhat=0 there). Recover observables `delta_dr=F0/f`, `theta_dr=3kF1/(4f)`, `shear_dr=F2/(2f)`.

## Frozen truncations and solver

For every ensemble ray and k solve L={8,17,32} with DOP853 rtol=1e-11, atol=1e-14.

Compare provider-default L=17 with L=32 using amplitude-normalized maximum residual over the complete D04 support. Frozen hierarchy-convergence threshold: <=1e-4 separately for delta_dr, theta_dr, and shear_dr at every k. L=8 vs17 is recorded descriptively as a coarse-truncation diagnostic.

## N=1 provider-form controls

Three independent control jobs, Gamma0/H*={0.03,0.3,3}, compare the N=1 ensemble background/hierarchy against the independently integrated direct single-DCDM background using L=17 and all three k. Require amplitude-normalized maximum residual <=1e-4 in delta_dr, theta_dr, shear_dr.

## Classification

An ensemble ray is `M27_DDM_DR_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE` iff all L17-vs-L32 residuals pass and all solutions are finite.

Aggregate 27/27 plus all three N=1 controls gives `M27_DDM_27_BRANCH_DR_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE`.

Even aggregate pass does not promote K3 or K4: self-consistent metric feedback, gauge robustness, full Boltzmann observable mapping and likelihood remain open. Provider/numerical failures are not physical falsification.

`K1_promoted=false`, `K3_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
