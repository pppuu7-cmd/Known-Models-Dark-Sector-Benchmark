# M16 — interacting vacuum / running-vacuum family audit

Updated: 2026-09-10
Wave: W03 Tier-B
Status: `INTERACTING_VACUUM_SUBCASE_REPRESENTED_BY_M02_FULL_RUNNING_VACUUM_OPEN`

## Scope

The executed IDECAMB subcase is

- `w=-1`;
- `Q = beta H rho_de`;
- `Q_mu = Q u_mu,c`;
- base `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`;
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`.

This record does **not** close the broader F16 running/decaying-vacuum `Lambda(H)` family. Genuine laws with explicit `H^2`, `dot H`, higher powers/derivatives, or a response channel not contained in the M02 interaction manifold remain open.

## K0 / source binding

Pinned IDECAMB source identifies `QForm_CF=1` with `Q=beta H rho_de`. The covariant selector documents `CovQForm_CF=1` as `Q_mu=Q u_mu,c`. The CPL fluid branch has the cosmological-constant point `w0=-1,w1=0,beta=0`. K0: `PASS_WITH_SCOPE`.

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

Provenance: run `34474389038`, job `102861550642`, immutable artifact `10150882133`, digest `sha256:f549f3c02de47a4152b89be1a8cbfc4782ffaf8b4671494d45d4216b78520b50`, machine-result commit `9619a5c825f71906c4e872fee70fbd06876357f0`.

## M16 ↔ M02 family-identity audit — terminal for this subcase

M02 is pinned to `kaeonikc/class_iv@ac627d54e9ce196a08878d1ba33999819925d19c`. Its source explicitly defines

`Q = alpha H rho_idm_iv + beta H rho_iv`.

Therefore the M16 executed interaction law is exactly the `alpha=0`, `rho_iv=rho_vac` slice of the M02 background interaction manifold after identifying the coupling coordinate `beta_M16 = beta_M02`.

The covariant/momentum-transfer prescription also matches within tested scope. M16 freezes `Q_mu=Q u_mu,c`. M02's interacting-vacuum perturbation branch is implemented in the synchronous frame comoving with the interacting pressureless component: its interacting-DM velocity is set to zero there and its density equation contains the same background exchange `alpha H rho_m + beta H rho_v`. Thus no extra degree of freedom, interaction law, scale/time law, or independently specified momentum-transfer channel is introduced by the executed M16 branch relative to M02.

Classification for the **executed interacting-vacuum subcase**:

`REPRESENTED_BY:M02_WITH_SCOPE`

This is a family-identity/coverage result, not a statement that interacting vacuum is physically correct or false. It also does not upgrade M02's still-open observation-space/holdout gates.

## Gate ledger

| K gate | State |
|---|---|
| K0 | PASS_WITH_SCOPE |
| K1 | PASS_WITH_SCOPE |
| K2 | REPRESENTED_BY:M02_WITH_SCOPE |
| K3 | REPRESENTED_BY:M02_WITH_SCOPE |
| K4 | REPRESENTED_BY:M02_WITH_SCOPE |
| K5 | REPRESENTED_BY:M02_WITH_SCOPE |
| K6 | PASS_REPRESENTED_BY:M02_WITH_SCOPE |
| K7 | INHERITS_M02_OPEN |
| K8 | NO_SEPARATE_NOVELTY_SUBCASE |
| K9 | INHERITS_M02_OPEN |

No separate beta-grid is authorized for this M16 subcase: it would duplicate the already admitted M02 response manifold. The broader F16 family remains nonterminal because genuine running-vacuum `Lambda(H)` response laws are not represented by this result.

## Exact next allowed F16 gate

Search and pin an independent public running-vacuum implementation whose defining vacuum law is not merely `Q=alpha H rho_m + beta H rho_v` with the same `Q_mu || u_c` closure. Before execution, freeze the exact `Lambda(H)`/`rho_v(H,dot H,...)` law, conservation exchange, perturbation prescription, reference limit, observable outputs and thresholds. If the candidate reduces algebraically to M02, record `REPRESENTED_BY` rather than launching a duplicate response grid.
