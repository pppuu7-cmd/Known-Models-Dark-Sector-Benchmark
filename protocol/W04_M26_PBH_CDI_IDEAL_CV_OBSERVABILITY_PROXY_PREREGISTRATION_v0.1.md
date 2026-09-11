# W04 M26 PBH-CDI ideal cosmic-variance observability proxy preregistration v0.1

## Trigger and scope

The frozen M26 PBH-CDI multi-observable gate established near-linear response scaling in TT, EE, TE and P(k) for masses 100, 1000 and 10000 Msun and PBH fractions {1, 0.1, 0.01, 0.001}. The canonical summary explicitly leaves the observation/likelihood gate open.

This follow-up reuses the immutable full spectra from parent Actions run `34555112732`; it does not rerun CLASS and does not alter the provider. The purpose is to quantify an **ideal full-sky, noise-free Gaussian CMB cosmic-variance upper-bound proxy**, not a survey likelihood or an observational exclusion.

## Immutable inputs

Parent run: `34555112732`, head `3b410cd24527c6cda1fcca1717f8c684f0afcf28`.

Artifacts:

- mass 100 Msun: `m26-pbh-cdi-cmb-m100`, artifact id `10182286505`, digest `sha256:2dca2fa66dfa9406e8608392472e4bc93ee76fb74b2fbfb4a37617c0aa858013`;
- mass 1000 Msun: `m26-pbh-cdi-cmb-m1000`, artifact id `10182275523`, digest `sha256:47d5a065efa824f4faa7c340cfcf92e8055b3fe7ad2cdaef4052af4674d2cbd3`;
- mass 10000 Msun: `m26-pbh-cdi-cmb-m10000`, artifact id `10182281166`, digest `sha256:21e84c5ee57643658bcebeed102666e4b4891878a526c4a3b37e784803ded9e3`.

For each artifact use `ref_00_cl.dat` as the adiabatic fiducial and `f0_00_cl.dat ... f3_00_cl.dat` as the four frozen PBH-fraction cases. Fractions are read from the artifact manifest and must equal `{1, 0.1, 0.01, 0.001}` in that order.

Use multipoles `2 <= ell <= 2500` and the TT/EE/TE columns only. Since all three spectra in a given ell carry the same D_ell = ell(ell+1)C_ell/(2pi) prefactor, the Fisher trace below is invariant to using the stored D_ell units.

## Frozen ideal-CV metric

For each ell construct the 2x2 T/E fiducial covariance matrix

`C_ell = [[TT_ref, TE_ref], [TE_ref, EE_ref]]`

and the signal perturbation

`DeltaC_ell = C_ell(case) - C_ell(ref)`.

The full-sky, noise-free Gaussian field-level signal-to-noise proxy is

`SNR^2 = sum_ell (2ell+1)/2 * Tr[(pinv(C_ell) DeltaC_ell)^2]`.

Use a symmetric Moore-Penrose inverse with `rcond=1e-12`. Record the number of multipoles requiring non-positive/ill-conditioned handling; if more than 5% of the requested multipoles are non-positive or non-finite, classify that mass as numerically blocked rather than interpreting its SNR.

Also record cumulative SNR contributions in frozen bands: 2--30, 31--500, 501--1500, 1501--2500.

## Frozen interpretation tiers

For every mass/fraction:

- `SNR < 1`: `BELOW_IDEAL_CV_1SIGMA`;
- `1 <= SNR < 5`: `IDEAL_CV_MARGINAL_1_TO_5SIGMA`;
- `SNR >= 5`: `IDEAL_CV_DETECTABLE_GE5SIGMA`.

Fit `log(SNR)` versus `log(PBH fraction)` over finite positive points. `fraction_scaling_pass=true` iff `|slope-1| <= 0.05`.

For each mass report the sampled fraction interval bracketing SNR=5 when present. Do not extrapolate a 5-sigma fraction outside the sampled interval; report only a one-sided bound.

Aggregate classification:

- `M26_PBH_CDI_IDEAL_CV_OBSERVABILITY_PROXY_ESTABLISHED` iff all three masses are numerically valid and pass the frozen SNR fraction-scaling criterion;
- `M26_PBH_CDI_IDEAL_CV_PROXY_NONLINEAR_OR_NUMERICALLY_UNRESOLVED` otherwise.

## Interpretation boundary

This proxy assumes full sky, no instrumental noise, no foregrounds, no lensing complications, fixed cosmological parameters and no nuisance/parameter degeneracies. It is therefore an optimistic theoretical upper bound on CMB distinguishability. It **does not close the observation/likelihood gate**, does not constitute a dataset constraint, does not promote K1/K4, and cannot physically falsify the PBH model.
