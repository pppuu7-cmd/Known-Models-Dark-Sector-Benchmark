# W07 M30 K4 output-path recovery v0.1

## Purpose
Recover the already-computed M30 local-2D K4 provider-precision ladder from immutable artifacts of Actions run `34719607382` without rerunning hi_class physics.

## Frozen parent evidence
Provider pin: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
Parent run: `34719607382`.
Immutable point artifacts:
- base: `10305654365`, digest `sha256:d0e76d03a0b3929d01bffafa3e3ecd4f7e3185eb94a953c3a8c9820a32db60bb`;
- radial: `10305053424`, digest `sha256:006a74d704115181b1e9815bcfdc1f17cd556e49b9b5f722470e8f6b6e83e976`;
- cT: `10305993667`, digest `sha256:803f16fd978fbf24e1363b9fa0e9c44e754d2d2d97ea6aafedf3268cf264e0a0`.

All parent status records reported build/default/permille/reference exit code 0. The existing analyzer nevertheless returned `FileNotFoundError` because it expects `<profile>_cl.dat` and `<profile>_pk.dat`, while this pinned hi_class output-root convention emits `<profile>_00_cl.dat` and `<profile>_00_pk.dat`.

## Allowed recovery
Analysis-only. Do not rebuild the provider and do not rerun a cosmology case. Download the three immutable parent artifacts, verify the expected `_00_cl.dat` and `_00_pk.dat` files exist, expose byte-identical copies under the analyzer's already-frozen logical names `<profile>_cl.dat` and `<profile>_pk.dat`, then apply the unchanged `verification/m30/k4_local_2d_precision.py` point and aggregate gates.

No physics, local points, precision profiles, observables, provider commit, thresholds, convergence rule, or classification rule may change.

## Fail closed
If an expected parent artifact/file is absent, a parent status code is nonzero, or the recovered byte copies differ from their `_00_` sources, classify recovery as blocked. Do not infer a numerical or physical failure.

## Scientific interpretation
Only the unchanged preregistered aggregate gate may promote K4. A green recovery workflow is not itself scientific PASS. `BLOCKED_IMPLEMENTATION`, path recovery failure, or missing files are not physical falsification.