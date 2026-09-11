# M28 perturbation-provider gap note v0.1

Date: 2026-09-11

## Purpose

Record the current provider/literature boundary for the superfluid-dark-matter benchmark before any independent perturbation implementation is attempted. This is an exploratory capability note, **not** a preregistered K-gate result.

## Public implementation search

The existing M28 background-provider audit pins `azieg/Superfluid-Dark-Matter-Cosmo` at commit `6d57a275aa120d0516f3e5526a024aa41b7e65d8`; that provider exposes an executable background calculation but no source-complete perturbation solver/reference map.

A fresh public-code search on 2026-09-11 using the exact arXiv identifier `2001.02591`, the exact title `Growth of Linear Perturbations in a Universe with Superfluid Dark Matter`, and combinations of `superfluid dark matter`, `CLASS`, `CAMB`, and the authors did not locate a public source-complete Einstein-Boltzmann implementation of the Banerjee-Bera-Mota superfluid-DM perturbation model. This is a search result, not a proof that no unpublished or unindexed implementation exists.

## Literature capability

Banerjee, Bera & Mota, *Growth of Linear Perturbations in a Universe with Superfluid Dark Matter*, JCAP 07 (2020) 034, arXiv:2001.02591, explicitly studies the linear cosmological growth problem. The paper gives:

- the superfluid effective Lagrangian and baryon-phonon coupling (their Eqs. 2.5--2.7);
- a background evolution equation and dust-like/background consistency bounds (Eqs. 3.1--3.6);
- a matter-dominated weak-field perturbation treatment using a Poisson equation (Eqs. 3.7--3.10);
- the linearized phonon/background equations (Eqs. 3.11--3.14);
- benchmark choices including `m = 1 eV`, `alpha = 1e-6`, `Lambda = 500 eV` for the worked perturbation calculation.

The paper itself frames this section in the weak-field/matter-dominated treatment. This is enough to define a reduced-order independent growth-control calculation, but it is not by itself a complete relativistic Einstein-Boltzmann provider for CMB transfer functions, radiation-era initial conditions, gauge cross-checks, or a source-complete K1/K5 closure.

Primary literature: https://arxiv.org/abs/2001.02591
Original model: https://arxiv.org/abs/1506.07877

## Frozen methodological consequence

Until a source-complete public provider is found or an independent covariant implementation is prospectively specified and validated:

1. do **not** treat the existing background provider as perturbation-complete;
2. do **not** substitute an interacting-DM/dark-energy repository for this model merely because it contains an interaction sector;
3. a next M28 calculation may be a **reduced-order growth reproduction/control** based on the published weak-field equations, but it must be labeled as such and may not promote a full K1/K5 perturbation gate;
4. any future full perturbation implementation requires a separate prospective preregistration covering gauge choice, Einstein constraints, radiation/baryon/photon coupling, initial conditions, numerical convergence, and an independent reference limit.

## Current status

`M28_FULL_PERTURBATION_PROVIDER_GATE = OPEN`

Reason: `NO_PUBLIC_SOURCE_COMPLETE_EINSTEIN_BOLTZMANN_PROVIDER_LOCATED_IN_CURRENT_AUDIT`.

This is a provider/capability boundary, not physical falsification of superfluid dark matter.
