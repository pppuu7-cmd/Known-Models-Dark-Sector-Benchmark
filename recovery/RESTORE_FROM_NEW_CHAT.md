# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-09
Purpose: resume KMDSB/DSIR benchmark development from another chat without relying on conversation memory.

## 0. Authority rule

If chat memory conflicts with repository evidence, repository evidence wins.

- W00-W02 authority: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 authority: `Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- transition: `recovery/AUTHORITY_DELTAS.md` AD-001.

Never silently rebase historical results.

## 1. Read order in a fresh chat

1. `recovery/STATE.md`
2. this file
3. `recovery/AUTHORITY_DELTAS.md`
4. `models/canonical_quintessence/result.json`
5. `models/canonical_quintessence/OBSERVATION_SPACE_AUDIT.md`
6. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
7. `protocol/W03_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
8. `protocol/W03_M07_OBSERVATION_SPACE_LESSONS.md`
9. `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`
10. `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`
11. `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`
12. `matrices/benchmark_matrix.csv`
13. `matrices/design_prior_ledger.csv`
14. active W03 model files.

Do not reconstruct the project from README alone.

## 2. Project roles

- DSIR: reconstruction/methodology authority.
- KMDSB: benchmark range for known dark-sector, dark-energy and modified-gravity models.
- Future original model: separate later repository; KMDSB supplies evidence-derived construction constraints.

## 3. Frozen B0-B9 funnel

B0 provenance -> B1 reference embedding -> B2 conservation/gauge/frame -> B3 physical/numerical domain -> B4 response/masks -> B5 observational identifiability -> B6 nearest comparator -> B7 quotient-surviving novelty -> B8 prospective holdout -> B9 synthesis/design priors.

Never collapse `FAIL`, `NONIDENTIFIABLE`, `BLOCKED_*`, `INCONCLUSIVE`, numerical failure and physical failure into one state.

## 4. Completed waves

### W00 COMPLETE
M00 LambdaCDM control and M01 smooth non-phantom wCDM. M01 is DSIR-compatible but `NONIDENTIFIABLE` in corrected DESI DR1 ShapeFit local control: `sigma(epsilon_w)=0.1781944`; epsilon=1e-4 is only `~5.61e-4 sigma`.

### W01 COMPLETE
M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.

### W02 COMPLETE
- E1 IDE/GDM `PASS_WITH_SCOPE`, closest angle `24.786398 deg`.
- E2 IDE/f(R) `PASS_WITH_SCOPE`, `42.450273/59.404101 deg`.
- E3 WDM alternative suppression `BLOCKED_IMPLEMENTATION`.
- E4 DCDM temporal scalar `INCONCLUSIVE`.
Keep theory-space and observation-space graphs separate.

## 5. W03 ACTIVE — M07 canonical quintessence reached current stopping rule

Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Branch:
`V=(1+A)exp(-lambda phi)`, alpha=0, B=0, non-attractor IC, phi_ini=1, phi'_ini=0, A shooting nuisance.
Exact field-reflection quotient identifies `(lambda,phi)~(-lambda,-phi)` and local invariant coordinate `q=lambda^2`.

Current gates:
B0 `PASS_WITH_SCOPE`; B1 `PASS_WITH_SCOPE`; B2 `PARTIAL`; B3 `PASS_WITH_SCOPE`; B4 `PASS_WITH_SCOPE`; B5 `NONIDENTIFIABLE`; B6 `PASS_WITH_SCOPE`; B7 `PARTIAL`; B8 `SUPPORTED`; B9 `PARTIAL`. Overall `DSIR_PREDICTIVE_SUPPORT`.

Machine authority: `models/canonical_quintessence/result.json`.
Human summary: `models/canonical_quintessence/OBSERVATION_SPACE_AUDIT.md`.

### 5.1 Numerical/reference controls

Natural shooting seed:
`A_seed=3 Omega_scf H0^2 exp(lambda phi_ini)-1`.

Strict production run `34338140447`, digest `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`.
Full-DE lambda-zero reference:
- achieved Omega `0.682686955181768` for target `0.682686955086854`;
- max|lnH| `1.08876e-10`;
- max|lnP| `2.16648e-10`.

Default CLASS shooting tolerance caused fake Omega drift up to `1.23798e-3` at lambda=.30 and ~38.1% response-norm distortion. Strict `tol_shooting_deltax_rel=1e-13` is authoritative.

### 5.2 Exact quotient and local coordinate

Fixed-chart lambda-sign parity run `34358465646` failed the frozen odd-fraction gate and remains preserved.

Correct field-reflection quotient run `34359042959`, digest `sha256:d5e747fc54aee3a8fe3c50372f5788d6c95bcddc47b3598cf1646d114ff041b1`, passed exactly for tested pairs.

q-coordinate convergence run `34359536106`, digest `sha256:6cd91f54d94982425cbec2055c42f7e087458ae3a4e350796f9a661623240b5d`:
- q-scaled low-k P relative difference .025 vs .075: `5.51889e-4`;
- angle `0.0273111 deg`.
Therefore `q=lambda^2` is the controlled local coordinate in this tested branch/scope.

Machine direction: `waves/wave_03_expanded_dark_energy/M07_LOCAL_Q_DIRECTION.json`.

### 5.3 B6 / theory-space nearest comparators

M07 local q vs C1 smooth-w: `6.69445 deg`.
M07 local q vs frozen designer f(R): `60.72848 deg`.

Cross-channel P/H comparator run `34373096320` shows that one shared C1 amplitude which best fits matter leaves ~30.9% H residual. This is a theory-space cross-channel separator only.

