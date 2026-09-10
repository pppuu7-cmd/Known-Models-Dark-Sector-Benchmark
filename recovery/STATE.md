# KMDSB current state / recovery handoff

Updated: 2026-09-10
Status: ACTIVE
Repository evidence overrides chat memory.

## 1. Mission

KMDSB is now a coverage program: pass all maintained **response-distinct known cosmological mechanism families** through the same mandatory-property funnel before deciding whether an existing family is sufficient, an adaptation/hybrid is needed, or a genuinely new dark-sector model is justified.

Do not interpret survival counts as probabilities of truth or failure counts as probabilities of falsity.

## 2. Authority chain

- W00-W02 numerical evidence: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 starting authority / M07 physical audits: `328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- W03 observation-method overlay from M08: `864952e1520d82473a9e976edfeb69f9899d174d`.
- later W03 overlay inspected for M09/M10: `bc28acc47cc5facba046741fd09f710ae8da9689`.
- exact transitions belong in `recovery/AUTHORITY_DELTAS.md`; never silently rebase old evidence.

## 3. Fresh-chat reading order

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
11. active model/wave files and current Actions.

## 4. Mandatory K0-K9 properties

- K0 authority/provenance
- K1 recoverable reference/decoupling limit
- K2 physical parameter geometry / quotient / tangent cone
- K3 conservation, gauge, frame and cosmological closure
- K4 numerical and residual robustness
- K5 multi-channel response and measured rank
- K6 strongest nearest-family manifold attack
- K7 exact common observation operator + covariance whitening/profile
- K8 quotient-surviving novelty + absolute profiled significance
- K9 prospective holdout

Existing B0-B9 audits remain the model-level records. K0-K9 are the cross-family coverage view.

## 5. Wave state

- W00 COMPLETE — reference/calibration and M01 nonidentifiability.
- W01 COMPLETE — IDE/GDM/WDM/f(R)/DCDM atlas.
- W02 COMPLETE — same-observable degeneracy attack; theory and observation graphs split.
- W03 ACTIVE — dark-energy mechanism census.
- W04 PLANNED — dark-matter census.
- W05 PLANNED — modified-gravity census.
- W06 PLANNED — unified/geometry/adversarial mixtures.
- W07 PLANNED — cross-family rigidity.
- W08 PLANNED — true holdout.
- W09+ PLANNED/ITERATIVE — escape search and literature-tail additions.

## 6. W03 closed/advanced results

### M07 canonical quintessence
`DSIR_PREDICTIVE_SUPPORT` with scope. Local quotient coordinate `q=lambda^2`. B5 is `NONIDENTIFIABLE` in corrected ShapeFit. Full 2D CPL absorbs its P+H theory response to about 1.11% residual; a common 15-coordinate ShapeFit bridge leaves about 1.067% whitened residual and `q=.09` only about `4.23e-4 sigma` after CPL profiling. Within-family prospective holdout is supported. Gauge/representation limitations keep B2/B7 partial.

### M08 CPL
Flexible 2D smooth-DE comparator. Local raw basis is rank-anisotropic (`sigma2/sigma1~0.0502`) and step-stable. It is the mandatory smooth-DE family manifold comparator for later W03 models where applicable.

### M09 native CLASS EDE
`BLOCKED_IMPLEMENTATION`. Upstream branch explicitly stops as unfinished, including at its zero point. Not a physical EDE falsification.

### M10 scalar EDE / CLASS_EDE
`DSIR_DISCRIMINATED` in scoped theory-response space. Stable early/scale response with nearly null late-time H. Same-solver full CPL attack leaves about 61.7% P+H residual; transferred broad-k shape residual about 83.3%; even S-only CPL refit leaves about 43.7%. K7/B5 observation binding remains OPEN; never identify the internal broad-k S diagnostic with observed ShapeFit `m+n` without an exact operator.

### M11 effective noncanonical / sound-speed representative
The standard-CLASS effective-fluid test is valid only as a response representative, not as generic covariant k-essence.

At frozen `w=-0.95` anchor, `q_s=1-c_s^2` gives a step-stable direction. It is far from constant-w and survives a same-anchor full CPL theory-manifold attack: about 92.56% combined P+H residual, about 90.53% P-block residual, and about 88.29% even for P-only CPL profiling. However its absolute secondary rank is tiny (`sigma2/sigma1~6.94e-4`). Therefore covariant validation was prospectively made mandatory before family promotion.

### M11b covariant CLASS_GSF validation — terminal provider attempt
Pinned provider: `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`, model 6.

Evidence:

1. Initial model-6 probe: build PASS and pure LCDM PASS, but every GSF case failed during background shooting/evolution with NDF15/LU `Possibly singular matrix`. Actions run `34429080377`, job `102720508845`, probe artifact SHA256 `5bf05fa2cacee1fb90cd8c15557b6bf1e94dcbe207b78c3058122752b3c8afda`.
2. Source audit showed model 6 implements `P=X^(n+1)/A^n - V0 phi^m`, `n=(1-cs2)/(2cs2)`, while the original probe started at zero kinetic energy. A prospectively frozen nonzero `phi'_ini` ladder `{1e-20,1e-18,1e-17,1e-16}` with both signs was then tested for reference-like and noncanonical cases. Run `34429876130`: LCDM PASS, all 16 GSF diagnostic cases exit 1; classification `RECOVERY_NO_EXECUTABLE_REGION_IN_FROZEN_LADDER`.
3. Provider-wide control then built the exact same source and ran the provider's **unmodified committed `dgf.ini`** after deleting pre-existing outputs. Run `34429997792`: build exit 0, DGF exit 0, fresh background and P(k) outputs produced; classification `PROVIDER_CONTROL_PASS`.
4. Repository search found no author-supplied working `gsf_parameters = 6` example at the pinned provider commit.

