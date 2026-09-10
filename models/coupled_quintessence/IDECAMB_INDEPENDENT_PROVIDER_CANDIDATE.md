# M14 independent perturbation-complete provider candidate: IDECAMB

Date: 2026-09-10
Status: `CANDIDATE_PROVENANCE_AUDIT_NEXT`

## Candidate

Patch repository pinned at:

`liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

Its README explicitly states that IDECAMB provides coupled quintessence (CQ) and coupled-fluid models. The committed `test_ide.ini` defines `Class_IDE = 2` as coupled quintessence, `beta_cq` as the coupling constant, and separates potential/coupling forms (`UForm_CQ`, `QForm_CQ`).

The patch README instructs users to apply it to the public `cmbant/CosmoMC` `planck2018` branch. The current branch head resolves to exact immutable commit:

`cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`.

This base pin is a candidate compatibility anchor, not yet a demonstrated successful overlay/build.

## Why this is stronger than the current iDM K3 route

IDECAMB's `camb/equations_ppfi.f90` actively contains the CQ coupling parameter in the cosmological equations, including an exponential-coupling energy-transfer function `Coup_CQ = CQP%beta * grhoc_t * gphidot` and a beta-dependent CDM density expression. This makes it a plausible independent route to a perturbation-complete M14 implementation rather than a background-only coupling with a commented perturbation correction.

No K3 PASS is granted from source keywords alone. The exact perturbation evolution equations and conservation closure must be source-bound before promotion.

## Next prospectively allowed gate

1. Pin both patch and base commits above.
2. Audit the README/manual overlay map exactly; do not infer unmentioned file renames.
3. Build the overlaid CosmoMC/CAMB provider without modifying physics.
4. Run an author configuration/provider control if its data dependencies permit; if Planck likelihood data block execution, isolate a CAMB-theory control only if the repository itself documents a valid route.
5. Source-bind active CQ background and perturbation equations and the beta->0 decoupling map.
6. Only then preregister K1 regression and nonzero-beta K2-K5 grid.

Failure to overlay/build is `BLOCKED_IMPLEMENTATION/PROVENANCE`, not evidence against coupled quintessence.
