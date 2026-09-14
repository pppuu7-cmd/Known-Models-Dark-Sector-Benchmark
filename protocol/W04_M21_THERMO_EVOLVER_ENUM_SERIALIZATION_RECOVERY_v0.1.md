# W04 M21 thermodynamics-evolver enum serialization recovery v0.1

Frozen: 2026-09-14 after terminal harness-blocked run `34883668337` and before any recovery scientific execution.

Parent scientific preregistration remains:
`protocol/W04_M21_CONDITIONAL_THERMO_EVOLVER_CROSSCHECK_v0.1.md`.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Observed blocker

All six parent lanes failed before scientific output. Exact run logs show CLASS stopped in `input_read_precisions()` at `parser_read_int(...,"thermo_evolver",...)` because the harness serialized semantic enum labels (`ndf15` or `rk`) as strings.

Exact source declares `enum evolver_type { rk, ndf15 }`, hence exact integer serialization is:

- `rk = 0`;
- `ndf15 = 1`.

The existing common control `evolver=0` already demonstrates integer enum serialization in this benchmark.

## Recovery scope

The only permitted change is textual serialization of `thermo_evolver`:

- semantic `ndf15` lanes shall write `thermo_evolver = 1`;
- semantic `rk` lanes shall write `thermo_evolver = 0`.

The manifest/lane metadata shall retain the semantic solver label and additionally record the serialized integer.

No scientific dimension changes. The six mandatory lanes remain exactly:

- NDF_T1E5: ndf15, 1e-5
- NDF_T1E6: ndf15, 1e-6
- NDF_T1E7: ndf15, 1e-7
- RK_T1E5: rk, 1e-5
- RK_T1E6: rk, 1e-6
- RK_T1E7: rk, 1e-7

Same physical INIs, provider pin, generic `evolver=0`, precision baselines, outputs, hard timeouts, response metric, thresholds and frozen classifier.

## Recovery gates

Each generated profile must contain exactly one `thermo_evolver` and one `tol_thermo_integration` key. Before CLASS execution, the recovery harness must assert the integer serialization is exactly 0 for RK and 1 for NDF15, while semantic metadata matches the parent lane identity.

Any new parser/harness failure remains BLOCKED and cannot be interpreted scientifically.

## Interpretation ceiling

Recovery only restores the preregistered experiment to executable form. It cannot alter the parent hypotheses, thresholds or scientific claim ceiling.
