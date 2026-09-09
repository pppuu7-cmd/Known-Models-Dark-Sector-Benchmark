# KMDSB current state / recovery handoff

Updated: 2026-09-09

## Authority
- W00-W02: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03: `Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- transition: `recovery/AUTHORITY_DELTAS.md` AD-001.
- repository evidence overrides chat memory.

## Recovery read order
1. `recovery/RESTORE_FROM_NEW_CHAT.md`
2. this file
3. `models/canonical_quintessence/result.json`
4. `models/canonical_quintessence/OBSERVATION_SPACE_AUDIT.md`
5. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
6. `protocol/W03_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
7. `protocol/W03_M07_OBSERVATION_SPACE_LESSONS.md`
8. `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`
9. `matrices/benchmark_matrix.csv`
10. `matrices/design_prior_ledger.csv`
11. active W03 files.

## Completed waves
- W00 COMPLETE: M00 LambdaCDM control; M01 smooth-w scoped `NONIDENTIFIABLE` in corrected ShapeFit (`sigma(epsilon_w)=0.1781944`; epsilon=1e-4 gives ~5.61e-4 sigma).
- W01 COMPLETE: M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.
- W02 COMPLETE: E1 IDE/GDM `PASS_WITH_SCOPE` (24.7864 deg closest); E2 IDE/f(R) `PASS_WITH_SCOPE` (42.4503/59.4041 deg); E3 `BLOCKED_IMPLEMENTATION`; E4 `INCONCLUSIVE`.

## W03 ACTIVE

### M07 canonical quintessence — current terminal scoped state

Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Branch:
`V=(1+A)exp(-lambda phi)`, alpha=0, B=0, non-attractor IC, phi_ini=1, phi'_ini=0, A shooting nuisance.
Exact field-reflection quotient identifies `(lambda,phi)~(-lambda,-phi)` and the controlled local coordinate is `q=lambda^2`.

Current gates:
- B0 `PASS_WITH_SCOPE`
- B1 `PASS_WITH_SCOPE`
- B2 `PARTIAL`
- B3 `PASS_WITH_SCOPE`
- B4 `PASS_WITH_SCOPE`
- B5 `NONIDENTIFIABLE`
- B6 `PASS_WITH_SCOPE`
- B7 `PARTIAL`
- B8 `SUPPORTED` (level-1 within-family prospective interpolation only)
- B9 `PARTIAL`
Overall: `DSIR_PREDICTIVE_SUPPORT`.

### Numerical / quotient controls
Natural seed:
`A_seed=3 Omega_scf H0^2 exp(lambda phi_ini)-1`.

Strict production run `34338140447`, digest `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`.
Lambda-zero full-DE reference: max|lnH| `1.08876e-10`, max|lnP| `2.16648e-10`.
Default shooting tolerance generated fake Omega drift up to `1.23798e-3`; strict `tol_shooting_deltax_rel=1e-13` is authoritative.

Field-reflection quotient run `34359042959` PASSED exactly for tested pairs; fixed-chart lambda-sign parity failure remains preserved as a coordinate-chart control.

q-coordinate perturbation convergence run `34359536106`, digest `sha256:6cd91f54d94982425cbec2055c42f7e087458ae3a4e350796f9a661623240b5d`:
- q-scaled P relative difference `.025 vs .075` = `5.51889e-4`
- angle = `0.0273111 deg`
- q direction vs C1 = `6.69445 deg`
- q direction vs frozen f(R) = `60.72848 deg`.

### B2 gauge/frame status — PARTIAL
Raw P,d_m,phi,psi pass paired synchronous/Newtonian `1e-4` regression, but small model/reference residuals do not.

Initial `lnP(model/ref)` response mismatch: `0.0309915691`.
Independent precision convergence run `34390302626`, digest `sha256:da93dd0b1afa983cffbc07e162f54cb728b6ede22c070bfc2b4d9001a4a0faed`:
- baseline `0.0309915691`
- tight `0.0309879842`
- improvement ratio `0.9998843`, failing preregistered <=0.50 requirement.

