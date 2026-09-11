# W04 M27 DDM dark-radiation high-L refinement preregistration v0.1

## Trigger
The frozen L={8,17,32} hierarchy-convergence batch completed 27/27 ensemble rays and 3/3 N=1 controls. N=1 controls passed, but only 20/27 ensemble rays passed the prospective L17->L32 threshold; aggregate classification is `M27_DDM_DR_HIERARCHY_CONVERGENCE_NOT_ESTABLISHED`. Maximum L17->L32 amplitude-normalized residual was 0.004003933161124123 > 1e-4. This is not physical falsification and does not authorize retuning the DDM physics.

## Question
Is the failure localized to provider-default `l_max_dr=17`, with the same hierarchy converging at higher truncation, or does material truncation sensitivity persist beyond L=32?

## Frozen physics and grid
Keep exactly the previous hierarchy gate physics and numerical support:
- delta={0.5,1,2}; y={1,2,3}; Gamma0/H*={0.03,0.3,3}; N=64;
- k/H*={0.1,1,10}; D04 support; same synchronous-comoving prescribed metric forcing;
- same exact ensemble background, tau reconstruction, flat hierarchy equations and cotK terminal closure;
- DOP853, rtol=1e-11, atol=1e-14.

No physical parameters, support threshold, forcing, background equations or solver tolerances may change after results are seen.

## Frozen refinement
For every one of the 27 ensemble rays, solve L={17,32,64}. Record L17->L32 for continuity with the parent gate and classify the new refinement only from L32->L64.

For each k and each of delta_dr, theta_dr, shear_dr, compute the same amplitude-normalized maximum residual used in the parent gate. Require residual <=1e-4 for every channel at every k and finite solutions.

A ray passes iff all L32->L64 residuals pass. Aggregate PASS requires all 27 rays.

## Classification
- all 27 pass: `M27_DDM_DR_HIGH_L_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE`;
- otherwise: `M27_DDM_DR_HIGH_L_HIERARCHY_CONVERGENCE_NOT_ESTABLISHED`;
- execution failure: `M27_DDM_DR_HIGH_L_HIERARCHY_NUMERICAL_BLOCKED`.

Even aggregate PASS does **not** erase the parent L17->L32 failure and does not promote K1/K3/K4. It would establish only that a higher truncation is numerically converged under the prescribed-metric source-level calculation and would justify a separately preregistered production profile using the converged hierarchy. Self-consistent Einstein-metric feedback, gauge robustness, full Boltzmann observables and likelihood remain open.

`K1_promoted=false`, `K3_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
