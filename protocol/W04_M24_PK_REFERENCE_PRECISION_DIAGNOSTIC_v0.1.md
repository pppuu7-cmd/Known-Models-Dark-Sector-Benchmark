# W04 M24 ETHOS-1 P(k) reference-precision diagnostic v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION
Family: F24 / M24 ETHOS-like interacting dark sector
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Parent K1 result: `M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED`

## Purpose
The original exact-pin K1 ladder has an exact zero/omitted identity, but its P(k) response contracts only weakly from `a_idm_dr=60000` to `600`, with a shallow small-tail log slope. This diagnostic tests whether that apparent P(k) plateau is sensitive to the provider-shipped reference precision profile `pk_ref.pre`. It is a numerical localization gate only and cannot promote K1.

## Frozen physical configuration
Use exactly the parent ETHOS-1 physical configuration and source generator from `verification/m24/ethos1_k1_reference.py`, with no physical parameter changes. Execute only:
- `ref`: `a_idm_dr` omitted;
- `zero`: `a_idm_dr=0`;
- `top`: `a_idm_dr=60000 Mpc^-1` (parent `a0`);
- `tail`: `a_idm_dr=600 Mpc^-1` (parent `a4`).

The same four cases are executed under two numerical profiles:
1. `default`: no precision file;
2. `pk_ref`: the exact provider-shipped `pk_ref.pre` from the pinned CLASS commit.

No CLASS source, precision file, physical input, interpolation rule, response floor or threshold is edited.

## Frozen metrics and controls
For each profile:
- all four runs must exit 0 and emit finite P(k);
- `ref` versus `zero` normalized-L2 P(k) difference must be `<=1e-12`;
- compute normalized-L2 responses of `top` and `tail` relative to `zero` on positive common k support with the same log-k interpolation rule used by the parent K1 analyzer;
- require `top_R2 > 1e-6` before interpreting a contraction ratio;
- define `tail_over_top = tail_R2/top_R2`.

Cross-profile numerical sensitivity is additionally measured by normalized-L2 differences default-vs-`pk_ref` for `zero`, `top` and `tail`, on common positive k support. These are diagnostics only.

## Frozen classification
- `M24_PK_REF_CONTRACTION_RECOVERED_REQUIRES_FULL_LADDER_CONFIRMATION`: both profiles pass zero identity; `pk_ref` top response exceeds `1e-6`; `pk_ref tail_over_top <=0.25`.
- `M24_PK_PLATEAU_PERSISTS_REFERENCE_PRECISION`: both profiles pass zero identity; `pk_ref` top response exceeds `1e-6`; `pk_ref tail_over_top >0.25`; and the `pk_ref` ratio differs from the default ratio by at most 20% relative.
- `M24_PK_PLATEAU_PRECISION_SENSITIVE`: both profiles pass zero identity; `pk_ref` top response exceeds `1e-6`; `pk_ref tail_over_top >0.25`; and the ratio differs from default by more than 20% relative.
- `M24_PK_REFERENCE_PRECISION_CONTROL_BLOCKED`: either zero identity fails, required output is missing/nonfinite, or a provider run fails.

This diagnostic cannot promote K1. A recovered `<=0.25` ratio only authorizes a separately preregistered full five-point K1 confirmation under `pk_ref.pre`, using the original frozen K1 rule. All outcomes retain `physical_falsification=false` and do not exclude ETHOS or F24.
