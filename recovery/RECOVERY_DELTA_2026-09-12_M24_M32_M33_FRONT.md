# KMDSB recovery delta — 2026-09-12 active frontier

## M24 / F24 — ETHOS-like IDM-DR K1 localization

Small-a4 diagnostic run `34712620163`, job `103604016263`, artifact `10304820222` (`sha256:fb4e9d2fbec93dc3ced8f174f83c908d076bac31e88b469b3c5ec81e18188ad9`) shows P(k) normalized residuals for `a_idm_dr={600,200,60,20}` Mpc^-1 of `{2.0393132033774542e-06,2.0355838471472935e-06,2.0312929269389156e-06,2.030108969932068e-06}`. The all-four log-log slope is `0.0013770723401537077`; `R2(20)/R2(600)=0.9954866013567006`. Diagnostic only; no K1 promotion or physical falsification.

The earlier ad-hoc full-ladder harness omitted `build: 0` from `status.json`. A process-only repair was frozen before rerun; provider, physics, grids, analyzer and thresholds were unchanged. Corrected full-compatible run `34716044903`, job `103613350956`, commit `d0696195da093e942cc579c43bdd7daeb39224ae`, artifact `10305155772` (`sha256:2c5b9e4be3acdad6ca391be39c349e868039d97df1560580bbfa0dbd188b40d2`) completes all provider cases with rc=0 and exact zero-vs-omitted identity `R2=0` in TT/EE/TE/P(k). The P(k) ladder is `{2.582285897613336e-06,2.208878685483948e-06,2.091672623349137e-06,2.048524252564187e-06,2.0393132033775004e-06}` for `a_idm_dr={60000,18000,6000,1800,600}`. Tail/top=`0.7897317664408595`, smallest-three log-log slope=`0.011110250072532211`; frozen quarter-contraction fails. Analyzer classification `M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED`, K1 `NOT_PROMOTED`, physical falsification false. Durable result: `waves/wave_04_dark_matter/M24_K1_COMPATIBLE_FULL_LADDER_DIAGNOSTIC_RESULT.json`.

Precision-profile matrix run `34716054597`, commit `16399c0d7ffd6d033d57c8f6d4f85a956d870eda`, has independent `UR20/UR30/UR40` lanes still executing at this checkpoint. It is diagnostic-only and cannot override the earlier preregistered authorization condition for canonical K1 promotion.

## M31 / F31 — EFT/Horndeski K2 CMB tangent localization

Reference-CMB precision run `34702705097`, job `103577165523`, artifact `10300871714` initially reported a baseline-reproduction mismatch because a fine-pair-only result was being compared against a broader three-level band classification. Prospectively defined immutable recovery run `34708033251`, job `103591546889`, artifact `10302631267` (`sha256:7bfe21974b53712545694d269ea78e09ce6bf2667f0864c55d6dac134c4b3ef1`) verifies the fine-pair metrics exactly against the prior localization artifact and classifies `M31_REFERENCE_PRECISION_HIGH_ELL_NONCONVERGENCE_PERSISTS`.

Under provider `cl_ref.pre`, only `ell=2-30` passes the frozen 5deg/0.25 diagnostic criterion. Acoustic-low `31-200`, acoustic-mid `201-1000`, high `1001-2500`, and full `2-2500` fail. Sliding-ell immutable localization run `34710290496`, job `103597707471`, artifact `10303440900` (`sha256:8a1b483cfb520a107cfa188ce6efde3724edaeafde88d1c551abbc8a5b2c3dbb`) classifies `M31_TT_HIGH_ELL_NONCONVERGENCE_LOCALIZED`: under `cl_ref`, first failure is `ell=31-100`, with 1/15 windows passing and 14/15 failing; default precision first fails at `ell=201-400`, with 3/15 passing. K2 remains OPEN; no family exclusion or physical falsification.

## M32 / F32 — DGP provider build infrastructure

K0i exact O3 compilation on Ubuntu-22.04 and K0j cross-image control on Ubuntu-24.04 both reach a live exact-pin Intel `ifx` compile of `umuscl.o`, then receive a runner-level shutdown/exit 143 without explicit compiler/source diagnostics. K0j run `34716115931`, job `103613543497`, durable result `waves/wave_05_modified_gravity/M32_K0J_UMUSCL_HOSTED_IMAGE_CONTROL_RESULT.json`, weakens an Ubuntu-image-specific explanation.

K0k compiler-phase localization was preregistered before execution. Run `34716897688`: exact Intel preprocessing of `hydro/umuscl.f90` with frozen macros succeeds (`rc=0`, nonempty output; job `103615679269`, artifact `10305640272`, `sha256:2cb254b70e6881a1d649f8ef5d896f81d82f441f8fef451fac38cff543b6dc25`), while exact-checkpoint object compilation at O0 still receives hosted shutdown/143 after a live `ifx` process (job `103615678974`). Synthesis classification `M32_K0K_COMPILE_STAGE_HOSTED_BLOCKER_PERSISTS_BELOW_O3`. Durable result: `waves/wave_05_modified_gravity/M32_K0K_UMUSCL_COMPILER_PHASE_LOCALIZATION_RESULT.json`. This is an infrastructure blocker after preprocessing, not K0/scientific/physical failure. Further optimization-flag repetitions are low information and M32 is parked pending a genuinely different execution environment.

## M33 / F33 — cubic tracker K2 tangent

Provider-reference-precision tangent run `34710982930`, job `103599612833`, artifact `10303169036` (`sha256:9432e33fda46d1142112dda8e8718ddbeb131d22701f99e2aba634a868680ce5`) completes all five provider cases. Frozen combined tangent: signed cosine `0.9885980734821153` (<0.995), principal angle `8.66044611575416` deg (>5), relative norm mismatch `0.4830260716171997` (>0.25), and finer symmetric displacement does not contract in both CMB and P(k). Classification `M33_CUBIC_TRACKER_REFERENCE_PRECISION_TANGENT_NONCONVERGENCE_PERSISTS`; canonical K2 remains OPEN, no physical falsification.

## M20 / F20 — SIDM K4 numerical robustness frontier

M20 has canonical scoped K1 PASS but K4 remains untested. `protocol/W04_M20_K4_NUMERICAL_AXIS_LOCALIZATION_PREREGISTRATION_v0.1.md` was frozen before execution. New run `34717401562`, workflow commit `c6c176c43cda25e468f1a2a865c7c61e5cc1f55c`, contains two independent diagnostic lanes at fixed physics/provider: `hermite5` changes only `N_herm 3->5`; `dz01` changes only `dz 0.2->0.1`. Both compare their own zero-reference structural responses at `sigma0_m={1,0.1,0.01}` against baseline using prospectively frozen symmetric-discrepancy labels. Diagnostic-only: `K4_promoted=false`, `physical_falsification=false` in every outcome.

## Guardrail

Green CI is not scientific PASS. Infrastructure/numerical blockers remain separate from physical falsification. Frozen thresholds are not retuned after seeing results. Duplicate heavy work is not launched merely to occupy runners.
