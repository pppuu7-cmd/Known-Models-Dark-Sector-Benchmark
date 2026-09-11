# W05 M32 K0f — checkpoint mtime recovery preregistration v0.1

## Purpose
Recover the already prospectively authorized provider-native Intel build after K0e exhausted four nominal checkpoint stages because a fresh exact-pin checkout assigns source files fresh mtimes while restored checkpoint `.o/.mod` files retain older mtimes. The stage-4 evidence shows identical `state_before` and `state_after` object inventories while `make` recompiles the build from its beginning and is interrupted at `umuscl.o`; therefore K0e did not test cumulative compilation as intended.

This is an infrastructure/checkpoint-plumbing correction only. It is not a new scientific model choice and no K0/K1+ conclusion follows from build success alone.

## Frozen parent evidence
- provider: `nat-woodcock/EFT-Ramses`
- provider commit: `849ddb716041316d0e223ba22badc0d630b72435`
- parent run: `34645828172`
- parent stage-4 artifact: `m32-k0e-stage4`, artifact id `10281849079`, digest `sha256:6df68fece20e6d2b8b1e6561bfa629b00109b074b7113bde34ec837334195c31`
- K0e classification: `M32_K0E_CHECKPOINT_BUDGET_EXHAUSTED`
- stage-4 first causal observation: restored object inventory is unchanged across the 25-second stage, while stdout recompiles the same early object sequence and stderr ends at intentional timeout/interrupt of `umuscl.o`.

## Frozen provider/build
Unchanged from K0e:
- Intel oneAPI `ifx` + Intel MPI `mpiifx`
- serial provider-native `make`
- `F90=mpiifx`
- `FFLAGS=-O3 -g -mcmodel=large -traceback -fpe0 -ftrapuv -cpp $(DEFINES)`
- exact same provider target and preprocessor configuration
- no source, Makefile, physics, DGP parameter, numerical constant, optimization, or target edits.

## Only allowed recovery change
After exact-pin checkout and extraction of the immutable parent/stage checkpoint:
1. verify exact provider pin;
2. hash every restored `.o/.mod` byte payload;
3. update **mtime only** of restored `.o/.mod` files so they are newer than the identical exact-pin source checkout;
4. re-hash and require byte-for-byte equality;
5. continue the same serial `make` for up to four sequential 25-second stages, carrying forward exact generated `.o/.mod/ramses3d` bytes between stages.

No object/module content may be edited. Mtime normalization is permitted only because source identity is fixed by the exact commit and the restored products were generated from that same commit with the same frozen compiler/flags.

## Frozen interpretation
- executable appears with build rc=0 -> `M32_K0F_PROVIDER_INTEL_BUILD_RECOVERED_MTIME_CHECKPOINTED`
- explicit compiler/linker non-timeout failure -> `M32_K0F_PROVIDER_INTEL_BUILD_STILL_BLOCKED`
- all four corrected stages end only by intentional timeout with no executable -> `M32_K0F_CHECKPOINT_BUDGET_EXHAUSTED`
- restored byte hashes change across mtime normalization -> `M32_K0F_CHECKPOINT_INTEGRITY_FAILURE`
- provenance/pin failure -> `M32_K0F_BLOCKED_PROVENANCE`

A recovered build does **not** by itself promote K0. A separate prospective native DGP runtime test with finite outputs and an explicit control/reference remains mandatory. No K0f outcome is physical falsification of DGP.
