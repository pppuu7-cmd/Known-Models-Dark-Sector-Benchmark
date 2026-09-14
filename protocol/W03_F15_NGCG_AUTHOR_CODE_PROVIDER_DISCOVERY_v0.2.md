# W03 F15 NGCG author-code provider discovery v0.2

Frozen: 2026-09-14
Family: F15 / M15 generalized Chaplygin / unified dark fluid
Status: PREREGISTERED

## Purpose
The broad exact-NGCG code search in Actions run 34826008004 returned no source-complete provider after manual review. This gate performs a narrower, nonduplicating author/equation keyed search before declaring the public-provider route exhausted.

## Scientific scope
Target is an implementation of the response-distinct NGCG/GCG perturbation family, not merely a background likelihood script. A candidate must expose enough source to audit the background law, perturbation closure (single-fluid or decomposed), sound speed/nonadiabatic prescription, momentum-frame prescription where decomposed, and a reference/decoupling map.

The original NGCG paper is Xin Zhang, Feng-Quan Wu, Jingfei Zhang, astro-ph/0411221, with p=-A_tilde(a)/rho^alpha and dual interacting-XCDM interpretation. Later growth-only/background implementations are provenance leads unless they implement a full perturbation/Boltzmann closure.

## Frozen independent search lanes
1. `"Xin Zhang" "Chaplygin" CAMB`
2. `"Feng-Quan Wu" Chaplygin code`
3. `"Jingfei Zhang" NGCG code`
4. `"astro-ph/0411221" code`
5. `"p = -" "rho" "alpha" chaplygin perturbation extension:py`
6. `"chaplygin" "delta" "theta" extension:c`
7. `"chaplygin" "delta" "theta" extension:f90`
8. `"new generalized chaplygin" growth perturbation code`

## Fail-closed candidate rule
Machine search may only label a hit `SOURCE_REVIEW_CANDIDATE`. It is not K0/K1 evidence. Markdown, XML/RSS, bibliographies, paper corpora, educational prose and generic parameter-fitting notebooks without perturbation equations are rejected. A source-complete candidate requires implementation-bearing code plus identifiable cosmological equations and executable integration path.

## Interpretation
No hit or no source-complete candidate => `F15_AUTHOR_CODE_DISCOVERY_NO_SOURCE_COMPLETE_PROVIDER`; this is provenance/implementation blocked, not physical falsification.

A surviving candidate => freeze exact repository SHA and perform source/equation/reference-map audit before any K1 execution.

No thresholds or scientific gates from prior M15 work may be weakened after seeing results.
