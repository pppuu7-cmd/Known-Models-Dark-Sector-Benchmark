# KMDSB Wave Testing Protocol v0.1

Frozen: 2026-09-08

## Purpose

KMDSB is executed in waves, analogous in discipline to KMQGB but with DSIR-specific scientific gates. A wave is not just a folder: it is a frozen adversarial question asked of a defined model set under the same B0–B9 protocol.

## Wave record

Every wave must define:

- `wave_id` and scientific question;
- frozen DSIR authority snapshot(s);
- model queue and comparator graph;
- entry criteria;
- exit criteria;
- primary gates under pressure;
- allowed masks / valid response blocks;
- preregistered hard tests where applicable;
- result summary and design-prior delta;
- unresolved escape routes to be attacked by later waves.

## Wave lifecycle

`PLANNED -> ACTIVE -> CONDITIONALLY_COMPLETE -> COMPLETE`

A wave may also be `BLOCKED` if its central hard test cannot be executed with reproducible implementation/data.

Parallel preparation of the next wave is allowed, but a later wave cannot retroactively close an earlier wave's unresolved hard criterion.

## Frozen initial wave map

### Wave 0 — Calibration and semantics

Question: can KMDSB reproduce the DSIR reference origin and distinguish compatibility from observational identifiability without manufacturing novelty?

Models:
- M00 LambdaCDM;
- M01 smooth non-phantom DE / local wCDM ray.

Primary gates: B0–B5.

Exit criteria:
1. M00 null/reference control is reproduced with no fake residual novelty.
2. M01 passes or fails B0–B4 under the frozen C1 scope.
3. M01/B5 receives a hard observation-space classification using a documented operator/covariance, or an explicit `BLOCKED_DATA` classification with provenance of the missing object.

Wave 0 cannot be COMPLETE while M01/B5 is merely `PARTIAL`.

### Wave 1 — Baseline dark-sector control atlas

Question: do the frozen DSIR control families remain well-defined under one common model-audit protocol, and where do domain geometry / response-block masks first force nontrivial distinctions?

Queue:
- M02 interacting dark sector (C2 IDE);
- M03 generalized dark matter (C3 GDM);
- M04 thermal warm dark matter (C4 WDM);
- M05 designer f(R) (C5 MG comparator);
- M06 DCDM -> dark radiation (C6 withheld-family mechanism control).

M00 and M01 remain comparators but are not re-counted as new Wave-1 models.

Primary gates: B1–B6, with B8 bookkeeping for already-existing withheld evidence.

Wave-1 exit criteria:
1. Every queued model has `audit.md` + `result.json`.
2. Physical-domain geometry is explicit (including tangent cones / one-sided directions where needed).
3. Response masks are block-aware; no low-k/high-k zero padding.
4. Every raw-theory separator is labeled separately from observation-space discrimination.
5. A first comparator graph identifies which model pairs require slip, time, high-k, or other channels to break degeneracies.

### Wave 2 — Same-observable degeneracy attack

Question: which models can mimic one another in a restricted observable block but separate after adding orthogonal channels/time/sign information?

Entry condition: Wave-1 comparator graph exists.

### Wave 3 — Dark-energy family expansion

Question: how robust are DSIR conclusions under broader DE microphysics/parameterizations beyond the C1 local control?

### Wave 4 — Dark-matter family expansion

Question: how robust are response/mask/scale conclusions under additional DM mechanisms?

### Wave 5 — Modified-gravity expansion

Question: how many dark-sector signatures remain attribution-degenerate with gravity-sector modifications?

### Wave 6 — Adversarial mimicry

Question: can deliberately chosen known models evade the discriminants accumulated in Waves 0–5?

### Wave 7 — Cross-family rigidity

Question: which relations or residual-space structures survive across mechanisms rather than within one family?

### Wave 8 — True holdout

Question: do frozen cross-family candidates survive models/mechanisms that were not used to construct them?

### Wave 9+ — Escape search / iterative adversaries

Repeatedly search for known counterexamples, blind directions, comparator equivalences, domain failures, and mechanism classes that escape the current funnel.

## Cross-wave rules

1. Later evidence may revise a model audit, but the original wave result is preserved with an authority delta.
2. No percentage-of-models-false statistic is allowed from a convenience catalogue.
3. Wave survival counts are descriptive of the tested catalogue, not a measure over theory space.
4. Design priors are accumulated only with provenance to the model/gate that generated them.
5. A repeated failure pattern becomes a candidate methodology constraint only after at least one adversarial wave tests an escape route.
6. A candidate universal relation must survive a true holdout wave before being elevated toward a DSIR G8-style predictive claim.
