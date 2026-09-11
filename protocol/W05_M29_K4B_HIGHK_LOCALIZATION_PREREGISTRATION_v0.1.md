# W05 M29 Brans-Dicke K4b high-k numerical-localization preregistration v0.1

Date: 2026-09-11
Provider: `hiclass-code/hi_class_public` commit `0009f51d89e6465c79e570b496c66fc90058fa77`.
Parent gate: `M29_K4_NOT_ESTABLISHED_NUMERICAL_ROBUSTNESS`.

## Motivation fixed before K4b execution

The frozen K4 run executed all cells and produced finite outputs, but the `permille`-to-`ref` P(k) maximum failed at both omega points. Post-run forensic inspection localized the largest discrepancy to the sparse high-k end of the non-reference P(k) grid while median/central errors were much smaller. K4b is therefore a diagnostic attribution experiment, not a replacement acceptance test and not a route to retroactively relax K4.

K3 remains separately `BLOCKED_IMPLEMENTATION` by the pinned provider's gauge capability. No K4b outcome is physical falsification.

## Frozen model points

Use exactly the same supported Brans-Dicke points and conventions as K4:

- `omega_BD=15`,
- `omega_BD=1e4`,
- shipped `gravity_models/brans_dicke.ini`, changing only omega and output root,
- `background_Nloga=40000` for every K4b arm.

## Frozen profiles

Run five independent profiles per omega (`fail-fast:false`):

1. `baseline_permille`: provider `cl_permille.pre` only beyond the common dense background.
2. `grid_ref`: `cl_permille.pre` plus exactly the `cl_ref.pre` k-sampling block: `k_min_tau0=0.002`, `k_max_tau0_over_l_max=3`, `k_step_sub=0.015`, `k_step_super=0.0001`, `k_step_super_reduction=0.1`.
3. `evolution_ref`: `cl_permille.pre` plus the `cl_ref.pre` scalar perturbation-evolution block: `evolver=0`, start/tight-coupling/source triggers, scalar hierarchy maxima, `tol_perturbations_integration=1e-6`, `perturbations_sampling_stepsize=0.01`, and the radiation/ur/ncdm fluid-approximation settings copied verbatim from `cl_ref.pre`.
4. `pk_core_ref`: union of `grid_ref` and `evolution_ref` overrides, still retaining `cl_permille.pre` CMB transfer settings.
5. `full_ref`: provider `cl_ref.pre` with the same common dense background; this is the numerical comparison reference, not a physical truth model.

No cosmological/model parameter is changed between profiles.

## Frozen observable and metrics

Primary diagnostic observable: linear `P(k)` from `*_pk.dat`.

For each non-reference profile versus `full_ref`, compare on the profile's native k points inside common support using linear interpolation of the denser/reference curve. Record:

- point count,
- symmetric-relative-error max and RMS,
- median, p95 and p99,
- k location of the maximum,
- number and k range of native output points.

The symmetric error is `2|x-y|/(|x|+|y|+1e-300)` as in K4.

## Frozen attribution rule

For each omega define the parent discrepancy `E0` as the global max P(k) error of `baseline_permille` relative to `full_ref`. For each diagnostic profile define fractional reduction `R = 1 - E_profile/E0`.

A block is called **sufficient to localize the parent max discrepancy** only if it reduces the max error by at least 80% (`R >= 0.80`) for **both** omega points.

Classification order is frozen:

1. if `grid_ref` meets 80% for both and `evolution_ref` does not: `GRID_DOMINATED`;
2. if `evolution_ref` meets 80% for both and `grid_ref` does not: `EVOLUTION_DOMINATED`;
3. if both individual blocks meet 80% for both: `BOTH_INDIVIDUALLY_SUFFICIENT`;
4. if neither individual block does, but `pk_core_ref` meets 80% for both: `COMBINED_GRID_EVOLUTION`;
5. otherwise: `UNRESOLVED_REF_PROFILE_DEPENDENCE`.

Execution failure/non-finite output is classified separately as diagnostic infrastructure/numerical failure.

## Interpretation boundary

K4b never sets `K4_promoted=true`. Its only purpose is to determine whether the already-preserved K4 failure is attributable to the reference k-sampling block, the perturbation-evolution block, their combination, or additional `cl_ref.pre` settings. Any subsequent K4c acceptance test must be separately preregistered after K4b and must preserve the original K4 result.
