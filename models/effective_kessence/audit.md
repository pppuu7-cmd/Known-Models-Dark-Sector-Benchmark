# M11 — effective k-essence / sound-speed response representative

Status: ACTIVE
Wave: W03 dark-energy mechanism census
Family: F11
Preregistration: `protocol/W03_M11_EFFECTIVE_KESSENCE_PREREGISTRATION_V0_1.md`

## Scope

This benchmark does not claim that a CLASS fluid with free `cs2_fld` is the full covariant space of k-essence Lagrangians `P(phi,X)`. It tests the cosmological response feature most directly associated with a broad noncanonical scalar-DE class: a rest-frame sound speed different from the canonical value `c_s^2=1`.

A covariant M11b implementation is required if the effective representative either (a) produces a distinct response that needs microphysical/stability validation, or (b) fails to span a known covariant kinetic model in an orthogonal channel.

## Frozen physical geometry

At exact `w=-1`, the DE perturbation sector vanishes and sound speed is unidentifiable. Therefore M11 uses a stratified geometry:

- reference/decoupling regression: pure LambdaCDM vs fluid `w=-1, cs2=1`;
- sound-speed geometry on fixed anchor `w=-0.95`;
- one-sided subluminal coordinate `q_s=1-cs2>=0`;
- tangent estimates at q_s=.05 and .10;
- smooth-w comparator derivative at the same anchor with `delta w=1e-3`.

This prevents a false zero-rank conclusion from differentiating a parameter exactly on a stratum where it has no physical effect.

## K-gate status before first run

- K0 `PASS_WITH_SCOPE` — solver/branch/coordinates preregistered.
- K1 `OPEN` — pure Lambda vs fluid-zero regression pending machine record.
- K2 `PASS_WITH_SCOPE` — subluminal one-sided q_s and rank-stratified anchor explicitly frozen.
- K3 `PARTIAL` — standard CLASS fluid conservation/PPF branch used; no independent gauge regression yet for derived residual.
- K4 `OPEN` — q_s step convergence is a hard gate.
- K5 `OPEN` — multi-response/rank calculation pending.
- K6 `OPEN` — first comparator is smooth-w at same anchor; full CPL attack follows if distinct.
- K7 `OPEN` — no observational promotion from theory response.
- K8 `OPEN`.
- K9 `OPEN`.

## First computation

Workflow: `.github/workflows/w03-m11-effective-kessence.yml`.
Run #1 `34426134138` completed all preregistered workflow stages successfully, including enforcement. A second persistence run was triggered after hardening the workflow so the canonical JSON is committed to the repository rather than existing only in the Actions artifact.

Do not change the frozen anchor, steps or thresholds after this output.
