# M21 K1 v1 diagnostic audit — 2026-09-11

## Status of the frozen v1 result
The hosted recovery run `34538026870` successfully built pinned CLASS and executed the exact CDM reference plus all five finite mixed cold+warm cases. It persisted `M21_K1_REFERENCE_LIMIT_NOT_ESTABLISHED` under the prospectively frozen v1 gate. This result must be preserved as the outcome of that gate, but the audit below shows that it is **not** evidence of physical non-convergence of the mixed cold+warm family.

## 1. Background H block: axis-order analysis defect
CLASS background output at the pinned provider has column 1 = redshift `z` and column 4 = `H [1/Mpc]`. The raw redshift grid is strictly descending from early times to today and is identical between the reference and every finite case.

The v1 analyzer called `numpy.interp` directly with the descending reference redshift array. `numpy.interp` assumes an increasing interpolation coordinate, so the recorded H residual near 2 was an analysis-contract defect.

Direct same-grid comparison of the raw H column gives p95 symmetric residuals:

- f_w=0.10: 2.53509409e-05
- f_w=0.03: 7.60541719e-06
- f_w=0.01: 2.53515187e-06
- f_w=0.003: 7.60546902e-07
- f_w=0.001: 2.53515751e-07

The log-log exponent over the three smallest fractions is p = 0.99999903. Thus the background H block is internally consistent with a linear approach to the pure-CDM boundary. The v1 H failure is invalidated as a numerical-analysis artifact; this does not by itself promote K1 because the other v1 blocks remain governed by their frozen gate.

## 2. CMB f_w=0.003 excursion: deterministic, not stochastic runner noise
The finite point f_w=0.003 exhibits a deterministic high-ell excursion in TT/EE/TE under default CLASS precision. It is present in two independent hosted executions with byte-identical output:

- run `34537696887`;
- run `34538026870`.

For `f3_00_cl.dat` both runs have SHA256
`f80aab3a7964e1d30e91f542dbc3baf2dc2c3841020f54f705fe0e314eced66b`.

For `f3_00_pk.dat` both runs have SHA256
`89da656588bf9a039843c77daf15431dae045bc86dfd52708d4afc3e615dddec`.

Therefore the excursion is reproducible at the frozen default precision and cannot be dismissed as nondeterministic hosted-run noise. A precision study is required before interpreting it physically.

## 3. P(k): whole-domain p95 saturates while the response amplitude converges
The frozen whole-domain P(k) p95 residual sequence is approximately
`2.88e-4, 1.00e-4, 5.60e-5, 5.00e-5, 4.89e-5`, which causes the v1 smallest-three exponent criterion to fail.

However the RMS residual over the same cases is
`2.2318e-2, 6.5139e-3, 2.1456e-3, 6.5206e-4, 2.1665e-4`, with smallest-three log-log exponent p = 0.99569988.

This reveals an important funnel failure mode: a global p95 statistic can saturate on a broad near-null numerical floor when the physically distinctive response is localized to a smaller high-k support. Such a statistic can falsely become non-identifying even while the support-localized response approaches the reference smoothly.

## Methodological conclusion
The v1 classification remains historically valid **for the frozen v1 statistic**, but it is not a physical failure of M21. The audit identifies two separate funnel issues:

1. interpolation operators must canonicalize monotonic coordinate orientation before cross-grid comparison;
2. reference-limit gates for support-localized responses must not rely exclusively on a whole-domain percentile that can be dominated by near-null regions.

These are methodology findings relevant to the future model/funnel design.

## Allowed next step
Preregister an M21 K1 v2 test before changing any metric. The v2 test should:

- fix coordinate orientation generically (ascending sort before interpolation);
- use the provider-authored `cl_ref.pre` as a source-bound precision reference or a prospectively selected subset of its ncdm/CMB precision settings;
- retain the original fraction ladder and exact CDM branch;
- preserve whole-domain metrics as diagnostics;
- add prospectively frozen support-aware P(k) blocks (e.g. low/mid/high-k partitions determined before execution, not after seeing the v2 result);
- define a provider-precision-floor equivalence state for CMB channels whose physical response falls below independently sourced numerical precision rather than forcing an artificial power-law slope through numerical noise.

No K1 promotion is authorized by this audit.
