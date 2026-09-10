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