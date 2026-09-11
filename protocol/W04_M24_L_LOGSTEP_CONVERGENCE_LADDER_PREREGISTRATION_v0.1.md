# W04 M24 `l_logstep` convergence ladder preregistration v0.1

## Trigger

Run `34556010712` isolated the M24 CMB excursion to CLASS multipole logarithmic sampling: `l_logstep=1.026` alone changed `Emax` from about 62.645 to 0.823, while `l_linstep=25` alone only reduced it to about 8.77. The CLASS pinned provider default is `l_logstep=1.12`; the pinned `cl_ref.pre` value is 1.026.

This diagnostic tests whether the disappearance of the a_idm_dr=6000 excursion is a stable convergence trend in the `l_logstep` direction rather than a single-value accident.

## Frozen ladder

Use the exact pinned CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`, the same M24 physical cases and the same IDR compatibility setting `idr_streaming_trigger_tau_over_tau_k=49` on both branches.

Run these independent profile values in parallel:

`l_logstep = {1.10, 1.08, 1.06, 1.04, 1.03, 1.026, 1.02}`.

The control branch keeps the provider default `l_logstep=1.12`. No physical ETHOS parameter is retuned.

For every ladder value execute the same ten cases: control/profile x {ref, zero, a18k, a6k, a1p8k}. Preserve exact-zero identity.

## Frozen analysis

For each value reuse the existing M24 global numerical precision diagnostic and record profile `Emax`, channel excursion factors, direct profile/default a6k response ratios, exact-zero identity and provider status.

Aggregate diagnostics:

- `localized` at a value iff the existing frozen classifier returns `M24_GLOBAL_PRECISION_EXCURSION_LOCALIZED`;
- `first_localized_value`: largest tested `l_logstep` classified localized;
- `monotone_Emax_with_10pct_slack`: when ordered from coarse to fine sampling (1.10 -> ... -> 1.02), each next Emax must not exceed 1.10 times the previous Emax;
- `fine_pair_stability`: symmetric relative difference in Emax between 1.026 and 1.02 <= 0.25, provided both are localized.

This ladder does not promote K4 by itself. A stable ladder supports a numerical-sampling attribution and permits a later independent reproduction/observable-robustness gate. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
