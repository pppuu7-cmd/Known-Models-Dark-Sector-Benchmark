# M08 — CPL time-varying smooth dark energy audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **PREREGISTERED / IMPLEMENTATION CONTROL OPEN**  
W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`  
Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Scientific role

M08 is not introduced merely as another dark-energy model. It is the stronger phenomenological nearest comparator motivated by M07.

M07 canonical quintessence is strongly near-aligned with constant-w C1 in low-k matter response, while a shared C1 amplitude leaves a larger background/time residual. The M08 question is therefore:

> Can a two-dimensional time-varying smooth-DE manifold absorb the M07 P/H cross-channel separator that constant-w C1 cannot?

This question is frozen before M08 response vectors are inspected.

## Model branch

Pinned CLASS fluid sector:
- `fluid_equation_of_state = CLP`;
- `w0_fld`, `wa_fld` are the physical equation-of-state parameters;
- `cs2_fld = 1` is fixed for the first smooth-DE comparator branch;
- `use_ppf = yes` is frozen for perturbation handling, so crossing or approaching `w=-1` is not silently converted into a different benchmark branch;
- LambdaCDM reference: `(w0_fld,wa_fld)=(-1,0)`.

CPL convention:

`w(a)=w0+wa(1-a)`.

Local coordinates around LambdaCDM will be written as

`epsilon0 = 1+w0`,

`epsilon_a = wa`.

The two response directions are not assumed independent until the numerical local basis is rank-tested.

## Initial domain and controls

The first implementation/control grid is symmetric and diagnostic only:
- `epsilon0 = +/-1e-3` at `wa=0`;
- `wa = +/-1e-3` at `w0=-1`;
- exact LambdaCDM control `(epsilon0,wa)=(0,0)`.

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

The first M08-to-M07 comparison is **unwhitened theory-response geometry**. Observation-space promotion requires a pinned operator/covariance afterward.

## B0-B9 initial ledger

| Gate | State | Requirement |
|---|---|---|
| B0 identity/provenance | `PASS_WITH_SCOPE` | pinned CLASS CLP/PPF branch and exact parameter semantics |
| B1 reference embedding | `PARTIAL` | analytic LambdaCDM intersection identified; numerical reference regression pending |
| B2 conservation/gauge/frame | `PARTIAL` | CLASS fluid+PPF implementation pinned; paired-response bookkeeping audit still required for promoted perturbation claims |
| B3 physical/numerical control | `OPEN` | local +/- probes, precision stability and finite outputs pending |
| B4 response/masks | `OPEN` | P/H local basis not yet produced |
| B5 observational identifiability | `OPEN` | only after controlled local basis |
| B6 nearest comparator | `OPEN` | primary target is M07 q direction with one shared 2D CPL fit |
| B7 quotient-surviving novelty | `OPEN` | depends on residual after CPL profiling |
| B8 prospective holdout | `OPEN` | no relation frozen yet |
| B9 synthesis | `PARTIAL` | scientific role and adversarial question preregistered |

## Anti-overclaim

- M08 is a phenomenological comparator, not a canonical scalar-field model.
- PPF numerical regularity across `w=-1` does not make every CPL point microphysically realizable.
- A successful 2D fit would not prove CPL is the true dark-energy model.
- A failed 2D fit would not prove M07 is the true model.
- No theory-space fit is observational discrimination until covariance/operator projection is performed.
