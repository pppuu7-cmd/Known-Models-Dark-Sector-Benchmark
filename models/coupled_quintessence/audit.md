# M14 coupled quintessence / interacting dynamical DM — provider and K0 audit

Updated: 2026-09-10
Overall current state: `K1_PASS_ON_INDEPENDENT_IDECAMB_K2_GEOMETRY_NEXT`

## Intended census family

M14 is the microphysical coupled-quintessence family: a dynamical scalar dark-energy degree of freedom coupled to dark matter, with energy-momentum exchange / field-dependent dark-matter response. This is not interchangeable with the earlier phenomenological IDE M02 unless the full response is shown to lie in the same manifold.

## Provider

Pinned source:

`kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`

The provider README describes quintessence interacting with dynamical dark matter and documents `make clean; make class -j` followed by `./class iDM.ini`. The named root `iDM.ini` is absent from the pinned tree, which initially caused a conservative `BLOCKED_PROVENANCE_PROVIDER_SEARCH` classification.

A later exhaustive pinned-tree inspection found tracked author-generated CLASS workloads under `benchmark/*/tmp_ini/`. The recovery control therefore used exact tracked input:

`benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini`

No physical setting was reconstructed. The only runtime change was the absolute author-machine output `root` path.

## Provider-control result

Preregistration:
`protocol/W03_M14_IDM_PROVIDER_CONTROL_RECOVERY_PREREGISTRATION_v0.1.md`

Workflow:
`.github/workflows/w03-m14-idm-provider-control-recovery.yml`

Actions run:
`34439614496`

Machine result:
`waves/wave_03_expanded_dark_energy/M14_IDM_PROVIDER_CONTROL_RECOVERY_RESULT.json`

Result:
- provider build exit: `0`;
- CLASS workload exit: `0`;
- fresh `C_ell`, lensed `C_ell`, linear/nonlinear `P(k)` and parameter products produced;
- classification: `M14_PROVIDER_CONTROL_PASS_TRACKED_AUTHOR_WORKLOAD`.

This closes the broad K0 provenance/executability blocker for this pinned provider with scope. It does **not** promote K1-K9.

## Source-bound caution before K1

The tracked workload comments that it is an uncoupled q-sector configuration and its scalar parameter vector has `q1=q2=q3=q4=0`, while it still sets `model_cdm=i` and `cdm_c=0.1`.

The provider's Cobaya generator explicitly distinguishes:
- uncoupled: `q1=q2=q3=q4=0`, `exp1=exp2=0`;
- coupled: q-sector parameters are varied.

However the source also contains a separate `cdm_c`-dependent dark-matter term (`rho_cdm_prime`) and adds a coupling contribution to the scalar effective derivative. Therefore `q1-q4=0` alone must not be assumed to be the complete physical decoupling map.

## Gate ledger

- K0 provenance/authority: `PASS_WITH_SCOPE`.
- K1 reference/decoupling limit: `PASS_WITH_SCOPE` on both the original iDM anchor and the independent IDECAMB source-exact decoupling invariants.
- K2 physical parameter geometry: `PASS_WITH_SCOPE` for iDM `cdm_c`; `NOT_TESTED` yet for IDECAMB `beta_cq`.
- K3 conservation/gauge/frame closure: `PARTIAL` on iDM; `SOURCE_COMPLETE_WITH_SCOPE` candidate on IDECAMB, numerical closure still open.
- K4 numerical robustness: `FAIL_LOCAL_CONVERGENCE` on the preregistered iDM `.01/.02` grid; `NOT_TESTED` yet on IDECAMB.
- K5 multichannel response/rank: `BLOCKED_BY_K4_K3` for iDM; `NOT_TESTED` on IDECAMB.
- K6 nearest-family manifold: `NOT_TESTED`.
- K7 common observation/covariance: `NOT_TESTED`.
- K8 quotient-surviving novelty/significance: `NOT_TESTED`.
- K9 prospective holdout: `NOT_TESTED`.

No family-level physical falsification is recorded.

### M14 K1 total-decoupling regression — PASS on iDM

Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. The source audit separates two interaction mechanisms: the q1-q4 `coupling_scf` sector and the hyperbolic field-dependent CDM-mass branch selected by `model_cdm=i` and controlled by `cdm_c`. The prospectively frozen total-decoupling point retained `model_cdm=i`, kept q1-q4=0 and set `cdm_c=0`; the comparator used the identical scalar/cosmological workload with provider-default standard CDM.

After two plumbing-only harness repairs (missing numpy, then duplicate overwrite_root), unchanged physics/thresholds were rerun in Actions run `34443825112`. Both cases exited 0. Frozen metrics: background max symmetric relative difference `7.450488193403606e-12` <= `1e-8`; matched P(k) max symmetric relative difference `0.0` <= `1e-6`. Classification: `M14_K1_DECOUPLING_PASS`. Result commit `52a20ffe3fa4d80a8361540847d8192b04217734`; immutable artifact `10138908138`.

### M14 K2 signed geometry + K4/K5 local response gate on iDM

K2 source audit closes the local quotient question for the `cdm_c` axis at the tracked hyperbolic anchor. The provider defines `m_CDM(phi)=m0/2[1-tanh(cdm_c phi)]`; the same frozen anchor uses a directional hyperbolic scalar potential `V(phi)=c1[1-tanh(c2 phi)]` with positive `c2=0.98`. A field reflection therefore does not identify `+cdm_c` and `-cdm_c` while holding the physical scalar anchor fixed. The provider inference generator also admits signed `cdm_c`. K2 is `PASS_WITH_SCOPE` with `c=cdm_c in R`; q1-q4 remain a separate interaction-law axis.

