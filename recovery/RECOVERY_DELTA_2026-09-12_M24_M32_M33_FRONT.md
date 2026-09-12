# KMDSB recovery delta — 2026-09-12 active frontier

## M24 / F24 — ETHOS-like IDM-DR K1 localization

Small-a4 run `34712620163` and corrected full-compatible run `34716044903` show a persistent shallow P(k) residual plateau under the source-compatible reference profile. Corrected full ladder has exact zero-vs-omitted identity `R2=0` in TT/EE/TE/P(k), but P(k) tail/top=`0.7897317664408595` and smallest-three slope=`0.011110250072532211`; analyzer classification `M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED`, K1 `NOT_PROMOTED`, physical falsification false. Precision robustness run `34716054597` completed UR20/UR30/UR40 with tail/top respectively `0.7897760999538475`, `0.7897317664408595`, `0.7897414408215833`, absolute spread `4.433351298793742e-05`. The plateau is therefore highly robust to this precision knob; further UR-trigger sweep is low information. Durable results: `M24_K1_COMPATIBLE_FULL_LADDER_DIAGNOSTIC_RESULT.json` and `M24_K1_PRECISION_PROFILE_ROBUSTNESS_SWEEP_RESULT.json`.

## M31 / F31 — EFT/Horndeski K2 CMB tangent localization

Immutable recovery run `34708033251` verifies the fine-pair parent exactly and classifies `M31_REFERENCE_PRECISION_HIGH_ELL_NONCONVERGENCE_PERSISTS`. Sliding-ell run `34710290496` localizes reference-precision first failure to `ell=31-100`; only 1/15 cl_ref windows pass, versus default first failure `ell=201-400` and 3/15 pass. K2 remains OPEN; no family exclusion or physical falsification.

## M32 / F32 — DGP provider build infrastructure

K0i Ubuntu-22.04 and K0j Ubuntu-24.04 both reach a live exact-pin Intel `ifx` compile of `umuscl.o`, then receive runner shutdown/143 without explicit compiler/source diagnostics. K0k run `34716897688` further localizes the boundary: exact Intel preprocessing of `hydro/umuscl.f90` succeeds (`rc=0`, nonempty output), while exact-checkpoint object compilation still receives hosted shutdown/143 even at O0. Synthesis `M32_K0K_COMPILE_STAGE_HOSTED_BLOCKER_PERSISTS_BELOW_O3`. This is infrastructure blockage after preprocessing, not K0/scientific/physical failure. M32 is parked pending a genuinely different execution environment.

## M33 / F33 — cubic tracker K2 tangent

Reference-precision run `34710982930` gives combined tangent cosine `0.9885980734821153`, angle `8.66044611575416` deg, relative norm mismatch `0.4830260716171997`, and no fine symmetric contraction in both CMB/P(k). Classification `M33_CUBIC_TRACKER_REFERENCE_PRECISION_TANGENT_NONCONVERGENCE_PERSISTS`; K2 remains OPEN, no physical falsification.

## M20 / F20 — SIDM K4 numerical robustness

Scoped K1 is PASS, while K4 was previously untested. Prospectively frozen two-axis diagnostic recovery run `34717549823` is now terminal. The independent dz axis (`0.2 -> 0.1`, N_herm=3 fixed) is `M20_K4_AXIS_LOW_SENSITIVITY_DIAGNOSTIC`: exact-zero identities are exact, max symmetric response discrepancy `0.03852684135623168`, median `0.02231018298872599`. The independent Hermite axis (`N_herm 3 -> 5`, dz=0.2 fixed) is `M20_K4_AXIS_STRONG_SENSITIVITY_DIAGNOSTIC`: exact-zero identities are exact, max discrepancy `0.8842068464159993`, median `0.37251299304632857`. Thus the dominant K4 blocker is Hermite quadrature rather than dz. Durable aggregate: `waves/wave_04_dark_matter/M20_K4_NUMERICAL_AXIS_LOCALIZATION_RESULT.json`.

Prospectively frozen Hermite convergence run `34717652237`, job `103617657859`, artifact `10305426444` (`sha256:e30f7b80932719f26725b476381b5d8b9c9ec3de8c7387c9a016d64f5689db0e`) evaluates N_herm={5,7,9}. Max discrepancy decreases `1.1726655606126613 -> 0.8211898017857969`; median `0.30659483056319403 -> 0.18334344734842292`, but terminal max remains far above frozen 0.10. Classification `M20_K4_HERMITE_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`.

Prospectively frozen high-order extension run `34717756538`, job `103617936805`, artifact `10305886096` (`sha256:f35c58d996c885400a3fe071378d5292de038818f5be8b3a7b82daca0ab6d511`) evaluates N_herm={9,11,13}. Max discrepancy again decreases `0.6803476320209885 -> 0.6135806018848695`; median `0.14665619753904058 -> 0.13463557778224539`. Classification `M20_K4_HERMITE_HIGH_ORDER_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`. Numerical closure is still not established at N_herm=13; no K4 promotion or physical falsification. Durable result: `waves/wave_04_dark_matter/M20_K4_HERMITE_HIGH_ORDER_EXTENSION_RESULT.json`.

A wider asymptotic extension N_herm={13,17,21} was preregistered before execution and launched as run `34717891994`; it is queued at this checkpoint. It tests whether the slow convergence continues or stalls. Always diagnostic-only.

## M22 / F22 — annihilating-DM K4 precision robustness

M22 has K1 `PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION_EXACT_ZERO` while K4 was previously NOT_TESTED. A new precision-ladder diagnostic was preregistered before execution in `protocol/W04_M22_K4_PRECISION_LADDER_LOCALIZATION_PREREGISTRATION_v0.1.md`. It freezes the K1-v2 physics and three strong/mid/tail p_ann points, and runs three independent numerical profiles: default, provider `cl_permille.pre`, and provider `cl_ref.pre`. Each profile has its own omitted/zero controls and TT/EE/TE/P(k) response cells. Run `34717830680` contains three independent profile jobs plus aggregate analysis and is queued at this checkpoint. The diagnostic cannot promote K4 or establish physical failure by itself.

## Guardrail

Green CI is not scientific PASS. Infrastructure/numerical blockers remain separate from physical falsification. Frozen thresholds are not retuned after seeing results. Duplicate heavy work is not launched merely to occupy runners.
