# W04 M26 PBH provider build recovery preregistration v0.1

Status: **FROZEN BEFORE RECOVERY EXECUTION**

## Trigger

The first parallel provider-control run `34549280581` produced `PROVIDER_EXECUTION_BLOCKED` for evaporation, spherical accretion and disk accretion before any physical case executed. The shared build status was return code 2.

The immutable evaporation build log shows that the ExoCLASS executable `class` was successfully linked. The non-zero `make` return occurred only afterward when the default `all` target attempted to build/install the optional Python wrapper `classy` and failed because `Cython` was absent from the runner environment.

The pinned provider Makefile defines `all: class libclass.a classy` and also exposes `class` as an independent target. The KMDSB provider-control harness invokes only `./class`; it does not import `classy`.

## Frozen mechanical repair

Repeat the same three child controls with all physical inputs and thresholds unchanged, but replace the build command

`make -C exoclass -j2`

with

`make -C exoclass -j2 class`

No provider source patch, compiler flag change, cosmological parameter change, PBH parameter change, threshold change, or observable change is permitted.

## Parallel execution

The three children remain independent matrix jobs:

- evaporation;
- spherical accretion;
- disk accretion.

Within each child, baseline/explicit-zero/finite cases may execute in parallel because they share no mutable solver state beyond read-only provider binaries; each writes a unique output root.

## Classification semantics

Use the original provider-control classifications from `W04_M26_PBH_ENERGY_INJECTION_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md` unchanged. Recovery metadata must record:

- original blocked run id `34549280581`;
- recovery preregistration path;
- build target `class`;
- `physical_falsification = false` unless and until a later physical gate explicitly permits such an interpretation.

A provider-reference-control pass remains only a scoped authorization for a later, separately preregistered multi-point K1 continuity/scaling ladder; it is not K1 promotion and not a family-level PBH verdict.
