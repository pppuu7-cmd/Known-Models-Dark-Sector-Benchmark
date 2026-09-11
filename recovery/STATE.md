# KMDSB current state / recovery handoff

Updated: 2026-09-10
Status: ACTIVE
Repository evidence overrides chat memory.

## 1. Mission
KMDSB is a coverage program: pass all maintained response-distinct known cosmological mechanism families through K0-K9/B0-B9 before deciding EXISTING_SUFFICIENT / ADAPT_EXISTING / HYBRID_REQUIRED / NEW_REQUIRED. Survival counts are not probabilities of truth and blockers are not falsifications.

## 2. Authority/read order
W00-W02 numerical authority: DSIR `e3276e2193f6a5200b541a194e3175356ae5a1c1`; W03 start/M07: `328f2ca80b724870b851c7fe6366cce1ca5086cd`; observation-method overlay from M08: `864952e1520d82473a9e976edfeb69f9899d174d`; later M09/M10 overlay inspected: `bc28acc47cc5facba046741fd09f710ae8da9689`. Exact transitions: `recovery/AUTHORITY_DELTAS.md`.

Fresh-chat order: `RESTORE_FROM_NEW_CHAT.md` -> this file -> required-properties protocol -> census -> mandatory matrix -> wave protocol -> future-model methodology -> benchmark/design ledgers -> research log -> current wave/model files and Actions.

## 3. Mandatory properties
K0 provenance; K1 reference/decoupling; K2 physical geometry/quotient; K3 conservation/gauge/frame/closure; K4 numerical robustness; K5 multichannel response/rank; K6 strongest nearest-family manifold attack; K7 exact common observation operator/covariance; K8 quotient-surviving novelty plus absolute profiled significance; K9 prospective holdout.

## 4. Wave state
W00 COMPLETE; W01 COMPLETE; W02 COMPLETE; W03 ACTIVE; W04 DM PLANNED; W05 MG PLANNED; W06 unified/geometry/adversarial PLANNED; W07 cross-family rigidity PLANNED; W08 true holdout PLANNED; W09+ escape/literature-tail iterative.

## 5. W03 core evidence
- M07 canonical quintessence: clean quotient/reference and within-family support, but full CPL absorbs P+H response to ~1.11%; scoped ShapeFit residual ~1.067%, q=.09 only ~4.23e-4 sigma after CPL profiling. B2/B7 partial.
- M08 CPL: step-stable but anisotropic 2D smooth-DE comparator; parameter count != rank.
- M09 native CLASS EDE: `BLOCKED_IMPLEMENTATION`, not EDE falsification.
- M10 CLASS_EDE scalar EDE: scoped theory-space survivor/discriminated; full CPL leaves ~61.7% P+H residual; K7 exact observation bridge open.
- M11 effective sound-speed representative: at w=-0.95 q_s direction is step-stable and survives full local CPL (~92.56% combined residual) but absolute secondary rank is tiny (~6.94e-4). Covariant validation mandatory before family promotion.
- M12 smooth phantom: response represented by same local constant-w line with opposite orientation (acute angle ~0.03789 deg, line residual ~0.0661%); ghost/stability issue remains separate.
- M13a smooth crossing: `REPRESENTED_BY:M08_WITH_SCOPE`; M13b pinned SimpleMC now supplies a genuine two-field background true-crossing representative with scoped K0/K1 support, but K3 perturbation closure is unavailable and the provider marks two-field ICs unfinished.

## 6. M11b covariant CLASS_GSF route — terminal provider-specific blocker
Pinned `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`, model 6.

- run `34429080377`: build PASS, LCDM PASS, all model-6 GSF cases fail in background shooting/evolution with singular-matrix diagnostics;
- source: `P=X^(n+1)/A^n - V0 phi^m`, `n=(1-cs2)/(2cs2)`;
- frozen nonzero kinetic-seed recovery run `34429876130`: LCDM PASS, all 16 GSF diagnostics fail; `RECOVERY_NO_EXECUTABLE_REGION_IN_FROZEN_LADDER`;
- provider-control run `34429997792`: exact same pinned source builds and unmodified committed model-1 `dgf.ini` runs with fresh background/P(k); `PROVIDER_CONTROL_PASS`;
- no author-supplied working model-6 example found at pin.

