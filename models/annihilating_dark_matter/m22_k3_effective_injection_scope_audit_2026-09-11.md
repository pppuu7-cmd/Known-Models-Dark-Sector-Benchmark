# M22 annihilating-DM K3 effective-injection scope audit — 2026-09-11

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Implemented physics
The native CLASS exotic-injection module imports the standard background CDM density and computes the annihilation energy-injection rate as

`energy_rate = rho_cdm^2 * DM_annihilation_efficiency * (1 + boost_factor)`

for the default constant-efficiency case (modulo the optional redshift-dependent efficiency prescription).

The deposited energy is then distributed into thermodynamic channels such as heating, hydrogen/helium ionization and Lyman-alpha excitation.

## Conservation / depletion scope
The implementation is an effective CMB energy-deposition model. The source audit finds the annihilation parameter in the thermodynamics/exotic-injection path, while the standard background CDM density continues to supply the injection source. No paired annihilation sink term was found in the background CDM continuity equation that would evolve the depletion of rho_cdm consistently with the deposited power.

This is physically reasonable in the conventional small-depletion p_ann regime, where annihilation is treated as a perturbative energy-injection effect on recombination. But it is not a source-complete cosmological stress-energy implementation of an arbitrarily strong annihilating-DM sector.

## K3 classification
`PARTIAL_EFFECTIVE_ENERGY_DEPOSITION_NO_EXPLICIT_DM_DEPLETION_CLOSURE`

Consequences:
- a K1 reference-limit PASS is meaningful for the native effective p_ann response;
- the provider can support CMB-response benchmarking in its intended small-depletion regime;
- it cannot by itself establish full conservation closure for the entire annihilating-DM family;
- K5-K9 claims must retain this approximation scope unless an independently source-complete depletion implementation is used or a quantitative negligible-depletion bound is prospectively established for the tested region.

## Scientific boundary
This is not a physical falsification of annihilating dark matter. It is a scope limitation of the provider/phenomenological approximation and becomes a design requirement for any future original model: if energy transfer changes a sector's stress energy at an appreciable level, the donor sink and recipient source must be closed consistently rather than represented only in the observable-side thermodynamics.
