# M15 generalized/decomposed Chaplygin provider search

Date: 2026-09-10
Status: `EXACT_PUBLIC_PROVIDER_NOT_YET_FROZEN`
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

Current provider status: the authors' group page advertises public GitHub code in general and displays the paper/results, but the exact modified CLASS repository/commit corresponding to arXiv:1702.00651 was **not located in the present search**. Therefore no execution is authorized yet.

### C. `sum33it/scalpy`

A public `GCG` class exists and is useful as a lightweight analytic/background cross-check. However, its advertised GCG functionality is not a Boltzmann perturbation implementation equivalent to the CAMB/CLASS M15 target. It is therefore unsuitable as the sole K3-K5 provider.

## Current M15 conclusion

- exact perturbation family: scientifically well-defined;
- independent published CAMB implementation: identified, source commit not frozen;
- independent published CLASS implementation: identified, source commit not frozen;
- IDECAMB: rejected as exact perturbation provider, retained as scoped background comparator;
- lightweight GCG background code: available but insufficient for multichannel perturbation scoring;
- M15 K1-K9: **not authorized** until source provenance is solved.

Classification:

`M15_PROVIDER_PROVENANCE_OPEN_AFTER_PERTURBATION_IDENTITY_GATE`

## Next search order

1. locate an archived/forked source tree or author repository for the 2017 modified CLASS implementation;
2. search author/project repositories and supplementary material for the 2013 decomposed-CAMB implementation;
3. if neither public implementation can be frozen, implement the published perturbation equations as a **new KMDSB verification implementation**, clearly labelled as independent reproduction rather than original-provider evidence;
4. cross-check the reproduction at alpha=0 against LambdaCDM and against analytic background identities before any DSIR K4/K5 ranking claim.

A new in-repo implementation is allowed only after its equations, gauge, initial conditions, reference limit, and validation suite are separately preregistered. It must not be presented as the authors' original code.
