# W04 M24 `l_logstep` transition-bracket preregistration v0.1

## Trigger

The frozen seven-point l_logstep ladder found all tested values 1.10..1.02 to be `M24_GLOBAL_PRECISION_EXCURSION_LOCALIZED` with exact identity, while the provider default l_logstep=1.12 retains Emax about 62.645. The preregistered monotonic-convergence criterion failed because the localized Emax values oscillate within the sub-unity regime, but the fine pair 1.026/1.02 is stable.

This diagnostic maps the narrow interval between the last tested localized coarse value 1.10 and the provider default 1.12 to distinguish a sharp sampling-grid transition from a smooth precision trend.

## Frozen grid

Use the same pinned CLASS commit, M24 physical cases, IDR compatibility control `idr_streaming_trigger_tau_over_tau_k=49`, and frozen analyzer as the parent ladder.

Run independent values:

`l_logstep = {1.1025, 1.1050, 1.1075, 1.1100, 1.1125, 1.1150, 1.1175}`.

Immutable endpoints:

- 1.1000: Emax=0.23026690746463432, LOCALIZED;
- 1.1200 provider default: Emax=62.6449744969262, not localized.

No ETHOS physical parameter or other precision parameter changes.

## Frozen analysis

For every new point record exact-zero identity, Emax, channel excursion factors and the existing frozen classifier.

Order the nine endpoint+new values by l_logstep. Define:

- `transition_bracket`: the highest localized tested point and the next higher tested point that is not localized, if such adjacent points exist;
- `abrupt_adjacent_jump`: true iff any adjacent Emax ratio `max/min >=5`;
- `all_new_exact_identity`: every new point preserves exact-zero identity <= existing threshold.

Classification:

- `M24_L_LOGSTEP_SHARP_GRID_TRANSITION_LOCALIZED` iff a transition bracket exists, `abrupt_adjacent_jump=true`, and all new exact identities pass;
- `M24_L_LOGSTEP_TRANSITION_SMOOTH_OR_UNRESOLVED` otherwise;
- provider failures remain blocked.

This is a numerical attribution diagnostic only. It does not promote K1 or K4 and does not constitute physical falsification.
