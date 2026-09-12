# W07 M31 immutable CMB ell-localization preregistration v0.1

Date: 2026-09-12
Model: M31 effective beyond-Horndeski in pinned hi_class
Purpose: analysis-only localization of the already-observed radial finite-difference nonconvergence inside the CMB TT response. This protocol cannot promote K2 and cannot establish physical family failure.

## Immutable inputs

Use only the already-computed raw artifacts:
- parent central stencil: run `34694420359`, artifact `10298453048`, radial h = 0.002 and 0.001;
- finer central stencil: run `34695461864`, artifact `10298900445`, radial h = 0.0005 and 0.00025;
- provider commit must be `0009f51d89e6465c79e570b496c66fc90058fa77` in both artifacts.

No new hi_class execution, k-cut change, tolerance change, interpolation change, step shrinking or retuning is authorized.

## Frozen TT localization

The shipped M31 `*_00_cl.dat` files contain one CMB response column, TT, over ell=2..2500. Evaluate radial central derivatives separately on these fixed ell bands:
- low: 2-30
- acoustic-low: 31-200
- acoustic-mid: 201-1000
- high: 1001-2500
- full: 2-2500

For each band compare adjacent immutable derivative scales:
- h=0.001 vs h=0.0005;
- h=0.0005 vs h=0.00025.

Normalize each derivative by the L2 norm of the base TT vector on that same band. Reuse the frozen convergence criterion: principal angle <= 5 degrees AND relative norm mismatch <= 0.25.

## Interpretation

Classify each ell band as converged only if both adjacent-scale comparisons pass. The global descriptive classification may state whether nonconvergence is low-ell localized, high-ell localized, multi-band, or not localized under these fixed bands.

Regardless of the outcome:
- `K2_promoted=false`;
- `physical_falsification=false`;
- `family_exclusion=false`.

This audit localizes an immutable numerical response phenomenon only; it does not authorize another step-size search.