# KMDSB current state / recovery handoff

Updated: 2026-09-10
Status: ACTIVE
Repository evidence overrides chat memory.

## 1. Authority chain

- W00-W02 numerical evidence: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 starting authority / M07 physical audits: `328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- W03 observation-method overlay used from M08 onward: `864952e1520d82473a9e976edfeb69f9899d174d`.
- later W03 overlay inspected for M09/M10: `bc28acc47cc5facba046741fd09f710ae8da9689`.
- exact transitions belong in `recovery/AUTHORITY_DELTAS.md`; never silently rebase old model evidence.

## 2. Active governing documents

Read in this order in a fresh chat:
1. `recovery/RESTORE_FROM_NEW_CHAT.md`
2. this file
3. `protocol/REQUIRED_PROPERTIES_COVERAGE_PROTOCOL_v0.1.md`
4. `matrices/model_family_census.csv`
5. `matrices/mandatory_properties_matrix.csv`
6. `protocol/WAVE_TESTING_PROTOCOL_v0.2.md`
7. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`
8. `matrices/benchmark_matrix.csv`
9. `matrices/design_prior_ledger.csv`
10. `logs/research_log.md`
11. active model/wave files.

## 3. Project mission changed from convenience catalogue to coverage program

User directive on 2026-09-10: pass **all known model classes** through the mandatory properties before deciding whether a new original model is needed.

KMDSB now defines "all known" operationally as all maintained **response-distinct cosmological mechanism families**, not every paper title or parameter relabeling.

A new top-level family is required when it adds a new cosmological DOF, interaction/conservation law, characteristic scale/time law, perturbation closure, metric/tensor response, nonlinear response or other response direction that is not represented by an existing family manifold.

Cold collisionless particle realizations that are cosmologically response-equivalent to CDM can be marked `REPRESENTED_BY:M00`; if an escape channel is found, they are promoted to their own benchmark family.

Current census: `matrices/model_family_census.csv`.
Current uniform property matrix: `matrices/mandatory_properties_matrix.csv`.

## 4. Mandatory K0-K9 properties for every family

- K0 authority/provenance
- K1 recoverable reference/decoupling limit
- K2 physical parameter geometry / exact quotient
- K3 conservation, gauge, frame and cosmological closure
- K4 numerical robustness / residual robustness
- K5 multi-channel response and measured rank
- K6 strongest nearest-family manifold attack
- K7 exact common observation operator + covariance whitening/profile
- K8 quotient-surviving novelty + absolute profiled significance
- K9 prospective holdout

Existing B0-B9 model audits remain authoritative model records; K0-K9 are the cross-model mandatory-properties view.

## 5. Wave state

- W00 COMPLETE — calibration/reference + M01 nonidentifiability.
- W01 COMPLETE — IDE/GDM/WDM/f(R)/DCDM atlas.
- W02 COMPLETE — same-observable degeneracy attack; theory/observation graph split.
- W03 ACTIVE — dark-energy mechanism census.
- W04 PLANNED — dark-matter mechanism census.
- W05 PLANNED — modified-gravity census.
- W06 PLANNED — unified/geometry + adversarial mixtures.
- W07 PLANNED — cross-family rigidity.
- W08 PLANNED — true holdout.
- W09+ PLANNED/ITERATIVE — escape search and literature-tail additions.

Active wave planning authority: `protocol/WAVE_TESTING_PROTOCOL_v0.2.md`.

## 6. W03 tested results through M10

### M07 canonical quintessence
Overall `DSIR_PREDICTIVE_SUPPORT`.
- controlled local quotient coordinate `q=lambda^2`;
- B5 `NONIDENTIFIABLE` in corrected ShapeFit control;
- within-family prospective holdout supported;
- full 2D CPL M08 absorbs its P+H theory direction to about 1.11% residual;
- in one common 15-coordinate ShapeFit bridge CPL profiling leaves only about 1.067% whitened residual and q=.09 about `4.23e-4 sigma`;
- small derived metric/growth residuals retain gauge/representation limitations; B2/B7 remain PARTIAL.

Interpretation: clean microphysics + predictive interpolation do not imply mechanism-level observational novelty.

### M08 CPL smooth time-varying DE
Overall `DSIR_COMPATIBLE`.
- local P+H basis angle about `9.179 deg`;
- raw `sigma2/sigma1=0.0502`, demonstrating parameter count != response rank;
- step-stable at 1e-3 -> 5e-4;
- common ShapeFit whitening changes geometry and strongly absorbs M07.

