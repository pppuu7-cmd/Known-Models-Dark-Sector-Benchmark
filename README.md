# KMDSB — Known Models Dark-Sector Benchmark

A controlled test range for passing known dark-sector and modified-gravity model families through the DSIR funnel.

## Mission

KMDSB is now explicitly **coverage-driven**. Before deciding whether an original dark-sector model is needed, the project maintains a census of response-distinct known cosmological mechanism families and passes each family through the same mandatory properties.

"All known models" is operationalized as **all maintained response-distinct mechanism families**, not every paper title or parameter relabeling. A new family ID is added when a construction introduces a genuinely new cosmological degree of freedom, interaction/conservation law, characteristic scale/time law, perturbation closure, metric/tensor response, nonlinear response or other response direction not represented by the current family manifold.

Cold collisionless particle realizations with the same cosmological response can be represented by the CDM family; any variant that escapes in an orthogonal channel is promoted to a separate benchmark family.

## Governing protocols

- `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md` — detailed per-model B0-B9 funnel.
- `protocol/REQUIRED_PROPERTIES_COVERAGE_PROTOCOL_v0.1.md` — uniform all-family K0-K9 coverage contract and new-model necessity criterion.
- `protocol/WAVE_TESTING_PROTOCOL_v0.2.md` — active census-driven wave plan.
- `protocol/STATUS_TAXONOMY.md` — semantic distinction between PASS, FAIL, NONIDENTIFIABLE, BLOCKED and related states.
- `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md` — evidence-fed construction methodology for a future original model.

## Mandatory properties K0-K9

Every family is tested for:

K0 provenance/authority; K1 recoverable reference or decoupling limit; K2 physical parameter geometry and exact quotient; K3 conservation/gauge/frame/closure; K4 numerical and residual robustness; K5 multi-channel response and measured rank; K6 strongest nearest-family manifold attack; K7 exact common observation operator/covariance whitening and profiling; K8 quotient-surviving novelty plus absolute profiled significance; K9 prospective holdout.

A blocked implementation or missing observation bridge remains in the matrix. It is not silently removed and is not called a physical falsification.

## Coverage files

- `matrices/model_family_census.csv` — maintained known-family census.
- `matrices/mandatory_properties_matrix.csv` — K0-K9 state for every family.
- `matrices/benchmark_matrix.csv` — detailed B0-B9 tested-model summary.
- `matrices/design_prior_ledger.csv` — requirements learned for a future original model.
- `matrices/design_prior_promotion_log.md` — evidence behind ACTIVE/REINFORCED promotion.

## Wave state

- W00 Calibration and semantics — **COMPLETE**.
- W01 Baseline dark-sector atlas — **COMPLETE**.
- W02 Same-observable degeneracy attack — **COMPLETE**.
- W03 Dark-energy mechanism census — **ACTIVE**.
- W04 Dark-matter mechanism census — PLANNED.
- W05 Modified-gravity census — PLANNED.
- W06 Unified/geometry and adversarial combinations — PLANNED.
- W07 Cross-family rigidity — PLANNED.
- W08 True holdout — PLANNED.
- W09+ Escape search / literature-tail adversaries — iterative.

## Current W03 highlights

M07 canonical quintessence is physically/numerically controlled and has level-1 predictive support, but its late-time response is almost entirely absorbed by the flexible M08 CPL manifold; in the common ShapeFit control its largest tested deformation is only about `4.23e-4 sigma` after CPL profiling.

M09 upstream CLASS EDE is an explicit implementation blocker (`EDE implementation not finished`), not a physical EDE falsification.

M10 published CLASS_EDE scalar early dark energy is the strongest W03 theory-response survivor so far: a same-solver full CPL attack leaves about `61.7%` P+H residual and `83.3%` transferred broad-k shape residual; observational K7 remains open until an exact early-shape operator is bound.

M11 effective k-essence/noncanonical sound-speed response is now active under a preregistered stratified test. At exact `w=-1` sound speed is unidentifiable, so the noncanonical direction is tested at frozen anchor `w=-0.95` using one-sided `q_s=1-c_s^2` convergence and a smooth-w comparator at the same anchor.

## Scientific boundary

KMDSB does **not** infer a percentage of theory space that is true or false from catalogue counts. `NONIDENTIFIABLE`, `BLOCKED_IMPLEMENTATION`, `BLOCKED_OPERATOR_BINDING`, numerical failure, physical-domain failure and a genuinely falsified frozen prediction are different outcomes.

The permitted interim conclusion remains:

> a new model is increasingly motivated by the benchmark, but it is not proven necessary until the Tier-A known-family census and cross-family adversarial/observation/holdout gates are closed.

## Recovery

Start a fresh chat with `recovery/STATE.md`, then `recovery/RESTORE_FROM_NEW_CHAT.md`. Repository evidence wins if conversation memory disagrees.
