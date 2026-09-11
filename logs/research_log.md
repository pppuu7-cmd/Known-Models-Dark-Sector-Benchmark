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


### M14 tracked-author-input provider recovery
The earlier broad statement that the pinned `kabeleh/iDM@dc55e59...` tree contained no exact author input was corrected after exhaustive tree search: tracked author-generated PGO inputs exist under `benchmark/*/tmp_ini/`. A prospective provider-control was frozen around `benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini`, permitting only the absolute output-root path to change. Actions run `34439614496` returned build exit 0, CLASS exit 0 and fresh Cl/lensed-Cl/P(k) products. K0 is therefore `PASS_WITH_SCOPE`. K1 remains untested because the workload has q1-q4=0 but `cdm_c=0.1`, and source inspection shows a separate cdm_c-dependent dark-matter/scalar coupling path. The next gate is a source-exact total-decoupling audit followed by a separately preregistered K1 regression. No physics FAIL.

### M14 K1 total-decoupling regression — PASS

Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. The source audit separates two interaction mechanisms: the q1-q4 `coupling_scf` sector and the hyperbolic field-dependent CDM-mass branch selected by `model_cdm=i` and controlled by `cdm_c`. The prospectively frozen total-decoupling point retained `model_cdm=i`, kept q1-q4=0 and set `cdm_c=0`; the comparator used the identical scalar/cosmological workload with provider-default standard CDM.

After two plumbing-only harness repairs (missing numpy, then duplicate overwrite_root), unchanged physics/thresholds were rerun in Actions run `34443825112`. Both cases exited 0. Frozen metrics: background max symmetric relative difference `7.450488193403606e-12` <= `1e-8`; matched P(k) max symmetric relative difference `0.0` <= `1e-6`. Classification: `M14_K1_DECOUPLING_PASS`. Result commit `52a20ffe3fa4d80a8361540847d8192b04217734`; immutable artifact `10138908138`.

K1 is `PASS_WITH_SCOPE` for this provider/anchor. K2-K9 remain open. Next authorized step is K2 geometry/quotient audit of `cdm_c` around zero with q-sector held at zero; q-sector must be treated as a separate interaction-law axis rather than mixed into one coupling coordinate.



### M14 K2/K4/K5 signed-c gate and K3 source closure audit
K2 was source-bound before execution: at the author hyperbolic anchor, signed `cdm_c` is a two-sided physical coordinate rather than a c^2 quotient. A preregistered c={0,+-.01,+-.02} gate was run. Initial run `34447848716` had analyzer-only missing-numpy failure after all physical cases executed. Dependency-only repair preserved frozen physics and thresholds. Terminal run `34448063620`, job `102777173085`, artifact `10140443081`, result commit `c43727de9316b76a7b8be8a7f7fb127e4b14b326` executed all five cases. Frozen K4 failed: tangent norm mismatch 0.398207 (>0.10), angle 16.0238 deg (>3 deg). K5 is blocked even though finite response amplitude is large (max |Delta ln O|~1.015 at |c|=.01). This means the .01/.02 grid is not a reliable local linear tangent; it is not a model falsification.

Independent K3 source audit found the cdm_c interaction active in background/CDM density and the scalar KG equation, while `source/perturbations.c` contains the intended interacting `delta_cdm` mass-density correction only as commented code. K3=`PARTIAL`; provider spectra cannot be promoted as a complete conservation-consistent coupled-quintessence perturbation prediction.


