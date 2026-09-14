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
Activation job is terminal PASS and authorizes all 13 mandatory lanes. Do not use partial stage-3 substantive values before the aggregate is terminal.

Mandatory parameter family:

- G1A: `recfast_Nz0`, `tol_thermo_integration`, `recfast_x_He0_trigger_delta`, `recfast_x_H0_trigger_delta`;
- G2B: `l_logstep`, `l_linstep`, `hyper_sampling_flat`, `hyper_sampling_curved_low_nu`, `hyper_sampling_curved_high_nu`, `hyper_nu_sampling_step`, `hyper_phi_min_abs`, `hyper_x_tol`, `hyper_flat_approximation_nu`.

All 13 jobs run independently; each job executes immutable `ref/f2/f3/f4` with hard per-case timeout and uploads artifacts even on failure. Aggregate classification is frozen before execution.

## OUTCOME_INDEPENDENT_SOURCE_AUDIT

See `models/mixed_cold_warm/m21_stage3_exact_pin_source_semantic_audit_2026-09-14.md`.

Important source facts established without stage-3 values:

1. exact `cl_ref.pre` contains `recfast_Nz0=100000`, but exact `include/precisions.h` has no such precision field; exact parser handles unread keys as warnings/unused inputs. Therefore `recfast_Nz0` is a legacy/unconsumed negative-control entry at this pin.
2. `tol_thermo_integration` is directly consumed by the thermodynamics evolver.
3. frozen M21 has `Omega_k=0`. Exact `transfer.c` shows the flat branch directly consumes `hyper_sampling_flat` and `hyper_phi_min_abs`; curved sampling/nu controls are non-flat paths. `hyper_x_tol` is open-universe-specific; `hyper_flat_approximation_nu` is curved-only.
4. `hyper_phi_min_abs=1e-10` and `hyper_x_tol=1e-4` equal exact defaults, so their individual stage-3 lanes are no-op controls.
5. source-active non-default G2B candidates for this flat benchmark are principally `l_logstep`, `l_linstep`, and `hyper_sampling_flat`.

These facts do not alter or prune the frozen 13-lane matrix.

## CLAIM_CEILING

Stage-3 is numerical localization only. No partial or terminal stage-3 result may be promoted directly to a CLASS bug, production tuning rule, M21 K1/K3/K4 PASS/FAIL, or physical mixed-dark-matter conclusion.

## NEXT_ACTION

1. Check run `34878158930`.
2. If non-terminal, do not duplicate it and do not consume partial parameter values; only outcome-independent source/provenance work is allowed.
3. Once aggregate is terminal, verify artifact identities and frozen classifier, materialize canonical terminal result, then decide whether any further diagnostic is authorized.
