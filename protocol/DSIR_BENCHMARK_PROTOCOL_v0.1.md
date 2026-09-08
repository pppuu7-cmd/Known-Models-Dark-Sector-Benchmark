# KMDSB DSIR Benchmark Protocol v0.1

Frozen: 2026-09-08

## 1. Objective

Apply the DSIR response-first methodology to known models under a common, auditable sequence of gates. The benchmark is designed both to test existing theories and to harvest constraints/design priors for a future dark-sector model.

The protocol inherits the DSIR rule that theory labels are interpretations of a common response space, not privileged response coordinates.

## 2. Authority and frozen DSIR inputs

Each audit must record the DSIR commit or documented scope it relies on. v0.1 is aligned to the DSIR architecture in which:

- Data, Response and Theory layers are separated;
- covariance whitening is mandatory for rank/identifiability claims;
- `R_obs` and `R_model(pi)` are distinct;
- exact definitions, Bianchi/conservation identities, shared calibrations, gauge/frame artifacts and measurement-induced covariance directions are quotiented before residual-law claims;
- undefined cells are masked rather than set to zero;
- a discovery claim requires a prospective withheld test.

## 3. Per-model funnel

### B0 — Identity and provenance

**Question:** Is the tested object defined precisely enough to reproduce?

Required evidence:
- model/family name and scope;
- equations/action/effective parameterization or pinned implementation;
- parameter domain and reference point;
- solver/code provenance when numerical outputs are used.

Hard failure: the tested object changes definition during the audit or cannot be specified reproducibly.

### B1 — DSIR embedding / reference-limit gate

**Question:** Can the model be mapped into the frozen DSIR Theory→Response bookkeeping?

Required evidence:
- explicit reference limit/intersection with LambdaCDM or declaration that no such limit exists;
- response coordinates and valid blocks identified;
- no hidden zero-padding of unavailable channels.

Possible outcomes include `PASS`, `PASS_WITH_SCOPE`, `FAIL`, `BLOCKED_IMPLEMENTATION`, and `NOT_APPLICABLE`.

### B2 — Conservation, gauge/frame and bookkeeping gate

**Question:** Are conservation/Bianchi constraints and gauge/frame transformations handled consistently?

For internal dark-sector interactions, total conservation must be explicit. Raw gauge-specific perturbations are not accepted as common DSIR coordinates without an invariant mapping.

A failure here invalidates downstream physical comparison until repaired.

### B3 — Physical-domain and numerical-control gate

**Question:** Is the tested parameter domain physically admissible and numerically converged on the claimed block?

Checks may include positivity/stability, one-sided tangent cones, solver thresholds, zero/reference limits, resolution/precision sensitivity, and common-baseline consistency.

`BLOCKED_NUMERICAL` is distinct from a theory failure.

### B4 — Response-coverage and mask gate

**Question:** Which response directions are actually represented?

Record a block-aware mask over, as applicable:
- expansion/AP;
- matter/growth response;
- Weyl/lensing;
- metric slip;
- tensor/GW propagation;
- interaction/coupling observables;
- nonlinear or high-k response;
- time-domain/decay response.

Every missing cell is classified as `undefined`, `solver-limited`, `not-computed`, `near-null`, or `not-applicable`. Missing cells are never silently zero-filled.

### B5 — Reference identifiability gate

**Question:** In the identifiable subspace, can the model be distinguished from the LambdaCDM reference under the frozen covariance/noise treatment?

Rules:
- covariance whitening is required for observational rank claims;
- raw theory-space separation may be reported, but cannot be called observational distinguishability;
- tangent/Jacobian rank is distinguished from global linear-span rank;
- a null result may mean data blindness rather than model falsification.

LambdaCDM itself receives `NOT_APPLICABLE_CONTROL` here because it defines the reference origin.

### B6 — Nearest-comparator discrimination gate

**Question:** Can the candidate be separated from its strongest known alternative explanation on at least one valid common block?

The audit must name the comparator and the separating observable/response direction. A scale-only similarity that is broken by time evolution, sign, slip or another channel is recorded explicitly rather than collapsed into one scalar distance.

### B7 — Quotient-surviving residual novelty gate

**Question:** After removing exact identities, shared calibrations, gauge artifacts and known measurement degeneracies, is there a nontrivial residual relation or discriminator left?

Outcomes:
- `NO_NOVELTY_EXPECTED` for null controls;
- `NONIDENTIFIABLE` when the residual lies in an observational null direction;
- `SUPPORTED` only when the relation is not a bookkeeping identity.

Passing B7 is not yet a discovery claim.

### B8 — Prospective withheld prediction gate

**Question:** Does a frozen relation/discriminator survive a test that was not used to construct it?

Strength ladder:
1. withheld interpolation point within a known ray;
2. withheld regime/block;
3. withheld model family/mechanism;
4. genuinely future/new observational data.

The level must be recorded. Retrospective agreement cannot be relabeled as a prospective pass.

### B9 — Model-level synthesis / design-prior extraction

Produce two outputs:

1. **Model verdict** — what the DSIR funnel actually establishes about this model.
2. **Design-prior delta** — what a future dark-sector model must preserve, avoid, or add because of this audit.

No model receives a blanket `correct/incorrect` label from DSIR alone unless a frozen physical prediction is genuinely falsified within its claimed domain.

## 4. Allowed gate states

Use the controlled vocabulary in `STATUS_TAXONOMY.md`. Free-form verdicts may explain a state but may not replace it.

## 5. Evidence standard

Every nontrivial gate verdict must cite at least one of:
- a frozen DSIR hard result;
- a reproducible calculation committed in KMDSB;
- an external implementation/source with pinned provenance;
- a preregistered test and its output.

## 6. Overall classifications

The overall class is not a vote over gates. It describes the strongest justified interpretation:

- `CONTROL_PASS_WITH_SCOPE`
- `DSIR_COMPATIBLE`
- `DSIR_COMPATIBLE_NONIDENTIFIABLE`
- `DSIR_DISCRIMINATED`
- `DSIR_PREDICTIVE_SUPPORT`
- `BLOCKED`
- `PHYSICAL_DOMAIN_FAIL`
- `FROZEN_PREDICTION_FAIL`
- `INCONCLUSIVE`

## 7. Anti-overclaim rules

1. Raw theory-space angle/SVD separation != observational discrimination.
2. Low identifiable rank != proof of unification unless the observational operator has enough rank.
3. Catalog frequency != theory prior; use sensitivity to defensible family weights.
4. Undefined channels != zero response.
5. A one-family interpolation pass != a universal law.
6. A known model failing novelty != the theory being physically false.
7. No new-physics/discovery wording before a prospective B8-level test appropriate to the claim.

## 8. Benchmark iteration rule

Each iteration must update:
- the affected `audit.md` and `result.json`;
- `matrices/benchmark_matrix.csv` when a verdict changes;
- `logs/research_log.md`;
- `recovery/STATE.md` when the research frontier moves.

This keeps KMDSB recoverable from repository state alone.
