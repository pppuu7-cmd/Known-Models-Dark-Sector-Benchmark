# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-08
Purpose: allow the KMDSB/DSIR benchmark development to be resumed from another chat without relying on memory of the previous conversation.

## 0. Rule of authority

If chat memory conflicts with repository state, the repository wins.

Scientific authority currently pinned for existing audits:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

Do not silently substitute a newer DSIR commit into an existing audit. Record an authority delta or new audit revision.

## 1. Project roles

- `Dark-Sector-Influence-Reconstruction` (DSIR): main formal reconstruction/methodology authority.
- `Known-Models-Dark-Sector-Benchmark` (KMDSB): controlled test range that passes known dark-sector and modified-gravity models through the DSIR funnel.
- Future original dark-sector model: must eventually live in a separate repository; KMDSB supplies evidence-derived construction requirements.

## 2. Files to read first in a fresh chat

Read in this order:
1. `recovery/STATE.md` — shortest current handoff/frontier.
2. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md` — methodology accumulated for the future original model.
3. `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md` — frozen B0-B9 per-model funnel.
4. `protocol/WAVE_TESTING_PROTOCOL_v0.1.md` — wave logic.
5. `protocol/STATUS_TAXONOMY.md` — verdict semantics.
6. `matrices/wave_matrix.csv` — wave-level state.
7. `matrices/benchmark_matrix.csv` — per-model state.
8. `matrices/design_prior_ledger.csv` — current design priors DP-*.
9. `logs/research_log.md` — chronology and scientific decisions.
10. Active-wave directory under `waves/`.

Do not reconstruct the project from README alone.

## 3. Frozen benchmark gate sequence

B0 — identity/provenance
B1 — DSIR embedding/reference limit
B2 — conservation/gauge/frame bookkeeping
B3 — physical-domain/numerical control
B4 — response coverage/masks
B5 — LambdaCDM/reference identifiability
B6 — nearest-comparator discrimination
B7 — quotient-surviving residual novelty
B8 — prospective withheld prediction
B9 — synthesis/design-prior extraction

Critical semantic rule: FAIL, NONIDENTIFIABLE, BLOCKED_*, comparator equivalence and physical inconsistency are not synonyms.

## 4. Current wave state at this checkpoint

### W00 — Calibration and semantics
Status: COMPLETE.

M00 LambdaCDM: `CONTROL_PASS_WITH_SCOPE`.

M01 smooth non-phantom DE / local wCDM ray: controlled DSIR deformation but observationally `NONIDENTIFIABLE` in the scoped corrected DESI DR1 ShapeFit control.

Key calibration numbers for M01/B5:
- local amplitude coordinate: `epsilon_w`;
- nuisance-free scoped sensitivity: `sigma(epsilon_w) ~= 0.1782`;
- frozen minimal step: `epsilon_w = 1e-4`;
- significance of that step: about `5.61e-4 sigma`.

Interpretation: this is not physical falsification. It demonstrates that a clean theory-space response can be far below realistic covariance scale.

### W01 — Baseline dark-sector control atlas
Status: COMPLETE.

Models:
- M02 IDE;
- M03 GDM;
- M04 thermal WDM;
- M05 designer f(R);
- M06 decaying CDM -> dark radiation.

Central methodological results:
- IDE requires physical tangent-cone/one-sided geometry before differentiation;
- GDM demonstrates that parameter count is not identified rank and that additional channels such as slip can be high-value degeneracy breakers;
- WDM forces explicit high-k windowing, characteristic-scale and mask discipline;
- designer f(R) forces modified-gravity comparators and explicit near-GR solver-threshold handling;
- DCDM reinforces prospective/temporal holdout semantics.

### W02 — Same-observable degeneracy attack
Status: ACTIVE.

Frozen edges:
- E1 IDE vs GDM;
- E2 IDE vs designer f(R);
- E3 WDM vs alternative small-scale suppression;
- E4 DCDM vs alternative temporal-history mechanism.

E1 status: `PASS_WITH_SCOPE` in unwhitened common low-k `r_Delta(k,z)` tangent geometry on the frozen 7x5 nodes.

Exact stored source:
`waves/wave_02_degeneracy_attack/E1_result.json`

Key values:
- IDE alpha_negative vs GDM cs2: acute angle `24.934547 deg`;
- IDE alpha_negative vs GDM cv2: acute angle `24.786398 deg` (closest pair);
- IDE beta vs GDM cs2: oriented `123.714916 deg`, acute-line `56.285084 deg`;
- IDE beta vs GDM cv2: oriented `123.706615 deg`, acute-line `56.293385 deg`.

Hard interpretation: exact directional equivalence/collinearity is rejected in this frozen theory-response block. Observation-space promotion remains open.

E2 status: `PASS_WITH_SCOPE` in unwhitened common low-k `r_Delta(k,z)` geometry. The f(R) side is the minimum resolved `B0=1e-6` production ray, not an exact B0->0 tangent because of the pinned solver GR threshold.

Exact stored source:
`waves/wave_02_degeneracy_attack/E2_result.json`

Key values:
- IDE alpha_negative vs designer f(R): acute angle `42.450273 deg`; best scalar projection residual fraction `0.674950`;
- IDE beta vs designer f(R): acute angle `59.404101 deg`; residual fraction `0.860778`.

Hard interpretation: exact IDE/f(R) directional equivalence is rejected within this theory-space scope. No slip separator may be claimed because the frozen observability atlas has slip unknown for the relevant sides.

E3 current result: expected/appropriate classification is `BLOCKED_IMPLEMENTATION` unless a second pinned small-scale suppression family is implemented on the same k,z grid, baseline and conventions. Frozen DSIR search found no already prepared fuzzy/axion/SIDM-like high-k response product suitable for a hard comparator edge. Do not fabricate a synthetic comparator.

E4 current frontier: determine whether frozen DSIR contains a second mechanism evaluated in the same temporal-localization coordinate as C6 DCDM. If not, classify as `BLOCKED_IMPLEMENTATION`. Do not compare post-hoc mismatched temporal coordinates.

## 5. Design-prior state

Current ledger:
`matrices/design_prior_ledger.csv`

It contains DP-0001 through DP-0604 (30 active requirements at this checkpoint).

Important rule: these are evidence-derived priors, not axioms for the future model. The construction methodology defines conceptual promotion levels ACTIVE -> REINFORCED -> CORE -> RETIRED. Do not hard-code all current priors into a new theory yet.

## 6. Immediate next actions after restoration

Resume in this order:
1. finish E4 provenance/implementation check against the frozen DSIR snapshot;
2. write explicit E3 and E4 result records with `BLOCKED_IMPLEMENTATION` if no valid second comparator exists;
3. split W02 outputs into a theory-space comparator graph and an observation-space comparator graph;
4. mark W02 COMPLETE only after every frozen edge has a terminal status (`PASS_WITH_SCOPE`, `FAIL`, `NONIDENTIFIABLE`, `BLOCKED_*`, etc.);
5. update `matrices/wave_matrix.csv`, `recovery/STATE.md`, this recovery manual and `logs/research_log.md`;
6. open W03 for an expanded dark-energy family only after W02 closure criteria are met.

## 7. What must never be inferred after restoration

Do not infer that:
- a DSIR gate failure means the physical model is globally false;
- a theory-space angle proves observational distinguishability;
- a missing channel is zero;
- a solver threshold is a physical tangent;
- a retrospective fit is a prospective holdout success;
- an absent comparator can be replaced with a synthetic one without changing the claim class.

## 8. Formula/logic recovery essentials

Canonical DSIR residual:
`X_{mu nu} = M0^2 G_{mu nu} - T^{known}_{mu nu}`.

Local response geometry:
- form physically admissible directional responses/Jacobians only after domain constraints are frozen;
- if one-sided, use a tangent-cone directional derivative rather than symmetric finite differences.

Theory-space direction comparison:
`cos(theta) = (u . v)/(||u|| ||v||)`.

Observation-space whitening:
`J_white = C^{-1/2} R J`.

Nuisance-free local Fisher block:
`F = J^T R^T C^{-1} R J`.

For nuisance parameters, use profiled/marginalized information before making identifiability claims.

## 9. Repository maintenance rule

At every meaningful frontier change update all four layers:
- evidence: per-model/per-edge audit + machine-readable result;
- synthesis: benchmark/wave/design-prior matrices;
- methodology: `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md` when a durable rule changes;
- recovery: `recovery/STATE.md`, this file and chronology in `logs/research_log.md`.

A new chat should be able to resume by reading the repository alone.
