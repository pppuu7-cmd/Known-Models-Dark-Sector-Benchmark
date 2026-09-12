# W07 M33 noise-safe K1 confirmation implementation lock v0.1

Date: 2026-09-12
Parent protocol: `protocol/W07_M33_NOISE_SAFE_K1_CONFIRMATION_v0.1.md`.

This file freezes implementation details that were not numerically specified in the parent protocol. It does not change any arm, threshold, provider pin, stability profile, or interpretation rule.

## Strict-vs-safe no-dynamics-change metric
At `Omega_smg=0.01`, compare strict `D_safe_smg=0` against safe `D_safe_smg=1e-100`.

CMB normalized-L2: intersect exact integer ell rows, retain all common finite numerical C_l columns after ell, flatten them, and compute `||safe-strict||_2 / ||strict||_2`. P(k) normalized-L2: retain the strict P(k) grid only within the overlapping finite k support, linearly interpolate safe P(k) only inside that overlap, and compute `||safe-strict||_2 / ||strict||_2`. Zero denominator, nonfinite data, missing support, or either nonzero solver exit blocks the confirmation. Each metric must be `<=1e-12` exactly as preregistered.

## K1 ladder implementation
Only after the strict-vs-safe control passes, invoke the repository-standard `verification/k1/decoupling_ladder.py` unchanged on safe arms ordered `0.01,0.005,0.002,0.001` versus the explicit GR control. The analyzer output is evidence only; this workflow never edits canonical matrices and always reports `K1_promoted=false`.
