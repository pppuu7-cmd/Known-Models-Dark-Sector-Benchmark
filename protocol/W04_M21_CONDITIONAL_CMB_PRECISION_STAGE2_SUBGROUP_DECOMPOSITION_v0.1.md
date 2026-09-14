# W04 M21 conditional CMB precision stage-2 subgroup decomposition v0.1

Frozen: 2026-09-14 while the recovered G1/G2/G3 parent decomposition run `34869857740` is non-terminal and before any recovered parent-group scientific result is available.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Parent protocols:

- `protocol/W04_M21_CONDITIONAL_CMB_PRECISION_COMPONENT_DECOMPOSITION_v0.1.md`
- `protocol/W04_M21_CMB_PRECISION_COMPONENT_SERIALIZATION_RECOVERY_v0.2.md`

Source-map authority:

- `waves/wave_04_dark_matter/M21_CMB_PRECISION_COMPONENT_SOURCE_MAP.json`

## Status

**CONDITIONAL / NOT AUTHORIZED TO EXECUTE until the recovered parent G1/G2/G3 aggregate is terminal.**

This protocol exists to prevent post-hoc scalar-knob selection if one or more parent precision groups are sufficient.

## Activation rule

For each parent group independently:

- activate that group's stage-2 subgroups only if its terminal parent classification is `GROUP_REMOVES_EXCURSION` or `GROUP_REDUCES_EXCURSION`;
- do not execute stage-2 subgroups for a parent classified `GROUP_INSUFFICIENT` or `GROUP_BLOCKED`;
- if multiple parent groups are sufficient, activate all corresponding subgroup families in parallel and record all sufficient subgroups without choosing a preferred parent post hoc.

The full-reference activation remains `M21_FULL_CMB_REFERENCE_PRECISION_REMOVES_EXCURSION` from run `34864827822`.

## Common frozen baseline

Every stage-2 lane starts from the same effective baseline used by the parent component diagnostic:

1. exact `class/cl_permille.pre`;
2. exact `verification/m21/m21_ncdm_tight.pre`;
3. `evolver=0`;
4. only the subgroup assignments listed below.

Serialize with the same deterministic unique-key last-frozen-assignment semantics defined by the v0.2 serialization recovery. No duplicate-key parser ambiguity is permitted.

Physical cases remain exactly `ref/f2/f3/f4`; provider pin, cosmology, outputs, gauge, modes, k range and l_max remain unchanged.

## G1 stage-2 partition — thermodynamics / perturbation-source evolution

Two G1 entries, `tol_perturbations_integration=1.e-6` and `perturbations_sampling_stepsize=0.01`, are already present with identical values in the common `m21_ncdm_tight.pre` baseline. They are therefore explicit no-op members of the parent G1 construction and are not re-tested as causal stage-2 changes.

### G1A — recombination / thermodynamics table accuracy

Append exactly:

```ini
recfast_Nz0=100000
tol_thermo_integration=1.e-5
recfast_x_He0_trigger_delta=0.01
recfast_x_H0_trigger_delta=0.01
```

### G1B — source-start and tight-coupling transition timing

Append exactly:

```ini
start_small_k_at_tau_c_over_tau_h=0.0004
start_large_k_at_tau_h_over_tau_k=0.05
tight_coupling_trigger_tau_c_over_tau_h=0.005
tight_coupling_trigger_tau_c_over_tau_k=0.008
start_sources_at_tau_c_over_tau_h=0.006
```

### G1C — photon/UR hierarchy and streaming evolution

Append exactly:

```ini
l_max_g=50
l_max_pol_g=25
l_max_ur=50
radiation_streaming_approximation=2
radiation_streaming_trigger_tau_over_tau_k=240.
radiation_streaming_trigger_tau_c_over_tau=100.
ur_fluid_approximation=2
ur_fluid_trigger_tau_over_tau_k=50.
```

The three active G1 subgroups plus the two baseline-identical no-op entries exhaust the parent G1 assignment set.

## G2 stage-2 partition — sampling / projection grid

### G2A — perturbation k-grid density and range

Append exactly:

```ini
k_min_tau0=0.002
k_max_tau0_over_l_max=3.
k_step_sub=0.015
k_step_super=0.0001
k_step_super_reduction=0.1
```

### G2B — multipole / hyperspherical projection sampling

Append exactly:

```ini
l_logstep=1.026
l_linstep=25
hyper_sampling_flat=12.
hyper_sampling_curved_low_nu=10.
hyper_sampling_curved_high_nu=10.
hyper_nu_sampling_step=10.
hyper_phi_min_abs=1.e-10
hyper_x_tol=1.e-4
hyper_flat_approximation_nu=1.e6
```

### G2C — transfer q-grid sampling

Append exactly:

```ini
q_linstep=0.20
q_logstep_spline=20.
q_logstep_trapzd=0.5
q_numstep_transition=250
```

These three subgroups exactly partition the parent G2 assignment list.

## G3 stage-2 partition — scalar transfer/source support

### G3A — scalar transfer k-support window

Append exactly:

```ini
transfer_neglect_delta_k_S_t0=100.
transfer_neglect_delta_k_S_t1=100.
transfer_neglect_delta_k_S_t2=100.
transfer_neglect_delta_k_S_e=100.
```

### G3B — temporal/visibility source support

Append exactly:

```ini
neglect_CMB_sources_below_visibility=1.e-30
transfer_neglect_late_source=3000.
```

These two subgroups exactly partition the parent G3 assignment list.

## Execution design if activated

For every activated subgroup, run an independent `ref/f2/f3/f4` matrix. Different activated subgroups may run concurrently. No subgroup may use another subgroup's result during execution.

Apply unchanged parent TT/EE/TE response metrics and the same frozen parent numerical scale:

`Emax_parent_RK = 534.8355868817356`.

For each subgroup define `Emax_subgroup=max(E_TT,E_EE,E_TE)`.

Frozen classification:

- `SUBGROUP_REMOVES_EXCURSION` iff all TT/EE/TE excursion factors <= 3;
- `SUBGROUP_REDUCES_EXCURSION` iff removal fails but `Emax_subgroup <= Emax_parent_RK/3`;
- `SUBGROUP_INSUFFICIENT` otherwise;
- missing/nonfinite/provider-invalid evidence -> `SUBGROUP_BLOCKED`, never physical failure.

For each activated parent:

- record **all** sufficient subgroups;
- if one or more subgroups are sufficient: `<PARENT>_STAGE2_SUBGROUP_SUFFICIENCY_IDENTIFIED`;
- if no subgroup is sufficient while the parent was sufficient: `<PARENT>_STAGE2_WITHIN_GROUP_INTERACTION_REQUIRED`;
- if any required subgroup is blocked: `<PARENT>_STAGE2_BLOCKED`.

## Interpretation ceiling

Stage-2 sufficiency narrows a numerical precision-sensitive module family. It does not establish a unique bug, does not authorize single-parameter tuning, does not promote K1/K3/K4, and is not a physical falsification of mixed cold+warm dark matter.

Any later single-parameter diagnostic requires a new preregistration after this stage is terminal.