### 2026-09-10 M14 IDECAMB K1/K2/K4 scale-localization
- Recovered author-supported theory output without external likelihoods: run 34463892501 PASS infrastructure only.
- Prospective K1 at unseen alpha=.2,.8: run 34464322763 PASS_WITH_SCOPE; exact gQ=0 and standard CDM dilution invariant.
- K2 source geometry: provider-supported one-sided beta>=0 tangent cone; no sign quotient asserted.
- Frozen K4 beta=.005/.01: run 34464786896 FAIL_LOCAL_CONVERGENCE; K5 blocked.
- Separate preregistered smaller-step ladder down to 5e-5/1e-4: run 34465008067 also FAIL. Norm mismatch improves to 29.83% but angle worsens to 11.32 deg and response remains O(1) in early DE/w. Stop step chasing; audit Broyden/shooting branch continuity.
- No family-level physical falsification and no observational discrimination claim.
- M15: recorded IDECAMB NGCG decomposed-background candidate; perturbation/source-selector binding remains open.

## 2026-09-10 — M14 full-serialization control closes output-precision hypothesis

Consumed run `34467577947` / job `102839655588` / artifact `10148183299` / machine-result commit `283bfac6650ea6683ceba288a1dd08341b16ecb9`. Only serialization precision was increased; physical source, beta `{0,5e-8,1e-7}`, and frozen K4 thresholds were unchanged. All cases exit 0. Combined norm mismatch is `0.00807248`, but angle remains `7.61003 deg >3 deg`. Instability persists in rho_de, w, TT and especially EE, whereas rho_c, H and qhat are stable. Classification: `M14_IDECAMB_FULL_SERIALIZATION_NOT_SUFFICIENT`; K4 remains FAIL and K5 blocked. This excludes output-text precision as the explanation but is not a physical failure of M14.


## 2026-09-10 — M16 interacting-vacuum K0/K1 terminal sync

Pinned IDECAMB/CosmoMC interacting-vacuum subfamily `w=-1`, `Q=beta H rho_de`, `Q_mu || u_c` passed the prospectively frozen beta=0 K1 regression against the same-overlay noninteracting LambdaCDM branch. Run 34474389038, job 102861550642, artifact 10150882133, digest `sha256:f549f3c02de47a4152b89be1a8cbfc4782ffaf8b4671494d45d4216b78520b50`; `.quantity` and `.theory_cl` max symmetric relative difference are both exactly 0.0 on common finite support. K0/K1 are PASS_WITH_SCOPE only. F16 is not yet declared response-distinct from M02 and this does not cover all running-vacuum Lambda(H) models. Next gate: exact M16-vs-M02 family-identity/representation audit before any beta-grid promotion.


## 2026-09-10 — M16/M02 family-identity resolution

The executed IDECAMB interacting-vacuum branch `Q=beta H rho_v`, `Q_mu || u_c` is source-identical in mechanism space to the `alpha=0` submanifold of pinned M02 `kaeonikc/class_iv@ac627d54e9ce196a08878d1ba33999819925d19c`, whose source defines `Q=alpha H rho_m + beta H rho_v` and uses the interacting-pressureless-component-comoving synchronous perturbation branch. Classification: `REPRESENTED_BY:M02_WITH_SCOPE`. Do not launch a duplicate M16 beta response grid. This does not close F16: genuinely response-distinct running-vacuum `Lambda(H)`, `H^2`, `dot H` or derivative laws remain open. Strict census count therefore remains 4/46 terminal/represented families, 42/46 requiring strict closure. Next F16 gate: pin a public genuinely running-vacuum implementation and algebraically audit it against M02 before execution.

## 2026-09-10 — M14 LisaGoh/CDE regularization split and upstream-branch audit
Consumed Actions run `34490297354` / job `102914977778` / artifact `10157548938` (`sha256:1e5d006704453d6d71aea4626d3c105996eee4370886cc226a270fe21f2c888e`). Frozen split result: R2 alone is noninterfering but does not execute exact beta=0; R1 executes an exact route but perturbs nonsingular author/tiny-seed spectra, so it fails noninterference. `LisaGoh/CDE` has visible branches main and 7bin; 7bin head `2a572b39d4ae0a3c940b6f179585686ae1a03881` retains the same unguarded scalar theta denominator and beta-prime/phi-prime term. No author-supported regular exact-reference path found. Classification `M14_LISAGOH_CDE_AUTHOR_BRANCH_REFERENCE_REGULARIZATION_NOT_FOUND`; provider blocker only, no physical FAIL. Census count unchanged. Audit: `models/coupled_quintessence/lisagoh_author_branch_reference_audit_2026-09-10.md`.


