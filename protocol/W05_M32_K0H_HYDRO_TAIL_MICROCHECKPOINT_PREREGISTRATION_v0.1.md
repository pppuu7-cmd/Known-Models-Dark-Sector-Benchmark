# W05 M32 K0h — hydro-tail microcheckpoint recovery preregistration v0.1

Date: 2026-09-12
Model: M32 DGP provider build infrastructure recovery.
Provider: `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435`.
Immutable parent: K0f stage-1 artifact `10283774354` from run `34647841987`.

## Purpose
The immutable K0f stage-1 checkpoint contains the complete MODOBJ layer, the completed AMR object prefix, and the hydro prefix through `uplmde.o`. Its build stdout shows that the next target begun by the exact provider Makefile was `umuscl.o`. Later hosted attempts were externally terminated while `ifx` was active and did not emit a compiler/source diagnostic. This gate changes only infrastructure granularity: compile the remaining hydro-tail objects as short independent target jobs from the same immutable checkpoint.

## Frozen compiler and source
No science, source, Makefile, preprocessor, optimization or numerical setting may change.
- exact provider commit: `849ddb716041316d0e223ba22badc0d630b72435`
- Intel oneAPI `ifx` through Intel MPI `mpiifx`
- `F90=mpiifx`
- `FFLAGS=-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)`
- provider `NVECTOR=64 NDIM=3 NPRE=8 NVAR=5 SOLVER=hydro`

## Immutable checkpoint integrity
Every matrix job must download artifact `10283774354`, extract `checkpoint.tar`, verify the provider pin, hash all restored `.o/.mod` files, touch mtime only so exact-pin sources are older than the immutable products, rehash and require byte-for-byte equality before compiling its target.

## Frozen target set
The exact provider HYDROOBJ order after the completed `uplmde.o` prefix is:
1. `umuscl.o`
2. `interpol_hydro.o`
3. `godunov_utils.o`
4. `condinit.o`
5. `hydro_flag.o`
6. `hydro_boundary.o`
7. `boundana.o`
8. `read_hydro_params.o`
9. `synchro_hydro_fine.o`
10. `gas_analytics.o`

Each target is compiled independently from the same immutable stage-1 module/object checkpoint. The matrix is `fail-fast:false`. No failed target is replaced, patched or skipped after viewing results.

## Frozen per-target interpretation
- rc=0 and requested `.o` exists -> `TARGET_COMPILED_EXACT_PIN`.
- explicit `ifx`/source/module/compiler diagnostic -> `TARGET_COMPILER_OR_SOURCE_BLOCKED` (infrastructure/implementation evidence only).
- runner shutdown, exit 143, timeout, cancellation or missing terminal compiler diagnostic -> `TARGET_HOSTED_INFRASTRUCTURE_BLOCKED`.
- checkpoint hash mismatch or provider pin mismatch -> `TARGET_INTEGRITY_BLOCKED`.

The aggregate is diagnostic only. Even all ten targets compiling does **not** promote K0 and does not establish a working DGP executable. Subsequent Poisson/PM/ramses/link and then a prospectively frozen native DGP runtime plus explicit reference/control remain mandatory. No outcome here is physical falsification of DGP.
