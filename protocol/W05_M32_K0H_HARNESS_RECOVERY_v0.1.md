# W05 M32 K0h harness-only recovery v0.1

Date: 2026-09-12
Parent scientific/infrastructure contract: `protocol/W05_M32_K0H_HYDRO_TAIL_MICROCHECKPOINT_PREREGISTRATION_v0.1.md`.
Parent run: `34710463111`.

## Causal defect
The target compile completed before the post-compile classifier, but the workflow had changed directory to `work/provider/bin` and then the Python classifier attempted to read `result/build_stdout.log` and `result/build_stderr.log` as relative paths. Nine jobs uploaded immutable artifacts containing their build exit code, logs and, when successful, compiled target object. The `umuscl.o` job did not upload an artifact.

This is a harness path defect only. No compiler, source, flags, target list, threshold or physical setting may change.

## Frozen recovery
1. Recover and classify the nine immutable target artifacts already uploaded by run `34710463111` using only `build_exit_code.txt`, object existence and build logs.
2. Recompute only the missing `umuscl.o` target from the same immutable stage-1 artifact `10283774354`, with the same exact provider pin, `mpiifx`, flags and mtime-only checkpoint normalization.
3. Aggregate all ten target classifications under the unchanged K0h interpretation.

No successfully computed target may be recompiled merely because its classifier failed. No K0 promotion or physical conclusion follows from this recovery.
