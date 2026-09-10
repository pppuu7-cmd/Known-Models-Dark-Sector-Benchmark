# F16 running-vacuum provenance candidate audit

Date: 2026-09-10
Status: CANDIDATE_BLOCKED_PROVENANCE_PUBLIC_SOLVER
Family: F16 running/decaying vacuum Lambda(H)

## Candidate
Chao-Qiang Geng, Chung-Chi Lee, Lu Yin, *Constraints on a special running vacuum model*, Eur. Phys. J. C 80, 69 (2020), DOI 10.1140/epjc/s10052-020-7653-z; arXiv:2001.05092.

Published model law:

Lambda(H) = 3 alpha H^2 + 3 beta H0^4 H^-2 + Lambda0.

The LambdaCDM reference is explicitly alpha=beta=0. The paper states that the authors modified CAMB because matter/radiation background densities are not analytic for this model, and it derives linear matter/radiation perturbation equations. This is response-distinct from the already represented IDE subcase Q=beta H rho_v because the vacuum density is an explicit nonlinear function of H, including H^2 and H^-2 terms.

## Provenance search performed
Repository/current-frontier and recent Actions were inspected first. No queued/running duplicate F16 production run was present; latest validated KMDSB sync remains run 34480218871.

External/public-source searches were then made for an exact public CAMB/CosmoMC implementation associated with this paper/model. The publication page confirms use of modified CAMB/CosmoMC, but its data-availability statement points to observational datasets rather than an immutable source-code repository. Current GitHub searches did not identify an author-bound public solver snapshot that can be pinned to an exact commit/release.

## Gate decision
K0 is **not promoted to PASS**. Classification for this candidate route is:

`CANDIDATE_BLOCKED_PROVENANCE_PUBLIC_SOLVER`

This is not BLOCKED_IMPLEMENTATION and not a scientific failure of running-vacuum cosmology. No equations are to be reimplemented from the paper and presented as an author/provider result. No K1 numerical gate may be launched until an exact public solver source is pinned or an explicitly preregistered independent-verification implementation is authorized under the protocol.

## Prospective K0/K1 requirements once a provider is found
1. Pin exact repository + commit/release and author/source relation.
2. Freeze exact Lambda(H) law and conservation split used by the code.
3. Freeze perturbation prescription, including treatment/neglect of delta rho_Lambda and momentum transfer.
4. Freeze alpha=beta=0 LambdaCDM reference path.
5. Run provider/infrastructure control first.
6. Only after provider control, preregister K1 numerical regression thresholds before viewing the reference result.
7. Before K2-K6, attack algebraic/response identity against M02 and other interacting-vacuum manifolds; H-dependent vacuum law must not be reduced to a name-level distinction.

## Scientific caution
The paper's perturbation treatment includes assumptions about vacuum perturbations; those assumptions must be source-bound and scored under K3 separately from background execution. A successful CAMB run would therefore establish infrastructure, not conservation/gauge closure by itself.

## Next allowed F16 action
Continue searching for an immutable author-linked or independently documented public implementation of a genuine Lambda(H), H^2, dot-H, inverse-H, or derivative running-vacuum law. If no such provider can be established, retain F16 open and proceed to the next nonduplicative W03 family while preserving this provenance blocker.