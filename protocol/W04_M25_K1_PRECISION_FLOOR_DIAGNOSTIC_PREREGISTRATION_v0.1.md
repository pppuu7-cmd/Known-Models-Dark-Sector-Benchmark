# W04 M25 K1 precision-floor diagnostic preregistration v0.1

Status: **FROZEN BEFORE HIGH-PRECISION EXECUTION**

## Trigger

The support-order recovery of the original M25 K1 run established the H limit cleanly (tail exponent approximately 1), while P(k) and CMB TT/EE/TE stopped improving smoothly at residuals of roughly 1e-5 to 1e-4 for the smallest eta values. This pattern is consistent with a numerical precision floor but is not sufficient to declare one.

This diagnostic asks whether the small-eta tail resumes the preregistered decoupling scaling when the same physical cases are recomputed with CLASS's own reference precision profiles.

## Frozen physical inputs

Use the exact M25 K1 case files and PSD tables from immutable workflow run `34548988620`, artifact `10180157389`.

No physical parameter, PSD, abundance coordinate, cosmology, CLASS commit, output set, or eta value may be changed.

Only the three tail points are recomputed:

- eta = 0.01 (`e2`)
- eta = 0.003 (`e3`)
- eta = 0.001 (`e4`)

for both provider PSD shapes `m0` and `m1`, together with a matching pure-CDM reference.

## Frozen CLASS provider and precision profiles

CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Retain the already-audited background quadrature-capacity repair `_QUADRATURE_MAX_BG_: 800 -> 4000`; this is infrastructure capacity only and was used in the original K1 run.

Run two independent official precision profiles from the same pinned CLASS tree:

1. `cl_ref.pre` — CLASS reference CMB precision profile;
2. `pk_ref.pre` — the corresponding reference P(k) profile, with the neutrino hierarchy extended relative to `cl_ref.pre`.

The invocation is the documented multi-file form `./class case.ini profile.pre`.

## Parallelization

The four `(PSD shape, precision profile)` combinations are independent and must be scheduled as separate matrix jobs when runner capacity permits:

- m0 × cl_ref
- m0 × pk_ref
- m1 × cl_ref
- m1 × pk_ref

Within each job, reference/e2/e3/e4 cases have unique output roots and may run at most two-at-a-time.

## Frozen diagnostics

Before residual evaluation, sort every table by its first support coordinate, as required by the support-order recovery.

For each job compute symmetric normalized residual p95 values for:

- H(z)
- P(k)
- CMB TT
- CMB EE
- CMB TE

at e2/e3/e4 against the same-profile pure-CDM reference.

Fit `R95 ~ eta^p` over the three tail points.

A block has `TAIL_SCALING_RECOVERED` iff:

1. p95 is monotone toward eta -> 0 with 2% slack;
2. the e4 p95 is lower than e2 p95;
3. fitted exponent `p > 0.5`.

The profile-level target is:

- for `cl_ref`: TT, EE and TE must all recover tail scaling;
- for `pk_ref`: P(k), TT, EE and TE must all recover tail scaling.

H is an audit block and is expected to retain its already-established scaling; H failure blocks a clean precision-floor interpretation.

## Interpretation

Allowed profile classifications:

- `M25_PRECISION_FLOOR_TAIL_SCALING_RECOVERED`
- `M25_PRECISION_FLOOR_TAIL_SCALING_PARTIAL`
- `M25_PRECISION_FLOOR_TAIL_SCALING_NOT_RECOVERED`
- `M25_PRECISION_FLOOR_DIAGNOSTIC_PROVIDER_BLOCKED`

This diagnostic cannot promote K1 by itself because only the three tail points are recomputed. If the `pk_ref` profile recovers all target blocks for both PSD shapes, the next permitted step is a separately preregistered full five-point K1 confirmation under `pk_ref.pre`.

All outcomes retain `physical_falsification = false` and `K4_promoted = false`.
