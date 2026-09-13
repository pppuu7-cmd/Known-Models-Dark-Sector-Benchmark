# M13b public perturbation-provider reconnaissance delta — 2026-09-13

Target: F13/M13b true two-field quintom perturbation closure  
Status: `NO_NEW_PUBLIC_SOURCE_COMPLETE_PROVIDER_IN_RECON_TRANCHE`  
Physical falsification: **NO**

## Purpose

Refresh the 2026-09-10 provider search before taking the already-authorized independent-verification route. This is a provenance/coverage audit only; absence of a public code hit is not evidence against quintom physics.

## Goh–Taylor 2026 source status

The scientifically strongest target remains L. W. K. Goh and A. N. Taylor, arXiv:2606.27049 / MNRAS 551 (2026) stag1403, `Quintom model perturbations and constraints with observational data`.

The published paper specifies a minimally coupled canonical field `phi` plus phantom field `psi`, derives their linear perturbation equations in conformal Newtonian gauge, and states that the two-field system was implemented in a modified Boltzmann code. This is a family match for M13b and a physically strong K3 candidate.

A renewed 2026-09-13 public-source check found no newly released immutable quintom implementation under the identifiable `LisaGoh` GitHub account. The visible repositories remain `CDE`, `cosmosis-standard-library`, `ecole-euclid-2023`, and `unions-shear-ustc-cea`; no quintom/CLASS repository or tagged source archive was located in this tranche. Therefore the original-provider K0 status remains `BLOCKED_SOURCE_PROVENANCE` and execution as the authors' provider remains unauthorized.

## Additional public quintom code hits

Two additional public source hits were inspected:

1. `ja-vazquez/Scalar_Fields@a4ddce6049f601e090040889b4bb7af371c22921/Quintom.py`.
   - Explicit canonical/phantom background energy densities and opposite-sign background equations are present.
   - The implementation integrates background scalar variables and Hubble evolution with `odeint`.
   - No metric/Boltzmann perturbation system, `delta phi`/`delta psi` perturbation evolution, or source-complete K3 closure was found in the inspected code/repository search.
   - Classification for strict M13b K3: `BACKGROUND_ONLY_NOT_K3_PROVIDER`.

2. `igomezv/cosmo_tools@6f82a0dd6966ee2ab5abde2eb5c35dd0720b6ea1/models/quintom/Quintom.py`.
   - Again contains a two-field background system with canonical and phantom kinetic signs and explicit initial-condition TODOs.
   - The code evolves background fields/Hubble quantities and plotting/derived background observables.
   - No Boltzmann/Einstein perturbation closure was found in the inspected file/repository search.
   - Classification for strict M13b K3: `BACKGROUND_ONLY_NOT_K3_PROVIDER`.

These hits do not improve on the already-pinned SimpleMC background evidence and cannot close K3/K4/K5.

## Decision

No new public source-complete perturbation provider was located in this prospective reconnaissance tranche. The previously authorized fallback is therefore activated:

`published covariant equations -> independently labelled KMDSB verification implementation -> equation-closure gate -> later metric/Boltzmann embedding`

The independent implementation MUST NOT be labelled as the Goh–Taylor source code. It may use the published equations as scientific authority while retaining independent implementation provenance.

## Immediate next gate

Preregister and execute an equation-level K3A closure verifier before any Boltzmann implementation. The verifier must:

- preserve canonical/phantom sign differences in background and perturbation equations;
- verify stress-energy/continuity identities;
- verify the hyperbolic-tangent potential derivatives used by both fields;
- demonstrate that direct field-variable evolution is algebraically regular at the effective `w=-1` crossing;
- explicitly flag the effective-fluid `theta_DE` denominator as singular/ill-conditioned at `sum_i(rho_i+p_i)=0`, so it cannot be used as the fundamental crossing variable;
- make no K4/K5 or observational claim.

Only after K3A passes may a separately preregistered independent Einstein–Boltzmann embedding be attempted.