Conclusion: this model-6 route is `BLOCKED_IMPLEMENTATION_PROVENANCE`, not physical k-essence failure. Do not continue arbitrary post-hoc IC tuning. M11 covariant promotion remains blocked pending a different independently justified DE implementation.

## 7. Scherrer modified-hi_class candidate — provider PASS but representative mismatch
Pinned `Eladio-Moreno/k-essence-dynamics@f3f010e1ed74c86ce6a431a435fa93988f749ee2`, `Cuadratico/`.

Provider-control recovery: run `34430793576` passes when the harness respects the author input's actual `root=output/test_`; fresh background/P(k)/transfer/perturbation outputs are produced. The earlier apparent failure was only an output-prefix harness error.

Source implements Scherrer-type `G2=-F0+F2*(X-X0)^2-0.5*m_phi^2 phi^2`. But the committed author example has `Omega_Lambda=0.69`, `Omega_cdm=0`, scalar matter target `DM_schm=0.26`, and the modified input source explicitly stores `pba->f0_schm=0` after computing a nominal local f0 value. Therefore acceleration is supplied by a separate Lambda sector and the scalar is matter-like.

Classification: `REPRESENTATIVE_MISMATCH_NO_M15_PROMOTION`.

Consequences:
- not a genuine single-sector unified DM+DE M15 representative;
- not a DE-only M11 covariant validator;
- no K1-K9 scientific promotion from this provider-control;
- not a physical failure of Scherrer k-essence/GCG/unified dark fluid.

Authority files: `models/scherrer_unified_dark_sector/representative_scope_audit.md` and `waves/wave_03_expanded_dark_energy/M15_SCHERRER_REPRESENTATIVE_SCOPE_RESULT.json`.

## 7b. M18 ghost-condensate / dilatonic-ghost reference route — provider-specific K1 blocker

Pinned `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`, model 1. Source implements `P=-X+c1 exp(lambda phi) X^2`; the committed author DGF point uses lambda=.2 and executes. A prospective diagnostic reference was derived before execution: lambda=0 gives shift-symmetric `P=-X+c1 X^2`, whose stationary condensate locus `P_X=0` implies `c1 X=1/2` and `w=-1`.

Run `34435874904` was infrastructure-only: build PASS, then a literal output-root harness mismatch stopped before cases. Plumbing was fixed without changing lambda/IC/shooting physics. Run `34435998290`: LCDM exit 0, unchanged author DGF exit 0, lambda-zero reference exit 139 with no lambda-zero products. Canonical result: `waves/wave_03_expanded_dark_energy/M18_GHOST_CONDENSATE_REFERENCE_PROBE_RESULT.json`; audit: `models/ghost_condensate/audit.md`; immutable artifact: `w03-m18-ghost-condensate-reference-probe`.

The pinned shooting source itself comments `BUG: problem if the guess is very good (f1~0)` and for `fabs(f1)<1e-5` evaluates a step containing `f1/fabs(f1)`. Therefore the symmetric reference route is classified `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER`, not physical ghost-condensate failure. Do not post-hoc tune ICs or patch the external solver to force K1. Search an independent implementation or author-supported numerically regular reference prescription.