Direct transfer-level run `34390614155`, digest `sha256:6805465c0c8b932a15c6bab20641cc1599a36bd428707efd1eb396ce624ab9b8`:
- ln|d_m_model/d_m_ref| mismatch `0.03104952`
- fractional Weyl `(phi+psi)` response mismatch `0.12892986`.

Interpretation: current residual representations have a persistent cross-gauge/systematic floor. This is not evidence of physical gauge dependence, but the metric/Weyl channel cannot be promoted as a clean mechanism separator in this representation. Do not endlessly tighten M07; revisit only with a genuinely different gauge-invariant observable construction.

### B5 observation-space identifiability — NONIDENTIFIABLE
Workflow run `34390859777`, digest `sha256:91cd68778994d06a3d41c849a7dadf2ccb9ca23f8abd924666dc41d6d2f526c4`.
Same corrected DESI DR1 ShapeFit AP+growth+shape covariance used by M01; optimistic unmarginalized control.

Local q Fisher:
- `F_q=0.19428289`
- `sigma_q=2.26872951`.
Exact production points:
- lambda=.025 -> `0.0002755 sigma`
- .075 -> `0.0024795 sigma`
- .15 -> `0.0099386 sigma`
- .30 -> `0.0400892 sigma`.

Result: `NONIDENTIFIABLE_IN_FROZEN_LOCAL_CONTROL_SCOPE`, not physical falsification.

### B6/B7 nearest C1 comparator
Theory-space P/H cross-channel separator exists: same matter-fit amplitude leaves ~30.9% H residual, but this alone is not observational novelty.

ShapeFit covariance profiling of C1 smooth-w:
- whitened acute angle q vs epsilon_w = `33.72395 deg`
- sigma_q unprofiled = `2.26885`
- sigma_q profiled over C1 = `4.08661`
- orthogonal residual fraction = `0.55519`
- largest q=.09 profiled significance = `0.022023 sigma`.

Therefore B7 remains `PARTIAL`: covariance whitening reveals a non-collinear direction, but it carries negligible absolute information in this control.

### B8 prospective holdout — SUPPORTED_WITH_SCOPE
Preregistered lambda=.225 within-family interpolation holdout:
- run `34339027169`
- digest `sha256:3f7f149356f56284d137223b3e32b32992aea815400072b0be86db5e9d0fd576`
- lnH relative L2 error `0.0013263`, angle `0.019998 deg`
- lnP relative L2 error `0.0098686`, angle `0.524953 deg`.
This is only level-1 within-family predictive support, not a general law.

## Future-model methodology
`matrices/design_prior_ledger.csv` now contains **48 ACTIVE requirements**, DP-0001..DP-0814.
Latest additions:
- DP-0812: orthogonal channels count only after gauge/frame and subtraction-floor robustness;
- DP-0813: predictive regularity and observational identifiability are independent axes;
- DP-0814: report absolute profiled covariance-weighted significance alongside whitened angle.

## Immediate scientific continuation

M07 has reached its current stopping rule. Next target in W03: **M08 dynamic smooth dark energy / CPL w0-wa comparator**.

Primary preregistered question for M08:
Can a two-dimensional time-varying smooth-DE manifold absorb the M07 P/H cross-channel separator that constant-w C1 cannot?

Required order:
1. inspect/pin exact solver semantics for CPL and perturbation treatment;
2. define physical coordinates and LambdaCDM reference `(w0,wa)=(-1,0)`;
3. freeze admissible/stability domain before finite differences;
4. construct local 2D P+H response basis on matched grids;
5. fit M07 q direction with one shared CPL parameter vector across P and H;
6. only then consider observation-space projection/whitening.

## Non-negotiable
No zero-imputation; no theory-angle=observational claim; no numerical failure=physical failure; no missing comparator=uniqueness; no unquotiented rank claims; no retrospective B8; no silent authority rebase; no promoting an orthogonal channel whose derived response fails gauge/frame robustness.
