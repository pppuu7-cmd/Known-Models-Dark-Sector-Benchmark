# W04 M25 K1 high-precision quadrature-capacity recovery preregistration v0.1

Status: **FROZEN BEFORE RECOVERY EXECUTION**

## Trigger

The first `pk_ref.pre` precision-floor diagnostic jobs for both frozen sterile-neutrino PSD shapes (`m0`, `m1`) built CLASS successfully and ran the pure-CDM reference, but every ncdm tail case stopped in `background_ncdm_init -> get_qsampling` because the official high-precision profile requests `tol_ncdm = 1e-10` while the pinned CLASS source limits the non-background quadrature to `_QUADRATURE_MAX_ = 250` points.

The solver error explicitly recommends increasing `_QUADRATURE_MAX_` as the last-resort capacity repair when the required tolerance cannot be reached with the fixed maximum number of points. The same pinned source defines `_QUADRATURE_MAX_BG_ = 800`; the original M25 K1 workflow already used the audited capacity-only repair `_QUADRATURE_MAX_BG_: 800 -> 4000` without changing the tolerance.

This recovery extends the same capacity-only principle to the perturbation/non-background ncdm quadrature.

## Frozen mechanical repair

At CLASS commit `e85808324f51fc694d12e3ed7439552a3c3f9540`, change only:

- `_QUADRATURE_MAX_`: `250 -> 4000`
- `_QUADRATURE_MAX_BG_`: `800 -> 4000` (same already-used M25 infrastructure repair)

No tolerance is relaxed. In particular all `cl_ref.pre` / `pk_ref.pre` precision settings, including `tol_ncdm_bg = 1e-10` and `tol_ncdm_synchronous/newtonian = 1e-10`, remain unchanged.

No PSD, cosmology, abundance, eta, observable, output range, residual definition, gate threshold, or scientific interpretation is changed.

## Frozen execution

Repeat the same four independent precision-floor jobs from `W04_M25_K1_PRECISION_FLOOR_DIAGNOSTIC_PREREGISTRATION_v0.1.md`:

- `m0 x cl_ref`
- `m0 x pk_ref`
- `m1 x cl_ref`
- `m1 x pk_ref`

Use the exact physical case files from original M25 K1 run `34548988620`, artifact `10180157389`, recomputing only pure-CDM reference plus eta `0.01, 0.003, 0.001` tail points.

The four matrix jobs are independent. Inside each job, reference/e2/e3/e4 have unique output roots and may run at most two-at-a-time.

## Frozen analysis

Use `verification/m25/m25_k1_precision_floor_diagnostic.py` unchanged. Therefore all support sorting, p95 residuals, 2% monotonic slack, smallest-vs-largest condition, and tail exponent `p > 0.5` gates remain exactly as preregistered.

## Interpretation

Allowed profile classifications are unchanged:

- `M25_PRECISION_FLOOR_TAIL_SCALING_RECOVERED`
- `M25_PRECISION_FLOOR_TAIL_SCALING_PARTIAL`
- `M25_PRECISION_FLOOR_TAIL_SCALING_NOT_RECOVERED`
- `M25_PRECISION_FLOOR_DIAGNOSTIC_PROVIDER_BLOCKED`

All outcomes retain `K1_promoted = false`, `K4_promoted = false`, and `physical_falsification = false`.

Only if `pk_ref` recovers all target tail blocks for both PSD shapes may a later separately preregistered full five-point K1 confirmation be launched.