Preregistration: `protocol/W03_M14_K2K5_CDM_C_LOCAL_RESPONSE_PREREGISTRATION_v0.1.md`. Frozen cases were `c={0,+0.01,-0.01,+0.02,-0.02}`. First run `34447848716` executed all physical cases but analyzer-only failed because numpy was absent; immutable diagnostic artifact `10140372383`. A dependency-only repair left all physics and thresholds unchanged. Terminal run `34448063620`, job `102777173085`, artifact `10140443081`, result commit `c43727de9316b76a7b8be8a7f7fb127e4b14b326` executed all five cases.

Frozen result: tangent relative norm mismatch `0.3982074689691215` exceeds `0.10`; tangent angle `16.023831966915793 deg` exceeds `3 deg`. Therefore K4 is `FAIL_LOCAL_CONVERGENCE` for the preregistered .01/.02 local grid. The response is not small (`max |Delta ln O|` at |c|=.01 is `1.0152679911983955`), but K5 is `BLOCKED_BY_K4`; no rank/novelty promotion is allowed from a nonconverged tangent. This is a local-linearization failure, not falsification of coupled quintessence.

### M14 K3 perturbation-closure source audit on iDM

The pinned source actively places `cdm_c` in the background CDM density, `rho_cdm_prime`, the scalar effective derivative and Klein-Gordon equation. In `source/perturbations.c`, however, the explicit interacting-DM contribution that would add the field-dependent mass-density perturbation to `delta_cdm` is present only as commented-out code. No active `cdm_c`/`model_cdm==2` perturbation closure was found. Machine-readable audit: `models/coupled_quintessence/k3_perturbation_closure_audit.json`.

K3 is therefore `PARTIAL`: background response can be used with scope, but P(k)/Cl from this branch cannot be promoted as a conservation-complete coupled-quintessence perturbation prediction. This is a provider implementation/closure limitation, not a physical failure of M14.

## Independent IDECAMB route

Pinned overlay:

- base `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`;
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`.

The provider README explicitly describes IDECAMB as a CAMB/CosmoMC patch for coupled quintessence and coupled fluids. Modern gfortran requires the compatibility-only flag `-fallow-argument-mismatch`; the isolated recovery build passed without changing any physics source.

A dedicated CQ execution control with the documented `Class_IDE=2`, `UForm_CQ=1`, `QForm_CQ=1` passed. The source implements the exponential coupling actively in both background and perturbation objects: `Coup_CQ=beta*grhoc_t*gphidot`, `grhoca2=grhoc/a*exp[-beta(gphi-gphi0)]`, `gC` built from `gQ`, and `gD(1)=gQ`. Unlike the iDM route, the intended perturbation coupling is not a commented placeholder.

### Theory-output route — PASS

The initial output-schema probe kept external Planck/BAO/Pantheon likelihood DEFAULTs while the no-CLIK build intentionally omitted the external Planck likelihood stack; it therefore emitted no diagnostic files and was correctly classified as infrastructure-only `OUTPUT_SCHEMA_NOT_EMITTED`.

A prospectively frozen theory-only route then removed only the external likelihood DEFAULTs, retained `batch3/common.ini`, `action=4`, `get_sigma8=T` and all CQ/cosmological settings, and enabled the author `test_output_root` hook. Run `34463892501`, job `102827831899`, artifact `10146717720` passed and emitted:

- `m14_cq_theory0.quantity`: 2000 numeric rows, 11 columns;
- `m14_cq_theory0.theory_cl`: 2499 numeric rows, 6 columns;
- parameter output.

Classification: `THEORY_OUTPUT_ROUTE_PASS`. Result commit `de0debf99827200ab9cc503d7351b811e73cf8ec`. This was infrastructure only, not a K1 score.

The provider source binds `.quantity` columns as `a,z,grhov_t,grhoc_t,adotoa,wde,gQ,gphi,gphidot,gU,dgU`.

### IDECAMB K1 decoupling invariants — PASS_WITH_SCOPE

Preregistration: `protocol/W03_M14_IDECAMB_K1_DECOUPLING_PREREGISTRATION_v0.1.md`.

To avoid retrospectively scoring the already inspected author-center `alpha_quint=0.02` point, the K1 gate froze two previously unseen scalar anchors: `alpha_quint=0.2` and `0.8`, both with exact `beta_cq=0`. Source identities require `gQ=0`, standard CDM dilution `a*grhoc_t=constant`, and vanishing active interaction-source coefficients.

Terminal Actions run `34464322763`, job `102829203132`, artifact `10146904871`, result commit `3af4e94ae84186dd0644af48a2da48199dbabbfe` passed both anchors. Each produced 2000x11 `.quantity` and 2499-row `.theory_cl`, all parsed values finite; every serialized `gQ` value is exactly zero. The measured relative drift of `a*grhoc_t` is `1.1147809168407837e-4` at both anchors, below the prospectively frozen `2e-4` serialization-aware threshold.

Classification: `M14_IDECAMB_K1_DECOUPLING_PASS_WITH_SCOPE`. Scope is explicit: this is a source-exact interaction-off invariant test across prospectively withheld scalar dynamics, not an independent cross-solver comparator.

## Next allowed M14 gate

1. Source-bind IDECAMB `beta_cq` physical domain/quotient. The author input prior is one-sided (`0..0.15`), but the equations are algebraically signed; do not infer a two-sided physical coordinate until field/coupling sign equivalences are audited.
2. After K2 is frozen, preregister an IDECAMB K4/K5 local response/convergence grid around `beta_cq=0` using the now validated theory-output schema.
3. If K4 passes, measure multichannel rank and then attack with the nearest full comparator manifold (M02 phenomenological IDE and smooth-DE/CPL directions as appropriate).
4. Keep the original iDM K4 failure and K3 limitation as provider-specific authoritative results; the independent IDECAMB route does not erase them.