## 2026-09-11 — M17 K7a / M19 newest validated frontier
- M17 K7a Planck-2018 Plik_lite covariance attempt persisted at commit `d0b7f411fbc7b150dc6b490a8f26a2be0f850768` with classification `M17_K7A_OPERATOR_OR_OUTPUT_BLOCKED`: both theory cases execute, but provider output ends at ell=2500 while the prospectively frozen operator requires coverage through at least ell=2508. K6 remains unchanged; K7 is only `PARTIAL_COVARIANCE_WEIGHTING_ONLY`; no observational significance claim.
- M19 RECFAST input-localization run `34529493026`, job `103046449912`, artifact `10172921144` (digest `sha256:f29368a15f7f8721f103d8e1951c644e128f383a36aa2c5ed4f4be38512b0cd4`) observes `KMDSB_RECFAST_A=NaN` before RECFAST interpolation. This is an exact-zero provider defect localization, not FDM falsification.
- M19 external-CDM convergence run `34534753238`, job `103063647012`, artifact `10174965834` (digest `sha256:6aa296a14f9ba1149ca3672a99a3a7a896adf032d7c17faf306b303d5565f325`) executes all finite ULA cases `f_ax={0.10,0.03,0.01,0.003,0.001}` but the pinned historical CAMB comparator fails to compile on modern GNU Fortran because `outtransf(EV,...)` collides case-insensitively with an imported symbol. Classification remains `M19_EXTERNAL_CDM_REFERENCE_EXECUTION_BLOCKED`; no K1 promotion.
- A compatibility-only repair has been frozen prospectively in `protocol/W04_M19_EXTERNAL_CDM_REFERENCE_COMPATIBILITY_PREREGISTRATION_v0.1.md`: rename only the local/dummy `EV` identifier to `EVout` inside `outtransf`, archive exact diff, and keep provider pin, cosmology, fractions, outputs and scientific thresholds unchanged. Current launch commit is `f6a029f15b0eacff56a2e785388e68de2ff4ecfe`; consume its Action before any scientific promotion.
- Strict coverage bookkeeping remains 4/46 terminal/represented among F00-F45; 42 still require strict closure.


## 2026-09-11 — M17 K7a measured / M19 blockwise external-limit frontier
- M17 K7a is no longer output-blocked. After prospectively frozen output-coverage and header-format recoveries, the pinned HDE c=0.6 and best-CPL cases both execute through ell=2600 and the validated Planck-2018 Plik_lite 613-bin operator gives S_cov=3.1648604655690433 (S_cov^2=10.0163417665219). This remains fixed-cosmology covariance weighting only; K7b nuisance/cosmological profiling is mandatory before any observational-distinguishability claim.
- M19 external-limit run with the preregistered semantic transfer projection and blockwise analyzer executes every provider point successfully. Passing common blocks: CMB_TE, Pk, T_cdm, T_b, T_r, T_tot. Failing frozen convergence gates: CMB_TT, CMB_EE, T_g, T_nu. Classification is M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_NOT_ESTABLISHED; K1 remains open. The pattern is diagnostic of a likely cross-provider/low-fraction floor in several channels and must not be called FDM falsification.
- Strict terminal/represented coverage remains 4/46. Operational polygon readiness is approximately 50%; this estimate is not a strict census metric.


