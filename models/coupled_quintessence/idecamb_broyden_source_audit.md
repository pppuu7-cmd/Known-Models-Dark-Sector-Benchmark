# M14 IDECAMB coupled-quintessence Broyden shooting audit

Updated: 2026-09-10
Status: `UPSTREAM_SHOOTING_UPDATE_DEFECT_CANDIDATE`
Scientific effect: **M14 K4 cannot be interpreted as physical local non-convergence until this numerical implementation issue is controlled.**
Physical falsification: **NO**

## Trigger

The preregistered source-scaled M14 gate at beta={0,5e-8,1e-7} reduced the tangent-norm mismatch below the frozen 10% threshold but retained an angle failure (>3 deg). Increasing diagnostic serialization precision did not remove the angle failure. The next preregistered logical step was therefore branch/root/initial-condition continuity rather than further step chasing.

## Pinned upstream source

Provider:

`liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

File:

`camb/equations_ppfi.f90`

The coupled-quintessence background is solved after `GetCorrect_initial`, whose comment says it obtains `gU0` and `gphi0` with a Broyden iteration.

The relevant inverse-Jacobian update in the pinned source is:

```fortran
v1=matmul(H0,df)
v2=dx-v1
t1=dot_product(v2,dx)
t2=dot_product(dx,v1)
H1=(1+t1/t2)*H0
```

The same scalar-rescaling pattern also appears in the coupled-fluid helper, but this audit concerns the M14 coupled-quintessence path only.

## Secant-condition audit

Let

- `s = dx`,
- `y = df`,
- `H = H0`,
- `v1 = H y`,
- `v2 = s - H y`,
- `rho = s^T H y = t2`.

For the usual good-Broyden inverse update, the rank-one update is

`H_new = H + (s-Hy) (s^T H) / (s^T H y)`.

This construction enforces the inverse secant relation

`H_new y = s`

(up to numerical precision when the denominator is nonzero).

The pinned IDECAMB line instead gives

`H_new = scalar * H`.

Then

`H_new y = scalar * H y`,

which can equal `s` only in the special case where `s` is collinear with `H y` with exactly the required scale. In a generic two-dimensional shooting problem this does **not** implement the Broyden rank-one secant correction.

Therefore the source implementation labelled as Broyden is not algebraically equivalent to the standard inverse-Jacobian Broyden update.

## Why this matters for M14

The two shooting variables are `gU0` and `gphi0`. They are adjusted so that the integrated solution reaches both the required present dark-energy density and the target present field value. A defective inverse-Jacobian update can:

1. converge inefficiently or to a step-history-dependent point;
2. amplify small changes in beta into changes of the selected shooting solution;
3. create an artificial rotation of the finite-difference response vector even when the underlying differential equations have a smooth local tangent.

This is a plausible numerical explanation for the remaining source-scaled K4 angular failure, but it is **not yet proven causal**. A controlled patched-vs-upstream run is required.

## Classification change authorized by this audit

Until the diagnostic control is complete, interpret the current IDECAMB M14 state as

`K4 = BLOCKED_IMPLEMENTATION_SHOOTING_AUDIT`

rather than as evidence for a physical failure of local differentiability.

Retain all prior K4 numerical results; do not delete or relabel their raw classifications. The change is in scientific interpretation, not in recorded measurements.

## Preregistered next diagnostic

A single diagnostic-only control is authorized:

1. use the exact same pinned provider, potential/coupling branch, alpha anchor, beta grid `{0,5e-8,1e-7}`, response vector, and frozen K4 thresholds;
2. replace **only** the coupled-quintessence inverse-Jacobian update by the standard good-Broyden rank-one formula;
3. retain the high-precision diagnostic serialization already audited;
4. record final shooting variables and residual norm for every beta point;
5. compare patched K4 with the unmodified source-scaled result;
6. do not promote a patched provider to a physical benchmark implementation solely because the diagnostic passes.

Decision rule:

- if the corrected numerical update materially restores tangent-direction convergence, classify the upstream M14 provider as `BLOCKED_IMPLEMENTATION_BROYDEN_UPDATE` and search for/construct an independently validated implementation before physical M14 scoring;
- if the corrected update leaves the angular failure materially unchanged while shooting residuals and branch variables are smooth, continue to initial-condition/asymptotic-anchor sensitivity rather than step-size chasing.

No observational claim and no model-family falsification are authorized by this audit.
