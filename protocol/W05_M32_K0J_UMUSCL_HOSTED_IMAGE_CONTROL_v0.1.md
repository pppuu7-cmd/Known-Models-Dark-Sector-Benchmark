# W05 M32 K0j UMUSCL hosted-image control v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION

## Motivation
K0i twice reached a live `ifx` compilation of the exact `umuscl.o` target and then the Ubuntu-22.04 GitHub-hosted runner received an external shutdown signal, producing exit 143 without an explicit compiler/source diagnostic. This is infrastructure evidence, not a scientific failure.

## Frozen control
Change only the GitHub-hosted execution image from `ubuntu-22.04` to `ubuntu-24.04`. Preserve exactly:
- provider `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435`;
- immutable stage-1 checkpoint artifact `10283774354`;
- checkpoint byte-hash verification and mtime-only normalization;
- Intel oneAPI `ifx`/`mpiifx` family installed from the Intel repository;
- target `make umuscl.o`;
- `F90='mpiifx'`;
- `FFLAGS='-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)'`;
- `OMP_NUM_THREADS=1`.

No provider source, compiler flags, Makefile, checkpoint bytes, model parameter, or scientific criterion may be edited.

## Frozen interpretation
- rc=0 and `umuscl.o` exists -> `M32_K0J_UMUSCL_COMPILED_EXACT_PIN_HOST_IMAGE_RECOVERED`;
- explicit compiler/source diagnostic -> `M32_K0J_UMUSCL_COMPILER_OR_SOURCE_BLOCKED`;
- runner shutdown / cancellation / rc 143 without compiler diagnostic -> `M32_K0J_UMUSCL_HOSTED_INFRASTRUCTURE_BLOCKED_CROSS_IMAGE`.

Always `K0_promoted=false` until the object is successfully produced and the next preregistered provider build stage is completed. Always `physical_falsification=false`.
