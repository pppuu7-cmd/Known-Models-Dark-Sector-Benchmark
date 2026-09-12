# W07 M33 pinned-provider nonmonotonic stability-map preregistration v0.1

Date: 2026-09-12
Model: M33 cubic Galileon in `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
Purpose: prospectively map the two suspicious regions exposed by immutable evidence: the original `Omega_smg=0.001` ghost veto and the newly observed isolated/nonmonotonic veto at `Omega_smg=0.004` while nearby tested points are executable.

## Immutable parent evidence
- original parser-compliant run: `Omega_smg=0.001` veto, `0.01` valid;
- W07 refinement run `34702935162`: `0.0015,0.002,0.003,0.006,0.008` valid, `0.004` ghost-vetoed.

## Frozen grid
Execute exactly these additional points, with no adaptive additions:
- low region: `0.0011, 0.0012, 0.0013, 0.0014`;
- 0.004 region: `0.0035, 0.00375, 0.004, 0.00425, 0.0045, 0.005`.

`0.004` is intentionally repeated in a fresh build/job to test reproducibility of the provider veto.

Use the identical parser-compliant cubic Galileon route as prior runs: edit only `Omega_smg`, remove `Omega_Lambda` and `Omega_fld`, retain all other shipped model/stability settings.

## Classification
Each point is `valid` iff exit=0 and finite CMB/P(k) are produced. Nonzero exit with the same provider ghost-stability diagnostic is `provider_stability_veto`; other failures are `provider_or_harness_failure`.

Report contiguous tested valid/veto segments only. Do not interpolate between points and do not call any segment a universal physical stability boundary. Explicitly report whether the repeated `0.004` classification agrees with run `34702935162`.

Always set `K1_promoted=false`, `physical_falsification=false`, `family_wide_stability_claim=false`.