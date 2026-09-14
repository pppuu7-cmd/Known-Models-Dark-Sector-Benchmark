# M21 stage-3 current front — 2026-09-14

## STATE_READ

Authoritative repository: `pppuu7-cmd/Known-Models-Dark-Sector-Benchmark`.
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## TERMINAL_PARENT

M21 CMB precision stage-2 subgroup decomposition is terminal.

- run: `34872522336`
- aggregate artifact: `10360228613`
- digest: `sha256:2a6499bcafdd321a5f3832870657aca12210e5f5a64f1b3dc429b56cbbc24e7c`
- classification: `M21_CMB_PRECISION_STAGE2_COMPLETE`
- G1A: `SUBGROUP_REMOVES_EXCURSION`, `Emax=0.03431664516144772`
- G2B: `SUBGROUP_REDUCES_EXCURSION`, `Emax=34.304759775112494`
- G1B/G1C/G2A/G2C: insufficient
- K1/K3/K4 not promoted; no physical falsification.

Canonical terminal summary:
`waves/wave_04_dark_matter/M21_CMB_PRECISION_STAGE2_SUBGROUP_DECOMPOSITION_TERMINAL.json`.

## ACTIVE_GATE

Prospectively frozen stage-3 single-parameter decomposition:
`protocol/W04_M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_v0.1.md`.

Execution run: `34878158930`, head `92fc5387c5e9d59df39e792c9dbaab3bfb708f58`.
Activation is PASS. All 13 mandatory parameter jobs are now terminal `success`; aggregate job `104094581455` is queued at this recovery update. Do not consume individual parameter artifacts or values before the aggregate is terminal.

Mandatory parameter family:

- G1A: `recfast_Nz0`, `tol_thermo_integration`, `recfast_x_He0_trigger_delta`, `recfast_x_H0_trigger_delta`;
- G2B: `l_logstep`, `l_linstep`, `hyper_sampling_flat`, `hyper_sampling_curved_low_nu`, `hyper_sampling_curved_high_nu`, `hyper_nu_sampling_step`, `hyper_phi_min_abs`, `hyper_x_tol`, `hyper_flat_approximation_nu`.

## TERMINAL EXACT-PIN SOURCE AUDIT

Machine audit run `34878816263` is terminal `success`.

- artifact: `10361793059`
- digest: `sha256:fb0d901bda733bb45121a11535628b0c0dc4b30fd034f14f0eafb391cfe49662`
- classification: `M21_STAGE3_SOURCE_SEMANTIC_AUDIT_PASS_WITH_SCOPE`
- canonical result: `waves/wave_04_dark_matter/M21_STAGE3_EXACT_PIN_SOURCE_SEMANTIC_AUDIT_RESULT.json`
- narrative audit: `models/mixed_cold_warm/m21_stage3_exact_pin_source_semantic_audit_2026-09-14.md`.

Important exact-pin facts established without stage-3 numerical values:

1. `recfast_Nz0`: zero runtime consumers; not an exact-pin precision declaration; legacy/unconsumed reference-profile entry.
2. `recfast_x_He0_trigger_delta`: exact declaration/default `0.05`, but zero runtime consumers in the exact repository tree.
3. `recfast_x_H0_trigger_delta`: exact declaration/default `0.05`, but zero runtime consumers in the exact repository tree.
4. `tol_thermo_integration`: four direct runtime consumers in `source/thermodynamics.c`; among the four G1A changes it is the only runtime-consumed key.
5. frozen M21 has `Omega_k=0`. G2B runtime/branch audit shows flat-relevant non-default candidates are principally `l_logstep`, `l_linstep`, and `hyper_sampling_flat`; curved-only/default-identical lanes remain required negative controls.
6. `hyper_phi_min_abs=1e-10` and `hyper_x_tol=1e-4` equal exact defaults.

These source facts do not alter or prune the prospectively frozen 13-lane numerical matrix.

## REFERENCE-PROFILE INTERPRETATION

See `models/mixed_cold_warm/m21_reference_profile_monotonicity_audit_2026-09-14.md`.

Exact `cl_ref.pre` is not a componentwise monotone precision-tightening ladder. In particular it sets `tol_thermo_integration=1e-5` while the exact default is `1e-6`; the same coexistence is already present at checked commit `45195306dac09fab6bd9cf23320974f418c81f27` from 2023-10-10, where `cl_ref.pre` has the same blob SHA as the M21 pin. Therefore stage-2/stage-3 reference-profile sensitivity must not be called convergence-by-tightening without a separate directional gate.

## CONDITIONAL SUCCESSOR PREPARED PROSPECTIVELY

Before stage-3 aggregate result, froze:
`protocol/W04_M21_CONDITIONAL_THERMODYNAMICS_TOLERANCE_DIRECTION_AUDIT_v0.1.md`.

Implementation/workflow are already committed. The workflow is triggered only after completion of the stage-3 workflow and activates only if terminal stage-3 is complete, input identity passes, G1A is unblocked, and `G1A__tol_thermo_integration` is numerically sufficient. Otherwise it remains skipped historical preparation.

Frozen tolerance ladder: `1e-4, 3e-5, 1e-5, 3e-6, 1e-6, 3e-7, 1e-7`. Only `tol_thermo_integration` varies. This gate distinguishes tightening-preserved removal/sufficiency from a reference-value path-specific or nonmonotone response; it cannot promote K1/K3/K4.

## CLAIM_CEILING

Stage-3 and its conditional successor are numerical-localization/diagnostic gates only. They cannot directly establish a CLASS bug, authorize production tuning, promote M21 K1/K3/K4, or physically falsify/validate mixed cold+warm dark matter.

## NEXT_ACTION

1. Check aggregate job `104094581455` / run `34878158930`.
2. If still non-terminal, do not duplicate it and do not consume individual parameter values.
3. Once aggregate is terminal, verify artifact identity/digest and frozen classification and materialize a canonical terminal stage-3 result.
4. Observe whether the already-preregistered conditional thermodynamics-tolerance workflow activates. If it activates, its seven tolerance lanes are the authorized next numerical gate; if not, choose the next gate from the terminal stage-3 result without modifying historical criteria.
