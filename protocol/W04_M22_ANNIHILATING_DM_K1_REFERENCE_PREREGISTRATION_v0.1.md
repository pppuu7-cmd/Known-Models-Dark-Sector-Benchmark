# W04 M22 annihilating-DM K1 reference preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT
Date: 2026-09-11
Family: F22 / M22 annihilating dark matter energy injection

## Provider / provenance
- Solver: `lesgourg/class_public`
- Frozen commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- Native control parameter: `DM_annihilation_efficiency` in m^3 s^-1 J^-1.
- Provider source defaults this parameter to zero and only enables exotic injection when the value is strictly positive.
- Provider example `scripts/varying_pann.py` scans 0 to 1.11e-22 and identifies TT/EE as affected observables while P(k) is expected to be unaffected to the scope of that example.

## Scope
This gate asks only whether the native annihilation-energy-injection implementation has an executable and continuous same-solver LambdaCDM reference as p_ann -> 0. It does not establish K3-K9, observational preference, a particle model, or a physical falsification.

## Frozen cosmology
Use the provider example Planck-2018-like fixed settings to minimize undocumented choices:
- omega_b = 2.255065e-2
- omega_cdm = 1.193524e-1
- H0 = 67.76953 km/s/Mpc
- A_s = 2.123257e-9
- n_s = 0.9686025
- z_reio = 8.227371
- output = tCl,pCl,mPk
- lensing = no
- P_k_max_1/Mpc = 3.0
- l_max_scalars = 2500
- recombination = HyRec
- non linear = none
- overwrite_root = yes

No nuisance/cosmological refit is permitted in K1.

## Cases
1. `ref`: parameter omitted entirely.
2. `zero`: `DM_annihilation_efficiency = 0`.
3. finite ladder, unchanged cosmology:
   - 1.11e-22
   - 3.33e-23
   - 1.11e-23
   - 3.33e-24
   - 1.11e-24

The coordinate is one-sided: p_ann >= 0. No signed quotient is asserted.

## Frozen metrics
For TT, EE and TE, on the exact common ell grid use
`R2 = ||C_l(p_ann)-C_l(0)||_2 / max(||C_l(0)||_2, 1e-300)`.
This avoids a percentile failure on near-null or sign-changing support.

For P(k), interpolate only if needed on the common positive-k overlap in log-k and use the same normalized L2 residual. P(k) is a negative-control channel, not a required positive response channel.

## Exact-zero identity gate
`zero` and `ref` must both execute and satisfy for TT/EE/TE/P(k):
- identical table shape and coordinates where native grids are expected to match;
- normalized L2 residual <= 1e-12.

If the exact zero path does not execute or fails identity, K1 is not promoted.

## Finite-tail continuity gate
For each positive-response channel TT and EE:
- all finite cases execute and metrics are finite;
- residual at 1.11e-22 > 1e-8;
- sequence is non-increasing as p_ann decreases, allowing 2% numerical slack between adjacent values;
- smallest-ladder residual <= 0.25 * largest-ladder residual;
- power-law slope fitted to the three smallest positive points is strictly positive, p > 0.20.

TE is diagnostic: apply the same continuity tests but failure alone does not veto K1 if TT and EE pass, because TE is sign-changing and can be support-sensitive. Its status must still be recorded.

P(k) negative-control condition:
- max normalized L2 residual over the finite ladder <= 1e-4.
A larger P(k) response does not automatically falsify the family; it blocks this scoped gate pending source/physics audit.

## Classification
- PASS: `M22_K1_REFERENCE_LIMIT_PASS_WITH_SCOPE_NATIVE_ENERGY_INJECTION`
- NOT ESTABLISHED: `M22_K1_REFERENCE_LIMIT_NOT_ESTABLISHED`
- PROVIDER BLOCKED: `M22_K1_PROVIDER_EXECUTION_BLOCKED`

Every non-PASS state has `physical_falsification=false` and leaves K4-K9 unpromoted.
