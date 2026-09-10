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

The design-prior ledger contains DP-0001..DP-0604, 30 ACTIVE requirements at this checkpoint.

### Wave 02 active degeneracy attack

E1 IDE vs GDM stored `PASS_WITH_SCOPE` in frozen unwhitened common low-k `r_Delta(k,z)` tangent geometry.
Closest pair: IDE alpha_negative vs GDM cv2, acute angle `24.786398074293924 deg`.

E2 IDE vs designer f(R) stored `PASS_WITH_SCOPE`; acute angles `42.450272692967864 deg` and `59.40410068973369 deg` against the minimum-resolved f(R) production ray.

E3 lacked a valid second same-convention non-WDM high-k comparator and was held for explicit `BLOCKED_IMPLEMENTATION` handling rather than synthetic comparison.

E4 remained open pending a common temporal coordinate.

### Future-model methodology/recovery

Created the F0-F9 construction methodology and full restore-from-new-chat manual. Repository evidence was frozen as the authority if chat memory conflicts.

---

## 2026-09-09 — Iteration 003: Wave 02 closure, authority transition, Wave 03 microphysical DE launch

### DSIR authority delta

DSIR `main` advanced from the W00-W02 frozen authority
`e3276e2193f6a5200b541a194e3175356ae5a1c1`
to
`328f2ca80b724870b851c7fe6366cce1ca5086cd`.

The inspected 11-commit delta contains DSIR4 ordered-join/radial-support/process-recovery work. W00-W02 were not silently rebased. The transition is recorded in `recovery/AUTHORITY_DELTAS.md` AD-001; W03 may start from the newer authority.

### W02 E3 — WDM vs alternative suppression

Terminal state: `BLOCKED_IMPLEMENTATION`.

The pinned WDM high-k block exists, but the frozen DSIR C0-C6 authority contains no second non-WDM small-scale suppression family implemented on a valid matched high-k response grid/baseline. No uniqueness claim is permitted from this coverage gap.

Stored:
- `waves/wave_02_degeneracy_attack/E3_WDM_vs_alt_suppression.md`
- `waves/wave_02_degeneracy_attack/E3_result.json`

### W02 E4 — DCDM vs temporal alternatives

A common amplitude-invariant temporal coordinate was built from the same 7x5 low-k response grid:

`q_z(z)=sum_k r(k,z)^2/sum_{z,k}r(k,z)^2`

`z_R=exp[sum_z q_z ln(1+z)]-1`.

DCDM Exp053A sequence:
`{0.6304573019,0.6343829813,0.6419613202,0.6562403431}`.

Applying the identical coordinate to frozen local response directions gave:
- C1 smooth-w `0.6214182972`;
- IDE alpha-negative `0.9516948867`;
- IDE beta `1.0839529728`;
- GDM cs2 `0.7315736878`;
- GDM cv2 `0.7362246207`;
- designer f(R) `0.4547904059`.

C1 is the nearest scalar comparator to all sampled DCDM points, with absolute gaps about `{0.0090390,0.0129647,0.0205430,0.0348220}`.

Because no preregistered cross-model scalar-distance threshold or observational covariance exists, and one scalar compresses the full temporal profile, E4 is `INCONCLUSIVE`, not PASS and not BLOCKED.

Reproducible calculator:
`code/wave02_temporal_centroid_comparator.py`.

### W02 closure

Wave 02 is COMPLETE.

Frozen edge states:
- PC1 GDM vs f(R): `PASS_WITH_SCOPE`;
- E1 IDE vs GDM: `PASS_WITH_SCOPE`;
- E2 IDE vs f(R): `PASS_WITH_SCOPE`;
- E3 WDM vs alternative suppression: `BLOCKED_IMPLEMENTATION`;
- E4 DCDM vs temporal alternatives: `INCONCLUSIVE`.

All W02 hypotheses H1-H4 are `SUPPORTED` within scope:
1. restricted-block degeneracy != full equivalence;
2. missing implementation creates legitimate blocked edges;
3. minimum discriminating suite is a graph problem;
4. observational promotion is separate.

Separate synthesis files were created:
- `THEORY_SPACE_GRAPH.md`;
- `OBSERVATION_SPACE_GRAPH.md`.

No new W02 pairwise edge was promoted to observational discrimination.

### W02 design-prior deltas

Added DP-0701..DP-0704. Ledger count is now 34 ACTIVE requirements.

Key new constraints:
- no uniqueness from missing comparator implementation;
- separate theory-space and observation-space graphs;
- scalar characteristic summaries require full-profile stress tests;
- use smallest sufficient common response block, not smallest convenient summary.

### W03 opened — Expanded dark-energy mechanisms

