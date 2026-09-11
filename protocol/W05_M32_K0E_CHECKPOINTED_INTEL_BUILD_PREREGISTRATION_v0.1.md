# W05 M32 K0e — checkpointed Intel provider build preregistration v0.1

## Purpose
Separate repeated hosted-runner shutdowns from EFT-Ramses build correctness without altering provider source, physics, compiler family, flags, or target. K0d twice installed Intel oneAPI successfully and entered native `mpiifx` compilation, then the GitHub hosted runner was externally terminated with signal 143 before any compiler fatal diagnostic.

## Frozen provider/build
- repository: `nat-woodcock/EFT-Ramses`
- commit: `849ddb716041316d0e223ba22badc0d630b72435`
- Intel oneAPI `ifx` + Intel MPI `mpiifx`
- serial provider-native `make`
- `F90=mpiifx`
- `FFLAGS=-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)`
- clean removal only of tracked/generated `bin/*.o`, `bin/*.mod`, `bin/ramses3d` before stage 1

## Only infrastructure intervention
Run the same serial build in up to four sequential hosted jobs. Each stage allows 25 seconds of `make`, interrupts it with SIGINT before the observed external runner-shutdown window, archives only generated `*.o`, `*.mod`, and `ramses3d`, and restores those exact build products into a fresh exact-pin checkout for the next stage.

No source, Makefile, preprocessor model define, DGP parameter, numerical constant, compiler flag, optimization level, or target changes are permitted.

## Frozen interpretation
- executable appears with build rc=0 -> `M32_K0E_PROVIDER_INTEL_BUILD_RECOVERED_CHECKPOINTED`
- explicit compiler/linker non-timeout failure -> `M32_K0E_PROVIDER_INTEL_BUILD_STILL_BLOCKED`
- all four stages end only by intentional timeout and no executable -> `M32_K0E_CHECKPOINT_BUDGET_EXHAUSTED`
- provenance/pin failure -> `M32_K0E_BLOCKED_PROVENANCE`

A recovered build **does not promote K0**. A separate prospective native DGP runtime test with finite outputs and an explicit control/reference remains mandatory.

No K0e outcome is physical falsification of DGP.
