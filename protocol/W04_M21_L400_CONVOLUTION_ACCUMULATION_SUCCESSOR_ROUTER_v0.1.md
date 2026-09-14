# W04 M21 l=400 convolution-accumulation successor router v0.1

Frozen: 2026-09-15 after terminal transfer-convolution recovery `34907528331`, while the first successor router `34908508458` is still non-terminal and before any convolution sign/cancellation result is known.

## Purpose

If and only if the first frozen router authorizes `CONVOLUTION_SIGN_CANCELLATION` and the corresponding analysis-only gate completes, map its terminal classification to exactly one next mechanism-localization family without post-hoc branch selection.

This router performs no CLASS execution and may inspect only the terminal aggregate artifact of the authorized convolution sign/cancellation gate.

## Frozen routing table

- `M21_L400_CONVOLUTION_EDGE_CORRECTION_LOCALIZED_WITH_SCOPE`
  -> `BESSEL_EDGE_TRIGGER_GEOMETRY`

- `M21_L400_CONVOLUTION_TRAPEZOID_WEIGHT_GEOMETRY_LOCALIZED_WITH_SCOPE`
  -> `TAU_WEIGHT_GRID_GEOMETRY`

- `M21_L400_CONVOLUTION_WEIGHTED_POINTWISE_INTERACTION_LOCALIZED_WITH_SCOPE`
  -> `SIGNED_CONTRIBUTION_FACTOR_DECOMPOSITION`

- `M21_L400_CONVOLUTION_SIGNED_CANCELLATION_LOCALIZED_WITH_SCOPE`
  -> `CUMULATIVE_ZERO_CROSSING_PHASE`

- `M21_L400_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE`
  -> `ACCUMULATION_WINDOW_LOCALIZATION`

- `M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED`
  -> no scientific successor; `DEBUG_ONLY`

- any `...NOT_AUTHORIZED` result -> no scientific successor; `ROUTER_PARENT_INCONSISTENT`

Unknown classifications -> `ROUTER_BLOCKED_UNKNOWN_PARENT_CLASS`.

## Successor meanings

`BESSEL_EDGE_TRIGGER_GEOMETRY` is analysis-only first: localize which q nodes carry edge correction, their `tau0_minus_tau_min_bessel`, correction sign/amplitude, and whether the f3 specificity is due to edge activation/deactivation or amplitude at common activation state.

`TAU_WEIGHT_GRID_GEOMETRY` is analysis-only first: compare native tau/u node counts, interval widths and trapezoidal weights on the immutable support, with no resampling-derived classification unless prospectively frozen.

`SIGNED_CONTRIBUTION_FACTOR_DECOMPOSITION` is analysis-only first: decompose the already-recorded signed contribution `C=S*R*w` into sign pattern versus absolute amplitude response, keeping source/radial/weight values immutable.

`CUMULATIVE_ZERO_CROSSING_PHASE` is analysis-only first: localize zero crossings, extrema and the u-phase at which the f3 cumulative signed curve departs from the neighbor envelope. It must not choose windows by looking at the terminal curve; any windows/quantiles used for classification require a separately frozen protocol.

`ACCUMULATION_WINDOW_LOCALIZATION` must use prospectively fixed fractional cumulative-contribution windows, not visually chosen tau intervals. A recommended future design is equal absolute-budget quantile bins frozen before inspecting per-bin case specificity.

## Claim ceiling

Routing and any downstream numerical-path localization do not establish a CLASS defect, production precision/integration settings, a physical WDM scale or resonance, K1/K3/K4 promotion, or physical validation/falsification.
