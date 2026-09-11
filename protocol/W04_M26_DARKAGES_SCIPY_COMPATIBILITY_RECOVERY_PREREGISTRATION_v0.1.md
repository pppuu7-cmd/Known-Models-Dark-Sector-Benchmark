# W04 M26 DarkAges SciPy compatibility recovery preregistration v0.1

## Trigger

The cacheless raw-transfer recovery removed serialized `.obj` transfer objects successfully, preserved raw transfer-table hashes, but all three finite PBH cases still exited non-zero. The finite log now fails before the physical recipe is evaluated with:

`ImportError: cannot import name 'trapz' from 'scipy.integrate'`

The pinned historical DarkAges source imports `scipy.integrate.trapz`; modern SciPy no longer exports that symbol.

## Frozen intervention

This recovery changes dependency compatibility only:

- ExoCLASS remains pinned to `7c4b26e50d240f1f45f120b623aab2dba13094fd`.
- Retain the already preregistered cacheless raw-transfer intervention: suppress only the two `transfer_dump(...)` cache writes and delete `.obj` files before finite execution.
- Pin `scipy==1.13.1`, the pre-removal API line that still provides `scipy.integrate.trapz`.
- Pin `numpy==2.2.6` to a version within SciPy 1.13.1's supported NumPy range.
- Do not edit DarkAges recipes, common.py, transfer tables, PBH parameters, cosmology, or scientific thresholds.

## Execution

Reuse the successful baseline and exact-null evidence from run `34550083757`. Recompute only the finite case for each independent child:

- evaporation;
- spherical;
- disk.

The three child recoveries SHOULD run concurrently with `fail-fast: false`.

Before executing CLASS, verify in Python that `from scipy.integrate import trapz` succeeds and record NumPy/SciPy versions.

## Decision rule

- Non-zero finite execution remains `PROVIDER_EXECUTION_BLOCKED` and is not physical falsification.
- Successful finite execution is passed to the unchanged M26 provider-control analyzer.
- This recovery alone cannot promote K1/K4 and cannot constitute physical falsification.
- No physical parameter or response threshold may be adjusted after seeing the result.
