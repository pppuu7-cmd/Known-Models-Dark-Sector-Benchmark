# W04 M25 CLASS bridge quadrature-cap recovery preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F25 / M25 resonantly produced sterile-neutrino-like WDM
Parent bridge: run `34545741673`, result commit `2f460716a0b2af96d0fac671a65066f609e6a543`
Parent classification: `M25_CLASS_BRIDGE_BLOCKED_CLASS_PROVIDER`
Sterile-production provider: `ntveem/sterile-dm@e4486265e8207aa0dd28decc8c8d897266c0a52a`
Boltzmann provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Purpose
Recover the already-preregistered M25 nonthermal-PSD density bridge from a provider numerical-capacity failure without changing the physical model, source-derived PSD transform, quadrature tolerance, cosmology, or scientific acceptance thresholds.

The parent run reached CLASS `background_ncdm_init` but `get_qsampling` failed to reach the provider-default relative tolerance `tol_ncdm_bg=1e-5` with the compiled background quadrature cap of 800 points. The provider error explicitly identifies increasing `_QUADRATURE_MAX_BG_` as a numerical-capacity remedy. This parent result is infrastructure/numerical-provider BLOCKED and is not a physical M25 failure.

## Frozen recovery intervention
Keep the exact CLASS source pin and change only the compile-time numerical capacity:

`_QUADRATURE_MAX_BG_: 800 -> 4000`

The workflow must verify that the pinned source contains exactly the expected `#define _QUADRATURE_MAX_BG_ 800` token before replacement and exactly the `4000` token afterward. No other CLASS source line may be intentionally modified.

Forbidden changes:
- do not relax `tol_ncdm_bg` or any other tolerance;
- do not change `_QUADRATURE_MAX_` for perturbations;
- do not smooth, extrapolate, resample, clip, renormalize, or otherwise alter the two upstream PSDs;
- do not change q mapping, mass, temperature ratio, degeneracy, cosmology, or `omega_ncdm` anti-hiding rule;
- do not pass `omega_ncdm` / `Omega_ncdm`;
- do not change the original 1% density gate or factor-of-two negative-control gate.

This is a one-shot recovery profile. If 4000 background abscissae still fail to satisfy the unchanged `1e-5` internal CLASS requirement, record a blocker; do not increase the cap again within this protocol.

## Frozen bridge science
Reuse `verification/m25/m25_class_bridge.py` and the immutable upstream artifact from provider-control run `34544624039` unchanged.

For each of the same two stock PSDs require the original gates:
1. valid strictly increasing q and nonnegative finite `f0`;
2. `|omega_CLASS - omega_provider| / omega_provider <= 0.01`;
3. `1.98 <= omega_sum / omega_average <= 2.02` for the deliberate doubled-PSD negative control;
4. both stock models pass.

## Frozen classification
- CLASS cannot build or `get_qsampling` still cannot converge at cap 4000: `M25_CLASS_BRIDGE_QMAX4000_BLOCKED`.
- CLASS executes but any original density/negative-control gate fails: `M25_CLASS_BRIDGE_QMAX4000_DENSITY_NOT_VALIDATED`.
- Both stock models pass every original gate: `M25_CLASS_BRIDGE_QMAX4000_DENSITY_VALIDATED`.

Always:
- `physical_falsification=false`;
- this recovery alone does not count as family-terminal coverage;
- `K1_promoted=false` inside this bridge result.

Only `M25_CLASS_BRIDGE_QMAX4000_DENSITY_VALIDATED` authorizes a new prospective M25 K1/reference-limit protocol. It does not itself establish K1.

## Interpretation guardrail
A PASS means the source-derived nonthermal PSD normalization is transportable into CLASS once the provider's fixed quadrature-capacity ceiling is removed while keeping its accuracy tolerance unchanged. It does not mean resonantly produced sterile-DM is preferred, excluded, or observationally distinguishable from thermal WDM.