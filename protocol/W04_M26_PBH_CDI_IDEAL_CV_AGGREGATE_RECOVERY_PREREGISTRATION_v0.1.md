# W04 M26 PBH-CDI ideal-CV aggregate recovery preregistration v0.1

## Trigger

Parent ideal-CV run `34626989657` completed all three independent mass analyzers successfully and uploaded their frozen `result.json` artifacts. The aggregate job then failed before reading the results because `verification/m26/pbh_cdi_ideal_cv_observability_proxy.py` imports NumPy at module import time and the aggregate runner did not install NumPy:

`ModuleNotFoundError: No module named 'numpy'`.

This is an aggregation-environment defect only. No parent spectrum, mass analysis, scientific metric, threshold, or classifier may be recomputed or changed in this recovery.

## Immutable child results

Source run: `34626989657`, head `0efcf5d59cea5dfc99f46b50849d5d2e628be1bf`.

Frozen analysis artifacts:

- `m26-ideal-cv-proxy-m100`: artifact id `10275235060`, digest `sha256:e7730e4f36e4a233373563f673b6bcdeb12bbb42770a86b7b514c85aa126f825`;
- `m26-ideal-cv-proxy-m1000`: artifact id `10275150217`, digest `sha256:e4d242526e797597760b0bad214de31636767a15692477b3652725fd8794621a`;
- `m26-ideal-cv-proxy-m10000`: artifact id `10274701188`, digest `sha256:4a6d6192845b9ee22c1f4c43c96cf43a4865de0cb53c831fc3ec243e7ed59bb9`.

The recovery must download these artifacts from run `34626989657`. It must not invoke CLASS, ExoCLASS, or the per-mass `analyze` subcommand.

## Frozen recovery action

1. Checkout the repository.
2. Install exactly `numpy==2.3.3`, solely to satisfy the analyzer module import.
3. Download the three immutable result artifacts from run `34626989657`.
4. Invoke the unchanged command:

`python3 verification/m26/pbh_cdi_ideal_cv_observability_proxy.py aggregate --collected collected --output summary.json`

5. Persist the resulting summary to the existing canonical wave/model paths.

No scientific criterion or result field may be modified after inspection of the child artifacts.

## Interpretation boundary

A successful recovery only restores the already-preregistered ideal full-sky noise-free CMB cosmic-variance proxy aggregate. The real observation/likelihood gate remains `OPEN`; no K1/K4 promotion and no physical falsification follows from this infrastructure recovery.
