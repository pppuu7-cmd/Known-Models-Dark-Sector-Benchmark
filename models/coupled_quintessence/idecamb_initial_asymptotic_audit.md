# M14 IDECAMB coupled-quintessence initial/asymptotic audit

Updated: 2026-09-10
Status: `BLOCKED_IMPLEMENTATION_ASYMPTOTIC_INITIALIZATION_PROVENANCE`
Physical falsification: **NO**
K5/K6 promotion: **NO**

## Pinned provider

- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- base `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- CQ branch: `Class_IDE=2`, `UForm_CQ=1`, `QForm_CQ=1`.

## Why this audit was reached

M14 passed a scoped beta=0 reference/invariant gate and has a source-complete perturbation coupling path, but all prospectively frozen local beta grids failed the directional part of K4. The final source-scaled grid beta={0,5e-8,1e-7} had a small norm mismatch but an ~8 degree tangent-angle mismatch. A high-precision serialization audit left the angle essentially unchanged. A preregistered diagnostic replacing the provider's nonstandard inverse-Jacobian update by a standard good-Broyden rank-one update also left the angle unchanged while the shooting coordinates and residuals varied smoothly.

Broyden-control provenance:
- run `34466179406`
- job `102835190766`
- artifact `10147638232`
- result `waves/wave_03_expanded_dark_energy/M14_IDECAMB_BROYDEN_CONTROL_RESULT.json`.

## Source-bound initial prescription

In `CoupledQuintModels` the provider fixes

`amin = 1.d-12`.

For the supported power-law potential the routine `InitialCondition_CQ` initializes the scalar with

`const = alpha*(2+alpha)^2*grhov*gU0 / [4*adotrad^2*(6+alpha)]`,

`phi_i = const^(1/(2+alpha)) * a^(4/(2+alpha))`,

and a corresponding tracker-like `phi'_i` expression.

The initial-condition formula contains the potential parameter alpha and the solved normalization `gU0`, but **no explicit beta-dependent coupled-asymptotic correction**.

By contrast, from the first integration step the CQ equations use the exponential coupling

`rho_c(a,phi) = rho_c0/a * exp[-beta*(phi-gphi0)]`,

`gQ = beta * rho_c(a,phi) * phi'`,

and the scalar equation contains the interaction contribution `gQ/phi'`.

Thus beta changes the evolved equations immediately while the provider initializes the supported power-law branch with a beta-independent tracker form apart from indirect shooting changes in gU0.

## Author-supported control audit

No separately documented coupled early-time asymptotic solution, beta-dependent initialization formula, alternate initial-condition branch, or user-selectable integration-start scale was found in the pinned CQ implementation. `amin` is a private hard-coded source parameter.

Changing `amin`, inventing a beta-dependent tracker correction, or replacing the initial state by a KMDSB-derived prescription would therefore be a new implementation rather than an author-supported provider control.

Under the preregistered decision rule, KMDSB must not perform such post-result tuning merely to obtain K4 convergence.

## Classification

For this IDECAMB provider route:

- K0: `PASS_WITH_SCOPE`;
- K1: `PASS_WITH_SCOPE` for the interaction-off invariants already tested;
- K2: `PASS_WITH_SCOPE`, one-sided beta>=0 on the author prior;
- K3: `SOURCE_COMPLETE_WITH_SCOPE` for active CQ background+perturbation coupling equations;
- K4: `BLOCKED_IMPLEMENTATION_ASYMPTOTIC_INITIALIZATION_PROVENANCE`;
- K5-K9: not promoted from this route.

The raw parent and recovery K4 failures remain immutable measurements. They are not reclassified as physical model failure; rather, their scientific interpretation is provider-limited because the beta>0 local response has not been shown to converge under an independently validated coupled-asymptotic initial prescription.

## Durable lesson

A smooth beta->0 source equation and smooth shooting coordinates are insufficient for derivative-level family validation if the finite-beta branch is initialized by an asymptotic prescription derived without the interaction and the provider supplies no validated coupled correction/control. In that situation, do not indefinitely reduce the parameter step or tune the start epoch. Treat K4 as implementation/provenance blocked and move to an independent provider.

## Next allowed M14 action

Search for a second coupled-quintessence implementation with:

1. explicit interaction-off limit;
2. active perturbation closure;
3. documented coupled early-time/initial conditions or a validated autonomous-system initialization;
4. reproducible theory observables.

Do not continue beta step shrinking or modify IDECAMB `amin`/ICs post hoc for scientific promotion.
