# M14 IDECAMB K4 channel-geometry audit

Date: 2026-09-10
Status: `CMB_AND_SCALAR_CHANNEL_INSTABILITY_LOCALIZED`
Physical falsification: **NO**

## Input

The coupling-aware-inner-IC diagnostic reproduced the previous high-precision-background combined K4 result almost exactly:

- relative tangent-norm mismatch: `0.009270617806507004`;
- combined angle: `8.041717531178694 deg`;
- frozen limits: mismatch `<=0.10`, angle `<=3 deg`.

Since both the corrected-Broyden diagnostic and the coupling-aware background-IC diagnostic left the combined angle essentially unchanged, the raw response vectors from the latest successful run were decomposed channel by channel without changing any model parameter or threshold.

The derivative comparison remains `h=5e-8` versus `2h=1e-7` at `alpha=0.02`.

## Channel-local K4 geometry

| channel | relative norm mismatch | tangent angle (deg) | fine-step max abs response |
|---|---:|---:|---:|
| `dln_rho_de` | `0.05639803` | `4.032370` | `6.952538e-4` |
| `dln_rho_c` | `1.9679e-8` | `0.000004` | `6.506409e-9` |
| `dln_H` | `1.0453e-5` | `0.013925` | `2.678329e-9` |
| `dw` | `0.1460276` | `6.844596` | `5.811729e-4` |
| `qhat` | `2.2229e-8` | `0.000010` | `2.971291e-9` |
| `dln_TT` | `0.3251605` | `49.620162` | `9.536980e-5` |
| `dln_EE` | `0.4795108` | `53.559476` | `6.322911e-5` |
| `dln_PP` | `0.3357869` | `41.169064` | `8.523333e-5` |

This shows that the combined `~8 deg` failure is not a uniform failure of the coupled-quintessence response. The CDM density, Hubble and normalized interaction channels are directionally stable at this step size; the strongest failures are in the CMB spectra, with weaker but still frozen-threshold failures in scalar-field `rho_de` and `w(a)`.

## Newly identified serialization asymmetry

The previous diagnostic-precision audit changed the IDECAMB `.quantity` writer from `11E15.5` to `11ES25.15E3`, but it did **not** change the CosmoMC CMB theory writer.

In the pinned CosmoMC base `source/CosmoTheory.f90`, `WriteTextCls` defines

`character(LEN=*), parameter :: fmt = '(1I6,*(E15.5))'`

and writes every `theory_cl` row with that format.

Therefore the current K4 vector combines high-precision background diagnostics with lower-precision CMB text serialization. Because the nonzero CMB response is only of order `1e-5` to `1e-4` in fractional amplitude on the fine step, the CMB finite-difference direction must be retested before its `40-54 deg` channel angles can be interpreted as solver/physics non-convergence.

## Authorized next diagnostic

Run the exact upstream physical model and frozen beta grid with **only** these output-format changes:

- IDECAMB `.quantity`: `11E15.5 -> 11ES25.15E3`;
- CosmoMC `.theory_cl`: `(1I6,*(E15.5)) -> (1I6,*(ES25.15E3))`.

Keep the upstream coupled-quintessence IC and upstream Broyden update unchanged. Report combined and per-channel K4 geometry.

No scientific-provider promotion, observational claim, or family falsification is authorized from serialization diagnostics alone.