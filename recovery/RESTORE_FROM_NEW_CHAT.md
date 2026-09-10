# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-10
Purpose: resume the known-model dark-sector benchmark without relying on prior chat context.

## 0. Authority rule

If chat memory conflicts with repository evidence, repository evidence wins.
Historical results are never silently rebased to a newer DSIR commit.

Authority chain currently used:
- W00-W02: DSIR `e3276e2193f6a5200b541a194e3175356ae5a1c1`;
- W03 start / M07 physical evidence: `328f2ca80b724870b851c7fe6366cce1ca5086cd`;
- W03 observation-method overlay from M08: `864952e1520d82473a9e976edfeb69f9899d174d`;
- later W03 overlay inspected for M09/M10: `bc28acc47cc5facba046741fd09f710ae8da9689`.

See `recovery/AUTHORITY_DELTAS.md` for transitions.

## 1. Fresh-chat read order

1. `recovery/STATE.md`
2. `protocol/REQUIRED_PROPERTIES_COVERAGE_PROTOCOL_v0.1.md`
3. `matrices/model_family_census.csv`
4. `matrices/mandatory_properties_matrix.csv`
5. `protocol/WAVE_TESTING_PROTOCOL_v0.2.md`
6. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`
7. `matrices/benchmark_matrix.csv`
8. `matrices/design_prior_ledger.csv`
9. `logs/research_log.md`
10. current wave/model files and Actions runs.

Do not restore the project from README alone.

## 2. Mission

KMDSB is now a **coverage-driven test range**. The user directed that all known model classes be passed through the mandatory properties before deciding whether a new original dark-sector model is needed.

Operational definition of `all known`:
maintain and close all **response-distinct cosmological mechanism families**, rather than every paper title or parameter relabeling.

A family remains in the census even if implementation or observation mapping is blocked. Blockage is evidence, not permission to remove it.

## 3. Uniform mandatory properties

Every family receives K0-K9:
K0 provenance; K1 reference/decoupling; K2 physical geometry/quotient; K3 conservation/gauge/frame/closure; K4 numerical robustness; K5 multichannel response/rank; K6 nearest-family manifold attack; K7 exact common observation operator/covariance; K8 surviving novelty plus absolute significance; K9 prospective holdout.

Existing per-model B0-B9 files remain authoritative detailed audits.

## 4. Wave status

- W00 COMPLETE — reference/semantics.
- W01 COMPLETE — IDE/GDM/WDM/f(R)/DCDM baseline atlas.
- W02 COMPLETE — same-observable degeneracy attack.
- W03 ACTIVE — dark-energy mechanism census.
- W04 PLANNED — dark-matter mechanism census.
- W05 PLANNED — modified-gravity census.
- W06 PLANNED — unified/geometry and adversarial combinations.
- W07 PLANNED — cross-family rigidity.
- W08 PLANNED — true holdout.
- W09+ — iterative escape search.

Exact queues and completion rules: `protocol/WAVE_TESTING_PROTOCOL_v0.2.md`.

## 5. Important completed W03 evidence

### M07 canonical quintessence
- local physical quotient `q=lambda^2`;
- clean reference/numerical convergence after shooting audit;
- corrected ShapeFit B5 `NONIDENTIFIABLE`;
- level-1 within-family prospective holdout supported;
- full CPL M08 absorbs the M07 P+H response to about 1.11% theory residual;
- common ShapeFit CPL profiling leaves only about 1.067% whitened residual and q=.09 about `4.23e-4 sigma`;
- B2/B7 remain PARTIAL because small derived residuals have gauge/representation limitations.

### M08 CPL smooth w(a)
- 2D local basis is strongly anisotropic (`sigma2/sigma1~0.0502`) but the weak second direction matters;
- finite-difference step stability passed;
- central lesson: profile the full nearest-family manifold, not one representative ray.

### M09 native CLASS EDE
- upstream branch explicitly stops with `EDE implementation not finished`;
- terminal classification `BLOCKED_IMPLEMENTATION` in that solver branch;
- not a physical falsification of EDE.

### M10 CLASS_EDE axion-like scalar EDE
- supported implementation and shooting controls pass;
- low-k P and broad-k shape tangents converge;
- fEDE=.05 produces ~4.72% broad-k shape while late-time H response is ~9.3e-7;
- full same-solver CPL manifold leaves ~61.7% P+H residual and ~83.3% transferred broad-k shape residual; even S-only CPL fit leaves ~43.7%;
- current scoped verdict `DSIR_DISCRIMINATED` in theory-response space;
- K7/B5 observation-space mapping remains open because the exact theory->observed early-shape operator is not yet bound. Do not equate the internal broad-k S diagnostic to ShapeFit `m+n` by heuristic mapping.

## 6. Census program

Current census file: `matrices/model_family_census.csv`.
It includes tested M00-M10, mandatory W03 DE queue, W04 DM queue, W05 modified-gravity queue, unified/geometry alternatives, and response-equivalent particle-realization rows.

Current coverage matrix: `matrices/mandatory_properties_matrix.csv`.

Cold collisionless WIMP/FIMP/heavy-particle or QCD-axion realizations are represented by CDM only when they add no distinct cosmological response. Ultralight/free-streaming/interacting/decaying regimes get separate families.

## 7. M11 active frontier

M11 is an **effective k-essence/noncanonical sound-speed response representative**. It is not yet a claim to cover all covariant `P(phi,X)` Lagrangians.

Preregistered file:
`protocol/W03_M11_EFFECTIVE_KESSENCE_PREREGISTRATION_V0_1.md`.

Key geometry:
- exact w=-1 makes sound speed unidentifiable;
- therefore use pure Lambda vs fluid w=-1 for K1;
- use fixed anchor w=-0.95 for the noncanonical perturbation direction;
- define one-sided subluminal `q_s=1-cs2>=0`;
- compare q_s=.05 and .10 tangents;
- compare against smooth-w direction at the same anchor.

Workflow:
`.github/workflows/w03-m11-effective-kessence.yml`.
Analyzer:
`code/w03_m11_effective_kessence.py`.

At the time of this handoff Actions run `34426134138` is active.
Frozen gates may not be changed after output is seen.

## 8. New-model necessity criterion

Do not claim the new model is necessary until Tier-A known families are terminal and adversarial cross-family waves are executed.

A benchmark-based necessity result requires at least one empirically relevant residual structure that survives:
- all tested nearest-family manifolds and physically admissible known-family combinations;
- exact common observation projection/covariance/nuisance profiling;
- numerical/gauge/systematic floors;
- physical/stability checks;
- a prospective withheld prediction.

Until then the permitted conclusion is: `new model motivated but not proven necessary`.

## 9. Immediate continuation

1. finish Actions `34426134138`;
2. preserve result/artifact/logs even if a hard gate fails;
3. classify M11 reference, sound-speed convergence, rank and smooth-DE degeneracy;
4. if distinct, attack M11 with full CPL manifold;
5. decide whether a covariant kinetic M11b implementation is needed;
6. synchronize model audit/result, benchmark matrix, census matrix, design-prior evidence, STATE/RESTORE and research log;
7. continue M12 phantom -> M13 quintom -> M14 coupled quintessence -> M15 unified dark fluid before W03 Tier-A closure.

## 10. Never infer

- implementation failure = physical failure;
- parameter count = response rank;
- separation from one ray = family uniqueness;
- theory-space separation = observational discovery;
- existence of covariance = valid common observation bridge;
- within-family interpolation = universal predictive law;
- a model omitted because no solver is convenient = model covered;
- catalogue survival count = fraction of theory space that is true or false.
