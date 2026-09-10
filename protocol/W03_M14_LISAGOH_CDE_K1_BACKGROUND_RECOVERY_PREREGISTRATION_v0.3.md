# W03 M14 LisaGoh/CDE K1 background-arm recovery preregistration v0.3

Date: 2026-09-10
Parent recovery run: `34488702506`

The v0.2 recovery set `output=` and `lensing=no`, but retained the committed `non linear = halofit`. CLASS input validation then stopped before background evolution because nonlinear computation requires a linear perturbation output. This is another output-request-only harness dependency.

## Frozen final recovery

Run only the exact-zero background arm again with the v0.2 settings and one additional computational-request change:

- `non linear =` (blank).

Thus arm A has `output=`, `lensing=no`, `non linear=`, `write background=yes`; physical parameters remain `beta_1=beta_2=beta_3=0`, `phi_ini_scf=0`, `phi_prime_ini_scf=0`.

No physical parameter, source equation, background precision, threshold or metric changes. Immutable parent B/C outcomes remain unchanged and must not be rerun.

Use exactly the K1 v0.1 thresholds and v0.2 combination rule. If this background-only arm passes, the combined classification is `M14_LISAGOH_CDE_K1_EXACT_REFERENCE_IMPLEMENTATION_BLOCKED` because the exact full perturbation arm already failed while the predeclared beta=0 tiny-seed full arm passed.

No physical family falsification is authorized.