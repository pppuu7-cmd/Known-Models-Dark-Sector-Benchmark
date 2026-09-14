# M21 l=400 transfer-convolution current front — 2026-09-15

Authoritative repository: `pppuu7-cmd/Known-Models-Dark-Sector-Benchmark`.
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Established parent chain

- Transfer/harmonic localization: `M21_L400_SPIKE_PRESENT_IN_E_TRANSFER_KERNEL_WITH_SCOPE`.
- k-support mapping: `M21_L400_K_SUPPORT_MAPPED_WITH_SCOPE`, with frozen active support `k05=0.03030247505892471`, `k95=0.04401375054733766` Mpc^-1 and peak near `0.030913138222910114` Mpc^-1.
- Sparse-l phase factorial: `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE`.
- No result promotes K1/K3/K4 and no physical falsification is authorized.

## Parent convolution run

Run `34906741049` used the frozen convolution-decomposition protocol and four parallel physical cases `ref,f2,f3,f4`.

All four case jobs completed with authority and null checks clean. The aggregate artifact classified `M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED` because `same_q_index_set=false`.

Post-terminal diagnosis established this was an output-instrumentation serialization failure:
- reference valid q support: `261..333`, 73 q nodes;
- f2 valid real q support also contains the same `261..333` nodes;
- same-q k max relative difference ref/f2 about `1.17e-10`, inside frozen `1e-6` bound;
- f2 diagnostic contained malformed/interleaved output rows and a spurious parsed q fragment, causing the raw set mismatch.

Do not interpret run `34906741049` as a scientific source/radial/convolution classification.

## Active recovery

Prospective recovery protocol:
`protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DIAGNOSTIC_SERIALIZATION_RECOVERY_v0.1.md`.

Only allowed execution change: `OMP_NUM_THREADS=1` for the diagnostic CLASS executions. No source patch, provider, physical input, precision profile, support, metric, threshold, analyzer or classifier changed.

Runner commit: `2338fb5a4ee92c8b94a1583089465e42d164f439`.
Recovery run: `34907528331`.

At handoff time the run is queued. Do not inspect partial scientific values. On terminal:
1. require all four case authority/null checks clean;
2. require original same-q support integrity and reconstruction gates to pass;
3. consume only the terminal aggregate artifact;
4. if non-blocked, materialize its frozen source/radial/product/convolution classification;
5. if still blocked, diagnose only the failing integrity check before opening any new scientific gate.

## Claim ceiling

Current evidence localizes a numerical CMB response through the scalar-E transfer path, with strong sparse-l phase sensitivity around direct l=400 and a narrow native-k support. It does not establish a CLASS defect, production tuning rule, globally converged CMB spectrum, K1/K3/K4 promotion, or physical validation/falsification of mixed cold+warm dark matter.
