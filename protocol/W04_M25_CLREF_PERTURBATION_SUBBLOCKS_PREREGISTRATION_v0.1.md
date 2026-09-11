# W04 M25 cl_ref perturbation sub-block diagnostics preregistration v0.1

## Trigger

M25 has now remained unresolved under: source-matched NCDM quadrature tolerances, `ncdm_fluid_approximation=3`, the provider `cl_permille.pre` transfer/projection profile, and (at least for m1 at preregistration time) an independent Newtonian-gauge branch. Background H continues to scale approximately linearly with eta while P(k)/CMB blocks do not.

Two deeper CLASS numerical sub-blocks from the provider `cl_ref.pre` are therefore frozen prospectively. They are independent diagnostics and SHOULD run in parallel for both sterile-neutrino PSD models.

## Common frozen inputs

- CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Immutable M25 PSD/cases from run `34548988620`, artifact `10180157389`.
- Tail cases: reference plus eta = 0.01, 0.003, 0.001.
- `tol_ncdm_bg=1e-6`, `tol_ncdm=1e-6`.
- `ncdm_fluid_approximation=3`.
- `_QUADRATURE_MAX_=4000`, `_QUADRATURE_MAX_BG_=4000` capacity-only repair.
- Synchronous gauge, so these tests are independent of the separate gauge diagnostic.
- No PSD, abundance, cosmology, eta, or acceptance-threshold changes.

## Frozen sub-block A: perturb_integrator

Add exactly the provider `cl_ref.pre` perturbation integrator settings:

- `evolver = 0`
- `tol_perturbations_integration = 1e-6`
- `perturbations_sampling_stepsize = 0.01`

## Frozen sub-block B: k_start_tca

Add exactly:

- `k_min_tau0 = 0.002`
- `k_max_tau0_over_l_max = 3`
- `k_step_sub = 0.015`
- `k_step_super = 0.0001`
- `k_step_super_reduction = 0.1`
- `start_small_k_at_tau_c_over_tau_h = 0.0004`
- `start_large_k_at_tau_h_over_tau_k = 0.05`
- `tight_coupling_trigger_tau_c_over_tau_h = 0.005`
- `tight_coupling_trigger_tau_c_over_tau_k = 0.008`
- `start_sources_at_tau_c_over_tau_h = 0.006`

## Execution

Matrix: `(m0,m1) x (perturb_integrator,k_start_tca)`. The four jobs are independent. Within each job, four CLASS cases have unique roots and MAY run two-at-a-time.

Apply the existing frozen tail-scaling judge to H, P(k), TT, EE and TE.

## Classification

- `M25_CLREF_SUBBLOCK_LOCALIZED` if H and all P(k)/TT/EE/TE blocks recover tail scaling.
- `M25_CLREF_SUBBLOCK_PARTIALLY_LOCALIZED` if at least one previously failing perturbation block recovers.
- `M25_CLREF_SUBBLOCK_INSENSITIVE` if none recover.
- `M25_CLREF_SUBBLOCK_PROVIDER_BLOCKED` on required execution failure.

No post-hoc combination or retuning is allowed before all four results are known. Diagnostic only: `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