## 2026-09-11 — M19 low-fraction baseline-floor localization
- Preregistered diagnostic: `protocol/W04_M19_LOW_FRACTION_FLOOR_DECOMPOSITION_PREREGISTRATION_v0.1.md`; analyzer: `verification/m19/low_fraction_floor_decomposition.py`.
- Hosted run `34537372309`, job `103072002975`, artifact `10175920762`, digest `sha256:88f917eebf7c867026d4c19219ddd7c0e1887d08b076feee1db459d337bd850b`; canonical result commit `921aa949b6abe2123df7b527205edb61d7f2241b`.
- Classification: `M19_LOW_FRACTION_BASELINE_FLOOR_LOCALIZED_WITH_SCOPE`. Using only the frozen f_ax={0.01,0.003,0.001} raw outputs, every common block approaches a stable provider-internal linear f_ax->0 asymptote. The previously failing CMB_TT, CMB_EE, T_g and T_nu blocks satisfy the frozen baseline-floor-dominance diagnostic; CMB_TE and T_r do as well. Pk, T_cdm, T_b and T_tot also converge internally but at f_ax=0.001 the finite physical fraction effect is still larger than the external baseline.
- Representative principal exponents: TT p=0.99299, EE p=0.99543, T_g p=0.99022, T_nu p=1.01597. Their fitted external-floor p95 values are respectively 0.020685, 0.030831, 0.0023123 and 0.276188, while their f_ax=0.001 provider-internal finite effects are 0.0003959, 0.0005079, 5.735e-05 and 0.004884.
- Scientific boundary: this strongly localizes the previous frozen nonconvergence to cross-provider baseline mismatch for those channels, but it does NOT promote K1, does NOT validate the crashing exact-zero axionCAMB path, and is NOT FDM falsification. Next gate is matched-baseline calibration or an independent implementation with an executable exact CDM limit.
- Strict terminal/represented census remains 4/46. Operational polygon readiness estimate is now approximately 51%; this is not a strict census metric.


## 2026-09-11 — W04 M20 K1-v2 PASS / M21 v1 methodology diagnostic
- M20 provider control: hosted run `34538139137`, pinned `shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`, upstream physics suite PASS and exact sigma0_m=0 CDM identity on 615 retained entries.
- M20 frozen v1 K1 is preserved as a fail because its universal p>0.5 exponent rule rejected physically nonanalytic channels. Source audit found `rc/rs0 = 2.555*sqrt(tt)+O(tt)` and `tt proportional sigma0_m` near zero, so K1 had incorrectly imposed differentiability.
- M20 preregistered K1-v2 hosted run `34538850087` PASS: classification `M20_K1_V2_NONLINEAR_REFERENCE_LIMIT_PASS_WITH_SCOPE`, no failing blocks, exact-zero identity PASS. Tail exponents: Vmax=0.9999711, rmax=0.9734892, rs=0.8870794, rhos=0.8666173, core=0.4877887. Artifact `10176465023`, digest `sha256:0c47e7ae8887d6081573be1e4dacf4dd2b49e184ee2361db661e5f0374cad0d5`. K1 scope is nonlinear halo response only; no K4/K6/K7 promotion.
- M21 same-solver CLASS exact reference plus finite ladder execute, but frozen v1 K1 result is not interpreted physically. Diagnostic audit identifies a descending-z interpolation error in H (direct H tail exponent p=0.99999903), whole-domain P(k) p95 support saturation despite RMS tail p=0.99569988, and a deterministic high-ell CMB excursion at f_w=0.003 reproduced byte-identically across two hosted runs. K1 remains open pending a prospectively preregistered precision/support-aware v2.
- These two cases add two methodology constraints to the funnel: K1 continuity must not impose universal differentiability, and comparison metrics must canonicalize coordinate orientation plus respect localized response support.
- Strict terminal/represented census remains 4/46. Operational polygon readiness estimate is approximately 53%; this is not a strict census metric.
- `NEW_MODEL: DESIGN_AUTHORIZED / NOT_YET_REQUIRED` remains unchanged.


