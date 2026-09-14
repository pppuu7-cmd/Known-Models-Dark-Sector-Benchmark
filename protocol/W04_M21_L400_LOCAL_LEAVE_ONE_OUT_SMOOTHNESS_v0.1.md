# W04 M21 l=400 local leave-one-out smoothness audit v0.1

Frozen: 2026-09-15 after terminal run `34901952566` classified `M21_L400_SINGLE_KNOT_VALUE_SUFFICIENT_FOR_HIGH_STATE_WITH_SCOPE`, and before any local leave-one-out statistic below is computed.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is **analysis-only**. It reuses immutable artifacts from factorial run `34887488405`; no CLASS rerun, physics change, precision retuning, threshold tuning, or new spectrum generation is allowed.

## Motivation

The terminal parents establish all of the following:

1. the thermodynamics branch map is not localized in exposed thermodynamics state tables;
2. the direct native CMB source branch map is not localized (`M21_CMB_BRANCH_NOT_LOCALIZED_IN_DIRECT_CMB_SOURCES`);
3. sparse-l factorial runs show a reproducible l=400 membership signature;
4. removing exactly l=400 from two independent HIGH sparse-knot supports makes both supports CALM, while common non-400 support remains CALM.

The remaining local question is whether the **computed l=400 response value itself is an isolated local outlier relative to its directly computed neighboring sparse knots**.

## Exact source authority

At the exact provider pin:

- `transfer_get_l_list()` defines the sparse multipoles used by the transfer module;
- `harmonic_cls()` copies `ptr->l` to `phr->l` and loops over those sparse l values, calling `harmonic_compute_cl()` at each one;
- only after all sparse-knot C_l values are computed does CLASS spline the table in l;
- `harmonic_cl_at_l()` evaluates arbitrary integer l by spline interpolation of that table.

Therefore the frozen neighborhoods below consist only of direct sparse harmonic knots:

- lane A `P400_ON_TAIL_OFF`: `(399,400,401)` are all exact sparse nodes;
- lane B `P400_EVEN_TAIL_OFF`: `(398,400,402)` are all exact sparse nodes.

No interpolated non-knot value is used by the primary classifier.

## Frozen artifacts and lanes

Parent run: `34887488405`.

- A: artifact `m21-lphase-P400_ON_TAIL_OFF` / id `10365592822`;
- B: artifact `m21-lphase-P400_EVEN_TAIL_OFF` / id `10365598517`.

Each lane must satisfy: exact provider head, all four cases `ref/f2/f3/f4` rc=0, exact lane name, exact sparse-l neighborhood, and the immutable input/profile identity recorded by its manifest.

## Frozen observable

Use EE only (column 3 of CLASS-format `cl.dat`, zero-based numeric column index 2 after parsing).

For each case c in `{f2,f3,f4}` define the response at sparse knot l:

`d_c(l) = C_c^EE(l) - C_ref^EE(l)`.

For each lane define symmetric neighbors `(l-,l+)` as above and the leave-one-out prediction

`dhat_c(400) = (d_c(l-) + d_c(l+))/2`.

Define the single-knot excursion

`E400 = |d_f3(400)| / max(|d_f2(400)|, |d_f4(400)|, 1e-300)`

and the neighbor-predicted excursion

`Ehat = |dhat_f3(400)| / max(|dhat_f2(400)|, |dhat_f4(400)|, 1e-300)`.

For each c define a normalized local residual

`Q_c = |d_c(400)-dhat_c(400)| / max(|dhat_c(400)|, (|d_c(l-)|+|d_c(l+)|)/2, 1e-300)`.

Then define

`J_resid = Q_f3 / max(Q_f2,Q_f4,1e-300)`.

Also report the same leave-one-out residual for the absolute reference EE curve, normalized by the local reference amplitude. It is report-only and cannot alter classification.

## Frozen thresholds

Reuse the established HIGH/CALM boundary without modification:

- HIGH iff E > 3;
- CALM otherwise.

Use the same factor-of-three specificity criterion for local residual localization:

- residual-specific iff `J_resid >= 3`.

No alternative threshold may be substituted after results are known.

## Frozen classification

For a lane, define `isolated_l400_spike=true` iff all three hold:

1. `E400 > 3`;
2. `Ehat <= 3`;
3. `J_resid >= 3`.

Aggregate classifications:

- both lanes isolated -> `M21_L400_ISOLATED_LOCAL_RESPONSE_SPIKE_SUPPORTED_WITH_SCOPE`;
- exactly one lane isolated -> `M21_L400_LOCAL_RESPONSE_SPIKE_PARTIAL`;
- neither lane isolated -> `M21_L400_LOCAL_RESPONSE_SPIKE_NOT_ESTABLISHED`;
- any artifact/schema/authority/node/input failure -> `M21_L400_LOCAL_LEAVE_ONE_OUT_BLOCKED`.

## Interpretation ceiling

A supported result localizes the anomaly to the directly computed harmonic response at one sparse multipole relative to its direct neighboring sparse knots. It does **not** by itself distinguish a transfer-function error from q-integration/harmonic accumulation, establish a CLASS bug, select a production precision profile, promote K1/K3/K4, or physically falsify mixed cold+warm dark matter.

If supported, the next admissible mechanistic gate is a prospectively frozen **l=400 transfer-vs-harmonic integrand audit** that records diagnostic transfer E-mode values and the EE q-integrand at l=400 plus control neighboring sparse l values without changing the numerical evolution.
