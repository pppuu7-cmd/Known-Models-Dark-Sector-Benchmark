# W03/M07 — gauge-response subtraction-floor audit

Date: 2026-09-09  
Status: **B2 PARTIAL — raw physical outputs pass paired-gauge regression; reconstructed lnP residual fails frozen response gate and does not converge away under stronger precision**

## Scope

Canonical M07 branch under pinned official CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`, lambda=0.075, q=lambda^2 local branch, matched LambdaCDM reference.

Internal solver gauges compared:
- synchronous;
- Newtonian.

Output conventions in both runs:
- `matter_source_in_current_gauge=no`;
- `get_perturbations_in_current_gauge=no`.

Thus the comparison targets physical/gauge-transformed output quantities rather than intentionally gauge-specific source variables.

Frozen gates before first result:
- raw `P,d_m,phi,psi` max symmetric relative difference <= `1e-4`;
- reconstructed `r_Delta=ln(P_M07/P_ref)` cross-gauge L2 relative difference <= `5e-3`.

The response threshold is not relaxed after seeing the result.

## First paired-gauge audit

Run: `34360101877`.

All raw outputs passed the `1e-4` gate. Representative maxima:
- reference P: `7.67283e-5`;
- M07 P: `7.67701e-5`;
- d_m: about `3.84e-5`;
- phi/psi: about `4.14e-5`.

But the small derived residual gave:

`||r_sync-r_newt|| / max(||r_sync||,||r_newt||) = 0.0309915691`

with absolute L2 residual mismatch

`2.04751426e-5`.

This failed the frozen `5e-3` response gate.

### Common-mode diagnosis

Gauge-error norms in log P:
- reference: `1.95830488e-4`;
- M07: `1.96986624e-4`;
- difference of those gauge errors: `2.04751426e-5`;
- cosine(reference gauge error, M07 gauge error): `0.9945834851`.

Therefore most of the internal-gauge numerical error is common-mode, but the M07-minus-reference subtraction amplifies the small non-common remainder relative to the physical residual itself.

## High-precision convergence audit

Run: `34371774424`.
Artifact digest: `sha256:56498b65951dacefbd5f7dc6e116c611b7cb36aa8a2b0cc148cb18efcb826c5e`.

No physical parameter or gate was changed. Numerical settings were tightened to:
- `tol_perturbations_integration=1e-10`;
- `perturbations_sampling_stepsize=0.002`;
- `k_per_decade_for_pk=80`;
- `k_per_decade_for_bao=80`;
- shooting remained `tol_shooting_deltax_rel=1e-13`.

The original response gate remained `5e-3`.

Result:
- raw physical outputs again pass `1e-4`;
- response L2 relative mismatch = `0.02975665236`;
- absolute response mismatch = `1.96128419e-5`;
- reference logP gauge-error norm = `1.95942962e-4`;
- M07 logP gauge-error norm = `1.96917316e-4`;
- error cosine = `0.9950276201`.

The response mismatch improved by only about 4% (`0.03099 -> 0.02976`) despite the substantial precision increase. The frozen `0.005` gate therefore remains failed.

## Interpretation

This is **not evidence that canonical quintessence is physically gauge dependent**. The raw physical outputs regress across gauges within the frozen tolerance.

It is evidence that the particular small residual

`ln(P_M07/P_LambdaCDM)`

has a persistent cross-gauge numerical subtraction floor of order `2e-5` in absolute L2 norm in this implementation/scope. Because the physical residual norm at lambda=.075 is only about `6.5e-4`, that floor is about 3% of the residual.

Consequences:
1. B2 remains `PARTIAL`, not PASS and not physical FAIL.
2. Production response convention remains explicitly pinned to synchronous internal gauge.
3. The measured cross-gauge floor must be carried as a numerical systematic in later B5/B7 interpretation.
4. A model/residual smaller than this floor cannot obtain mechanism-level significance from this response channel without an improved independent formulation.
5. Further blind precision tightening is not justified by the observed convergence plateau.

## Methodology lesson

Gauge invariance of the underlying observable does not guarantee arbitrary precision of a *difference of two nearly identical numerical solutions*. Residual reconstructions need their own numerical/gauge-floor audit after reference subtraction.

This audit generates design prior DP-0809.
