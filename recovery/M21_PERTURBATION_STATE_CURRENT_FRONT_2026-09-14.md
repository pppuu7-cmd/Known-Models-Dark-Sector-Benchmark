# M21 perturbation-state current front — 2026-09-14

## STATE_READ

Authoritative repository: `pppuu7-cmd/Known-Models-Dark-Sector-Benchmark`.
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Do not return to stage-2/stage-3, thermodynamics column mining, or one-direction transfer-l tail tightening as if they were unresolved.

## TERMINAL NUMERICAL LOCALIZATION BEFORE THIS FRONT

1. Stage-3 single-parameter decomposition: `tol_thermo_integration`, `l_logstep`, and `l_linstep` are the only sufficient/reducing single controls among the frozen G1A/G2B set.
2. Thermodynamics tolerance direction: `M21_THERMO_TOL_NONMONOTONE_DIRECTIONAL_RESPONSE`; no monotone thermodynamics tolerance limit was established.
3. Cross-evolver recovery: `M21_THERMO_EVOLVER_DEPENDENCE_MIXED`; 1e-5 removal is shared by NDF15/RK, 1e-6 excursion is shared, 1e-7 differs by solver.
4. Thermodynamics primary+secondary exposed-state audits: final class `M21_CMB_BRANCH_NOT_LOCALIZED_IN_EXPOSED_THERMO_STATE_COLUMNS`. Preregistered consequence closes further mining of the same thermodynamics output table.
5. Transfer-l tail: `M21_G2B_L_SAMPLING_TAIL_REMOVAL_NOT_STABLE`; denser one-direction tightening does not define a stable global limit.
6. Transfer-l grid-phase factorial: `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE`. At near-fixed sparse-l node count, l=400-present layouts are HIGH while l=400-absent layouts are CALM. This is downstream numerical phase sensitivity, not a CLASS-defect or physical conclusion.

Canonical secondary thermodynamics summary:
`waves/wave_04_dark_matter/M21_THERMO_SECONDARY_STATE_BRANCH_SIGNATURE_TERMINAL.json`.

## TERMINAL PERTURBATION OUTPUT CAPABILITY

Protocol:
`protocol/W04_M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_v0.1.md`.

Run `34894971251`, artifact `10368099599`, digest `sha256:d74ff4f12ca313c8f27b432348728f8f545b301fd3b468b38554c63e93649dad`.

Classification:
`M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_PASS_WITH_SCOPE`.

Exact-CDM native scalar perturbation table is reproducible and has 6931 rows x 17 columns:
`tau,a,delta_g,theta_g,shear_g,pol0_g,pol1_g,pol2_g,delta_b,theta_b,psi,phi,delta_ur,theta_ur,shear_ur,delta_cdm,theta_cdm`.

Reference geometry:
- tau0 = `14182.53118318 Mpc`
- tau_star = `280.8165335002 Mpc`
- z_star = `1088.78`
- D_star = `13901.714649679801 Mpc`

Frozen successor anchors from l=[100,400,800,1200,2000]:
- `0.00719335725988`
- `0.0287734290395`
- `0.057546858079`
- `0.0863202871185`
- `0.143867145198` Mpc^-1.

Canonical capability:
`waves/wave_04_dark_matter/M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_TERMINAL.json`.
Config:
`verification/m21/m21_perturbation_state_gate_config.json`.

## ACTIVE SCIENTIFIC GATE

Protocol:
`protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md`.

Workflow run:
`34895647832`, head `cfd02c67ee8d9306e65a7c8c80004473e23aab50`.

Six mandatory numerical lanes run independently in parallel:
`NDF_T1E5,NDF_T1E6,NDF_T1E7,RK_T1E5,RK_T1E6,RK_T1E7`.
Each executes immutable `ref/f2/f3/f4` at all five frozen k anchors.

Primary window: `500 <= z <= 2500` via scale factor alignment.
Common-state and ncdm-only families are frozen from exact source authority.
J localization threshold remains `3`; fixed denominator reporting floor is `1e-12`, prospectively added before any branch execution to suppress 12-digit output-rounding blowups.

Do not inspect or act on partial lane values. Wait for the aggregate.

## OUTCOME LOGIC

- full branch map + no control localization -> `M21_PERTURBATION_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE`;
- >=2 branch-change edges -> `M21_PERTURBATION_STATE_BRANCH_SIGNATURE_PARTIAL`;
- <2 branch-change edges -> `M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES`;
- integrity/schema/runtime failure -> BLOCKED.

If NOT_LOCALIZED, native perturbation-state mining is closed and the next layer is direct CMB source/transfer/harmonic interpolation, informed independently by the l=400 sparse-grid phase signature.

## CLAIM CEILING

K1/K3/K4 remain unpromoted. No current result is a physical mixed-dark-matter verdict, CLASS defect, production precision rule, or global convergence proof.
