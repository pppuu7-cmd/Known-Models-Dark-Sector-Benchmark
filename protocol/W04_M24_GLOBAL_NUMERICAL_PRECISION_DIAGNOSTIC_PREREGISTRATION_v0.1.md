# W04 M24 global numerical-precision diagnostic preregistration v0.1

## Motivation

The M24 ETHOS-like dark-sector K1 anomaly has survived two targeted numerical-boundary checks:

1. dark-sector tight-coupling threshold variation;
2. interacting-dark-radiation hierarchy depth variation through `l_max_idr = 70`.

A broader provider-defined precision stress test is therefore warranted before altering any physical ETHOS parameterization.

## Frozen physical cases

Provider: `lesgourg/class_public`

Pinned commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`

The physical cases are unchanged from the existing M24 diagnostics:

- omitted interaction reference;
- exact `a_idm_dr = 0` null;
- `a_idm_dr = 18000 Mpc^-1`;
- `a_idm_dr = 6000 Mpc^-1`;
- `a_idm_dr = 1800 Mpc^-1`.

All other cosmological and ETHOS-like parameters are inherited unchanged from `verification/m24/dark_tca_threshold_diagnostic.py`.

## Precision profiles

Two independent provider-supplied precision profiles are tested against the provider defaults:

- `cl_permille.pre` — intermediate high-precision CMB profile;
- `cl_ref.pre` — provider reference profile documented to stabilize CMB TT/EE at approximately the 0.01% level.

No line in either provider precision file may be edited for this diagnostic.

The two profile branches are independent and SHOULD run concurrently. Within each branch, all cases have unique output roots and MAY run concurrently as well.

## Measurements

For each profile and for its same-job provider-default control:

1. verify exact-null (`a_idm_dr=0`) versus omitted-interaction identity;
2. measure relative L2 responses in TT, EE, TE and P(k);
3. compute the existing M24 excursion factor for the middle point `a_idm_dr=6000` relative to the larger/smaller neighboring points;
4. compare the middle-point response and excursion factor directly between default and high-precision execution.

## Frozen diagnostic classification

For a tested precision profile:

- `...EXCURSION_LOCALIZED` if the default maximum CMB excursion factor is > 9, the high-precision maximum is <= 3, and at least two of TT/EE/TE middle-point responses fall by a factor >= 5.
- `...EXCURSION_STRONGLY_SENSITIVE` if the ratio of maximum excursion factors is >= 3, or at least two TT/EE/TE middle-point response ratios differ by a factor >= 3.
- `...EXCURSION_INSENSITIVE` otherwise, provided execution succeeds.
- `...PROVIDER_BLOCKED` if required provider runs fail.

This is diagnostic-only. It cannot by itself promote K1/K4 or constitute physical falsification.

## Interpretation rule

If both `cl_permille.pre` and `cl_ref.pre` leave the anomaly insensitive, generic CLASS numerical precision is disfavored as its source and the next M24 work should move to another physical/numerical boundary rather than further tightening precision.

If either profile localizes or strongly changes the excursion, subsequent work must isolate which precision sub-block is responsible before any physical interpretation.
