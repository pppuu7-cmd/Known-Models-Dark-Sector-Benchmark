# W03/W06 M15 — Scherrer provider output-location recovery v0.1

Status: **FROZEN AFTER ORIGINAL PROVIDER-CONTROL FAILURE, BEFORE RECOVERY RUN**

The original provider-control run `34430588917` is preserved as `SCHERRER_PROVIDER_CONTROL_FAIL_EXAMPLE`: build exit 0, author `hi.ini` exit 0, but the harness found no `output/hi*` files.

The preserved author-run log states `Writing output files in output/test_...`. Independent inspection of the exact unmodified `Cuadratico/hi.ini` confirms the explicit line:

`root = output/test_`

Therefore the original failure was caused by the KMDSB harness looking under the wrong output prefix. No Scherrer physical, stability, precision, shooting or cosmological parameter is changed in this recovery.

## Frozen recovery

1. Clone the same exact provider commit `f3f010e1ed74c86ce6a431a435fa93988f749ee2`.
2. Build the same `Cuadratico/class` binary.
3. Delete pre-existing `Cuadratico/output/test_*` products.
4. Run the same author-supplied `Cuadratico/hi.ini` unmodified.
5. Require run exit 0.
6. Require fresh `output/test_*` products after the run, including at minimum `test_background.dat` and one matter-power file if those products are written by the unmodified configuration.
7. Preserve exact file list and SHA256 values.

Terminal classes:
- `SCHERRER_OUTPUT_RECOVERY_PASS`
- `SCHERRER_OUTPUT_RECOVERY_FAIL_BUILD`
- `SCHERRER_OUTPUT_RECOVERY_FAIL_RUN`
- `SCHERRER_OUTPUT_RECOVERY_FAIL_FRESH_OUTPUT`

PASS only repairs the provider-control bookkeeping. It does not score K1–K9 or turn the Scherrer implementation into a DE-only M11 validation. Its bookkeeping remains unified-dark-sector because the author input sets `Omega_cdm=0` and `DM_schm=0.26`.
