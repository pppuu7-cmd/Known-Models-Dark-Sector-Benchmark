# W04 M21 l=400 conditional flat-identity predicate counterfactual v0.1

Frozen: 2026-09-15 while path-scope recovery run `34917028014` of the late-source predicate ULP audit is non-terminal, before any recovered predicate values are inspected.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Activation

This gate is authorized only if the terminal authoritative predicate audit classifies exactly:

`M21_L400_LATE_SOURCE_PREDICATE_ULP_SPLIT_LOCALIZED_WITH_SCOPE`.

For every other parent classification the gate must skip without CLASS execution.

## Exact-source basis frozen before activation

On the exact pin:

- thermodynamics computes `angular_rescaling = ra_rec/(conformal_age - tau_rec)`;
- transfer copies that value into `ptr->angular_rescaling`;
- the late-source decision uses the strict predicate `l > transfer_neglect_late_source * angular_rescaling`;
- the exact default `transfer_neglect_late_source` is `400.0`;
- direct scalar-E sets `neglect=true` if the outer predicate is true.

For the frozen cosmology `Omega_k=0`, the mathematical FLRW identity gives comoving angular distance to recombination equal to `conformal_age - tau_rec`; however the two implemented numerical paths are not assumed to be bitwise identical. This gate tests the branch consequence of the exact flat identity without changing physical inputs.

## Frozen counterfactual

Cases remain `ref,f2,f3,f4`.

For each case run two lanes:

1. `native`: exact provider behavior;
2. `flat_identity_predicate`: only when the environment gate is active **and** the provider background has `sgnK==0`, evaluate the late-source predicate using the exact binary64 value `1.0` in place of `ptr->angular_rescaling` **for that predicate only**.

Implementation constraints for the counterfactual lane:

- patch only `source/transfer.c`;
- set a file-local read-only diagnostic/counterfactual flag from `pba->sgnK==0` in `transfer_init()` before the parallel q loop;
- do not modify `pth->angular_rescaling`, `ptr->angular_rescaling`, q-period, q/k grids, Bessel geometry, source arrays, precision values, physical parameters, integration order or harmonic calculation outside the single late-source predicate operand;
- keep `transfer_neglect_late_source` at the actual runtime value from the provider;
- `OMP_NUM_THREADS=1`;
- same exact physical input and `P400_ON_TAIL_OFF` profile;
- same frozen k support and diagnostic schema sufficient to record native/counterfactual predicate and endpoint.

The native lane must reproduce the immutable authoritative parent with full-CMB normalized L2 <= `1e-12`.

## Frozen expectations and classification

At `l=400` and runtime threshold `400.0`, the exact flat-identity counterfactual evaluates `400 > 400*1.0`, hence false.

If the authorized native parent has `{ref,f2,f4}=true, f3=false`, define:

- `branch_normalized`: all four counterfactual predicates are false;
- `endpoint_normalized`: all four counterfactual cases are Bessel-limited rather than late-source-cut-limited on the frozen support;
- `f3_null`: f3 native vs counterfactual full-CMB normalized L2 <= `1e-12` and its direct l=400 transfer/endpoint diagnostics are unchanged to frozen reconstruction tolerance;
- `changed_only_expected_cases`: any counterfactual endpoint changes occur only in native-true cases `ref,f2,f4`.

Classification:

- if all four conditions hold -> `M21_L400_FLAT_IDENTITY_PREDICATE_BRANCH_CAUSAL_WITH_SCOPE`;
- if branch normalizes but endpoint does not -> `M21_L400_FLAT_IDENTITY_PREDICATE_ENDPOINT_MISMATCH_BLOCKED`;
- if endpoint normalizes but f3 changes beyond null tolerance -> `M21_L400_FLAT_IDENTITY_COUNTERFACTUAL_NONLOCAL_BLOCKED`;
- if the exact flat-identity counterfactual fails to normalize the predicate pattern -> `M21_L400_FLAT_IDENTITY_PREDICATE_NOT_CAUSAL_WITH_SCOPE`;
- any provider/patch/null/integrity failure -> `M21_L400_FLAT_IDENTITY_COUNTERFACTUAL_BLOCKED`.

## Claim ceiling

A `BRANCH_CAUSAL_WITH_SCOPE` result would establish that binary64 deviation of the implemented flat angular-rescaling quantity from the exact mathematical flat identity is causally sufficient for the l=400 late-source branch/support split under this benchmark. It would still not, by itself, establish a general CLASS defect, a production code fix, a physical WDM scale, K1/K3/K4 promotion, or physical validation/falsification. Any defect/fix claim would require an additional prospective regression across independent flat cosmologies and nearby multipoles/thresholds.