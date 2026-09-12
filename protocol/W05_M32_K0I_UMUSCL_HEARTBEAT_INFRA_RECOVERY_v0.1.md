# W05 M32 K0i — umuscl hosted-infrastructure heartbeat recovery v0.1

Date: 2026-09-12
Model: M32 DGP / EFT-Ramses.
Provider: `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435`.

## Trigger
K0h terminal synthesis run `34710916271`, artifact `10303092426`, established `M32_K0H_NINE_HYDRO_TARGETS_COMPILED_UMUSCL_HOSTED_INFRASTRUCTURE_BLOCKED`: nine hydro-tail targets compile with exact pinned Intel settings, while `umuscl.o` repeatedly receives external hosted-runner shutdown / exit 143 during `ifx` and emits no compiler/source diagnostic.

## Frozen science/compiler contract
No source, Makefile, macro, numerical constant, optimization level, target, DGP parameter, or compiler flag may change.
- exact provider commit above;
- immutable stage-1 checkpoint artifact `10283774354`;
- Intel oneAPI `ifx` through `mpiifx`;
- `F90=mpiifx`;
- `FFLAGS=-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)`;
- exact target `umuscl.o`.

## Only allowed infrastructure changes
1. use GitHub hosted `ubuntu-22.04` instead of the repeatedly terminated `ubuntu-24.04` target attempt;
2. run the exact `make umuscl.o ...` command in background while the shell emits a timestamped heartbeat every 5 seconds; the compiler process, stdin, flags and files are untouched;
3. set `OMP_NUM_THREADS=1` only as a host resource-control environment variable; no OpenMP code generation flag is added.

Checkpoint extraction, exact-pin verification, mtime-only normalization and byte-hash integrity are unchanged.

## Frozen interpretation
- rc=0 and `umuscl.o` exists -> `M32_K0I_UMUSCL_COMPILED_EXACT_PIN_INFRA_RECOVERED`.
- explicit compiler/source diagnostic -> `M32_K0I_UMUSCL_COMPILER_OR_SOURCE_BLOCKED`.
- hosted shutdown / 143 / cancellation without compiler diagnostic -> `M32_K0I_UMUSCL_HOSTED_INFRASTRUCTURE_BLOCKED_PERSISTS`.
- checkpoint/provenance mismatch -> `M32_K0I_INTEGRITY_BLOCKED`.

No K0 promotion and no physical falsification are allowed. Successful `umuscl.o` compilation only authorizes a prospectively frozen remaining-object/link continuation using exact pinned build products.
