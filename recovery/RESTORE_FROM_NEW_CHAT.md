# KMDSB recovery manual — restore from a new chat

Updated: 2026-09-09
Purpose: resume KMDSB/DSIR benchmark development from another chat without relying on conversation memory.

## 0. Authority rule

If chat memory conflicts with repository state, repository evidence wins.

Do **not** assume one DSIR commit applies to every historical result.

- W00-W02 evidence: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`.
- W03 starting authority: `Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`.
- exact transition and 11-commit delta: `recovery/AUTHORITY_DELTAS.md` AD-001.

Never silently rebase an old audit.

## 1. Project roles

- DSIR: formal reconstruction/methodology authority.
- KMDSB: test range for known dark-sector and modified-gravity models through DSIR.
- Future original model: later separate repository; KMDSB supplies evidence-derived requirements.

## 2. Read order in a fresh chat

1. `recovery/STATE.md`
2. `recovery/AUTHORITY_DELTAS.md`
3. `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`
4. `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`
5. `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`
6. `protocol/STATUS_TAXONOMY.md`
7. `matrices/wave_matrix.csv`
8. `matrices/benchmark_matrix.csv`
9. `matrices/design_prior_ledger.csv`
10. `logs/research_log.md`
11. active-wave directory under `waves/`

Do not reconstruct the project from README alone.

## 3. Frozen B0-B9 funnel

B0 identity/provenance  
B1 DSIR embedding/reference limit  
B2 conservation/gauge/frame bookkeeping  
B3 physical-domain/numerical control  
B4 response coverage/masks  
B5 reference/observational identifiability  
B6 nearest-comparator discrimination  
B7 quotient-surviving novelty  
B8 prospective withheld prediction  
B9 synthesis/design-prior extraction

Critical semantics: `FAIL`, `NONIDENTIFIABLE`, `BLOCKED_*`, `INCONCLUSIVE`, comparator degeneracy and physical inconsistency are not synonyms.

## 4. Completed waves

### W00 — Calibration and semantics — COMPLETE

M00 LambdaCDM: `CONTROL_PASS_WITH_SCOPE`.

M01 smooth non-phantom DE/wCDM: DSIR-compatible but `NONIDENTIFIABLE` in the scoped corrected DESI DR1 ShapeFit control.

Calibration:
- `sigma(epsilon_w) ~= 0.1782`;
- frozen `epsilon_w=1e-4`;
- significance about `5.61e-4 sigma`.

Lesson: clean theory response != observational identifiability.

### W01 — Baseline dark-sector control atlas — COMPLETE

M02 IDE, M03 GDM, M04 thermal WDM, M05 designer f(R), M06 DCDM.

Durable results:
- IDE: physical tangent-cone/one-sided geometry precedes differentiation;
- GDM: parameter count != identified rank; additional metric/slip channels can break matter-response near-collinearity;
- WDM: high-k windows, masks and characteristic-scale motion are first-class;
- designer f(R): MG comparators and solver GR-threshold discipline are required;
- DCDM: prospective temporal/withheld semantics must stay explicit.

### W02 — Same-observable degeneracy attack — COMPLETE

Exact closure: `waves/wave_02_degeneracy_attack/result.json`.

Theory/edge states:
- PC1 GDM vs designer f(R): `PASS_WITH_SCOPE` positive control; scale-only near-mimicry is broken by time/full-response information.
- E1 IDE vs GDM: `PASS_WITH_SCOPE`; closest acute theory-response angle `24.7863980743 deg`.
- E2 IDE vs designer f(R): `PASS_WITH_SCOPE`; acute angles `42.4502726930 deg`, `59.4041006897 deg`.
- E3 WDM vs alternative small-scale suppression: `BLOCKED_IMPLEMENTATION`; no second pinned same-convention non-WDM high-k family exists in frozen C0-C6 coverage. This is not WDM uniqueness.
- E4 DCDM vs alternative temporal histories: `INCONCLUSIVE`; a common temporal centroid exists but is too lossy to act as a frozen hard mechanism discriminator.

E4 coordinate:
`q_z(z)=sum_k r(k,z)^2/sum_{z,k}r(k,z)^2`
`z_R=exp[sum_z q_z ln(1+z)]-1`.

DCDM sequence:
`{0.6304573019,0.6343829813,0.6419613202,0.6562403431}`.

Same-coordinate frozen alternatives:
- C1 smooth-w `0.6214182972`;
- IDE alpha-negative `0.9516948867`;
- IDE beta `1.0839529728`;
- GDM cs2 `0.7315736878`;
- GDM cv2 `0.7362246207`;
- designer f(R) `0.4547904059`.

The nearest scalar alternative to sampled DCDM is C1; absolute centroid gaps are about `{0.0090390,0.0129647,0.0205430,0.0348220}`. No preregistered scalar cross-model threshold/covariance exists, so E4 remains `INCONCLUSIVE`.

Keep separate:
- `waves/wave_02_degeneracy_attack/THEORY_SPACE_GRAPH.md`
- `waves/wave_02_degeneracy_attack/OBSERVATION_SPACE_GRAPH.md`

No W02 pairwise theory-space edge was promoted to observational discrimination.

## 5. Design methodology state

Living construction methodology:
`protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`

Pipeline F0-F9:
authority/provenance -> reference limit -> physical geometry -> conservation/gauge/frame -> multi-channel response -> observational whitening -> nearest-comparator attack -> quotient novelty -> prospective holdout -> candidate synthesis.

Current ledger:
`matrices/design_prior_ledger.csv`

Count: **34 ACTIVE requirements, DP-0001..DP-0704**.

W02 additions:
- DP-0701: no uniqueness from an unimplemented comparator;
- DP-0702: theory-space and observation-space graphs remain separate;
- DP-0703: scalar characteristic summaries require full-profile stress tests;
- DP-0704: use the smallest sufficient common block, not the smallest convenient summary.

These are not all axioms. Conceptual promotion remains `ACTIVE -> REINFORCED -> CORE -> RETIRED` after independent/adversarial evidence.

## 6. Active Wave 03

Directory:
`waves/wave_03_expanded_dark_energy/`

Status: ACTIVE.

First target:
M07 canonical scalar-field / quintessence.

M07 audit/result:
- `models/canonical_quintessence/audit.md`
- `models/canonical_quintessence/result.json`

Solver provenance:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Pinned initial branch:
`V(phi)=((phi-B)^alpha+A) exp(-lambda phi)` with `alpha=0`, `B=0`, so `V=(1+A)exp(-lambda phi)`.

Canonical stress from the pinned implementation:
`rho_phi=[phi_prime^2/(2a^2)+V]/3`
`p_phi=[phi_prime^2/(2a^2)-V]/3`.

Important solver semantics:
- default `scf_tuning_index=0` would allow `Omega_scf` shooting to tune `lambda`;
- M07 forbids that because `lambda` is the physical model shape parameter;
- M07 uses `scf_tuning_index=2`, so `A` is the normalization/shooting nuisance;
- `attractor_ic_scf=no`, with explicit initial `phi`/`phi_prime`, avoids conflating the physical branch with CLASS tracking-attractor conventions.

Reference logic:
at `lambda=0` and zero field velocity, `p_phi=-rho_phi`; a split Lambda + constant-scalar control should reproduce total LambdaCDM response if solver/bookkeeping is correct.

Current gate state:
B0 `PASS_WITH_SCOPE`; B1 `PARTIAL`; B2 `PARTIAL`; B3-B8 open; B9 partial; overall `INCONCLUSIVE`.

## 7. M07 implementation-probe chronology

Workflow:
`.github/workflows/w03-m07-quintessence-probe.yml`

Analyzer:
`code/w03_m07_quintessence_probe.py`

Run #1 / Actions run `34319481691`, head `89e0ba040900fa17ada29c35987d322ba9e36b8a`:
- pinned CLASS build: PASS;
- config generation: PASS;
- mandatory REF + lambda-zero run step: FAIL before analysis;
- no physical conclusion permitted;
- original workflow failed before preserving diagnostics.

Workflow was immediately hardened so every case records an exit code and logs/artifacts are uploaded even if mandatory controls fail.

Current diagnostic rerun at this checkpoint:
Actions run `34319672901`, head `f0fbbf2043c4bf6b29c259d5ccd29aec893030f4`.

Mandatory cases:
1. `REF_LCDM`: `Omega_scf=0`;
2. `SCF_SPLIT_L0`: `Omega_scf=0.10`, `lambda=0`, zero explicit initial velocity;
3. finite `lambda={0.05,0.10,0.20}` are **diagnostic only** and cannot become B8 evidence.

Do not freeze a production science threshold from the finite-lambda probe. First diagnose plumbing and numerical reference floor; then preregister the hard production tolerance before production science.

## 8. Immediate restoration actions

1. inspect Actions run `34319672901` status and artifact `w03-m07-quintessence-probe`;
2. read `probe_logs/ref.log`, `probe_logs/scf_l0.log` and `*.exit` first;
3. if config/plumbing error exists, fix it without altering W03 scientific hypotheses;
4. obtain successful REF + lambda-zero control;
5. only then freeze a hard M07 B1 production reference tolerance based on the measured infrastructure floor plus explicit safety margin;
6. run a production scalar branch on the standard DSIR 7x5 low-k grid;
7. attack M07 against M01 smooth-w and M05 designer f(R);
8. no observation-space promotion without pinned covariance/operator.

## 9. Never infer

- gate failure == global theory falsification;
- theory-space angle == observational discrimination;
- missing channel == zero;
- missing comparator == uniqueness;
- solver threshold == physical tangent;
- one scalar characteristic epoch == mechanism identity;
- infrastructure finite-lambda samples == prospective holdout support;
- newest DSIR main == authority for every historical audit.

## 10. Maintenance rule

At every meaningful frontier change synchronize:
- evidence: audit/result and computation artifacts;
- synthesis: benchmark/wave/design-prior matrices;
- methodology: future-model construction rules when durable evidence changes them;
- recovery: `STATE.md`, this file, `AUTHORITY_DELTAS.md` when relevant;
- chronology: `logs/research_log.md`.

A new chat must be able to continue from repository state alone.
