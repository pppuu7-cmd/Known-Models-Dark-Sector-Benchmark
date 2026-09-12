# KMDSB recovery delta — 2026-09-12 M24/M32/M33 frontier

## M24 / F24 — ETHOS-like IDM-DR K1 localization

A diagnostic small-a4 extension completed successfully in run `34712620163`, job `103604016263`, head commit `a12042642038343927a8997bb0059d30bd25d9b5`, artifact `10304820222`, artifact digest `sha256:fb4e9d2fbec93dc3ced8f174f83c908d076bac31e88b469b3c5ec81e18188ad9`.

Under the prospectively compatible provider reference-precision profile, the P(k) normalized residuals for `a_idm_dr={600,200,60,20}` Mpc^-1 are `{2.0393132033774542e-06,2.0355838471472935e-06,2.0312929269389156e-06,2.030108969932068e-06}`. The all-four log-log slope is `0.0013770723401537077`; the residual ratio `R2(20)/R2(600)=0.9954866013567006`. Classification remains diagnostic-only `M24_SMALL_A4_TAIL_EXECUTED`; no K1 promotion and no physical falsification.

Two ad-hoc frozen-ladder workflows had a process-only bookkeeping defect: successful CLASS builds were not represented by `build: 0` in `status.json`, while the unchanged authoritative analyzer requires that key. Consequently their earlier `PROVIDER_EXECUTION_BLOCKED` classification was harness-invalid despite all provider cases returning zero. A prospective recovery was frozen before rerun; only `status.json` initialization was changed. Physics, provider pin, grids, thresholds and analyzer remain unchanged.

Active recovery computations at this delta:
- full compatible frozen ladder run `34716044903`, commit `d0696195da093e942cc579c43bdd7daeb39224ae`;
- precision-profile matrix run `34716054597`, commit `16399c0d7ffd6d033d57c8f6d4f85a956d870eda`, three independent lanes `UR20/UR30/UR40` with fail-fast disabled.

Do not update canonical K1 until these recovery artifacts are terminal and consumed. The full-compatible and precision-profile reruns are diagnostic-only and cannot override the earlier preregistered authorization condition for canonical K1 promotion.

## M33 / F33 — cubic tracker K2 tangent

Provider-reference-precision tangent run `34710982930`, job `103599612833`, head commit `abcaf7773db60cf30a7512a457625d4f6f43d696`, artifact `10303169036`, digest `sha256:9432e33fda46d1142112dda8e8718ddbeb131d22701f99e2aba634a868680ce5` completed with all five provider cases executable.

Frozen combined tangent diagnostics: signed cosine `0.9885980734821153` (<0.995), principal angle `8.66044611575416` deg (>5), relative norm mismatch `0.4830260716171997` (>0.25), and the finer symmetric displacements do not contract in both CMB and P(k). Classification: `M33_CUBIC_TRACKER_REFERENCE_PRECISION_TANGENT_NONCONVERGENCE_PERSISTS`. Canonical K2 remains OPEN, K2 is not promoted, and this is not physical falsification. The result strengthens localization against a simple default-precision explanation.

## M32 / F32 — DGP provider build infrastructure

K0i run `34711054960`, attempt 2, job `103604333371` reached a live exact-pin `ifx` compilation of `umuscl.o`. Repeated shell heartbeats were observed, then the GitHub-hosted Ubuntu-22.04 runner emitted an external shutdown signal and the step exited `143`; no compiler/source diagnostic preceded the shutdown. This remains infrastructure blockage, not scientific failure.

K0j prospectively changed only the hosted image to Ubuntu-24.04 while preserving provider commit `849ddb716041316d0e223ba22badc0d630b72435`, immutable checkpoint artifact `10283774354`, oneAPI compiler family, exact target and O3 flags. Run `34716115931`, job `103613543497`, on Ubuntu `24.04.5`, image `20260907.300.1`, Azure `westus3`, again reached a live `ifx` compile, emitted heartbeats at `20:07:30/35/40/45Z`, then received a runner-level shutdown at `20:07:52Z` and exited `143`. No explicit compiler/source diagnostic preceded shutdown. Frozen classification: `M32_K0J_UMUSCL_HOSTED_INFRASTRUCTURE_BLOCKED_CROSS_IMAGE`; K0 remains unpromoted and physical/scientific falsification remains false. Durable result: `waves/wave_05_modified_gravity/M32_K0J_UMUSCL_HOSTED_IMAGE_CONTROL_RESULT.json`.

This materially weakens an Ubuntu-22-specific explanation. The blocker is now localized to hosted execution during the exact UMUSCL compilation path, but compiler phase remains unresolved.

K0k was preregistered before execution in `protocol/W05_M32_K0K_UMUSCL_COMPILER_PHASE_LOCALIZATION_v0.1.md`. It launches two independent infrastructure-only lanes in run `34716897688`: Intel preprocessing of the exact `hydro/umuscl.f90` source/macros, and exact-checkpoint `umuscl.o` compilation with only optimization changed from O3 to O0. K0k cannot promote K0 and cannot establish physical/scientific failure; it only discriminates preprocessing/front-end viability from optimization/code-generation workload sensitivity.

## Guardrail

Green CI is not scientific PASS. Infrastructure/numerical blockers must remain separate from physical falsification. Do not retune frozen thresholds after seeing results. Do not launch duplicate heavy work merely to occupy runners.
