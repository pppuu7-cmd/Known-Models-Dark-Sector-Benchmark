# W05 M32 K0b — EFT-Ramses clean-build recovery preregistration v0.1

## Purpose
Localize the existing `M32_K0_BLOCKED_PROVIDER_BUILD` result without changing DGP physics, provider revision, compiler family, or benchmark semantics.

## Frozen provider
- repository: `nat-woodcock/EFT-Ramses`
- commit: `849ddb716041316d0e223ba22badc0d630b72435`
- toolchain: Ubuntu GNU `gfortran` + OpenMPI `mpif90`
- build invocation: provider-native `bin/Makefile`, serial `make`

## Pre-existing evidence
The pinned repository tracks precompiled `bin/*.o` and `bin/*.mod` artifacts, including `bin/amr_parameters.mod`. The preceding exact-pin GNU MPI build reads the tracked module and exits 2 with `Fatal Error: Reading module 'amr_parameters.mod' ... Unexpected EOF`.

## Only permitted intervention
After exact checkout, delete only tracked/generated Fortran build products in `bin/`:

```text
*.o
*.mod
```

No source (`*.f90`), Makefile, DGP parameter, numerical constant, or physics option may be changed.

## Frozen classification
- provenance failure -> `M32_K0B_BLOCKED_PROVENANCE`
- clean serial build exit != 0 -> `M32_K0B_CLEAN_BUILD_STILL_BLOCKED`
- clean serial build exit = 0 and native executable exists -> `M32_K0B_PROVIDER_BUILD_RECOVERED`

Even `PROVIDER_BUILD_RECOVERED` **does not promote K0**. A separate prospective production-DGP execution with finite model outputs/reference control is required for K0 promotion.

No outcome is a physical falsification of DGP.
