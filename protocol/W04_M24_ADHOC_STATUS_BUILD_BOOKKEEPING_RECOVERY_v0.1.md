# W04 M24 ad-hoc status/build bookkeeping recovery v0.1

Date: 2026-09-12
Status: FROZEN BEFORE RECOVERY EXECUTION

## Defect
The ad-hoc full compatible K1 ladder and precision-profile sweep execute the pinned CLASS build in a fail-fast step, but initialize `status.json` as an empty object. The unchanged authoritative analyzer `verification/m24/ethos1_k1_reference.py` requires the key `build` together with `ref`, `zero`, and `a0..a4`. Therefore a successful build followed by successful provider cases is prematurely classified as `M24_ETHOS1_K1_PROVIDER_EXECUTION_BLOCKED` because `status.get("build")` is `None`.

## Frozen process-only repair
After the build step has returned success, initialize `status.json` with exactly `{ "build": 0 }` instead of `{}`. No CLASS source, provider pin, cosmological parameter, IDM-DR parameter, precision-profile value, case grid, numerical threshold, K1 decision rule, or analyzer code may change.

## Interpretation
The pre-recovery ad-hoc classifications are harness-invalid for scientific interpretation. The recovery rerun is authoritative only if the same pinned physics workload executes and the unchanged analyzer consumes a complete status map. Infrastructure failure remains infrastructure failure; a failed frozen K1 gate remains a scientific/numerical negative result and must not be retuned.
