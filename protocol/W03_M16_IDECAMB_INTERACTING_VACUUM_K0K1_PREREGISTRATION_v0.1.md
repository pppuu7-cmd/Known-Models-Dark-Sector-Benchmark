# W03 M16 IDECAMB interacting-vacuum K0/K1 preregistration v0.1

Frozen: 2026-09-10
Target: F16/M16 running/interacting vacuum
Scope: **interacting-vacuum subfamily only**, not the full running-vacuum Lambda(H) class.
Scientific promotion authorized: K0/K1 only.

## Provider

- base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- compatibility-only build flag already validated in M14: `-fallow-argument-mismatch`.

## Family identity

Use IDECAMB coupled-fluid branch:

- `Class_IDE = 1`
- `WForm_CF = 1` (CPL)
- `w0 = -1`
- `w1 = 0`
- `QForm_CF = 1`: `Q = beta H rho_de`
- `CovQForm_CF = 1`: `Q_mu = Q u_{mu,c}`

At `w=-1` the dark-energy component is vacuum-like; nonzero beta transfers energy between vacuum and CDM. This is a response-distinct interacting-vacuum representative. It does **not** by itself represent every Lambda(H), H^4, derivative-vacuum or alternative covariant-transfer prescription.

Source equations to be preserved exactly:

`Coup_CF = beta * aH * grhov_t` for QForm 1, with coupled background equations and active PPF interacting-fluid perturbation closure from the pinned provider.

## K1 reference map

Reference coordinate: `beta_cf -> 0` with `w0=-1,w1=0` and all ordinary cosmological settings identical.

Comparator: same pinned overlay routed through noninteracting CPL (`Class_IDE = 0`) at `w0=-1,w1=0`.

The source explicitly has a cosmological-constant branch condition when `w0=-1`, `w1=0`, `beta=0`.

## Execution route

Start from provider `test_ide.ini`; comment external likelihood DEFAULT lines while keeping `batch3/common.ini`; set `test_output_root` to unique roots; disable `test_check_compare`. No physics source edit is allowed.

Two cases:

1. `vacuum_beta0`: Class_IDE=1, w0=-1, w1=0, beta_cf=0, QForm=1, CovQForm=1.
2. `lcdm_cmp`: Class_IDE=0, w0=-1, w1=0, otherwise identical.

## Frozen K1 metrics

Compare provider-emitted numeric theory files on common row/column support.

- `.quantity`: maximum symmetric relative difference <= `2e-8`.
- `.theory_cl`: maximum symmetric relative difference <= `2e-8` after excluding rows/entries nonfinite in either case; no zero imputation.
- both cases must exit 0, emit nonempty numeric files and select their intended branches.

If file schemas differ or no exact common numeric support exists: K1 is `BLOCKED_OUTPUT_SCHEMA`, not FAIL.

## Interpretation

PASS establishes a scoped interaction-off LambdaCDM reference for this IDECAMB interacting-vacuum representative. It does not close K2-K9 and does not establish equivalence to general running-vacuum Lambda(H) models.

FAIL means only the frozen numerical K1 reference regression failed. Infrastructure/configuration failures remain BLOCKED and are not physical evidence.
