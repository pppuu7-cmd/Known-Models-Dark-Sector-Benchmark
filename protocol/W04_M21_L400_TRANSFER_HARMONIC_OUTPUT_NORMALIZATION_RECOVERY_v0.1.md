# W04 M21 l=400 transfer-vs-harmonic output-normalization recovery v0.1

Frozen: 2026-09-15 while parent run `34904313450` is still non-terminal, after exact source inspection identified a deterministic QA-normalization mismatch and before any parent transfer/integrand scientific values are consumed.

Parent protocol: `protocol/W04_M21_L400_TRANSFER_VS_HARMONIC_DIAGNOSTIC_v0.1.md`.
Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Pre-terminal harness diagnosis

The parent instrumentation records internal raw sparse harmonic

`phr->cl[..., index_ct_ee]`.

The parent analyzer attempted to compare this raw internal value directly with CLASS-format `cl.dat` EE output.

Exact provider `source/output.c` establishes that `output_one_line_of_cl()` uses

`factor = l*(l+1)/(2*pi)`

and, for `format=class`, writes

`factor * cl[index_ct]`.

Exact `include/common.h` sets `_OUTPUTPRECISION_ = 12` and `class_fprintf_double` prints scientific notation at that precision.

Therefore raw internal `phr->cl` and `cl.dat` are not identity-normalized quantities. A direct equality check is structurally invalid and can only create a harness blocker. This diagnosis does not inspect or depend on the parent transfer/integrand scientific metrics.

## Recovery scope

No CLASS rerun is allowed if the parent lane artifacts contain all of:

- `diag_ref.dat`, `diag_f2.dat`, `diag_f3.dat`, `diag_f4.dat`;
- `lane_meta.json`;
- `l400_transfer_harmonic_patch_manifest.json`;
- the new instrumented `output/*_cl.dat` tables.

The recovery reuses those immutable artifacts plus the same immutable matching factorial-parent artifacts from run `34887488405`.

Only one QA operation changes:

For diagnostic raw internal EE value `Craw(l)` compare

`l(l+1)/(2*pi) * Craw(l)`

against the parsed CLASS-format output EE value.

Because the output is rounded at `_OUTPUTPRECISION_=12`, freeze the QA relative agreement threshold at

`5e-12`.

This is an output-serialization/rounding guard only; it is NOT a scientific threshold.

## Frozen invariants retained without change

All parent scientific definitions remain byte-for-byte semantic invariants:

- exact provider pin;
- lanes A/B and their direct sparse neighbors;
- physical `ref/f2/f3/f4` inputs;
- factorial precision profiles;
- instrumented-vs-immutable-parent full C_l null gate `R_null <= 1e-12`;
- common-k reference-node construction;
- transfer `D_X` and `E_X` definitions;
- EE-integrand `D_X` and `E_X` definitions;
- HIGH boundary `E>3`;
- local-l400 specificity requirement;
- aggregate layer classifier;
- claim ceiling.

No transfer/integrand metric, response value, k window, or scientific threshold may change in this recovery.

## Recovery authority

The analysis-only recovery is authorized only if parent run `34904313450` reaches terminal state and its A/B artifacts are present. It may proceed regardless of whether the parent aggregate itself is BLOCKED, because the purpose is to repair the already-source-proven invalid normalization check using immutable raw evidence.

If either parent lane lacked complete diagnostics because execution itself failed, the corresponding recovery lane remains BLOCKED; no CLASS rerun is silently substituted.

## Classification

Use the exact parent classifier names:

- `M21_L400_SPIKE_PRESENT_IN_E_TRANSFER_KERNEL_WITH_SCOPE`;
- `M21_L400_SPIKE_EMERGES_IN_EE_INTEGRAND_WITH_SCOPE`;
- `M21_L400_SPIKE_EMERGES_IN_HARMONIC_ACCUMULATION_WITH_SCOPE`;
- `M21_L400_TRANSFER_HARMONIC_LOCALIZATION_MIXED_WITH_SCOPE`;
- `M21_L400_TRANSFER_HARMONIC_DIAGNOSTIC_BLOCKED`.

The recovery result must explicitly record the parent run, parent artifact digests, exact normalization factor rule, and that no CLASS execution occurred.
