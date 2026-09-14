# W04 M21 conditional CMB precision-component decomposition v0.1

Frozen: 2026-09-14 while `W04 M21 full CMB reference-precision diagnostic` is still non-terminal.

Status: **CONDITIONAL / NOT AUTHORIZED TO EXECUTE YET**.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.
Parent numerical baseline: RK P2 = exact `cl_permille.pre` + `verification/m21/m21_ncdm_tight.pre` + `evolver=0`.

## Activation condition

Execute this decomposition only if the terminal full-reference gate classifies either

- `M21_FULL_CMB_REFERENCE_PRECISION_REMOVES_EXCURSION`, or
- `M21_FULL_CMB_REFERENCE_PRECISION_REDUCES_EXCURSION`.

If the terminal classification is `...EXCURSION_PERSISTS`, this protocol remains historical preparation and MUST NOT be launched.

## Purpose

Identify which pre-frozen category of changes present in exact `cl_ref.pre`, but absent from the parent RK P2 baseline, is sufficient to reduce the f_w=0.003 CMB excursion. No individual scalar knob may be selected after seeing the full-reference result.

All lanes reuse unchanged physical ref/f2/f3/f4 cases, exact provider pin, RK evolver, output set, gauge, k range and l_max.

## Frozen baseline shared by all component lanes

Start from exact `cl_permille.pre`, append `verification/m21/m21_ncdm_tight.pre`, then append `evolver=0`.

Thus the already tested ncdm hierarchy/tolerances and RK integrator are common controls. Each component lane appends exactly one group below.

## Group G1 — perturbation/source evolution

Append exactly:

```
recfast_Nz0=100000
tol_thermo_integration=1.e-5
recfast_x_He0_trigger_delta=0.01
recfast_x_H0_trigger_delta=0.01
start_small_k_at_tau_c_over_tau_h=0.0004
start_large_k_at_tau_h_over_tau_k=0.05
tight_coupling_trigger_tau_c_over_tau_h=0.005
tight_coupling_trigger_tau_c_over_tau_k=0.008
start_sources_at_tau_c_over_tau_h=0.006
l_max_g=50
l_max_pol_g=25
l_max_ur=50
tol_perturbations_integration=1.e-6
perturbations_sampling_stepsize=0.01
radiation_streaming_approximation=2
radiation_streaming_trigger_tau_over_tau_k=240.
radiation_streaming_trigger_tau_c_over_tau=100.
ur_fluid_approximation=2
ur_fluid_trigger_tau_over_tau_k=50.
```

The ncdm settings in full `cl_ref.pre` are excluded here because they are already present in the common M21 tight baseline.

## Group G2 — k/l/q transfer and projection grid

Append exactly:

```
k_min_tau0=0.002
k_max_tau0_over_l_max=3.
k_step_sub=0.015
k_step_super=0.0001
k_step_super_reduction=0.1
l_logstep=1.026
l_linstep=25
hyper_sampling_flat=12.
hyper_sampling_curved_low_nu=10.
hyper_sampling_curved_high_nu=10.
hyper_nu_sampling_step=10.
hyper_phi_min_abs=1.e-10
hyper_x_tol=1.e-4
hyper_flat_approximation_nu=1.e6
q_linstep=0.20
q_logstep_spline=20.
q_logstep_trapzd=0.5
q_numstep_transition=250
```

## Group G3 — CMB transfer-support truncation

Append exactly:

```
transfer_neglect_delta_k_S_t0=100.
transfer_neglect_delta_k_S_t1=100.
transfer_neglect_delta_k_S_t2=100.
transfer_neglect_delta_k_S_e=100.
neglect_CMB_sources_below_visibility=1.e-30
transfer_neglect_late_source=3000.
```

Vector/tensor transfer thresholds from `cl_ref.pre` are omitted because this frozen family gate requests scalar modes only.

## Explicit exclusions

- `accurate_lensing`, `num_mu_minus_lmax`, `delta_l_max` are excluded because the frozen M21 INIs use `lensing=no` and do not request lensed Cls.
- nonlinear/halofit settings are excluded because `non linear = none`.
- tensor hierarchy settings are excluded because `modes=s`.
- no model or ncdm physical parameter changes are allowed.

## Execution design if activated

Run three independent matrices G1/G2/G3, each with ref/f2/f3/f4. No matrix may use another component's result during execution. Apply the same TT/EE/TE whole-vector and ell-band metrics as the full-reference gate.

For each group define `Emax_group = max(E_TT,E_EE,E_TE)`.

Frozen sufficiency categories:

- `GROUP_REMOVES_EXCURSION` if all TT/EE/TE excursion factors <=3;
- `GROUP_REDUCES_EXCURSION` if removal fails but `Emax_group <= Emax_parent_RK/3` with frozen `Emax_parent_RK=534.8355868817356`;
- `GROUP_INSUFFICIENT` otherwise.

Aggregate classification:

- one or more sufficient groups: record all sufficient groups; do not choose one post hoc if multiple qualify;
- no sufficient group while full `cl_ref.pre` had reduced/removed the anomaly: `M21_CMB_REFERENCE_PRECISION_INTERACTION_REQUIRED`;
- missing/nonfinite evidence: BLOCKED, never physical failure.

## Interpretation ceiling

Component sufficiency localizes numerical implementation sensitivity only. It does not prove a unique bug and does not promote K1. `K1_promoted=false`, `physical_falsification=false`.
