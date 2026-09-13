# W03 M13b K3D2-B post-handoff ULP seam recovery v0.1

Frozen: 2026-09-14 after run 34787682303 and before any ULP-seam numerical result is inspected.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Parent: `protocol/W03_M13B_K3D2B_CONDITIONAL_RESTART_FLOATING_BOUNDARY_RECOVERY_v0.1.md`.

## Established facts

The conditional disabled-adapter path passes its strict null regression: both CLASS runs return zero, H0 relative difference is exactly zero, and normalized P(k) L2 is `5.350776836980277e-16`, below the frozen `1e-10` gate.

For the enabled qcf+qpf path, the recovered first NDF15 segment now reaches the exact `loga_handoff=log(1/6)` endpoint. The second NDF15 segment fails when it starts at that same coordinate because the isolated endpoint is owned by the frozen-left branch while immediately later points are post-handoff. The failure is therefore localized to the numerical seam at the second-segment initial coordinate; B1/B2/B3 remain unevaluated.

## Recovery definition

The first segment remains exactly `[loga_ini, loga_handoff]` and ends with the same state vector.

The second segment starts at the smallest representable floating-point coordinate strictly greater than `loga_handoff`, generated only by `nextafter(loga_handoff, loga_final)`. The state vector is **not evolved, interpolated, reset, fitted or otherwise altered** between segments.

Two prospectively fixed enabled lanes are required:

- U1: one `nextafter` step after the handoff;
- U2: two repeated `nextafter` steps after the handoff.

The purpose of U2 is sensitivity control. It is not a second candidate to choose from after seeing results.

The disabled qcf/qpf branch retains the untouched one-call upstream NDF15 path. The four background guards remain `a <= exp(log(1./6.))`. No perturbation code is changed by this recovery.

## Frozen implementation gates for U1 and U2

Each lane must satisfy:

- build succeeds;
- provider return code is zero;
- stdout+stderr contain neither `step size too small` nor `stepsize underflow`;
- exactly one finite positive-H background table is produced;
- samples exist below and above `a=1/6`;
- z=5 interpolation satisfies `|phi-0.92| <= 2e-4`, `|psi-1.02| <= 2e-4`, `|dphi/dN| <= 2e-3`, `|dpsi/dN| <= 2e-3`.

These are the same implementation-only handoff gates as the parent recovery. Crossing/today physics is still not evaluated here.

## Frozen U1/U2 sensitivity gates

Interpolate both successful backgrounds on the common native scale-factor domain and compare the directly exposed qfield background quantities. Require:

- relative H difference at a=1 <= `1e-10`;
- absolute differences at a=1 in phi, psi, dphi/dN and dpsi/dN each <= `1e-8`;
- maximum over a fixed 257-point uniform grid in ln(a), restricted to `a >= 1/6`, of the normalized state distance

  `sqrt((dphi)^2+(dpsi)^2+(d(dphi/dN))^2+(d(dpsi/dN))^2) / max(1, sqrt(phi^2+psi^2+(dphi/dN)^2+(dpsi/dN)^2))`

  <= `1e-7`;
- maximum relative H difference on the same grid <= `1e-8`.

No threshold may be relaxed retrospectively.

## Classification

If both lanes and all sensitivity gates pass:

`M13B_K3D2B_POST_HANDOFF_ULP_SEAM_IMPLEMENTATION_PASS_WITH_SCOPE`.

This authorizes a separately frozen full K3D2-B regression using **U1**, the minimal representable post-handoff coordinate. U2 remains only a sensitivity witness.

Otherwise:

`M13B_K3D2B_POST_HANDOFF_ULP_SEAM_BLOCKED`.

K3 remains PARTIAL. K4/K5 remain closed. No author-code reproduction or physical falsification is claimed.
