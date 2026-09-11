# W04 M27 N=1 comoving-daughter support ladder preregistration v0.1

## Trigger

The density-based daughter-support diagnostic shows the same p95 relative residual (~4.4e-5) across rho_dr amplitude cuts because physical radiation density is amplified by a^-4 at early times. In contrast, the conserved/injected comoving daughter energy `D=a^4 rho_dr` has a global maximum absolute discrepancy normalized to max(D) of only ~3e-11 to 7e-10.

This indicates that the remaining N=1 discrepancy must be localized against accumulated comoving injected energy before defining any replacement reference gate. This diagnostic is exploratory attribution only; it does not change the existing failed parent gate.

## Frozen systems

Use exactly the same exact-survival and algebraically identical comoving-direct N=1 systems, cosmology, DOP853 settings, a-grid and Gamma0/H* values `{0.03,0.3,3.0}` as the preceding conditioning audits.

## Prospective D-support ladder

For each Gamma0, let `Dmax=max(D_exact,D_direct)` at a=1. Report symmetric-relative residual statistics on the six cumulative-energy supports:

- D12: `(D_exact+D_direct) > 1e-12 Dmax`
- D10: `>1e-10 Dmax`
- D08: `>1e-8 Dmax`
- D06: `>1e-6 Dmax`
- D04: `>1e-4 Dmax`
- D02: `>1e-2 Dmax`

For each support record n, earliest a, p50/p95/p99/max. Also retain the global amplitude-normalized absolute D error and H/parent p95 residuals.

## Interpretation

No single support level is an acceptance gate in this diagnostic. The output is used only to determine whether the relative discrepancy converges away as accumulated injected energy becomes numerically resolved. A later reference recovery, if justified, must be separately preregistered before it can affect M27 classification.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
