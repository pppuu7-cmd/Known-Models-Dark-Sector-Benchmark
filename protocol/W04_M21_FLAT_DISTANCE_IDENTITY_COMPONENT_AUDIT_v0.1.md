# W04 M21 flat-distance identity component audit v0.1

Frozen: 2026-09-15 after terminal late-source predicate result `M21_L400_LATE_SOURCE_PREDICATE_ULP_SPLIT_LOCALIZED_WITH_SCOPE` and while the separately preregistered flat-identity predicate counterfactual is non-terminal, before any component-audit execution.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Purpose

Measure the two exact binary64 operands that form the provider's flat-universe `angular_rescaling` at recombination and determine the numerical identity residual without changing any physics or branch decision.

This gate is independent of whether the flat-identity predicate counterfactual is causal.

## Exact-source basis

On the exact pin, thermodynamics computes:

- `tau_rec` through `background_tau_of_z(pba,z_rec,...)`;
- `da_rec` through `background_at_z(pba,z_rec,long_info,...)`;
- `ra_rec = da_rec*(1+z_rec)`;
- `angular_rescaling = ra_rec/(conformal_age-tau_rec)`.

For `sgnK==0`, the stored background angular-distance column is constructed from `conformal_distance = conformal_age - tau_table[index]`, but `tau_rec` and `da_rec` at non-grid `z_rec` are obtained through distinct interpolation routes. This gate measures their binary64 residual.

## Frozen execution

Cases: `ref,f2,f3,f4` as four independent jobs.

For each case:

- exact existing physical input;
- exact `P400_ON_TAIL_OFF` precision profile;
- exact provider pin;
- no counterfactual and no provider state mutation;
- CLASS timeout 2700 s; job timeout 55 min;
- compare full `cl.dat` with immutable matching clean recovery case from run `34907528331`; normalized L2 must be <= `1e-12`.

## Output-only instrumentation

Patch only exact `source/thermodynamics.c`. Immediately after the native assignment

`pth->angular_rescaling=pth->ra_rec/(pba->conformal_age-pth->tau_rec);`

and only when `KMDSB_M21_FLAT_DISTANCE_IDENTITY_DIAG` is non-empty, append exactly one row containing at `%.17g` precision:

1. `pba->sgnK`
2. `z_rec`
3. `tau_rec`
4. `conformal_age`
5. `conformal_age - tau_rec`
6. `da_rec`
7. `ra_rec`
8. `ra_rec - (conformal_age-tau_rec)`
9. relative residual `(ra_rec-denominator)/denominator`
10. `angular_rescaling`
11. `angular_rescaling-1`.

The diagnostic must not change any provider value or execution order.

## Frozen analysis

Require all cases:

- exact provider pin;
- `sgnK==0`;
- one schema-clean row;
- CLASS rc=0;
- only `source/thermodynamics.c` modified;
- full-CMB null L2 <= `1e-12`.

Report for each case:

- exact components above;
- signed ULP distance of `ra_rec` from the denominator using ordered positive-double bit representations;
- signed ULP distance of `angular_rescaling` from `1.0`;
- consistency `abs(ra_rec/denominator-angular_rescaling) <= 0.5 ulp(angular_rescaling)`.

No fitted tolerance or response classifier is introduced.

Classification:

- all authority checks pass and the measured component ratio exactly reproduces the already-terminal signed angular-rescaling ULP pattern `{ref:-5,f2:-4,f3:+1,f4:-2}` -> `M21_FLAT_DISTANCE_INTERPOLATION_RESIDUAL_REPRODUCED_WITH_SCOPE`;
- authority clean but ULP pattern differs -> `M21_FLAT_DISTANCE_COMPONENT_PATTERN_MISMATCH_BLOCKED`;
- any integrity/null/provider failure -> `M21_FLAT_DISTANCE_COMPONENT_AUDIT_BLOCKED`.

## Claim ceiling

A reproduced component residual establishes the numerical origin of the `angular_rescaling` ULP split as the ratio of two independently interpolated representations of the same mathematical flat distance. It does not establish that either interpolator is individually inaccurate, does not establish a general CLASS defect, does not prescribe a production fix, and does not promote K1/K3/K4 or physically validate/falsify M21.