W03 status: ACTIVE.
Starting DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`.

First target: M07 canonical scalar-field / quintessence using pinned official CLASS
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Pinned scalar-field branch:
`V(phi)=(1+A)exp(-lambda phi)` (`alpha=0`, `B=0`).

Critical provenance decision:
CLASS default scalar shooting can tune `lambda` (`scf_tuning_index=0`) when `Omega_scf` is targeted. KMDSB forbids this because `lambda` is the physical shape parameter. M07 sets `scf_tuning_index=2`, using `A` only as potential-normalization/shooting nuisance. Explicit non-attractor initial conditions are used.

At `lambda=0` and zero field velocity, the canonical stress has `p_phi=-rho_phi`; a split Lambda + constant scalar should therefore reproduce LambdaCDM total response if implementation/bookkeeping is clean. This is a numerical control to be tested, not assumed.

M07 current gate ledger:
- B0 `PASS_WITH_SCOPE`;
- B1 `PARTIAL`;
- B2 `PARTIAL`;
- B3-B8 open;
- B9 `PARTIAL`;
- overall `INCONCLUSIVE`.

### M07 Actions probe chronology

Created:
- `.github/workflows/w03-m07-quintessence-probe.yml`;
- `code/w03_m07_quintessence_probe.py`;
- `models/canonical_quintessence/audit.md`;
- `models/canonical_quintessence/result.json`.

First Actions run `34319481691` at head `89e0ba040900fa17ada29c35987d322ba9e36b8a`:
- pinned CLASS checkout/build: PASS;
- configs written: PASS;
- mandatory REF + lambda-zero run step: FAIL immediately;
- analysis/artifact steps skipped by original fail-fast workflow.

Interpretation: infrastructure/configuration failure only. No physical M07 conclusion.

The workflow was hardened in commit `f0fbbf2043c4bf6b29c259d5ccd29aec893030f4` to preserve every case exit code, logs and artifact even on mandatory failure, and to enforce the mandatory control only after diagnostics are uploaded.

Diagnostic rerun: Actions run `34319672901`.

Finite `lambda={0.05,0.10,0.20}` points in this probe are explicitly descriptive only. They cannot be promoted to B8 evidence. A hard production reference tolerance will be preregistered only after the infrastructure/reference floor is measured.

### Current frontier

1. finish diagnostic Actions run `34319672901`;
2. inspect preserved REF/lambda-zero logs;
3. repair configuration/plumbing without changing W03 hypotheses;
4. obtain clean lambda-zero split-reference;
5. preregister production B1 tolerance;
6. compute standard DSIR response for a controlled production scalar branch;
7. attack M07 against M01 smooth-w and M05 designer f(R).


---

## 2026-09-10 — Iteration: M11b/M14/M15 provider and representative hardening

### M11b CLASS_GSF
Pinned `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`. Model-6 target cases remained non-executable after the prospectively frozen nonzero kinetic-seed recovery (run `34429876130`: LCDM PASS, 16/16 GSF diagnostics exit 1), while the provider's unmodified model-1 `dgf.ini` executed successfully (provider-control run `34429997792`). The route is terminal provider-specific `BLOCKED_IMPLEMENTATION_PROVENANCE`, not k-essence falsification.

### M15 Scherrer candidate
Pinned `Eladio-Moreno/k-essence-dynamics@f3f010e1ed74c86ce6a431a435fa93988f749ee2`. Provider execution was recovered in run `34430793576`; the earlier apparent failure was an output-prefix harness mistake (`root=output/test_`). Source audit then showed the author example has `Omega_Lambda=0.69`, a matter-like scalar target `DM_schm=0.26`, and stored `f0_schm=0`: separate Lambda supplies acceleration. Classification `REPRESENTATIVE_MISMATCH_NO_M15_PROMOTION`; this example is neither a genuine single-sector M15 unified DM+DE representative nor an M11 DE-only covariant validator. No physical falsification.

### M14 coupled quintessence candidate
Pinned `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. README documents `make clean; make class -j` then `./class iDM.ini`; committed regression/benchmark files reference `iDM.ini` and timing tables record historical exit-code-0 runs. However `iDM.ini` itself is absent from the exact public pinned tree (direct contents fetch 404). KMDSB therefore refuses to reconstruct an author point post hoc. Classification `BLOCKED_PROVENANCE_MISSING_AUTHOR_INPUT`; next recovery is an immutable archival exact config (prefer the provider-cited archive) or another provider. No physics conclusion.

### Methodology delta
Provider execution and family-representative validity are distinct gates. A working solver/example must still pass stress-energy/sector bookkeeping before scientific promotion; a documented but untracked author input cannot be reconstructed and treated as immutable provenance.


### M18 ghost-condensate reference gate
Pinned `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7` model 1. Source-level K1 candidate was frozen prospectively: at lambda=0, `P=-X+c1 X^2`, and the stationary `P_X=0` locus gives `w=-1`. First Actions run `34435874904` stopped before physics on an output-root harness mismatch; build passed. Plumbing-only repair preserved the frozen physical cases. Run `34435998290` then gave LCDM exit 0, unchanged author DGF exit 0, lambda-zero reference exit 139. The provider shooting code explicitly documents an `f1~0` bracketing bug and uses `f1/fabs(f1)` in that regime. Classification: `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER`; K0 `PASS_WITH_SCOPE`, K1 blocked, K2-K9 not tested. No physical M18 failure and no post-hoc IC/source patch authorized.
