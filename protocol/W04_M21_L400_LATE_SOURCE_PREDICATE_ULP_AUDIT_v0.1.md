# W04 M21 l=400 late-source predicate ULP audit v0.1

Frozen: 2026-09-15 after terminal serialization-recovered convolution run `34907528331` established a real support-domain split (`ref/f2/f4` end at native index 2905 while `f3` extends to the q-dependent Bessel boundary), and before any late-source predicate diagnostic execution or case values are generated.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Purpose

Test the exact provider branch that can convert a tiny floating-point change in flat-universe `angular_rescaling` into a discrete late-time scalar-E source truncation at direct `l=400`.

This gate is independent of the amplitude result of the source-support tail counterfactual: the support-domain split itself is already terminal evidence from the clean recovery artifact.

## Exact source authority

On the exact provider, `transfer_late_source_can_be_neglected()` initializes `neglect=false` and applies the strict predicate

`l > transfer_neglect_late_source * angular_rescaling`.

For scalar CMB E (`index_tt_e`), if that outer predicate is true, `neglect` is set true.

The precision default is `transfer_neglect_late_source = 400.0` and the active diagnostic multipole is exactly `l=400`.

In `transfer_integrate()`, the Bessel-overlap limit is determined first. If `ptw->neglect_late_source == true`, `index_tau_max` is then decremented while

`tau0_minus_tau[index_tau_max] < ptw->tau0_minus_tau_cut`.

Thus a change of this boolean can directly turn a Bessel-limited integration into an earlier late-source-cut-limited integration.

For the frozen flat cosmology `Omega_k=0`, CLASS documents `angular_rescaling=1` in the mathematical flat limit. The implemented value is computed as `ra_rec/(conformal_age-tau_rec)` and may differ from exactly 1 by floating-point roundoff. This gate measures, but does not prejudge, that difference.

## Frozen execution

Cases: `ref,f2,f3,f4` in four independent parallel jobs.

For every case:

- use exact existing mixed-cold+warm physical input;
- use exact `P400_ON_TAIL_OFF` precision-profile construction;
- exact provider pin above;
- `OMP_NUM_THREADS=1` so diagnostic output is serialized by the provider's own `Tools::TaskSystem`;
- CLASS timeout 2700 s, job timeout 55 min;
- compare full `cl.dat` to the immutable matching clean recovery case artifact from run `34907528331`; require normalized L2 <= `1e-12`.

No physics, precision, grid, threshold, source, integration order or provider return value may be changed.

## Output-only instrumentation

Patch only exact `source/transfer.c`. At the tail of the already-completed native `transfer_integrate()` call, and only for:

- scalar mode;
- transfer type E;
- direct `l=400`;
- frozen k support `0.03030247505892471 <= k <= 0.04401375054733766` Mpc^-1,

dump one summary row per q containing:

1. `index_q`
2. `k`
3. `l`
4. `angular_rescaling` (`%.17g`)
5. `transfer_neglect_late_source`
6. exact right-hand side `transfer_neglect_late_source*angular_rescaling`
7. evaluated strict predicate `l > RHS`
8. actual `ptw->neglect_late_source`
9. `ptw->tau_size`
10. `index_tau_max_Bessel`
11. final `index_tau_max`
12. `ptw->tau0_minus_tau_cut`
13. final `tau0_minus_tau[index_tau_max]`
14. `tau0_minus_tau_min_bessel`
15. final native transfer value.

The patch must be output-only and must not alter CLASS state.

## Frozen integrity

Require:

- exact provider pin;
- only `source/transfer.c` modified;
- CLASS rc=0;
- null CMB L2 <= `1e-12` against recovery parent;
- exactly one schema-valid row for every common frozen q node;
- common q-set equals the clean recovery q-set;
- same-q k relative differences <= `1e-6`;
- evaluated predicate equals stored `ptw->neglect_late_source` on every scalar-E row;
- all rows within one case agree exactly on `angular_rescaling`, threshold and predicate;
- final `index_tau_max` agrees with the clean recovery diagnostic for every q.

Any failure -> `M21_L400_LATE_SOURCE_PREDICATE_AUDIT_BLOCKED`.

## Frozen ULP reporting

Parse each round-trippable `angular_rescaling` double and report:

- `angular_rescaling - 1`;
- signed ULP distance from IEEE-754 double `1.0` using ordered positive-double bit representations;
- exact predicate margin `l - 400*angular_rescaling`;
- whether final endpoint is earlier than Bessel endpoint (`index_tau_max < index_tau_max_Bessel`).

These are report-only values; no fitted tolerance is introduced.

## Frozen classification

Let the case-level actual predicate pattern be the exact booleans from the provider.

- if `ref=true`, `f2=true`, `f4=true`, `f3=false`, and for all q the three true-predicate cases end before the Bessel endpoint while f3 ends at the Bessel endpoint -> `M21_L400_LATE_SOURCE_PREDICATE_ULP_SPLIT_LOCALIZED_WITH_SCOPE`
- if all four predicate booleans are identical while the already-authoritative support-domain split is reproduced -> `M21_L400_LATE_SOURCE_PREDICATE_NOT_EXPLANATORY_WITH_SCOPE`
- if predicates differ but not in the frozen `{ref,f2,f4}=true, f3=false` pattern -> `M21_L400_LATE_SOURCE_PREDICATE_OTHER_SPLIT_WITH_SCOPE`
- if the expected boolean pattern occurs but endpoint consequences do not match -> `M21_L400_LATE_SOURCE_PREDICATE_CONSEQUENCE_MISMATCH_BLOCKED`
- any authority/integrity/non-interference failure -> `M21_L400_LATE_SOURCE_PREDICATE_AUDIT_BLOCKED`.

## Claim ceiling

A localized predicate split would establish the numerical branch mechanism creating the l=400 support difference. It would not by itself establish a CLASS defect, because a separate prospective flat-identity/counterfactual audit would still be required before judging whether the floating-point branch behavior is erroneous or merely an expected implementation detail. It does not establish a physical WDM scale, production precision settings, K1/K3/K4 promotion, or physical validation/falsification.
