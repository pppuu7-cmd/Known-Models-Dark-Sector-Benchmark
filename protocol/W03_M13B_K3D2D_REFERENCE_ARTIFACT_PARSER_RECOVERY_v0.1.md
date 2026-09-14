# W03 M13b K3D2-D reference artifact parser recovery v0.1

Date frozen: 2026-09-14

## Immutable authority

This recovery is artifact-only. It MUST NOT execute CLASS, rebuild the provider, alter `cl_ref.pre`, or reinterpret the successful default lane.

Authority:

- parent workflow run `34793932614`;
- reference artifact `10329550837`;
- artifact digest `sha256:563bc5829e516a8a09f2d3fae995789c2c2a36d60267527a7a5b4f6e6407c676`;
- provider pin `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`;
- frozen protocol `protocol/W03_M13B_K3D2D_SELF_CONSISTENT_REFERENCE_REENTRY_v0.1.md`.

The parent reference provider returned nonzero rc after exact `cl_ref.pre` execution. The workflow post-parser then crashed while converting a corrupted/interleaved diagnostic token. The parser crash is harness/provenance plumbing and does not erase the provider failure already contained in the immutable artifact.

## Purpose

Recover a robust machine-readable classification and geometry from the immutable raw artifact without rerunning any solver.

## Frozen parser rules

1. Read `result/provider_rc.txt`, `result/stderr.txt`, `result/stdout.txt` from the immutable artifact.
2. Parse `KMDSB_GAUGE_IVP_FIXED` and `KMDSB_GAUGE_IVP_FIXED_FINAL` diagnostics. The boundary fixed point is PASS only if a final record states `converged=1`, iterations in `[1,16]`, final max residual `<=1e-12`, and tolerance exactly `1e-12` to printed precision.
3. Parse every unique top-level `KMDSB_MODE_FAIL` record by `(index_md,index_ic,index_k,k)` even when its nested RK diagnostic is malformed.
4. Parse nested `KMDSB_RK_COLLAPSE` key/value fields independently. A malformed numeric token or truncated/interleaved interval is recorded as raw text plus `null`; it MUST NOT crash the parser or delete the top-level mode failure.
5. A record is `strict_clean_geometry` only when all of `x,step_ratio,minimum,hdid,hnext,step_index,rk_interval_start,rk_interval_end` parse as finite values, the interval closing bracket is present, and `step_index` is an integer.
6. Also report the count of all records containing an RK-collapse signature, irrespective of diagnostic corruption.
7. Compute ranges only from strict-clean numeric records; separately report malformed/interleaved record identities and raw fragments.
8. Test frozen direct modes K1=`0.00022398828992555914` and K10=`0.0022398828992555913` with relative matching tolerance `1e-8` against all top-level failing k values.
9. Provider rc != 0 plus fixed-point PASS plus at least one RK-collapse signature authorizes a numerical-blocker classification even if some diagnostic lines are malformed.
10. Do NOT evaluate B1/B2/B3, TT/P(k) precision differences, or physical model validity when provider rc != 0.

## Frozen classification

If source/precision guard from parent run passed, provider rc != 0, fixed point passed, and at least one RK-collapse signature is recovered:

`M13B_K3D2D_SELF_CONSISTENT_REFERENCE_RK_NUMERICAL_BLOCKER_LOCALIZED`.

If the immutable artifact lacks sufficient raw evidence for that statement:

`M13B_K3D2D_REFERENCE_ARTIFACT_RECOVERY_INCONCLUSIVE`.

Malformed/interleaved diagnostic lines are reported as a separate harness-quality field and do not change the classification when the underlying provider failure and RK-collapse signatures are independently present.

## Claim ceiling

All outcomes preserve:

- default NDF15 same-IVP B1/B2/B3 PASS_WITH_SCOPE from run `34793433652`;
- reference B1/B2/B3 `NOT_EVALUATED` for this nonzero-rc run;
- default/reference numerical reproducibility `NOT_EVALUATED`;
- historical pre-IVP-fix RK blocker as immutable history;
- `K3_state_ceiling=PARTIAL`;
- `K4_promoted=false`;
- `K5_promoted=false`;
- `physical_falsification=false`;
- no author-code or public-V0 reproduction claim.

## Next authorized frontier

Only after this artifact recovery is terminal may a new prospectively frozen output-only first-step error-control decomposition audit be launched. Such an audit may instrument RK local-error/error-scale contributions for representative failing and neighboring passing modes, but MUST NOT change `cl_ref.pre`, RK tolerances, `minimum_variation`, solver family, physics equations, seam location, or initial surface.
