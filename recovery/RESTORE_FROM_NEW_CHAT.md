# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-09
Purpose: resume KMDSB/DSIR benchmark development from another chat without relying on conversation memory.

## 0. Authority rule

If chat memory conflicts with repository evidence, repository evidence wins.

Historical scientific authorities are not silently rebased:
- W00-W02: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 starting authority / M07 physical evidence: `328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- current W03 observation-space methodology overlay from corrected M08 onward: `864952e1520d82473a9e976edfeb69f9899d174d`.
- exact transitions: `recovery/AUTHORITY_DELTAS.md` AD-001 and AD-002.

Authority continuity is provenance/history, not numerical equality or successful replay.

## 1. Read order in a fresh chat

1. `recovery/STATE.md`
2. this file
3. `recovery/AUTHORITY_DELTAS.md`
4. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`
5. `protocol/W03_M08_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
6. `models/canonical_quintessence/result.json`
7. `models/cpl_dark_energy/result.json`
8. `waves/wave_03_expanded_dark_energy/M08_M07_ABSORPTION_AUDIT.md`
9. `waves/wave_03_expanded_dark_energy/M08_M07_ABSORPTION_RESULT.json`
10. `matrices/benchmark_matrix.csv`
11. `matrices/design_prior_ledger.csv`
12. `logs/research_log.md`
13. active W03 workflows/files.

Do not reconstruct the project from README alone.

## 2. Project roles

- DSIR: formal reconstruction/methodology authority.
- KMDSB: model-family benchmark / adversarial test range.
- Future original model: later separate repository; KMDSB supplies evidence-derived construction constraints.

## 3. Frozen B0-B9 funnel

B0 provenance -> B1 reference embedding -> B2 conservation/gauge/frame -> B3 physical/numerical control -> B4 response/masks -> B5 observational identifiability -> B6 nearest comparator -> B7 quotient-surviving novelty -> B8 prospective holdout -> B9 synthesis/design priors.

Do not collapse `FAIL`, `NONIDENTIFIABLE`, `BLOCKED_*`, `INCONCLUSIVE`, implementation failure and physical failure.

## 4. Completed waves

### W00 COMPLETE
M00 LambdaCDM control; M01 smooth non-phantom wCDM scoped `NONIDENTIFIABLE` in corrected DESI DR1 ShapeFit.

### W01 COMPLETE
M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.

### W02 COMPLETE
- E1 IDE/GDM theory-response separation `PASS_WITH_SCOPE`.
- E2 IDE/f(R) theory-response separation `PASS_WITH_SCOPE`.
- E3 WDM alternative suppression `BLOCKED_IMPLEMENTATION`.
- E4 temporal scalar comparator `INCONCLUSIVE`.

Keep theory-space and observation-space graphs separate.

## 5. W03 — M07 canonical quintessence

Overall: `DSIR_PREDICTIVE_SUPPORT`.

Current gates:
B0 `PASS_WITH_SCOPE`; B1 `PASS_WITH_SCOPE`; B2 `PARTIAL`; B3 `PASS_WITH_SCOPE`; B4 `PASS_WITH_SCOPE`; B5 `NONIDENTIFIABLE`; B6 `PASS_WITH_SCOPE`; B7 `PARTIAL`; B8 `SUPPORTED` level-1; B9 `PARTIAL`.

### Controlled branch

Pinned CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

`V=(1+A)exp(-lambda phi)`, alpha=0, B=0, non-attractor IC, A is shooting nuisance, lambda physical.

Exact field reflection `(lambda,phi)->(-lambda,-phi)` gives local quotient coordinate

`q=lambda^2`.

Machine direction:
`waves/wave_03_expanded_dark_energy/M07_LOCAL_Q_DIRECTION.json`.

### Key M07 results

- Lambda-zero reference in strict production: lnH/lnP floor ~`1e-10`.
- strict shooting tolerance required; solver default distorted finite response strongly.
- q convergence at lambda .025/.075: relative difference `5.52e-4`, angle `0.0273 deg`.
- q direction vs C1 constant-w: `6.694 deg`.
- q direction vs frozen f(R): `60.728 deg`.
- B2: raw observables cross-gauge stable, small derived residuals not; do not promote metric/Weyl separator in current representation.
- B5 corrected ShapeFit: `sigma_q~2.269`; q=.09 only `~0.0401 sigma` -> `NONIDENTIFIABLE` in that scope.
- after C1 profiling: q=.09 only `~0.0220 sigma`; B7 remains `PARTIAL`.
- prospective lambda=.225 within-family holdout passes; B8 strength level 1 only.

### New M08 consequence for M07

The earlier P/H cross-channel separator against constant-w does **not** survive a stronger 2D CPL family comparator.

Do not promote the M07 constant-w P/H residual as mechanism-level novelty.

M07 remains useful as a controlled/predictive benchmark family, but its tested P/H signature lies almost entirely inside the local CPL smooth-DE span.

## 6. W03 — M08 CPL time-varying smooth dark energy

Scientific role: stronger phenomenological nearest-family comparator.

Branch:

`w(a)=w0+wa(1-a)`

`epsilon0=1+w0`, `epsilon_a=wa`

CLASS CLP, `cs2_fld=1`, `use_ppf=yes`.

Pure-fluid closure:
- explicit `Omega_Lambda=0`;
- `Omega_fld` inferred by solver closure.

### M08 run #1 — preserved implementation failure

Actions `34391852165`, digest `sha256:0c8cf5c2de8f3d4cc9f62d9a8574a60656db38caee297b01b6fdf1674517045e`.

All cases stopped before evolution because both `Omega_Lambda` and `Omega_fld` were specified. This is configuration failure only, not physical CPL failure.

### M08 run #2 — local basis PASS_WITH_SCOPE

Actions `34394929596`, head `a3bb13aab2f181fed31882d31f819c9d0b0a7a36`, digest `sha256:561bf0abc6b9247fe9bd517c142eeac5f96c677eab430993bd6cb1473e3a6a97`.

Local central step `1e-3` in epsilon0/wa.

Combined 35-node lnP + 7-node lnH basis:
- direction angle `9.1790225 deg`;
- singular values `{1.88297176,0.09452819}`;
- `sigma2/sigma1=0.0502016`.

Central nonlinearity ratios are ~`3.4e-4` to `1.33e-3`.

Interpretation: nominal parameter dimension 2 but strongly anisotropic response. This independently reinforces `parameter count != response rank`.

Machine basis:
`waves/wave_03_expanded_dark_energy/M08_CPL_LOCAL_BASIS.json`.

### M08 -> M07 absorption result

Reproducible calculator:
`code/w03_m08_absorb_m07.py`.

Result:
`waves/wave_03_expanded_dark_energy/M08_M07_ABSORPTION_RESULT.json`.

Fit one shared CPL parameter vector to concatenated M07 local q P+H response.

Best coefficients per unit q:
- `epsilon0/q = 0.1406534871`
- `wa/q = -0.2006790927`.

Residual after 2D CPL fit:
- combined `1.107%`
- P `0.864%`
- H `1.993%`.

Same-solver constant-w-like epsilon0-only residual:
- combined `15.820%`
- P `12.064%`
- H `29.149%`.

Thus CPL improves absorption by about `14.3x` overall.

Classification:
`CPL_ABSORBS_M07_CROSSCHANNEL_SEPARATOR_WITH_SCOPE`.

This is local unwhitened theory-space evidence, not observational equivalence.

## 7. DSIR main advancement / AD-002

Inspected DSIR main `864952e...` is 23 commits ahead of W03 starting authority `328f2ca...`.

Relevant Article-2 G5 changes:
- cross-family data-whitened stress contract prospectively frozen;
- synthetic fail-closed QA PASS;
- real ACT x unWISE 26-coordinate covariance/operator machinery located and reusable;
- multi-family provider -> exact same 26-coordinate response matrix is not yet bound;
- real classifying G5 execution is therefore still blocked by the mapping/interface, not by covariance acquisition.

Hard rule now used for M08 and later:

A covariance alone is insufficient for cross-family observational promotion. Every compared family must be propagated through one exact prospectively frozen observation operator into the same coordinate vector/order/units/masks on which the covariance acts.

Do not relabel the earlier model-specific ShapeFit controls as DSIR Article-2 G5 closure.

## 8. Future-model methodology

Active methodology:
`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`.

M08-specific lessons:
`protocol/W03_M08_MODEL_CONSTRUCTION_LESSONS_v0.1.md`.

Design ledger currently contains **51 ACTIVE requirements, DP-0001..DP-0817**.

Newest rules:
- DP-0815: profile the full implemented local comparator-family manifold/span, not one representative ray;
- DP-0816: exact common observation-operator/covariance coordinate bridge before cross-family observation-space claims;
- DP-0817: closure/normalization assignments are explicit provenance and configuration failure != physical failure.

M08 also reinforces DP-0303 and DP-0504.

## 9. Immediate continuation

Highest-priority next work:

1. preregister and run M08 local-step stability at a second smaller finite-difference step; confirm the 2D CPL tangent plane and the M07 absorption coefficients are stable;
2. only after that, build a common M07/M08 observational-operator manifest obeying AD-002;
3. if DSIR main later binds the ACT x unWISE multi-family provider bridge, reuse that exact 26-coordinate chain rather than inventing a substitute;
4. search for a gauge-robust response channel outside the CPL smooth-DE span;
5. use further W03 families to begin promoting repeated priors to `REINFORCED` where justified.

## 10. Never infer

- configuration/numerical failure == physical failure;
- parameter count == response rank;
- separation from one ray == separation from the comparator family;
- theory-space absorption == observational equivalence;
- covariance exists == covariance is coordinate-compatible;
- predictive holdout == observability;
- newest DSIR main == authority for every old result;
- missing comparator == uniqueness.

## 11. Maintenance rule

Every meaningful frontier change must synchronize:
- model audit/result;
- wave evidence;
- benchmark/design-prior matrices;
- active construction methodology;
- `STATE.md`, this manual and authority deltas;
- research chronology.

A new chat must be able to continue from repository evidence alone.
