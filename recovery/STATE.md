# KMDSB current state / recovery handoff

Updated: 2026-09-09

## Authority

- W00-W02 numerical evidence: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 starting authority / M07 physical audits: `Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- current W03 observation-space methodology overlay from M08 onward: `Dark-Sector-Influence-Reconstruction@864952e1520d82473a9e976edfeb69f9899d174d`.
- transitions: `recovery/AUTHORITY_DELTAS.md` AD-001 and AD-002.
- repository evidence overrides chat memory.

Do not silently rebase M07 or older waves onto `864952e...`.

## Recovery read order

1. `recovery/RESTORE_FROM_NEW_CHAT.md`
2. this file
3. `recovery/AUTHORITY_DELTAS.md`
4. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`
5. `protocol/W03_M08_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
6. `models/canonical_quintessence/result.json`
7. `models/cpl_dark_energy/result.json`
8. `waves/wave_03_expanded_dark_energy/M08_M07_ABSORPTION_AUDIT.md`
9. `matrices/benchmark_matrix.csv`
10. `matrices/design_prior_ledger.csv`
11. `logs/research_log.md`

## Completed waves

- W00 COMPLETE: M00 LambdaCDM; M01 smooth-w scoped `NONIDENTIFIABLE` in corrected ShapeFit.
- W01 COMPLETE: M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.
- W02 COMPLETE: E1 IDE/GDM and E2 IDE/f(R) theory-response separation; E3 WDM alternative `BLOCKED_IMPLEMENTATION`; E4 temporal centroid `INCONCLUSIVE`.

## W03 ACTIVE

### M07 canonical quintessence — current scoped terminal state

Overall: `DSIR_PREDICTIVE_SUPPORT`.

Gates:
- B0 `PASS_WITH_SCOPE`
- B1 `PASS_WITH_SCOPE`
- B2 `PARTIAL`
- B3 `PASS_WITH_SCOPE`
- B4 `PASS_WITH_SCOPE`
- B5 `NONIDENTIFIABLE`
- B6 `PASS_WITH_SCOPE`
- B7 `PARTIAL`
- B8 `SUPPORTED` level-1 within-family only
- B9 `PARTIAL`

Controlled local coordinate after exact field-reflection quotient:
`q=lambda^2`.

M07 low-k local q direction is strongly near-aligned with constant-w C1 and far from frozen designer f(R).

ShapeFit B5:
- `sigma_q ~= 2.2687` optimistic unmarginalized;
- largest production q=.09 only `~0.0401 sigma`.
After C1 profiling:
- `sigma_q ~= 4.0866`;
- q=.09 only `~0.0220 sigma`.

B2 remains PARTIAL because small derived residuals retain cross-gauge representation floors even when raw P/d_m/phi/psi pass regression. Do not resume simple tolerance tightening.

B8: prospective lambda=.225 interpolation holdout passes in-family; this is predictive regularity, not mechanism uniqueness.

### M08 CPL time-varying smooth DE — ACTIVE / primary adversarial result obtained

Scientific role: stronger phenomenological nearest-family comparator to test whether the M07 P/H separator survives flexible smooth `w(a)`.

Branch:
- `w(a)=w0+wa(1-a)`;
- `epsilon0=1+w0`, `epsilon_a=wa`;
- CLASS CLP fluid, `cs2_fld=1`, `use_ppf=yes`;
- pure fluid closure: `Omega_Lambda=0`, `Omega_fld` inferred by CLASS.

#### M08 run #1 — preserved implementation failure

Actions `34391852165`, artifact digest `sha256:0c8cf5c2de8f3d4cc9f62d9a8574a60656db38caee297b01b6fdf1674517045e`.

All cases failed before cosmological evolution because both `Omega_Lambda` and `Omega_fld` were specified. Classification: configuration/closure failure only, not physical CPL failure.

Correction commit: `a3bb13aab2f181fed31882d31f819c9d0b0a7a36`.

#### M08 run #2 — local basis PASS_WITH_SCOPE

Actions `34394929596`, artifact digest `sha256:561bf0abc6b9247fe9bd517c142eeac5f96c677eab430993bd6cb1473e3a6a97`.

All five cases pass.
Reference self-floor: zero by construction relative to the matched CPL Lambda point.

Local combined P+H geometry:
- epsilon0 vs wa angle `9.1790225 deg`;
- singular values `{1.88297176, 0.09452819}`;
- `sigma2/sigma1 = 0.0502016`.

Central nonlinearity ratios at step 1e-3 are `3.44e-4` to `1.33e-3`.

Interpretation: nominally 2D CPL response is strongly anisotropic / near-one-dimensional. Parameter count != response rank.

### M08 absorbs the M07 constant-w P/H separator

Reproducible inputs:
- `M07_LOCAL_Q_DIRECTION.json`
- `M08_CPL_LOCAL_BASIS.json`
- calculator `code/w03_m08_absorb_m07.py`
- result `M08_M07_ABSORPTION_RESULT.json`.

One shared CPL parameter vector is fitted to the concatenated 35-node lnP + 7-node lnH M07 local q direction.

Best coefficients per unit q:
- `epsilon0/q = 0.1406534871`
- `wa/q = -0.2006790927`.

CPL residual fractions:
- combined P+H `1.107%`
- P `0.864%`
- H `1.993%`.

Same-solver constant-w-like epsilon0-only baseline:
- combined `15.820%`
- P `12.064%`
- H `29.149%`.

CPL improves the residual by about `14.3x` overall.

Classification:
`CPL_ABSORBS_M07_CROSSCHANNEL_SEPARATOR_WITH_SCOPE`.

This is a strong negative result for M07 **mechanism-level novelty**, not a physical failure of M07. M07 remains a controlled and within-family predictive benchmark, but the previously identified constant-w P/H separator is not robust against the stronger smooth-DE family manifold.

## DSIR main advancement / AD-002

Compared with W03 starting authority `328f2ca...`, inspected DSIR main `864952e...` is 23 commits ahead.

Relevant new Article-2 G5 state:
- prospective data-whitened cross-family stress contract frozen;
- synthetic fail-closed QA PASS;
- real covariance/operator machinery exists for ACT x unWISE 26-coordinate chain;
- cross-family theory -> exact same 26-coordinate provider matrix is **not yet bound**;
- real classifying G5 execution therefore remains blocked by interface/mapping, not covariance acquisition.

Hard rule adopted for M08 and later observation-space work:
A covariance alone is insufficient. Every compared family must pass through one exact frozen observation operator into the same coordinate vector/order/units/masks on which the covariance acts.

Do not call existing model-specific ShapeFit controls cross-family G5 closure.

## Future-model methodology state

Active construction methodology is now:
`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`.

Design ledger now contains **51 ACTIVE requirements, DP-0001..DP-0817**.

New M08/AD-002 requirements:
- DP-0815: profile the full implemented local comparator-family span/manifold, not one representative ray;
- DP-0816: exact common observation operator + covariance coordinate bridge required for cross-family observation-space promotion;
- DP-0817: closure/normalization conventions are explicit benchmark provenance and configuration failures remain distinct from physical failures.

M08 independently reinforces DP-0303 (parameter count != response rank) and DP-0504 (new microphysics != new observable direction).

## Immediate scientific continuation

The old question "does M07 differ from constant-w?" is closed as insufficiently adversarial.

Highest-value next frontier:

1. validate M08 local-basis step stability with a second preregistered step before treating the 2D span as a durable tangent plane;
2. then build an exact common M07/M08 observation-operator manifest satisfying AD-002 before any cross-family observational claim;
3. if the ACT x unWISE multi-family provider bridge becomes available in DSIR main, prefer reusing that exact 26-coordinate chain rather than inventing a new covariance map;
4. search for a gauge-robust response channel that lies outside the CPL span (scale dependence, temporal cross-relation, metric/slip only after representation robustness, nonlinear/high-k, tensor/coupling where defined);
5. use subsequent W03 mechanisms to begin promoting repeated design priors from ACTIVE to REINFORCED rather than only accumulating new priors.

## Non-negotiable

No zero imputation; no numerical failure=physical failure; no pairwise ray separation=family uniqueness; no independent comparator refits by block; no theory-angle=observational claim; no covariance without exact operator-coordinate compatibility; no retrospective B8; no silent authority rebase.
