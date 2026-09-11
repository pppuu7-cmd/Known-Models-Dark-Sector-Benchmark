# W04 M25 K1 support-order recovery preregistration v0.1

Status: **FROZEN BEFORE RECOVERY REANALYSIS**

## Motivation and scope

The first execution of the prospectively frozen M25 abundance-decoupling K1 test completed successfully at workflow run `34548988620`, but its analyzer inherited `metric()` from `verification/m21/mixed_cold_warm_k1_reference.py`. That metric uses `numpy.interp(x, xp, ...)` without first enforcing monotone increasing `xp`.

CLASS output tables are not guaranteed to share a common row-order convention. In particular, a background table may be emitted on a decreasing support coordinate. `numpy.interp` requires an increasing interpolation support. Therefore an order-dependent analysis failure can masquerade as a non-decoupling response.

This recovery is strictly a numerical-analysis repair. It does **not** alter the M25 physical coordinate, the provider products, CLASS pin, eta ladder, observables, gate thresholds, or scientific interpretation rules.

## Immutable upstream evidence

Use only the artifact produced by run `34548988620`:

- artifact name: `w04-m25-k1-abundance-decoupling`
- artifact id at preregistration time: `10180157389`
- physical cases and CLASS outputs: unchanged from the original run
- original preregistration: `protocol/W04_M25_RESONANT_STERILE_K1_ABUNDANCE_DECOUPLING_PREREGISTRATION_v0.1.md`

No CLASS recomputation is permitted in this recovery.

## Frozen mechanical repair

For every numeric output table used by the K1 metric:

1. retain all finite numeric rows exactly once;
2. sort rows by the first column in increasing order before interpolation;
3. require at least three rows and at least two numeric columns;
4. record the original support order as one of `strictly_increasing`, `strictly_decreasing`, `nonmonotonic`, or `degenerate`;
5. reject duplicate/degenerate interpolation support if it prevents a unique increasing coordinate.

No smoothing, clipping, rebinning, outlier deletion, precision change, observable deletion, or threshold relaxation is allowed.

## Frozen gate

Retain the original M25 K1 gate exactly:

- eta ladder: `0.10, 0.03, 0.01, 0.003, 0.001`;
- both pinned sterile-provider PSD shapes;
- blocks: H, P(k), CMB TT, CMB EE, CMB TE;
- for every block and every model:
  - p95 residual must be monotone toward eta -> 0 with the original 2% slack;
  - the smallest-eta residual must be lower than the largest-eta residual;
  - the log-log fit exponent over the three smallest eta values must be > 0.5.

All five blocks for both PSD shapes must pass for K1 promotion.

## Frozen classification

Allowed classifications:

- `M25_K1_ABUNDANCE_DECOUPLING_PASS_WITH_SCOPE_ORDER_RECOVERED`
- `M25_K1_ABUNDANCE_DECOUPLING_NOT_ESTABLISHED_ORDER_RECOVERED`
- `M25_K1_SUPPORT_ORDER_RECOVERY_BLOCKED`

A pass promotes only the same scoped abundance-to-zero mixed-CDM embedding limit as the original preregistration. A non-pass remains `physical_falsification = false`; it indicates that the strict K1 limit has not yet been numerically established and may motivate a separately preregistered precision-floor diagnostic.

## Audit comparison

The recovery result must store:

- original run id and artifact id;
- original classification;
- original support-order audit for every loaded table;
- recovered per-block metrics and pass flags;
- whether the recovered classification differs from the original solely because of support-order normalization.