Therefore the current CLASS_GSF model-6 route is closed as **`BLOCKED_IMPLEMENTATION_PROVENANCE`**, not physical failure. Do not continue arbitrary post-hoc initial-condition tuning. See `models/covariant_kessence/audit.md`.

### M12 smooth phantom
Smooth phenomenological phantom is response-represented by the same local constant-w line with opposite orientation: acute angle about `0.03789 deg`, best-line residual about `0.0661%`. This does not erase the separate ghost/vacuum-stability problem of a minimal wrong-sign scalar.

### M13 crossing coverage split
M13a phenomenological PPF/CPL phantom-divide crossing is `REPRESENTED_BY:M08_WITH_SCOPE`. M13b true covariant multi-DOF quintom remains mandatory because entropy/isocurvature/relative-field perturbations can add response directions not contained in the 2D CPL fluid manifold.

## 7. Independent covariant k-essence candidate found after M11b blocker

Candidate repository: `Eladio-Moreno/k-essence-dynamics`.
Current repository authority inspected: commit `f3f010e1ed74c86ce6a431a435fa93988f749ee2` (2026-01-07).

Important provenance correction: the root README is essentially empty and the repository has only a few commits; do not call it validated solely because the code exists.

However `Cuadratico/` is a modified hi_class tree with explicit Scherrer-model source changes and an author-supplied `hi.ini`. Source inspection gives `X=y_sch+X0` and

`G2 = -F0 + F2*(X-X0)^2 - 0.5*m_phi^2*phi^2`,

with explicit background equations and hi_class stability tests. The author-supplied `hi.ini` contains a concrete Scherrer parameter point. This makes it a legitimate **provider-control candidate** for a new independent M11c attempt, but scientific use is forbidden until the exact unmodified author example builds/runs and provenance/reference gates are preregistered.

## 8. Coverage queue immediately after this handoff

W03 Tier-A:
- M11 effective response: theory survivor, covariant family promotion blocked pending independent validation.
- M11b CLASS_GSF model-6: terminal `BLOCKED_IMPLEMENTATION_PROVENANCE` for that provider/branch.
- M11c independent Scherrer/hi_class candidate: provider-control/preregistration next.
- M12: smooth response represented with scope.
- M13a: represented by M08; M13b covariant multifield quintom still open.
- M14 coupled quintessence: QUEUED.
- M15 generalized Chaplygin/unified dark fluid: QUEUED.

Tier-B W03: M16 running/interacting vacuum, M17 holographic DE, M18 ghost condensate.
Then W04/W05 queues from `model_family_census.csv` and `WAVE_TESTING_PROTOCOL_v0.2.md`.

## 9. New-model necessity criterion

Do not start the original model merely because some known families are weak, degenerate, blocked or pathological.

A benchmark-driven necessity claim requires sufficient census closure plus adversarial waves and at least one empirically relevant residual structure that survives all tested known-family manifolds/physically admissible combinations, common observation projection/covariance/nuisance profiling, numerical/gauge/systematic floors, physical/stability gates, and prospective holdout.

Until then: **new model motivated but not proven necessary**.

## 10. Non-negotiable rules

No zero-imputation. No implementation/numerical failure = physical falsification. No pairwise ray separation = family uniqueness. No parameter count = rank. No family-specific operator for a cross-family observation claim. No covariance without exact operator binding. No retrospective B8. No silent authority rebase. No model removed from census because implementation is inconvenient. Do not tune an external solver after a frozen recovery ladder has failed unless a new independently preregistered physical prescription justifies the new degree of freedom.

## 11. Immediate next actions

1. preregister and execute provider-control for `Eladio-Moreno/k-essence-dynamics@f3f010e.../Cuadratico`, using the author-supplied Scherrer `hi.ini` unchanged before any KMDSB retuning;
2. if provider-control PASSes, audit its exact Scherrer equations, stability variables, output channels and physical reference/decoupling path and preregister M11c scientific comparison to M11 effective sound-speed response;
3. if provider-control or provenance fails, retain M11 covariant family validation as blocked and do not tune it into a PASS;
4. in parallel advance M13b implementation/provenance or M14 if a clean independent implementation is available;
5. synchronize `model_family_census.csv`, `mandatory_properties_matrix.csv`, `RESTORE_FROM_NEW_CHAT.md` and `logs/research_log.md` after every terminal result;
6. do not declare `NEW_REQUIRED` before the coverage/holdout criterion is satisfied.
