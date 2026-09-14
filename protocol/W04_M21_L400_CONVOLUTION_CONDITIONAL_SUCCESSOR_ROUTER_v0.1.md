# W04 M21 l=400 convolution conditional successor router v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before any recovered source/radial/convolution classifier is known.

Provider remains `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Purpose

Route the already-frozen parent classification from `protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_v0.1.md` to the next mechanism-localization gate without post-hoc branch selection.

This router performs no CLASS execution and reads no individual case artifacts or partial values. It may read only the terminal aggregate artifact from recovery run `34907528331`.

## Frozen routing table

Parent classification -> authorized successor set:

- `M21_L400_TRANSFER_SPIKE_SOURCE_PROFILE_LOCALIZED_WITH_SCOPE`
  -> `SOURCE_FACTORIZATION`
- `M21_L400_TRANSFER_SPIKE_RADIAL_KERNEL_LOCALIZED_WITH_SCOPE`
  -> `RADIAL_KERNEL_GEOMETRY`
- `M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE`
  -> `SOURCE_FACTORIZATION`, `RADIAL_KERNEL_GEOMETRY` in parallel
- `M21_L400_TRANSFER_SPIKE_SOURCE_RADIAL_INTERACTION_WITH_SCOPE`
  -> `CONVOLUTION_SIGN_CANCELLATION`
- `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`
  -> `CONVOLUTION_SIGN_CANCELLATION`
- `M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED`
  -> no scientific successor; `DEBUG_ONLY`

Any unknown classification -> `ROUTER_BLOCKED_UNKNOWN_PARENT_CLASS` and no scientific successor.

## Source-factorization source authority

On the exact provider, scalar E transfer maps `index_tt_e` to perturbation source `index_tp_p`. The scalar polarization source is constructed as

`S_E(k,tau) = sqrt(6) * g(tau) * P(k,tau)`

where `g` is the visibility function and, outside RSA, scalar `P` is either the TCA expression proportional to photon shear or the full combination of polarization monopole/quadrupole and photon shear. This authority is used only to define the next gate; no source-factorization result is assumed by the router.

## Radial-kernel source authority

The exact transfer module maps scalar E to `SCALAR_POLARISATION_E`. In flat geometry the radial branch is determined by the hyperspherical/flat-Bessel interpolation at `x=k(tau0-tau)` and the fixed scalar-E multipole prefactor. The router assumes no radial result.

## Convolution branch authority

The parent protocol already dumps the native source, radial function, trapezoidal weight and signed contribution `source*radial*w_trapz`. Therefore interaction/accumulation successors must first be analysis-only on the clean recovered diagnostic and must not rerun CLASS unless that analysis itself ends BLOCKED.

## Claim ceiling

Routing does not promote K1/K3/K4, does not establish a CLASS defect or a production precision/threading recommendation, and does not constitute physical validation or falsification.
