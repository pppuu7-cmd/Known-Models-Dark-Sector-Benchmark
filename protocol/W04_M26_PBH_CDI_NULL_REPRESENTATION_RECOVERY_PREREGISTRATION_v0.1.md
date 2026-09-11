# W04 M26 PBH CDI null-representation recovery preregistration v0.1

## Trigger

The M26 CLASS CDI transfer run `34552202481` executed the adiabatic reference and all four positive-fraction CDI cases successfully for every tested mass (100, 1000, 10000 Msun). Only the explicit mixed-mode null case failed. CLASS rejects an enabled primordial CDI mode with exactly zero auto-amplitude (`one_amplitude <= 0`).

This is a provider representation boundary: the physical zero-CDI limit is represented by omitting the CDI mode, not by enabling it with `f_cdi=0`.

## Frozen recovery

Do not recompute any CLASS case. Reuse the immutable mass artifacts from run `34552202481`.

For each mass:

- use the already successful pure adiabatic `ref` output as the provider-valid exact null representation;
- retain all already computed finite cases `f0..f3` unchanged;
- do not alter the PBH-to-CDI amplitude mapping, mass/fraction grid, cosmology, CLASS pin, k-window, plateau-slope criterion, fraction-scaling criterion, or mass-scaling criterion.

The failed explicit zero run remains in provenance and is recorded as `EXPLICIT_ZERO_UNSUPPORTED_BY_PROVIDER`; it is not interpreted as a physical failure.

## Gates

For each mass, evaluate only the prospectively frozen finite-case gates from `W04_M26_PBH_CDI_TRANSFER_GATE_PREREGISTRATION_v0.1.md`:

- positive high-k Delta P;
- high-k plateau log-slope |slope| <= 0.15;
- fraction scaling exponent within 0.05 of 1.

The exact-null gate is satisfied by provider representation semantics only if the pure adiabatic reference contains no CDI mode and is the same cosmological reference used for all finite cases.

Aggregate mass scaling remains within 0.05 of 1 at every positive fraction.

## Classification

Per mass: `M26_PBH_CDI_TRANSFER_PASS_WITH_PROVIDER_NULL_SCOPE` if all finite gates pass and null omission provenance is valid.

Aggregate: `M26_PBH_CDI_TRANSFER_MASS_FRACTION_PASS_WITH_PROVIDER_NULL_SCOPE` if all three mass branches and all mass-scaling gates pass.

This remains transfer-level scoped evidence. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`; observation-space validation remains open.
