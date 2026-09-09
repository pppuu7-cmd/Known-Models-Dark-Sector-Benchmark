# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-09
Purpose: resume KMDSB/DSIR benchmark development from another chat without relying on conversation memory.

## 0. Authority rule

If chat memory conflicts with repository evidence, repository evidence wins.

- W00-W02 authority: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 starting authority: `Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- transition: `recovery/AUTHORITY_DELTAS.md` AD-001.

Never silently rebase historical results.

## 1. Read order

1. `recovery/STATE.md`
2. `recovery/AUTHORITY_DELTAS.md`
3. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
4. `protocol/W03_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
5. `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`
6. `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`
7. `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`
8. `protocol/STATUS_TAXONOMY.md`
9. `matrices/wave_matrix.csv`
10. `matrices/benchmark_matrix.csv`
11. `matrices/design_prior_ledger.csv`
12. `logs/research_log.md`
13. active wave directory

Do not reconstruct the project from README alone.

## 2. Project roles

- DSIR: reconstruction/methodology authority.
- KMDSB: benchmark range for known dark-sector / dark-energy / MG models.
- Future original model: separate later repository; construction requirements are extracted here first.

## 3. Frozen B0-B9 funnel

B0 provenance -> B1 reference embedding -> B2 conservation/gauge/frame -> B3 physical/numerical domain -> B4 response/masks -> B5 observational identifiability -> B6 nearest comparator -> B7 quotient novelty -> B8 prospective holdout -> B9 synthesis/design priors.

Never collapse `FAIL`, `NONIDENTIFIABLE`, `BLOCKED_*`, `INCONCLUSIVE`, numerical failure and physical failure into one state.

## 4. Completed waves

### W00 COMPLETE
M00 LambdaCDM control and M01 smooth non-phantom wCDM.
M01 is DSIR-compatible but `NONIDENTIFIABLE` in scoped corrected DESI DR1 ShapeFit; `sigma(epsilon_w)~0.1782`, `epsilon_w=1e-4` is only ~`5.61e-4 sigma`.

### W01 COMPLETE
M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.
Key requirements: tangent cones, conservation, multi-channel rank, high-k masks, MG comparator, temporal/holdout semantics.

### W02 COMPLETE
- E1 IDE/GDM `PASS_WITH_SCOPE`, closest angle `24.786398 deg`.
- E2 IDE/f(R) `PASS_WITH_SCOPE`, `42.450273/59.404101 deg`.
- E3 WDM alternative suppression `BLOCKED_IMPLEMENTATION`.
- E4 DCDM temporal scalar `INCONCLUSIVE`.
Keep theory-space and observation-space graphs separate.

## 5. W03 ACTIVE — M07 canonical quintessence

Solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Frozen canonical branch:
`V(phi)=(1+A)exp(-lambda phi)`, `alpha=0`, `B=0`, non-attractor IC, `phi_ini=1`, `phi_prime_ini=0`, physical `lambda`, nuisance `A`, `scf_tuning_index=2`.

Current gate state:
B0 PASS_WITH_SCOPE; B1 PASS_WITH_SCOPE; B2 PARTIAL; B3 PASS_WITH_SCOPE; B4 PASS_WITH_SCOPE; B5 OPEN; B6 PASS_WITH_SCOPE; B7 OPEN; B8 OPEN; B9 PARTIAL; overall `DSIR_COMPATIBLE`.

### 5.1 Reference/numerical calibration

Natural seed:
`A_seed(lambda)=3 Omega_scf H0^2 exp(lambda phi_ini)-1`.

Run `34325977559` fixed the original shooting failure and established subdominant reference calibration.

Authoritative strict production/shooting audit: run `34338140447`, artifact `w03-m07-shooting-precision-audit`, digest `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`.

Dark-energy-dominant lambda-zero reference:
- target Omega_scf `0.682686955086854`;
- achieved `0.682686955181768`;
- `max|lnH|=1.08876e-10`;
- `max|lnP|=2.16648e-10`;
- `w=-1`, `phi=1`, `phi'=0`.

Default shooting tolerance created fake target drift up to `1.23798e-3` at lambda=.30; strict `tol_shooting_deltax_rel=1e-13` reduced that error to about `3.01e-10`. Default vs strict lambda=.30 matter responses differ ~38.1% in relative norm. Use only strict vectors for science.

### 5.2 B6 nearest comparator

Run `34358089618`.
Common block: unwhitened 7x5 low-k `r_Delta(k,z)`.

M07 vs C1 smooth-w acute angles:
`.025:15.9702`, `.075:6.9206`, `.15:6.6924`, `.30:6.6114 deg`.

