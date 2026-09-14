# W03 F16 public provider discovery sweep v0.1

Date frozen: 2026-09-14
Family: F16 running/decaying vacuum Lambda(H)

## Purpose
Run a non-scientific, provenance-only GitHub discovery sweep for public source candidates implementing response-distinct running-vacuum laws. This sweep cannot promote K0/K1 and cannot classify physics.

## Frozen query lanes
Search GitHub repository and code indexes independently with these exact semantic targets:

1. `running vacuum CAMB cosmology`
2. `running vacuum CLASS cosmology`
3. `Lambda(H) CAMB cosmology`
4. `H0^4 H^-2 CAMB`
5. `rho_Lambda CAMB running vacuum`
6. `running vacuum CosmoMC`

Each lane must preserve raw API records for reproducibility. A candidate is only a discovery hit, not a provider, unless later human/source audit establishes an immutable public repository, exact commit/release, model law, perturbation prescription, and reference map.

## Fail-closed rules
- Search/API failure is `DISCOVERY_INFRASTRUCTURE_BLOCKED`, not absence of implementations.
- Zero results is `NO_CANDIDATE_IN_FROZEN_QUERY_LANE`, not evidence that no public implementation exists.
- Do not execute candidate code in this sweep.
- Do not infer family identity from repository name alone.
- Do not promote K0/K1 from search results.

## Next gate
Aggregate unique repositories/files, then source-audit only candidates that visibly contain a genuine H-dependent vacuum law or paper-linked implementation. If none qualify, retain F16 provenance-blocked and move to the next independent W03 family.
