# W03 M14 LisaGoh/CDE K1 reference/decoupling preregistration v0.1

Date: 2026-09-10
Provider: `LisaGoh/CDE@b85a675af7544a5183e402964550811aa805b698`
Parent provider control: run `34487561326` — `M14_LISAGOH_CDE_PROVIDER_CONTROL_PASS`

## Purpose

Test the interaction-off reference limit of the public source-complete coupled-dark-energy provider without hiding a possible exact-reference numerical singularity behind nonzero seeds.

The pinned source uses a constant scalar potential,

`V = kappa*(70000/c)^2`, `dV=d2V=0`,

and a three-bin coupling `beta(a)` linear in `beta_1,beta_2,beta_3`. Therefore `beta_1=beta_2=beta_3=0` implies `beta(a)=beta'(a)=0` identically.

The author input explicitly states that for the constant potential one may set `phi_ini_scf=0` and `phi_prime_ini_scf=0`. In that exact state the background equations algebraically reduce to a rigid-vacuum scalar plus standard conserved CDM.

However the perturbation source contains terms proportional to `beta'/phi_prime_scf`, and the scalar velocity-source construction contains a denominator `rho_scf+p_scf`. Thus the exact physical reference may expose a provider-specific `0/0` implementation singularity. This possibility is frozen before execution and must not be repaired post hoc.

## Frozen arms

All arms start from the committed `CDE.ini`; only the listed fields and output root/request are changed.

### A — exact-zero background reference (primary algebraic control)

- `beta_1=beta_2=beta_3=0`
- `phi_ini_scf=0`
- `phi_prime_ini_scf=0`
- perturbation output disabled (`output=`) solely to isolate the background reference
- `write background=yes`
- `root=output/k1_exact_bg_`

### B — exact-zero full perturbation reference (strict K1 forward-model control)

- same exact-zero coupling and exact-zero scalar IC as arm A
- retain the committed perturbation/output requests, gauge and precision settings
- `root=output/k1_exact_full_`

### C — committed-tiny-seed uncoupled diagnostic (non-rescue diagnostic)

- `beta_1=beta_2=beta_3=0`
- retain committed `phi_ini_scf=1e-8`, `phi_prime_ini_scf=1e-7`
- retain full perturbation/output requests
- `root=output/k1_tiny_full_`

Arm C is diagnostic only. If B fails while C succeeds, the result is an exact-reference implementation singularity; C may not convert that into a strict K1 pass.

## Frozen arm-A background invariants

Parse the generated background table and require finite values plus:

- `max |beta| <= 1e-15`;
- `max |dbeta/dz| <= 1e-15`;
- `max |phi_prime_scf| <= 1e-14`;
- `max |w_scf+1| <= 1e-12`;
- relative span of `rho_scf <= 1e-12`;
- relative span of `rho_cdm*a^3 <= 1e-8`.

For any positive reference series `x`, the frozen relative-span functional is

`Rspan(x) = (max(x)-min(x)) / max(max(abs(x)), 1e-300)`.

For the CDM conservation diagnostic use `a=1/(1+z)` from the background table and apply the same functional to `x=rho_cdm*a^3`.

The relatively looser CDM conservation tolerance is a numerical ODE/output tolerance, not a physics tolerance.

## Frozen classifications

- `M14_LISAGOH_CDE_K1_PASS_WITH_SCOPE` if A satisfies every invariant and B executes to completion with fresh nonempty background, perturbation, linear P(k), CMB Cl and transfer outputs.
- `M14_LISAGOH_CDE_K1_EXACT_REFERENCE_IMPLEMENTATION_BLOCKED` if A passes but B fails or cannot produce the required full outputs. C is then used only to distinguish an exact-reference singularity from a generic beta=0 failure.
- `M14_LISAGOH_CDE_K1_UNCOUPLED_ROUTE_BLOCKED` if A passes, B fails and C also fails.
- `M14_LISAGOH_CDE_K1_BACKGROUND_REFERENCE_FAIL` if arm A executes but violates any frozen invariant.
- `M14_LISAGOH_CDE_K1_BLOCKED_INFRASTRUCTURE` if arm A itself cannot be executed/parsed for nonphysical infrastructure reasons.

No result from this test physically falsifies the M14 family. A failure is provider/reference-route specific.

## Gate consequences

Strict K1 promotion requires the full exact-zero arm B. A background-only pass is recorded separately but cannot authorize K4/K5. K3 source completeness remains a separate gate even if B executes.

No seed adjustment, source edit, denominator regularization, tolerance relaxation or parameter-grid change is allowed after seeing this test.