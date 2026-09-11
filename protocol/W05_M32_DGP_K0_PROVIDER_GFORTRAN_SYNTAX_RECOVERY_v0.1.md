# W05 M32 DGP K0 provider GNU-Fortran syntax recovery v0.1

Date: 2026-09-11
Family: M32 / F32 DGP braneworld.
Parent recovery evidence: run `34642361612` (canonical MPI-toolchain recovery; duplicate run evidence is non-authoritative).

## Causal localization

After installing the missing MPI/Fortran toolchain, the exact pinned provider build reaches `mpif90` but fails before model execution because the active Makefile flags are Intel-Fortran syntax (`-traceback -fpe0 -ftrapuv`) while the GitHub Ubuntu `mpif90` wrapper invokes GNU Fortran.

The pinned provider Makefile itself supplies a commented, explicit `MPI, gfortran syntax` configuration:

- `F90 = mpif90 -frecord-marker=4 -O3 -ffree-line-length-none -g -fbacktrace`
- `FFLAGS = -x f95-cpp-input $(DEFINES)`

Therefore this is a compiler-configuration/provider-build portability issue, not DGP physics.

## Frozen recovery

Pin `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435` exactly. Install only `gfortran`, `openmpi-bin`, `libopenmpi-dev`. Do not edit any provider source or Makefile. Invoke `make` with command-line overrides copied byte-for-byte in semantics from the provider's own commented MPI-gfortran configuration:

`make F90='mpif90 -frecord-marker=4 -O3 -ffree-line-length-none -g -fbacktrace' FFLAGS='-x f95-cpp-input $(DEFINES)'`

No model parameters, equations, cosmology, scientific thresholds, source files, or implementation logic may be changed.

## Frozen classification

- `M32_K0_PROVIDER_PROBE_PASS_WITH_SCOPE` iff exact pin and DGP/Vainshtein provenance are verified and this provider-native GNU MPI build exits zero.
- `M32_K0_BLOCKED_PROVIDER_BUILD` otherwise after localizing the first new causal build error.
- `M32_K0_BLOCKED_PROVENANCE` if exact pin/provenance fail.

Any PASS promotes only K0 with provider/build scope. It is not a DGP production cosmology calculation. K1-K9 remain open. Any build failure is not physical falsification.
