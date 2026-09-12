# W07 M33 provider-documented noise-safe K1 confirmation v0.1

Date: 2026-09-12
Model: cubic Galileon in `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
Purpose: prospectively test whether the cubic-Galileon reference path satisfies the standard KMDSB K1 decoupling rule when using the provider-documented `D_safe_smg` mechanism specifically intended to tolerate tiny negative values caused by numerical noise around zero.

## Motivation and immutable prerequisite
W07 diagnostics established that the strict `D_safe_smg=0` vetoes are tiny (`|D_min|~1e-106`) and nonmonotonic across nearby Omega_smg, while a fixed `D_safe_smg=1e-100` makes all preregistered veto points executable with finite CMB/P(k). This confirmation does not reinterpret those runs as physical stability; it tests a single prospectively fixed provider-supported numerical profile.

## Frozen profile and arms
Use `D_safe_smg=1e-100`, `a_min_stability_test_smg=0`, with all other shipped cubic Galileon settings unchanged, at exactly:
`Omega_smg = {0.01, 0.005, 0.002, 0.001}`.
Use the same parser-compliant removal of `Omega_Lambda` and `Omega_fld` as prior successful runs.

Build an explicit GR control by removing `Omega_smg`, `Omega_Lambda`, `Omega_fld`, `gravity_model`, and `gravity_submodel` from the same source config, as in the earlier parser recovery.

## Mandatory no-dynamics-change control
At `Omega_smg=0.01`, execute both:
- strict provider stability profile `D_safe_smg=0`;
- noise-safe profile `D_safe_smg=1e-100`.
Both must exit 0 with finite outputs. Their CMB and P(k) normalized-L2 difference must each be <=1e-12. Otherwise the confirmation is invalid.

## Frozen K1 rule
After the no-dynamics-change control passes, apply the repository-standard `verification/k1/decoupling_ladder.py` to the four noise-safe arms versus explicit GR. It requires:
- finest response < coarsest;
- each adjacent response <=1.20 times the previous;
- finest/coarsest <=0.25;
- log-log correlation >=0.90.

A passing result may recommend `K1=PASS_WITH_SCOPE_NUMERICAL_NOISE_SAFE_PROFILE`, but this workflow itself does not edit the canonical matrix. Full physical family stability is not established.

Always set `K1_promoted=false` in this execution artifact, `physical_falsification=false`, and `family_wide_stability_claim=false`. Canonical promotion, if warranted, requires a separate immutable synthesis/sync step.