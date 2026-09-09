# M08 — CPL time-varying smooth dark energy audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **ACTIVE / IMPLEMENTATION CONTROL RERUNNING**  
Initial W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`  
Observation-space methodology overlay from corrected rerun onward: `864952e1520d82473a9e976edfeb69f9899d174d` (see `recovery/AUTHORITY_DELTAS.md` AD-002)  
Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Scientific role

M08 is the stronger phenomenological nearest comparator motivated by M07.

M07 canonical quintessence is strongly near-aligned with constant-w C1 in low-k matter response, while a shared C1 amplitude leaves a larger background/time residual. The M08 question is therefore:

> Can a two-dimensional time-varying smooth-DE manifold absorb the M07 P/H cross-channel separator that constant-w C1 cannot?

This question was frozen before M08 response vectors were inspected.

## Model branch

Pinned CLASS fluid sector:
- `fluid_equation_of_state = CLP`;
- `w0_fld`, `wa_fld` are the physical equation-of-state parameters;
- `cs2_fld = 1` is fixed for the first smooth-DE comparator branch;
- `use_ppf = yes` is frozen for perturbation handling;
- LambdaCDM reference: `(w0_fld,wa_fld)=(-1,0)`.

CPL convention:

`w(a)=w0+wa(1-a)`.

Local coordinates:

`epsilon0 = 1+w0`,  
`epsilon_a = wa`.

The two response directions are not assumed independent until the numerical local basis is rank-tested.

## Closure convention

The intended M08 branch is pure CPL dark energy with no separate cosmological constant:

- `Omega_Lambda = 0` is explicit;
- `Omega_fld` is **not** simultaneously specified; pinned CLASS infers the fluid density from the closure budget.

This convention became explicit after the first implementation run exposed the solver input rule below.

## Initial implementation failure — preserved

Actions run `34391852165`, head `79047859b242a0fbcad75cdae5ad3b7c95f36b2f`, artifact digest `sha256:0c8cf5c2de8f3d4cc9f62d9a8574a60656db38caee297b01b6fdf1674517045e`.

All five cases (`ref`, `e0p`, `e0m`, `wap`, `wam`) exited with code 1 before cosmological evolution. CLASS rejected the configuration because both

`Omega_Lambda = 0`

and

`Omega_fld = 0.682686955086854`

were specified. The pinned solver requires one of `Omega_Lambda` or `Omega_fld` to remain unspecified for closure (outside the special scalar-field case described by the error path).

Classification: **implementation/configuration failure only**. It is not a physical failure of CPL, PPF, phantom crossing, or the two-dimensional local manifold.

Correction commit: `a3bb13aab2f181fed31882d31f819c9d0b0a7a36` removes explicit `Omega_fld` and retains `Omega_Lambda=0`; the corrected run is Actions `34394929596`.

The failed first run remains immutable evidence and is not overwritten by the rerun.

## Initial domain and controls

The first scientific/control grid remains unchanged by the implementation fix:
- `epsilon0 = +/-1e-3` at `wa=0`;
- `wa = +/-1e-3` at `w0=-1`;
- exact LambdaCDM-fluid control `(epsilon0,wa)=(0,0)`.

Because `use_ppf=yes` is frozen, these local probes may cross the phantom boundary numerically without being reinterpreted as canonical scalar-field physics. M08 is a phenomenological smooth-fluid comparator, not a claim that every point has a canonical quintessence realization.

No M08 finite-difference output is B8 evidence.

## Preregistered M08 hypotheses

### H-M08-1 — 2D dynamic-DE absorption test

The 2D CPL local span may absorb substantially more of the M07 combined low-k matter + background-H direction than constant-w C1.

The fit must use **one shared parameter vector** `(epsilon0,epsilon_a)` across all included blocks. Independent refits by block are forbidden.

### H-M08-2 — residual novelty criterion

If the best common CPL fit leaves a substantial M07 residual in a controlled block, that residual strengthens the case for a genuinely microphysical/time-response separator.

If CPL absorbs the M07 direction, the correct lesson is the opposite: the M07/C1 separator was insufficiently adversarial, and future original models need observables beyond a flexible smooth `w(a)` history.

### H-M08-3 — rank before interpretation

Parameter count 2 does not imply identified response rank 2. The local CPL P/H Jacobian must be SVD/rank tested before model-comparison claims.

## Frozen common blocks for first comparison

Use the same W03 response conventions where valid:
- background `ln H(z)` on the seven frozen z nodes;
- low-k matter `ln P(k,z)` on the frozen 7x5 grid;
- matched LambdaCDM baseline;
- same solver family/precision for all M08 local directions.

The first M08-to-M07 comparison is unwhitened theory-response geometry.

## Observation-space rule after AD-002

The newer DSIR Article-2 G5 contract is adopted prospectively for any M08 observational/cross-family promotion:

- a covariance is not sufficient by itself;
- every compared model must be mapped through one frozen observation/operator bridge into exactly the same coordinate vector on which that covariance acts;
- coordinate order, units, masks and provenance must be bound before the output is read;
- no zero-imputation, response/covariance relabeling or post-hoc rank cutoff is permitted.

Therefore a later M08/M07 observation-space comparison may not mix a CLASS-derived vector for one family with an unrelated analytic proxy for another and call the result cross-family G5 closure. Existing model-specific B5 controls remain scoped evidence only.

## B0-B9 current ledger

| Gate | State | Requirement |
|---|---|---|
| B0 identity/provenance | `PASS_WITH_SCOPE` | pinned CLASS CLP/PPF branch and exact parameter semantics |
| B1 reference embedding | `PARTIAL` | analytic LambdaCDM intersection and corrected closure convention identified; numerical reference regression rerunning |
| B2 conservation/gauge/frame | `PARTIAL` | CLASS fluid+PPF implementation pinned; promoted perturbation claims still require controlled bookkeeping |
| B3 physical/numerical control | `OPEN` | first run configuration-blocked; corrected local probes running |
| B4 response/masks | `OPEN` | P/H local basis not yet admitted |
| B5 observational identifiability | `OPEN` | must obey AD-002 exact observation-bridge rule |
| B6 nearest comparator | `OPEN` | primary target is M07 q direction with one shared 2D CPL fit |
| B7 quotient-surviving novelty | `OPEN` | depends on residual after CPL profiling and later observation-space survival |
| B8 prospective holdout | `OPEN` | no relation frozen yet |
| B9 synthesis | `PARTIAL` | scientific role, adversarial question and implementation lesson recorded |

## Anti-overclaim

- M08 is a phenomenological comparator, not a canonical scalar-field model.
- PPF numerical regularity across `w=-1` does not make every CPL point microphysically realizable.
- The first run is an input-closure failure, not a theory failure.
- A successful 2D fit would not prove CPL is the true dark-energy model.
- A failed 2D fit would not prove M07 is the true model.
- No theory-space fit is observational discrimination until a common frozen observation operator/covariance projection is performed.
