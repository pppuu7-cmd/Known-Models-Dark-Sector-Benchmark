# W03 M14 IDECAMB source-scaled local gate — preregistration v0.1

Frozen: 2026-09-10

## Authority and non-erasure

The prior beta=.005/.01 gate and fixed smaller-step ladder down to 5e-5/1e-4 remain terminal K4 failures. This gate does not weaken either result.

Source audit of the exact coupled-quintessence equation identifies the early-time force ratio, not arbitrary post-hoc shrinkage, as the relevant scale. At the already validated beta=0 reference's earliest diagnostic point a=1e-4,

`beta_* = a^2 |dU| / grhoc_t = 7.813256771938583e-7`.

The prior smallest beta=5e-5 was ~64 beta_* and therefore remained nonperturbative in the earliest scalar equation.

## Frozen grid

Use the same pinned IDECAMB/CosmoMC provider, alpha_quint=0.02 anchor, theory-only output route and eight-channel response vector as the prior K4 gate.

Run only:

- beta=0;
- h=5e-8;
- 2h=1e-7.

Both finite steps are <0.13 beta_* and are frozen before execution.

## Frozen K4 thresholds

Unchanged:
- relative tangent-norm mismatch <= 0.10;
- tangent angle <= 3 deg.

All runs must exit 0, select coupled quintessence and emit finite required output.

## Frozen K5 scope

Only if K4 passes, apply the unchanged non-null floor `max |r_h| >= 5e-5`. One varied physical coordinate implies at most local rank 1.

Because some CMB/output coordinates may be unchanged at five-significant-digit serialization at this extremely small step, zero differences are legitimate measured zeros and are retained; missing/non-finite coordinates remain masked/failing and are never zero-imputed.

## Decision

- K4 pass: `M14_IDECAMB_K4_SOURCE_SCALED_PASS_WITH_NARROW_LOCALITY`; earlier coarser failures remain authoritative evidence that the tangent neighborhood is extremely narrow/history-sensitive.
- K4 fail: `M14_IDECAMB_K4_SOURCE_SCALED_FAIL`; stop shrinking beta and move to branch/shooting/initial-condition continuity audit.
- K5 is `PASS_WITH_SCOPE_RANK1`, `NONIDENTIFIABLE_AT_OUTPUT_FLOOR`, or `BLOCKED_BY_K4` according to the frozen rules.

No observational or family-level falsification claim is authorized.