## 8. Current frontier
- F11/M11: `THEORY_SURVIVOR_COVARIANT_VALIDATION_BLOCKED`; search for independent covariant DE implementation remains open.
- F13/M13: `BACKGROUND_TRUE_CROSSING_REPRESENTATIVE_K1_PASS_WITH_SCOPE_K3_BLOCKED`. Pinned `ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0` executes on a provider-era Python stack. A prospectively frozen scan of the author's own two uncoupled parameter slices found robust `w=-1` crossings at 5/18 finite nonfallback points already for `z<3`. Exact `mphan=0` reduction to the provider canonical one-field branch gives zero H/rho/w difference, and the positive small-mass ladder scales smoothly ~mphan^2. The same source explicitly says it is still figuring out two-field initial conditions, and this SimpleMC route is background-only; K3 perturbation closure is blocked, so no K4/K5 promotion.
- F14/M14 coupled quintessence: two-provider record retained. Original iDM K1 passes but K3 is partial and K4 fails. Independent IDECAMB K1/K2 pass with scope but repeated K4 controls leave a directional-convergence failure; full serialization gives angle 7.61003 deg >3 deg while norm mismatch passes. No family falsification.
- F15/M15: exact NGCG provider remains open. IDECAMB is background-equivalent and momentum-frame bindable but rejected as an exact perturbation provider because its transfer perturbation closure is not the published gauge-complete decomposed-NGCG closure.
- F16-F17 remain W03 Tier-B queue; F16 running/interacting-vacuum provider search may proceed in parallel only after exact public source provenance is pinned.
- F18/M18 is `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER_SEARCH`: author DGF executes, but the prospectively defined lambda=0 condensate K1 path hits a provider shooting singularity; independent implementation/reference required.

Strict census bookkeeping among F00-F45: 4/46 are terminal/represented in the strict sense (F00, F09, F44, F45); 42 still require strict closure. This count is coverage bookkeeping only.

## 9. Durable methodology rule added at this frontier
A provider executable control is necessary infrastructure evidence but is not representative validation. Before K1/K5 promotion, audit the actual stress-energy decomposition, sector budget, source branch and reference map. Similar labels/Lagrangians or a successful author example do not authorize reassignment to the intended census family.

A second durable rule from M13b: a background true-crossing demonstration is enough to establish mechanism representability at K0/K1 scope, but cannot substitute for source-complete perturbation closure. Multi-DOF background crossing and smooth CPL/PPF crossing are distinct implementations even when both cross w=-1.

## 10. New-model necessity rule
No `NEW_REQUIRED` before sufficient census closure + adversarial cross-family waves + exact common observation/covariance profiling + numerical/gauge/systematic/stability floors + prospective holdout. Current permitted global conclusion: new model may be motivated, but necessity is not established.

## 11. Immediate next allowed gates
1. M13b: search for an independent public perturbation-capable true two-field quintom provider. If none is source-complete, preregister an independent verification implementation from published covariant equations; do not use SimpleMC background-only outputs as K3/K5 evidence.
2. M14: do not shrink beta or change serialization again. Seek an independent source-complete implementation or author-supported branch/initialization prescription before further physical K4/K5 interpretation.
3. M15: continue genuine NGCG/GCG provider search with exact perturbation prescription; do not promote IDECAMB background equivalence to perturbation-family identity.
4. F16: open running/interacting-vacuum provider search in parallel, but no K1 run until exact source/commit, vacuum interaction law, perturbation prescription and LambdaCDM limit are frozen.
5. M18: seek a different public implementation or author-supported numerically regular condensate reference; do not patch/tune CLASS_GSF post hoc.
6. Keep M11b CLASS_GSF terminal and search only independently justified covariant DE routes.

### M14 K1 total-decoupling regression — PASS

Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. The source audit separates two interaction mechanisms: the q1-q4 `coupling_scf` sector and the hyperbolic field-dependent CDM-mass branch selected by `model_cdm=i` and controlled by `cdm_c`. The prospectively frozen total-decoupling point retained `model_cdm=i`, kept q1-q4=0 and set `cdm_c=0`; the comparator used the identical scalar/cosmological workload with provider-default standard CDM.