### 2026-09-11 — M27 high-L hierarchy refinement terminal
Actions run `34564218394`, launch commit `100292b4fd7a016642e5f6a35dbdd903ed489625`, result commit `8d8881349b32970bd1dcc750e7879d53f22d0958`. The prospectively frozen L32->L64 refinement passed 27/27 M27 ensemble branches with maximum amplitude-normalized residual `1.806015929192509e-06`. The earlier L17->L32 failure is preserved (`max=0.004003933161124123`), so the result localizes hierarchy-depth error under prescribed metric forcing rather than erasing the parent negative result. Classification: `M27_DDM_DR_HIGH_L_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE`; K1/K3/K4 global promotion remains false; no physical falsification. Exact next layer is a self-consistent Einstein/metric closure route, preceded by provider-capability/provenance audit where appropriate. Strict census count remains 4/46 terminal/represented.

### 2026-09-11 — M27 stock CLASS multi-parent provider boundary
Validated Actions run `34568316761` (head `5b303e0198150cb1cbfa4d0b263da33ff372e7e8`; jobs source-audit `103164884425`, provider-control `103164884629`, aggregate `103165079604`) completed successfully. The exact pinned stock provider `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540` exposes one scalar `Gamma_dcdm`/one DCDM parent and no native vector/list/indexed multi-parent decay semantics, while the frozen one-species DCDM control executes with finite background, P(k), and C_ell outputs. Canonical result commit `8beb946378b3cf5795288e66e600ffdc3aa74add`: `M27_STOCK_CLASS_MULTI_DCDM_PROVIDER_UNAVAILABLE`. This is a provider capability boundary, not physical DDM falsification and does not promote K1/K3/K4. Allowed continuation: another pinned public multi-parent provider, or a separately preregistered independent covariant implementation with N=1 stock-CLASS regression.

### 2026-09-11 — M28 superfluid background-provider audit
Prospectively frozen audit `protocol/W04_M28_SUPERFLUID_BACKGROUND_PROVIDER_AUDIT_PREREGISTRATION_v0.1.md` pinned `azieg/Superfluid-Dark-Matter-Cosmo@860818c776bf8f000c08e4f02c1a23c5f48a8f52`. Actions run `34572388771` completed: source-audit job `103177121614`, provider-control `103177121964`, aggregate `103177269000`; artifacts `10188258584` (`sha256:5c1617743ad90a027d6aa021ece4bb6da153ded72dd859d9eda875b14eb692a0`) and `10188270990` (`sha256:3e0e786fec6ae99189ca112f534b46693d62f10fb7898cdb1d8a0f8a5645df38`). Canonical result commit `b40d50908e42c5989630371887af0722fa3192e7`: `M28_BACKGROUND_ONLY_PROVIDER_EXECUTABLE_K1_K3_K5_OPEN`. The committed notebook is a genuine superfluid-DM background candidate and executes with finite output, but has no explicit same-model CDM/decoupling coordinate and no perturbation/Boltzmann/Einstein closure. Therefore no K0/K1/K3/K5 promotion and no physical falsification. Continuation is an authoritative source-complete superfluid cosmology provider with explicit reference map; background execution alone cannot establish response-distinctness from CDM.

### 2026-09-11 — M23 cross-gauge PASS_WITH_SCOPE; K4 numerical robustness not established
Validated Actions run `34596841563` (head `5ca2b547a4d5be7bf8f8d8a7be13f00302ab588d`; aggregate job `103256026485`) completed all 14 case×gauge branches after the preregistered IDR precision-key repair. Aggregate artifact `10262840156`, digest `sha256:d36dc8134fe4d4066a0de635093610263915262c072d67152f335ffc86f7a1b4`; canonical result commit `605d97039eedee0d779b8a2d518667a92a32250e`. Classification: `M23_K3_CROSS_GAUGE_NUMERICAL_PASS_WITH_COMMON_OBSERVABLE_SCOPE` and `M23_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED`. All provider executions succeeded. The frozen precision ladder fails K4 because cl_permille->cl_ref differences are non-monotone, especially TT/EE, relative to default->cl_permille; no threshold or physics is retuned. Analysis-only localization is recorded in `M23_K4_PRECISION_LADDER_LOCALIZATION_RESULT.json`. This is not physical NADM/DM-DR falsification.


