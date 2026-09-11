# W05 M29 Brans-Dicke K4 numerical-robustness preregistration v0.1

Date: 2026-09-11
Provider: `hiclass-code/hi_class_public` commit `0009f51d89e6465c79e570b496c66fc90058fa77`.
Prerequisite evidence: M29 K0 PASS_WITH_SCOPE and M29 K1 GR-limit PASS_WITH_SCOPE.
K3 gauge closure is separately provider-blocked and is not silently treated as PASS.

## Frozen model points

Test two supported synchronous-gauge Brans-Dicke points:

- `omega_BD=15` (the shipped author/example point; strong finite modification),
- `omega_BD=1e4` (GR-approach point already inside the validated K1 ladder).

All other Brans-Dicke conventions remain those of the shipped `gravity_models/brans_dicke.ini` including `M2_tuning_smg=yes`, `M2_today_smg=1`, `phi_ini=1`, `phi_prime_ini=0`, and the shipped early-time settings.

## Frozen precision profiles

Independent matrix arms, `fail-fast:false`:

1. `default`: shipped Brans-Dicke example unchanged except root/omega.
2. `dense_bg`: add `background_Nloga=40000` while keeping default perturbation/CMB precision.
3. `permille`: `background_Nloga=40000` plus provider `cl_permille.pre`.
4. `ref`: `background_Nloga=40000` plus provider `cl_ref.pre`.

`ref` is the frozen numerical reference, not a physical truth model.

## Frozen observables and metric

Compare on common support using interpolation with no zero-filling:

- background H column (`background.dat`, x column 0, H column 3),
- CMB TT (`cl.dat`, ell column 0, TT column 1),
- linear P(k) (`pk.dat`, k column 0, P column 1).

Use symmetric relative error `2|x-y|/(|x|+|y|+1e-300)` and record max and RMS.

## Frozen K4 acceptance

For **both** omega points:

- every profile exits 0 and yields finite common support;
- `permille` versus `ref` TT: max <= `5e-3`, RMS <= `1e-3`;
- `permille` versus `ref` P(k): max <= `1e-3`, RMS <= `5e-4`;
- `permille` versus `ref` background H: max <= `1e-4`, RMS <= `5e-5`;
- RMS error relative to `ref` must not increase from `dense_bg` to `permille` by more than 20% in any channel.

The `default` profile is diagnostic: it quantifies the known SMG background-sampling floor but is not required to be monotonically worse than every refined profile.

If runs are finite but the frozen precision criteria fail, classify `M29_K4_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS`; this is not physical falsification. Provider/infrastructure failure is classified separately. K4 PASS does not override the independent K3 provider block.