After two plumbing-only harness repairs (missing numpy, then duplicate overwrite_root), unchanged physics/thresholds were rerun in Actions run `34443825112`. Both cases exited 0. Frozen metrics: background max symmetric relative difference `7.450488193403606e-12` <= `1e-8`; matched P(k) max symmetric relative difference `0.0` <= `1e-6`. Classification: `M14_K1_DECOUPLING_PASS`. Result commit `52a20ffe3fa4d80a8361540847d8192b04217734`; immutable artifact `10138908138`.

K1 is `PASS_WITH_SCOPE` for this provider/anchor. K2-K9 remain open. Next authorized step is K2 geometry/quotient audit of `cdm_c` around zero with q-sector held at zero; q-sector must be treated as a separate interaction-law axis rather than mixed into one coupling coordinate.

## M14 update — signed geometry, local-convergence FAIL, perturbation closure partial

Provider remains `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. K2: signed `cdm_c` is a two-sided physical coordinate at the frozen hyperbolic anchor; `+c` and `-c` are not quotiented by field reflection because the fixed scalar potential is itself directional.

Preregistered K2-K5 run `34448063620` (job `102777173085`, artifact `10140443081`, machine-result commit `c43727de9316b76a7b8be8a7f7fb127e4b14b326`) executed c=0,+-.01,+-.02. K4 fails the frozen local convergence gate: relative tangent mismatch 0.398207 >0.10 and angle 16.0238 deg >3 deg. K5 is blocked by K4; large finite response is not a substitute for a converged tangent.

K3 source audit is PARTIAL: cdm_c coupling is active in background/KG, but the interacting delta_cdm mass-perturbation correction in `source/perturbations.c` is commented out and no active equivalent was found. Do not promote this provider's P(k)/Cl as complete coupled-quintessence perturbation response. No M14 physical falsification.

Immediate M14 next gate: prioritize a source-complete perturbation implementation/provider. A new, independently preregistered smaller-step background-only test may map nonlinear geometry, but it must not erase or relabel the failed .01/.02 K4 gate and cannot close perturbation K3/K5.

## 2026-09-10 — M14 independent IDECAMB frontier after K1/K2/K4 scale audit

Pinned independent provider: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075` over `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`. Compatibility-only `-fallow-argument-mismatch` build recovery does not edit physics.

- theory-only output route: PASS, run `34463892501`, job `102827831899`, artifact `10146717720`, result commit `de0debf99827200ab9cc503d7351b811e73cf8ec`; emits 2000x11 `.quantity` and 2499-row `.theory_cl`.
- K1 interaction-off invariants: PASS_WITH_SCOPE, run `34464322763`, job `102829203132`, artifact `10146904871`, result commit `3af4e94ae84186dd0644af48a2da48199dbabbfe`. Previously unseen `alpha_quint={0.2,0.8}`, exact `beta=0`: all finite, `gQ=0` exactly, relative drift of `a*grhoc_t=1.1147809168407837e-4 <=2e-4`.
- K2: PASS_WITH_SCOPE one-sided `q_beta=beta_cq>=0`; author prior is `[0,0.15]`; no beta^2 quotient.
- K4 parent local grid: FAIL_LOCAL_CONVERGENCE, run `34464786896`, job `102830709421`, artifact `10147076509`, result commit `a88ff59137e0bf4e7b97f27cc8122a79063f1f6f`; beta `.005/.01` gives norm mismatch `0.425623`, angle `4.3851 deg`. K5 blocked.
- prospectively frozen smaller-step recovery: FAIL, run `34465008067`, job `102831413732`, artifact `10147169505`; even finest `.00005/.00010` gives norm mismatch `0.298317`, angle `11.3215 deg`, with large `max|dln rho_de|=4.1418` and `max|dw|=1.9590`. This result does not erase the parent K4 fail.

Do **not** keep shrinking beta steps. The source equations are algebraically continuous at beta=0, while the numerical solution does not approach the beta=0 branch smoothly. Next M14 gate is a provider branch/shooting-continuity audit focused on `GetCorrect_initial` / Broyden root selection and solved `(gU0,gphi0)` continuity. No K5/K6 promotion until this is resolved.

