# M21 l=400 scalar-E transfer internal-path audit — 2026-09-15

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Written while transfer-convolution decomposition run `34906010762` is non-terminal. This audit is outcome-independent and does not use its scientific values.

## Perturbation source -> transfer source

For each transfer k, `transfer_interpolate_sources()` spline-interpolates the perturbation source along the perturbation-module k grid, independently at each perturbation tau. The interpolation is the standard cubic-spline expression using source values and precomputed source second derivatives.

For scalar CMB E, `transfer_sources()` leaves `redefine_source = FALSE`: CMB polarization is not among the branches that redefine the source by selection/window/background factors. Hence:

- `tau_size = ppt->tau_size`;
- `sources` is a plain copy of the already k-interpolated perturbation source;
- `tau0_minus_tau = tau0 - ppt->tau_sampling`;
- trapezoidal tau weights are computed on that coordinate.

Thus any source-profile anomaly found by the active decomposition would be downstream of the native perturbation source table specifically through the perturbation-source -> transfer-k interpolation step, not through an additional CMB-E tau resampling/window operation.

## Scalar-E radial path

For flat M21 (`Omega_k=0`), `transfer_radial_function()` selects the flat Bessel interpolation structure `pBIS`, with `HERMITE4` interpolation.

For `SCALAR_POLARISATION_E` it interpolates `Phi_l` and forms the radial kernel with the exact l-dependent prefactor

`sqrt(3/8*(l+2)*(l+1)*l*(l-1))/s2`

and `cscKgen^2 * Phi_l` (flat rescaling is unity).

## Convolution

`transfer_integrate()` determines the overlap with the Bessel support, computes the radial array, calls `array_trapezoidal_convolution(sources,radial,w_trapz,...)`, and applies an exact Bessel-edge triangle correction only when the convolution is truncated by the Bessel lower-support boundary.

The active diagnostic dumps these already-native arrays only after the final transfer value has been computed, and independently verifies reconstruction from `source*radial*w_trapz + edge_correction`.

## Mechanistic interpretation of the frozen classifier

- `...SOURCE_PROFILE_LOCALIZED...` -> first candidate layer is the transfer-k spline of the perturbation polarization source;
- `...RADIAL_KERNEL_LOCALIZED...` -> first candidate layer is the flat HERMITE4 Bessel/radial evaluation;
- `...SOURCE_AND_RADIAL_MIXED...` -> both profiles carry f3-specific response;
- `...SOURCE_RADIAL_INTERACTION...` -> neither profile alone is specific, but their pointwise product is;
- `...CONVOLUTION_ACCUMULATION...` -> specificity emerges only through weighted tau integration/cancellation.

These are numerical-path localizations only, not defect or physical-model verdicts.
