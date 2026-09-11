# W04 M24 cl_ref precision-block isolation preregistration v0.1

## Trigger

The recovered full `cl_ref.pre` diagnostic at CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540` changes the M24 middle-point excursion from `Emax ~ 62.645` to `Emax ~ 0.841` while preserving the exact a_idm_dr=0 identity. The earlier `cl_permille.pre` diagnostic was insensitive. Therefore the anomaly is numerical/approximation-sensitive, but the responsible `cl_ref` sub-block is not yet identified.

## Frozen physical cases

Use exactly the M24 cases already used by the full precision diagnostic:

- omitted interaction reference;
- exact a_idm_dr=0 null;
- a_idm_dr = 18000, 6000, 1800 Mpc^-1.

All cosmology and ETHOS-like physical parameters remain unchanged.

## Common compatibility control

CLASS rejects simultaneous UR and IDR approximation switches at the same threshold. To keep every comparison executable without confounding block attribution, both the control and tested branch set only:

`idr_streaming_trigger_tau_over_tau_k = 49`

No other control-side precision option is changed.

## Prospectively frozen cl_ref blocks

Six independent precision blocks are tested one-at-a-time and SHOULD run concurrently:

1. `thermo`
   - recfast_Nz0=100000
   - tol_thermo_integration=1e-5
   - recfast_x_He0_trigger_delta=0.01
   - recfast_x_H0_trigger_delta=0.01

2. `perturb_integrator`
   - evolver=0
   - tol_perturbations_integration=1e-6
   - perturbations_sampling_stepsize=0.01

3. `k_start_tca`
   - k_min_tau0=0.002
   - k_max_tau0_over_l_max=3
   - k_step_sub=0.015
   - k_step_super=0.0001
   - k_step_super_reduction=0.1
   - start_small_k_at_tau_c_over_tau_h=0.0004
   - start_large_k_at_tau_h_over_tau_k=0.05
   - tight_coupling_trigger_tau_c_over_tau_h=0.005
   - tight_coupling_trigger_tau_c_over_tau_k=0.008
   - start_sources_at_tau_c_over_tau_h=0.006

4. `hierarchy_streaming`
   - l_max_g=50
   - l_max_pol_g=25
   - l_max_ur=50
   - radiation_streaming_approximation=2
   - radiation_streaming_trigger_tau_over_tau_k=240
   - radiation_streaming_trigger_tau_c_over_tau=100
   - ur_fluid_approximation=2
   - ur_fluid_trigger_tau_over_tau_k=50

5. `sampling_projection`
   - l_logstep=1.026
   - l_linstep=25
   - hyper_sampling_flat=12
   - hyper_sampling_curved_low_nu=10
   - hyper_sampling_curved_high_nu=10
   - hyper_nu_sampling_step=10
   - hyper_phi_min_abs=1e-10
   - hyper_x_tol=1e-4
   - hyper_flat_approximation_nu=1e6
   - q_linstep=0.20
   - q_logstep_spline=20
   - q_logstep_trapzd=0.5
   - q_numstep_transition=250

6. `transfer_lensing`
   - all cl_ref transfer_neglect_delta_k_* values = 100
   - neglect_CMB_sources_below_visibility=1e-30
   - transfer_neglect_late_source=3000
   - l_switch_limber=40
   - accurate_lensing=1
   - num_mu_minus_lmax=1000
   - delta_l_max=1000

NCDM-specific cl_ref settings are excluded because M24 has no NCDM component. Tensor-only hierarchy settings and halofit precision are excluded because this diagnostic uses scalar linear observables.

## Measurement and classification

For each block, compare its five cases with the common-compatibility control using the same support-aware response metric and frozen excursion classification as `global_numerical_precision_diagnostic.py`.

A block is `LOCALIZED` only under the already frozen criterion: default/control Emax > 9, tested Emax <= 3, and at least two TT/EE/TE middle-point responses fall by >=5x. `STRONGLY_SENSITIVE`, `INSENSITIVE`, and `PROVIDER_BLOCKED` retain the existing definitions.

No block may be recombined or retuned until all six one-at-a-time results are known. This diagnostic cannot promote K1/K4 or constitute physical falsification.
