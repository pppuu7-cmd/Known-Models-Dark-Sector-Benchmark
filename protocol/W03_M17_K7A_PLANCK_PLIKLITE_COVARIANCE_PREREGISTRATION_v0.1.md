# W03 M17 K7a Planck-2018 Plik_lite covariance test — preregistration v0.1

## Purpose
Measure how much of the already-preregistered M17 `c=0.6` versus best-refined CPL separation survives projection into a real observational covariance metric.

This is **K7a only**. It is a covariance-weighted separation measurement at fixed cosmological/nuisance coordinates. It is not full observational distinguishability and cannot close K7 without subsequent nuisance/cosmological profiling (K7b).

## Frozen authority
K6 authority must be:
- `models/holographic_dark_energy/M17_C060_JOINT_CPL_K6_REFINEMENT_RESULT.json`;
- classification `M17_C060_K6_REFINEMENT_SURVIVOR`;
- best CPL `w0=-1.2498700663555409`, `wa=0.8082964747357178`.

## Theory provider
Use the same pinned M17 provider lineage as K6:
- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`;
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`.

Freeze:
- HDE: `WForm_CF=2`, `c_hde=0.6`, `beta_cf=0`, `Use_PPF=T`;
- CPL comparator: `WForm_CF=1`, `w0=-1.2498700663555409`, `w1=0.8082964747357178`, `beta_cf=0`, `Use_PPF=T`;
- all dataset likelihoods disabled during theory generation;
- nonlinear lensing disabled as in K6;
- `lmax_computed_cl=2600` so Planck TT bins through ell=2508 are covered.

## Observation operator
Pin `heatherprince/planck-lite-py@2c0d0f67e59ce781654cf62dd7fb10757b0e60be` and use its Planck-2018 high-l TTTEEE data only (`use_low_ell_bins=False`).

Frozen public inputs:
- 215 TT bins;
- 199 TE bins;
- 199 EE bins;
- full 613x613 covariance from `c_matrix_plik_v22.dat`;
- Planck bin weights/edges in `bweight.dat`, `blmin.dat`, `blmax.dat`.

The provider `.theory_cl` contract is `L TT TE EE`. Values are treated as `D_l = l(l+1)C_l/(2 pi)` in microK^2, matching the PlanckLitePy input contract. This contract must be validated by header plus finite rows through at least ell=2508 before the metric is evaluated.

## Frozen metric
Let `x_HDE` and `x_CPL` be the 613-dimensional Plik_lite binned theory vectors produced by the exact PlanckLitePy binning rules, in the order TT, TE, EE. Let `F=C^{-1}` be the public Plik_lite inverse covariance.

Define

`Delta = x_HDE - x_CPL`

and

`S_cov^2 = Delta^T F Delta`, `S_cov = sqrt(S_cov^2)`.

Also report TT-only, TE-only, EE-only quadratic contributions using the corresponding covariance principal blocks, and the full-vector Euclidean norm only as a diagnostic.

## No threshold / no K7 promotion
No significance threshold is frozen in this K7a test. The output is a measured covariance-weighted separation, not a binary discovery gate. Therefore the only successful classification is:

`M17_K7A_PLANCK_PLIKLITE_COVARIANCE_MEASURED`

provided all source, binning, covariance positive-definiteness and finite-output checks pass.

K7 remains `PARTIAL_COVARIANCE_WEIGHTING_ONLY` after K7a regardless of the numerical S_cov. K7b must profile at least amplitude/calibration and defensible cosmological nuisance directions before an observational distinguishability claim is eligible.

## Failure semantics
Any source, output, binning or covariance failure is `M17_K7A_OPERATOR_OR_OUTPUT_BLOCKED`. It is not physical falsification of HDE and does not alter K6.
