# W04 M21 l=400 conditional summation-arithmetic stability audit v0.1

Frozen: 2026-09-15 before any terminal result from the authorized convolution sign/cancellation successor.

Provider authority remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Activation

This gate is analysis-only and may execute only if a terminal convolution accumulation analysis establishes either:

- `M21_L400_CONVOLUTION_SIGNED_CANCELLATION_LOCALIZED_WITH_SCOPE`; or
- `M21_L400_CONVOLUTION_ACCUMULATION_NOT_FURTHER_LOCALIZED_WITH_SCOPE`.

It may run in parallel with a separately authorized cumulative-phase/window localization because it tests a logically independent question: floating-point summation arithmetic versus quadrature/profile geometry.

No CLASS rerun and no provider modification are authorized.

## Exact source authority

On the exact provider, `array_trapezoidal_convolution()` initializes a double accumulator `res=0.0` and evaluates the native tau sequence with

`res += integrand1[i] * integrand2[i] * w_trapz[i]`

before assigning `*I=res`.

There is no compensated, pairwise, long-double or reproducible summation in this routine.

The clean recovered diagnostic already stores each native double contribution `C_i = source_i * radial_i * w_i`, the final native transfer value, and the Bessel-edge correction.

## Frozen inputs

Use only clean recovered diagnostic blocks accepted by run `34907528331` and its immutable q support/weights. Do not alter rows, q nodes, tau order, source/radial values, weights, edge correction or parent support.

For every accepted `(case,q)` block retain the exact native `index_tau` order.

## Frozen arithmetic reconstructions

From the stored finite double contributions `C_i`, compute four sums before adding the unchanged edge correction:

1. `S_native_order_double`: ordinary Python-equivalent sequential IEEE-754 double accumulation in native order;
2. `S_reverse_order_double`: ordinary double accumulation in exact reverse native order;
3. `S_kahan_double`: Kahan compensated double summation in native order;
4. `S_fsum`: correctly/faithfully rounded high-accuracy `math.fsum` over the same stored doubles.

Do not sort by magnitude for classification. A magnitude-sorted pairwise result may be report-only.

For method m define reconstructed transfer

`T_m = S_m + edge_correction`.

The stored provider transfer is `T_native`.

First require `T_native_order_double` to reproduce `T_native` to relative `1e-10`, preserving the parent reconstruction authority. Otherwise BLOCK.

## Frozen arithmetic-sensitivity metric

For each non-native method m and case c,q define

`A_m(c,q) = |T_m - T_native| / max(sum_i |C_i| + |edge|, 1e-300)`.

This denominator measures perturbation relative to the absolute contribution budget rather than the possibly cancellation-small final transfer.

Using immutable parent q weights `W_q`, define

`R_m(c) = sqrt(sum_q W_q A_m(c,q)^2 / sum_q W_q)`

and f3 specificity

`E_m = R_m(f3) / max(R_m(f2), R_m(f4), 1e-300)`.

Also report, without changing classification:

- relative difference `|T_m-T_native|/max(|T_native|,1e-300)`;
- condition/cancellation factor `(sum |C_i|+|edge|)/max(|T_native|,1e-300)`;
- ULP distance where finite and representable;
- per-q maximum and parent-weighted quantiles.

## Frozen classification

The gate is intended to distinguish material arithmetic-order sensitivity from a geometrical/quadrature cancellation mechanism.

Define a material arithmetic perturbation as BOTH:

- `max_q |T_fsum-T_native| / max(|T_native|,1e-300) > 1e-6`, and
- `E_fsum > 3`.

This threshold is frozen prospectively before the cancellation result and is diagnostic-only; it does not alter any parent threshold.

Classify:

- material condition true -> `M21_L400_ACCUMULATION_FLOATING_SUMMATION_SENSITIVITY_LOCALIZED_WITH_SCOPE`;
- otherwise -> `M21_L400_ACCUMULATION_FLOATING_SUMMATION_NOT_MATERIAL_WITH_SCOPE`;
- any authority/reconstruction/non-finite failure -> `M21_L400_SUMMATION_ARITHMETIC_STABILITY_BLOCKED`.

Reverse-order and Kahan results are corroborating/report-only; `fsum` controls the frozen classification.

## Claim ceiling

A positive result would show that native floating-point summation arithmetic materially contributes to the localized numerical response. It would not by itself establish a CLASS defect, because the diagnostic uses already-rounded stored double contributions and does not re-evaluate source/radial products at higher precision.

A negative result would rule out ordinary accumulation roundoff at this diagnostic resolution as the dominant explanation, leaving quadrature geometry/cancellation phase as the next mechanism.

No outcome promotes K1/K3/K4 or physically validates/falsifies M21.
