# M13b Goh–Taylor 2026 perturbation-capable CLASS provider audit

Updated: 2026-09-10
Target: F13/M13b true two-field quintom
Status: `PHYSICALLY_STRONG_PROVIDER_CANDIDATE_K0_SOURCE_PROVENANCE_BLOCKED`
Execution authorized: **NO**
Physical falsification: **NO**

## Candidate

L. W. K. Goh and A. N. Taylor,

- arXiv:2606.27049, `Quintom Model Perturbations`;
- peer-reviewed version: MNRAS 551 (2026), article `stag1403`, published 24 July 2026, corrected/typeset 7 August 2026;
- title in final version: `Quintom model perturbations and constraints with observational data`.

This is substantially stronger than the background-only SimpleMC M13b representative because the paper explicitly derives the linear perturbations of the canonical and phantom scalar fields and states that the two-field system was implemented in the Einstein–Boltzmann code CLASS.

## Family identity

The paper uses a minimally coupled dark-energy sector with

- canonical quintessence field `phi`;
- phantom field `psi` with negative kinetic contribution;
- common hyperbolic-tangent potential

`V(phi) = V0 [tanh(s(1-phi)) + 1]`,

with the same functional form for the second field.

The relative field velocities generate a genuine phantom-to-quintessence crossing. This is a true multi-DOF quintom mechanism rather than a PPF/CPL effective-fluid crossing.

Family identity: `MATCH_M13B`.

## Perturbation scope

The final paper gives the scalar-field density/pressure perturbations and perturbed Klein–Gordon equations in conformal Newtonian gauge and states that CLASS was modified to include both scalar fields. It presents matter perturbations, matter power spectrum and CMB consequences. Therefore, if the exact source is obtained, this implementation is potentially capable of closing the K3 gap left by SimpleMC.

The paper reports, among other effects, roughly percent-level suppression of the linear matter power spectrum and a large-scale CMB temperature/late-ISW response for its fitted quintom cosmologies. These published outputs are only qualitative/benchmark targets until source reproduction is possible.

## Public-source search

Searches performed on 2026-09-10 covered:

- exact paper title plus GitHub / code / CLASS terms;
- arXiv identifier `2606.27049` plus code terms;
- author name / ORCID / GitHub identity;
- the public GitHub account `LisaGoh` and its visible repositories;
- code searches in the public `LisaGoh/CDE` and `LisaGoh/cosmosis-standard-library` trees for quintom-specific material.

The author's public GitHub account is identifiable, but no public repository containing the 2026 quintom-modified CLASS implementation was located.

The MNRAS Data Availability statement says that the underlying data will be shared on reasonable request to the corresponding author; it does not provide a public source archive or immutable source identifier for the modified CLASS.

## K0 decision

KMDSB requires an exact source/version/commit or equivalent immutable source archive before executing an external scientific provider. The publication alone is not enough to reconstruct hidden implementation choices and label the reconstruction as the authors' provider.

Therefore:

- family/mechanism identity: `PASS_CANDIDATE`;
- published perturbation specification: `STRONG_CANDIDATE`;
- public executable source provenance: `BLOCKED_NOT_PUBLICLY_PINNED`;
- K0 scientific promotion: `BLOCKED_SOURCE_PROVENANCE`;
- K1-K9 execution from this provider: **NOT AUTHORIZED**.

Classification:

`M13B_GOH_TAYLOR_2026_CLASS_K0_SOURCE_PROVENANCE_BLOCKED`

This is not a criticism of the paper and not a physical model failure. It is a reproducibility/provenance gate specific to KMDSB.

## Relation to SimpleMC evidence

The current M13b evidence is complementary:

1. pinned SimpleMC: public executable two-field background true-crossing representative; exact K1 reduction to canonical one-field branch passes; no validated Boltzmann perturbation closure and author IC warning;
2. Goh–Taylor 2026: published source-complete *physics description* including linear perturbations and a modified CLASS implementation, but the implementation source itself is not publicly pinned.

Together these make M13b scientifically much less ambiguous than before, but they still do not close strict K3/K4/K5.

## Next allowed route

Priority order:

1. continue searching for a newly released public source archive, repository, tagged release, supplementary file or Zenodo record corresponding to arXiv:2606.27049 / MNRAS stag1403;
2. if an exact source becomes available, pin it immediately and preregister provider control, K1 reference, K3 equation-to-source mapping and only then K4/K5 response tests;
3. if the code remains nonpublic, an independent KMDSB reproduction from the published covariant equations is allowed only under a separate preregistration and must be labelled `independent verification implementation`, never the Goh–Taylor original provider;
4. do not erase the SimpleMC background evidence while waiting for perturbation-capable provenance.