M15 side finding: IDECAMB contains an explicitly commented NGCG coupled-fluid branch with the decomposed-NGCG background interaction form. This makes it a serious candidate rather than an automatic representative mismatch, but perturbation prescription/input-selector provenance remains open. See `models/generalized_chaplygin/idecamb_ngcg_candidate_audit.md`.

## 2026-09-10 — M14 IDECAMB full-serialization control consumed

Run `34467577947` (job `102839655588`, artifact `10148183299`, machine-result commit `283bfac6650ea6683ceba288a1dd08341b16ecb9`) changed only diagnostic text precision and retained beta `{0,5e-8,1e-7}` and frozen K4 thresholds. Combined norm mismatch `0.00807248` passes, but angle `7.61003 deg` fails the `3 deg` criterion. `dw`, TT and EE remain directionally unstable while CDM density, H and qhat are stable. Serialization precision is not a sufficient explanation; K5 remains blocked. Do not shrink beta again or modify output formatting. M14 remains nonterminal and is not physically falsified.

Immediate M14 route: independent source-complete provider or author-supported coupled early-time/branch prescription. In parallel continue M13b and genuine M15 provider searches; F16 may open under its own pinned/preregistered provider.

## 2026-09-10 — M13b SimpleMC true-crossing background/K1 consumed

Pinned provider `ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0`. A modern-environment `DistanceMetric` import blocker was resolved strictly by restoring a provider-era Python 3.8 / sklearn 1.1.3 runtime; provider physics was unchanged. Public `ParseModel('Quintom')` execution is finite.

Prospectively frozen author-slice scan run `34472766666`, result commit `10abd8ae5393c4b81ec6c20029331636e2fe9f3c`: 18/18 finite nonfallback points; 5/18 robustly cross `w=-1` already for the author's `z<3` domain. Classification `M13B_SIMPLEMC_AUTHOR_SLICE_CROSSING_FOUND_WITH_SCOPE`.

Prospectively frozen K1 reference run `34473072953`, result commit `3b98fe8ba6011826e03cc207243ec65355efe821`: at exact `mphan=0`, two-field vs provider canonical one-field branch gives `max|Delta H/H|=0`, `max|Delta rho/rho|=0`, `max|Delta w|=0`, with identical finite nonfallback IC. Positive `mphan={1e-3,5e-4,2.5e-4}` discrepancies fall by ~4x per halving, consistent with smooth leading `mphan^2` dependence.

M13b status is therefore `BACKGROUND_TRUE_CROSSING_REPRESENTATIVE_K1_PASS_WITH_SCOPE_K3_BLOCKED`. Source explicitly marks two-field initial conditions as unfinished, and SimpleMC does not supply the source-complete two-field Boltzmann perturbation closure needed for K3-K5. Do not interpret this as perturbation-level or observational validation. Authority audit: `models/quintom/simplemc_background_representative_audit_2026-09-10.md`.

## 2026-09-10 — M16 interacting-vacuum K0/K1 terminal sync

Pinned IDECAMB/CosmoMC interacting-vacuum subfamily `w=-1`, `Q=beta H rho_de`, `Q_mu || u_c` passed the prospectively frozen beta=0 K1 regression against the same-overlay noninteracting LambdaCDM branch. Run 34474389038, job 102861550642, artifact 10150882133, digest `sha256:f549f3c02de47a4152b89be1a8cbfc4782ffaf8b4671494d45d4216b78520b50`; `.quantity` and `.theory_cl` max symmetric relative difference are both exactly 0.0 on common finite support. K0/K1 are PASS_WITH_SCOPE only. F16 is not yet declared response-distinct from M02 and this does not cover all running-vacuum Lambda(H) models. Next gate: exact M16-vs-M02 family-identity/representation audit before any beta-grid promotion.


## 2026-09-10 — M16/M02 family-identity resolution

