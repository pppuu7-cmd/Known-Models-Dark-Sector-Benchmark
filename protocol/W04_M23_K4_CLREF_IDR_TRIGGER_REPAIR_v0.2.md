# W04 M23 K4 `cl_ref.pre` IDR-trigger compatibility repair v0.2

## Status
Prospectively frozen infrastructure/numerical-configuration repair. This document supersedes only the *input-key spelling* of v0.1. It does **not** change the M23 cosmology, Gamma ladder, gauges, observable blocks, K3/K4 thresholds, or scientific classification rules frozen in `W04_M23_DM_DR_DAO_K4_CROSS_GAUGE_PRECISION_PREREGISTRATION_v0.1.md`.

## Evidence motivating this repair
The v0.1 rerun (`34592190477`) remained provider-blocked in all 14 branches. `default` and `cl_permille.pre` still exited 0, while the repaired reference profile exited 1 before scientific output with the same CLASS guard:

`idr_streaming_trigger_tau_over_tau_k == ur_fluid_trigger_tau_over_tau_k`.

The run artifact proves that v0.1 appended `dark_radiation_trigger_tau_over_tau_k = 49.` but the internal IDR precision value remained at the default 50.

Pinned CLASS source at `e85808324f51fc694d12e3ed7439552a3c3f9540` defines the actual precision field as

`idr_streaming_trigger_tau_over_tau_k`

in `include/precisions.h`. The provider error text refers to the same quantity using the legacy/descriptive phrase `dark_radiation_trigger_tau_over_tau_k`; that phrase is not the operative precision-field name in this pin.

Therefore v0.1 failed because the appended key did not set the field that the guard compares. This is a harness/configuration repair defect, not M23 K3/K4 scientific evidence.

## Frozen minimal repair v0.2
For the **reference precision profile only**:

1. Copy pinned provider `cl_ref.pre` byte-for-byte to run-local `m23_cl_ref_idr.pre`.
2. Append exactly:

   `idr_streaming_trigger_tau_over_tau_k = 49.`

3. Do not append or retain the ineffective v0.1 key `dark_radiation_trigger_tau_over_tau_k`.
4. Use this one repaired `.pre` file in place of stock `cl_ref.pre` for all 14 case x gauge branches.

The numerical value 49 is unchanged from v0.1 and remains prospectively fixed: it is adjacent to but distinct from the provider reference-profile UR trigger 50, ncdm trigger 51, and radiation-streaming trigger 240.

## Frozen unchanged science
- CLASS pin: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Cases: `ref`, `zero`, and the same five finite `Gamma_0_nadm` values.
- Gauges: synchronous and Newtonian.
- Precision ladder: default -> `cl_permille.pre` -> repaired reference profile.
- Required common observables: TT, TE, EE, P(k).
- K4 fine threshold: `R_fine <= 1e-4`, with the already-frozen contraction rule.
- K3 numerical cross-gauge threshold: `R_gauge <= 1e-4` on common observables at reference precision.
- Missing/undefined outputs mask and block PASS; no zero imputation.
- Provider/infrastructure/configuration failure is not physical failure.

## Fail-closed interpretation
If v0.2 still fails reference execution, keep `M23_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED` and `M23_K3_CROSS_GAUGE_NUMERICAL_NOT_ESTABLISHED`; inspect only the next first causal provider/configuration failure. Do not change M23 physics, Gamma values, gauges, precision thresholds, or classification thresholds.

If all reference executions succeed, apply only the original prospectively frozen K3/K4 metrics. A green workflow alone is not a scientific PASS.
