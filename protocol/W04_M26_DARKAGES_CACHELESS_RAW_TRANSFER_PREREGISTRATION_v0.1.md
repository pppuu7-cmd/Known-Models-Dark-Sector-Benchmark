# W04 M26 DarkAges cacheless raw-transfer recovery preregistration v0.1

## Scope

This is an infrastructure-only recovery for the already preregistered M26 PBH energy-injection provider controls. It does not change the physical PBH cases, cosmology, observables, response thresholds, or scientific classification gate.

The three children remain independent and are evaluated separately:

- `evaporation`
- `spherical`
- `disk`

They MAY run concurrently.

## Frozen provenance

- Provider: `GFAbellan/ExoCLASS`
- Provider commit: `7c4b26e50d240f1f45f120b623aab2dba13094fd`
- Existing baseline/null evidence source run: `34550083757`
- Existing finite-case generator and analyzer: `verification/m26/m26_energy_injection_provider_control.py`
- Parent cache-bypass recovery run: `34550402384`

The parent recovery established that build, baseline and exact-null execution succeed while the finite case remains provider-blocked after deletion of serialized `.obj` files before execution.

## Localized infrastructure hypothesis

At the pinned provider commit, DarkAges initializes transfer functions from immutable ASCII tables under `DarkAgesModule/transfer_functions/original/`, serializes initialized Python objects with `dill`, and later subprocesses reload those serialized objects with an `isinstance(..., transfer)` guard.

The observed finite-only failure is consistent with an inter-process Python serialization/type-identity failure rather than a physical PBH failure.

## Frozen recovery intervention

The only provider-source intervention allowed in this recovery is:

1. Leave all files under `DarkAgesModule/transfer_functions/original/` unchanged.
2. In `DarkAgesModule/DarkAges/__init__.py`, suppress only the two `transfer_dump(...)` calls inside `_transfer_init_and_dump()`:
   - the channel cache write `transfer_Ch*.obj`;
   - the corrected-transfer cache write `transfer_Corr.obj`.
3. Delete any existing `DarkAgesModule/transfer_functions/*.obj` files immediately before the finite run.
4. Therefore every DarkAges subprocess must reconstruct its transfer objects directly from the pinned raw `original/Transfer_*.dat` tables and must not persist/reload serialized transfer objects.

No transfer table, interpolation formula, injection spectrum, PBH parameter, CLASS parameter, or scientific threshold may be edited.

## Execution plan

For each child independently:

1. Reuse the successful baseline and exact-null output files from run `34550083757` without recomputation.
2. Prepare the unchanged finite case using the existing M26 harness.
3. Build the pinned ExoCLASS provider after the cacheless infrastructure patch.
4. Execute only the finite case.
5. Run the unchanged M26 analyzer against the reused baseline/null and newly computed finite output.
6. Record status, logs, provider patch, and resulting classification.

The three child jobs are independent and SHOULD be launched in parallel with `fail-fast: false`.

## Decision rule

- If a finite case still exits non-zero, classify that child as provider execution blocked. This is **not** physical falsification.
- If the finite case executes and the unchanged provider-control gate passes, record the existing scoped provider-control pass classification from the analyzer.
- This infrastructure recovery by itself does not promote K1 or K4 and cannot constitute physical falsification.
- No post-hoc modification of the finite physical point or acceptance thresholds is allowed.

## Audit requirements

Artifacts must retain:

- exact provider pin;
- patch diff;
- raw-transfer file hashes before execution;
- count/list of `.obj` files before and after the finite execution;
- finite stdout/stderr log;
- status JSON;
- unchanged-case manifest;
- analyzer result.
