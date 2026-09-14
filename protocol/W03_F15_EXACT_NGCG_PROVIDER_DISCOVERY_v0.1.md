# W03 F15 exact NGCG provider discovery v0.1

Date: 2026-09-14
Family: F15 / M15 generalized Chaplygin / unified dark fluid
Purpose: search for an independent public implementation of the genuinely decomposed/generalized/New generalized Chaplygin gas perturbation system, without reusing IDECAMB background-equivalent transfer closure as though it were the published NGCG perturbation prescription.

## Frozen scientific scope

A candidate may advance to source review only if implementation-bearing source exposes evidence for all of:
1. NGCG/GCG/unified Chaplygin law or its explicit decomposed equivalent;
2. cosmological background evolution;
3. linear perturbation / gauge / Boltzmann evolution;
4. an executable implementation path.

Preferred evidence additionally exposes the published decomposed closure, effective sound speed, momentum-transfer/frame prescription, or an exact LambdaCDM/reference map.

## Frozen exclusions

Reject paper text, notebooks without solver code, pure background fits, generic IDE implementations lacking the NGCG perturbation closure, KMDSB itself, and lexical collisions. A machine `SOURCE_COMPLETE_REVIEW` label is triage only and cannot promote K0/K1. Exact source/commit/equations/reference-map review is mandatory before any scientific run.

## Frozen query tranche

Eight independent lanes:
- `"new generalized chaplygin gas" perturbation extension:py`
- `"new generalized chaplygin gas" CAMB`
- `"new generalized chaplygin gas" CLASS`
- `NGCG perturbation cosmology extension:py`
- `"generalized chaplygin gas" perturbations extension:c`
- `"generalized chaplygin gas" perturbations extension:f90`
- `"chaplygin" "sound speed" Boltzmann`
- `"chaplygin" "momentum transfer" cosmology`

## Classification

- any mechanically qualifying source -> `F15_NGCG_SOURCE_COMPLETE_CANDIDATE_FOUND`, requiring manual exact-source review;
- only partial implementation leads -> `F15_NGCG_PROVENANCE_LEADS_ONLY`;
- no qualifying source with at least one successful lane -> `F15_NGCG_NO_QUALIFYING_PUBLIC_SOURCE_IN_FROZEN_TRANCHE`;
- all lanes blocked -> `F15_NGCG_DISCOVERY_INFRASTRUCTURE_BLOCKED`.

For every outcome: `K0_promoted=false`, `K1_promoted=false`, `physical_falsification=false` until manual source review and a separately preregistered provider-control/reference gate.
