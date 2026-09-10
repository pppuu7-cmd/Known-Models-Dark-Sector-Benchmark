# W03 M14 LisaGoh/CDE K1 background-arm recovery preregistration v0.2

Date: 2026-09-10
Parent K1 run: `34488423569`
Parent preregistration: `W03_M14_LISAGOH_CDE_K1_REFERENCE_PREREGISTRATION_v0.1.md`

## Parent outcomes frozen

- Arm B exact-zero full reference: exit 1 during perturbation integration with `Failure in sp_ludcmp. Possibly singular matrix!`; no required full outputs.
- Arm C beta=0 with committed tiny scalar seeds: exit 0 and produced fresh nonempty background, perturbation, linear P(k), CMB Cl and transfer outputs.
- Arm A exact-zero background-only control never reached background integration because the harness set `output=` while retaining the author's `lensing=yes`; CLASS input validation correctly rejected lensing without tCl/pCl/lCl.

Therefore only arm A suffered an input/output-request plumbing mismatch. B and C must not be rerun or altered in this recovery.

## Frozen recovery

Run only arm A again, identical to the parent exact-zero background arm except for one computational-request correction:

- retain `beta_1=beta_2=beta_3=0`;
- retain `phi_ini_scf=0`, `phi_prime_ini_scf=0`;
- retain `output=`;
- additionally set `lensing=no`;
- retain `write background=yes`;
- use `root=output/k1_exact_bg_recovery_`.

No source, physical parameter, initial condition, threshold or background precision may change.

## Frozen metrics

Use exactly the parent thresholds and functional:

`Rspan(x)=(max(x)-min(x))/max(max(abs(x)),1e-300)`.

Require finite background values and:

- max |beta| <= 1e-15;
- max |dbeta/dz| <= 1e-15;
- max |phi_prime_scf| <= 1e-14;
- max |w_scf+1| <= 1e-12;
- Rspan(rho_scf) <= 1e-12;
- Rspan(rho_cdm*a^3) <= 1e-8.

## Final classification using immutable parent B/C

- If recovered A passes, classify the combined K1 record `M14_LISAGOH_CDE_K1_EXACT_REFERENCE_IMPLEMENTATION_BLOCKED`: background exact reference is valid, exact full perturbation route fails, while predeclared tiny-seed beta=0 diagnostic succeeds.
- If recovered A executes but violates a frozen invariant, classify `M14_LISAGOH_CDE_K1_BACKGROUND_REFERENCE_FAIL`.
- If recovered A is blocked again for a new nonphysical reason, retain `BLOCKED_INFRASTRUCTURE` pending explicit audit; do not alter thresholds.

A passing recovered A does **not** convert strict K1 to PASS_WITH_SCOPE because the exact full arm B already failed. It instead localizes the blocker to the perturbation implementation around the exact reference state.

No physical M14 falsification is authorized.