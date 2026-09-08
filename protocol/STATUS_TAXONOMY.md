# KMDSB status taxonomy

Frozen vocabulary for benchmark v0.1.

## Per-gate states

- `PASS` — hard requirement met in the stated domain.
- `PASS_WITH_SCOPE` — requirement met, but only for an explicitly limited solver/domain/block.
- `PARTIAL` — meaningful evidence exists but the gate is not closed.
- `SUPPORTED` — positive evidence below hard-pass standard.
- `FAIL` — the frozen gate requirement is contradicted within its stated domain.
- `BLOCKED_IMPLEMENTATION` — no adequate reproducible implementation/embedding is presently available.
- `BLOCKED_NUMERICAL` — numerical control is inadequate for a verdict.
- `BLOCKED_DATA` — observational information is insufficient for the requested discrimination.
- `NONIDENTIFIABLE` — tested responses project into an observationally unresolved/null direction under the stated operator/covariance.
- `NOT_APPLICABLE` — the gate has no meaningful application to this model/scope.
- `NOT_APPLICABLE_CONTROL` — not applicable specifically because the model defines the null/reference control.
- `NO_NOVELTY_EXPECTED` — valid null-control outcome; absence of novelty is part of the test design.
- `OPEN` — not yet tested.
- `INCONCLUSIVE` — tested evidence conflicts or is insufficient for a defensible state.

## Overall model classes

- `CONTROL_PASS_WITH_SCOPE` — null/reference control reproduced in the stated scope.
- `DSIR_COMPATIBLE` — model is reproducibly embedded and survives the applicable bookkeeping/domain gates.
- `DSIR_COMPATIBLE_NONIDENTIFIABLE` — physically/bookkeeping compatible but not distinguishable in the tested observational subspace.
- `DSIR_DISCRIMINATED` — at least one hard valid response discriminator separates the model from the stated comparator(s); this is not yet predictive confirmation.
- `DSIR_PREDICTIVE_SUPPORT` — a frozen discriminator/relation survives an appropriate prospective withheld test.
- `BLOCKED` — strongest conclusion is an implementation, numerical, or data blockage.
- `PHYSICAL_DOMAIN_FAIL` — claimed parameter/domain point violates a frozen physical-admissibility requirement.
- `FROZEN_PREDICTION_FAIL` — a genuinely preregistered/frozen prediction is contradicted in its claimed domain.
- `INCONCLUSIVE` — no stronger classification is justified.

## Interpretation rule

Never convert `NONIDENTIFIABLE`, `BLOCKED_*`, or `NO_NOVELTY_EXPECTED` into “the model is false.” Only the evidence and the exact frozen gate/domain may support a physical falsification statement.
