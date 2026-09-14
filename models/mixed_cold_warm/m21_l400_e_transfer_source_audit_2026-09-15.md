# M21 l=400 scalar E-transfer source-path audit — 2026-09-15

Provider authority: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is an outcome-independent source audit written while transfer-vs-harmonic run `34904313450` is non-terminal. It does not use or predict that run's scientific values.

## Frozen M21 precision baseline relevant to scalar E

The active transfer-phase experiments use exact `cl_permille.pre` plus `verification/m21/m21_ncdm_tight.pre` and generic `evolver=0`.

At the exact provider pin, `cl_permille.pre` contains:

- `hyper_flat_approximation_nu = 7000.`
- `transfer_neglect_delta_k_S_t0 = 0.17`
- `transfer_neglect_delta_k_S_t1 = 0.05`
- `transfer_neglect_delta_k_S_t2 = 0.17`
- `transfer_neglect_delta_k_S_e = 0.13`
- `delta_l_max = 1000`

The M21 ncdm-tight overlay changes ncdm background/perturbation accuracy and perturbation sampling, but does not override `transfer_neglect_delta_k_S_e`.

The full frozen G3 transfer/source-support precision group was executed in run `34869857740` and was `GROUP_INSUFFICIENT`: `Emax=535.0227223028012` versus parent `534.8355868817356`. That full G3 profile includes the reference transfer-neglect controls, including `transfer_neglect_delta_k_S_e=100`, together with other G3 controls. Stage-2 therefore did not activate the G3A/G3B subgroup decomposition. Correct scope: the scalar-E cutoff has **not been individually isolated**, but changing it inside the full G3 reference bundle was not sufficient to remove or materially reduce the excursion.

## Exact transfer type mapping

For CMB polarization the transfer module defines `ptr->index_tt_e` and maps it to perturbation polarization source `ppt->index_tp_p`.

For scalar mode, `transfer_select_radial_function()` selects

`SCALAR_POLARISATION_E`

for `index_tt == ptr->index_tt_e`.

## Exact scalar-E radial kernel

The scalar-E radial branch obtains the hyperspherical/spherical Bessel function through `interpolate_Phi(...)` at the current sparse `index_l` and applies

`factor = sqrt(3/8 * (l+2)(l+1)l(l-1)) / s2`

followed by a radial factor proportional to

`factor * cscKgen^2 * Phi_l * rescale_function`.

For the frozen M21 cosmology `Omega_k=0`, this is the flat scalar-polarization radial path; no curved-universe branch is physically active.

## Exact sparse-l evaluation

For each q/k, transfer computation loops the sparse `ptr->l` list. Before evaluating a transfer function it calls `transfer_can_be_neglected(...)`.

For scalar E one exact neglect condition is

`l < (k - transfer_neglect_delta_k_S_e) * ra_rec`.

With the active `cl_permille.pre`, the scalar-E threshold parameter is exactly `0.13`.

This is a discrete l/k-dependent branch in the transfer path. Its existence makes it a legitimate secondary source-level candidate for any transfer-localized sparse-knot effect, but the full-G3 null-reduction result substantially weakens a simple explanation in which the cutoff alone is the sole cause. **No causal attribution is made here.** A dedicated prospective one-factor test would be justified only after k/q support mapping places the excess near this exact branch geometry.

## Transfer to harmonic EE

The harmonic module consumes the stored scalar-E transfer values `ptr->transfer[...,ptr->index_tt_e,...]` at each direct sparse l and native q/k node.

For adiabatic scalar EE it forms the pointwise harmonic integrand

`P_R(k) * Delta_l^E(k) * Delta_l^E(k) * 4*pi/k`.

The q/k integrand is then accumulated into the direct sparse C_l. Only after all direct sparse C_l values are computed is the C_l table splined in l for arbitrary integer-l output.

Therefore the active transfer-vs-harmonic diagnostic can separate:

1. a response excess already present in `Delta_l^E(k)`;
2. one first apparent after quadratic/primordial EE weighting;
3. one first apparent only after harmonic q/k accumulation.

## What is NOT established

This audit does not establish that `transfer_neglect_delta_k_S_e` causes the l=400 spike. It does not establish a Bessel interpolation defect, a CLASS bug, a production precision choice, global convergence, K1/K3/K4 promotion, or physical mixed-dark-matter validation/falsification.

If the active parent localizes the spike to `Delta_l^E(k)`, the next admissible sequence is:

1. map the frozen k/q support of the excess with `protocol/W04_M21_CONDITIONAL_L400_K_SUPPORT_MAPPING_v0.1.md`;
2. compare that support to the exact scalar-E neglect boundary and radial/source integration regions;
3. only then preregister a one-factor cutoff/path test if the geometric support actually intersects a relevant branch boundary.
