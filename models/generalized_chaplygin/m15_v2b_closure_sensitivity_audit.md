# M15 V2b closure-axis provenance and algebra audit

Date: 2026-09-10
Status: `CLOSURE_AXIS_STRUCTURALLY_NONCANCELLING_V2B_PREREGISTERED`
Scientific promotion: **NO K3/K5 promotion yet**

## Authority inspected

- R. F. vom Marttens et al., *Does a generalized Chaplygin gas correctly describe the cosmological dark sector?*, PDU 15 (2017) 114-124, arXiv:1702.00651.
- Existing KMDSB source map `m15_v2_equation_to_class_map.md`.
- Validated independent V1 alpha=0 reference result and V2a exact finite-alpha background result.

## Provenance result

The published perturbation section defines `c_s,A^2` as the comoving sound speed. For the `w_Lambda=-1` vacuum-like component, Eq. (45) retains `c_s^2` in the DE energy balance and Eq. (46) retains it in the spatial interaction perturbation `fhat`.

The numerical section inspected from the start of Section VII through the CMB/transfer/growth discussion specifies the sampled `alpha`, corresponding `Omega_c0` intervals and `h`, and states that the previous perturbation system is implemented in modified CLASS, but does not state a numerical choice for `c_s,Lambda^2`.

Therefore the current exact-author-numerics blocker is retained. Neither `c_s^2=0` nor `1` may be called the authors' numerical closure without new provenance.

## Algebraic non-cancellation result

For Eq. (45), solving exactly as instructed by the paper gives

`Qhat = (rho_Lambda/a) [delta_Lambda' + 3 H (c_s^2+1) delta_Lambda - (a Q/rho_Lambda)(psi-delta_Lambda)]`.

Holding the same background and perturbation state fixed, the difference between endpoint closures CS1 (`c_s^2=1`) and CS0 (`c_s^2=0`) is therefore

`Delta Qhat = 3 H rho_Lambda delta_Lambda / a`.

From Eq. (46),

`fhat = c_s^2 rho_Lambda delta_Lambda/a - Q vhat`,

so

`Delta fhat = rho_Lambda delta_Lambda/a`.

These terms enter the CDM continuity and Euler equations (47)-(48). Hence the sound-speed choice is not an algebraically cancelling implementation nuisance. For finite `alpha`, Eq. (49) gives

`delta_Lambda = -(2 alpha/(3H)) Thetahat`,

so the closure difference is generically nonzero whenever the scalar expansion perturbation is nonzero.

At the exact reference `alpha=0`, Eq. (49) forces `delta_Lambda=0`, and both endpoint closure differences vanish. This supplies a strong prospective implementation control for V2b: CS0 and CS1 must both reduce to the same alpha=0 LambdaCDM result before any finite-alpha sensitivity is consumed.

## Scientific meaning

This audit establishes only that the published equations contain a genuine perturbation-closure axis. It does **not** establish that CS0 and CS1 generate observationally distinguishable spectra, nor that both endpoints are stable/admissible over the full domain, nor which endpoint (if either) was used by the authors.

Under the KMDSB coverage protocol, this axis cannot be silently fixed and then used as the unique F15 representative. The numerical question is now prospectively frozen in `waves/wave_03_expanded_dark_energy/M15_V2B_CLOSURE_SENSITIVITY_PREREGISTRATION.md`.

## Current gate state

- K0: `PASS_WITH_SCOPE_INDEPENDENT_REPRODUCTION`.
- K1: `PASS_WITH_SCOPE_ALPHA0_LCDM_EXACT` from V1.
- K2: finite-alpha background geometry supported; closure-domain geometry remains incomplete.
- K3: remains `BLOCKED_EXACT_AUTHOR_SOUND_SPEED_PROVENANCE`; independent closure verification is now authorized under a separate label.
- K4: background-only partial evidence from V2a; perturbation robustness not tested.
- K5-K9: not opened by this audit.

No physical/family falsification is implied.

## Exact next gate

Implement the preregistered V2b alpha=0 CS0/CS1 reference scaffold on the pinned CLASS base, archive the exact source diff and full products, and consume the reference artifact before running finite `alpha=+/-0.05` closure sensitivity.
