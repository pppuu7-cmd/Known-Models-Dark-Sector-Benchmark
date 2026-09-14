# W04 M21 l=400 late-source predicate compile recovery v0.1

Frozen: 2026-09-15 after run `34910039150` demonstrated a compile-only instrumentation blocker and before any recovered predicate execution.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Parent gate

The scientific contract remains `protocol/W04_M21_L400_LATE_SOURCE_PREDICATE_ULP_AUDIT_v0.1.md` unchanged.

The authoritative support-domain parent is `M21_L400_LOWER_U_SUPPORT_EXTENSION_DOMINANT_WITH_SCOPE` from run `34909263775`. No scientific value from the blocked predicate run is admissible.

## Observed blocker

Run `34910039150` reached the output-only patch build but did not begin CLASS science execution for the already-failed cases. `build.log` reports:

`source/transfer.c: ... error: 'ppr' was not declared in this scope`

The diagnostic had been inserted at the tail of `transfer_integrate()`, whose signature does not contain `struct precision *ppr`, while the diagnostic attempted to print `ppr->transfer_neglect_late_source`.

This is an instrumentation compile failure, not a provider execution result and not a scientific classification.

## Frozen recovery change

The only allowed source-instrumentation recovery is to keep the patch confined to exact `source/transfer.c` and add diagnostic-only read-only plumbing for the already-existing precision value:

1. add one file-local diagnostic scalar initialized to an invalid sentinel;
2. in `transfer_init()`, before the parallel q loop and only when `KMDSB_M21_L400_LATE_SOURCE_DIAG` is enabled, copy the actual runtime `ppr->transfer_neglect_late_source` into that diagnostic scalar;
3. at the existing tail diagnostic in `transfer_integrate()`, read that copied scalar instead of dereferencing nonexistent `ppr`;
4. require the diagnostic scalar to have been initialized when the diagnostic environment gate is active.

The copied scalar must never be read by native CLASS branch decisions and must never modify `ppr`, `ptr`, `ptw`, source arrays, grids, transfer values, return values, precision or execution order. It exists solely for output metadata.

No literal replacement of the runtime threshold is permitted even though the exact provider default is 400.0; the recovered diagnostic must report the actual runtime precision value.

## Unchanged scientific contract

All original frozen requirements remain unchanged:

- exact physical inputs and `P400_ON_TAIL_OFF` precision profile;
- exact provider pin;
- `OMP_NUM_THREADS=1`;
- same k support;
- null full-CMB L2 <= `1e-12` against clean recovery run `34907528331`;
- same diagnostic row schema;
- same q/k/endpoint integrity;
- same ULP reporting;
- same frozen predicate classification table.

The recovered workflow must compile the patched provider in preflight before launching case jobs. Any compile failure remains `BLOCKED` and cannot be interpreted scientifically.

## Claim ceiling

This recovery repairs diagnostic plumbing only. It does not alter or adjudicate the late-source predicate, does not establish a CLASS defect, does not promote K1/K3/K4, and cannot physically validate or falsify M21.
