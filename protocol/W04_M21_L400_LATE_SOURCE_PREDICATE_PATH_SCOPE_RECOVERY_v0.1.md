# W04 M21 l=400 late-source predicate path-scope recovery v0.1

Frozen: 2026-09-15 after terminal run `34911245274` and before any recovered re-execution.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Parent scientific contract

The scientific contract remains `protocol/W04_M21_L400_LATE_SOURCE_PREDICATE_ULP_AUDIT_v0.1.md` unchanged, including all physics, precision, k-support, diagnostic schema, null threshold, ULP reporting and classification rules. The compile-only instrumentation recovery in `protocol/W04_M21_L400_LATE_SOURCE_PREDICATE_COMPILE_RECOVERY_v0.1.md` also remains unchanged.

## Observed blocker

Run `34911245274` passed exact-source patch/compile preflight. Each of the four independent CLASS executions reached the post-run authority check and then failed in the local `find_cl()` helper because the new-result lookup was rooted at `.` and used recursive search. Since the immutable parent artifact had been downloaded under `parent/`, the helper found two matching files for the same case, e.g. for f3:

- `output/f3_00_cl.dat`
- `parent/output/f3_00_cl.dat`

The same path-collision mechanism applies to the four matrix cases. This is a harness file-discovery blocker after CLASS execution, not a provider/scientific result.

## Frozen recovery change

The only allowed recovery change is to scope file discovery explicitly:

- new CLASS output: search only under `./output/`;
- immutable clean parent: search only under `<PARENT_ARTIFACT_DIR>/output/`.

No recursive search from repository root is permitted.

No provider source, physical input, precision value, l-grid, k support, diagnostic patch, thread control, timeout, CMB null threshold, predicate test, ULP metric, analyzer or classification rule may change.

## Required integrity

Every recovered case must still require:

- exact provider pin;
- CLASS rc=0;
- only `source/transfer.c` modified by the output-only diagnostic;
- `OMP_NUM_THREADS=1`;
- schema-clean diagnostic;
- normalized full-CMB L2 <= `1e-12` against the immutable matching case from run `34907528331`.

The aggregate must apply the already-frozen predicate/endpoint classifier unchanged.

## Claim ceiling

This recovery repairs harness path scoping only. It cannot establish or alter the late-source predicate mechanism, a CLASS defect, production precision guidance, K1/K3/K4 status, or physical validation/falsification.