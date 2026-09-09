# M07 — canonical scalar-field / quintessence audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **ACTIVE / IMPLEMENTATION CALIBRATION**  
W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`  
Pinned scalar solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Model identity

M07 is a minimally coupled canonical scalar field with standard kinetic term and a controlled pure-exponential potential branch of the pinned CLASS `scf` implementation.

CLASS potential family:

`V(phi) = ((phi-B)^alpha + A) exp(-lambda phi)`.

Initial M07 branch:

`alpha = 0`, `B = 0`, hence

`V(phi) = (1+A) exp(-lambda phi)`.

Canonical solver stress:

`rho_phi = [phi_prime^2/(2a^2) + V]/3`

`p_phi = [phi_prime^2/(2a^2) - V]/3`.

The perturbation solver exposes scalar-field density and velocity response sources (`delta_scf`, `theta_scf`) in addition to the standard matter and metric outputs.

## Parameter/provenance decision

The default CLASS scalar-field shooting convention can tune parameter index 0 (`lambda`) when `Omega_scf` is specified. That convention is unsuitable for a benchmark in which `lambda` is itself the physical slope parameter.

M07 therefore freezes:

- `attractor_ic_scf = no`;
- explicit initial `phi` and `phi_prime`;
- `scf_tuning_index = 2`;
- potential normalization `A` is the shooting nuisance used to hit the requested `Omega_scf`;
- `lambda` remains fixed by the benchmark point.

This separation is required before any local derivative/Jacobian is defined.

## Reference-intersection logic

At `lambda = 0` and `phi_prime = 0`, the pure-exponential branch becomes a constant potential. Then the canonical scalar stress obeys

`p_phi = -rho_phi`.

A matched split-reference control can therefore replace a fixed fraction of Lambda by the constant scalar while leaving the total dark-energy response at the LambdaCDM origin, if the solver/bookkeeping implementation is correct.

The first hard numerical task is to test this statement, not to assume it.

## B0-B9 gate ledger

| Gate | State | Evidence / requirement |
|---|---|---|
| B0 identity/provenance | `PASS_WITH_SCOPE` | canonical CLASS `scf` branch, exact upstream commit, potential subset and shooting semantics pinned |
| B1 DSIR embedding/reference limit | `PARTIAL` | analytic constant-field intersection identified; numerical matched LambdaCDM reference regression pending |
| B2 conservation/gauge/frame bookkeeping | `PARTIAL` | minimally coupled canonical solver implementation and perturbation channels exist; matched response/gauge controls not yet run |
| B3 physical-domain/numerical control | `OPEN` | need shooting convergence, positive finite scalar density, `A>-1` where required for positive pure-exponential normalization, precision/reference checks |
| B4 response coverage/masks | `OPEN` | standard low-k matter/growth planned; scalar/metric outputs must be mapped and unavailable cells explicitly masked |
| B5 reference identifiability | `OPEN` | no observational promotion before B0-B4 control |
| B6 nearest comparator | `OPEN` | attack M01 smooth-w and M05 designer f(R) after common response is produced |
| B7 quotient-surviving novelty | `OPEN` | premature |
| B8 prospective withheld prediction | `OPEN` | no finite-lambda relation may be promoted retrospectively from the implementation probe |
| B9 synthesis/design priors | `PARTIAL` | provenance/shooting separation already informs methodology; final model verdict pending |

## Initial implementation probe

The first run is explicitly an infrastructure/reference probe, not a prospective model-discovery test.

Planned matched cases:

1. `REF_LCDM`: `Omega_scf=0`.
2. `SCF_SPLIT_L0`: fixed positive scalar fraction, `lambda=0`, explicit zero initial velocity; Lambda fills remaining closure.
3. finite-`lambda` split cases used only to confirm solver behavior and estimate a sensible later production grid.

The probe must record:
- final achieved `Omega_scf`;
- shooting normalization `A`;
- finite/positive background quantities;
- `w_phi(z)` and field evolution;
- matched `H(z)` and low-k `P(k,z)` residuals against the pure LambdaCDM reference;
- exact CLASS config and upstream SHA.

No finite-lambda result from this probe is allowed to become B8 evidence.

## Current expected verdict

`INCONCLUSIVE` until B1-B3 are numerically calibrated.

## Design-prior pressure already visible

- physical theory parameters and closure/shooting nuisance parameters must be explicitly separated;
- exact analytic reference intersections require numerical regression before being used as tangent origins;
- microphysical DE must expose perturbation/time response rather than being reduced to a fitted background `w(z)`.
