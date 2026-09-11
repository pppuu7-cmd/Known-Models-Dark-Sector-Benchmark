# W05 M32 DGP K0 MPI toolchain recovery v0.1

Date: 2026-09-11
Parent run: `34642254638`.
Parent classification: `M32_K0_BLOCKED_PROVIDER_BUILD`.

## First causal failure

The exact pinned provider was cloned and DGP/Vainshtein provenance checks passed, but the provider-documented `cd bin && make` stopped at its first compile command because `mpif90` was absent from the clean GitHub-hosted Ubuntu runner (`make: mpif90: No such file or directory`, exit 127 at the compiler invocation; make exit 2).

This is an infrastructure/toolchain defect, not a provider-physics failure and not a DGP physical failure.

## Frozen recovery

Repeat only the provider build/provenance probe with the same provider commit `849ddb716041316d0e223ba22badc0d630b72435` and the same unmodified `cd bin && make` command. Before cloning/building, install only the missing standard Fortran/MPI build toolchain from the runner distribution:

- `gfortran`
- `openmpi-bin`
- `libopenmpi-dev`

No provider source, Makefile, compiler flags, DGP equations, model parameters, scientific thresholds, or classification rules may be modified.

## Classification

The original frozen K0 classifications remain unchanged. A successful toolchain-recovered build may yield `M32_K0_PROVIDER_PROBE_PASS_WITH_SCOPE`; any subsequent build failure is localized to the next first causal provider/dependency/infrastructure defect and remains non-physical until demonstrated otherwise.
