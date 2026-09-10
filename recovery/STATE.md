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
- M13a smooth crossing: `REPRESENTED_BY:M08_WITH_SCOPE`; M13b true covariant multi-DOF quintom remains mandatory.

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
- F13/M13: partial; true multifield quintom provider/provenance open.
- F14/M14 coupled quintessence: `K0_PASS_WITH_SCOPE_K1_SOURCE_AUDIT_REQUIRED`. Although root `iDM.ini` is absent, the exact pinned tree contains tracked author-generated workload `benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini`. Prospectively preregistered run `34439614496` builds the provider and executes that workload with exit 0 and fresh Cl/P(k) products after a root-only plumbing edit. K1 is not promoted: q1-q4=0 but `cdm_c=0.1`, and source contains a separate cdm_c-dependent coupling path; audit the complete decoupling map before any reference regression.
- F15/M15: `QUEUED_REPRESENTATIVE_SEARCH`; Scherrer candidate rejected on family-identity bookkeeping, so a genuine generalized-Chaplygin/unified-dark-fluid provider is still required.
- F16-F17 remain W03 Tier-B queue.
- F18/M18 is now `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER_SEARCH`: author DGF executes, but the prospectively defined lambda=0 condensate K1 path hits a provider shooting singularity; independent implementation/reference required.

Strict census bookkeeping among F00-F45: 4/46 are terminal/represented in the strict sense (F00, F09, F44, F45); 42 still require strict closure. This count is coverage bookkeeping only.

## 9. Durable methodology rule added at this frontier
A provider executable control is necessary infrastructure evidence but is not representative validation. Before K1/K5 promotion, audit the actual stress-energy decomposition, sector budget, source branch and reference map. Similar labels/Lagrangians or a successful author example do not authorize reassignment to the intended census family.

## 10. New-model necessity rule
No `NEW_REQUIRED` before sufficient census closure + adversarial cross-family waves + exact common observation/covariance profiling + numerical/gauge/systematic/stability floors + prospective holdout. Current permitted global conclusion: new model may be motivated, but necessity is not established.

## 11. Immediate next allowed gates
1. M14: K0 provider recovery is complete with scope via tracked author workload and run `34439614496`. Source-audit the complete coupling/decoupling map including q1-q4, exp1-exp2, `model_cdm` and `cdm_c`.
2. Only after the total coupling-off transformation is source-bound, prospectively preregister a K1 regression against the correct uncoupled scalar+CDM comparator.
3. If K1 PASSes, define physical coupling coordinates/tangent geometry and only then launch K2-K5 production response grids.
4. In parallel continue M13b and M15 genuine-provider searches; do not repurpose Scherrer or CPL as coverage shortcuts.
5. M18: seek a different public implementation or author-supported numerically regular condensate reference; do not patch/tune CLASS_GSF post hoc.
6. Keep M11b CLASS_GSF terminal and search only independently justified covariant DE routes.

### M14 K1 total-decoupling regression — PASS

Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. The source audit separates two interaction mechanisms: the q1-q4 `coupling_scf` sector and the hyperbolic field-dependent CDM-mass branch selected by `model_cdm=i` and controlled by `cdm_c`. The prospectively frozen total-decoupling point retained `model_cdm=i`, kept q1-q4=0 and set `cdm_c=0`; the comparator used the identical scalar/cosmological workload with provider-default standard CDM.

After two plumbing-only harness repairs (missing numpy, then duplicate overwrite_root), unchanged physics/thresholds were rerun in Actions run `34443825112`. Both cases exited 0. Frozen metrics: background max symmetric relative difference `7.450488193403606e-12` <= `1e-8`; matched P(k) max symmetric relative difference `0.0` <= `1e-6`. Classification: `M14_K1_DECOUPLING_PASS`. Result commit `52a20ffe3fa4d80a8361540847d8192b04217734`; immutable artifact `10138908138`.

K1 is `PASS_WITH_SCOPE` for this provider/anchor. K2-K9 remain open. Next authorized step is K2 geometry/quotient audit of `cdm_c` around zero with q-sector held at zero; q-sector must be treated as a separate interaction-law axis rather than mixed into one coupling coordinate.

