# W04 M21 l=400 convolution signed-accumulation audit v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before its recovered classifier is known.

## Activation

Authorized only if the frozen successor router receives either:

- `M21_L400_TRANSFER_SPIKE_SOURCE_RADIAL_INTERACTION_WITH_SCOPE`; or
- `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`.

Otherwise skip without CLASS execution.

## Parent authority

Use only the clean recovered diagnostic from the exact provider `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540` and the immutable parent l=400 k-support weight `W_j`.

This gate is analysis-only. No CLASS rerun, source patch, precision change, grid change, or new physical case is authorized.

The clean parent diagnostic supplies, for every accepted q block and native tau index:

- source `S`;
- radial function `R`;
- trapezoidal weight `w`;
- signed native contribution `C=S*R*w`;
- final transfer value;
- Bessel-edge correction;
- `u=tau0-tau`.

The parent integrity gate already requires

`transfer_final = sum_i C_i + edge_correction`

to relative error <= `1e-10`.

## Frozen derived profiles

For each accepted q and each case `ref,f2,f3,f4` construct in the exact native integration order:

- `Wtau`: trapezoidal-weight profile `w_i`;
- `C`: signed weighted contribution `C_i`;
- `Q`: cumulative signed convolution `Q_n=sum_{i<=n} C_i`;
- `A`: cumulative absolute contribution `A_n=sum_{i<=n} |C_i|`.

For cross-case profile comparison, express profiles as functions of native `u=tau0-tau`, restrict to strict four-case overlap, and interpolate non-reference profiles linearly onto retained reference u nodes. Do not resample or reorder before forming the native cumulative sums.

For X in `{Wtau,C,Q}` use the same normalized L2 profile distance, immutable q support weighting and specificity ratio as the parent protocol:

`E_X=A_X(f3)/max(A_X(f2),A_X(f4),1e-300)`.

Reuse the established boundary `E>3`.

For the scalar Bessel-edge correction define the q-weighted RMS case difference from reference and the analogous specificity `E_edge`.

Also report, without changing classification, per-q cancellation factor

`kappa = sum_i |C_i| / max(|sum_i C_i + edge|,1e-300)`

for each case, plus f3-minus-neighbor excess quantiles in u for `|delta C|^2` and `|delta Q|^2`.

## Frozen classification priority

Apply in this order:

1. `E_edge>3` -> `M21_L400_CONVOLUTION_EDGE_CORRECTION_LOCALIZED_WITH_SCOPE`
2. else `E_Wtau>3` -> `M21_L400_CONVOLUTION_TRAPEZOID_WEIGHT_GEOMETRY_LOCALIZED_WITH_SCOPE`
3. else `E_C>3` -> `M21_L400_CONVOLUTION_WEIGHTED_POINTWISE_INTERACTION_LOCALIZED_WITH_SCOPE`
4. else `E_Q>3` -> `M21_L400_CONVOLUTION_SIGNED_CANCELLATION_LOCALIZED_WITH_SCOPE`
5. else -> `M21_L400_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE`

Any malformed block, lost reconstruction authority, q-set mismatch, insufficient common-u support, or non-finite derived profile -> `M21_L400_CONVOLUTION_SIGN_CANCELLATION_BLOCKED`.

## Claim ceiling

This is numerical mechanism localization only. It does not establish a CLASS defect, production integration/grid settings, a physical WDM scale, K1/K3/K4 promotion, or physical validation/falsification.