M07 vs frozen designer-f(R):
`.025:73.0805`, `.075:62.1181`, `.15:61.0432`, `.30:60.7968 deg`.

Interpretation: strong low-k matter near-degeneracy with smooth-w; far from frozen f(R). Exact non-collinearity is theory-space only. No observational promotion.

### 5.3 Fixed-coordinate parity test — FAIL_WITH_SCOPE

Run `34358465646`, artifact digest `sha256:807e935cfa758df81c251531a672c829f430ab41a44e3219fe67a0fbbbe6cb40`.
Test changed `lambda -> -lambda` at fixed `phi_ini=+1`; preregistered lnP odd/even threshold `1e-3`.

- |lambda|=.025: `7.4666e-3` FAIL
- |lambda|=.075: `2.0277e-3` FAIL

Preserve this failure; do not loosen threshold. See `M07_FIXED_COORDINATE_PARITY_FAILURE.md`.

### 5.4 Exact field-reflection quotient parity — PASS_WITH_SCOPE

Exact canonical quotient for B=0:
`(lambda,phi_ini)->(-lambda,-phi_ini)`.

Run `34359042959`, artifact `w03-m07-field-reflection-quotient-parity`, digest `sha256:d5e747fc54aee3a8fe3c50372f5788d6c95bcddc47b3598cf1646d114ff041b1`.
Preregistered odd-fraction max: `1e-6`.

At |lambda|=.025 and .075:
- lnP odd/even = `0`;
- lnH odd/even = `0`;
- response angle = `0 deg`.

Therefore sign(lambda) is redundant on this physical quotient. `q=lambda^2` is a valid invariant coordinate candidate, but q-linearity is still a separate test.

Evidence: `M07_FIELD_REFLECTION_QUOTIENT_PARITY.md`.

### 5.5 q-linearity diagnostic

q-scaled H response already converges well:
- lambda .025 vs .075 relative difference ~`9.97e-4`;
- angle ~`0.0294 deg`.

q-scaled low-k P response does not under baseline perturbation precision:
- relative difference ~`0.2307`;
- angle `12.5058 deg`.

This channel split motivates a perturbation precision audit rather than immediate rejection of q.

Active run at this recovery checkpoint:
`34359536106`, workflow `.github/workflows/w03-m07-perturbation-precision-q-audit.yml`.

It reruns lambda=.025/.075 with the same strict shooting but tight perturbation settings:
`tol_perturbations_integration=1e-8`, `perturbations_sampling_stepsize=0.01`.

Frozen before result:
- tight q-scaled P relative difference <= `0.05`;
- tight q-scaled P angle <= `2.0 deg`.

Do not change these thresholds after reading the run.

## 6. Future-model design ledger

`matrices/design_prior_ledger.csv` currently has 41 ACTIVE requirements, DP-0001..DP-0807.

W03 additions DP-0801..DP-0807 include:
- physical/nuisance separation;
- natural-scale initialization;
- reference regression before finite science;
- perturbation/time treatment of microphysical DE;
- phenomenological-DE nearest comparator;
- solver tolerance conditioning;
- quotient exact redundancies before parity/derivative/Jacobian/local-coordinate claims.

These are evidence priors, not axioms. Promotion remains ACTIVE -> REINFORCED -> CORE -> RETIRED.

## 7. Immediate continuation

1. Inspect run `34359536106` and artifact.
2. If frozen tight q gate passes, freeze `q=lambda^2` as the local quotient coordinate within tested M07 scope and construct the q-response direction.
3. If it fails, keep q parity but classify the residual as perturbation numerical floor vs true q nonlinearity; do not alter thresholds.
4. Then address B2 explicit gauge/additional-response bookkeeping and build an orthogonal response channel to break M07/C1 near-degeneracy.
5. Next B5 observational whitening; B7 quotient novelty only after orthogonal-channel survival.
6. B8 remains untouched until a prospective relation is frozen before holdout exposure.

## 8. Never infer

- numerical failure == physical failure;
- exact field-reflection parity == q-linearity;
- theory-space angle == observational discrimination;
- near-alignment == physical equivalence;
- missing comparator == uniqueness;
- production grid == B8 evidence;
- newest DSIR main == authority for old waves.

## 9. Maintenance rule

Every meaningful frontier change must synchronize:
- per-model audit/result;
- wave evidence;
- benchmark/design-prior matrices;
- future-model methodology;
- `recovery/STATE.md` and this manual;
- `logs/research_log.md`.

A new chat must be able to continue from repository evidence alone.
