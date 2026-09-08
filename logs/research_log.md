# KMDSB research log

## 2026-09-08 — Iteration 001: benchmark bootstrap and first controls

### Objective
Create a DSIR-in-action test range analogous in discipline to KMQGB, while preserving the scientific distinctions specific to DSIR.

### Authority inspected
- `pppuu7-cmd/Known-Models-Quantum-Gravity-Benchmark` — architecture pattern: protocol, per-model audits/results, matrices, recovery state and machine-readable records.
- `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1` — DSIR scientific authority.

### Protocol decisions frozen
1. Per-model gates B0–B9 were defined.
2. `FAIL`, `NONIDENTIFIABLE`, `BLOCKED_*`, `NO_NOVELTY_EXPECTED` and control N/A states are semantically distinct.
3. Undefined response cells are masked, never zero-imputed.
4. Raw theory-space separation is not observational discrimination.
5. Prospective withheld prediction is required before predictive/discovery promotion.
6. Every model audit must emit a design-prior delta for future dark-sector model construction.

### M00 LambdaCDM
Overall: `CONTROL_PASS_WITH_SCOPE`.

Key result: KMDSB reproduces the DSIR C0 reference-origin logic without interpreting zero residual as novelty. Scope remains explicit because DSIR G0 is globally PARTIAL pending a broader solver-independent reference suite.

Design priors added: DP-0001..DP-0004.

### M01 smooth non-phantom DE / wCDM local ray
Initial overall: `DSIR_COMPATIBLE`; subsequently promoted to scoped non-identifiability result in Wave 00 after B5 covariance work.

Design priors initiated: DP-0101..DP-0104; later extended by B5 identifiability calibration.

---

## 2026-09-08 — Iteration 002: waves 0-2, future-model methodology and recovery hardening

### Wave 00 closure

Wave 00 `Calibration and semantics` is COMPLETE.

M01/B5 was evaluated in the corrected DESI DR1 ShapeFit control rather than a synthetic covariance.

Scoped nuisance-free local result:
- `sigma(epsilon_w) ~= 0.1782`;
- frozen minimal local step `epsilon_w = 1e-4`;
- corresponding significance about `5.61e-4 sigma`.

Result: M01 is DSIR-compatible but observationally `NONIDENTIFIABLE` in that scoped control. This is explicitly not a physical falsification.

Additional design priors DP-0105 and DP-0106 were added: every clean local response must be compared with a real covariance scale, and weak nuisance-free sensitivity calls for orthogonal observables rather than interpretive complexity.

### Wave 01 closure

Wave 01 `Baseline dark-sector control atlas` is COMPLETE.

Models covered:
- M02 IDE;
- M03 GDM;
- M04 thermal WDM;
- M05 designer f(R);
- M06 DCDM.

Cross-model methodology extracted:
- admissible parameter geometry/tangent cones precede linearization;
- total dark-sector conservation and full-history constraints are explicit;
- parameter count is not identified rank;
- multiple response channels, including slip-like and temporal axes, are valuable degeneracy breakers;
- characteristic-scale motion, high-k windows and masks must be controlled;
- dark-sector claims must be attacked by modified-gravity comparators;
- holdout tests must remain prospective and relation-specific.

The design-prior ledger now contains DP-0001..DP-0604, 30 ACTIVE requirements.

### Wave 02 active degeneracy attack

E1 IDE vs GDM is stored as `PASS_WITH_SCOPE` in the frozen unwhitened common low-k `r_Delta(k,z)` tangent block.

Exact source: `waves/wave_02_degeneracy_attack/E1_result.json`.

Closest adversarial pair:
- IDE alpha_negative vs GDM cv2;
- acute line angle `24.786398074293924 deg`.

Other stored pairs:
- IDE alpha_negative vs GDM cs2: `24.93454727387643 deg`;
- IDE beta vs GDM cs2: oriented `123.71491585045106 deg`, acute `56.285084149548936 deg`;
- IDE beta vs GDM cv2: oriented `123.70661502967042 deg`, acute `56.29338497032958 deg`.

Interpretation is limited to rejection of exact theory-response collinearity in the frozen block. Observation-space promotion remains open.

E2 IDE vs designer f(R) is stored as `PASS_WITH_SCOPE` in the same class of frozen unwhitened low-k comparison.

Exact source: `waves/wave_02_degeneracy_attack/E2_result.json`.

Stored acute angles:
- IDE alpha_negative vs designer f(R): `42.450272692967864 deg`, scalar-projection residual fraction `0.6749500663877402`;
- IDE beta vs designer f(R): `59.40410068973369 deg`, residual fraction `0.8607784571671175`.

The f(R) direction is the minimum resolved `B0=1e-6` production ray, not an exact B0->0 tangent because of the pinned solver GR threshold. Slip cannot be claimed as a separator in this frozen edge because the observability atlas marks it unknown for the relevant sides.

E3 WDM vs alternative small-scale suppression: no already pinned fuzzy/axion/SIDM-like high-k response family was found in the frozen DSIR authority on a directly valid common implementation. The protocol must prefer `BLOCKED_IMPLEMENTATION` to constructing a synthetic comparator.

E4 DCDM vs alternative temporal-history mechanism remains the active same-coordinate provenance check. If no second mechanism exists in the same temporal-localization coordinate, the terminal result must be `BLOCKED_IMPLEMENTATION`.

### Future-model methodology created

Created:
`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`

The methodology converts benchmark pressure into an F0-F9 construction pipeline:
- F0 authority/provenance freeze;
- F1 recoverable reference/decoupling limit;
- F2 physical parameter geometry before differentiation;
- F3 conservation/gauge/frame closure;
- F4 multi-channel response architecture;
- F5 covariance-aware observation-space identifiability;
- F6 nearest-comparator attack;
- F7 quotient-surviving novelty;
- F8 prospective holdout prediction;
- F9 candidate synthesis/promotion.

It also introduces a conceptual design-prior maturation ladder `ACTIVE -> REINFORCED -> CORE -> RETIRED`. This does not silently rewrite the CSV ledger; promotion evidence is to be recorded explicitly as future waves accumulate.

### Recovery system hardened

Created:
`recovery/RESTORE_FROM_NEW_CHAT.md`

Updated:
`recovery/STATE.md`

Updated README entry points so a fresh chat can recover the project without dependence on conversation memory.

Recovery rule frozen:
if chat memory conflicts with repository evidence, repository evidence wins.

### Current frontier

1. finish E4 same-coordinate comparator provenance check;
2. write terminal E3/E4 result records;
3. build separate theory-space and observation-space comparator graphs;
4. close W02 only when every frozen edge has a terminal status;
5. update matrices/methodology/recovery/log;
6. then open W03 expanded dark-energy family.
