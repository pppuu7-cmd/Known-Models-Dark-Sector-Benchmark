# W04 M21 l=400 edge-correction absolute sufficiency audit v0.1

Frozen: 2026-09-15 after terminal recovery `34907528331` established `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`, while the frozen signed-convolution successor is not yet authoritative in GitHub Actions. A local implementation-QA preview revealed that a pure specificity ratio can become arbitrarily large when neighboring edge corrections are exactly zero even if the absolute candidate amplitude is negligible. This protocol does not alter, replace, or reinterpret the already-frozen signed-convolution classifier.

## Activation

Run only if the authoritative result of `protocol/W04_M21_L400_CONVOLUTION_SIGN_CANCELLATION_v0.1.md` is:

`M21_L400_CONVOLUTION_EDGE_CORRECTION_LOCALIZED_WITH_SCOPE`.

Otherwise skip without scientific classification.

## Inputs

Use only the clean recovered case artifacts from run `34907528331`. No CLASS execution is authorized.

For each accepted q node, read from the frozen diagnostic:

- total scalar-E transfer `T_c(q)` for case c;
- Bessel-edge correction `B_c(q)` for case c.

The same q-set, provider identity, reconstruction, and geometry integrity gates from the parent recovery remain mandatory.

## Frozen amplitude construction

Define total transfer differences from reference:

`r_c(q) = T_c(q) - T_ref(q)` for c in `{f2,f3,f4}`.

Define the already-established parent f3-specific excess power:

`W_T(q) = max(r_f3(q)^2 - max(r_f2(q)^2,r_f4(q)^2), 0)`.

Define edge differences:

`b_c(q) = B_c(q) - B_ref(q)`.

Define the analogous edge-specific excess power:

`W_B(q) = max(b_f3(q)^2 - max(b_f2(q)^2,b_f4(q)^2), 0)`.

Compute

`R_edge = sqrt(sum_q W_B(q) / sum_q W_T(q))`.

This ratio compares like-dimensioned amplitudes and requires no fitted scale or post-hoc threshold.

Also construct the exact edge-replaced f3 counterfactual

`T_f3_cf(q) = T_f3(q) - (B_f3(q)-B_ref(q))`

and report the f3-specific excess norm before and after the replacement using the same frozen neighboring f2/f4 comparison.

## Frozen classification

- if `sum W_T <= 0` or any parent integrity fails -> `M21_L400_EDGE_ABSOLUTE_SUFFICIENCY_BLOCKED`
- if `R_edge < 1` -> `M21_L400_EDGE_SPECIFICITY_ABSOLUTELY_INSUFFICIENT_WITH_SCOPE`
- if `R_edge >= 1` -> `M21_L400_EDGE_AMPLITUDE_CAPABLE_NOT_SUFFICIENTLY_PROVEN_WITH_SCOPE`

The boundary 1 is not a tuned scientific tolerance: by construction a candidate amplitude smaller than the frozen total excess amplitude cannot by itself equal the entire excess in this norm. `R_edge >= 1` is only a necessary amplitude-capability condition, not causal proof.

## Claim ceiling

This audit exists specifically to prevent a ratio-with-zero specificity from being mistaken for an amplitude-sufficient mechanism. It does not alter the parent classifier, prove a CLASS defect, establish a physical WDM scale, promote K1/K3/K4, or physically validate/falsify the model.
