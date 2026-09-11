# W05 M29 Brans-Dicke K1 GR-limit preregistration v0.1

Date: 2026-09-11
Family: F29 / M29 Brans-Dicke scalar-tensor gravity
Gate: K1 reference/GR limit
Provider: `hiclass-code/hi_class_public` pinned at `0009f51d89e6465c79e570b496c66fc90058fa77`
Prerequisite: W05 M29 K0 provider probe must be terminal `PASS_WITH_SCOPE`; otherwise this K1 gate is not authorized to run.

## Frozen physical path

Use the provider's native `gravity_model=brans_dicke` branch and shipped conventions. Preserve:

- `Omega_Lambda=0`, `Omega_fld=0`, `Omega_smg=-1`;
- `M2_tuning_smg=yes`, `M2_today_smg=1`;
- `phi_ini=1`, `phi_prime_ini=0` radiation-era-attractor convention;
- shipped early-time stability/reference settings;
- same common cosmological defaults in every arm.

Only `omega_BD` is changed. The finite ladder is:

`omega_BD = [1e2, 1e3, 1e4, 1e5]`.

The reference is a vanilla LCDM run from the exact same pinned hi_class executable with the same requested outputs. The physical GR reference is approached as `omega_BD -> infinity`; no finite point is declared mathematically identical a priori.

## Frozen observables

1. background H-like expansion column on the common background support;
2. CMB TT on common ell support;
3. linear matter P(k) at z=0 on common k support.

Undefined/non-common rows are masked, never zero-filled. Comparisons use symmetric relative error `2|x-y|/(|x|+|y|+floor)` with a channel-appropriate tiny numerical floor determined only by machine underflow scale, not data-dependent tuning.

For each channel record max relative error and RMS relative error. Also record adjacent-decade contraction of the RMS error.

## Frozen K1 acceptance

K1 is `PASS_WITH_SCOPE_BRANS_DICKE_GR_LIMIT` only if:

- every BD ladder arm and LCDM reference exits 0 and all compared samples are finite;
- final (`omega_BD=1e5`) max relative error is <= `5e-3` independently for background, TT and P(k);
- final RMS relative error is <= `1e-3` independently for all three channels;
- from `1e2 -> 1e3 -> 1e4`, RMS error contracts strictly in all three channels;
- the `1e5` point may be numerical-floor limited, but its RMS error must not exceed the `1e4` RMS error by more than 20% in any channel;
- at least the `omega_BD=1e2` point is distinguishable from LCDM (`max relative error > 1e-5`) in at least one channel, guarding against an inactive branch.

If only the final floor/nonmonotonicity condition fails while all runs remain finite, classify `K1_NOT_ESTABLISHED_NUMERICAL_FLOOR`, not physical failure. Provider/configuration failure is `BLOCKED_IMPLEMENTATION`. A nonconvergent finite ladder is not by itself physical falsification.

## Parallelization

The four BD ladder arms and LCDM reference are mutually independent and should run as a matrix with `fail-fast:false`. Aggregate/classification occurs only after the explicit barrier.

## Scope guard

Passing K1 establishes only the same-provider GR/reference limit along this frozen Brans-Dicke path. It does not establish K2-K9, observational viability, uniqueness, or a family-level preference/exclusion.