The executed IDECAMB interacting-vacuum branch `Q=beta H rho_v`, `Q_mu || u_c` is source-identical in mechanism space to the `alpha=0` submanifold of pinned M02 `kaeonikc/class_iv@ac627d54e9ce196a08878d1ba33999819925d19c`, whose source defines `Q=alpha H rho_m + beta H rho_v` and uses the interacting-pressureless-component-comoving synchronous perturbation branch. Classification: `REPRESENTED_BY:M02_WITH_SCOPE`. Do not launch a duplicate M16 beta response grid. This does not close F16: genuinely response-distinct running-vacuum `Lambda(H)`, `H^2`, `dot H` or derivative laws remain open. Strict census count therefore remains 4/46 terminal/represented families, 42/46 requiring strict closure. Next F16 gate: pin a public genuinely running-vacuum implementation and algebraically audit it against M02 before execution.

## 2026-09-10 — M14 LisaGoh/CDE regularization split + author-branch audit
Consumed run `34490297354`, job `102914977778`, artifact `10157548938`, digest `sha256:1e5d006704453d6d71aea4626d3c105996eee4370886cc226a270fe21f2c888e`. Baseline repeatability passed. Only R2 is noninterfering on author and beta=0 tiny-seed controls, but R2 still fails exact full-reference execution (`R2_exact=1`). R1 opens the exact route but changes nonsingular spectra, so it fails the frozen noninterference requirement; R12 inherits that interference. Upstream `LisaGoh/CDE` branch `7bin@2a572b39d4ae0a3c940b6f179585686ae1a03881` retains the same scalar-velocity zero denominator and `beta_prime/phi_prime_scf` structure; no author-supported regular exact-beta=0 prescription was found. Classification: `M14_LISAGOH_CDE_AUTHOR_BRANCH_REFERENCE_REGULARIZATION_NOT_FOUND`. This is a provider/reference blocker, not physical falsification. Do not continue denominator patches, seed tuning, beta shrinking or serialization changes on this route. Next M14 gate: independent public source-complete provider with author-supported regular reference and active perturbation closure.


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


## 2026-09-11 — W04 M22/M23 K1 closure and new reference-semantics rules
- M22 annihilating-DM native CLASS v1 (`34540790113`) preserved as frozen NOT_ESTABLISHED solely because its preregistered P(k) negative-control threshold was violated. Exact zero/omitted identity was zero and TT/EE/TE passed; P(k) itself contracted smoothly.
- M22 prospective v2 (`34541280629`) PASS: `M22_K1_V2_REFERENCE_LIMIT_PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION`. New sub-v1 tail down to 3.33e-26 m^3 s^-1 J^-1 gives no failing blocks. New-tail exponents: TT=0.915833, EE=0.739755, TE=0.474335, Pk=0.926422. K1 is promoted with effective-energy-injection scope only.
- M22 K3 source audit is PARTIAL: CLASS deposits rho_cdm^2 p_ann energy into recombination/thermodynamics without an explicit matched background DM depletion sink. This is a provider/effective-approximation scope, not annihilating-DM falsification.
- M23 DM-DR/DAO hosted run `34541145589` PASS: `M23_K1_DECOUPLING_PASS_WITH_SCOPE_FIXED_DM_DR_CONTENT`. Omitted-vs-zero coupling identity is exact in TT/EE/TE/P(k); finite Gamma_0 responses contract monotonically with tail exponents TT=1.039107, EE=0.987203, TE=0.997913, Pk=0.998773.
- M23 source K3 is scoped PASS: paired IDM/DR Euler momentum-exchange terms are present; numerical cross-gauge residual regression remains open.
- New durable reference-semantics rules are recorded in `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_W04_ADDENDUM_2026-09-11.md`: parameter-key presence can alter physical defaults; qualitative 'unaffected' statements are not strict null theorems; interaction decoupling normally preserves species content.
- Strict terminal/represented census remains 4/46. Operational polygon readiness estimate advances conservatively to approximately 55%; this is not a strict census metric.
- `NEW_MODEL: DESIGN_AUTHORIZED / NOT_YET_REQUIRED` remains unchanged.


