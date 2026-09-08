# KMDSB current state / recovery handoff

Updated: 2026-09-08

## Mission
Pass known dark-sector and modified-gravity models through a frozen DSIR benchmark funnel, record why each gate passes/fails/blocks, and accumulate evidence-derived design requirements for a future original dark-sector model.

## Scientific authority
Main DSIR snapshot currently used by existing audits:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

Do not silently replace this snapshot inside an existing audit. If authority advances, record a new audit revision or authority-delta note.

## Recovery entry points

Full recovery manual:
`recovery/RESTORE_FROM_NEW_CHAT.md`

Future-model methodology:
`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`

Frozen per-model funnel:
`protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`

## Gate sequence
- B0 identity/provenance
- B1 DSIR embedding/reference limit
- B2 conservation/gauge/frame bookkeeping
- B3 physical-domain/numerical control
- B4 response coverage/masks
- B5 LambdaCDM/reference identifiability
- B6 nearest-comparator discrimination
- B7 quotient-surviving residual novelty
- B8 prospective withheld prediction
- B9 synthesis/design-prior extraction

## Wave state

### W00 Calibration and semantics — COMPLETE

M00 LambdaCDM: `CONTROL_PASS_WITH_SCOPE`.

M01 smooth non-phantom DE / local wCDM ray: `DSIR_COMPATIBLE_NONIDENTIFIABLE` in the scoped corrected DESI DR1 ShapeFit control.

Key M01/B5 calibration:
- `sigma(epsilon_w) ~= 0.1782`;
- frozen `epsilon_w = 1e-4`;
- local significance about `5.61e-4 sigma`.

Interpretation: physical/DSIR compatibility does not imply observational identifiability.

### W01 Baseline dark-sector control atlas — COMPLETE

M02 IDE, M03 GDM, M04 thermal WDM, M05 designer f(R), M06 DCDM were passed through the frozen B0-B9 protocol within their pinned scopes.

Durable methodology extracted:
- physical tangent-cone geometry precedes differentiation;
- multi-channel response is required to attack degeneracy;
- parameter count is not identified rank;
- high-k windows/masks/characteristic-scale motion are first-class controls;
- modified-gravity comparators are mandatory for dark-sector claims;
- prospective/temporal holdout semantics must remain distinct from retrospective fitting.

### W02 Same-observable degeneracy attack — ACTIVE

Frozen edges:
- E1 IDE vs GDM — `PASS_WITH_SCOPE` theory-space;
- E2 IDE vs designer f(R) — `PASS_WITH_SCOPE` theory-space;
- E3 WDM vs alternative small-scale suppression — no pinned second comparator found; terminal status should be `BLOCKED_IMPLEMENTATION` unless a valid same-grid comparator is identified;
- E4 DCDM vs alternative temporal-history mechanism — current active provenance/implementation check.

E1 exact source: `waves/wave_02_degeneracy_attack/E1_result.json`.
Closest pair: IDE alpha_negative vs GDM cv2, acute angle `24.786398 deg`.
Exact directional equivalence is rejected only in the frozen unwhitened low-k response block; observation-space promotion remains open.

E2 exact source: `waves/wave_02_degeneracy_attack/E2_result.json`.
Acute angles against minimum-resolved designer-f(R) ray: `42.450273 deg` and `59.404101 deg`.
Exact directional equivalence is rejected only in the frozen theory-response scope; observation-space promotion remains open.

## Future-model methodology state

The living construction protocol is now:
`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`

It defines stages F0-F9:
- authority/provenance freeze;
- recoverable reference limit;
- admissible parameter geometry;
- conservation/gauge/frame closure;
- multi-channel response architecture;
- covariance-aware identifiability;
- nearest-comparator attack;
- quotient-surviving novelty;
- prospective holdout;
- candidate synthesis/promotion.

Current design-prior ledger:
`matrices/design_prior_ledger.csv`

It contains DP-0001..DP-0604 (30 ACTIVE requirements). They are not yet all axioms. Conceptual promotion is ACTIVE -> REINFORCED -> CORE -> RETIRED after repeated/adversarial evidence.

## Highest-priority task

Finish W02 cleanly:
1. complete E4 same-coordinate comparator provenance check;
2. write terminal E3/E4 result records, using `BLOCKED_IMPLEMENTATION` if required rather than synthetic comparators;
3. split theory-space and observation-space comparator graphs;
4. close W02 only when all frozen edges have terminal statuses;
5. update matrices, methodology, recovery documents and research log;
6. then open W03 expanded dark-energy family.

## Non-negotiable rules

1. Never zero-impute missing channels.
2. Never equate theory-space separation with observational discrimination.
3. Never equate non-identifiability with theory falsification.
4. Never promote a retrospective relation to prospective B8 support.
5. Physical parameter geometry is frozen before differentiation/Jacobian construction.
6. Never fabricate a comparator to force a PASS/FAIL; use `BLOCKED_*` when evidence/implementation is absent.
7. Every completed audit/wave adds explicit design-prior deltas and updates recovery state.
8. If chat memory conflicts with repository state, repository evidence wins.
