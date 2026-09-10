# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-10
Purpose: resume the known-model dark-sector benchmark without relying on prior chat context.

## 0. Authority rule

If chat memory conflicts with repository evidence, repository evidence wins. Historical results are never silently rebased to a newer DSIR commit.

Authority chain:
- W00-W02: DSIR `e3276e2193f6a5200b541a194e3175356ae5a1c1`;
- W03 start / M07 physical evidence: `328f2ca80b724870b851c7fe6366cce1ca5086cd`;
- W03 observation-method overlay from M08: `864952e1520d82473a9e976edfeb69f9899d174d`;
- later W03 overlay inspected for M09/M10: `bc28acc47cc5facba046741fd09f710ae8da9689`.

See `recovery/AUTHORITY_DELTAS.md` for transitions.

## 1. Fresh-chat read order

1. `recovery/STATE.md`
2. this file
3. `protocol/REQUIRED_PROPERTIES_COVERAGE_PROTOCOL_v0.1.md`
4. `matrices/model_family_census.csv`
5. `matrices/mandatory_properties_matrix.csv`
6. `protocol/WAVE_TESTING_PROTOCOL_v0.2.md`
7. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`
8. `matrices/benchmark_matrix.csv`
9. `matrices/design_prior_ledger.csv`
10. `logs/research_log.md`
11. current wave/model files and live Actions.

Do not restore the project from README alone.

## 2. Mission and coverage definition

KMDSB is a **coverage-driven test range**. The user requires all known model classes to pass through the same mandatory properties before a decision on a new original model.

Operationally, `all known` means all maintained **response-distinct cosmological mechanism families**, not every paper title. A new top-level family is required when a model adds a new degree of freedom, conservation/interaction law, characteristic scale/time law, perturbation closure, metric/tensor response or other response direction not represented by an existing family manifold.

A family stays in the census even if implementation or observation mapping is blocked. `BLOCKED` is evidence, not removal permission.

## 3. Mandatory K0-K9

Every family receives:
K0 provenance; K1 reference/decoupling; K2 physical geometry/quotient; K3 conservation/gauge/frame/closure; K4 numerical robustness; K5 multichannel response/rank; K6 strongest nearest-family manifold attack; K7 exact common observation operator/covariance; K8 surviving novelty plus absolute profiled significance; K9 prospective holdout.

Existing B0-B9 model audits remain the detailed authority.

## 4. Wave state

- W00 COMPLETE — reference/semantics.
- W01 COMPLETE — IDE/GDM/WDM/f(R)/DCDM atlas.
- W02 COMPLETE — degeneracy attack with theory/observation graph split.
- W03 ACTIVE — dark-energy census.
- W04 PLANNED — dark-matter census.
- W05 PLANNED — modified gravity.
- W06 PLANNED — unified/geometry/adversarial combinations.
- W07 PLANNED — cross-family rigidity.
- W08 PLANNED — true holdout.
- W09+ — iterative escape search.

Exact queues: `protocol/WAVE_TESTING_PROTOCOL_v0.2.md` and `matrices/model_family_census.csv`.

## 5. W03 core evidence

### M07 canonical quintessence
Local quotient `q=lambda^2`. B5 `NONIDENTIFIABLE`. Full CPL absorbs P+H theory response to ~1.11%; in one common ShapeFit bridge it leaves ~1.067% whitened residual and `q=.09` only ~`4.23e-4 sigma` after CPL profiling. Within-family holdout supported. B2/B7 remain partial because small derived residuals have gauge/representation limitations.

### M08 CPL
2D smooth-DE comparator, strongly anisotropic but step-stable. Its weak second direction destroys apparent M07 mechanism novelty. Durable rule: profile the full nearest-family manifold, not one ray.

### M09 native CLASS EDE
Terminal `BLOCKED_IMPLEMENTATION`: upstream branch explicitly stops as unfinished. Not EDE physics falsification.

### M10 CLASS_EDE scalar EDE
Stable early/scale response with nearly null late-time H. Same-solver full CPL attack leaves ~61.7% P+H residual; transferred broad-k shape residual ~83.3%; even S-only CPL refit leaves ~43.7%. Current scoped theory-space verdict `DSIR_DISCRIMINATED`. K7 remains open: never equate internal broad-k S to observed ShapeFit `m+n` without an exact operator.

### M11 effective k-essence / variable sound speed
Effective-fluid representative only. At `w=-0.95`, one-sided `q_s=1-cs2` response is step-stable and survives full local CPL attack (~92.56% combined P+H residual; ~90.53% P residual; ~88.29% even for P-only CPL fit), but its absolute secondary rank is tiny (`sigma2/sigma1~6.94e-4`). Covariant validation was therefore frozen as mandatory before family promotion.

### M11b first covariant provider attempt — CLASS_GSF model 6
Pinned `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`.

- initial probe run `34429080377`: provider builds and LCDM runs; every model-6 GSF case fails in background shooting/evolution with an NDF15 LU singular-matrix error;
- source audit: model 6 uses `P=X^(n+1)/A^n - V0 phi^m`, `n=(1-cs2)/(2cs2)` and the original probe had zero kinetic initial state;
- prospectively frozen nonzero kinetic-seed ladder `{1e-20,1e-18,1e-17,1e-16}`, both signs, run `34429876130`: LCDM passes, all 16 GSF diagnostic cases fail; classification `RECOVERY_NO_EXECUTABLE_REGION_IN_FROZEN_LADDER`;
- provider control run `34429997792`: exact pinned source builds and the provider's unmodified committed model-1 `dgf.ini` runs with fresh background and P(k); classification `PROVIDER_CONTROL_PASS`;
- no author-supplied `gsf_parameters = 6` working example was found at the pinned commit.

Therefore that provider/branch is **`BLOCKED_IMPLEMENTATION_PROVENANCE`** for M11b. Do not keep tuning initial conditions post hoc. This is not k-essence falsification. Authority: `models/covariant_kessence/audit.md`.

### M12 smooth phantom
Phenomenological smooth phantom is represented by the same local constant-w response line with opposite orientation: acute angle ~`0.03789 deg`, best-line residual ~`0.0661%`. Minimal wrong-sign scalar ghost/vacuum-stability pathology remains a separate physical issue.

### M13 crossing split
M13a smooth PPF/CPL crossing is `REPRESENTED_BY:M08_WITH_SCOPE`. M13b true covariant multi-DOF quintom remains mandatory because additional entropy/isocurvature/relative-field perturbations can add response directions beyond CPL.

## 6. Independent Scherrer code discovered — bookkeeping classification matters

Repository inspected: `Eladio-Moreno/k-essence-dynamics@f3f010e1ed74c86ce6a431a435fa93988f749ee2`.

The root README is nearly empty and the repository has only a few commits, so existence alone is not scientific validation. However `Cuadratico/` is a modified hi_class tree with explicit source code for a Scherrer-type scalar:

`X = y_sch + X0`

`G2 = -F0 + F2*(X-X0)^2 - 0.5*m_phi^2*phi^2`.

It includes an author-supplied `hi.ini`, and standard hi_class scalar/tensor ghost/gradient stability checks are enabled there.

Crucial classification: this author configuration has `Omega_cdm=0` and `DM_schm=0.26`, so the scalar supplies both dark-matter-like and dark-energy-like components. It is therefore **not a clean M11 DE-only covariant validation**. Treat it as a candidate unified-dark-sector/Scherrer subfamily for M15/W06 unless a distinct DE-only branch is prospectively demonstrated. Do not use it to promote M11.

## 7. Current coverage frontier

- F11/M11: theory-response survivor; covariant family promotion BLOCKED after first provider attempt.
- M11b CLASS_GSF model 6: terminal provider-specific `BLOCKED_IMPLEMENTATION_PROVENANCE`.
- Scherrer modified-hi_class implementation: candidate for unified dark-sector M15, provider-control still required before science.
- F12/M12: smooth phantom response represented with scope.
- F13/M13: partial; phenomenological crossing represented, true covariant multifield quintom open.
- F14/M14 coupled quintessence: queued; a promising public implementation with explicit CLASS source and author `iDM.ini` has been identified but must be pinned/preregistered before use.
- F15/M15 unified dark fluid: queued, with Scherrer code now a candidate alongside generalized Chaplygin.

## 8. New-model necessity rule

Do not claim `NEW_REQUIRED` because some models are weak, degenerate, blocked or pathological. A benchmark-based necessity verdict requires sufficient census closure plus adversarial cross-family waves and at least one empirically relevant residual structure that survives known-family manifolds/combinations, exact common observation projection/covariance/nuisance profiling, numerical/gauge/systematic floors, stability/domain checks and a prospective withheld prediction.

Until then the only permitted global conclusion is: **new model motivated but not proven necessary**.

## 9. Immediate continuation

1. do not reopen arbitrary CLASS_GSF model-6 tuning; keep that M11b provider blocker terminal;
2. run only a preregistered provider-control for the Scherrer author `hi.ini`, and classify it under unified-dark-sector bookkeeping rather than M11 unless evidence shows a DE-only branch;
3. inspect/pin a clean M14 coupled-quintessence provider (candidate: public `kabeleh/iDM`) and require its author-supplied `iDM.ini` to reproduce before any KMDSB parameter grid;
4. continue M13b provenance search independently, without treating CPL crossing as true multifield coverage;
5. update census/K-matrix/STATE/RESTORE/log after terminal results;
6. never change frozen scientific thresholds after seeing results.

## 10. Never infer

- implementation failure = physical failure;
- parameter count = response rank;
- separation from one ray = family uniqueness;
- theory-space separation = observational discovery;
- covariance existence = valid common observation bridge;
- within-family interpolation = universal predictive law;
- unavailable solver = family covered;
- unified scalar bookkeeping = DE-only k-essence validation;
- catalogue survival counts = fraction of theories true/false.
