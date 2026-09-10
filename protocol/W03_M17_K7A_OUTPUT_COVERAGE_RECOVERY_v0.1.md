# W03 M17 K7a output-coverage recovery v0.1

## Status
Prospective output-plumbing recovery only. No HDE/CPL physics, provider pin, Planck operator, covariance metric, or scientific threshold is changed.

## Trigger
The first K7a run executed both HDE c=0.6 and frozen best-CPL theory cases successfully but `.theory_cl` stopped at ell=2500, while the frozen Planck-2018 Plik_lite operator needs complete TT/TE/EE input through ell=2508.

## Source localization
The pinned CosmoMC/IDECAMB configuration inherits `batch3/params_CMB_defaults.ini`, where `lmin_store_all_cmb = 2500`. CosmoMC documents this parameter as forcing storage/output of all CMB spectra only up to that multipole. K7a already requests `lmax_computed_cl = 2600`, so the calculation ceiling is not the identified blocker; the all-spectrum storage ceiling is.

## Frozen repair
For K7a cases only, override:

`lmin_store_all_cmb = 2600`

while retaining `lmax_computed_cl = 2600`, `use_nonlinear_lensing = F`, the same HDE/CPL coordinates, and all other case construction unchanged.

## Gate
- both cases must exit zero;
- `.theory_cl` must contain the existing four-column `L TT TE EE` contract and reach at least ell=2508;
- the previously validated Plik_lite 613-bin Fisher operator is then applied unchanged;
- any covariance value is reported without post-hoc success threshold; K7 remains partial until K7b nuisance/cosmological profiling.

This recovery cannot itself establish observational distinguishability or physical falsification.