### M09 solver-native CLASS EDE implementation control
Overall `BLOCKED`.
Pinned upstream CLASS EDE branch explicitly stops with `EDE implementation not finished`; zero-point included. This is `BLOCKED_IMPLEMENTATION`, not physical falsification of EDE.

### M10 CLASS_EDE axion-like scalar EDE
Overall current scoped verdict `DSIR_DISCRIMINATED` in theory-response space.
- published CLASS_EDE implementation used as separate model, not a hidden patch to M09;
- shooting reaches requested fEDE/log10zc at ~1e-7--1e-6 accuracy;
- local low-k P tangent convergence ~0.31%, broad-k shape tangent ~0.99%;
- at fEDE=.05, broad-k shape reaches ~4.72% while late-time H response is only ~9.3e-7;
- same-solver full 2D CPL attack leaves ~61.7% P+H residual;
- transferred broad-k S residual ~83.3%; even S-only CPL refit leaves ~43.7%.

M10 K7/B5 observational promotion remains OPEN because the exact theory->ShapeFit early-shape operator binding has not yet been established. Do not map the internal broad-k S diagnostic to observed `m+n` heuristically.

## 7. New census-driven coverage queue

Tier-A W03 remaining:
- M11 effective/covariant k-essence response class
- M12 phantom scalar DE
- M13 quintom / phantom-divide crossing
- M14 coupled quintessence
- M15 generalized Chaplygin / unified dark fluid

Tier-B W03:
- M16 running/interacting vacuum
- M17 holographic DE
- M18 ghost-condensate kinetic branch

W04 and W05 full queues are frozen in `WAVE_TESTING_PROTOCOL_v0.2.md` and `model_family_census.csv`.

## 8. M11 ACTIVE NOW

M11 first-stage scope is an **effective k-essence/sound-speed response representative**, not a claim to cover the entire covariant `P(phi,X)` theory space.

Preregistration:
`protocol/W03_M11_EFFECTIVE_KESSENCE_PREREGISTRATION_V0_1.md`.

Reason for stratified geometry:
At exact `w=-1`, DE perturbations vanish, so `cs2` is unidentifiable. M11 therefore separates:
1. K1 reference branch `w->-1`, comparing pure LambdaCDM with fluid `w=-1, cs2=1`;
2. K5 sound-speed branch on frozen anchor `w=-0.95`.

One-sided subluminal coordinate:
`q_s = 1-cs2 >= 0`.

Frozen steps:
- q_s=.05 (`cs2=.95`)
- q_s=.10 (`cs2=.90`)
with convergence requirement <=10% relative norm and <=3 deg direction change.

Smooth-w comparator at the same anchor uses w=-.949 / -.951, step .001.

Pinned solver:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Workflow:
`.github/workflows/w03-m11-effective-kessence.yml`.
Analyzer:
`code/w03_m11_effective_kessence.py`.

Current Actions run at this handoff:
`34426134138` — in progress, building pinned CLASS.

Do not change anchor/steps/hard thresholds after successful solver output.

## 9. New-model necessity criterion

Do not start the original model merely because individual known families are weak or degenerate.

A benchmark-driven necessity claim requires Tier-A closure plus adversarial waves and at least one empirically relevant residual structure that:
- survives all tested known-family manifolds and physically admissible combinations;
- survives exact common observation projection/covariance/nuisance profiling;
- lies above numerical/gauge/systematic floors;
- has acceptable physical/stability domain;
- supports a prospective withheld prediction.

Until then: `new model motivated but not proven necessary`.

## 10. Non-negotiable rules

No zero-imputation; no numerical/implementation failure = physical failure; no pairwise ray separation = family uniqueness; no parameter count = rank; no separate comparator fit per claimed response block; no theory-space angle = observational claim; no covariance without exact coordinate/operator binding; no retrospective B8; no silent authority rebase; no model removed from census because implementation is inconvenient.

## 11. Immediate next actions

1. finish M11 run `34426134138` and preserve artifact/logs;
2. classify pure-Lambda vs fluid-zero reference gate;
3. classify sound-speed convergence/non-null and rank against smooth-w at the same anchor;
4. if M11 effective response is distinct, attack it with full CPL manifold before any novelty statement;
5. decide whether a covariant `P(phi,X)`/kinetic implementation is required as a separate M11b subcase;
6. update benchmark/census/K-matrix/model audit/result/recovery/log;
7. continue sequentially M12 -> M15 before W03 Tier-A closure.
