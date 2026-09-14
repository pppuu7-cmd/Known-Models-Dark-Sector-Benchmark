# M21 stage-3 exact-pin source-semantic audit — 2026-09-14

Provider authority: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540` (CLASS v3.3.4 commit).

Purpose: outcome-independent source audit while the prospectively frozen stage-3 matrix is running. This note does not alter any stage-3 lane, threshold, or interpretation ceiling.

## Exact reference profile

The pinned `cl_ref.pre` contains all G1A and G2B high-precision assignments used by the M21 decomposition, including:

- `recfast_Nz0=100000`
- `tol_thermo_integration=1.e-5`
- `recfast_x_He0_trigger_delta=0.01`
- `recfast_x_H0_trigger_delta=0.01`
- `l_logstep=1.026`
- `l_linstep=25`
- the G2B hyperspherical sampling/tolerance assignments through `hyper_flat_approximation_nu=1.e6`.

## Parser authority

At the exact pin, `input_read_precisions()` assigns defaults and parses precision inputs through macro expansion of `include/precisions.h`. Therefore a precision-file key absent from `precisions.h` is not a normal active precision field at this pin; it can remain an unused input entry rather than changing solver state.

## G1A semantic audit

Exact `include/precisions.h` defines:

- `tol_thermo_integration` with default `1.e-6`;
- `recfast_x_He0_trigger_delta` with default `0.05`, explicitly a smoothing factor for recombination approximation switching;
- `recfast_x_H0_trigger_delta` with default `0.05`, explicitly a smoothing factor for recombination approximation switching.

However, no `recfast_Nz0` precision parameter is present in the exact-pin `include/precisions.h`, despite the key being present in the pinned `cl_ref.pre`. A full-text check of the exact-pin `input.c` likewise finds no `recfast_Nz0` reader. Under the exact parser architecture this makes `recfast_Nz0` a legacy/unconsumed reference-profile entry, not an active precision control.

Prospective consequence only: stage-3 must still execute the frozen `G1A__recfast_Nz0` negative-control lane, but a scientific localization must not attribute G1A sufficiency to that key unless execution evidence contradicts this source audit through some separately identified consumption path.

## G2B semantic audit

Exact `include/precisions.h` confirms active precision fields and documents their numerical role:

- `l_linstep` default `40` and `l_logstep` default `1.12`: sampling of multipoles over which Bessel/transfer functions are evaluated;
- `hyper_sampling_flat` default `8.0`: flat-case sampling points per approximate wavelength;
- `hyper_sampling_curved_low_nu` default `7.0` and `hyper_sampling_curved_high_nu` default `3.0`: curved-case sampling density below/above the nu transition;
- `hyper_nu_sampling_step` default `1000.0`: transition nu between low/high curved sampling rules;
- `hyper_phi_min_abs` default `1.e-10`: small Bessel-function value used to determine the first x point;
- `hyper_x_tol` default `1.e-4`: tolerance used to determine the first x point;
- `hyper_flat_approximation_nu` default `4000.0`: nu boundary controlling the flat approximation for Bessel functions.

Thus G2B is genuinely a projection/Bessel/hyperspherical-sampling precision family at the exact pin, not a dark-matter-physics parameter family.

## Interpretation ceiling

This audit establishes source consumption/semantics only. It does not predict the numerical stage-3 classification, does not select a preferred parameter, does not authorize tuning, and does not promote K1/K3/K4. The prospectively frozen stage-3 aggregate remains authoritative for numerical sufficiency.
