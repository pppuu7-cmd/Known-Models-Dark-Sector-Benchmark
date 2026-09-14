# W04 F19 independent ultralight-axion/FDM provider discovery v0.1

Frozen: 2026-09-14
Status: PREREGISTERED
Family: F19/M19 fuzzy / ultralight axion dark matter

## Motivation
The two already-audited axionCAMB-lineage implementations execute finite-ULA controls but inherit a singular exact-zero-axion reference path. Existing finite-fraction/internal-asymptotic convergence evidence does not establish the external pure-CDM K1 identity. This tranche therefore searches for an **independent implementation lineage** with a documented regular zero-ULA/pure-CDM reference map.

## Frozen exclusions
Do not promote or count as an independent provider:
- `Ra-yne/AxiECAMB` or `dgrin1/axionCAMB` and direct forks/lineage copies;
- paper metadata, notebooks with no executable solver, review prose, catalogs, RSS/arXiv mirrors;
- transfer-function fitting formulae without a dynamical perturbation implementation;
- background-only scalar-field code lacking linear perturbations;
- generic axion particle-physics code without cosmological Boltzmann/growth response.

## Source-complete review requirements
A candidate can advance only if exact source review can identify all of:
1. public immutable repository commit/release;
2. explicit ULA/FDM/scalar-DM background or density evolution;
3. linear perturbation / Boltzmann / transfer response carrying the ULA/FDM degree of freedom;
4. an explicit parameter controlling the ULA abundance/fraction and a documented or source-visible zero-abundance/pure-CDM limit;
5. no dependence on the already-blocked axionCAMB exact-zero implementation path.

A machine lexical hit is only `SOURCE_REVIEW_CANDIDATE`; it is never K0/K1 evidence.

## Frozen discovery lanes
Run all lanes independently with `fail-fast:false` and aggregate only after a barrier:
1. `AxiCLASS ultralight axion CLASS perturbations`
2. `"ultralight axion" "perturbations.c"`
3. `"fuzzy dark matter" CLASS Boltzmann code`
4. `"scalar field dark matter" CLASS perturbations`
5. `"Omega_ax" CLASS extension:c`
6. `"axion fraction" "transfer" cosmology extension:py`
7. `"ultralight scalar" CAMB perturbations -axionCAMB`
8. `"fuzzy" "Boltzmann" "dark matter" code`

Only implementation-bearing paths (`.py,.c,.cc,.cpp,.h,.hpp,.f,.f90,.jl`) are retained for manual source review. Obvious prose/data/corpus paths are rejected mechanically.

## Frozen classification
- infrastructure failure in any lane: `F19_INDEPENDENT_PROVIDER_DISCOVERY_INFRASTRUCTURE_PARTIAL`;
- >=1 implementation-bearing candidate: `F19_INDEPENDENT_PROVIDER_SOURCE_REVIEW_CANDIDATES_FOUND`;
- otherwise: `F19_INDEPENDENT_PROVIDER_DISCOVERY_NO_CANDIDATE`.

No discovery outcome promotes K0/K1, changes the existing axionCAMB blocker, or constitutes physical falsification.

## Next gate
For each machine candidate, pin exact candidate commit and inspect equations/source/reference map. Only a source-complete independent candidate may receive a separately preregistered provider-control and K1 zero-abundance test.