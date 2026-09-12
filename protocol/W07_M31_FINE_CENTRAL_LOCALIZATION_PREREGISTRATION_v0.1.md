# W07 M31 finer central localization preregistration v0.1

## Motivation

The first prospectively frozen M31 central-Jacobian run `34694420359` did not satisfy the derivative-convergence gate at coarse/fine steps `0.002/0.001`. This is a numerical/localization result, not a physical failure. The prior result remains immutable and is not relabeled.

This follow-up asks only whether the same two local directions become numerically stable on a smaller, prospectively frozen central stencil. Thresholds and response construction are unchanged.

## Provider and base

Pinned provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

Base M31 point:

`parameters_smg = (c_K,c_B,c_M,c_T,c_H,M2_ini) = (0.1,0.05,0.02,0,0.03,1)`.

Radial direction preserves `(c_K,c_B,c_M,c_H)=(q,0.5q,0.2q,0.3q)` with `c_T=0`, `M2_ini=1` around `q0=0.1`.

Independent direction varies only `c_T` at the base.

## Frozen finer stencil

For both radial q and c_T coordinates:

- coarse central step: `5.0e-4`;
- fine central step: `2.5e-4`.

No further step shrinking is authorized by this v0.1 protocol.

## Response and unchanged thresholds

Use the same global common-support concatenated CMB + P(k) derivative vector and base-block L2 normalizations as `W07_M30_M31_CENTRAL_LOCAL_JACOBIAN_PREREGISTRATION_v0.1`.

A derivative converges iff:

- principal angle coarse-vs-fine `<=5 deg`; and
- relative norm mismatch `<=0.25`.

Fine radial-vs-c_T directions are separated iff principal angle `>=10 deg`.

Classifications:

- both derivatives converge and separation passes: `M31_FINE_CENTRAL_LOCAL_2D_RESPONSE_RANK_EVIDENCE`;
- a derivative fails convergence: `M31_FINE_CENTRAL_LOCAL_DERIVATIVE_NOT_CONVERGED`;
- both converge but are near-collinear: `M31_FINE_CENTRAL_LOCAL_2D_RESPONSE_NEAR_COLLINEAR`;
- base/control failure: `M31_FINE_CENTRAL_LOCAL_CONTROL_BLOCKED`;
- arm/provider failure: `M31_FINE_CENTRAL_LOCAL_PROVIDER_BLOCKED`.

## Scope guard

A positive result would show only finer-scale local rank evidence. It does not erase the previous nonconvergence at larger steps, does not promote K2, and does not establish full DHOST/beyond-Horndeski covariant geometry, quotient structure, stability domain or observational distinction. Always keep `K2_promoted=false` and `physical_falsification=false`.