### 2026-09-11 — M23 shared CLASS precision-profile transfer control
Pure LambdaCDM control at pinned CLASS e85808324f51fc694d12e3ed7439552a3c3f9540 classified `GENERAL_CLASS_PRECISION_PROFILE_NONNESTED_CONTROL` under preregistered stock default -> cl_permille -> cl_ref comparison in synchronous and Newtonian gauges. This diagnostic preserves the parent M23 K3/K4 classifications and is not physical falsification. See `waves/wave_04_dark_matter/M23_CLASS_PRECISION_PROFILE_TRANSFER_CONTROL_RESULT.json`.

## 2026-09-11 — W04 numerical-localization update
- M23 shared-CLASS precision-profile transfer control: run `34607933085`, result commit `1c69421819506b4d2ec1bb701ff7401079b7f3ca`, aggregate artifact `10266359162` (`sha256:5c63da518699a50529498dde7f391b8d5a851fabdd1d0e4c3d411d3fadee6412`). Pure LambdaCDM in both synchronous and Newtonian gauges reproduces the same non-nested `default -> cl_permille -> cl_ref` behavior in TT, EE and P(k). Classification `GENERAL_CLASS_PRECISION_PROFILE_NONNESTED_CONTROL`. This localizes the M23 K4 failure to a shared CLASS precision-profile property rather than IDM-DR-specific physics; M23 K4 remains NOT_ESTABLISHED and no physical falsification is inferred.
- M25 explicit-RK manual quadrature recovery: run `34601708310`, result commit `e2208c3ab135ae7de566d9283f7e90599949d4fd`; N=500/1000/2000/4000 all execute. N=2000->4000 P(k) tail-r95 symmetric differences are `[9.9095922e-06, 3.0539054e-06, 1.0696168e-06]`, but manual N=4000 versus the earlier automatic baseline is `[1.9969104, 1.9976967, 1.9978565]`. Classification `M25_M0_PK_QUADRATURE_RK_SENSITIVE`; K1/K4 not promoted; no physical falsification. A matched-evolver automatic-quadrature control is preregistered to remove the remaining evolver confound.

### 2026-09-11 — M25 matched-evolver quadrature control
Validated run `34614012430`, result commit `97e56cc6e90b4337ac915198362903582d05ca32`, classification `M25_M0_PK_MATCHED_EVOLVER_QUADRATURE_AGREEMENT`. At matched `evolver=0`, automatic quadrature agrees with manual N=4000 with symmetric relative differences `[2.2619695830008982e-4, 6.843414083315417e-5, 2.284619684214263e-5]`, all below the frozen 25% gate. The automatic-RK branch still differs from the immutable older automatic baseline by approximately `[1.99691, 1.99770, 1.99786]`. This localizes the historical discrepancy away from pure quadrature and toward the evolver/compile-capacity numerical layer. K1/K4 are not promoted; physical falsification is false. Next prospectively frozen gate: `protocol/W04_M25_M0_PK_EVOLVER_ISOLATION_CONTROL_PREREGISTRATION_v0.1.md`.

### 2026-09-11 — M25 evolver-isolation control
Prospectively frozen control classified `M25_M0_PK_CAPACITY_OR_EVOLVER_CONFOUNDED`. M25 evolver-isolation classification M25_M0_PK_CAPACITY_OR_EVOLVER_CONFOUNDED. default-vs-explicit-RK D=[0.00033737134333093973, 0.00028064006403436003, 0.00038114151078310097]; raised-cap-default-vs-old-auto D=[1.9969086343781357, 1.9976958815287216, 1.9978555964406235]. Matched-evolver quadrature agreement and manual N=2000->4000 convergence are preserved. K1/K4 are not promoted and physical falsification is false. Canonical machine result: `models/resonant_sterile_neutrino_wdm/M25_M0_PK_EVOLVER_ISOLATION_CONTROL_RESULT.json`.
