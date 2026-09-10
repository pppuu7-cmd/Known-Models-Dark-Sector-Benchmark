# W03 M14 IDECAMB diagnostic-precision audit — preregistration v0.1

Frozen: 2026-09-10

## Motivation

The source-scaled K4 gate at beta={0,5e-8,1e-7} is terminal `M14_IDECAMB_K4_SOURCE_SCALED_FAIL`: norm mismatch 0.855% passes the 10% criterion, but direction angle 8.688 deg fails the frozen 3 deg criterion. That failure is immutable.

The same provider writes its background diagnostic `.quantity` through `write(1,'(11E15.5)')`, i.e. only about five significant decimal digits. At the source-scaled fine step, several measured channel changes are already O(1e-5--1e-4), so the direction metric can plausibly be limited by diagnostic serialization even when the solver state itself is smooth.

This audit tests that narrow measurement hypothesis before any Broyden/root-branch instrumentation.

## Allowed provider modification

Use the exact pinned overlay:
- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

Make exactly one diagnostic-only source edit after overlay and before build:

`write (1,'(11E15.5)') ...`

becomes

`write (1,'(11ES25.15E3)') ...`

in the author `test_output_root` quantity-output block.

No equation, parameter, initial condition, Broyden iteration, ODE tolerance, cosmological setting, or theory Cl output is changed. The source diff must be stored in the immutable artifact and must contain only this formatting replacement. This gate therefore measures output-resolution sensitivity, not a different physical implementation.

## Frozen physical grid and response

Reuse exactly the source-scaled grid and anchor:
- alpha_quint=0.02;
- beta={0,5e-8,1e-7};
- same theory-only execution route;
- same eight response channels and masks as `W03_M14_IDECAMB_SOURCE_SCALED_LOCAL_PREREGISTRATION_v0.1.md`.

No new beta point is introduced.

## Frozen K4 diagnostic criteria

Recompute the same tangent quantities with unchanged thresholds:
- relative norm mismatch <= 0.10;
- angle <= 3 deg.

This audit does **not** erase the original low-precision K4 FAIL.

Classifications:
- high-precision metrics pass: `DIAGNOSTIC_SERIALIZATION_LIMIT_CONFIRMED`; K4 scientific state becomes `PASS_WITH_SCOPE_HIGH_PRECISION_DIAGNOSTIC` for the source-scaled locality while retaining all low-precision/coarser FAIL records.
- high-precision angle still fails: `DIAGNOSTIC_SERIALIZATION_NOT_SUFFICIENT`; do not reduce beta further; proceed to shooting/branch continuity audit.
- build/run/diff validation failure: diagnostic audit BLOCKED only.

K5 may be scored only if high-precision K4 passes, using the same non-null floor 5e-5. No observational discrimination or family falsification is authorized.
