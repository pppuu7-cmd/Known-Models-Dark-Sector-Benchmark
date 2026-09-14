# W04 M21 perturbation-state duplicate-coordinate recovery v0.1

Frozen after run `34895647832` completed all six heavy perturbation-state lanes successfully but the aggregate returned `M21_PERTURBATION_STATE_BRANCH_SIGNATURE_BLOCKED` solely because native CLASS perturbation tables contain exact duplicate scale-factor coordinates. This recovery is analysis-only: no CLASS rerun, no physics/input/profile/k/window/J-threshold changes.

Parent authority: run `34895647832`; provider `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`; parent protocol `W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md`; frozen J floor `1e-12`, localization `J>=3`, branch/control edges, variables, k anchors and `500<=z<=2500` window remain unchanged.

## Causal defect

The parent parser intentionally rejected any duplicate `a` coordinate. Native provider tables contain exact repeated `a` rows at sparse event boundaries, so interpolation cannot be defined without an explicit side convention. This is a representation/parser boundary, not a physical failure.

## Recovery rule

For every table, retain provider file order and require all coordinates finite and positive. For an exact duplicated `a` value construct two deterministic views:

- `FIRST`: keep the first provider row at that exact `a`;
- `LAST`: keep the last provider row at that exact `a`.

No averaging, jittering, nearest-neighbour synthesis, tolerance-based merging, row deletion outside exact duplicates, or post-result selection is allowed.

Run the complete frozen parent classifier independently on FIRST and LAST views. Recovery is scientifically usable only if:

1. both views finish without BLOCKED;
2. both have identical final classification;
3. every frozen branch-change and same-branch-control edge has identical `edge_localized` Boolean in both views;
4. both preserve the parent cross-lane input identity checks.

If any condition fails, classification is `M21_PERTURBATION_STATE_DUPLICATE_RECOVERY_AMBIGUOUS_BLOCKED` and no downstream source audit is authorized.

If all conditions pass, emit `M21_PERTURBATION_STATE_DUPLICATE_RECOVERY_ROBUST` plus the common inherited parent classification and both full result payloads. The inherited classification has exactly the same consequence rule and interpretation ceiling as the parent protocol. This recovery cannot promote K1/K3/K4 or establish physical M21 failure.

## Compute rule

Reuse immutable lane artifacts from run `34895647832`; do not repeat the six heavy CLASS lanes. Analysis-only recovery is the only authorized next operation for this blocker.
