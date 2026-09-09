# KMDSB current state / recovery handoff

Updated: 2026-09-09

## Authority
- W00-W02: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03: `Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- transition: `recovery/AUTHORITY_DELTAS.md` AD-001.
- repository evidence overrides chat memory.

## Recovery read order
1. `recovery/RESTORE_FROM_NEW_CHAT.md`
2. this file
3. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
4. `protocol/W03_MODEL_CONSTRUCTION_LESSONS_v0.1.md`
5. `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`
6. `matrices/design_prior_ledger.csv`
7. `models/canonical_quintessence/audit.md`
8. `models/canonical_quintessence/result.json`
9. `waves/wave_03_expanded_dark_energy/`

## Completed waves
- W00 COMPLETE: M00 LambdaCDM control; M01 smooth-w is scoped `NONIDENTIFIABLE` in corrected ShapeFit (`sigma(epsilon_w)~0.1782`, epsilon=1e-4 -> ~5.61e-4 sigma).
- W01 COMPLETE: M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM.
- W02 COMPLETE: E1 IDE/GDM `PASS_WITH_SCOPE` (24.7864 deg closest); E2 IDE/f(R) `PASS_WITH_SCOPE` (42.4503/59.4041 deg); E3 `BLOCKED_IMPLEMENTATION`; E4 `INCONCLUSIVE`.

## W03 ACTIVE — M07 canonical quintessence

Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Branch:
`V=(1+A)exp(-lambda phi)`, alpha=0, B=0, non-attractor IC, phi_ini=1, phi'_ini=0, A shooting nuisance, physical parameter reduced by exact field-reflection quotient.

Current gates:
B0 PASS_WITH_SCOPE; B1 PASS_WITH_SCOPE; B2 PARTIAL; B3 PASS_WITH_SCOPE; B4 PASS_WITH_SCOPE; B5 OPEN; B6 PASS_WITH_SCOPE; B7 OPEN; B8 OPEN; B9 PARTIAL. Overall `DSIR_COMPATIBLE`.

### Numerical controls
Natural seed:
`A_seed=3 Omega_scf H0^2 exp(lambda phi_ini)-1`.

Authoritative strict production run `34338140447`, digest `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`.
Lambda-zero full-DE reference:
- target Omega `0.682686955086854`;
- achieved `0.682686955181768`;
- max|lnH| `1.08876e-10`;
- max|lnP| `2.16648e-10`.

Default shooting tolerance caused fake Omega drift up to `1.23798e-3` at lambda=.30 and ~38.1% response-norm distortion. Strict `tol_shooting_deltax_rel=1e-13` is authoritative.

### B6 comparator
Run `34358089618`, low-k 7x5 theory-space.
M07 vs smooth-w angles: 15.9702, 6.9206, 6.6924, 6.6114 deg for lambda .025,.075,.15,.30.
M07 vs f(R): 73.0805,62.1181,61.0432,60.7968 deg.
Strong smooth-w near-degeneracy; no observational claim.

### Quotient geometry
Fixed phi_ini parity run `34358465646` FAILED preregistered 1e-3 lnP odd-fraction gate (7.47e-3, 2.03e-3). Preserve failure.

Exact field-reflection quotient `(lambda,phi)->(-lambda,-phi)` run `34359042959` PASSED: odd fractions exactly 0 and pair angles 0 deg at |lambda|=.025,.075. Digest `sha256:d5e747fc54aee3a8fe3c50372f5788d6c95bcddc47b3598cf1646d114ff041b1`.

### Local coordinate q=lambda^2 — PASS_WITH_SCOPE
Perturbation precision audit run `34359536106`, digest `sha256:6cd91f54d94982425cbec2055c42f7e087458ae3a4e350796f9a661623240b5d`.
Frozen tight settings: `tol_perturbations_integration=1e-8`, `perturbations_sampling_stepsize=0.01`.
Frozen gate: q-scaled P relative difference <=0.05 and angle <=2 deg.
Measured lambda .025 vs .075:
- relative difference `5.51889e-4`;
- angle `0.0273111 deg`;
- qscaled norms `0.11748477`, `0.11745212`.
PASS.

Therefore within this branch/scope the correct local invariant coordinate is `q=lambda^2`; meaningful local direction is `dr/dq`, not `dr/dlambda|0`.
Machine direction: `waves/wave_03_expanded_dark_energy/M07_LOCAL_Q_DIRECTION.json`.
Local q direction vs C1 smooth-w: `6.69445 deg`; vs C5 f(R): `60.72848 deg`.

### Active B2 gauge audit
Actions run `34360101877`, workflow `.github/workflows/w03-m07-gauge-bookkeeping-audit.yml`.
Paired synchronous/Newtonian internal gauges at lambda=.075 with tight perturbation and shooting settings. Outputs use `matter_source_in_current_gauge=no` and `get_perturbations_in_current_gauge=no` so physical `P`, `d_m`, `phi`, `psi` should regress across internal gauges.
Frozen raw gauge max relative threshold: `1e-4`; response-lnP L2 relative threshold: `5e-3`.
Do not change thresholds after result.

## Future-model design priors
`matrices/design_prior_ledger.csv`: 42 ACTIVE requirements DP-0001..DP-0808.
New W03 core pressures: physical/nuisance separation; natural-scale initialization; solver-tolerance audit; phenomenological nearest comparator; quotient exact redundancies before rank; channel-wise numerical convergence of local coordinates.

## Immediate continuation
1. inspect run `34360101877` and artifact;
2. if PASS, promote B2 within paired-gauge scope and freeze gauge regression evidence;
3. next build orthogonal metric/time response against C1 smooth-w using the now-controlled local q direction;
4. then B5 covariance whitening and B7 quotient-surviving novelty;
5. B8 remains untouched until a genuinely prospective relation is frozen.

## Non-negotiable
No zero-imputation; no theory-angle=observational claim; no numerical failure=physical failure; no missing comparator=uniqueness; no shooting of physical lambda; no unquotiented rank claims; no retrospective B8; no silent authority rebase.
