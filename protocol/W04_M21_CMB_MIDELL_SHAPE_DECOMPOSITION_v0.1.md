# W04 M21 CMB mid-ell shape decomposition v0.1

Frozen: 2026-09-14 before shape decomposition of immutable M21 raw spectra.

Parent run/artifact: `34542162543` / `10178334419`, digest `sha256:640472f79c7e55d9edf4ed39ed35d4ab692fcf4700fad4d50edbad0642f7c65c`.
Parent localization: `M21_CMB_ELL_BAND_LOCALIZATION_PASS_WITH_SCOPE`, with TT/EE/TE all `MID_LOCALIZED` for both NDF15 and RK.

## Purpose

Determine whether the deterministic f_w=0.003 mid-ell anomaly is morphologically consistent with a low-rank CMB amplitude/peak-shift error or instead has a more complex shape. This is artifact-only and cannot change K1.

## Frozen data and band

Use only `ndf_out` and `rk_out` TT/EE/TE raw Cl arrays from the immutable artifact. Require identical ell grids. Analyze exactly `501 <= ell <= 1200`.

Fractions are fixed: f2=0.01, f3=0.003, f4=0.001.

## Frozen smooth-fraction subtraction

Construct the no-excursion interpolation at f3 linearly in the physical fraction coordinate:

`w = (0.003-0.001)/(0.01-0.001) = 2/9`;

`C_pred_f3 = C_f4 + w*(C_f2-C_f4)`.

Define the isolated anomaly vector

`A = C_f3 - C_pred_f3`.

This is a diagnostic interpolation only; it is not a physical theorem about mixed WDM response.

## Frozen templates

For each branch/channel on the fixed band:

1. amplitude template `T_amp = C_ref`;
2. shift template `T_shift = d C_ref / d ln ell`, using centered finite differences in the interior and one-sided differences at the two endpoints.

Normalize `T_amp` to unit norm. Orthogonalize `T_shift` against the normalized amplitude template by one Gram-Schmidt step, then normalize it. If either template norm is below `1e-300`, evidence is invalid.

Project anomaly A onto the two orthonormal templates.

Record:

- amplitude projection energy fraction `(A dot T_amp)^2 / ||A||^2`;
- shift projection energy fraction `(A dot T_shift_orth)^2 / ||A||^2`;
- two-template explained energy fraction = sum of those fractions;
- coefficient signs;
- normalized residual after removing both templates.

Also compute cosine similarity of the isolated anomaly vectors between RK and NDF15 for the same channel.

## Frozen categories

Per branch/channel:

- `AMPLITUDE_LIKE` if explained fraction >=0.80 and amplitude fraction >=0.70;
- `PEAK_SHIFT_LIKE` if explained fraction >=0.80 and shift fraction >=0.70;
- `LOW_RANK_MIXED` if explained fraction >=0.80 but neither single fraction reaches 0.70;
- `COMPLEX_SHAPE` otherwise.

Cross-solver morphology is `CONSISTENT` for a channel if categories match and anomaly cosine similarity >=0.995. Otherwise `BRANCH_DEPENDENT`.

## Controls

- reproduce the parent mid-band f3 excursion factors for TT/EE/TE within relative `1e-12` or absolute `1e-15`;
- verify interpolation weight exactly equals 2/9 in binary64 as recorded;
- anomaly norms finite and nonzero;
- no spectra outside the immutable parent artifact are used.

## Classification

All controls pass: `M21_CMB_MIDELL_SHAPE_DECOMPOSITION_PASS_WITH_SCOPE`.
Malformed/missing/inconsistent evidence: `M21_CMB_MIDELL_SHAPE_DECOMPOSITION_INVALID_EVIDENCE`.

## Interpretation ceiling

This diagnostic can motivate a later source/transfer/recombination numerical gate but cannot identify a unique implementation defect by itself. `K1_promoted=false`, `physical_falsification=false`.
