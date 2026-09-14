# W04 M21 conditional K1-v2 numerical-reference preregistration v0.1

Frozen: 2026-09-14 while runs `34884124030` (thermodynamics cross-evolver enum recovery) and `34883823728` (transfer-l tail convergence) are non-terminal. No substantive value from either active run was used in this design.

Provider remains exactly:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This protocol does **not** activate K1-v2 now. It freezes the conditions and selection rule under which a full K1-v2 may later be executed.

## Scientific question

After numerical-path diagnostics are resolved, does the same pinned source-complete mixed cold+warm CLASS realization approach the exact CDM boundary continuously as `f_w -> 0` on a numerically validated reference profile?

The historical K1-v1 result remains preserved. Its descending-H interpolation defect and whole-domain P(k) support saturation are not reused as physical failures.

## Activation requirements

K1-v2 may execute only if **both** active numerical parent aggregates are terminal, input-identity clean, and satisfy:

1. transfer-l parent classification exactly
   `M21_G2B_L_SAMPLING_TAIL_CONTRACTION_SUPPORTED_WITH_SCOPE`;
2. thermodynamics cross-evolver parent classification is exactly one of:
   - `M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED`, or
   - `M21_THERMO_SOLVER_INDEPENDENT_TIGHT_LIMIT_SUPPORTED_WITH_SCOPE`.

Any mixed/blocked/unsupported thermodynamics classification, any l-tail non-contraction/removal instability, or any identity failure leaves K1-v2 `NOT_AUTHORIZED_NUMERICAL_REFERENCE_OPEN`.

## Frozen numerical-profile selection rule

No manual choice is permitted after parent results.

### Transfer-l settings

If activation requirement (1) passes, primary K1-v2 uses the already frozen densest tail endpoint:
- `l_logstep = 1.005`
- `l_linstep = 10`

Numerical shadow uses the immediately preceding frozen tail point:
- `l_logstep = 1.0075`
- `l_linstep = 12`

### Thermodynamics solver

If cross-evolver class is `M21_THERMO_NDF15_SPECIFIC_SENSITIVITY_SUPPORTED`:
- primary/shadow thermodynamics solver = RK (`thermo_evolver=0`).

If cross-evolver class is `M21_THERMO_SOLVER_INDEPENDENT_TIGHT_LIMIT_SUPPORTED_WITH_SCOPE`:
- primary/shadow thermodynamics solver = provider-default NDF15 (`thermo_evolver=1`).

### Thermodynamics tolerance

For either authorized solver branch:
- primary: `tol_thermo_integration = 1e-7`;
- numerical shadow: `tol_thermo_integration = 1e-6`.

Thus the primary and shadow profiles are selected entirely by frozen parent classifications. No other precision parameter may differ between them except the frozen primary/shadow l-grid and thermodynamics tolerance above.

Both profiles retain:
- `cl_permille.pre`;
- `verification/m21/m21_ncdm_tight.pre`;
- generic `evolver=0`;
- all physical inputs unchanged.

## Frozen physical realization and ladder

Reuse verbatim the K1-v1 physical model and full ladder from `W04_M21_MIXED_COLD_WARM_K1_REFERENCE_PREREGISTRATION_v0.1.md`:

- exact CDM reference;
- `f_w = {0.10, 0.03, 0.01, 0.003, 0.001}`;
- `omega_dm=0.1200` fixed;
- `m_ncdm=3000 eV`, `T_ncdm=0.71611`;
- same common cosmology and output requests.

Both primary and numerical-shadow profiles must run all six physical cases independently. No cached spectra from diagnostic runs may substitute for these executions.

## Frozen coordinate handling

For every cross-grid comparison:
- retain finite rows only;
- sort the coordinate in strictly increasing order before interpolation;
- use strict overlap only;
- no extrapolation;
- if coordinates are exactly identical after sorting, direct same-grid comparison is used.

This explicitly repairs the K1-v1 descending-redshift H-axis defect.

## Frozen response metrics

Report both historical symmetric-residual diagnostics and noise-safe normalized-L2 metrics.

