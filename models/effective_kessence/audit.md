# M11 — effective k-essence / sound-speed response representative

Status: ACTIVE / STAGE A COMPLETE
Wave: W03 dark-energy mechanism census
Family: F11
Preregistration: `protocol/W03_M11_EFFECTIVE_KESSENCE_PREREGISTRATION_V0_1.md`
Canonical machine result: `waves/wave_03_expanded_dark_energy/M11_EFFECTIVE_KESSENCE_RESULT.json`

## Scope

This benchmark does not claim that a CLASS fluid with free `cs2_fld` is the full covariant space of k-essence Lagrangians `P(phi,X)`. It tests the cosmological response feature most directly associated with a broad noncanonical scalar-DE class: a rest-frame sound speed different from the canonical value `c_s^2=1`.

A covariant M11b implementation remains required if this effective response survives the strongest smooth-DE manifold attack and needs microphysical/stability validation, or if a known covariant kinetic model exposes an orthogonal response not represented here.

## Frozen physical geometry

At exact `w=-1`, the DE perturbation sector vanishes and sound speed is unidentifiable. Therefore M11 uses a stratified geometry:

- reference/decoupling regression: pure LambdaCDM vs fluid `w=-1, cs2=1`;
- sound-speed geometry on fixed anchor `w=-0.95`;
- one-sided subluminal coordinate `q_s=1-cs2>=0`;
- tangent estimates at q_s=.05 and .10;
- smooth-w comparator derivative at the same anchor with `delta w=1e-3`.

This prevents a false zero-rank conclusion from differentiating a parameter exactly on a stratum where it has no physical effect.

## Actions chronology

- run #1 `34426134138`: all scientific steps and preregistered gates PASS; result existed in immutable artifact.
- run #2 `34426280522`: scientific gates PASS again; only repository persistence failed because concurrent documentation commits caused a non-fast-forward push. This is an infrastructure bookkeeping episode, not a scientific failure.
- run #3 `34426484303`: all scientific gates PASS and race-safe canonical result persistence PASS.

## Stage-A hard-gate results

### Reference / decoupling regression

Pure LambdaCDM vs fluid `w=-1, cs2=1`:

- `max |ln P_fld0/P_LCDM| = 0`
- `max |ln H_fld0/H_LCDM| = 0`

Frozen K1 thresholds are passed exactly in this solver/configuration scope.

### Sound-speed tangent convergence

For `q_s=1-cs2` evaluated at the fixed `w=-0.95` anchor:

- relative difference between `J_s(q_s=.05)` and `J_s(q_s=.10)` = `0.0391167` = 3.91%
- angle = `0.140712 deg`

Frozen convergence requirements (<=10% and <=3 deg) PASS.

The sound-speed direction is non-null in the low-k matter block.

### Geometry against smooth constant-w at same anchor

Combined 35-node lnP + 7-node lnH:

- angle `J_w` vs `J_s` = `69.758951 deg`
- residual fraction of `J_s` after optimal projection onto `J_w` = `0.9382454`

Thus the sound-speed perturbation direction is not a rescaled smooth-w response in this theory-space block.

However its absolute tangent norm is tiny relative to the smooth-w direction:

- `||J_w|| = 2.02130323`
- `||J_s|| = 0.00149449`
- combined two-column singular values `{2.02130329, 0.00140220}`
- `sigma2/sigma1 = 6.9371e-4`

This is a crucial distinction: **directional novelty is not observational identifiability**. A weak but geometrically orthogonal direction cannot be promoted without an exact observation-space projection and absolute significance.

The sound-speed response has zero H component in this fixed-background effective-fluid construction; its tested information is perturbation/scale structure only.

## Current K-gate state

- K0 `PASS_WITH_SCOPE`
- K1 `PASS_WITH_SCOPE`
- K2 `PASS_WITH_SCOPE`
- K3 `PARTIAL` — CLASS fluid/PPF bookkeeping used, but no independent gauge/representation audit for the derived residual.
- K4 `PASS_WITH_SCOPE` — preregistered q_s convergence passed.
- K5 `PASS_WITH_SCOPE` — independent perturbation response direction measured, but extremely weak singular value.
- K6 `PARTIAL` — smooth-w ray rejected as sufficient comparator; full CPL manifold at the same `w=-0.95` anchor is the preregistered next attack.
- K7 `OPEN`
- K8 `PARTIAL` — theory-space sound-speed residual survives one-ray projection only; no observational novelty claim.
- K9 `OPEN`

## Immediate next hard test

Build the full two-direction CPL comparator **at the same anchor `w0=-0.95, wa=0, cs2=1`**, fit one shared `(delta w0, delta wa)` vector to the M11 sound-speed P+H tangent, and report combined/per-block residuals. The existing M08 tangent at LambdaCDM is not silently reused because tangent geometry can change away from `w=-1`.

If the full CPL manifold absorbs the sound-speed direction, M11 is response-represented by flexible smooth DE in this block. If a substantial residual survives, a covariant M11b kinetic implementation becomes higher priority before claiming k-essence-family novelty.
