# W04 M21 l=400 conditional convolution sign/cancellation audit v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before its recovered source/radial/convolution classification is known.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Authorization

This gate is executable only if the terminal artifact from `W04 M21 l400 convolution successor router v0.1` authorizes `CONVOLUTION_SIGN_CANCELLATION`.

It performs no CLASS execution. It may consume only the clean recovered case diagnostics from run `34907528331`, its terminal aggregate, and the immutable parent l=400 excess weights already frozen by the parent protocols.

If not authorized, skip without scientific output.

## Purpose

The parent diagnostic already records, for every valid `(case,q,tau)` row,

- source `S`;
- radial kernel `R`;
- trapezoidal weight `w`;
- signed native contribution `C = S R w`;
- final transfer value;
- optional Bessel-edge correction.

This gate tests whether the f3-specific transfer response is generated primarily by exceptional positive/negative cancellation or by a shifted cumulative signed-integration phase rather than by a large standalone source or radial profile.

## Parent integrity

Require all parent recovered integrity gates to pass unchanged, including exact provider identity, null C_l check, same q-index set, same-q k geometry, block reconstruction and consecutive tau rows.

Any failure -> `M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED`.

## Frozen per-q quantities

For each case c and valid q, using the native row order after sorting by `index_tau`, define:

`I(c,q) = sum_i C_i + edge_correction`

`B(c,q) = sum_i |C_i| + |edge_correction|`

`Q(c,q) = |I(c,q)| / max(B(c,q),1e-300)`

where smaller Q means stronger signed cancellation.

Also define positive and negative budgets:

`Pplus = sum max(C_i,0) + max(edge,0)`

`Pminus = sum max(-C_i,0) + max(-edge,0)`.

Define normalized cumulative signed curve on native u-order:

`F_j(c,q) = (sum_{i<=j} C_i) / max(B(c,q),1e-300)`.

The edge correction is appended only to the final cumulative point.

For cross-case cumulative comparison, use the same strict common-u interpolation rule as the parent source/radial analyzer: retain reference u nodes inside the four-case overlap and linearly interpolate other cumulative curves onto them.

## Frozen response metrics

Cancellation-ratio response:

`dQ(c,q) = Q(c,q) - Q(ref,q)`.

Support-weighted amplitude:

`A_Q(c) = sqrt(sum_q W_q dQ(c,q)^2 / sum_q W_q)`.

Specificity:

`E_Q = A_Q(f3) / max(A_Q(f2),A_Q(f4),1e-300)`.

Cumulative-profile response:

`D_F(c,q) = ||F_c-F_ref||_2 / max(||F_ref||_2,1e-300)`

on the frozen common-u grid, then

`A_F(c) = sqrt(sum_q W_q D_F(c,q)^2 / sum_q W_q)`

`E_F = A_F(f3) / max(A_F(f2),A_F(f4),1e-300)`.

Reuse the established specificity threshold `E > 3`; do not tune it.

Also report without affecting classification:

- `Q`, `Pplus`, `Pminus`, and `Pplus/Pminus` per case/q;
- count and u-locations of sign changes in C;
- per-q E_Q and E_F analogues;
- parent `E_P` and `E_C` values if present in the recovered aggregate;
- fraction of absolute contribution budget accumulated before the final 10%, 25%, 50% of native u-range.

## Frozen classification

- `E_Q > 3` -> `M21_L400_TRANSFER_SPIKE_SIGN_CANCELLATION_RATIO_LOCALIZED_WITH_SCOPE`;
- else if `E_F > 3` -> `M21_L400_TRANSFER_SPIKE_CUMULATIVE_SIGNED_PHASE_LOCALIZED_WITH_SCOPE`;
- else -> `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE`.

Any invalid/zero parent weight, malformed block, failed reconstruction, insufficient common-u support, or non-finite metric -> `M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED`.

## Interpretation ceiling

A positive localization identifies a numerical integration/cancellation mechanism inside the already-localized scalar-E transfer convolution. It does not establish a CLASS defect, a physical warm-dark-matter resonance or scale, a production precision recommendation, K1/K3/K4 promotion, or physical validation/falsification.
