# W03 M14 IDECAMB coupled-quintessence theory-only output route — preregistration v0.1

Date frozen: 2026-09-10
Scientific promotion authorized by this gate: **NO**.

## Purpose

Recover an author-compatible theory-output execution route for the independently pinned coupled-quintessence provider after the prior output-schema probe terminated before theory output because the executable was built without the external Planck CLIK likelihood stack.

This is an infrastructure/output gate only. It does not score K1-K9 and cannot overwrite any previous M14 result.

## Frozen provider provenance

- base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- overlay procedure: copy the IDECAMB tracked files over the pinned CosmoMC tree, matching the provider README installation instruction.
- compiler compatibility flag already isolated by the earlier provider-build recovery: `-fallow-argument-mismatch`. No Fortran source edit is permitted.

## Source basis frozen before execution

At the pinned CosmoMC base, `action=4` calls `Setup%DoTests`. The cosmology likelihood calculator calls `CalculateRequiredTheoryChanges()` before likelihood summation. With `get_sigma8=T`, the cosmology calculator requests transfer/power theory. `test_output_root` writes the computed `Params%Theory` only when the parameter point is valid and non-`logZero`.

The previous CQ output-schema probe kept the author Planck likelihood DEFAULTs while the executable was intentionally built without CLIK, so execution stopped at the external-likelihood requirement before the requested theory files were emitted. That result remains authoritative as `OUTPUT_SCHEMA_NOT_EMITTED` for that exact route.

## Prospectively frozen transformation of author `test_ide.ini`

Start from the exact overlay's tracked `test_ide.ini` and make only the following diagnostic-route changes:

1. Set `Class_IDE = 2` (provider-documented coupled-quintessence class).
2. Set `param[beta_cq]= 0` (analytic coupling-off point; used here only to simplify the infrastructure control, not yet scored as K1).
3. Enable `test_output_root = m14_cq_theory0` using the author-provided output hook.
4. Comment out only the active external likelihood DEFAULTs in the Planck/BAO/Pantheon blocks:
   - `batch3/plik_rd12_HM_v22_TTTEEE.ini`
   - `batch3/lowl.ini`
   - `batch3/lowE.ini`
   - `batch3/lensing.ini`
   - `batch3/BAO.ini`
   - `batch3/Pantheon18.ini`
5. Keep `DEFAULT(batch3/common.ini)` unchanged so the provider's standard cosmology/theory settings remain authoritative.
6. Comment out the author likelihood-value regression line `test_check_compare = 1820.775`, because no external likelihoods are being evaluated in this infrastructure route.
7. Keep `action=4`, `get_sigma8=T`, CQ potential/coupling forms, `alpha_quint`, H0 parameterization and all other cosmological settings unchanged.

No cosmological parameter is tuned after seeing output. No likelihood DEFAULT may be selectively reintroduced based on result.

## Frozen success classification

`THEORY_OUTPUT_ROUTE_PASS` iff all are true:

- provider build exit = 0;
- theory-only CQ run exit = 0;
- log explicitly selects coupled quintessence (`Class_IDE=2` provider message);
- at least one fresh file with prefix `m14_cq_theory0` is emitted;
- at least one emitted file contains numeric rows.

Otherwise classify the narrow reason (`BUILD_BLOCKED`, `THEORY_ROUTE_RUN_BLOCKED`, or `THEORY_OUTPUT_NOT_EMITTED`). None is a physical failure of coupled quintessence.

## Next gate if PASS

Inspect the exact emitted schema without changing the theory point. Then separately preregister K1 `beta_cq=0` decoupling regression against the same scalar model with interaction disabled, including observable matching rules and numerical thresholds frozen before K1 outputs are inspected.
