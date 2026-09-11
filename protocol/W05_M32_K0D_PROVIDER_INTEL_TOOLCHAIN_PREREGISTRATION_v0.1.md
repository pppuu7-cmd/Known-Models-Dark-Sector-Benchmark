# W05 M32 K0d — provider-intended Intel toolchain recovery preregistration v0.1

## Purpose
Test whether the pinned EFT-Ramses DGP provider builds under the compiler family implied by its active COSMA Makefile configuration, after GNU recovery work established that the remaining failures are portability/compiler-language issues rather than DGP physics.

## Frozen provider
- repository: `nat-woodcock/EFT-Ramses`
- commit: `849ddb716041316d0e223ba22badc0d630b72435`
- delete only tracked/generated `bin/*.o` and `bin/*.mod` before building
- serial provider-native `make`

## Provider-toolchain evidence
At the exact pin, `bin/Makefile` has an active `F90 = mpif90` COSMA block with Intel-style flags:

```text
-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)
```

The same Makefile lists an explicit MPI-ifort syntax block. Current Intel oneAPI replaces retired `ifort` with `ifx`; Intel MPI supplies the `mpiifx` wrapper. The recovery therefore uses current Intel `mpiifx` with the provider's active Intel-style flags, without modifying source or model settings.

## Frozen environment intervention
Install from Intel's official oneAPI APT repository:
- `intel-oneapi-compiler-fortran`
- `intel-oneapi-mpi-devel`

Source `/opt/intel/oneapi/setvars.sh`, record exact package/compiler/MPI versions, and build with:

```text
F90 = mpiifx
FFLAGS = -O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)
```

No source file, DGP parameter, Makefile content, numerical constant, preprocessor model define, or optimization setting may be edited.

## Frozen classification
- exact pin / DGP provenance failure -> `M32_K0D_BLOCKED_PROVENANCE`
- Intel toolchain unavailable/install failure -> `M32_K0D_BLOCKED_TOOLCHAIN_INSTALL`
- build nonzero or executable absent -> `M32_K0D_PROVIDER_INTEL_BUILD_STILL_BLOCKED`
- clean build exit 0 and `ramses3d` executable present -> `M32_K0D_PROVIDER_INTEL_BUILD_RECOVERED`

Even `PROVIDER_INTEL_BUILD_RECOVERED` does **not** promote K0. A separate preregistered native DGP production execution with finite native outputs and an explicit control/reference remains mandatory.

No outcome constitutes physical falsification of DGP.
