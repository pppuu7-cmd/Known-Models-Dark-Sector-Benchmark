# M16 — interacting vacuum / running-vacuum subfamily audit

Updated: 2026-09-10
Wave: W03 Tier-B
Status: `INTERACTING_VACUUM_K1_PASS_WITH_SCOPE_FAMILY_IDENTITY_AUDIT_NEXT`

## Tested scope

This record covers only the pinned IDECAMB interacting-vacuum subfamily

- `w=-1`;
- `Q = beta H rho_de`;
- `Q_mu = Q u_mu,c`;
- base `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`;
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`.

It does **not** yet represent all running-vacuum `Lambda(H)` constructions, derivative-vacuum laws, or other covariant transfer directions.

## K0 / source binding

The pinned source documents coupled-fluid `QForm_CF=1` as `Q=beta H rho_de`, and its CPL branch has an explicit cosmological-constant condition at `w0=-1,w1=0,beta=0`. K0: `PASS_WITH_SCOPE`.

## K1 frozen reference gate

Preregistration: `protocol/W03_M16_IDECAMB_INTERACTING_VACUUM_K0K1_PREREGISTRATION_v0.1.md`.

Frozen comparison:
- interacting branch: `Class_IDE=1`, `w0=-1`, `w1=0`, `beta_cf=0`, `QForm_CF=1`, `CovQForm_CF=1`;
- comparator: same overlay, noninteracting branch `Class_IDE=0`, `w0=-1`, `w1=0`;
- symmetric-relative threshold: `2e-8`;
- undefined/nonfinite entries masked, never zero-imputed.

Machine result:
- both exits: 0;
- `.quantity`: max symmetric relative difference `0.0`, 16000 common finite entries / 2000 rows;
- `.theory_cl`: max symmetric relative difference `0.0`, 14994 common finite entries / 2499 rows.

K1: `PASS_WITH_SCOPE`.

## Provenance

- run `34474389038`
- job `102861550642`
- immutable artifact `10150882133`
- artifact digest `sha256:f549f3c02de47a4152b89be1a8cbfc4782ffaf8b4671494d45d4216b78520b50`
- machine-result commit `9619a5c825f71906c4e872fee70fbd06876357f0`

## Gate ledger

| K gate | State |
|---|---|
| K0 | PASS_WITH_SCOPE |
| K1 | PASS_WITH_SCOPE |
| K2 | NOT_TESTED |
| K3 | PARTIAL_SOURCE_BOUND |
| K4 | NOT_TESTED |
| K5 | NOT_TESTED |
| K6 | OPEN_FAMILY_IDENTITY_M02_OVERLAP_AUDIT |
| K7 | NOT_TESTED |
| K8 | NOT_TESTED |
| K9 | NOT_TESTED |

No physical falsification follows from this record.

## Exact next allowed gate

Before opening a beta response grid, compare the F16 equations/parameter manifold and covariant transfer prescription against the already-tested F02/M02 IDE family. Determine prospectively whether this interacting-vacuum branch is response-distinct, a constrained M02 submanifold (`REPRESENTED_BY:M02`), or only partially overlapping. Only if a response-distinct direction remains may a separate F16 K2-K6 production program be opened. Full running-vacuum `Lambda(H)` coverage remains separately required.
