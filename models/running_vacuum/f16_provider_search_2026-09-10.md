# F16/M16 running/interacting-vacuum provider search

Updated: 2026-09-10
Status: `PUBLIC_SOURCE_PROVENANCE_OPEN`
Execution authorized: **NO**
Physical family falsification: **NO**

## Target family

F16 is the running/decaying vacuum / interacting-vacuum class in which the vacuum sector has `w_vac=-1` but evolves through explicit exchange with material species and/or a running law such as `rho_vac(H,dot H)`.

A useful strict representative must expose both the background exchange and the perturbation prescription. Background-equivalent dynamical-DE mappings are not enough for K3-K5.

## Candidate A — modern RVM / RRVM, Solà Peracaula et al. 2023

Reference: arXiv:2304.11157, `Running Vacuum in the Universe: Phenomenological Status in Light of the Latest Observations, and Its Impact on the sigma8 and H0 Tensions`.

The paper studies low-energy running-vacuum models with vacuum density of the schematic form

`rho_vac(H) = 3/(8 pi G) [c0 + nu H^2 + tilde_nu dot H] + ...`

and uses CLASS plus MontePython in the observational analysis. The rigid-vacuum comparison is explicitly the zero-running limit (e.g. `nu_eff=0` for the quoted RVM parameterization), making this attractive for K1.

Scientific strengths:

- contemporary data analysis;
- Einstein–Boltzmann treatment rather than background-only distances;
- explicit LambdaCDM/rigid-vacuum limit;
- running-vacuum family identity is direct rather than inferred from a generic IDE map.

Current blocker:

- searches by exact title, arXiv ID, authors, CLASS/MontePython terms and parameter names did not locate an immutable public modified-CLASS source tree corresponding to this analysis;
- the paper identifies use of CLASS/MontePython but does not by itself provide an exact public code commit sufficient for KMDSB provider execution.

Classification: `F16_RVM_2023_STRONG_PHYSICS_CANDIDATE_K0_SOURCE_OPEN`.

## Candidate B — Perico & Tamayo running-vacuum perturbations

Reference: arXiv:1607.07825 / JCAP 08 (2017) 026, `Running Vacuum Cosmological Models: Linear Scalar Perturbations`.

This work explicitly derives linear scalar perturbations for two running scenarios, `Lambda(H^2)` and `Lambda(R)`, and reports numerical integration with a modified CLASS implementation. The vacuum is decomposed into contributions interacting with material species, with distinct coupling structure for the two scenarios. The publication presents CMB and matter-power consequences and a Planck analysis.

Scientific strengths:

- explicit perturbation-level family specification;
- two response-distinct running-vacuum prescriptions;
- modified CLASS was actually used;
- free-parameter-zero limit returns the standard adiabatic/LambdaCDM behavior according to the model construction.

Current blocker:

- no exact public modified-CLASS repository/tag/commit was found in the present search;
- publication equations are sufficient for a future independent verification implementation, but not enough to label such a reconstruction the authors' provider.

Classification: `F16_PERICO_TAMAYO_PHYSICS_DEFINED_PROVIDER_SOURCE_OPEN`.

## Additional interacting-vacuum literature

The search also identified modern geodesic/inhomogeneous interacting-vacuum and Shan–Chen-type vacuum models with explicit linear perturbation prescriptions. These are scientifically relevant candidate subfamilies, especially for testing whether a simple RVM span is sufficient, but no exact public source-complete Boltzmann implementation has yet been pinned in KMDSB.

## Public-code search outcome

Searches performed on 2026-09-10 included combinations of:

- `running vacuum`, `RVM`, `RRVM`, `Lambda(H^2)`, `Lambda(R)`;
- `CLASS`, `MontePython`, `CAMB`;
- author names and arXiv identifiers;
- characteristic parameter names such as `nu_eff`.

No repository was found that can yet be bound unambiguously to one of the published perturbation-capable F16 implementations with an immutable scientific source commit.

This is a provenance result, not evidence that no public implementation exists anywhere.

## Current F16 gate

- family identity: `DEFINED`;
- published perturbation equations: `AVAILABLE_FOR_MULTIPLE_SUBFAMILIES`;
- exact public provider provenance: `OPEN`;
- K0 execution: `NOT_AUTHORIZED`;
- K1-K9: `NOT_TESTED`.

Do not promote a background-only H(a) script or generic IDE emulator to F16 K3/K5 evidence.

## Next allowed route

1. continue source search through author/group repositories, supplementary archives and Zenodo records for the 2023 RRVM/RVM and 2017 Lambda(H^2)/Lambda(R) implementations;
2. if an exact public source appears, pin source + branch/commit and freeze its zero-running reference before provider execution;
3. if no provider becomes available, an independent KMDSB implementation from published perturbation equations may be considered only under separate preregistration with explicit conservation/gauge/initial-condition tests;
4. retain distinct `Lambda(H^2)` and `Lambda(R)` prescriptions if their response operators are demonstrably non-equivalent rather than collapsing them by label alone.
