# W03 M14 IDECAMB full-serialization preregistration v0.1

Date: 2026-09-10
Target: M14 coupled quintessence
Purpose: determine whether low-precision CMB text serialization is responsible for the channel-local K4 instability that remains after background diagnostic precision was increased.

## Frozen provider and physical model

- base `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- `Class_IDE=2`
- `UForm_CQ=1`
- `QForm_CQ=1`
- `alpha_quint=0.02`
- upstream coupled-quintessence background initial condition unchanged
- upstream Broyden update unchanged
- all physical background/perturbation equations and numerical tolerances unchanged
- external likelihoods disabled; theory-output mode only

## Frozen beta grid

`beta_cq = {0, 5e-8, 1e-7}`.

No step-size search is authorized.

## Only authorized source changes

1. IDECAMB background diagnostic writer:
   `write (1,'(11E15.5)')` -> `write (1,'(11ES25.15E3)')`.
2. CosmoMC `WriteTextCls` format:
   `'(1I6,*(E15.5))'` -> `'(1I6,*(ES25.15E3))'`.

These changes affect text serialization only, not the calculated theory arrays.

## Frozen response vector

- `dln rho_de(a)`
- `dln rho_c(a)`
- `dln H(a)`
- `dw(a)`
- `qhat(a)`
- `dln TT(ell)`
- `dln EE(ell)`
- `dln PP(ell)`

## Frozen K4 thresholds

For derivative vectors from `h=5e-8` and `2h=1e-7`:

- combined relative tangent-norm mismatch `<=0.10`;
- combined tangent angle `<=3.0 deg`.

The same metrics must additionally be reported separately for every channel, but per-channel metrics do not replace the already frozen combined rule.

## Pre-control values

With high-precision `.quantity` but default `E15.5` `.theory_cl` serialization:

- combined mismatch `0.009270610485819343`;
- combined angle `8.04171613320909 deg`.

Latest channel-local diagnostic on equivalent outputs:

- `dln_rho_de`: mismatch `0.05639803`, angle `4.032370 deg`;
- `dln_rho_c`: mismatch `1.9679e-8`, angle `0.000004 deg`;
- `dln_H`: mismatch `1.0453e-5`, angle `0.013925 deg`;
- `dw`: mismatch `0.1460276`, angle `6.844596 deg`;
- `qhat`: mismatch `2.2229e-8`, angle `0.000010 deg`;
- `dln_TT`: mismatch `0.3251605`, angle `49.620162 deg`;
- `dln_EE`: mismatch `0.4795108`, angle `53.559476 deg`;
- `dln_PP`: mismatch `0.3357869`, angle `41.169064 deg`.

## Predeclared interpretation

- If full serialization precision restores the combined frozen K4 pass, classify `M14_IDECAMB_K4_SERIALIZATION_ARTIFACT_CAUSAL_SUPPORT`. This remains diagnostic and does not by itself validate all solver accuracy.
- If the combined angle remains above `3 deg` but CMB channel angles fall by at least 50% in all three CMB channels, classify `M14_IDECAMB_CMB_SERIALIZATION_PARTIAL_CAUSAL_SUPPORT`; continue with solver-accuracy/tolerance audit using preregistered controls.
- If CMB channel angles remain at least 50% of their pre-control values, classify `M14_IDECAMB_FULL_SERIALIZATION_NOT_SUFFICIENT` and do not spend another iteration on text precision.
- Any build/execution/output-shape failure is implementation-blocked and carries no physical inference.

No observational claim, K5 promotion, or M14 family falsification is authorized by this diagnostic.