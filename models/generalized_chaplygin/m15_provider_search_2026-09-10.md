# M15 generalized/decomposed Chaplygin provider search

Date: 2026-09-10
Status: `AUTHOR_PUBLIC_CLASS_FORK_FOUND_PAPER_BRANCH_NOT_BOUND`
Scientific promotion: **NO**

## Why a new provider is required

The pinned IDECAMB default coupled-fluid branch has the correct decomposed-NGCG homogeneous interaction law and can match the geodesic dark-matter momentum-transfer frame, but its extended-PPF transfer-perturbation parametrization is not the same explicit gauge-complete `delta Q` closure used in the published geodesic decomposed-NGCG equations. It is therefore retained only as a background/interacting-fluid comparator, not as an exact M15 perturbation provider.

## Literature implementations identified

### A. Wang et al. / Wands et al. decomposed Chaplygin gas (2013)

Reference: arXiv:1301.5315 / Phys. Rev. D 87, 083503.

The paper explicitly treats two perturbation prescriptions for the same decomposed generalized Chaplygin background:

1. barotropic: nonzero adiabatic/rest-frame sound speed;
2. geodesic: dark matter follows geodesics and the effective rest-frame sound speed is zero.

The numerical analysis is implemented in CAMB/synchronous gauge. This is scientifically attractive for M15 because it makes the perturbation prescription explicit and therefore provides a clean target for the new perturbation-closure identity gate.

Current provider status: the publication is identified, but a pinned public source repository/commit reproducing the paper implementation was **not located in the present search**. Do not reconstruct hidden implementation choices from the paper and call that the original provider.

### B. vom Marttens et al. generalized Chaplygin dark-sector model (2017)

Reference: arXiv:1702.00651 / Physics of the Dark Universe 15 (2017) 114-124.

The paper states that it uses a modified CLASS implementation to calculate CMB and matter spectra for a generalized Chaplygin dark sector split into CDM plus constant-w dark energy, with first-order perturbation equations written explicitly in the paper.

This is a second strong implementation target because the perturbation equations and Boltzmann solver family are independent of the IDECAMB candidate.

#### Direct author-GitHub audit

A stronger provenance lead has now been found: paper author Rodrigo von Marttens has a public repository

`rodrigovonmarttens/class_public`.

Current repository facts checked on 2026-09-10:

- repository is public;
- default branch is `master`;
- branch enumeration exposes only `master` at present;
- current HEAD is `aa92943e4ab86b56970953589b4897adf2bd0f99`;
- that HEAD commit is the CLASS v3.2 multi-interacting-DM implementation associated with arXiv:2010.04074, not a Chaplygin commit;
- code search on the current branch for `Chaplygin` and `gcg` returns no model identifier;
- the author's public `montepython_public` fork likewise yields no `gcg` hit in the current indexed branch;
- historical repository commits around 2017 visible on the retained branch track ordinary CLASS development and do not by themselves bind a Chaplygin modification to arXiv:1702.00651.

Therefore the existence of an author-owned CLASS fork is **not yet provenance for the 2017 GCG implementation**. It is an important negative control: KMDSB must not equate “same author + CLASS fork” with “paper source”. Deleted/private/unmerged historical branches are not reconstructed by assumption.

Current provider status: `AUTHOR_REPO_FOUND_BUT_2017_GCG_SOURCE_NOT_BOUND`.

### C. `sum33it/scalpy`

A public `GCG` class exists and is useful as a lightweight analytic/background cross-check. However, its advertised GCG functionality is not a Boltzmann perturbation implementation equivalent to the CAMB/CLASS M15 target. It is therefore unsuitable as the sole K3-K5 provider.

## Current M15 conclusion

- exact perturbation family: scientifically well-defined;
- independent published CAMB implementation: identified, source commit not frozen;
- independent published CLASS implementation: identified;
- author-owned public CLASS repository: now identified and audited, but no current/historical evidence inspected so far binds its accessible branch to the 2017 GCG modification;
- IDECAMB: rejected as exact perturbation provider, retained as scoped background comparator;
- lightweight GCG background code: available but insufficient for multichannel perturbation scoring;
- M15 K1-K9: **not authorized** until source provenance is solved or a separately preregistered independent reproduction is validated.

Classification:

`M15_PROVIDER_PROVENANCE_OPEN_AUTHOR_CLASS_FORK_NOT_PAPER_BOUND`

## Next search order

1. inspect author/project forks, tags, archived mirrors and supplementary/data links specifically for the 2017 modified CLASS tree rather than generic CLASS forks;
2. search author/project repositories and supplementary material for the 2013 decomposed-CAMB implementation;
3. if neither public implementation can be frozen, implement the published perturbation equations as a **new KMDSB verification implementation**, clearly labelled as independent reproduction rather than original-provider evidence;
4. cross-check the reproduction at alpha=0 against LambdaCDM and against analytic background identities before any DSIR K4/K5 ranking claim.

A new in-repo implementation is allowed only after its equations, gauge, initial conditions, reference limit, and validation suite are separately preregistered. It must not be presented as the authors' original code.
