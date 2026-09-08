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
Overall: `DSIR_COMPATIBLE`.

Key result: the frozen C1 one-sided local ray is a controlled Theory→Response deformation with a clean LambdaCDM intersection and cross-solver calibration control. B5 remains `PARTIAL` because observational kernels/covariance whitening are still required before a hard identifiability claim.

Design priors added: DP-0101..DP-0104.

### Current scientific frontier
The first genuinely new KMDSB computation should target **M01/B5 observational-space identifiability**, not merely repeat the already-known raw C1 response separation.

Parallel catalogue frontier after that: M02 IDE, whose one-sided physical tangent-cone geometry is already frozen in DSIR and therefore provides a strong adversarial test of the new protocol.