### 5.4 B2 gauge/frame status — PARTIAL

Raw paired synchronous/Newtonian P,d_m,phi,psi pass the frozen `1e-4` regression, but small model/reference residuals do not.

Initial lnP residual mismatch: `0.0309915691`.
Independent precision run `34390302626`, digest `sha256:da93dd0b1afa983cffbc07e162f54cb728b6ede22c070bfc2b4d9001a4a0faed`:
- baseline `0.0309915691`;
- tight `0.0309879842`;
- improvement ratio `0.9998843`, failing frozen <=0.50 convergence requirement.

Direct transfer-level run `34390614155`, digest `sha256:6805465c0c8b932a15c6bab20641cc1599a36bd428707efd1eb396ce624ab9b8`:
- ln|d_m_model/d_m_ref| mismatch `0.03104952`;
- fractional Weyl response mismatch `0.12892986`.

Conclusion: current residual representations contain a persistent cross-gauge/systematic floor. This is not physical gauge dependence, but metric/Weyl response cannot be promoted as a clean discriminator in the current representation.

### 5.5 B5 — NONIDENTIFIABLE in corrected ShapeFit control

Run `34390859777`, digest `sha256:91cd68778994d06a3d41c849a7dadf2ccb9ca23f8abd924666dc41d6d2f526c4`.
Result file: `models/canonical_quintessence/b5_shapefit_q_fisher_result.json`.

Same corrected DESI DR1 ShapeFit AP+growth+shape covariance as M01; optimistic unmarginalized control.

- `F_q=0.19428289`;
- `sigma_q=2.26872951`.
Production significances:
- lambda=.025 -> `0.0002755 sigma`;
- .075 -> `0.0024795 sigma`;
- .15 -> `0.0099386 sigma`;
- .30 -> `0.0400892 sigma`.

Classification: `NONIDENTIFIABLE_IN_FROZEN_LOCAL_CONTROL_SCOPE`, not physical falsification.

### 5.6 B7 — nearest-C1 profiling in observation space

Result file: `models/canonical_quintessence/b7_shapefit_c1_profile_result.json`.

Same ShapeFit covariance, profiling C1 epsilon_w amplitude:
- whitened acute angle q vs epsilon = `33.72395 deg`;
- orthogonal residual fraction = `0.55519`;
- sigma_q unprofiled = `2.26885`;
- sigma_q profiled over C1 = `4.08661`;
- largest tested q=.09 profiled significance = `0.022023 sigma`.

Thus a non-collinear whitened component exists but its absolute information is negligible. B7 remains `PARTIAL`; no observational mechanism novelty claim.

### 5.7 B8 — prospective within-family support

Preregistered lambda=.225 holdout:
- run `34339027169`;
- digest `sha256:3f7f149356f56284d137223b3e32b32992aea815400072b0be86db5e9d0fd576`.
Prediction rule was frozen before execution from q-scaled training points lambda={.075,.15,.30}.

Holdout errors:
- lnH relative L2 `0.0013263`, angle `0.019998 deg`;
- lnP relative L2 `0.0098686`, angle `0.524953 deg`.

Classification: `SUPPORTED`, strength level 1 only. This is local within-family predictive regularity, not a universal law and not observational discrimination.

## 6. Future-model design methodology

`matrices/design_prior_ledger.csv` now contains **48 ACTIVE requirements**, DP-0001..DP-0814.

Latest W03 requirements:
- DP-0812: orthogonal channels count only after gauge/frame and subtraction-floor robustness;
- DP-0813: predictive regularity and observational identifiability are independent promotion axes;
- DP-0814: after whitening/comparator profiling report absolute profiled significance as well as angle/residual fraction.

Read `protocol/W03_M07_OBSERVATION_SPACE_LESSONS.md` before designing a new model.

## 7. M07 stopping rule

Do not spend unlimited cycles tightening the same M07 gauge residual. Further M07 work is justified only if a genuinely different gauge-invariant observable construction or new observational operator is introduced.

## 8. Immediate continuation — M08

Next W03 target: **M08 time-varying smooth dark energy / CPL w0-wa comparator**.

Primary preregistered question:
Can a two-dimensional time-varying smooth-DE manifold absorb the M07 P/H cross-channel separator that constant-w C1 cannot?

Required sequence:
1. inspect and pin exact solver implementation and perturbation semantics for CPL;
2. freeze LambdaCDM reference `(w0,wa)=(-1,0)` and physical/admissible domain before differentiation;
3. build a controlled 2D local response basis in matched P and H blocks;
4. fit M07 local q direction using one shared CPL parameter vector across both blocks;
5. report residual geometry before observational interpretation;
6. only then apply covariance whitening / profiling where a pinned operator exists.

If CPL absorbs M07, future-model lesson: flexible time-dependent phenomenological DE is the stronger comparator and a viable original model needs an additional perturbative/metric/time signature. If it does not, the M07 cross-channel separator is reinforced.

## 9. Never infer

- numerical failure == physical failure;
- predictive holdout support == observability;
- whitened angle == detection;
- theory-space separator == observational novelty;
- near-alignment == physical equivalence;
- missing comparator == uniqueness;
- production grid == B8 evidence;
- newest DSIR main == authority for old waves.

## 10. Maintenance rule

Every meaningful frontier change must synchronize:
- per-model audit/result;
- benchmark and design-prior matrices;
- future-model methodology when evidence changes construction rules;
- `recovery/STATE.md` and this manual;
- chronology/log.

A new chat must be able to continue from repository evidence alone.
