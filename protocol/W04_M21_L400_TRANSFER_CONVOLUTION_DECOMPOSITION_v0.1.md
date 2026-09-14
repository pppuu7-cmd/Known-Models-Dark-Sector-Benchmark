# W04 M21 l=400 transfer-convolution decomposition v0.1

Frozen: 2026-09-15 after terminal k-support map `M21_L400_K_SUPPORT_MAPPED_WITH_SCOPE` and before any new source/radial/convolution diagnostic values are generated.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Parent authority

Required canonical parents:

- `M21_L400_TRANSFER_VS_HARMONIC_RECOVERY_TERMINAL.json` class `M21_L400_SPIKE_PRESENT_IN_E_TRANSFER_KERNEL_WITH_SCOPE`;
- `M21_L400_K_SUPPORT_MAPPING_TERMINAL.json` class `M21_L400_K_SUPPORT_MAPPED_WITH_SCOPE`.

Frozen active support:

- l = 400 only;
- k05 = `0.03030247505892471` Mpc^-1;
- k95 = `0.04401375054733766` Mpc^-1;
- parent excess weight is the already-defined non-negative `W(k)` from the k-support protocol.

## Exact source path

On the exact provider pin, scalar E transfer computation maps `index_tt_e` to the polarization perturbation source and calls `transfer_integrate()`.

For non-Dirac sources `transfer_integrate()`:

1. reads the prepared transfer source array `ptw->sources` and coordinate `ptw->tau0_minus_tau`;
2. determines the Bessel-overlap endpoint `index_tau_max`;
3. calls `transfer_radial_function()` for the selected l/k and radial type `SCALAR_POLARISATION_E`;
4. calls `array_trapezoidal_convolution(sources, radial_function, ..., w_trapz, trsf)`;
5. optionally applies the exact Bessel-edge triangle correction.

Thus the full native transfer value can be reconstructed from the dumped source, radial function, trapezoidal weights and correction.

## Output-only instrumentation

Patch exact `source/transfer.c` only. The patch is enabled only by environment variable `KMDSB_M21_L400_CONV_DIAG` and only when all are true:

- scalar mode;
- `index_tt == ptr->index_tt_e`;
- direct l exactly 400;
- `k05 <= k <= k95`.

After the native convolution and Bessel correction have already completed, write rows containing:

`index_q, k, index_tau, tau0_minus_tau, source, radial, w_trapz, source*radial*w_trapz, transfer_final, bessel_edge_correction, index_tau_max, tau0_minus_tau_min_bessel`.

The patch MUST NOT modify CLASS arrays, transfer values, precision, q/l grids, sources, radial kernels, weights, or integration order. I/O must be serialized with an OpenMP critical region to avoid interleaved diagnostic writes.

## Frozen execution

Use one already-authoritative HIGH layout only: `P400_ON_TAIL_OFF`. The prior A/B transfer diagnostics are numerically identical at direct l=400 and have identical k-support; this gate decomposes that shared l=400 transfer computation rather than retesting sparse-l layout dependence.

Execute physical cases in **four independent parallel jobs**:

`ref, f2, f3, f4`.

Each job:

- uses exact `mixed_cold_warm_k1_reference.py` physical input for its case;
- uses exact existing `P400_ON_TAIL_OFF` precision profile construction;
- uses the same provider pin;
- has CLASS timeout 2700 s and job timeout 55 min;
- downloads immutable parent A artifact from run `34887488405` and requires new full `cl.dat` normalized L2 difference <= `1e-12` for its case.

## Frozen diagnostic integrity

For every dumped `(case,index_q)` block:

- at least 20 tau rows must exist;
- `index_tau` must be consecutive from 0 through `index_tau_max`;
- k must lie inside the frozen support;
- reconstruct
  `Delta_recon = sum(source*radial*w_trapz) + bessel_edge_correction`;
- require relative difference from `transfer_final` <= `1e-10`.

Across cases require the same set of support `index_q` values. At a common `index_q`, require relative k difference from reference <= `1e-6`; otherwise BLOCK rather than silently pairing unrelated q nodes.

These are diagnostic integrity gates, not scientific thresholds.

## Frozen profile comparison

For each common `index_q`, use reference `u = tau0_minus_tau` rows within the strict overlap of all four cases. Interpolate the other cases linearly in u onto the retained reference u nodes. Require at least 20 common u nodes.

Compare three profile quantities:

- `S`: source;
- `R`: radial function;
- `P`: pointwise unweighted product `source*radial`.

For X in `{S,R,P}`, case c in `{f2,f3,f4}`, and q-index j define

`D_X(c,j) = ||X_c-X_ref||_2 / max(||X_ref||_2,1e-300)`.

Use the immutable parent l=400 transfer diagnostic to reconstruct the frozen parent excess weight at the same q indices:

`W_j = max(r_f3(j)^2 - max(r_f2(j)^2,r_f4(j)^2),0)`

where `r_c = Delta_E_c - Delta_E_ref`.

Define support-weighted amplitudes

`A_X(c) = sqrt( sum_j W_j D_X(c,j)^2 / sum_j W_j )`

and specificity

`E_X = A_X(f3) / max(A_X(f2),A_X(f4),1e-300)`.

Reuse the established specificity boundary `E > 3`.

Also report, without changing classification, per-q E_X values, maxima, medians, and the weighted-contribution profile using native `source*radial*w_trapz` on each case grid.

## Frozen classification

After all integrity and non-interference gates pass:

- `E_S > 3` and `E_R <= 3` -> `M21_L400_TRANSFER_SPIKE_SOURCE_PROFILE_LOCALIZED_WITH_SCOPE`;
- `E_R > 3` and `E_S <= 3` -> `M21_L400_TRANSFER_SPIKE_RADIAL_KERNEL_LOCALIZED_WITH_SCOPE`;
- `E_S > 3` and `E_R > 3` -> `M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE`;
- `E_S <= 3`, `E_R <= 3`, but `E_P > 3` -> `M21_L400_TRANSFER_SPIKE_SOURCE_RADIAL_INTERACTION_WITH_SCOPE`;
- `E_S <= 3`, `E_R <= 3`, `E_P <= 3`, while parent transfer localization remains valid -> `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`;
- any provider/input/profile/null/table/reconstruction/q-index integrity failure -> `M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED`.

## Interpretation ceiling

This is a numerical mechanism localization inside the scalar-E transfer calculation. It does not establish a CLASS defect, a production precision profile, a physical warm-dark-matter scale, K1/K3/K4 promotion, or physical validation/falsification.
