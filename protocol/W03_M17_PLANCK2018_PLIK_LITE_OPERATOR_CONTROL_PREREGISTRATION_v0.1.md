# W03 / M17 — Planck 2018 Plik-lite observation-operator control preregistration v0.1

Date: 2026-09-11

## Purpose

Validate a branch-blind covariance/whitening operator before applying it to the M17 holographic-dark-energy K7/B5 observation-space test. This control **does not use M17 outputs** and cannot change any M17 scientific gate by itself.

## Frozen operator implementation

- repository: `heatherprince/planck-lite-py`
- commit: `2c0d0f67e59ce781654cf62dd7fb10757b0e60be`
- year: 2018
- spectra: `TTTEEE`
- low-ell replacement bins: disabled
- high-ell range: Plik-lite native range (`ell >= 30`)

The implementation states that its 2018 data files come from the Planck Legacy Archive and that the high-ell implementation follows public Planck Plik-lite.

## Frozen files

The following files at the pinned commit are part of the operator and must be hashed during execution:

- `data/planck2018_plik_lite/c_matrix_plik_v22.dat`
- `data/planck2018_plik_lite/cl_cmb_plik_v22.dat`
- `data/planck2018_plik_lite/blmin.dat`
- `data/planck2018_plik_lite/blmax.dat`
- `data/planck2018_plik_lite/bweight.dat`
- `planck_lite_py.py`

## Frozen structural checks

The control must verify:

1. TT bin count = 215.
2. TE bin count = 199.
3. EE bin count = 199.
4. total high-ell TTTEEE bins = 613.
5. covariance shape = `613 x 613`.
6. covariance is finite and symmetric after applying the same triangular symmetrization convention as the implementation.
7. covariance admits a Cholesky factorization (positive definite in the used coordinate set).
8. binning weights and bin boundaries are finite/integer as appropriate and cover the implementation’s declared ranges.

## Frozen numerical self-test

Use the implementation’s own bundled spectrum `data/Dl_planck2015fit.dat` and its documented 2018 high-ell TTTEEE expectation:

`loglike_expected = -291.33481235418026`

Pass threshold:

`abs(loglike_measured - loglike_expected) <= 1e-9`.

This is an operator implementation self-test only; the bundled spectrum’s filename does not make it an M17 cosmology.

## Classification

- all frozen checks pass -> `M17_PLIK_LITE_OPERATOR_CONTROL_PASS`
- pinned checkout/hash/read failure -> `M17_PLIK_LITE_OPERATOR_PROVENANCE_BLOCKED`
- structural covariance/binning failure -> `M17_PLIK_LITE_OPERATOR_STRUCTURE_FAIL`
- numerical self-test outside threshold -> `M17_PLIK_LITE_OPERATOR_NUMERICAL_FAIL`

## Scientific claim boundary

A PASS only authorizes preregistration of the subsequent M17 observation-space test. It does **not** establish M17 observational distinguishability, K7/B5, physical falsification, or novelty.
