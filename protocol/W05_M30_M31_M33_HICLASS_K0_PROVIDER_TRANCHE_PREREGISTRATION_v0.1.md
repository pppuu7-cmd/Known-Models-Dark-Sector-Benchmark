# W05 M30/M31/M33 hi_class K0 provider tranche preregistration v0.1

Date: 2026-09-11
Pinned provider: `hiclass-code/hi_class_public` commit `0009f51d89e6465c79e570b496c66fc90058fa77`.
Gate: K0 provenance/executability only.

## Frozen independent arms

All arms use the exact pinned executable and run in parallel with `fail-fast:false`.

### M30 — Horndeski/EFT-DE manifold representative

Start from shipped `gravity_models/propto_omega_bh.ini` and set only the beyond-Horndeski amplitude `c_H` to zero:

`parameters_smg = 1., 0.5, 0.2, 0., 0., 1.`

This is an executable Horndeski effective-alpha subspace on the provider's LCDM expansion prescription. Passing K0 proves only this representative/subspace, not exhaustive Horndeski coverage.

### M31 — beyond-Horndeski/DHOST representative

Use shipped `gravity_models/propto_omega_bh.ini` unchanged, including nonzero `c_H=0.3`, `kineticity_safe_smg=1e-2`, and `background_Nloga=40000`.

Separately preserve the provider's own warning in `gravity_models/glpv_galileon_4.ini`: the self-consistent covariant Galileon setup currently fails background shooting in this version and the shipped GLPV example uses `Omega_smg_debug`. Therefore a successful effective-alpha arm may only be classified `PASS_WITH_SCOPE_EFFECTIVE_BH_PARAMETERIZATION`; it cannot establish full covariant GLPV/DHOST closure.

### M33 — covariant Galileon

Use shipped `gravity_models/galileon_3.ini` cubic covariant Galileon example unchanged except output root. It is configured as self-consistent dark energy with `Omega_Lambda=0`, `Omega_fld=0`, `Omega_smg=-1` and requests `tCl,mPk` plus background output.

### Shared control

A minimal vanilla LCDM arm from the same pinned hi_class executable requests `tCl,mPk` and background output.

## Frozen K0 acceptance per model arm

- exact provider pin;
- exit code 0;
- finite non-empty TT, P(k), and background outputs;
- branch-active guard: max relative difference against same-provider LCDM > `1e-6` in TT or P(k).

If executable and active:

- M30 -> `M30_K0_PASS_WITH_SCOPE_HORNDESKI_EFFECTIVE_ALPHA_SUBSPACE`;
- M31 -> `M31_K0_PASS_WITH_SCOPE_EFFECTIVE_BH_PARAMETERIZATION_COVARIANT_GLPV_OPEN`;
- M33 -> `M33_K0_PASS_WITH_SCOPE_COVARIANT_CUBIC_GALILEON_PROVIDER`.

Build/runtime/output failure is provider/infrastructure blocking, never physical falsification. No K1-K9 promotion is authorized by this K0 tranche.