Normalized-L2 is `||x-y||_2 / max(||y||_2,1e-300)` after the frozen overlap/interpolation rule.

### H

Use the physical `H [1/Mpc]` column over the strict common redshift domain. Report p95 symmetric residual, RMS symmetric residual, and normalized-L2.

### P(k)

Determine one **global primary common positive-k interval** across exact CDM plus all five finite primary cases:
`[k_min,k_max] = [max_i min(k_i), min_i max(k_i)]`.

Freeze three support blocks by equal width in `ln k`:
- LOW: `[ln k_min, ln k_min + (ln k_max-ln k_min)/3]`;
- MID: next third;
- HIGH: final third, including the upper endpoint.

No boundary may be moved after outputs are seen.

For each block report p95/RMS symmetric residual and normalized-L2 finite-vs-CDM response. Whole-domain P(k) statistics remain diagnostic only and cannot veto a support-resolved pass by themselves.

### CMB

Use exact common integer multipoles for TT, EE, TE separately and report normalized-L2 plus historical p95/RMS symmetric residuals.

## Frozen numerical-floor control

For each physical case and retained observable block/channel, compute direct normalized-L2 between its primary and numerical-shadow outputs. Also compute the same primary-vs-shadow distance for exact CDM.

For finite case `i`, define conservative numerical floor
`F_i = max(D_shadow_primary(i), D_shadow_primary(CDM))`.

Define `Q_i = R_primary(i) / max(F_i,1e-300)`, where `R_primary(i)` is finite-vs-CDM normalized-L2 on the primary profile.

A point is:
- `IDENTIFIED` if `Q_i > 3`;
- `NUMERICALLY_EQUIVALENT_TO_BOUNDARY` if `Q_i <= 3`.

The factor 3 is frozen here before parent outcomes and is not tunable later.

## Frozen block convergence gate

For fractions ordered `0.10,0.03,0.01,0.003,0.001`, each H/P(k)-support/CMB block passes if all outputs are finite and either route A or B holds.

### Route A — identified convergence

All five points are IDENTIFIED, and:
1. primary normalized-L2 response is non-increasing at each fraction reduction with 5% relative slack;
2. response at 0.001 is lower than at 0.10;
3. log-log fit of normalized-L2 versus `f_w` over the three smallest fractions has exponent `p > 0.5`.

### Route B — convergence into numerical equivalence

At least the smallest-fraction point is NUMERICALLY_EQUIVALENT_TO_BOUNDARY, and:
1. once the sequence first enters numerical equivalence, no smaller fraction may re-emerge as IDENTIFIED with `Q>3`;
2. among all IDENTIFIED points preceding equivalence, primary normalized-L2 is non-increasing with 5% slack;
3. the last IDENTIFIED response, if any, is lower than the 0.10 response unless 0.10 is already numerically equivalent.

No slope is forced through numerically equivalent points.

## Frozen K1-v2 classification

Required blocks:
- H;
- P(k) LOW;
- P(k) MID;
- P(k) HIGH;
- CMB TT;
- CMB EE;
- CMB TE.

If activation/identity/execution fails: `M21_K1_V2_BLOCKED_NUMERICAL_REFERENCE`.

If every required block passes route A or B:
`M21_K1_V2_PASS_WITH_SCOPE_SAME_PROVIDER_NUMERICALLY_RESOLVED_ZERO_FRACTION_LIMIT`.

Otherwise:
`M21_K1_V2_REFERENCE_LIMIT_NOT_ESTABLISHED`.

A K1-v2 failure is not automatically physical falsification; any failing block must first be classified as numerical-floor, interpolation/support, execution, or physically persistent before a physical-failure claim is allowed.

## K2 and higher gates

On K1-v2 PASS, K2 may retain only the already established scoped geometry statement `f_w>=0` with an exact CDM boundary and no sign quotient.

This protocol does not promote K3, K4, K5 or higher properties. K4 requires a separate numerical-robustness protocol beyond the K1 primary/shadow control.
