# W04 M21 CLASS `cl_ref.pre` global-precision diagnostic preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F21 / M21 mixed cold+warm dark matter
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Parent evidence
The original M21 K1 ladder showed an isolated CMB excursion at warm fraction `f_w=0.003`. A dedicated P2 profile using `cl_permille.pre` plus the source-bound tight ncdm subset left the excursion intact. An independent integrator diagnostic then reproduced essentially the same `f_w=0.003` CMB response with both NDF15 and RK, so the effect is not localized to the default stiff integrator.

Canonical NDF15/P2 normalized-L2 excursion factors from the integrator diagnostic are frozen as the comparison baseline:
- TT: `67.5202694494654`
- EE: `211.58560557338748`
- TE: `323.42821108733295`
- `Emax = 323.42821108733295`.
The corresponding `f_w=0.003` responses are TT `6.876596406059055e-05`, EE `2.7773845469355833e-04`, TE `5.181261380722199e-04`.

## Question
Does the isolated CMB excursion persist under the provider's own comprehensive reference-precision preset `cl_ref.pre`, which tightens a broader set of perturbation/CMB sampling and approximation controls than the previously isolated ncdm precision changes?

This is a numerical-localization diagnostic only. It cannot promote K1 and cannot physically falsify mixed cold+warm dark matter.

## Frozen physics
Reuse `verification/m21/mixed_cold_warm_k1_reference.py` without modification. Run only:
- `ref` (`f_w=0`, no ncdm species),
- `f2` (`f_w=0.01`),
- `f3` (`f_w=0.003`),
- `f4` (`f_w=0.001`).

All cosmology, WDM mass `m_ncdm=3000 eV`, temperature ratio `T_ncdm=0.71611`, total dark-matter density, gauge and output requests remain exactly those of the parent M21 K1 test.

## Frozen numerical profile
Use the unmodified provider file `cl_ref.pre` from the pinned CLASS commit as the **only** `.pre` file. Verify its Git blob hash before execution:
`ccb86d11f72d9fa754b18dca40d23378b90c0699`.

Do not concatenate `m21_ncdm_tight.pre`, `cl_permille.pre`, or any local precision override. `cl_ref.pre` already defines the provider reference-precision profile and must be tested as a coherent preset.

## Frozen measurements
For TT, EE, TE and linear P(k), compute normalized L2 response of each finite fraction to `ref` over the exact/overlap grid used by the existing M21 diagnostics.

For each CMB channel define
`E_ch = R_ch(f=0.003) / max(R_ch(f=0.01), R_ch(f=0.001), 1e-300)`
and `Emax=max(E_TT,E_EE,E_TE)`.

Record direct ratios between `cl_ref` and the frozen P2/NDF15 parent values for `f=0.003` and for `Emax`.

## Frozen classification
Execution/build failure: `M21_CLREF_DIAGNOSTIC_PROVIDER_BLOCKED`.

Otherwise:
- `M21_CLREF_EXCURSION_LOCALIZED_TO_LOWER_PRECISION` if `Emax <= 3` **and** the `f=0.003` response is at least 5x smaller than P2 in at least two of TT/EE/TE.
- `M21_CLREF_EXCURSION_STRONGLY_REDUCED` if not localized, but either P2 `Emax / Emax_clref >= 3` or the `f=0.003` response is at least 3x smaller in at least two CMB channels.
- `M21_CLREF_EXCURSION_PERSISTS` otherwise.

P(k) is recorded as a control but does not set these CMB localization classes.

## Guardrails
- Always `K1_promoted=false`.
- Always `physical_falsification=false`.
- Preserve all earlier negative diagnostics.
- A localized/reduced result authorizes only a new prospective production-precision K1 protocol; it does not retroactively turn the old test into PASS.
- A persistent result sends M21 to a further approximation/source-boundary audit rather than to physical rejection.
