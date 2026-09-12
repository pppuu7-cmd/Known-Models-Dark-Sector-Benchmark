# W07 M35 pinned-source quotient geometry audit v0.1

Date: 2026-09-12
Model: M35 Einstein-Aether / Lorentz-violating gravity+DM scoped CLASS_LVDM representation
Provider: `Michalychforever/CLASS_LVDM@d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`
Purpose: source-level audit of nominal inputs versus derived combinations and possible quotient/equivalence structure. This is analysis-only and cannot upgrade canonical K2 beyond PARTIAL.

## Frozen source scope

Inspect only the exact pinned tree, especially:
- `include/perturbations.h`;
- `source/input.c`;
- `source/perturbations.c`;
- `Misha.ini`;
- `lcdm.ini`;
- README/documentation files present at the pinned commit.

## Frozen checks

1. Verify whether `alpha`, `beta`, `lambda`, `Y_dm` are represented as four separate stored/input coordinates.
2. Verify that the visible `alpha = 2 beta` source line, if present, is commented rather than an enforced assignment in the pinned production source.
3. Inventory explicit derived combinations involving the gravity coordinates, including the cosmological-G combination, `(beta+lambda)/alpha`, `(beta+3 lambda)/alpha`, and the alpha-dependent H scale when present.
4. Verify that `Y_dm` enters production perturbation logic nontrivially rather than being merely parsed/stored.
5. Record author-shipped configurations demonstrating the tested gravity ray and the numerical control/reference configuration.

## Interpretation

Four nominal source coordinates do not by themselves establish four physically independent directions. Derived combinations can induce degeneracies or quotient structure, and scalar CLASS_LVDM does not close the full covariant scalar/vector/tensor Einstein-Aether geometry.

If the four coordinates and nontrivial derived-combination structure are verified while no complete quotient/equivalence map is present in the frozen source scope, classify `M35_SOURCE_FOUR_INPUTS_DERIVED_COMBINATIONS_QUOTIENT_NOT_CLOSED`.

Always set `K2_promoted=false`, `canonical_K2_remains=PARTIAL`, `physical_falsification=false`, and `full_Einstein_Aether_SVT_claim=false`.