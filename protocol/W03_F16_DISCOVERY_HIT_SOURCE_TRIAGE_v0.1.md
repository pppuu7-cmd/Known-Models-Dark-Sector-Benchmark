# W03 F16 discovery-hit source triage v0.1

Frozen: 2026-09-14
Target: F16 running/decaying vacuum Lambda(H)
Parent discovery: Actions run `34794527520`, aggregate artifact `10329107420` (`f16-provider-discovery-aggregate`), which contains 53 public GitHub code hits from six prospectively frozen query lanes.

## Purpose

Convert the parent discovery pool into a reproducible, exact-commit candidate list without promoting any hit to K0 or K1. A search hit is not a provider.

## Frozen candidate unit and deduplication

1. Consume only the immutable aggregate from run `34794527520`; do not issue new discovery queries in this gate.
2. Group code hits by repository full name.
3. Exclude this KMDSB repository itself and empty repository identifiers.
4. Select at most one representative matched path per repository, using lexical URL order inherited from the aggregate.
5. Audit at most the first 20 unique repositories in case-insensitive repository-name order. This cap is computational only and is fixed before source inspection.

## Exact pinning

For every selected repository, resolve its current default branch and the exact HEAD commit SHA at execution. Fetch the matched file at that exact SHA. Record repository, default branch, exact SHA, matched path, source-fetch status, source size, and source hash.

## Frozen source-screen signals

This gate is a triage screen only. Record literal/source-level evidence for these categories:

- solver/ecosystem token: CAMB, CLASS, CosmoMC, cosmomc, camb, class;
- running-vacuum tokens: running vacuum, running_vacuum, rho_Lambda/rho_lambda, Lambda(H)/lambda_h;
- H-dependent law hints: simultaneous occurrence of an H/H0-like token with nu/vacuum/Lambda-like token;
- inverse-H/special-RVM hints: H^-2, H**-2, /H^2, H0^4, or equivalent plain-text strings;
- perturbation/conservation hints: perturb, delta, conservation, interaction, transfer, Q_mu, continuity.

No semantic equivalence is inferred from token presence alone.

## Classification

Per repository:

- `F16_SOURCE_HIT_FETCHED_TRIAGE_ONLY` if exact-SHA source fetch succeeds;
- `F16_SOURCE_HIT_METADATA_ONLY` if repository pin resolves but the matched path cannot be fetched at that pin;
- `F16_SOURCE_HIT_AUDIT_INFRASTRUCTURE_BLOCKED` if exact pinning itself cannot be resolved.

Aggregate candidate priority is purely mechanical:

- `HIGHER_SOURCE_REVIEW_PRIORITY` only when a fetched source has both a running-vacuum token and a solver/ecosystem token, or an explicit inverse-H/special-RVM hint;
- otherwise `LOWER_SOURCE_REVIEW_PRIORITY`.

## Claim ceiling

This gate cannot establish K0, K1, perturbation closure, physical viability, or falsification. It only produces exact-commit source-review candidates. Any candidate selected for provider validation requires a new preregistration that freezes the exact public commit, equations/law, sector conservation split, perturbation prescription, reference limit, grids, and thresholds before execution.
