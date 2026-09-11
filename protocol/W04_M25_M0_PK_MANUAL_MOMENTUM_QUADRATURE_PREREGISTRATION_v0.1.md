# W04 M25 m0 P(k) manual momentum-quadrature diagnostic preregistration v0.1

## Trigger

M25 m0 CMB residuals have been localized to a stable `l_logstep` numerical floor, while the P(k) block remains separately unresolved and is unchanged by CMB multipole sampling. The pinned CLASS automatic ncdm momentum integration uses `tol_ncdm`; manual quadrature is available via `ncdm_quadrature_strategy`, with `qm_trapz=3`, `ncdm_N_momentum_bins`, and `ncdm_maximum_q`.

The frozen sterile-provider PSD used by m0 e2/e3/e4 has 1000 tabulated samples with q support approximately `[0.0005033701435, 10.0673978363]`. In pinned CLASS, finite trapezoidal manual sampling evaluates q at `qmax/N, 2 qmax/N, ..., qmax`. Therefore choosing qmax=10.0 and N up to 4000 keeps every evaluated point inside provider support. No provider extrapolation is allowed.

## Frozen profiles

Use pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`, quadrature compile capacities 4000/4000, original m0 e2/e3/e4 PSD/cosmology cases, and common source-matched settings:

- `tol_ncdm_bg=1e-6`
- `tol_ncdm=1e-6`
- `ncdm_fluid_approximation=3`
- `ncdm_quadrature_strategy=3`
- `ncdm_maximum_q=10.0`
- `ncdm_N_momentum_bins = {500,1000,2000,4000}`

Run the four bin counts as independent matrix jobs with fail-fast=false. Restrict requested observables to `mPk` plus the automatically written background; CMB output is intentionally omitted because this gate is P(k)-only. The reference LCDM P(k)/background is copied byte-for-byte from the immutable original run 34548988620 and is not recomputed.

## Frozen per-point analysis

Use the same symmetric-relative p95 metric and eta ladder `{0.01,0.003,0.001}` as the existing M25 K1 precision-floor diagnostic, but evaluate only H and P(k). Record H tail scaling, P(k) r95 values, exponent and original tail-scaling Boolean.

A manual point is admissible only if all three runs execute and H tail scaling is recovered.

## Frozen aggregate gates

Let the 2000- and 4000-bin P(k) r95 triplets be the fine pair.

- `fine_bin_stability`: symmetric relative difference between N=2000 and N=4000 is <=0.25 for each of the three eta-specific P(k) r95 values.
- `fine_floor_flatness`: at N=4000, `max(r95)/min(r95) <= 2.0`.
- `auto_manual_fine_agreement`: compare the N=4000 r95 triplet with the source-matched automatic-quadrature baseline from run 34551925134; symmetric relative difference <=0.25 at every eta.

Classify:

- `M25_M0_PK_MANUAL_QUADRATURE_TAIL_RECOVERED` if the N=4000 original tail-scaling gate is recovered and fine_bin_stability passes;
- `M25_M0_PK_QUADRATURE_FLOOR_INSENSITIVE_STABLE` if fine_bin_stability, fine_floor_flatness and auto_manual_fine_agreement all pass but tail scaling does not;
- `M25_M0_PK_QUADRATURE_SENSITIVE` if fine_bin_stability passes but auto_manual_fine_agreement fails;
- otherwise `M25_M0_PK_MANUAL_QUADRATURE_NOT_ESTABLISHED`;
- execution/provider failures remain blocked.

This diagnostic cannot promote K1 or K4 by itself. `physical_falsification=false`.
