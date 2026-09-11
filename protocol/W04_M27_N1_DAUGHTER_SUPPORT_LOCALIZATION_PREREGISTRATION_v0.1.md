# W04 M27 N=1 daughter-radiation support localization preregistration v0.1

## Trigger

The comoving-variable N=1 conditioning audit leaves H and parent residuals at ~1e-13--1e-11 but daughter-radiation p95 symmetric-relative residuals near 4.4e-5 for all Gamma0/H* = 0.03, 0.3, 3.0. Because the daughter density starts exactly at zero, a relative metric may be dominated by early points with vanishingly small physical amplitude even when the absolute energy-transfer solution agrees.

This diagnostic localizes the residual. It does **not** alter or retroactively relax the frozen 1e-7 parent reference gate.

## Frozen systems

Reuse the same exact-survival N=1 representation and algebraically identical comoving direct N=1 system from the conditioning audit, with identical DOP853 tolerances, cosmology, a-grid, and Gamma0 values.

## Prospectively frozen diagnostic support slices

For each Gamma0/H* in {0.03,0.3,3.0}, define `rho_dr,max` as the maximum of the two daughter solutions. Evaluate daughter residuals on four independently reported support slices:

- S20: `(rho1+rho2) > 1e-20 * max(rho_dr,max,1)` (the original parent mask);
- S16: `(rho1+rho2) > 1e-16 * rho_dr,max`;
- S12: `(rho1+rho2) > 1e-12 * rho_dr,max`;
- S08: `(rho1+rho2) > 1e-8 * rho_dr,max`.

For each slice record p50, p95, p99, maximum symmetric-relative residual, earliest scale factor, and number of points.

Also record an amplitude-normalized absolute metric over all points:

`max |rho1-rho2| / max(rho_dr,max,1e-300)`

and the same metric for comoving daughter D.

## Interpretation labels

- `EARLY_NULL_RELATIVE_METRIC_LOCALIZED` if S20 p95 exceeds 1e-7 but S12 and S08 p95 are <=1e-7 and the global amplitude-normalized absolute daughter error is <=1e-8.
- `PERSISTENT_DAUGHTER_DISCREPANCY` if S12 or S08 p95 remains >1e-7.
- `NUMERICAL_BLOCKED` on solver failure.

These are diagnostic labels only. No K1/K4 promotion and no physical falsification may follow directly from this audit.
