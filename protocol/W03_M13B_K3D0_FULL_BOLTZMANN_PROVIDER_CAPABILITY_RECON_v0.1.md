# W03 M13b K3D0 full Boltzmann provider capability reconnaissance v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Scope: public source/provider reconnaissance for a full Einstein-Boltzmann continuation after K3C2  
Physical falsification: **NOT APPLICABLE / FORBIDDEN**

## Trigger

K3C2 independently establishes a two-mode cosmology-scale Newtonian-gauge perturbation bridge on the exact K3C1 background, but it deliberately omits the full photon/neutrino Boltzmann hierarchy, recombination and anisotropic stress. K3 therefore remains PARTIAL.

The next gate is provider capability, not physics fitting. Search criteria are frozen before candidate inspection to avoid post-hoc solver selection.

## Frozen required capability classes

A provider can be graded `DIRECT_PROVIDER_GRADE` only if public immutable source demonstrates all of:

1. a standard Einstein-Boltzmann cosmology stack with photons, baryons, CDM, neutrinos/radiation hierarchy and recombination or equivalent source-complete transfer computation;
2. two simultaneously dynamical scalar degrees of freedom or a clearly extensible multi-field architecture in the same realization;
3. ability to represent one positive-kinetic canonical field and one negative-kinetic/phantom field without replacing the pair by a single effective PPF/fluid crossing variable;
4. direct field perturbation evolution through `rho_DE+p_DE=0`, with no fundamental division by the total dark-energy `rho+p` or `theta_DE`;
5. accessible source for background, perturbation and Einstein coupling sufficient to audit signs and normalization;
6. reproducible public repository and pin/commit suitable for KMDSB provenance;
7. output access sufficient to regress background and at least metric/matter transfer quantities against K3C1/K3C2 controls.

A candidate is `ADAPTER_GRADE` if it supplies items 1, 5, 6 and 7 and exposes a source architecture in which two independent scalar background/perturbation species can be added without replacing the solver's Einstein/Boltzmann hierarchy. Adapter grade does not close K3 and does not authorize a claim that the unmodified provider implements quintom.

A candidate is `RELATED_NOT_GRADE` if it is single-field only, background-only, PPF/effective-fluid crossing only, lacks perturbations, lacks source/provenance, or otherwise misses the required architecture.

## Frozen search tranche

Public GitHub repository/name/code searches:

- `quintom CLASS perturbations`
- `quintom Boltzmann code`
- `two scalar field CLASS cosmology`
- `two field dark energy CLASS`
- `multi scalar CLASS perturbations`
- `phantom scalar CLASS perturbations`
- `canonical phantom CLASS`
- `multi field Boltzmann cosmology`

Named architecture checks regardless of keyword hits:

- official `lesgourg/class_public` / current CLASS source;
- `hiclass-code/hi_class_public`;
- `mcataneo/mochi_class_public`;
- public LisaGoh repositories and the already-audited Goh–Taylor provenance trail;
- already-pinned background quintom sources (`ja-vazquez/SimpleMC`, `ja-vazquez/Scalar_Fields`, `igomezv/cosmo_tools`).

Public literature/web search may be used only to discover named implementations or source links. A paper saying "modified CLASS" without an immutable public source is not provider grade.

## Frozen decision hierarchy

1. If any `DIRECT_PROVIDER_GRADE` candidate exists, pin its exact public commit and preregister a provider-control/K3D1 execution audit before modifying it.
2. Else if one or more `ADAPTER_GRADE` bases exist, rank them only by minimal required source intrusion and closeness to K3C1/K3C2 equations; then preregister one independent adapter construction. No code modification is authorized inside K3D0 itself.
3. If only `RELATED_NOT_GRADE` candidates exist, classify `M13B_K3D0_NO_DIRECT_FULL_BOLTZMANN_PROVIDER_ADAPTER_BASE_REQUIRED` and name the strongest adapter base(s).
4. If no usable Einstein-Boltzmann base exists, classify `M13B_K3D0_FULL_BOLTZMANN_PROVIDER_SEARCH_BLOCKED`.

No search outcome changes K3 above PARTIAL, promotes K4/K5, reproduces the author model, or constitutes physical falsification.

## Candidate audit record

For each inspected candidate record:

- repository and exact inspected ref/commit when available;
- whether it has full Boltzmann/recombination machinery;
- scalar-field multiplicity/architecture;
- phantom-sign capability;
- crossing variable discipline;
- source accessibility;
- classification: DIRECT_PROVIDER_GRADE / ADAPTER_GRADE / RELATED_NOT_GRADE;
- exact reason.

The final reconnaissance result must also preserve the K3C0 author-unit/source blocker independently of any adapter choice.
