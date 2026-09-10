# M14 IDECAMB coupled-quintessence Broyden shooting audit

Updated: 2026-09-10
Status: `BROYDEN_DEFECT_REAL_BUT_NOT_CAUSAL_FOR_CURRENT_K4_ROTATION`
Scientific effect: **M14 K4 remains blocked by provider/branch-continuity diagnostics; the upstream Broyden defect does not explain the observed source-scaled tangent rotation.**
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

## Frozen diagnostic control and result

Preregistration: `protocol/W03_M14_IDECAMB_BROYDEN_CONTROL_PREREGISTRATION_v0.1.md`.

Actions run: `34466179406`.
Job: `102835190766`.
Immutable artifact: `10147638232` (`w03-m14-idecamb-broyden-control`).
Machine result: `waves/wave_03_expanded_dark_energy/M14_IDECAMB_BROYDEN_CONTROL_RESULT.json`.

The diagnostic changed only the coupled-quintessence inverse-Jacobian update to the standard good-Broyden rank-one form and retained the previously audited high-precision diagnostic serialization. The physical equations, alpha anchor, beta grid, response vector and frozen K4 thresholds were unchanged.

All three frozen cases beta={0,5e-8,1e-7} executed with exit 0.

Patched-control metrics:

- relative tangent-norm mismatch = `0.009279120139592109` (PASS against <=0.10);
- tangent angle = `8.041541873388278 deg` (FAIL against <=3 deg);
- fine-step max absolute response = `6.952538051818101e-4`.

For comparison, the unmodified high-precision control had:

- relative tangent-norm mismatch = `0.009270610485819343`;
- tangent angle = `8.04171613320909 deg`.

The change in angle is only about `1.74e-4 deg`; therefore correcting the Broyden update does not materially restore the frozen K4 directional convergence.

The instrumented shooting solution is smooth across the same grid:

- beta=0: `(gU0,gphi0)=(0.9567029816909431,0.1299982393732581)`, residual norm `1.789909612091193e-7`;
- beta=5e-8: `(0.9567029856339913,0.1299982636654189)`, residual `1.789911197048994e-7`;
- beta=1e-7: `(0.9567029895685109,0.1299982879913752)`, residual `1.789910885597791e-7`.

Thus there is no evidence in this control for a discontinuous jump between distinct shooting roots over the frozen grid.

## Scientific interpretation

The upstream Broyden update is an implementation defect in the numerical method, but this controlled experiment shows that it is **not sufficient to explain** the current M14 K4 angular failure.

The prior raw K4 failures remain recorded and are not relabelled. However they still do not constitute a physical falsification of coupled quintessence, because the response is being measured in a provider whose asymptotic/initial-condition construction and beta->0 branch regularity have not yet been independently validated.

Current interpretation:

`K4 = BLOCKED_IMPLEMENTATION_INITIAL_ASYMPTOTIC_ANCHOR_AUDIT`

K5/K6 remain blocked.

## Next allowed diagnostic

Do not shrink beta again. The next gate must inspect the initial/asymptotic construction used by the CQ branch and identify whether the beta=0 solution and beta>0 solutions are initialized with the same physical asymptotic prescription. Before execution it must freeze:

1. the exact initial-scale-factor / integration-start prescription;
2. the analytic early-time scalar/CDM asymptotic conditions used by the provider;
3. any beta-dependent branch or denominator entering those conditions;
4. one or more source-justified alternative start points or asymptotic controls, if such alternatives are already supported by the provider;
5. the unchanged beta grid `{0,5e-8,1e-7}` and the same K4 metrics.

If no author-supported regular asymptotic control exists, classify this provider as blocked for M14 K4 and move to an independent implementation rather than inventing initial conditions.

No observational claim and no model-family falsification are authorized by this audit.
