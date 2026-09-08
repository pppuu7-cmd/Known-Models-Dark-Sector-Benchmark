# M02 — Interacting dark sector (IDE) local tangent-cone audit

Date: 2026-09-08  
Wave: `wave_01_baseline_atlas`  
KMDSB protocol: `DSIR_BENCHMARK_PROTOCOL_v0.1`  
DSIR authority: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Tested scope

Frozen DSIR C2 interacting-dark-sector implementation and its local geometry around the LambdaCDM intersection.

Pinned DSIR implementation lineage reported in the authority snapshot:
`kaeonikc/class_iv@ac627d54...`

The essential physical-domain fact is not optional bookkeeping: the local parameter space is a **tangent cone**, not an unconstrained Euclidean neighborhood.

Frozen C2 facts:

- zero/reference limit passes;
- `alpha > 0` violates the full-history `rho_iv >= 0` condition in the frozen setup;
- the valid alpha deformation is therefore one-sided (left-sided at the reference point);
- beta has a two-sided tangent;
- frozen low-k structure angle between alpha and beta responses: `58.9338 deg`;
- background-H angle: `10.8306 deg`.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | C2 implementation lineage and local parameterization are frozen in DSIR. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | Zero/reference limit passes in the frozen C2 implementation. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Internal dark-sector interaction is audited under the DSIR total-conservation contract; common perturbation response uses the frozen DSIR bookkeeping. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | Valid local domain is a tangent cone. The forbidden `alpha>0` branch is excluded rather than averaged into a symmetric derivative. |
| B4 Response coverage/masks | PASS_WITH_SCOPE | Background and frozen low-k structure responses exist for the valid local directions. Unavailable channels remain masked. |
| B5 Reference identifiability | PARTIAL | Nonzero valid local directions exist, but the quoted alpha/beta geometry is raw theory-space information; observation-space covariance whitening is still required for hard identifiability. |
| B6 Nearest-comparator discrimination | PARTIAL | Alpha and beta are strongly separated in frozen low-k structure response (`58.9338 deg`) but much closer in background-H (`10.8306 deg`). This demonstrates channel dependence, not yet survey-level discrimination. |
| B7 Quotient-surviving novelty | OPEN | Interaction-induced response is not by itself a new residual law after quotienting. |
| B8 Prospective withheld prediction | OPEN | No M02-specific KMDSB prospective discriminator has yet been frozen and tested. |
| B9 Synthesis/design prior | PASS | Tangent-cone geometry and positivity history yield direct methodology constraints. |

## Overall verdict

`DSIR_COMPATIBLE`

The frozen physically admissible C2 domain passes the compatibility portion of the DSIR funnel. **The excluded positive-alpha branch is a physical-domain failure of that branch, not a falsification of the whole IDE family.**

## Wave-1 hypothesis contribution

### W01-H1 — SUPPORTED HARD

M02 already establishes the methodological necessity of constrained local geometry. A symmetric alpha finite difference through the reference point would sample an inadmissible branch and therefore corrupt both Jacobians and rank/discriminator calculations.

### W01-H3 — SUPPORTED

Background-only geometry compresses the alpha/beta distinction relative to structure response (`10.8306 deg` vs `58.9338 deg`). Thus channel choice materially changes apparent degeneracy.

## Design-prior delta

DP-0201 — **Physical parameter geometry must precede linearization.** Derivatives/Jacobians are defined on the admissible tangent cone, not an assumed Euclidean parameter box.

DP-0202 — **History constraints matter.** A point that looks locally algebraically allowed may fail a full-history positivity requirement.

DP-0203 — **Interaction conservation is mandatory.** Internal exchange terms may redistribute components but must satisfy the frozen total-conservation contract.

DP-0204 — **Background-only matching is weak evidence.** Future candidates should be tested in structure/metric channels before claiming degeneracy or equivalence.

## Next M02 task

Observation-space B5/B6: project the admissible alpha/beta rays through a documented survey response/covariance and determine which combination remains identifiable after whitening.