## 2026-09-11 — M21 precision excursion survives support-aware and ncdm-tight audit
- Hosted precision diagnostic run `34540437512` completed successfully with classification `M21_DEFAULT_PRECISION_EXCURSION_PERSISTS`; it is diagnostic-only and does not promote K1.
- Default-v1 CMB excursion factors at f_w=0.003 relative to neighboring f=0.01/0.001 were TT=21.014, EE=75.213, TE=54.340.
- P1 cl_permille leaves the excursion essentially unchanged. P2 adds source-bound ncdm-tight settings including `tol_ncdm_bg=1e-10`, `l_max_ncdm=50`, `ncdm_fluid_approximation=3`, `tol_ncdm_synchronous/newtonian=1e-10`, tighter perturbation integration/sampling; excursion persists and neighboring-point numerical floors shrink, producing a maximum factor 381.554.
- Independent normalized-L2 audit of immutable artifact `10177473119` (digest `sha256:0d03e232511d5da8ba85e16967c7460d68ef0c6868ae07abd09a14efac942151`) also retains the f_w=0.003 anomaly, so this is not merely a pointwise-p95 support artifact.
- CLASS source audit confirms that when fixed `m_ncdm`/`T_ncdm` and an explicit `omega_ncdm` are supplied, the code rescales `factor_ncdm` and `deg_ncdm` to the target abundance; the mixed-fraction coordinate is therefore not rejected as trivially overdetermined.
- Current interpretation: deterministic numerical/solver-branch discontinuity remains localized in CMB. Next clean diagnostic should change the ODE evolver/solver branch at otherwise identical P2 physics and precision. No physical M21 failure.
- Global operational readiness remains approximately 55%; strict terminal/represented coverage remains 4/46.


### 2026-09-11 — M27 high-L hierarchy refinement terminal
Actions run `34564218394`, launch commit `100292b4fd7a016642e5f6a35dbdd903ed489625`, result commit `8d8881349b32970bd1dcc750e7879d53f22d0958`. The prospectively frozen L32->L64 refinement passed 27/27 M27 ensemble branches with maximum amplitude-normalized residual `1.806015929192509e-06`. The earlier L17->L32 failure is preserved (`max=0.004003933161124123`), so the result localizes hierarchy-depth error under prescribed metric forcing rather than erasing the parent negative result. Classification: `M27_DDM_DR_HIGH_L_HIERARCHY_CONVERGENCE_PASS_WITH_PRESCRIBED_METRIC_SCOPE`; K1/K3/K4 global promotion remains false; no physical falsification. Exact next layer is a self-consistent Einstein/metric closure route, preceded by provider-capability/provenance audit where appropriate. Strict census count remains 4/46 terminal/represented.

### 2026-09-11 — M27 stock CLASS multi-parent provider boundary
Validated Actions run `34568316761` (head `5b303e0198150cb1cbfa4d0b263da33ff372e7e8`; jobs source-audit `103164884425`, provider-control `103164884629`, aggregate `103165079604`) completed successfully. The exact pinned stock provider `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540` exposes one scalar `Gamma_dcdm`/one DCDM parent and no native vector/list/indexed multi-parent decay semantics, while the frozen one-species DCDM control executes with finite background, P(k), and C_ell outputs. Canonical result commit `8beb946378b3cf5795288e66e600ffdc3aa74add`: `M27_STOCK_CLASS_MULTI_DCDM_PROVIDER_UNAVAILABLE`. This is a provider capability boundary, not physical DDM falsification and does not promote K1/K3/K4. Allowed continuation: another pinned public multi-parent provider, or a separately preregistered independent covariant implementation with N=1 stock-CLASS regression.

