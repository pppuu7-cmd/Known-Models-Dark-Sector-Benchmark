# W04 M21 G2B transfer-l sampling direction / interaction audit v0.1

Frozen: 2026-09-14 after terminal stage-3 and before any new pair-grid execution.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.
Parent authority: stage-3 run `34878158930`, artifact `10361784318`, digest `sha256:733e995346926ebbb3dd7355a33fbc0090fb5cc027b66eea0c7c968bc86453a9`.

## Parent facts

Stage-3 is terminal `M21_CMB_PRECISION_STAGE3_COMPLETE` with cross-lane identity true.

Within G2B:
- `l_logstep=1.026` alone: `PARAMETER_REDUCES_EXCURSION`, `Emax=70.53199679337801`;
- `l_linstep=25` alone: `PARAMETER_REDUCES_EXCURSION`, `Emax=78.37222398394675`;
- all other G2B single-parameter lanes are insufficient;
- stage-2 full G2B gave `Emax=34.304759775112494`, suggesting but not proving interaction because stage-2 also changed other G2B controls.

Exact source audit identifies `l_logstep` and `l_linstep` as general transfer/Bessel multipole-sampling controls. Smaller `l_logstep` (closer to 1) and smaller `l_linstep` are finer sampling directions.

## Hypothesis

If the G2B reduction represents genuine l-grid sampling convergence rather than an isolated profile-path effect, then applying the two active controls jointly should improve over either stage-3 single-axis result and further refinement along a frozen joint path should not systematically restore the large f3 excursion.

## Frozen object / baseline

Same exact provider, same M21 `ref/f2/f3/f4`, same `cl_permille.pre + m21_ncdm_tight.pre + evolver=0` baseline. Only `l_logstep` and `l_linstep` vary. No hyperspherical, thermodynamics, dark-matter, cosmology, gauge, k-grid, integrator, or threshold change is allowed.

## Frozen new pair ladder

Four mandatory independent pair lanes:

- `LPAIR_I`: `l_logstep=1.05`, `l_linstep=32`
- `LPAIR_R`: `l_logstep=1.026`, `l_linstep=25`  (pure stage-3 reference pair)
- `LPAIR_T1`: `l_logstep=1.015`, `l_linstep=20`
- `LPAIR_T2`: `l_logstep=1.010`, `l_linstep=15`

All values are frozen before pair-lane results. No inserted/deleted point after execution.

## Execution

Four independent GitHub jobs in parallel. Each executes immutable `ref/f2/f3/f4` sequentially with a 2700-second hard timeout per CLASS call and uploads return codes/logs/hashes/products even on failure.

## Frozen metrics

Use unchanged `integrator_branch_diagnostic.response_profile` and `Emax=max(E_TT,E_EE,E_TE)`.

Per pair lane:
- `REMOVES` iff TT/EE/TE excursion factors all <= 3;
- `REDUCES` iff removal fails but `Emax <= 534.8355868817356/3`;
- `INSUFFICIENT` otherwise;
- invalid/nonfinite/provider failure -> `BLOCKED`.

Report direct TT/EE/TE differences from the tightest `LPAIR_T2` as diagnostic only.

## Frozen interaction/direction classification

Let `Elog=70.53199679337801` and `Elin=78.37222398394675` be immutable stage-3 single-axis Emax values.

If any mandatory pair lane is blocked -> `M21_G2B_L_SAMPLING_AUDIT_BLOCKED`.

Otherwise:

1. Reference-pair interaction is `INTERACTION_SUPPORTED` iff `E(LPAIR_R) < min(Elog,Elin)`; otherwise `INTERACTION_NOT_SUPPORTED`.
2. Tightening path is `DIRECTION_MONOTONE_SUPPORTED` iff each next Emax in `I -> R -> T1 -> T2` is <= `1.05 *` the previous Emax. The 5% slack is frozen prospectively for small numerical nonmonotonicity.
3. Final classification:
   - interaction + monotone -> `M21_G2B_L_SAMPLING_INTERACTION_AND_DIRECTION_SUPPORTED`;
   - interaction only -> `M21_G2B_L_SAMPLING_INTERACTION_SUPPORTED_DIRECTION_NONMONOTONE`;
   - no interaction + monotone -> `M21_G2B_L_SAMPLING_DIRECTION_SUPPORTED_NO_PAIR_INTERACTION`;
   - neither -> `M21_G2B_L_SAMPLING_NONMONOTONE_NO_PAIR_INTERACTION`.

Report interaction gain `min(Elog,Elin)/E(LPAIR_R)` and all Emax values, but do not add an extra threshold after result.

## Controls

- exact pin every lane;
- identical physical INI hashes across lanes;
- exactly the two frozen varied keys in each pair profile;
- same common baseline hashes;
- no hidden G2B/thermodynamics settings;
- all products finite and uniquely resolved.

## Interpretation ceiling

This is a numerical sampling diagnostic only. A monotone result supports the interpretation that l-sampling resolution contributes to the excursion, but does not establish global CLASS convergence, a code defect, an authorized production precision profile, or any physical M21 conclusion. No K1/K3/K4 promotion.
