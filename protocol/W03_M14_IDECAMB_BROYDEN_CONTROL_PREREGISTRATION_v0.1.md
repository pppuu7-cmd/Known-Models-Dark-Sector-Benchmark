# W03 M14 IDECAMB Broyden-control preregistration v0.1

Date: 2026-09-10
Target: M14 coupled quintessence
Purpose: diagnose whether the remaining source-scaled K4 angular failure is caused by the pinned provider's nonstandard shooting inverse-Jacobian update.

## Frozen provider and model

- base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- `Class_IDE=2`
- `UForm_CQ=1`
- `QForm_CQ=1`
- fixed `alpha_quint=0.02`
- external likelihoods disabled, theory-output mode only

## Frozen beta grid

`beta_cq = {0, 5e-8, 1e-7}`

This is exactly the prior source-scaled grid. No new step-size search is allowed in this diagnostic.

## Diagnostic-only source changes

Only two non-physical changes are authorized:

1. In the coupled-quintessence `GetCorrect_initial`, replace the scalar inverse-Jacobian rescaling

`H1=(1+t1/t2)*H0`

by the standard good-Broyden inverse rank-one update

`H1 = H0 + (s-Hy)(s^T H)/(s^T H y)`

implemented using the existing `dx`, `df`, `v1`, `v2`, `t2` variables.

2. Change the `.quantity` serialization from `11E15.5` to `11ES25.15E3`, matching the completed diagnostic-precision audit.

The physical background and perturbation equations, potential, coupling law, integration tolerance, anchor, and response definition must not be edited.

## Frozen response vector

Same as source-scaled M14:

- dln rho_de(a)
- dln rho_c(a)
- dln H(a)
- dw(a)
- qhat(a)
- dln TT(ell)
- dln EE(ell)
- dln PP(ell)

## Frozen K4 thresholds

For derivative vectors from h=5e-8 and 2h=1e-7:

- relative tangent-norm mismatch <= 0.10
- tangent angle <= 3.0 deg

K5 non-null floor remains `5e-5`, but K5 is not scientifically promoted from a patched diagnostic provider.

## Additional diagnostic outputs

For each beta point record:

- process exit code;
- final shooting residual norm if available from instrumented log;
- final shooting coordinates `(gU0,gphi0)` if available;
- response metrics above.

## Decision rule

- If corrected Broyden restores the frozen K4 directional convergence or materially reduces the angle while shooting variables/residuals become smooth, classify the upstream IDECAMB M14 result as blocked by a numerical shooting implementation defect; do not treat upstream K4 failure as model physics.
- If corrected Broyden leaves the angular failure materially unchanged and shooting diagnostics are smooth, continue to initial-condition/asymptotic-anchor sensitivity.
- If the corrected solver fails to execute or does not converge, classify the diagnostic itself as blocked; do not infer physical falsification.

No observational claim and no M14 family falsification are authorized by this diagnostic.