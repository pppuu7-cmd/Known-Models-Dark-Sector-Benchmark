# W04 M21 perturbation-state branch-signature audit v0.1

Frozen: 2026-09-14 after terminal `M21_CMB_BRANCH_NOT_LOCALIZED_IN_EXPOSED_THERMO_STATE_COLUMNS`, terminal `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE`, and while the non-scientific perturbation-output capability recon is still non-terminal. No f2/f3/f4 perturbation-state branch comparison has been generated at freeze time.

Provider must remain exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Scientific question

Does the already-observed f_w=0.003 CMB numerical branch map exist in native scalar perturbation states **before** transfer-l sparse interpolation/harmonic integration, or is it absent at this upstream layer?

This is a numerical localization audit. It is not a physical mixed-dark-matter test and cannot promote K1/K3/K4.

## Mandatory capability dependency

Execution is forbidden unless `protocol/W04_M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_v0.1.md` has a terminal result classified exactly
`M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_PASS_WITH_SCOPE`.

The successor config must copy, without alteration:

- capability run/artifact/digest;
- `D_star_Mpc`;
- `l_anchors = [100,400,800,1200,2000]`;
- the five `k_anchors_unrounded_Mpc_inv = l/D_star` values;
- the corresponding 12-significant-digit serialization values.

No k anchor may be added, removed, or shifted after branch results are available.

## Frozen physical cases

Generate cases from repository-owned `verification/m21/mixed_cold_warm_k1_reference.py` and execute only:

- `ref`: exact CDM, f_w=0;
- `f2`: f_w=0.01;
- `f3`: f_w=0.003;
- `f4`: f_w=0.001.

All original physical lines, output requests, gauge, cosmology, ncdm mass/temperature and l_max remain unchanged. Add only one `k_output_values` line containing the five capability-authorized serialized k anchors.

## Frozen numerical lanes

Use the exact common M21 baseline `cl_permille.pre + verification/m21/m21_ncdm_tight.pre + evolver=0` and the already-authoritative enum-serialization recovery semantics:

- `NDF_T1E5`: `thermo_evolver=1`, `tol_thermo_integration=1e-5` — CMB REMOVES;
- `NDF_T1E6`: `thermo_evolver=1`, `tol_thermo_integration=1e-6` — CMB INSUFFICIENT;
- `NDF_T1E7`: `thermo_evolver=1`, `tol_thermo_integration=1e-7` — CMB REMOVES;
- `RK_T1E5`: `thermo_evolver=0`, `tol_thermo_integration=1e-5` — CMB REMOVES;
- `RK_T1E6`: `thermo_evolver=0`, `tol_thermo_integration=1e-6` — CMB INSUFFICIENT;
- `RK_T1E7`: `thermo_evolver=0`, `tol_thermo_integration=1e-7` — CMB INSUFFICIENT.

Do not change transfer-l sampling in this gate.

All six lanes are independent and should execute in parallel. Each lane runs ref/f2/f3/f4 sequentially under hard per-case timeout and uploads artifacts even on failure.

## Frozen branch map

Branch-change edges:

1. `NDF_T1E5__NDF_T1E6`
2. `NDF_T1E6__NDF_T1E7`
3. `RK_T1E5__RK_T1E6`
4. `NDF_T1E7__RK_T1E7`

Same-branch controls:

1. `RK_T1E6__RK_T1E7`
2. `NDF_T1E5__RK_T1E5`
3. `NDF_T1E6__RK_T1E6`

This map is inherited from terminal `M21_THERMO_EVOLVER_DEPENDENCE_MIXED` and is not outcome-dependent.

## Frozen native scalar state families

Coordinates `tau [Mpc]` and `a` are not scientific state columns.

### Common-state family

Exact source-authorized titles present in ref and warm cases:

- `delta_g`, `theta_g`, `shear_g`;
- `pol0_g`, `pol1_g`, `pol2_g`;
- `delta_b`, `theta_b`;
- `psi`, `phi`;
- `delta_ur`, `theta_ur`, `shear_ur`;
- `delta_cdm`, `theta_cdm`.

If the capability schema or executed case schema lacks an applicable title above, or introduces an unexpected title collision, execution is BLOCKED rather than silently changing the family.

### ncdm-only family

Exact source-authorized titles present only in warm cases:

- `delta_ncdm[0]`
- `theta_ncdm[0]`
- `shear_ncdm[0]`
- `cs2_ncdm[0]`

The ncdm-only family is compared across f2/f3/f4 only; absence from ref is expected and must not be treated as a schema error.

No post-result column selection is allowed.

## Frozen coordinate/window/interpolation

For each k table use scale factor `a` as the alignment coordinate. Sort ascending in `a`, reject duplicate/non-finite coordinate rows, and interpolate the second lane onto the first lane in `log(a)` over strict overlap.

Primary physical window is exactly

`500 <= z <= 2500`, equivalently `1/2501 <= a <= 1/501`.

At least 16 common overlap samples are required for each compared variable/k/case cell. Full-time comparisons may be report-only and cannot change the classification.

## Frozen distance and f3-specificity statistics

For each edge E, case C, k anchor K and variable V define normalized L2 distance

`D(E,C,K,V) = ||x_A - x_B_interp||_2 / max(||x_A||_2, ||x_B_interp||_2, 1e-300)`.

For a common-state cell:

`J_common(E,K,V) = D(E,f3,K,V) / max(D(E,ref,K,V), D(E,f2,K,V), D(E,f4,K,V), 1e-300)`.

For an ncdm-only cell:

`J_ncdm(E,K,V) = D(E,f3,K,V) / max(D(E,f2,K,V), D(E,f4,K,V), 1e-300)`.

A cell is localized when `J >= 3`, reusing the already-preregistered branch-specificity threshold from the thermodynamics-state audits.

For each edge report:

- maximum J and its k/title for each family;
- count of cells with `J>=3` for each family;
- `edge_localized = true` if either family has at least one `J>=3` cell.

No lower threshold or alternate ranking may be substituted after execution.

## Frozen classification

Artifact/provider/profile/case/k/schema/time-overlap failure ->
`M21_PERTURBATION_STATE_BRANCH_SIGNATURE_BLOCKED`.

All four branch-change edges localized and zero same-branch controls localized ->
`M21_PERTURBATION_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE`.

At least two of four branch-change edges localized, but the full pattern above fails ->
`M21_PERTURBATION_STATE_BRANCH_SIGNATURE_PARTIAL`.

Fewer than two branch-change edges localized ->
`M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES`.

## Consequence rule

- MATCH/PARTIAL: next gate may localize the implicated state variable/k/time support or map it into exact CMB source terms; no CLASS-defect claim is authorized.
- NOT_LOCALIZED: native perturbation-state mining is closed under this table/metric. The next localization must move to the **CMB source/transfer/harmonic interpolation layer**, where the independent l=400 sparse-grid phase signature already supplies downstream evidence.
- BLOCKED: fix only the documented infrastructure/schema issue under a new recovery protocol; do not reinterpret as science.

## Interpretation ceiling

No classification from this gate establishes physical M21 failure/success, a production precision prescription, global numerical convergence, a CLASS defect, or K1/K3/K4 promotion.