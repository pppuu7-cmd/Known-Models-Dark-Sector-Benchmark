# W04 M26 DarkAges transfer-cache bypass recovery preregistration v0.1

Status: **FROZEN BEFORE EXECUTION**

## Trigger

M26 provider runtime recovery run `34550083757` established for all three PBH energy-injection children that:

- provider build succeeds;
- omitted-key baseline succeeds;
- provider-valid full-null case succeeds;
- only the finite PBH case fails.

The finite failure occurs in a later DarkAges subprocess during CLASS shooting. The first DarkAges invocation generates serialized transfer-function `.obj` cache files; a subsequent subprocess loads such a dump with `dill.load`, after which the provider's strict `isinstance(..., transfer)` check fails. This is a cache-serialization/runtime identity failure, not a PBH parameter failure.

The pinned DarkAges CLI itself already implements a `--nuke` path that removes generated `.obj` caches before importing `DarkAges`. Therefore cache invalidation is an intended provider maintenance operation.

## Immutable evidence reused

For each child, reuse baseline and provider-valid full-null numerical outputs from run `34550083757` and its corresponding immutable artifact:

- `m26-runtime-recovery-evaporation`
- `m26-runtime-recovery-spherical`
- `m26-runtime-recovery-disk`

Do not recompute baseline or null.

## Frozen repair

At pinned provider commit `7c4b26e50d240f1f45f120b623aab2dba13094fd`:

1. build only the executable target `class`, unchanged from prior recovery;
2. modify only `DarkAgesModule/bin/DarkAges` so that immediately before the first `from DarkAges...` import, generated files matching `transfer_functions/*.obj` are deleted;
3. do not delete or alter `transfer_functions/original/` tables;
4. do not delete model/interpolator caches outside `transfer_functions/`;
5. rerun only the finite physical case for each child.

This makes every automatically launched DarkAges subprocess reconstruct transfer objects from the immutable original text tables instead of loading the inter-process serialized cache.

No physical equation, transfer table, PBH parameter, cosmology, recombination mode, deposition mode, observable, threshold, or classification rule is changed.

## Parallel execution

The three finite children are independent because each matrix job has a separate checkout and filesystem:

- evaporation;
- spherical accretion;
- disk accretion.

Run these three jobs in parallel. There is only one finite CLASS process per child in this recovery.

## Frozen analysis

Combine:

- immutable baseline/null outputs from run `34550083757`;
- newly computed finite output from this recovery.

Run `verification/m26/m26_energy_injection_provider_control.py analyze` unchanged. The original provider-control thresholds and semantics remain frozen.

Allowed outcomes remain the original M26 provider-control classes. A scoped provider-control pass still means only provider operability + null semantics + resolved finite response. It does not promote K1, K4, or establish a family-level PBH verdict.

All outcomes retain `physical_falsification = false`.
