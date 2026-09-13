# M13b normalization-authority reconnaissance — 2026-09-13

Target: F13/M13b cosmology-scale normalization/provenance bridge  
Status: `NO_PUBLIC_AUTHORITATIVE_QUINTOM_NORMALIZATION_MAP_FOUND`  
Physical falsification: **NO**

## Trigger

K3C0 established that the public 2025 tanh benchmark cannot be inserted literally into a physical reduced-Planck cosmology together with its quoted H0/Omega values. The resulting >110-decade scale mismatch requires an explicit normalization/rescaling map before any author-model numerical reproduction can proceed.

## Public author repository refresh

A 2026-09-13 refresh of the public `LisaGoh` GitHub account returns four visible repositories:

- `LisaGoh/CDE`;
- `LisaGoh/cosmosis-standard-library`;
- `LisaGoh/ecole-euclid-2023`;
- `LisaGoh/unions-shear-ustc-cea`.

No public repository named or indexed as a quintom/modified-CLASS implementation was found. Targeted code searches for the public tanh benchmark/value combination and quintom identifiers also returned no source hit in the visible author repositories.

## Adjacent CLASS/mochi_class evidence

Public `cloe-org/cloelib` issue #292 (`Implement mochi_class`) is relevant only as adjacent provenance evidence:

- LisaGoh is an assignee;
- she explicitly reports creating branch `292-mochi-class` and `mochi_class_background.py` for a CLASS-family background/perturbation integration;
- a later project comment states that a file containing functions for a **specific parameterisation** was removed from the public repository and moved to a private repository.

This establishes that LisaGoh has public CLASS-family implementation activity and that some project-specific parameterisation code in adjacent work is private. It does **not** establish that the private code is the quintom implementation, does **not** provide a quintom normalization map, and must not be used to infer one.

## Publication availability evidence

The 2025 MNRAS article's data-availability statement says the underlying data will be shared on reasonable request to the corresponding author. This is not an immutable public source release and does not bind code units.

The 2026 perturbation article publicly states that a modified Boltzmann solver/CLASS-like implementation was used for the quintom inference, but the public article and currently visible author repositories do not expose an immutable source/commit that maps the printed `V0`, field and time/Hubble labels into solver variables.

## Related background implementation caution

The pinned SimpleMC two-field background provider already used elsewhere in M13b is an example of why labels cannot be transferred across implementations: its scalar density is explicitly normalized by Hubble-scale quantities (`V/(3 h^2)` in its internal background variable convention). It uses a different potential and is not authority for Goh–Taylor normalization.

Therefore SimpleMC may illustrate implementation-dependent normalization, but it cannot repair or define the Goh–Taylor unit map.

## Canonical conclusion

`NO_PUBLIC_AUTHORITATIVE_QUINTOM_NORMALIZATION_MAP_FOUND`.

Consequences:

1. Original-model cosmology-scale reproduction remains `BLOCKED_SOURCE_PROVENANCE / BLOCKED_UNIT_BINDING`.
2. No numerical factor derived from K3C0 may be silently applied to the published `V0` label.
3. No adjacent CDE, mochi_class, SimpleMC or generic CLASS convention may be reassigned as the missing quintom normalization without explicit source authority.
4. The independent K3A/K3B0/K3B1/K3B2 evidence remains valid in its stated scope.
5. The allowed continuation is a separately preregistered independent dimensionless cosmology-scale benchmark whose normalization is defined internally by explicit FRW closure, with no claim of reproducing Goh–Taylor Table/Figure parameter values.
