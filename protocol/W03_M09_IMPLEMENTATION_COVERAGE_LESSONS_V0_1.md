# W03 M09 implementation-coverage lessons v0.1

Frozen from M09 result on 2026-09-10.

## Evidence
M09 preregistered the native `class_public@e858083...` `fluid_equation_of_state=EDE` branch before execution. The pure Lambda control ran, while every EDE case including `Omega_EDE=0` stopped before background initialization with the upstream message `EDE implementation not finished`.

Source inspection then showed:
- an implemented `Omega_EDE(a)` and `dOmega_EDE/da`;
- implemented `w_EDE(a)`;
- an explicit `d2Omega_EDE/da2 = 0` placeholder in the perturbation derivative path;
- an unimplemented continuity integral terminated by `class_stop`.

## Methodological consequences

### IC-1 — advertised option != executable model
Parser options, enums, comments or partial source formulas do not count as implemented benchmark coverage. At least one reference/control must traverse every solver module needed by the claimed response.

### IC-2 — solver-limited is its own scientific state
`BLOCKED_IMPLEMENTATION` is neither `NEAR_NULL`, `NONIDENTIFIABLE`, nor `FAIL`. It carries information about coverage but no physical verdict.

### IC-3 — no silent completion
Removing an upstream stop, supplying a missing equation or replacing a placeholder creates a new implementation authority. Such a branch requires explicit equations, reference regressions, convergence tests and provenance before it can enter KMDSB.

### IC-4 — prefer independently published implementation for adversarial benchmarking
Where a published implementation already evolves the relevant background and perturbations, benchmarking that implementation is scientifically cleaner than silently repairing an unfinished dormant branch. M10 therefore uses pinned `mwt5345/class_ede` as a separate model/solver authority.

## Future-model impact
A future original dark-sector model must not only be mathematically specified; its observable claims must be backed by an executable validated response provider. Implementability and response-provider provenance are therefore part of the construction funnel, not post-publication engineering details.
