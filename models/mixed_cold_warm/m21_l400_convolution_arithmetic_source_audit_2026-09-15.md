# M21 l=400 convolution arithmetic source audit — 2026-09-15

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This audit was performed after terminal recovery run `34907528331` classified `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`, but before any terminal convolution sign/cancellation successor result. It is source-level and outcome-independent with respect to that successor.

## Exact native summation

On the exact pin, `tools/arrays.c::array_trapezoidal_convolution()` performs a plain sequential double-precision accumulation:

```c
double res=0.0;
for (i=0; i<n; i++){
  res += integrand1[i]*integrand2[i]*w_trapz[i];
}
*I = res;
```

There is no Kahan compensation, pairwise tree reduction, long-double accumulator or reproducible/high-accuracy summation in this routine.

For the active scalar-E path, `integrand1` is the prepared transfer source, `integrand2` the radial kernel, and `w_trapz` the native trapezoidal integration weight. The optional Bessel-edge triangle correction is applied after this sum in `transfer_integrate()`.

## Exact trapezoidal weights

For monotonic coordinate x, interior weights are the standard neighboring half-span

`w[i] = 0.5 * (x[i+1]-x[i-1])`

with half-interval edge weights. The arrays helper contains corresponding sign handling for decreasing coordinates.

Thus the recovered diagnostic column `source*radial*w_trapz` is the exact native per-row arithmetic term that enters the sequential accumulator, before the separately recorded edge correction.

## Consequence for prospective testing

If the authorized sign/cancellation successor localizes the f3 response to cumulative signed accumulation, a clean next question is whether the result is sensitive to floating-point addition order itself or instead to the underlying quadrature/cancellation geometry.

The prospectively frozen `protocol/W04_M21_L400_CONDITIONAL_SUMMATION_ARITHMETIC_STABILITY_v0.1.md` therefore compares, using the already-recorded finite double contributions only:

- native-order ordinary double accumulation;
- reverse-order ordinary double accumulation;
- Kahan double accumulation;
- high-accuracy `math.fsum` accumulation.

This can be done without rerunning or modifying CLASS. The native-order reconstruction remains guarded against the stored provider transfer.

## Claim ceiling

Even a positive arithmetic-sensitivity result would not alone establish a CLASS defect: the offline test begins from already-rounded stored double products. It would only establish that final addition arithmetic materially contributes at this diagnostic resolution. A negative result would leave quadrature geometry/cancellation phase as the stronger candidate.

No result in this audit promotes K1/K3/K4 or physically validates/falsifies M21.
