# W04 M21 transfer-l grid-phase factorial v0.1

Frozen: 2026-09-14 after terminal l-tail result `M21_G2B_L_SAMPLING_TAIL_REMOVAL_NOT_STABLE` and before any phase-lane execution.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Terminal motivation

The immutable T4 anchor uses `(l_logstep,l_linstep)=(1.005,10)`, has 817 sparse transfer-l nodes, contains l=400 and l=2499 as exact computed nodes, and has EE excursion factor `4.3134820992594936` (>3).

Post-terminal T3->T4 localization shows the f3 EE response-vector change is overwhelmingly localized in the 201--800 band, with l=400 the leading contributor, while f2/f4 response vectors change only at the ~1e-5--1e-4 relative level. This motivates a grid-phase test rather than further one-direction density tightening.

## Frozen common realization

Same exact provider pin, physical `ref/f2/f3/f4` cases, `cl_permille.pre + verification/m21/m21_ncdm_tight.pre`, generic `evolver=0`, exact cosmology, ncdm realization, outputs, `l_max_scalars=2500`, k-range and response metric as the terminal l-tail parent.

No thermodynamics precision setting is added: the parent transfer experiment baseline is preserved exactly.

## Exact sparse-l recurrence authority

Use exact `transfer_get_l_list()` flat recurrence to compute the expected node list before execution. Every lane manifest must record node count, whether l=400 and l=2499 are exact nodes, nodes in 394--406, and final eight nodes. Execution is BLOCKED if the generated signature differs from the frozen signature below.

## Frozen phase lanes

Immutable parent anchor P0 (not rerun):
- `P0_T4`: `(1.0050000,10)`; 817 nodes; l400=yes; l2499=yes.

Mandatory new lanes:

1. `P400_OFF_TAIL_ON`
   - `l_logstep=1.0050130`, `l_linstep=10`
   - 815 nodes
   - l400=no
   - l2499=yes
   - local nodes 394--406: `[394,395,396,397,398,399,401,403,405]`
   - tail: `[2439,2449,2459,2469,2479,2489,2499,2500]`

2. `P400_ON_TAIL_OFF`
   - `l_logstep=1.0049900`, `l_linstep=10`
   - 817 nodes
   - l400=yes
   - l2499=no
   - local nodes 394--406: `[394,395,396,397,398,399,400,401,403,405]`
   - tail: `[2431,2441,2451,2461,2471,2481,2491,2500]`

3. `P400_OFF_TAIL_OFF`
   - `l_logstep=1.0050400`, `l_linstep=9`
   - 817 nodes
   - l400=no
   - l2499=no
   - local nodes 394--406: `[394,395,396,397,399,401,403,405]`
   - tail: `[2437,2446,2455,2464,2473,2482,2491,2500]`

4. `P400_EVEN_TAIL_OFF`
   - `l_logstep=1.0051400`, `l_linstep=8`
   - 817 nodes
   - l400=yes and l402=yes
   - l2499=no
   - local nodes 394--406: `[394,396,398,400,402,404,406]`
   - tail: `[2446,2454,2462,2470,2478,2486,2494,2500]`

No lane may be inserted or removed after results are available.

## Frozen observables

For every new lane, compute the same TT/EE/TE normalized-response R2 for f2/f3/f4 relative to exact CDM and the same excursion factors.

Primary phase observable: **EE excursion factor** `E_EE = R2(f3)/max(R2(f2),R2(f4))`.

Reuse the already-preregistered excursion boundary:
- `HIGH` if `E_EE > 3`;
- `CALM` if `E_EE <= 3`.

Also report direct CMB R2 from every new lane to P0 and pairwise response-vector changes; these are descriptive and do not alter the primary classifier.

## Frozen pattern classifiers

P0 is known HIGH before this preregistration and is used only as an immutable anchor.

### l=400 phase signature

Classify `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE` if:
- `P400_ON_TAIL_OFF` is HIGH;
- `P400_EVEN_TAIL_OFF` is HIGH;
- `P400_OFF_TAIL_ON` is CALM;
- `P400_OFF_TAIL_OFF` is CALM.

This tests l=400 presence with two independent 400-present layouts and two 400-absent layouts, including both tail-on/off contexts.

### high-tail signature

If the l400 signature above fails, classify `M21_L_GRID_PHASE_HIGH_TAIL_SIGNATURE_SUPPORTED_WITH_SCOPE` only if:
- `P400_OFF_TAIL_ON` is HIGH;
- all three tail-off lanes are CALM.

### broader phase sensitivity

If neither exact signature holds, but `max(E_EE)/min(E_EE) >= 3` across the four new lanes, classify `M21_L_GRID_PHASE_SENSITIVITY_BROADER_THAN_FROZEN_SIGNATURES`.

Otherwise classify `M21_L_GRID_PHASE_SIGNATURE_NOT_ESTABLISHED`.

Any execution/pin/input/signature failure -> `M21_L_GRID_PHASE_FACTORIAL_BLOCKED`.

## Interpretation ceiling

A supported phase signature establishes numerical sensitivity to sparse-l node placement at nearly fixed node count. It does not establish a CLASS defect, production tuning rule, physical oscillation, globally converged spectrum, K1/K3/K4 result, or physical mixed-dark-matter verdict.
