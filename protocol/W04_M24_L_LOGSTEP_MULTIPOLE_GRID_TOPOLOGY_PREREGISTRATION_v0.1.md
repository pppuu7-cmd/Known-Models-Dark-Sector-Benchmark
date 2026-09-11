# W04 M24 `l_logstep` multipole-grid topology preregistration v0.1

## Trigger

The frozen M24 transition-bracket diagnostic localized the numerical transition to `l_logstep in [1.1175, 1.1200]`: the 1.1175 point remains localized while the provider default 1.1200 has the previously frozen large CMB excursion. Inspection of the pinned CLASS source shows that the transfer multipole grid is generated with an integer-truncated logarithmic increment and therefore can change topology discontinuously as `l_logstep` changes.

This diagnostic tests that numerical mechanism directly. It is prospective relative to all intermediate 1.1180--1.1195 outputs.

## Immutable parent configuration

- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- M24 physical cases and frozen analyzer: identical to the parent transition-bracket workflow.
- Compatibility control: `idr_streaming_trigger_tau_over_tau_k = 49`.
- No ETHOS physical parameter is changed.
- No precision parameter other than `l_logstep` is changed.
- Parent frozen endpoints: 1.1175 is localized; 1.1200 is the provider-default non-localized endpoint with Emax about 62.645.

## Frozen topology grid

Run independent matrix points with `fail-fast: false`:

`l_logstep = {1.1175, 1.1180, 1.1185, 1.1190, 1.1195, 1.1200}`.

At every point run the same ten parent cases. Instrument the pinned CLASS `transfer.c` only to dump the final in-memory `ptr->l[0..l_size_max-1]` sequence after it has been constructed. The instrumentation must not modify any CLASS state or numerical value.

Dump a separate grid file for every case so parallel execution cannot overwrite diagnostic data.

## Frozen per-point observables

For each point record:

1. the parent frozen CMB diagnostic (`Emax`, exact-zero identity, classifier);
2. CLASS exit codes;
3. `ptr->l_size_max` and the exact ordered multipole sequence for every profile case;
4. SHA-256 digest of each sequence;
5. whether all profile cases have an identical grid sequence;
6. if profile grids differ between adjacent `l_logstep` points: symmetric-difference size, first differing index, first differing values, and the number of changed tail nodes.

The default/control cases provide an internal provider-default grid reference and are not used to retune any threshold.

## Frozen aggregate criteria

Order points by `l_logstep`. For each adjacent pair compute:

- `cmb_jump_ratio = max(Emax_i,Emax_j)/max(min(Emax_i,Emax_j),1e-300)`;
- `grid_changed = true` iff ordered profile-grid digests differ;
- first differing index/value and symmetric difference.

Define `aligned_discontinuity=true` iff there exists an adjacent pair satisfying all of:

- `cmb_jump_ratio >= 5`;
- `grid_changed=true`;
- both points completed all profile cases;
- exact-zero identity passes at both points.

Classifications are frozen as:

- `M24_L_LOGSTEP_CMB_JUMP_ALIGNED_WITH_GRID_TOPOLOGY_CHANGE` if `aligned_discontinuity=true`;
- `M24_L_LOGSTEP_GRID_CHANGES_WITHOUT_ALIGNED_CMB_JUMP` if grids change but no aligned pair exists;
- `M24_L_LOGSTEP_GRID_TOPOLOGY_INVARIANT_ACROSS_BRACKET` if no profile grid changes;
- `M24_L_LOGSTEP_TOPOLOGY_PROVIDER_BLOCKED` if required provider outputs or grid dumps are missing/failed.

The first classification is a strong numerical localization of the CMB catastrophe to a discrete sampling-grid transition, but is not by itself a proof that every downstream numerical pathway is understood.

## Interpretation boundary

This diagnostic is numerical attribution only. It does **not** promote K1 or K4 and does **not** constitute physical falsification of M24/ETHOS. No classification threshold may be changed after viewing the new outputs.
