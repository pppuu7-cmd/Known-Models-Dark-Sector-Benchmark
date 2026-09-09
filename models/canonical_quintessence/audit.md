# M07 — canonical scalar-field / quintessence audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **ACTIVE / STRICT PRODUCTION CALIBRATED / LOCAL GEOMETRY AUDITING**  
W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`  
Pinned scalar solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Model identity

M07 is a minimally coupled canonical scalar field with standard kinetic term on the pinned CLASS `scf` pure-exponential subset

`V(phi)=((phi-B)^alpha+A) exp(-lambda phi)`,

with frozen

`alpha=0`, `B=0`, hence `V(phi)=(1+A) exp(-lambda phi)`.

Canonical solver stress:

`rho_phi=[phi_prime^2/(2a^2)+V]/3`

`p_phi=[phi_prime^2/(2a^2)-V]/3`.

Frozen branch:
- `attractor_ic_scf=no`;
- `phi_ini=1`;
- `phi_prime_ini=0`;
- physical theory parameter `lambda`;
- nuisance normalization `A`;
- `scf_tuning_index=2` so shooting changes `A`, never `lambda`.

`phi_ini=1` avoids the pinned CLASS alpha-zero coordinate singularity at `phi=B=0`; this does not change the alpha-zero pure-exponential physical branch because the constant field-coordinate shift is absorbed into the normalization nuisance.

## Reference intersection

At `lambda=0` and `phi_prime=0`, the potential is constant and

`p_phi=-rho_phi`.

Therefore replacing Lambda by a constant scalar at matched total density must reproduce LambdaCDM if solver/bookkeeping are clean.

This has now been verified twice:

### Subdominant calibration run `34325977559`

For `Omega_scf=0.10`, lambda zero gives:
- achieved `Omega_scf(today)=0.10000000013560413`;
- `w_scf=-1`, `phi=1`, `phi_prime=0` on all frozen nodes;
- `max_abs_lnH=5.46292e-11`;
- `max_abs_lnP=4.11152e-7`.

### Dark-energy-dominant strict production run `34338140447`

Target:
`Omega_scf_target=0.682686955086854`.

Lambda-zero result:
- achieved `Omega_scf(today)=0.682686955181768`;
- `w_scf=-1`, `phi=1`, `phi_prime=0`;
- `max_abs_lnH=1.08876e-10`;
- `max_abs_lnP=2.16648e-10`.

The preregistered production reference thresholds are satisfied by large margins.

## Numerical conditioning audit

Default CLASS one-dimensional shooting scales its root tolerance in the raw nuisance coordinate. Here `A~ -1` while the physically resolved normalization is `N=1+A << 1`. Default `tol_shooting_deltax_rel=1e-5` therefore allowed target-density drift that increased with lambda.

Default errors in `Omega_scf(today)-target`:
- lambda 0.025: `+2.57319e-8`;
- 0.075: `+3.11478e-6`;
- 0.15: `+6.10320e-5`;
- 0.30: `+1.23798e-3`.

A preregistered rerun changed only

`tol_shooting_deltax_rel: 1e-5 -> 1e-13`.

Strict errors:
- 0.025: `+2.57319e-8`;
- 0.075: `-3.43697e-11`;
- 0.15: `-1.58952e-10`;
- 0.30: `-3.01260e-10`.

All pass the frozen `1e-6` target-error gate.

This matters for the response itself: at lambda 0.30 the default vs strict 35-node `r_Delta` vectors differ by about `38.1%` in relative norm and `1.33 deg` in direction; H-response norm differs by about `49.6%`. Default vectors are therefore retained only as numerical-conditioning evidence. Strict run `34338140447` is authoritative for B4/B6.

See:
- `waves/wave_03_expanded_dark_energy/M07_SHOOTING_PRECISION_AUDIT.md`;
- `waves/wave_03_expanded_dark_energy/M07_SHOOTING_PRECISION_RESULT.md`;
- `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`.

## B6 nearest-comparator attack

Reproducible run: `34358089618`.

Common block:
`r_Delta(k,z)`, 7 frozen z nodes x 5 low-k nodes, unwhitened theory-response geometry.

Against C1 smooth non-phantom wCDM:
- lambda 0.025: acute angle `15.9702 deg`;
- 0.075: `6.9206 deg`;
- 0.15: `6.6924 deg`;
- 0.30: `6.6114 deg`.

For lambda >=0.075, best scalar projection still leaves roughly `11.5-12.0%` orthogonal residual. Exact collinearity is rejected, but the low-k matter-response near-degeneracy is strong.

Against the frozen minimum-resolved designer-f(R) ray:
- acute angles decrease from `73.0805 deg` at lambda 0.025 to `60.7968 deg` at lambda 0.30;
- best scalar projection leaves about `87-96%` residual.

Thus in this restricted block M07 is far closer to phenomenological smooth DE than to the frozen MG comparator. No observational discrimination is claimed.

See `waves/wave_03_expanded_dark_energy/M07_B6_NEAREST_COMPARATOR.md`.

## Emerging local-geometry question

Strict response norms approximately scale as lambda squared:

`||r_Delta||/lambda^2 = {0.1105,0.1167,0.1175,0.1189}`

for lambda `{0.025,0.075,0.15,0.30}`.

This raises a nontrivial local-coordinate issue: if the response is even in lambda, the naive first derivative `dr/dlambda` at lambda=0 vanishes even though a nonzero second-order response exists. A preregistered `+/-lambda` parity audit is running to test whether `q=lambda^2` is the appropriate near-reference coordinate.

Active workflow:
`.github/workflows/w03-m07-parity-coordinate-audit.yml`.

Preregistered hard parity threshold:
`||r_odd||/||r_even|| <= 1e-3`.

No post-hoc threshold is imposed on convergence of `r/lambda^2`; that is descriptive until separately frozen.

## B0-B9 gate ledger

| Gate | State | Evidence / requirement |
|---|---|---|
| B0 identity/provenance | `PASS_WITH_SCOPE` | pinned canonical CLASS scf subset, explicit IC and physical/nuisance semantics |
| B1 DSIR embedding/reference limit | `PASS_WITH_SCOPE` | subdominant and full-DE lambda-zero scalar replacements reproduce LambdaCDM within frozen numerical tolerances |
| B2 conservation/gauge/frame bookkeeping | `PARTIAL` | minimally coupled canonical implementation and matched total reference clean; explicit cross-gauge/additional-response audit pending |
| B3 physical-domain/numerical control | `PASS_WITH_SCOPE` | natural-scale seed + strict shooting pass frozen target and reference gates; positive finite backgrounds on production grid |
| B4 response coverage/masks | `PASS_WITH_SCOPE` | authoritative strict 7x5 low-k matter response produced for lambda `{0.025,0.075,0.15,0.30}`; broader metric/slip/time coverage still future work |
| B5 reference identifiability | `OPEN` | no observation-space promotion without pinned operator/covariance |
| B6 nearest comparator | `PASS_WITH_SCOPE` | strong C1 near-alignment but non-collinearity; large separation from frozen f(R) ray on common low-k theory-response block |
| B7 quotient-surviving novelty | `OPEN` | orthogonal channel / observation-space survival not yet established |
| B8 prospective withheld prediction | `OPEN` | no prospective relation/holdout frozen; production points are not B8 evidence |
| B9 synthesis/design priors | `PARTIAL` | numerical conditioning, comparator pressure and possible higher-order local coordinate feed methodology |

## Current overall verdict

`DSIR_COMPATIBLE`.

Precise meaning: M07 has a clean reference limit, controlled physical/numerical production branch and nontrivial DSIR response. Its restricted low-k response is nearly degenerate with smooth-w and has not yet been shown observationally distinguishable. This is not a falsification and not a uniqueness claim.

## Design-prior pressure from M07

- physical parameters and solver nuisance parameters must be separated;
- sensitive nuisance coordinates require natural-scale initialization and tolerance conditioning in the physically resolved combination;
- exact analytic reference intersections require numerical regression before finite-deformation science;
- microphysical DE must be attacked against both phenomenological DE and MG comparators;
- strong nearest-comparator alignment demands an orthogonal response channel before mechanism attribution;
- local model geometry may be higher-order, so the natural identifiable coordinate must be established before Jacobian/rank claims.
