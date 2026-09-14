# W04 M21 G2 execution-capacity recovery v0.1

Frozen: 2026-09-14 while recovered parent run `34869857740` has terminal G1/G3 lanes but G2 `f2/f3/f4` are still `in_progress`, before any G2 physical-lane outcome is available.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`  
Parent protocol: `protocol/W04_M21_CONDITIONAL_CMB_PRECISION_COMPONENT_DECOMPOSITION_v0.1.md`  
Serialization recovery: `protocol/W04_M21_CMB_PRECISION_COMPONENT_SERIALIZATION_RECOVERY_v0.2.md`

## Status

**CONDITIONAL / DO NOT EXECUTE unless a required G2 lane from run `34869857740` terminates specifically because of execution time/capacity rather than producing a valid provider result.**

If all four G2 lanes complete successfully in the parent run, this recovery is `NOT_APPLICABLE` and must never be run.

## Activation

Recovery is authorized only for a missing required G2 case whose parent lane has terminal evidence consistent with one of:

- internal provider wrapper timeout `rc=124`;
- GitHub job timeout/cancellation caused by the frozen execution-time ceiling after exact provider build/profile validation;
- equivalent hosted-runner capacity termination before an interpretable cosmological result is uploaded.

A provider-level numerical error, nonfinite cosmological output, scientific classification, or any successful G2 lane does **not** authorize rerunning that case under this protocol.

## Immutable scientific configuration

For each authorized missing case, rerun exactly the same recovered G2 profile and exact same physical input as in run `34869857740`:

- exact provider pin unchanged;
- `class/cl_permille.pre` unchanged;
- `verification/m21/m21_ncdm_tight.pre` unchanged;
- `evolver=0` unchanged;
- the frozen G2 assignment list unchanged;
- deterministic unique-key serialization unchanged;
- `ref/f2/f3/f4` case file unchanged;
- output requests, gauge, modes, l/k ranges unchanged;
- analyzer and frozen TT/EE/TE classification thresholds unchanged.

No tolerance, grid, physics parameter, response metric, or pass/fail threshold may be altered.

## Only permitted change

Execution allowance may be increased from the parent wrapper limit of 2700 seconds to **5400 seconds** for an authorized timed-out case, with the GitHub job timeout raised only enough to contain that wrapper limit (e.g. 100 minutes).

This is an infrastructure/execution-capacity recovery only.

## Evidence merge

- Reuse every successful immutable G2 artifact from parent run `34869857740`.
- Replace no successful lane.
- Add only recovered artifacts for cases that were missing solely because of an authorized capacity timeout.
- The final G2 group classifier must consume one exact valid artifact per `ref/f2/f3/f4` and apply the unchanged parent analyzer.

## Classification discipline

A successful capacity recovery has no scientific meaning by itself. Only the merged four-case G2 result may receive `GROUP_REMOVES_EXCURSION`, `GROUP_REDUCES_EXCURSION`, or `GROUP_INSUFFICIENT` under the frozen parent protocol.

If the longer execution also fails to produce valid evidence, G2 remains `GROUP_BLOCKED`; do not extend again without a new preregistered implementation diagnosis.

`K1_promoted=false`; `physical_falsification=false` for all recovery states.
