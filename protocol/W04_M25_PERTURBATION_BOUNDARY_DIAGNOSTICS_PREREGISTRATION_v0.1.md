# W04 M25 perturbation-boundary diagnostics preregistration v0.1

## Trigger

M25 source-matched tolerance and `ncdm_fluid_approximation=3` diagnostics leave the background H tail scaling near-linear while P(k), TT, EE and TE remain unresolved for both sterile-neutrino PSDs. The NCDM fluid approximation is therefore disfavored as the source of the perturbation-layer floor/excursion.

Two independent numerical boundaries are frozen prospectively and may run in parallel.

## Common frozen inputs

- CLASS pin: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Exact M25 PSD/case files from run `34548988620`.
- Cases per model: reference, eta=0.01, 0.003, 0.001.
- `tol_ncdm_bg = 1e-6`, `tol_ncdm = 1e-6`.
- `ncdm_fluid_approximation = 3` (`ncdmfa_none`).
- Audited capacity-only repair `_QUADRATURE_MAX_=4000`, `_QUADRATURE_MAX_BG_=4000`.
- No physical parameter, PSD sample, eta value, cosmology, or scientific threshold changes.

Models `m0` and `m1` are independent.

## Diagnostic A: transfer/projection precision

Append the provider's unmodified `cl_permille.pre` settings to the common profile. This file modifies only provider-defined transfer/projection precision controls (`hyper_flat_approximation_nu`, transfer-neglect thresholds, `delta_l_max`).

Classification asks whether any previously failing P(k)/TT/EE/TE tail-scaling block recovers.

## Diagnostic B: gauge branch

Keep the common precision profile but set `gauge = newtonian` for every case in the branch. Compare the same gauge-invariant output observables P(k), TT, EE and TE with the synchronous-branch scaling behavior.

Classification asks whether the tail-scaling failure is localized to the synchronous numerical branch.

## Decision labels

For each `(model, diagnostic)`:

- `M25_PERTURBATION_BOUNDARY_LOCALIZED` if all four target perturbation blocks recover;
- `M25_PERTURBATION_BOUNDARY_PARTIALLY_LOCALIZED` if one to three recover;
- `M25_PERTURBATION_BOUNDARY_INSENSITIVE` if none recover;
- `M25_PERTURBATION_BOUNDARY_PROVIDER_BLOCKED` on execution failure.

Diagnostic-only: `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
