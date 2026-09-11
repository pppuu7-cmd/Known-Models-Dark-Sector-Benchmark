# W04 M24 IDR hierarchy-depth diagnostic preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F24 / M24 ETHOS-like interacting dark sector
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Parent K1 result: run `34542337424`, `M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED`
Parent dark-TCA diagnostic: run `34544375473`, result commit `4aea51cf5061f002b817cc1357f86abd13923e36`, `M24_DARK_TCA_EXCURSION_INSENSITIVE`

## Question
The isolated CMB excursion at `a_idm_dr=6000 Mpc^-1` persists when the dark tight-coupling approximation is ended early or disabled. Test the next independent source-bound numerical hypothesis: truncation depth of the free-streaming interacting-dark-radiation Boltzmann hierarchy.

Pinned CLASS sets `l_max_idr=17` by default for interacting dark radiation. The same pinned precision source sets `idr_streaming_approximation=rsa_idr_none`, so this diagnostic isolates hierarchy depth rather than a late-time IDR streaming approximation.

This is a numerical diagnostic only. It cannot promote K1 and cannot physically falsify ETHOS.

## Frozen physical scope
Keep the ETHOS-1 realization and cosmology exactly as in the parent/TCA diagnostic:
- `f_idm=1`
- `xi_idr=0.5`
- `stat_f_idr=0.875`
- `nindex_idm_dr=4`
- `idr_nature=free_streaming`
- `alpha_idm_dr=1.5`
- `b_idr=0`
- same cosmology, output request, gauge, CLASS pin and all other precision settings.

Freeze the same coupling cases:
- omitted-coupling reference;
- explicit `a_idm_dr=0`;
- `a_idm_dr={18000,6000,1800} Mpc^-1`.

Do not change dark-TCA thresholds in this diagnostic; use provider defaults throughout.

## Frozen hierarchy profiles
1. `D_L17`: provider default `l_max_idr=17` (no override).
2. `L35`: only `l_max_idr=35`.
3. `L70`: only `l_max_idr=70`.

No CMB sampling, k sampling, integrator, l_max_ur, photon hierarchy, cosmology, or ETHOS physical parameter may change between profiles.

## Frozen measurements
For every profile:
- verify omitted-coupling vs explicit-zero identity in TT, EE, TE, and linear P(k);
- compute normalized L2 response of each finite coupling relative to same-profile zero;
- for TT/EE/TE define excursion factor at 6000:
  `E_ch = R_ch(6000)/max(R_ch(18000),R_ch(1800),1e-300)`;
- `Emax=max(E_TT,E_EE,E_TE)`;
- record direct L35-vs-L17 and L70-vs-L17 changes for every case/channel.

## Frozen diagnostic classification
Provider execution failure: `M24_IDR_HIERARCHY_DIAGNOSTIC_PROVIDER_BLOCKED`.

Otherwise:
- `M24_IDR_HIERARCHY_EXCURSION_LOCALIZED`: L17 has `Emax>9`, L70 has `Emax<=3`, and the L70 response at 6000 is at least 5x smaller than L17 in at least two of TT/EE/TE.
- `M24_IDR_HIERARCHY_EXCURSION_STRONGLY_SENSITIVE`: not localized, but L70 changes `Emax` by at least a factor 3, or changes the 6000 response by at least 3x in at least two CMB channels.
- `M24_IDR_HIERARCHY_EXCURSION_INSENSITIVE`: neither condition; the excursion persists without strong hierarchy-depth sensitivity.

L35 is trajectory/convergence evidence and does not alone define classification.

## Guardrails
Always set `K1_promoted=false` and `physical_falsification=false`.
Do not rewrite the parent K1 non-establishment.
If hierarchy sensitivity is found, preregister a separate convergence/production K1 profile before any K1 promotion.
If insensitive, continue to another independent numerical/physics-boundary audit; do not tune ETHOS physical parameters to obtain continuity.