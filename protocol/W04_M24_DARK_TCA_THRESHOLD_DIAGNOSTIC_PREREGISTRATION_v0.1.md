# W04 M24 dark-TCA threshold diagnostic preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F24 / M24 ETHOS-like interacting dark sector
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Parent result: `M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED` from run 34542337424.

## Question
The parent K1 ladder had an isolated CMB excursion at `a_idm_dr = 6000 Mpc^-1`, while `a=0` exactly matched the omitted-coupling reference and the neighboring nonzero points were much smaller. Determine whether this excursion is controlled by the CLASS dark tight-coupling approximation (dark-TCA) switching thresholds. This is a numerical diagnostic only; it cannot promote K1 or physically falsify ETHOS.

## Frozen physical scope
Keep the parent ETHOS-1 realization unchanged in every profile:
- `f_idm = 1`
- `xi_idr = 0.5`
- `stat_f_idr = 0.875`
- `nindex_idm_dr = 4`
- `idr_nature = free_streaming`
- `alpha_idm_dr = 1.5`
- `b_idr = 0`
- same cosmological parameters, output request, gauge and CLASS pin as the parent run.

No physical parameter may change between numerical profiles. The diagnostic coupling set is frozen to `a_idm_dr = {0, 18000, 6000, 1800} Mpc^-1`, plus an omitted-coupling reference. The three finite points bracket the parent excursion and are sufficient to test localization without repeating the full parent ladder.

## Source-bound numerical switch
Pinned CLASS defines dark-TCA ON only if both
`tau_dmu_idm_dr/tau_h < idm_dr_tight_coupling_trigger_tau_c_over_tau_h`
and
`tau_dmu_idm_dr/tau_k < idm_dr_tight_coupling_trigger_tau_c_over_tau_k`,
with `n_index_idm_dr >= 2` and free-streaming IDR. Provider defaults are `tau_k=0.01`, `tau_h=0.015`.

Freeze three profiles:
1. `D_DEFAULT`: provider defaults `(0.01, 0.015)`; no precision override.
2. `E_EARLY_OFF`: `(0.003, 0.0045)`, making the TCA-ON condition stricter and ending dark-TCA earlier.
3. `O_TCA_OFF`: `(0, 0)`, which makes both strict `<` conditions false for positive timescales and therefore disables dark-TCA.

All other precision parameters remain provider-default. Do not simultaneously change `l_max_idr`, sampling, integrator, cosmology or ETHOS physics.

## Frozen measurements
For each profile and each nonzero coupling, compute normalized L2 response relative to the same-profile explicit-zero case in TT, EE, TE and linear P(k). Verify omitted-vs-explicit-zero identity separately.

Define the CMB excursion factor at 6000 as
`E_ch = R_ch(6000) / max(R_ch(18000), R_ch(1800), 1e-300)`
for TT, EE, TE and `Emax=max(E_TT,E_EE,E_TE)`.

Also record the direct profile-vs-default response for each case and channel. This distinguishes a moving numerical boundary from a global accuracy offset.

## Frozen diagnostic classification
Provider execution failure is `M24_DARK_TCA_DIAGNOSTIC_PROVIDER_BLOCKED`.

Otherwise:
- `M24_DARK_TCA_EXCURSION_LOCALIZED`: default has `Emax > 9`, TCA-off has `Emax <= 3`, and the 6000 CMB response in TCA-off is at least 5x smaller than in default in at least two of TT/EE/TE.
- `M24_DARK_TCA_EXCURSION_STRONGLY_SENSITIVE`: not localized, but TCA-off changes `Emax` by at least a factor 3 (up or down), or changes the 6000 response by at least 3x in at least two CMB channels.
- `M24_DARK_TCA_EXCURSION_INSENSITIVE`: neither criterion above; the excursion persists without strong TCA-threshold sensitivity.

The EARLY_OFF profile is diagnostic trajectory evidence and does not itself set the class.

## Scientific guardrails
- Always `K1_promoted = false` in this diagnostic.
- Always `physical_falsification = false`.
- Do not rewrite the parent K1 failure/non-establishment.
- If dark-TCA sensitivity is established, a separate prospective production K1 profile must be preregistered before any K1 promotion.
- If the excursion is insensitive, move to an independent approximation-boundary audit; do not tune physical ETHOS parameters to make continuity pass.
