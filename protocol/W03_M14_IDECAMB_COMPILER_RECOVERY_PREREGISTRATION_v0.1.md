# W03 M14 IDECAMB compiler-compatibility recovery v0.1

Date: 2026-09-10
Scope: infrastructure recovery only; no scientific promotion.

The frozen provider-control run `34452683017` reached the patched `camb/equations_ppfi.f90` and failed under GNU Fortran 13.3.0 because modern gfortran diagnoses legacy argument mismatches in calls to `dverk`. No cosmological execution occurred.

## Frozen recovery

Repeat the exact pins and literal overlay from `W03_M14_IDECAMB_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md`, changing only compiler flags by adding GNU Fortran's compatibility flag `-fallow-argument-mismatch` while retaining preprocessing, optimization, OpenMP and free-line-length support.

Frozen command-level flags:

`-cpp -O3 -ffast-math -ffree-line-length-none -fopenmp -fmax-errors=4 -fallow-argument-mismatch`

No Fortran source, ini parameter, likelihood setting or cosmological equation may be edited.

Classification:
- executable produced: `M14_IDECAMB_PROVIDER_BUILD_PASS_COMPAT_FLAG`;
- compilation still fails: `M14_IDECAMB_BLOCKED_BUILD_AFTER_COMPAT_FLAG`.

A successful compile authorizes only the next source/decoupling audit. It does not promote K1-K9.
