# W03 M18 ghost-condensate / dilatonic-ghost reference probe preregistration v0.1

Status: PROSPECTIVE / DIAGNOSTIC ONLY
Date: 2026-09-10

## Purpose

Establish whether the already provider-validated `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7` model-1 dilatonic-ghost branch admits a clean, numerically executable condensate reference path before any M18 response-family production test.

This probe cannot promote K5-K9/B4-B8 and cannot be used as observational discrimination.

## Pinned implementation

- provider: `KunhaoZhong/CLASS_GSF`
- commit: `07e015246c4b40f4e22bb50c9a0a63a621bb61f7`
- model selector: `gsf_parameters[0]=1`
- author equation in `source/background.c`:
  `P(X,phi) = -X + c1 exp(lambda phi) X^2`
- author committed example: `dgf.ini`
- author example physical values encoded by `gsf_parameters = 1, 7, 1, 10, -18, 0.2, 1`; index 6 (`c1`) is the shooting nuisance.

## Reference geometry

For `lambda=0`, the Lagrangian is shift symmetric: `P(X)=-X+c1 X^2`.

`P_X = -1 + 2 c1 X`.

The condensate locus is therefore `P_X=0`, or `c1 X=1/2`. On that locus,

- `P=-X/2`;
- `rho=2 X P_X-P=X/2`;
- `w=P/rho=-1`.

Thus the prospective K1 diagnostic path is `lambda -> 0` with the provider's closure shooting retained on `c1`, plus direct inspection of whether the evolved solution approaches/maintains the condensate locus and whether its total expansion matches an otherwise identical Lambda closure control.

No claim is made in advance that the author's finite-IC shooting lands exactly on this locus.

## Frozen diagnostic cases

1. `lcdm`: same base cosmology, `Omega_gsf=0`, `Omega_Lambda` inferred by closure.
2. `dgf_author`: exact committed `dgf.ini`, unchanged except output root/verbosity only if needed by the harness.
3. `dgf_lambda0`: exact committed `dgf.ini` with only physical `lambda` changed from `0.2` to `0`; `c1` remains shooting index 6 and all initial-condition entries remain author values.

The probe must record build/case exit codes and preserve background files/logs.

## Diagnostic quantities

If all cases execute, report without a promotion threshold:

- max relative `H(z)` difference between `dgf_lambda0` and `lcdm` on their common finite redshift rows;
- max absolute `w_gsf+1` for the lambda-zero branch where finite;
- max absolute `P_X` for the lambda-zero branch where output exposes it;
- present-day `Omega_gsf`, if available;
- whether the author point produces finite background and P(k), as a repeated provider control.

This is a floor-finding probe. The result is one of:

- `REFERENCE_PROBE_EXECUTABLE`: lambda-zero and controls execute; production K1 tolerance still must be preregistered from the measured numerical/reference floor;
- `REFERENCE_PROBE_NOT_ON_CONDENSATE`: executable but finite-IC/shooting branch does not realize a credible w=-1/P_X=0 reference; K1 remains blocked pending an independently justified IC prescription;
- `BLOCKED_IMPLEMENTATION_REFERENCE_PROBE`: lambda-zero branch does not execute while provider author control does;
- `BLOCKED_PROVIDER`: exact author control itself no longer executes.

## Guardrails

- no post-result change of lambda, ICs, shooting index or solver tolerances inside this probe;
- configuration failure is not physical failure;
- provider execution is not M18 family validation;
- no theory-space diagnostic is an observational claim;
- undefined/missing columns are masked, never zero-imputed;
- a production response grid requires a new prospective preregistration after this probe.