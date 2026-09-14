# W03 F16 focused running-vacuum provider discovery v0.1

Status: PROSPECTIVELY FROZEN
Date: 2026-09-14

## Purpose
Find a genuinely response-distinct public running/decaying-vacuum implementation for F16 after the broad discovery sweep produced false positives and toy/background-only scaffolding.

## Frozen scope
Discovery/source-audit only. This protocol cannot promote K0/K1, cannot classify a theory false, and cannot execute a scientific parameter grid.

Search lanes are independent and may run in parallel. Each lane must search public GitHub code using exact mechanism phrases/signatures rather than generic `running`/`vacuum` tokens:

1. `running vacuum` + `H^2`/`H2` + cosmology
2. `rho_Lambda`/`rhoLambda` + `H^2` + `nu`
3. `Lambda(H)` + cosmology
4. `dot H`/`Hdot` + vacuum + cosmology
5. `RVM` + `CLASS`/`CAMB`
6. `running vacuum model` + perturbation/conservation
7. `vacuum energy` + `nu` + `H0` + `Omega_m`
8. `rho vacuum` + `Hubble` + `matter exchange`

## Candidate acceptance for source review
A candidate enters exact-source review only if the matched repository/file shows at least one of:
- explicit cosmological law `rho_Lambda(H)` / `Lambda(H)` / equivalent H-dependent vacuum density;
- explicit H^2 and/or dotH vacuum term with cosmological density parameters;
- implemented vacuum-matter conservation/exchange equations tied to that law;
- perturbation equations or an explicit binding to CLASS/CAMB/another perturbation solver for that law.

Names, bibliography entries, particle-physics RG running, Higgs vacuum stability, wordlists, and generic dark-energy prose are rejected mechanically.

## Provider qualification ceiling
Even a source-review candidate is not a K0 PASS until an exact immutable commit is pinned and the implementation scope, equations, free parameters, LambdaCDM/reference limit, conservation split, perturbation prescription, and output channels are documented. Background-only/toy implementations are `PROVENANCE_LEAD_ONLY`.

## Fail-closed outcomes
- `F16_FOCUSED_DISCOVERY_SOURCE_COMPLETE_CANDIDATE_FOUND`
- `F16_FOCUSED_DISCOVERY_PROVENANCE_LEADS_ONLY`
- `F16_FOCUSED_DISCOVERY_NO_QUALIFYING_PUBLIC_SOURCE`
- `F16_FOCUSED_DISCOVERY_INFRASTRUCTURE_BLOCKED`

None implies physical falsification or NEW_REQUIRED.
