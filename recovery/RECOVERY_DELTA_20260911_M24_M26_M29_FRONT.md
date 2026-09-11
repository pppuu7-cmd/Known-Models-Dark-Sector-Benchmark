# KMDSB recovery delta — 2026-09-11 — M24/M26 closures and M29 frontier

This note records only validated durable state. It does not promote K-gates beyond their machine results.

## M24 / F24 ETHOS-like dark sector

Canonical causal grid-swap run: `34627924337`.
Canonical result commit: `e0da7a772630d7b90ffd66bf426a28d5092895fa`.
Parent topology run: `34626787237`.
Classification: `M24_L_LOGSTEP_CMB_CATASTROPHE_CAUSALLY_TRANSFERS_WITH_MULTIPOLE_GRID`.

The bidirectional intervention transfers the large CMB error with the actual CLASS multipole grid. Frozen induction ratio and rescue ratio are both approximately `100.3184271345811`, and integrity checks pass. This is a strong causal numerical attribution of the sharp `l_logstep=1.12` CMB catastrophe to the discrete multipole-grid realization. It is explicitly **not** a physical ETHOS falsification. The result itself states `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.

Do not convert this numerical localization into a K1/K4 PASS. The next M24 scientific step, if required by the census protocol, must be a separately preregistered robust-grid/reference construction rather than another blind l_logstep scan.

## M26 / F26 PBH dark matter

Canonical ideal cosmic-variance recovery commit: `3681bc09c35f1f851339204b2b897430dbbc7c48`.
Parent multi-observable provider run: `34555112732`.
Classification: `M26_PBH_CDI_IDEAL_CV_OBSERVABILITY_PROXY_ESTABLISHED`.

All three masses are numerically valid and pass frozen fraction scaling. At PBH fraction 1 the idealized full-sky noise-free fixed-parameter CMB proxy gives approximately:

- `100 Msun`: SNR `0.0010255433`;
- `1000 Msun`: SNR `0.0102554325`;
- `10000 Msun`: SNR `0.1025543250`.

All sampled points are below ideal-CV 1 sigma. The fraction-loglog-SNR slopes are approximately one. This is an optimistic observability proxy only, not a survey likelihood or exclusion. `observation_likelihood_gate=OPEN`, `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.

## M25 / F25 sterile-provider numerical boundary

Preserve the latest compile-capacity isolation result: stock CLASS compile-time capacity blocks the high-resolution sterile-provider representation while raised-capacity matched-evolver/manual controls converge. Treat as provider/capacity boundary; no physical falsification and no K1/K4 promotion.

## M29 / F29 Brans-Dicke — new active frontier

Pinned public provider: `hiclass-code/hi_class_public` commit `0009f51d89e6465c79e570b496c66fc90058fa77`.
Native file: `gravity_models/brans_dicke.ini`.
Provider includes Brans-Dicke field evolution plus background and perturbation modules, `M2_tuning_smg=yes`, `M2_today_smg=1`, radiation-era attractor initialization for `phi_prime_ini=0`, and documented early-time stability settings.

K0 provider/provenance preregistration:
`protocol/W05_M29_HICLASS_BRANS_DICKE_K0_PROVIDER_PREREGISTRATION_v0.1.md`.
K0 workflow:
`.github/workflows/w05-m29-hiclass-k0-provider-probe.yml`.
K0 run launched: `34629672262`.

K1 GR-limit preregistration was frozen prospectively before consuming the K0 aggregate:
`protocol/W05_M29_BRANS_DICKE_K1_GR_LIMIT_PREREGISTRATION_v0.1.md`.
Frozen finite ladder: `omega_BD=[1e2,1e3,1e4,1e5]` against a same-provider LCDM reference, comparing background expansion, CMB TT and P(k). K1 workflow is fail-closed and is authorized only if the K0 canonical result is `M29_K0_PASS_WITH_SCOPE_PINNED_HICLASS_BRANS_DICKE_PROVIDER`.

## Global interpretation guard

None of M24 numerical localization, M25 provider/capacity blocking, M26 sub-CV proxy behavior, or an unfinished M29 gate authorizes `NEW_REQUIRED`, physical falsification of the corresponding family, or a statement that all known models fail. Continue the response-family census and later K5-K9/holdout layers under the frozen protocol.