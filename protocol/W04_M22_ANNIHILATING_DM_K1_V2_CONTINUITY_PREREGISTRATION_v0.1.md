# W04 M22 annihilating-DM K1 v2 continuity preregistration v0.1

Status: FROZEN BEFORE V2 NUMERICAL RESULT
Date: 2026-09-11

V1 remains authoritative as a failed frozen gate because its P(k) negative-control threshold was violated. See `models/annihilating_dark_matter/m22_v1_negative_control_audit_2026-09-11.md`. V2 does not overwrite that result.

## Provider and cosmology
Same provider, pin and common cosmology as v1:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Scientific question
Does the native annihilation energy-injection response approach the exact same-solver no-injection reference continuously in every measured channel, including the small but finite P(k) response revealed by v1?

K1 requires decoupling/continuity, not that any particular channel have zero derivative or be exactly invariant at finite p_ann.

## Cases
Retain an omitted-parameter reference and explicit zero case.

Use a new tail extending below the v1 range:
- 1.11e-23
- 3.33e-24
- 1.11e-24
- 3.33e-25
- 1.11e-25
- 3.33e-26
all in m^3 s^-1 J^-1.

The last three values were not present in v1 and are the prospective tail used to determine whether a numerical floor appears.

## Metric
Normalized L2 against explicit zero, exactly as v1, for TT, EE, TE and P(k).

## Exact-zero gate
Omitted parameter versus explicit zero must execute and remain identical with R2 <= 1e-12 for all four channels.

## Continuity gate — all four channels required
For TT, EE, TE and P(k):
- every value finite;
- R2 at 1.11e-23 > 1e-10;
- non-increasing sequence with 2% adjacent slack;
- final R2 <= 0.10 times the first v2-tail R2;
- log-log slope over the three newly introduced smallest points is positive, p > 0.20.

No universal differentiability or p≈1 requirement is imposed.

## Classification
PASS: `M22_K1_V2_REFERENCE_LIMIT_PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION`

NOT ESTABLISHED: `M22_K1_V2_REFERENCE_LIMIT_NOT_ESTABLISHED`

PROVIDER BLOCKED: `M22_K1_V2_PROVIDER_EXECUTION_BLOCKED`

Every outcome has `physical_falsification=false`; K3-K9 remain open.
