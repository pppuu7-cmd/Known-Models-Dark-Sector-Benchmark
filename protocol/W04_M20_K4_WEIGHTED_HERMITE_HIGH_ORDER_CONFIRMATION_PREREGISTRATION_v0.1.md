# W04 M20 / F20 SIDM K4 — weighted Hermite high-order confirmation preregistration v0.1

## Parent evidence
The prospective weighted-support recovery on `N_herm={13,17,21}` reduced the frozen unweighted high-order discrepancy from O(1) to O(1e-2), but did not satisfy its additional monotone-contraction clause: weighted max D was 0.014529410998643114 for 13->17 and 0.019693948085558 for 17->21. That parent classification is preserved and not relabelled.

## Question
Does the provider-weighted Hermite representation remain low-amplitude and settle under two new equal-order increments, or was the apparent recovery accidental/nonasymptotic?

## Frozen provider/physics/statistic
Same provider pin, physics, sigma/m cells and reference-CDM-weighted p95 statistic as `W04_M20_K4_WEIGHTED_HERMITE_SUPPORT_RECOVERY_PREREGISTRATION_v0.1.md`.

New equal-step orders only: `N_herm={21,25,29}`. No previously observed order is used to tune a threshold.

## Frozen classification
Let A=max weighted-summary symmetric discrepancy for 21->25 and B for 25->29 over the same 15 cells.

- `M20_K4_WEIGHTED_HIGH_ORDER_CONFIRMATION_PASS_DIAGNOSTIC` iff exact-zero integrity passes at all three orders, A<=0.10, B<=0.10 and B<=1.05*A.
- `M20_K4_WEIGHTED_HIGH_ORDER_LOW_AMPLITUDE_NONMONOTONE_DIAGNOSTIC` iff integrity passes and A<=0.10 and B<=0.10 but the contraction clause fails.
- otherwise `M20_K4_WEIGHTED_HIGH_ORDER_NONCONVERGENCE_PERSISTS_DIAGNOSTIC`.
- execution/nonfinite/shape/weight failure -> `M20_K4_WEIGHTED_HIGH_ORDER_EXECUTION_OR_INTEGRITY_BLOCKED`.

This remains confirmation evidence only: `K4_promoted=false`, `scientific_fail=false`, `physical_falsification=false` in every outcome. A later synthesis must also account for the independent dz axis and any additional numerical axes before K4 can be promoted.
