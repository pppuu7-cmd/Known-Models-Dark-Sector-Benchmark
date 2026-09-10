# M20 self-interacting dark matter provider audit — 2026-09-11

## Scope
F20/M20 is response-distinct primarily through nonlinear halo/subhalo evolution. A linear Boltzmann-only realization would therefore be insufficient for this family. The first provider search is intentionally restricted to public source-bound implementations that expose a CDM/reference limit and nonlinear SIDM observables.

## Primary candidate: SASHIMI-SIDM
Repository: `shinichiroando/sashimi-si`

Pinned candidate commit:
`e17d3664dac677b604fd4ff02fb2af105a6937fa`

Repository authors: Shin'ichiro Ando, Shunichi Horigome, Ethan Nadler, Daneng Yang, Hai-Bo Yu.

Source-bound publications named by the provider:
- Ando et al., arXiv:2403.16633;
- Yang et al., arXiv:2305.16176.

The provider states that it computes semi-analytical SIDM subhalo catalogs and supports both velocity-independent and velocity-dependent scattering. This is an appropriate nonlinear response layer for F20, but not a replacement for a cosmological linear-perturbation provider.

### Reference-limit evidence already present upstream
At the pinned commit, `test_sashimi.py` contains an end-to-end physics regression named `test_sidm_reduces_to_cdm_when_the_cross_section_vanishes`. It runs a small catalog with `sigma0_m=1e-8` and requires SIDM `Vmax`, `rmax`, `rs`, and `rhos` to agree with their simultaneously returned CDM counterparts at relative tolerance `1e-3`, while the SIDM core radius must be below `1e-3 r_s`.

The same test suite also directly checks equation-level derivatives, the SIDM cross-section integral, NFW constants, cosmological growth derivatives, positivity/finite catalog outputs, and consistency of the effective cross section used by the evolution.

This upstream small-cross-section regression is strong K0/K1-scaffold evidence, but it is **not** by itself a KMDSB K1 promotion because:
1. it uses one tiny but nonzero cross section rather than a preregistered convergence ladder to zero;
2. its `1e-3` acceptance threshold was chosen upstream, not prospectively by KMDSB;
3. it tests a reduced catalog setup and a halo/subhalo response, not the later common-observation-space gate.

## Secondary candidates
Public SIDM codes also exist for spherical N-body/gravothermal evolution and analytic halo-profile evolution. They may become useful independent-provider checks, but they are not promoted here because the current primary candidate already supplies source-bound nonlinear observables plus an explicit CDM-return regression.

## Provider decision
`M20_PROVIDER_CANDIDATE_ACCEPTED_FOR_PROSPECTIVE_K1_NONLINEAR_HALO_TEST`

No K gate is promoted by this audit.

## Next prospectively allowed test
Freeze a KMDSB cross-section ladder at fixed host/catalog settings and compare the provider's simultaneous SIDM and CDM outputs in multiple nonlinear channels. The test should include at minimum `Vmax`, `rmax`, `rs`, `rhos`, core radius, subhalo weight/survival response, and a reference-limit slope/stability criterion. Any exact `sigma0_m=0` execution must first be tested as a provider-control case rather than assumed safe.
