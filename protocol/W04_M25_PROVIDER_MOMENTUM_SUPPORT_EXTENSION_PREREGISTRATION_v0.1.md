# W04 M25 provider momentum-support extension preregistration v0.1

## Motivation

The preregistered M25 `pk_ref` precision diagnostic fails in CLASS `get_qsampling` at `tol_ncdm = 1e-10` even after increasing `_QUADRATURE_MAX_` and `_QUADRATURE_MAX_BG_` to 4000. CLASS explicitly reports that a file-interpolated PSD may require a wider q interval and/or higher input resolution.

The pinned sterile-dm provider itself defines `N_P_BINS = 1000` and `PTMAX_IN = 20 - 1e-5`. Therefore the next diagnostic must ask the physical provider to calculate a wider momentum tail rather than extrapolating the PSD downstream.

## Frozen provider

- Repository: `ntveem/sterile-dm`
- Commit: `e4486265e8207aa0dd28decc8c8d897266c0a52a`
- Stock reference evidence: M25 provider-control artifact from run `34544624039`
- Stock physics input: pinned repository `params.ini`, unchanged.

No sterile-neutrino mass, mixing angle, cosmology, rate table, redistribution table, ODE tolerance, or closure target may be changed.

## Two independent extension profiles

The following provider-grid profiles are frozen prospectively and SHOULD run in parallel:

1. `p30_n1500`
   - `PTMAX_IN = 30 - 1e-5`
   - `N_P_BINS = 1500`
   - `NMAX` unchanged.

2. `p40_n2000`
   - `PTMAX_IN = 40 - 1e-5`
   - `N_P_BINS = 2000`
   - `NMAX = 8192` only as storage capacity for the enlarged state vector.

Both profiles preserve approximately the stock momentum-bin spacing while extending the high-momentum support.

## Measurements

For both sterile-neutrino models in each profile, record:

- provider build/run status;
- closure density from `params.dat`;
- number of rows in `Snapshot100.dat`;
- final-temperature-normalized q minimum and maximum;
- q-support ratio versus the stock provider artifact;
- endpoint PSD-to-peak ratio for `f_nu + f_nubar`;
- overlap-shape normalized L2 difference after interpolation onto the stock q grid.

## Diagnostic classification

A profile is `M25_PROVIDER_MOMENTUM_SUPPORT_EXTENDED_WITH_STABLE_CLOSURE` when, for both models:

- provider build and execution succeed;
- generated snapshot is valid and non-negative;
- `abs(omega_wdm_h2 - 0.1188) <= 5e-4` (same stock provider-control closure tolerance);
- q maximum increases by at least 25% relative to stock;
- the endpoint PSD-to-peak ratio is lower than in stock.

Otherwise classify as `M25_PROVIDER_MOMENTUM_SUPPORT_EXTENSION_NOT_ESTABLISHED` or `...PROVIDER_BLOCKED` depending on execution status.

Overlap-shape L2 is diagnostic and is not used as a post-hoc acceptance knob.

## Scientific semantics

This test changes only provider numerical momentum support/capacity. It does not promote K1 or K4 and cannot constitute physical falsification. If one or both profiles establish wider support with stable closure, the next preregistered step may use that provider-computed tail in a downstream CLASS K1 precision recovery; no analytic/extrapolated tail is permitted before that result is known.
