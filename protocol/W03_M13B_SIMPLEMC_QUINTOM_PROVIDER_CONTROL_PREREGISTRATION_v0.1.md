# W03 M13b SimpleMC quintom provider-control preregistration v0.1

Date frozen: 2026-09-10
Scientific promotion authorized by this gate: NO

## Purpose
Test only whether a pinned public two-field quintom implementation is executable on its author-exposed `Quintom` route and preserve source/provenance diagnostics. This is a K0/provider-control gate, not K1-K9 production evidence.

## Pinned provider
`ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0` (SimpleMC 0.9.8 source tree).

Target implementation: `simplemc/models/QuintomCosmology.py`, exposed by `simplemc/runbase.py` as model `Quintom` with `vary_mquin=True, vary_mphan=True`.

## Source-bound physics identity
The implementation contains two scalar degrees of freedom. For variables `(phi,x_phi,psi,x_psi)`, the source dark-energy density contains `x_phi^2 - x_psi^2 + V/(3h^2)` and the Klein-Gordon RHS uses opposite potential-force signs for `phi` and `psi`. The quadratic/interacting potential is `V=0.5(mquin phi)^2+0.5(mphan psi)^2+coupling(phi psi)^2`. This is sufficient to treat the code as a genuine canonical+phantom two-field quintom *candidate* at background level rather than a CPL crossing relabel.

Author parameter defaults at the pin include `mquin=1.7`, `mphan=0.8`; the exposed `Quintom` route varies both and leaves the explicit interaction coupling off unless the separate `Quintom_couple` route is selected.

## Known limitations frozen before execution
1. The source explicitly comments `Still figuring out initial conditions for two fields.` The bisection-based present-density matching is therefore not assumed to be a validated physical early-time prescription.
2. The model computes homogeneous scalar dynamics/H(a)/w(a) inside SimpleMC. No Boltzmann perturbation equations for the two scalar fields are identified in this class. Therefore K3 perturbation closure and K5 multichannel perturbation rank cannot pass from this provider-control.
3. No reference/decoupling limit is scored in this gate. A candidate K1 map must be separately source-bound and prospectively preregistered only if provider execution succeeds and the initialization issue can be resolved without inventing physics.

## Frozen execution
Clone exact pin. Install only runtime dependencies needed for direct SimpleMC execution. Instantiate the author-exposed `Quintom` route through `ParseModel('Quintom')` when possible; if package-level import plumbing fails, also attempt direct `QuintomCosmology(vary_mquin=True,vary_mphan=True)` solely as a diagnostic, recording both routes separately.

Record: import/route exit status, `phi_ini`, finiteness of stored solution and H(a), finite w(a) after calling the provider helper, min/max w over the provider grid, and whether the sampled background crosses `w=-1`. Crossing is descriptive only and gives no K1-K9 promotion.

## Classification
- `M13B_SIMPLEMC_PROVIDER_CONTROL_PASS_WITH_SCOPE` only if the author-exposed route executes and returns finite homogeneous dynamics.
- `M13B_SIMPLEMC_DIRECT_CLASS_ONLY` if only direct class import works.
- `M13B_SIMPLEMC_PROVIDER_CONTROL_BLOCKED` if neither executes.

Even on PASS, expected family state remains partial because initialization provenance and perturbation closure are open. Execution failure is not a physical falsification of quintom cosmology.
