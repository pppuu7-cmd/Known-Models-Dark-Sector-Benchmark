# M21 numerical CMB precision current front — 2026-09-14

## STATE_READ

Authoritative repository: `pppuu7-cmd/Known-Models-Dark-Sector-Benchmark`.
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## TERMINAL STAGE-2

M21 CMB precision stage-2 subgroup decomposition is terminal.

- run: `34872522336`
- aggregate artifact: `10360228613`
- digest: `sha256:2a6499bcafdd321a5f3832870657aca12210e5f5a64f1b3dc429b56cbbc24e7c`
- classification: `M21_CMB_PRECISION_STAGE2_COMPLETE`
- G1A: `SUBGROUP_REMOVES_EXCURSION`, `Emax=0.03431664516144772`
- G2B: `SUBGROUP_REDUCES_EXCURSION`, `Emax=34.304759775112494`
- G1B/G1C/G2A/G2C: insufficient
- K1/K3/K4 not promoted; no physical falsification.

Canonical result:
`waves/wave_04_dark_matter/M21_CMB_PRECISION_STAGE2_SUBGROUP_DECOMPOSITION_TERMINAL.json`.

## TERMINAL STAGE-3

Prospectively frozen protocol:
`protocol/W04_M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_v0.1.md`.

- run: `34878158930`
- head: `92fc5387c5e9d59df39e792c9dbaab3bfb708f58`
- aggregate artifact: `10361784318`
- digest: `sha256:733e995346926ebbb3dd7355a33fbc0090fb5cc027b66eea0c7c968bc86453a9`
- classification: `M21_CMB_PRECISION_STAGE3_COMPLETE`
- cross-lane input identity: true
- all 13 mandatory parameter jobs and aggregate: terminal success
- canonical terminal result: `waves/wave_04_dark_matter/M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_TERMINAL.json`.

### G1A result

`G1A_STAGE3_SINGLE_PARAMETER_SUFFICIENCY_IDENTIFIED`.

Only sufficient parameter:
- `tol_thermo_integration=1e-5`: `PARAMETER_REMOVES_EXCURSION`, `Emax=0.03431664516144772`.

Insufficient controls reproduce the parent excursion exactly (`Emax=534.8355868817356`):
- `recfast_Nz0=100000`;
- `recfast_x_He0_trigger_delta=0.01`;
- `recfast_x_H0_trigger_delta=0.01`.

### G2B result

`G2B_STAGE3_SINGLE_PARAMETER_SUFFICIENCY_IDENTIFIED`.

Sufficient reducers:
- `l_logstep=1.026`: `Emax=70.53199679337801`;
- `l_linstep=25`: `Emax=78.37222398394675`.

All seven other G2B individual controls are insufficient. `hyper_sampling_flat=12` changes Emax only slightly (`534.8263913081856`); the remaining six frozen controls reproduce `534.8355868817356` exactly in this benchmark.

Stage-3 is numerical localization only and does not promote K1/K3/K4.

## TERMINAL EXACT-PIN SOURCE AUDIT

Machine audit run `34878816263` is terminal `success`.

- artifact: `10361793059`
- digest: `sha256:fb0d901bda733bb45121a11535628b0c0dc4b30fd034f14f0eafb391cfe49662`
- classification: `M21_STAGE3_SOURCE_SEMANTIC_AUDIT_PASS_WITH_SCOPE`
- canonical result: `waves/wave_04_dark_matter/M21_STAGE3_EXACT_PIN_SOURCE_SEMANTIC_AUDIT_RESULT.json`
- narrative audit: `models/mixed_cold_warm/m21_stage3_exact_pin_source_semantic_audit_2026-09-14.md`.

Source/numerical agreement is unusually clean:

1. `recfast_Nz0`: zero runtime consumers; stage-3 insufficient with exactly baseline Emax.
2. `recfast_x_He0_trigger_delta`: zero runtime consumers; stage-3 insufficient with exactly baseline Emax.
3. `recfast_x_H0_trigger_delta`: zero runtime consumers; stage-3 insufficient with exactly baseline Emax.
4. `tol_thermo_integration`: four direct runtime consumers in `source/thermodynamics.c`; stage-3 identifies it as the sole G1A sufficient parameter.
5. exact transfer source identifies `l_logstep/l_linstep` as general multipole-sampling controls; stage-3 identifies both as G2B sufficient reducers.
6. flat M21 branch / default-identical hyperspherical controls are numerically insufficient as expected from source semantics.

## REFERENCE-PROFILE INTERPRETATION

See `models/mixed_cold_warm/m21_reference_profile_monotonicity_audit_2026-09-14.md`.

Exact `cl_ref.pre` is not a componentwise monotone precision-tightening ladder. Crucially, it sets `tol_thermo_integration=1e-5` while exact default is `1e-6`; the same coexistence is already present at checked 2023 commit `45195306dac09fab6bd9cf23320974f418c81f27`. Therefore the G1A result is sensitivity to a reference-profile numerical path, not yet evidence of convergence-by-tightening.

## ACTIVE PARALLEL GATES

### A. Thermodynamics tolerance-direction audit

Protocol frozen before stage-3 result:
`protocol/W04_M21_CONDITIONAL_THERMODYNAMICS_TOLERANCE_DIRECTION_AUDIT_v0.1.md`.

Stage-3 satisfied its prospective activation condition. Workflow run `34879598732` activation is terminal success and all seven mandatory tolerance lanes are authorized/queued:
`1e-4, 3e-5, 1e-5, 3e-6, 1e-6, 3e-7, 1e-7`.

Only `tol_thermo_integration` varies. This gate asks whether the `1e-5` excursion removal survives actual tightening or is reference-value/path-specific/nonmonotone.

### B. G2B transfer-l sampling interaction/direction audit

Protocol:
`protocol/W04_M21_G2B_TRANSFER_L_SAMPLING_DIRECTION_INTERACTION_AUDIT_v0.1.md`.

Workflow run `34879864684` launched four independent pure-pair lanes:
- `LPAIR_I=(l_logstep=1.05,l_linstep=32)`;
- `LPAIR_R=(1.026,25)`;
- `LPAIR_T1=(1.015,20)`;
- `LPAIR_T2=(1.010,15)`.

This gate tests whether the two stage-3 sufficient transfer-l controls interact and whether further sampling refinement behaves directionally/monotonically. It is independent of the thermodynamics tolerance audit and may run in parallel.

## CLAIM_CEILING

All current gates are numerical localization/convergence diagnostics. They do not establish a CLASS bug, do not authorize production tuning, do not promote M21 K1/K3/K4, and do not physically falsify or validate mixed cold+warm dark matter.

## NEXT_ACTION

1. Do not rerun stage-2 or stage-3; both are terminal.
2. Check runs `34879598732` and `34879864684`; do not use partial substantive values while either aggregate is non-terminal.
3. Once each aggregate is terminal, verify artifact identities/digests and materialize canonical terminal results.
4. Use their joint result to decide whether the original f3 CMB excursion is best classified as a thermodynamics solver-path sensitivity, transfer-l sampling under-resolution, a mixed numerical interaction, or a still-unresolved numerical artifact.
5. K1/K3/K4 remain locked until a separately authorized gate establishes the required physical/numerical reference-limit conditions.
