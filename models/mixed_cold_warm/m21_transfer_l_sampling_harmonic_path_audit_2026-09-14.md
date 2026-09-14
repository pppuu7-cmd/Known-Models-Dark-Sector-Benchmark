# M21 transfer-l sampling -> harmonic C_l source-path audit — 2026-09-14

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is an outcome-independent source audit. It does not alter the active l-tail convergence classifier.

## Exact source chain

1. `source/transfer.c::transfer_get_l_list()` constructs the sparse transfer multipole list beginning at l=2. Its logarithmic increment is controlled by `l_logstep`; when that increment reaches the ceiling set by `l_linstep`, sampling switches to the linear step. For flat K=0, `angular_rescaling=1`, so decreasing either parameter directly densifies this list.
2. `source/harmonic.c` copies this list directly: `phr->l[index_l] = (double)ptr->l[index_l]`.
3. Harmonic output at requested l uses spline interpolation over `phr->l` (`array_interpolate_spline(phr->l, ...)`). Thus the two precision parameters govern the l sampling on which harmonic C_l values are represented/interpolated.

## Exact frozen-grid density for M21

M21 fixes `l_max_scalars=2500`. Applying the exact `transfer_get_l_list()` recurrence with flat `angular_rescaling=1` gives these list sizes (including the terminal lmax point):

- exact default `(1.12,40)`: 99 l nodes;
- parent I `(1.05,32)`: 159;
- parent R `(1.026,25)`: 246;
- parent T1 `(1.015,20)`: 362;
- parent T2 `(1.010,15)`: 492;
- active tail T3 `(1.0075,12)`: 611;
- active tail T4 `(1.005,10)`: 817.

Thus T2->T3 increases the sampled-l count by about 24%, and T3->T4 by about 34%, after T2 has already reached almost five times the default node count. The frozen tail therefore probes a substantial additional refinement rather than a negligible parameter displacement.

## Interpretation

The terminal direction/interaction result therefore has a concrete numerical pathway: denser `l_logstep/l_linstep` sampling can reduce an interpolation/sampling error in the transfer-to-harmonic CMB path. If the prospectively frozen tail audit also shows adjacent-grid contraction, the appropriate scoped description is `transfer-l sampling/interpolation under-resolution supported`.

This source chain does not establish that every CMB discrepancy comes from this mechanism, does not establish a code defect, and does not by itself prove global convergence.
