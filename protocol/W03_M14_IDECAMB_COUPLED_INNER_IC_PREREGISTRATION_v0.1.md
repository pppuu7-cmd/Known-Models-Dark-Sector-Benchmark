# W03 M14 IDECAMB coupling-aware inner-IC preregistration v0.1

Date: 2026-09-10
Target: M14 coupled quintessence
Purpose: test whether the pinned provider's beta-independent uncoupled radiation-era tracker initial condition causes the persistent source-scaled K4 tangent rotation.

## Motivation fixed before execution

The pinned coupled-quintessence source starts at `amin=1e-12` with the uncoupled inverse-power tracker

`phi proportional to a^[4/(2+alpha)]`,

which contains no beta dependence. Yet the full scalar equation contains the early coupling force `beta rho_c`, and the source-derived crossover estimate gives `beta/beta_star(amin) ~ 4.4e6` for the fine beta step `5e-8` at the actual start surface.

A direct global-`amin` sensitivity test was preregistered and attempted, but changing `amin` also truncated the background interpolation domain required later by CAMB and produced a segmentation/DVERK failure already at `amin=1e-8`. It was therefore classified as a blocked diagnostic, with no scientific inference.

This control keeps the global provider domain exactly at `amin=1e-12` and changes only the background initial state for nonzero beta.

## Frozen provider/model

- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- `Class_IDE=2`
- `UForm_CQ=1`
- `QForm_CQ=1`
- `alpha_quint=0.02`
- global `amin=1e-12` unchanged
- upstream Broyden root update unchanged
- physical evolution equations unchanged
- high-precision diagnostic serialization `11ES25.15E3`
- external likelihoods disabled; theory-output mode only

## Frozen beta grid

`beta_cq = {0, 5e-8, 1e-7}`.

No step-size search is authorized in this control.

## Diagnostic initial-state replacement

For `beta=0`, retain the exact upstream uncoupled tracker initial condition.

For `beta>0`, replace only the two initial-state values at `a=amin` by the leading regular radiation-era coupling-dominated particular solution derived from the pinned source equations:

`phi_i = beta * grhoc * amin / (2 adotrad^2)`

and

`(a^2 phi')_i = beta * grhoc * amin^2 / (2 adotrad)`.

This follows from the source equations in the limit where radiation dominates the conformal Hubble rate and `beta rho_c` dominates the inverse-power potential-gradient force at the start surface.

No perturbation equation, coupling law, potential law, present-day target, or integration tolerance is changed.

## Frozen response vector and K4 thresholds

Exactly as in the source-scaled M14 gate:

- dln rho_de(a)
- dln rho_c(a)
- dln H(a)
- dw(a)
- qhat(a)
- dln TT(ell)
- dln EE(ell)
- dln PP(ell)

For derivative vectors from h=5e-8 and 2h=1e-7:

- relative tangent-norm mismatch <= 0.10;
- tangent angle <= 3.0 deg.

## Additional diagnostics

Record for each beta point:

- process exit code;
- final shooting coordinates `(gU0,gphi0)` and residual norm if available;
- full channel response amplitudes;
- K4 mismatch and angle.

Retain the already measured upstream high-precision control values:

- mismatch `0.009270610485819343`;
- angle `8.04171613320909 deg`.

## Predeclared interpretation

- If the coupling-aware inner IC executes cleanly and satisfies both frozen K4 thresholds, classify `M14_IDECAMB_UPSTREAM_IC_NONUNIFORMITY_CAUSAL_SUPPORT`.
- If it does not pass but reduces the angle by at least 50% relative to `8.04171613320909 deg`, classify `M14_IDECAMB_INNER_IC_PARTIAL_CAUSAL_SUPPORT`.
- If the angle remains at least 50% of the upstream value, classify `M14_IDECAMB_INNER_IC_NOT_SUFFICIENT`.
- Any root/integration/output failure is `M14_IDECAMB_INNER_IC_DIAGNOSTIC_BLOCKED` and carries no physical conclusion.

A diagnostic pass does **not** promote this hand-derived leading asymptotic as the validated physical provider. It would instead require a matched-asymptotic derivation and/or an independent solver implementation before M14 physical K4/K5 scoring.

No observational claim and no model-family falsification are authorized.