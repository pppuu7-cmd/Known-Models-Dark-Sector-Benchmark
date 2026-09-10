# W03 M12 Phantom dark-energy preregistration v0.1

Frozen: 2026-09-10
Status: PREREGISTERED BEFORE OUTPUT
Coverage family: F12 / M12

## Scope split

M12 separates two questions that must not be conflated:

1. **response representative:** a smooth constant-w fluid on the phantom side `w<-1`, evolved with the same pinned CLASS/PPF machinery as the smooth-DE controls;
2. **minimal-field physical realization:** the textbook minimally coupled scalar with a wrong-sign kinetic term. This realization has the standard ghost/vacuum-stability concern and is not made physically healthy merely because its background fits data.

A phenomenological `w<-1` response does not imply that every theory producing effective phantom behavior contains a ghost. Stable effective phantom behavior in more general kinetic/modified-gravity/multifield constructions belongs to their own census families (M13/M18/M30/M31 etc.).

Literature scope note: see arXiv:1708.06981 for a review of phantom-DE viability/pathologies and alternatives producing apparent `w<-1`.

## Frozen response geometry

Reference point: `w=-1`, `cs2=1`, PPF enabled.

Two physically different one-sided coordinates:

- nonphantom: `q_plus = 1+w >= 0`, `w=-1+q_plus`;
- phantom: `q_minus = -(1+w) >= 0`, `w=-1-q_minus`.

Frozen steps for each ray:
- `h=1e-3`
- `2h=2e-3`.

Directions:

`J_plus(h) = r(w=-1+h)/h`

`J_minus(h) = r(w=-1-h)/h`.

Because the coordinates point away from Lambda on opposite sides, exact first-order representability by one smooth constant-w line predicts `J_minus ~ -J_plus`. The test compares both oriented vectors and unoriented response lines.

## Solver

Pinned CLASS `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Common settings:
- h=.67, omega_b=.0224, omega_cdm=.1200, flat;
- fluid branch `Omega_Lambda=0`, `Omega_fld` inferred by closure;
- CLP, `wa=0`, `cs2=1`, `use_ppf=yes`;
- synchronous, linear mPk, no reionization;
- same seven z and five low-k nodes as W03 controls;
- `tol_perturbations_integration=1e-8`;
- `perturbations_sampling_stepsize=.01`.

Also compute pure-Lambda vs fluid-w=-1 reference regression.

## Frozen hard gates

Reference:
- max |lnP| <=1e-6
- max |lnH| <=1e-8.

Each one-sided tangent convergence (`h` vs `2h`):
- relative norm difference <=0.02
- acute angle <=1 deg.

Response-line classification using h=1e-3:
- if acute line angle <=1 deg AND best line-projection residual <=0.02 -> `PHANTOM_RESPONSE_REPRESENTED_BY_CONSTANT_W_LINE_WITH_SCOPE`;
- if residual >=0.20 -> `PHANTOM_RESPONSE_SEPARATED_FROM_LOCAL_CONSTANT_W_LINE_WITH_SCOPE`;
- otherwise `INCONCLUSIVE_LOCAL_LINE_RELATION`.

This is theory-response only. No observational inference is allowed from the line geometry.

## Physical-domain interpretation

The response result and field-theory pathology are recorded independently:
- a line-equivalent response does not cure a ghost in the minimal wrong-sign scalar realization;
- a ghost concern in the minimal scalar does not falsify every effective theory with `w_eff<-1`;
- M13/M18/M30/M31 remain necessary coverage even if M12 is response-represented by M01/M08.
