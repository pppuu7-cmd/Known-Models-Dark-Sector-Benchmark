# KMDSB current state / recovery handoff

Updated: 2026-09-09

## Mission
Pass known dark-sector and modified-gravity models through the DSIR benchmark funnel, distinguish physical failure from non-identifiability/blocked coverage/numerical artifacts, and accumulate evidence-derived requirements for a future original dark-sector model.

## Authority state

W00-W02 numerical evidence remains frozen to:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.

W03 starts from:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.

See `recovery/AUTHORITY_DELTAS.md` AD-001. Never silently rebase historical evidence.

## Recovery entry points

1. `recovery/RESTORE_FROM_NEW_CHAT.md`
2. this file
3. `recovery/AUTHORITY_DELTAS.md`
4. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
5. `protocol/W03_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
6. `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`
7. `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`
8. `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`
9. `matrices/wave_matrix.csv`
10. `matrices/benchmark_matrix.csv`
11. `matrices/design_prior_ledger.csv`
12. `logs/research_log.md`
13. active wave directory

## Frozen B0-B9 funnel

B0 identity/provenance -> B1 reference limit -> B2 conservation/gauge/frame -> B3 physical/numerical control -> B4 response/masks -> B5 observational identifiability -> B6 nearest comparator -> B7 quotient-surviving novelty -> B8 prospective holdout -> B9 synthesis/design-prior extraction.

## Completed waves

### W00 — COMPLETE
- M00 LambdaCDM: `CONTROL_PASS_WITH_SCOPE`.
- M01 smooth non-phantom DE/wCDM: `DSIR_COMPATIBLE_NONIDENTIFIABLE` in corrected DESI DR1 ShapeFit control.
- `sigma(epsilon_w) ~= 0.1782`; `epsilon_w=1e-4` gives about `5.61e-4 sigma`.

### W01 — COMPLETE
M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.
Durable lessons: tangent cones before derivatives, multi-channel response, identified rank != parameter count, high-k/mask discipline, MG comparators, prospective holdout semantics.

### W02 — COMPLETE
- E1 IDE/GDM: `PASS_WITH_SCOPE`, closest acute angle `24.786398 deg`.
- E2 IDE/f(R): `PASS_WITH_SCOPE`, acute angles `42.450273`, `59.404101 deg`.
- E3 WDM/alternative suppression: `BLOCKED_IMPLEMENTATION`.
- E4 DCDM/temporal alternatives: `INCONCLUSIVE` under scalar temporal centroid.
Theory and observation graphs remain separate.

## W03 — ACTIVE: M07 canonical scalar-field / quintessence

Pinned solver:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Frozen branch:
`V(phi)=(1+A) exp(-lambda phi)`, `alpha=0`, `B=0`, `attractor_ic_scf=no`, `phi_ini=1`, `phi_prime_ini=0`, physical `lambda`, nuisance `A`, `scf_tuning_index=2`.

Canonical stress:
`rho_phi=[phi_prime^2/(2a^2)+V]/3`,
`p_phi=[phi_prime^2/(2a^2)-V]/3`.

### M07 gate state
- B0 `PASS_WITH_SCOPE`
- B1 `PASS_WITH_SCOPE`
- B2 `PARTIAL`
- B3 `PASS_WITH_SCOPE`
- B4 `PASS_WITH_SCOPE`
- B5 `OPEN`
- B6 `PASS_WITH_SCOPE`
- B7 `OPEN`
- B8 `OPEN`
- B9 `PARTIAL`
- overall `DSIR_COMPATIBLE`

### Reference and shooting calibration

Scale-aware nuisance seed:
`A_seed(lambda)=3 Omega_scf H0^2 exp(lambda phi_ini)-1`.

Subdominant calibration run `34325977559`, Omega_scf=0.10:
- lambda-zero achieved Omega `0.10000000013560413`;
- `max|lnH|=5.46292e-11`;
- `max|lnP|=4.11152e-7`.

Dark-energy-dominant strict production / shooting audit run `34338140447`, target Omega_scf `0.682686955086854`:
- lambda-zero achieved `0.682686955181768`;
- `max|lnH|=1.08876e-10`;
- `max|lnP|=2.16648e-10`.

Default CLASS shooting tolerance created fake finite-lambda target drift up to about `1.23798e-3` at lambda 0.30. Tightening only `tol_shooting_deltax_rel` from `1e-5` to `1e-13` reduced the lambda 0.30 target error to about `3.01e-10`. Default and strict lambda=0.30 matter-response vectors differed by about 38.1% in relative norm. Therefore strict run `34338140447` is authoritative for B4/B6.

### M07 B6 nearest-comparator attack

Run `34358089618`; common unwhitened 7x5 low-k `r_Delta(k,z)` block.

Against C1 smooth-w acute angles:
- lambda .025: `15.9702 deg`
- .075: `6.9206 deg`
- .15: `6.6924 deg`
- .30: `6.6114 deg`

Against frozen designer-f(R) ray:
- `.025: 73.0805 deg`
- `.075: 62.1181 deg`
- `.15: 61.0432 deg`
- `.30: 60.7968 deg`

Interpretation: M07 is strongly near-aligned with smooth-w in low-k matter response but far from the frozen f(R) direction. This is theory-space only, not observational discrimination. Strong alignment means an orthogonal channel is required before mechanism attribution.

### Fixed-coordinate parity failure

Run `34358465646`; fixed `phi_ini=+1`, test lambda -> -lambda; preregistered odd/even threshold `1e-3`.

Results:
- |lambda|=.025: lnP odd/even `7.4666e-3` -> FAIL
- |lambda|=.075: lnP odd/even `2.0277e-3` -> FAIL

This failure is preserved in `waves/wave_03_expanded_dark_energy/M07_FIXED_COORDINATE_PARITY_FAILURE.md`.

### Exact field-reflection quotient parity — PASS

For B=0, exact quotient map:
`(lambda,phi_ini)->(-lambda,-phi_ini)` with zero initial field velocity.

Run `34359042959`; artifact digest `sha256:d5e747fc54aee3a8fe3c50372f5788d6c95bcddc47b3598cf1646d114ff041b1`; preregistered odd-fraction max `1e-6`.

At |lambda|=.025 and .075:
- lnP odd fraction = `0`
- lnH odd fraction = `0`
- plus/minus response angle = `0 deg`

Thus sign(lambda) is redundant on the tested physical quotient. `q=lambda^2` is an admissible invariant coordinate candidate, but parity alone does not prove response linearity in q.

Evidence:
`waves/wave_03_expanded_dark_energy/M07_FIELD_REFLECTION_QUOTIENT_PARITY.md`.

### Current q-linearity / perturbation-precision frontier

Background H response already scales very cleanly with q=lambda^2:
- q-scaled H, lambda .025 vs .075: relative difference about `9.97e-4`, angle about `0.0294 deg`.

Low-k P response does not yet:
- q-scaled P, lambda .025 vs .075: relative difference about `0.2307`, angle `12.5058 deg`.

This channel split suggests a perturbation-sector precision floor rather than immediate failure of the q coordinate.

Active hard computation:
Actions run `34359536106`, workflow `.github/workflows/w03-m07-perturbation-precision-q-audit.yml`.
It compares baseline perturbation precision with a tight tier (`tol_perturbations_integration=1e-8`, `perturbations_sampling_stepsize=0.01`) at lambda .025 and .075 with shooting fixed at `1e-13`.

Preregistered tight-tier q gate:
- relative q-scaled P-vector difference <= `0.05`;
- q-scaled P-vector angle <= `2.0 deg`.

Do not alter these thresholds after seeing the result.

## Future-model methodology state

`matrices/design_prior_ledger.csv` contains **41 ACTIVE requirements**, DP-0001..DP-0807.

New W03 requirements include:
- physical vs nuisance parameter separation;
- natural-scale nuisance initialization;
- reference regression before finite-deformation science;
- perturbation/time tests for microphysical DE;
- phenomenological-DE nearest-comparator attack;
- solver precision audit in ill-conditioned nuisance coordinates;
- quotient exact parameter/field redundancies before local parity, derivative order, Jacobian rank or natural-coordinate claims.

Use `protocol/W03_MODEL_CONSTRUCTION_LESSONS_v0.1.md` for the Wave-03 construction implications.

## Highest-priority continuation

1. inspect completion/artifact of run `34359536106`;
2. if tight perturbation q gate passes, freeze q=lambda^2 as the local quotient coordinate within tested M07 scope and construct its local q-response direction;
3. if it fails, classify whether the remaining mismatch is perturbation solver floor or true q-nonlinearity; do not loosen thresholds;
4. once local coordinate is controlled, move to B2 additional gauge/response audit and orthogonal channel construction;
5. then B5 observational whitening against C1 smooth-w and B7 novelty test;
6. B8 remains untouched until a genuinely prospective relation/holdout is frozen.

## Non-negotiable rules

1. Never zero-impute missing channels.
2. Never equate theory-space separation with observational discrimination.
3. Never equate non-identifiability with falsification.
4. Never fabricate a comparator.
5. Never let shooting alter a frozen physical parameter.
6. Never let solver-default tolerance define a physical response.
7. Quotient exact redundancies before local-rank/coordinate claims.
8. Never promote infrastructure/production grid points retrospectively to B8.
9. Never silently rebase historical evidence to a newer DSIR authority.
10. If chat memory conflicts with repository evidence, repository evidence wins.
