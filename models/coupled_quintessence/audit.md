# M14 coupled quintessence / interacting dynamical DM — provider and K0 audit

Updated: 2026-09-10
Overall current state: `K0_PASS_WITH_SCOPE_K1_SOURCE_AUDIT_REQUIRED`

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

K1 remains `NOT_TESTED` until the exact source dependence of both the q-sector and `cdm_c` sector is audited and a prospective coupling-off regression is frozen.

## Gate ledger

- K0 provenance/authority: `PASS_WITH_SCOPE`.
- K1 reference/decoupling limit: `NOT_TESTED`.
- K2 physical parameter geometry: `NOT_TESTED`.
- K3 conservation/gauge/frame closure: `NOT_TESTED`.
- K4 numerical robustness: `NOT_TESTED` beyond provider executable control.
- K5 multichannel response/rank: `NOT_TESTED`.
- K6 nearest-family manifold: `NOT_TESTED`.
- K7 common observation/covariance: `NOT_TESTED`.
- K8 quotient-surviving novelty/significance: `NOT_TESTED`.
- K9 prospective holdout: `NOT_TESTED`.

No scientific FAIL is recorded.

## Next allowed M14 gate

1. Source-audit the exact full decoupling map, including q1-q4, exp1-exp2, `model_cdm`, and `cdm_c` dependencies.
2. Freeze one author-supported scalar background point and a coupling-off transformation before execution.
3. Run a K1 regression that checks the decoupled branch against its correct uncoupled scalar+CDM comparator in identical solver conventions.
4. Only after K1 passes define nonzero-coupling response coordinates and K2-K5 production grids.

### M14 K1 total-decoupling regression — PASS

Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`. The source audit separates two interaction mechanisms: the q1-q4 `coupling_scf` sector and the hyperbolic field-dependent CDM-mass branch selected by `model_cdm=i` and controlled by `cdm_c`. The prospectively frozen total-decoupling point retained `model_cdm=i`, kept q1-q4=0 and set `cdm_c=0`; the comparator used the identical scalar/cosmological workload with provider-default standard CDM.

After two plumbing-only harness repairs (missing numpy, then duplicate overwrite_root), unchanged physics/thresholds were rerun in Actions run `34443825112`. Both cases exited 0. Frozen metrics: background max symmetric relative difference `7.450488193403606e-12` <= `1e-8`; matched P(k) max symmetric relative difference `0.0` <= `1e-6`. Classification: `M14_K1_DECOUPLING_PASS`. Result commit `52a20ffe3fa4d80a8361540847d8192b04217734`; immutable artifact `10138908138`.

K1 is `PASS_WITH_SCOPE` for this provider/anchor. K2-K9 remain open. Next authorized step is K2 geometry/quotient audit of `cdm_c` around zero with q-sector held at zero; q-sector must be treated as a separate interaction-law axis rather than mixed into one coupling coordinate.


### M14 K2 signed geometry + K4/K5 local response gate

K2 source audit closes the local quotient question for the `cdm_c` axis at the tracked hyperbolic anchor. The provider defines `m_CDM(phi)=m0/2[1-tanh(cdm_c phi)]`; the same frozen anchor uses a directional hyperbolic scalar potential `V(phi)=c1[1-tanh(c2 phi)]` with positive `c2=0.98`. A field reflection therefore does not identify `+cdm_c` and `-cdm_c` while holding the physical scalar anchor fixed. The provider inference generator also admits signed `cdm_c`. K2 is `PASS_WITH_SCOPE` with `c=cdm_c in R`; q1-q4 remain a separate interaction-law axis.

Preregistration: `protocol/W03_M14_K2K5_CDM_C_LOCAL_RESPONSE_PREREGISTRATION_v0.1.md`. Frozen cases were `c={0,+0.01,-0.01,+0.02,-0.02}`. First run `34447848716` executed all physical cases but analyzer-only failed because numpy was absent; immutable diagnostic artifact `10140372383`. A dependency-only repair left all physics and thresholds unchanged. Terminal run `34448063620`, job `102777173085`, artifact `10140443081`, result commit `c43727de9316b76a7b8be8a7f7fb127e4b14b326` executed all five cases.

Frozen result: tangent relative norm mismatch `0.3982074689691215` exceeds `0.10`; tangent angle `16.023831966915793 deg` exceeds `3 deg`. Therefore K4 is `FAIL_LOCAL_CONVERGENCE` for the preregistered .01/.02 local grid. The response is not small (`max |Delta ln O|` at |c|=.01 is `1.0152679911983955`), but K5 is `BLOCKED_BY_K4`; no rank/novelty promotion is allowed from a nonconverged tangent. This is a local-linearization failure, not falsification of coupled quintessence.

### M14 K3 perturbation-closure source audit

The pinned source actively places `cdm_c` in the background CDM density, `rho_cdm_prime`, the scalar effective derivative and Klein-Gordon equation. In `source/perturbations.c`, however, the explicit interacting-DM contribution that would add the field-dependent mass-density perturbation to `delta_cdm` is present only as commented-out code. No active `cdm_c`/`model_cdm==2` perturbation closure was found. Machine-readable audit: `models/coupled_quintessence/k3_perturbation_closure_audit.json`.

K3 is therefore `PARTIAL`: background response can be used with scope, but P(k)/Cl from this branch cannot be promoted as a conservation-complete coupled-quintessence perturbation prediction. This is a provider implementation/closure limitation, not a physical failure of M14.
