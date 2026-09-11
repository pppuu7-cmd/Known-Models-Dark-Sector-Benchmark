# W04 M23 K4 `cl_ref.pre` IDR-trigger compatibility repair v0.1

## Status
Prospectively frozen infrastructure/numerical-configuration repair. This document does **not** change the M23 cosmology, Gamma ladder, gauges, observable blocks, K3/K4 thresholds, or scientific classification rules frozen in `W04_M23_DM_DR_DAO_K4_CROSS_GAUGE_PRECISION_PREREGISTRATION_v0.1.md`.

## Trigger for this repair
The first M23 K4/cross-gauge batch reached CLASS successfully for the default and `cl_permille.pre` profiles, but every `cl_ref.pre` execution returned nonzero before scientific output. The pinned CLASS error states that `dark_radiation_trigger_tau_over_tau_k` equals `ur_fluid_trigger_tau_over_tau_k` and requires these approximation switches to differ. At the pinned provider commit, stock `cl_ref.pre` sets `ur_fluid_trigger_tau_over_tau_k = 50`, `ncdm_fluid_trigger_tau_over_tau_k = 51`, and `radiation_streaming_trigger_tau_over_tau_k = 240`, while it does not set a dedicated dark-radiation trigger.

This is classified as provider/precision execution incompatibility, not M23 K3/K4 scientific failure.

## Frozen minimal repair
For the **reference precision profile only**:

1. Copy the pinned provider file `cl_ref.pre` byte-for-byte to a run-local `m23_cl_ref_idr.pre`.
2. Append exactly:

   `dark_radiation_trigger_tau_over_tau_k = 49.`

3. Use that single `.pre` file in place of stock `cl_ref.pre` for all 14 case x gauge branches.

Rationale fixed before rerun: 49 is the immediately adjacent integer below the provider's UR trigger 50 and remains distinct from the provider reference-profile values 50 (UR), 51 (ncdm), and 240 (radiation streaming). No physical M23 parameter is changed. No frozen K3/K4 threshold is changed.

## Frozen unchanged science
- CLASS pin: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Cases: `ref`, `zero`, and the same five finite Gamma_0_nadm values.
- Gauges: synchronous and Newtonian.
- Precision ladder: default -> `cl_permille.pre` -> repaired reference profile derived only as above.
- Required common observables: TT, TE, EE, P(k).
- K4 fine threshold: `R_fine <= 1e-4`, with the previously frozen contraction rule.
- K3 numerical cross-gauge threshold: `R_gauge <= 1e-4` on common observables at reference precision.
- Missing/undefined outputs remain masked and block PASS; no zero imputation.
- `provider/infrastructure failure != physical failure` remains mandatory.

## Fail-closed interpretation
If the repaired reference profile still fails execution, M23 remains `K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED` and `K3_CROSS_GAUGE_NUMERICAL_NOT_ESTABLISHED`; inspect only the first causal provider/configuration failure and do not retune physical parameters or thresholds.

If execution succeeds, classify only with the already-frozen M23 K3/K4 metrics. A green workflow alone is not a PASS.
