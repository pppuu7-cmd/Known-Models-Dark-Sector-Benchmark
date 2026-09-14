# W04 M21 CMB ell-band localization diagnostic v0.1

Frozen: 2026-09-14 before ell-band analysis of the immutable integrator-diagnostic artifact.

Family: F21 / M21 mixed cold+warm dark matter  
Parent result: `waves/wave_04_dark_matter/M21_INTEGRATOR_BRANCH_DIAGNOSTIC_RESULT.json`  
Parent run: `34542162543`  
Immutable artifact: `10178334419`, digest `sha256:640472f79c7e55d9edf4ed39ed35d4ab692fcf4700fad4d50edbad0642f7c65c`

## Purpose

The f_w=0.003 CMB excursion survives both NDF15 and RK while H and P(k) remain smooth. This artifact-only diagnostic asks where in multipole space the excess CMB residual norm is located. No CLASS rerun, parameter change, solver change, precision change or re-normalization is allowed.

## Frozen inputs

Use only the raw `*_cl.dat` files inside artifact `10178334419` for:

- branches: `ndf_out`, `rk_out`;
- cases: `ref`, `f2` (f_w=0.01), `f3` (f_w=0.003), `f4` (f_w=0.001);
- channels: TT column 1, EE column 2, TE column 3;
- require exactly identical ell grids within each branch for all four cases.

## Frozen ell bands

Use these non-overlapping fixed bands:

- `low`: 2 <= ell <= 29;
- `acoustic`: 30 <= ell <= 500;
- `mid`: 501 <= ell <= 1200;
- `damping`: 1201 <= ell <= 2500.

No band boundary may be moved after analysis.

## Frozen metrics

For each branch, case and channel define residual `d_ell = C_ell(case)-C_ell(ref)`.

For each band B:

`band_response_R2 = ||d_B||_2 / max(||C_ref,B||_2, 1e-300)`.

For f3 only define residual-energy share:

`energy_share_B = sum_B d_ell^2 / sum_{ell=2..2500} d_ell^2`.

For each band/channel/branch define excursion factor:

`E_B = R2(f3,B) / max(R2(f2,B), R2(f4,B), 1e-300)`.

Also compute direct RK-vs-NDF15 band R2 for `ref`, `f2`, `f3`, `f4`, using NDF15 as denominator reference.

## Frozen interpretation categories

For each branch/channel:

- `LOW_LOCALIZED` if low energy share >= 0.70;
- `ACOUSTIC_LOCALIZED` if acoustic share >= 0.70;
- `MID_LOCALIZED` if mid share >= 0.70;
- `DAMPING_LOCALIZED` if damping share >= 0.70;
- otherwise `BROAD_OR_MULTIBAND`.

Cross-branch localization is `CONSISTENT` for a channel if NDF15 and RK have the same category and the same largest-energy-share band. Otherwise it is `BRANCH_DEPENDENT`.

A band is called `STRONG_EXCURSION_BAND` only when `E_B >= 10` in both solver branches for the same channel. This threshold does not define K1 PASS/FAIL; it only marks where the already established excursion remains strongly isolated from f2/f4.

## Controls

1. Recompute the full 2<=ell<=2500 whole-vector normalized L2 for all branch/case/channel combinations and require agreement with the canonical integrator result to relative tolerance `1e-12` or absolute `1e-15`.
2. Residual-energy shares for f3 must sum to 1 within `1e-12` for each branch/channel.
3. Direct RK-vs-NDF15 full-vector metrics must reproduce the canonical result under the same tolerance.
4. The artifact digest/ID and parent run/head identities are recorded in the result.

## Classification

If all controls pass:

`M21_CMB_ELL_BAND_LOCALIZATION_PASS_WITH_SCOPE`.

Malformed/missing artifact or failed reproduction control:

`M21_CMB_ELL_BAND_LOCALIZATION_INVALID_EVIDENCE`.

This diagnostic does not choose a physical explanation by itself. The next gate should target the numerical/transfer layer corresponding to the observed localization pattern.

## Interpretation ceiling

`K1_promoted=false`, `physical_falsification=false`. This is localization of an already known numerical-response anomaly, not evidence for or against mixed warm dark matter physics.
