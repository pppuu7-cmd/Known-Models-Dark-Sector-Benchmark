# W05 M32 K0k UMUSCL compiler-phase localization v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION

## Motivation

K0i on GitHub-hosted Ubuntu 22.04 and K0j on Ubuntu 24.04 both restore the same immutable checkpoint, enter a live Intel `ifx` compilation of the exact `umuscl.o` translation unit, and are then terminated by a runner-level shutdown with exit 143 before any explicit compiler/source diagnostic. K0j therefore weakens an image-specific explanation but does not distinguish preprocessing/front-end viability from optimization/code-generation sensitivity.

This is an infrastructure-only causal-localization diagnostic. It cannot establish scientific validity, physical failure, or canonical K0.

## Frozen inputs

Preserve exactly:
- provider `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435`;
- source translation unit `hydro/umuscl.f90` selected by the provider Makefile rule `%.o: %.f90`;
- provider compile-time macros `-DNVECTOR=64 -DNDIM=3 -DNPRE=8 -DNVAR=5 -DSOLVERhydro`;
- immutable stage-1 checkpoint artifact `10283774354` for all required `.o/.mod` dependencies;
- checkpoint byte-hash verification before/after mtime normalization;
- Intel oneAPI `ifx`/`mpiifx` compiler family;
- `OMP_NUM_THREADS=1`;
- GitHub-hosted `ubuntu-24.04` execution image.

No provider source or checkpoint bytes may be edited.

## Independent lanes

### Lane P — preprocessing only
Run the exact `umuscl.f90` source through Intel preprocessing with the frozen macro set and no compilation/code generation. Require a non-empty preprocessed output and rc=0.

This lane asks only whether source discovery + preprocessing is viable in the hosted environment.

### Lane O0 — low-optimization object compile
Restore the exact checkpoint and compile the exact `umuscl.o` target with the same compiler family and semantic/debug flags as K0j, but replace `-O3` with `-O0`:

`FFLAGS='-O0 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)'`

This intentional flag change is diagnostic-only and may not promote K0. It asks whether the hosted shutdown is sensitive to the optimization/code-generation workload.

## Frozen interpretation

For Lane P:
- rc=0 and non-empty preprocessed output -> `M32_K0K_PREPROCESS_PASS`;
- explicit source/preprocessor diagnostic -> `M32_K0K_PREPROCESS_SOURCE_BLOCKED`;
- hosted shutdown/cancellation/143 -> `M32_K0K_PREPROCESS_HOSTED_INFRA_BLOCKED`.

For Lane O0:
- rc=0 and `umuscl.o` exists -> `M32_K0K_O0_OBJECT_COMPILED_DIAGNOSTIC_ONLY`;
- explicit compiler/source diagnostic -> `M32_K0K_O0_COMPILER_OR_SOURCE_BLOCKED`;
- hosted shutdown/cancellation/143 without explicit compiler/source diagnostic -> `M32_K0K_O0_HOSTED_INFRASTRUCTURE_BLOCKED`.

Synthesis:
- P passes and O0 compiles while frozen O3 K0i/K0j remain hosted-blocked -> `M32_K0K_OPTIMIZATION_OR_CODEGEN_WORKLOAD_SENSITIVE`;
- P passes but O0 is also hosted-blocked -> `M32_K0K_COMPILE_STAGE_HOSTED_BLOCKER_PERSISTS_BELOW_O3`;
- P itself is blocked -> preprocessing/source-discovery infrastructure requires localization before any compile-stage inference.

Always: `K0_promoted=false`, `physical_falsification=false`, `scientific_fail=false`. A successful O0 diagnostic is not a substitute for the exact provider O3 target required by canonical K0.
