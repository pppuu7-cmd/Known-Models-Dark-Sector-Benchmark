# W04 M25 nonthermal sterile-DM PSD -> CLASS bridge preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F25 / M25 resonantly produced sterile-neutrino-like WDM
Upstream provider result: run `34544624039`, artifact `10178793702`, classification `M25_PROVIDER_CONTROL_PASS_STOCK_RESONANT_PSD`
Sterile-production provider: `ntveem/sterile-dm@e4486265e8207aa0dd28decc8c8d897266c0a52a`
Boltzmann provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Purpose
Validate a source-derived, density-preserving mapping from the provider's final nonthermal sterile/antisterile PSD to CLASS's tabulated `ncdm` interface. This is a bridge-validation gate. It does not yet establish the M25 K1 response limit, K4 convergence, or observational discrimination.

## Source-derived mapping
The sterile provider evolves physical momentum bins from `T_HIGH=1e4 MeV` down to `T_LOW=10 MeV`. `Snapshot100.dat` is the final snapshot and contains `p(MeV), delta f_nu_s, delta f_nu_sbar`. The provider's own density routine maps its physical momentum at snapshot temperature `T` to today through

`p_today = (T_cmb,0 * nfactor / T) * p_snapshot`,

with `nfactor=(4/11)^(1/3)`.

CLASS tabulated ncdm files require first column `q=p/T_ncdm` and second column `f0(q)`, with `T_ncdm` a temperature ratio relative to `T_cmb`. Therefore freeze:

- `T_cmb = 2.7255 K`, matching the sterile provider stock input;
- `T_ncdm = (4/11)^(1/3)` exactly as represented in double precision by the bridge script;
- `q = p_snapshot / T_LOW = p_snapshot / 10 MeV`;
- `m_ncdm = 7115 eV`;
- `deg_ncdm = 1`.

CLASS documents `deg_ncdm=1` as one family, i.e. one particle plus antiparticle. Hence for the asymmetric stock spectra freeze

`f0(q) = 0.5 * (delta f_nu_s + delta f_nu_sbar)`.

This reduces to the ordinary single-family distribution when particle and antiparticle spectra are equal. The sterile/antisterile asymmetry is gravitationally represented through their summed stress-energy because the two states have the same mass and are collisionless in this CLASS bridge.

## Anti-hiding rule
Do **not** pass `omega_ncdm` or `Omega_ncdm` in the bridge-validation CLASS input. CLASS is allowed to infer its density from the mass, temperature ratio, degeneracy and tabulated PSD. Passing the target density would rescale the PSD normalization internally and could hide an incorrect bridge.

## Frozen upstream inputs
Download the immutable upstream artifact from run `34544624039`, artifact `10178793702`, and use the newly generated `generated_provider_outfiles/` products, not the provider's precommitted historical outputs.

Validate both stock model directories:
- `ms7.115E-03s24.000E-11L2.971E-03`
- `ms7.115E-03s28.000E-12L4.849E-03`

For each, read `Snapshot100.dat`, final `state.dat`, and `params.dat`. Require the final state temperature to agree with `10 MeV` to relative `1e-10` before constructing q.

## Frozen CLASS execution
Use the pinned CLASS Python wrapper (`classy`) and compute the background with one custom ncdm species. Common bridge-only cosmology:
- `h=0.675`
- `T_cmb=2.7255`
- `omega_b=0.0222`
- `omega_cdm=0`
- `N_ur=3.046`
- `N_ncdm=1`
- custom PSD file as above
- `m_ncdm=7115`
- `T_ncdm=(4/11)^(1/3)`
- `deg_ncdm=1`
- `use_ncdm_psd_files=1`
- no `omega_ncdm` / `Omega_ncdm`.

Read `Omega_nu` from classy and form `omega_ncdm_CLASS = Omega_nu*h^2`.

## Frozen positive bridge gate
For each of the two stock PSDs require:
1. finite, strictly increasing q;
2. finite, nonnegative f0;
3. `|omega_CLASS - omega_provider| / omega_provider <= 0.01`;
4. the two independently shaped stock PSDs each pass the density gate.

The 1% density tolerance is frozen prospectively to allow differences between the sterile provider's direct finite-grid integration and CLASS's tabulated-PSD quadrature/interpolation without permitting an order-one normalization error.

## Frozen normalization negative control
For each model also construct `f0_sum = f_s + f_sbar` while keeping `deg_ncdm=1` and all other settings identical. This deliberately double-counts the particle+antiparticle family under the documented CLASS convention. Require

`1.98 <= omega_sum / omega_average <= 2.02`.

This negative control is not a physical alternative; it tests the factor-of-two degeneracy convention used by the bridge.

## Frozen classification
- missing/corrupt upstream artifact: `M25_CLASS_BRIDGE_BLOCKED_UPSTREAM_ARTIFACT`
- CLASS build/wrapper failure: `M25_CLASS_BRIDGE_BLOCKED_CLASS_PROVIDER`
- source-derived transform invalid or final T mismatch: `M25_CLASS_BRIDGE_TRANSFORM_INVALID`
- CLASS runs but density/negative-control gates fail: `M25_CLASS_BRIDGE_DENSITY_NOT_VALIDATED`
- all gates pass: `M25_CLASS_BRIDGE_DENSITY_VALIDATED`

For all classifications:
- `K1_promoted=false`
- `physical_falsification=false`.

## Next-step rule
Only `M25_CLASS_BRIDGE_DENSITY_VALIDATED` authorizes a separate prospective M25 K1/reference protocol. The K1 protocol must define a physically meaningful cold/reference or production-parameter limit without changing PSD normalization by hand and must include response convergence. A successful density bridge alone is not a model-family PASS.
