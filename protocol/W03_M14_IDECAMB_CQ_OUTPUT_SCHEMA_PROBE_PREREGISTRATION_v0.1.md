# W03 M14 IDECAMB CQ output-schema probe preregistration v0.1

Status: FROZEN BEFORE EXECUTION
Date: 2026-09-10

Purpose: expose the provider's own diagnostic/theory output schema for the executable coupled-quintessence path before defining any K1 numerical metric or tolerance.

Providers:
- cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4
- liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075 overlay

Starting input: pinned author `test_ide.ini`.

Frozen edits only:
1. documented selector `Class_IDE = 1` -> `Class_IDE = 2`;
2. diagnostic reference point `param[beta_cq]= 0` (the provider source makes the EXP coupling proportional to beta);
3. enable the author-documented/commented test-output hook as `test_output_root = m14_cq_beta0`.

All other physics, likelihood, numerical and cosmological settings remain as in the author input. Existing compiler compatibility flag `-fallow-argument-mismatch` is allowed as build-only plumbing.

Outputs to preserve without interpretation:
- exact edited ini and diff;
- stdout/stderr and exit code;
- every fresh file whose basename starts with `m14_cq_beta0`;
- first/last data lines and detected numeric column count for each text output.

This probe cannot promote K1-K9/B4-B9. No thresholds or decoupling claims are permitted from its result. After the schema is known, define a separate prospective K1 regression with exact observables and tolerances.
