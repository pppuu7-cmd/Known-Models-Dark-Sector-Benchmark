# KMDSB current state / recovery handoff

Updated: 2026-09-09

## Mission
Pass known dark-sector and modified-gravity models through the DSIR benchmark funnel, distinguish physical failure from non-identifiability/blocked coverage, and accumulate evidence-derived requirements for a future original dark-sector model.

## Authority state

W00-W02 numerical evidence remains frozen to:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

DSIR main checked before W03:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`

The 11-commit inspected delta is recorded in `recovery/AUTHORITY_DELTAS.md` as AD-001. W03 may use the newer authority; old waves are not silently rebased.

## Recovery entry points

1. `recovery/RESTORE_FROM_NEW_CHAT.md`
2. `recovery/AUTHORITY_DELTAS.md`
3. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
4. `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`
5. `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`
6. `matrices/wave_matrix.csv`
7. `matrices/benchmark_matrix.csv`
8. `matrices/design_prior_ledger.csv`
9. `logs/research_log.md`
10. active wave directory

## Gate sequence

B0 identity/provenance -> B1 DSIR embedding/reference limit -> B2 conservation/gauge/frame -> B3 physical/numerical control -> B4 response/masks -> B5 reference identifiability -> B6 nearest comparator -> B7 quotient-surviving novelty -> B8 prospective holdout -> B9 synthesis/design-prior extraction.

## Wave state

### W00 Calibration and semantics — COMPLETE

- M00 LambdaCDM: `CONTROL_PASS_WITH_SCOPE`.
- M01 smooth non-phantom DE/wCDM: `DSIR_COMPATIBLE_NONIDENTIFIABLE` in the scoped corrected DESI DR1 ShapeFit control.
- Calibration: `sigma(epsilon_w) ~= 0.1782`; frozen `epsilon_w=1e-4` gives about `5.61e-4 sigma`.

### W01 Baseline dark-sector control atlas — COMPLETE

M02 IDE, M03 GDM, M04 WDM, M05 designer f(R), M06 DCDM completed in frozen scopes.

Durable lessons: tangent-cone geometry before differentiation; multiple channels; parameter count != identified rank; high-k/mask discipline; MG comparators; prospective holdout semantics.

### W02 Same-observable degeneracy attack — COMPLETE

Machine closure: `waves/wave_02_degeneracy_attack/result.json`.

Terminal edges:
- PC1 GDM vs designer f(R): `PASS_WITH_SCOPE` theory-response positive control;
- E1 IDE vs GDM: `PASS_WITH_SCOPE`; closest frozen acute angle `24.786398 deg`;
- E2 IDE vs designer f(R): `PASS_WITH_SCOPE`; acute angles `42.450273 deg`, `59.404101 deg`;
- E3 WDM vs alternative small-scale suppression: `BLOCKED_IMPLEMENTATION`; no second pinned same-convention high-k mechanism exists in frozen C0-C6 coverage;
- E4 DCDM vs temporal alternatives: `INCONCLUSIVE`; a common scalar temporal centroid exists but is not a hard mechanism separator.

E4 common coordinate:
`q_z(z)=sum_k r(k,z)^2/sum_{z,k} r(k,z)^2`
`z_R=exp[sum_z q_z ln(1+z)]-1`.

DCDM `z_R={0.6304573,0.6343830,0.6419613,0.6562403}`. Frozen alternative centroids: C1 `0.6214183`, IDE `0.9516949/1.0839530`, GDM `0.7315737/0.7362246`, designer f(R) `0.4547904`. Scalar `z_R` therefore remains lossy/inconclusive for cross-mechanism discrimination.

Separate graph files:
- `waves/wave_02_degeneracy_attack/THEORY_SPACE_GRAPH.md`
- `waves/wave_02_degeneracy_attack/OBSERVATION_SPACE_GRAPH.md`

No new W02 pairwise edge was promoted to observational discrimination.

### W03 Expanded dark-energy mechanisms — ACTIVE

First target: M07 canonical scalar-field / quintessence.

Starting W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`.
Pinned scalar solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Frozen initial branch:
`V(phi)=(1+A) exp(-lambda phi)`, explicit non-attractor IC, physical `lambda`, `A` as `Omega_scf` shooting nuisance (`scf_tuning_index=2`).

M07 current gates:
- B0 `PASS_WITH_SCOPE`;
- B1 `PARTIAL`;
- B2 `PARTIAL`;
- B3-B8 open;
- B9 `PARTIAL`;
- overall `INCONCLUSIVE` during calibration.

Active hard computation:
GitHub Actions run `34319481691`, workflow `.github/workflows/w03-m07-quintessence-probe.yml`, head `89e0ba040900fa17ada29c35987d322ba9e36b8a`.

Mandatory implementation controls:
1. pure LambdaCDM `Omega_scf=0`;
2. split-reference scalar `Omega_scf=0.10`, `lambda=0`, explicit zero initial velocity;
3. finite `lambda={0.05,0.10,0.20}` are diagnostic only and cannot become B8 evidence.

The probe must determine the actual numerical reference floor before a hard production tolerance is preregistered.

## Future-model methodology state

`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md` defines F0-F9.

`matrices/design_prior_ledger.csv` now contains DP-0001..DP-0704: **34 ACTIVE requirements**.

Wave-02 additions:
- DP-0701 no uniqueness from missing comparator;
- DP-0702 separate theory/observation graphs;
- DP-0703 stress-test scalar summaries against fuller profiles;
- DP-0704 smallest sufficient common block, not smallest convenient summary.

These remain evidence priors, not automatic axioms. Conceptual maturation: ACTIVE -> REINFORCED -> CORE -> RETIRED.

## Highest-priority continuation

1. inspect completion/artifact of Actions run `34319481691`;
2. if REF or lambda=0 split control fails, diagnose implementation without promoting any science claim;
3. if the probe succeeds, record numerical floor and preregister a hard M07 reference tolerance before production finite-lambda testing;
4. then map the controlled M07 production branch onto the standard DSIR 7x5 low-k response grid;
5. attack M07 against M01 smooth-w and M05 designer f(R) on valid common blocks;
6. update audit/result/matrices/methodology/recovery/log every time the frontier changes.

## Non-negotiable rules

1. Never zero-impute missing channels.
2. Never equate theory-space separation with observational discrimination.
3. Never equate non-identifiability with falsification.
4. Never fabricate a comparator to force PASS/FAIL.
5. Physical model parameters and solver shooting/nuisance parameters must remain explicitly separated.
6. Never use infrastructure-probe finite-lambda output as retrospective B8 evidence.
7. Never silently rebase old audits onto a newer DSIR authority.
8. If chat memory conflicts with repository state, repository evidence wins.