### 2026-09-11 — M28 superfluid background-provider audit
Prospectively frozen audit `protocol/W04_M28_SUPERFLUID_BACKGROUND_PROVIDER_AUDIT_PREREGISTRATION_v0.1.md` pinned `azieg/Superfluid-Dark-Matter-Cosmo@860818c776bf8f000c08e4f02c1a23c5f48a8f52`. Actions run `34572388771` completed: source-audit job `103177121614`, provider-control `103177121964`, aggregate `103177269000`; artifacts `10188258584` (`sha256:5c1617743ad90a027d6aa021ece4bb6da153ded72dd859d9eda875b14eb692a0`) and `10188270990` (`sha256:3e0e786fec6ae99189ca112f534b46693d62f10fb7898cdb1d8a0f8a5645df38`). Canonical result commit `b40d50908e42c5989630371887af0722fa3192e7`: `M28_BACKGROUND_ONLY_PROVIDER_EXECUTABLE_K1_K3_K5_OPEN`. The committed notebook is a genuine superfluid-DM background candidate and executes with finite output, but has no explicit same-model CDM/decoupling coordinate and no perturbation/Boltzmann/Einstein closure. Therefore no K0/K1/K3/K5 promotion and no physical falsification. Continuation is an authoritative source-complete superfluid cosmology provider with explicit reference map; background execution alone cannot establish response-distinctness from CDM.

### 2026-09-11 — M23 cross-gauge PASS_WITH_SCOPE; K4 numerical robustness not established
Validated Actions run `34596841563` (head `5ca2b547a4d5be7bf8f8d8a7be13f00302ab588d`; aggregate job `103256026485`) completed all 14 case×gauge branches after the preregistered IDR precision-key repair. Aggregate artifact `10262840156`, digest `sha256:d36dc8134fe4d4066a0de635093610263915262c072d67152f335ffc86f7a1b4`; canonical result commit `605d97039eedee0d779b8a2d518667a92a32250e`. Classification: `M23_K3_CROSS_GAUGE_NUMERICAL_PASS_WITH_COMMON_OBSERVABLE_SCOPE` and `M23_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED`. All provider executions succeeded. The frozen precision ladder fails K4 because cl_permille->cl_ref differences are non-monotone, especially TT/EE, relative to default->cl_permille; no threshold or physics is retuned. Analysis-only localization is recorded in `M23_K4_PRECISION_LADDER_LOCALIZATION_RESULT.json`. This is not physical NADM/DM-DR falsification.

## 2026-09-11 — W04 numerical-localization update
- M23 shared-CLASS precision-profile transfer control: run `34607933085`, result commit `1c69421819506b4d2ec1bb701ff7401079b7f3ca`, aggregate artifact `10266359162` (`sha256:5c63da518699a50529498dde7f391b8d5a851fabdd1d0e4c3d411d3fadee6412`). Pure LambdaCDM in both synchronous and Newtonian gauges reproduces the same non-nested `default -> cl_permille -> cl_ref` behavior in TT, EE and P(k). Classification `GENERAL_CLASS_PRECISION_PROFILE_NONNESTED_CONTROL`. This localizes the M23 K4 failure to a shared CLASS precision-profile property rather than IDM-DR-specific physics; M23 K4 remains NOT_ESTABLISHED and no physical falsification is inferred.
- M25 explicit-RK manual quadrature recovery: run `34601708310`, result commit `e2208c3ab135ae7de566d9283f7e90599949d4fd`; N=500/1000/2000/4000 all execute. N=2000->4000 P(k) tail-r95 symmetric differences are `[9.9095922e-06, 3.0539054e-06, 1.0696168e-06]`, but manual N=4000 versus the earlier automatic baseline is `[1.9969104, 1.9976967, 1.9978565]`. Classification `M25_M0_PK_QUADRATURE_RK_SENSITIVE`; K1/K4 not promoted; no physical falsification. A matched-evolver automatic-quadrature control is preregistered to remove the remaining evolver confound.

