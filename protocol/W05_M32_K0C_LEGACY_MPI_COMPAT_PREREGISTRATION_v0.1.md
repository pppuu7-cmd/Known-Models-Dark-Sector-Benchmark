# W05 M32 K0c — legacy MPI compiler compatibility recovery preregistration v0.1

## Purpose
Continue build-only localization of the pinned EFT-Ramses DGP provider after K0b clean rebuild removed the stale tracked-module failure and exposed a legacy Fortran/MPI argument-rank mismatch in `amr/bisection.f90`.

## Frozen provider and build
- repository: `nat-woodcock/EFT-Ramses`
- commit: `849ddb716041316d0e223ba22badc0d630b72435`
- Ubuntu GNU gfortran + OpenMPI `mpif90`
- provider-native `bin/Makefile`
- serial `make`
- delete only `bin/*.o` and `bin/*.mod` before build, as in K0b

## Only new permitted intervention
Add GNU compiler compatibility flag:

```text
-fallow-argument-mismatch
```

to `FFLAGS` only. No source file, Makefile, DGP parameter, numerical constant, optimization level, or physics option may be changed.

## Rationale
K0b stderr is a compile-time legacy MPI calling-interface mismatch (scalar vs rank-1 actual arguments to `MPI_ALLREDUCE`). The compatibility flag changes compiler diagnostics/acceptance for legacy argument mismatch; it does not alter the model equations or benchmark physics.

## Frozen classification
- exact pin / DGP provenance failure -> `M32_K0C_BLOCKED_PROVENANCE`
- build remains nonzero or executable absent -> `M32_K0C_LEGACY_MPI_COMPAT_STILL_BLOCKED`
- clean build succeeds and native executable exists -> `M32_K0C_PROVIDER_BUILD_RECOVERED_WITH_GNU_LEGACY_COMPAT`

Even a recovered executable **does not promote K0**. K0 promotion requires a separate preregistered native DGP production execution with finite outputs and an appropriate reference/control.

No outcome is physical falsification of DGP.
