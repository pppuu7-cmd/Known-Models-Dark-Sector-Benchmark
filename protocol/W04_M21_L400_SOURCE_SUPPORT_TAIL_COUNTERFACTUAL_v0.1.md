# W04 M21 l=400 source-support tail counterfactual v0.1

Frozen: 2026-09-15 after terminal serialization-recovered convolution artifact `10373467959` and after source-level support forensics, but before any tail-counterfactual sums or classifications are computed.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Parent structural evidence

The clean recovered diagnostics establish, before this gate:

- all four cases have the same q support `261..333` (73 nodes) and same-q k agrees far inside the frozen `1e-6` geometry bound;
- `ref`, `f2`, and `f4` each retain exactly native tau indices `0..2905` for every q;
- their Bessel-edge correction is exactly zero for all 73 q and the retained last `u=tau0-tau` remains thousands of Mpc above the q-dependent Bessel minimum;
- `f3` retains `0..index_tau_max(q)` with `index_tau_max=3745..5377` and has a non-zero Bessel-edge correction for all 73 q; its last u lies within about 11 Mpc of the Bessel minimum;
- exact `transfer_integrate()` first limits the source by Bessel overlap and then decrements `index_tau_max` while the source is exactly zero. Edge correction is applied only when the final limit is the Bessel limit;
- scalar E uses the full perturbation source time list before this transfer-integral truncation.

Thus the recovered artifact contains a real source-support-domain difference: the three neighboring/reference cases become exactly zero after a common retained endpoint while f3 remains non-zero to the Bessel overlap.

This gate quantifies that domain-support difference. It does not infer why the f3 source remains non-zero.

## No new CLASS execution

This gate is analysis-only. Use only the clean recovered case artifacts from run `34907528331` and the terminal recovered aggregate. Do not modify source, radial kernels, weights, grids, physics, provider state or stored rows.

## Frozen shared endpoint

Define `J_shared = 2905`, fixed prospectively from the exact common terminal native index of `ref/f2/f4` established above, not from response amplitude.

Require:

1. all `ref/f2/f4` q blocks end exactly at J_shared;
2. all f3 q blocks extend strictly beyond J_shared;
3. same q set and same-q k geometry pass parent bounds;
4. parent native reconstruction remains <= `1e-10` relative error;
5. all required rows are finite and consecutive.

Any failure -> `M21_L400_SOURCE_SUPPORT_TAIL_COUNTERFACTUAL_BLOCKED`.

## Frozen counterfactual

For each q, let native stored signed terms be `C_i = source_i * radial_i * w_i`.

Let:

`T_ref(q)` = stored native reference transfer;

`T_f2(q)`, `T_f4(q)` = stored native neighbor transfers;

`T_f3_full(q)` = stored native f3 transfer;

`T_f3_shared(q) = sum_{i=0..J_shared} C_i`.

Do not add a synthetic edge correction to `T_f3_shared`. Exact CLASS source-zero truncation semantics explicitly need no Bessel-edge correction when the next source values are zero; this counterfactual asks what the recorded f3 convolution would have been if its support had ended at the same source-zero endpoint as the three neighboring/reference cases while all retained f3 terms were unchanged.

The native f3 tail contribution is

`T_tail(q) = T_f3_full(q) - T_f3_shared(q)`.

Also report the direct recorded-tail sum `sum_{i>J_shared} C_i + native_edge`; require it to agree with `T_tail` to relative `1e-10` or BLOCK.

## Frozen specificity test

Use the immutable parent q weights `W_q` already stored in the recovered aggregate.

Define response amplitudes relative to reference:

`A(c) = sqrt(sum_q W_q [T_c(q)-T_ref(q)]^2 / sum_q W_q)`

for `c=f2,f4,f3_full,f3_shared`.

Define

`E_full = A(f3_full)/max(A(f2),A(f4),1e-300)`

`E_shared = A(f3_shared)/max(A(f2),A(f4),1e-300)`.

Reuse the already-established specificity threshold `E>3`; no new response threshold is introduced.

Also define report-only:

- `tail_fraction_of_f3_response_amplitude = A_tail/A(f3_full)`, where `A_tail=sqrt(sum W_q T_tail(q)^2/sum W_q)`;
- per-q full/shared responses and tail terms;
- tail absolute contribution budget `sum_{i>J_shared}|C_i|+|edge|`;
- u range of the tail and source magnitude at J_shared and at the native last point.

## Frozen classification

- `E_full > 3` and `E_shared <= 3` -> `M21_L400_F3_SPECIFICITY_LOCALIZED_TO_EXTENDED_SOURCE_SUPPORT_WITH_SCOPE`;
- `E_full > 3` and `E_shared > 3` -> `M21_L400_F3_SPECIFICITY_PERSISTS_ON_SHARED_SOURCE_SUPPORT_WITH_SCOPE`;
- `E_full <= 3` -> `M21_L400_SOURCE_SUPPORT_PARENT_SPECIFICITY_INCONSISTENT_BLOCKED`;
- any authority/integrity/reconstruction failure -> `M21_L400_SOURCE_SUPPORT_TAIL_COUNTERFACTUAL_BLOCKED`.

## Follow-up authority

If specificity localizes to the extended source support, the next admissible gate is a separately prospectively frozen **approximation-state/source-zero transition audit** around the shared endpoint. It should record RSA/TCA state and the scalar-polarization source factor P without changing the provider trajectory.

If specificity persists on shared support, continue with the already-frozen convolution sign/cancellation branch; the late support is then not sufficient to explain the anomaly.

These branches may be pursued in parallel only after this gate is terminal because they answer different mechanisms.

## Claim ceiling

The counterfactual is an offline numerical mechanism test on stored double contributions. It does not modify or correct CLASS, establish a production setting, define a physical WDM scale, promote K1/K3/K4, or physically validate/falsify M21.
