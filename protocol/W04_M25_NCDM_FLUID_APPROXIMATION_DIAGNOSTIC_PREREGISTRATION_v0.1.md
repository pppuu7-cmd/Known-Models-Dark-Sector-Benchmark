# W04 M25 NCDM fluid-approximation diagnostic preregistration v0.1

## Trigger

The source-matched M25 tolerance ladder shows that the background H response recovers near-linear eta scaling in both resonant sterile-neutrino models, while P(k) and CMB blocks do not. For model m0 the eta=0.003 perturbation observables show a pronounced non-monotonic excursion; model m1 is smoother but still has shallow tail exponents. This localizes the unresolved K1 issue downstream of abundance/background closure and motivates a perturbation-approximation boundary test.

## Provider-defined diagnostic

CLASS remains pinned to `e85808324f51fc694d12e3ed7439552a3c3f9540`.

At this provider revision, `ncdm_fluid_approximation = 3` maps to `ncdmfa_none`; the provider's neutrino-hierarchy example describes this setting as a higher-precision, significantly slower option.

## Frozen inputs

Reuse the exact M25 K1 PSD/case files from run `34548988620`, artifact `10180157389`.

For both models `m0` and `m1`, execute only:

- reference CDM case;
- eta=0.01 (`e2`);
- eta=0.003 (`e3`);
- eta=0.001 (`e4`).

Use the already preregistered source-matched quadrature tolerances:

- `tol_ncdm_bg = 1e-6`
- `tol_ncdm = 1e-6`

Retain only the audited capacity repair `_QUADRATURE_MAX_=4000`, `_QUADRATURE_MAX_BG_=4000`.

The sole new perturbation intervention is:

`ncdm_fluid_approximation = 3`

No PSD values, sterile-neutrino parameters, eta values, cosmology, other precision controls, or scientific acceptance thresholds may change.

## Parallel execution

The m0 and m1 branches are independent and SHOULD run concurrently. Within each branch, the four CLASS cases have unique roots and MAY run two-at-a-time.

## Measurements and decision rule

Apply the unchanged tail-scaling analyzer used by the source-matched tolerance diagnostic to H, P(k), CMB TT, EE and TE.

Additionally compare the no-fluid results with the existing `t1e6` source-matched results from run `34551435626`.

- `M25_NCDM_FLUID_APPROXIMATION_LOCALIZED` if disabling the approximation recovers all target perturbation blocks (P(k), TT, EE, TE) plus H tail scaling for a model.
- `...PARTIALLY_LOCALIZED` if at least one previously failing perturbation block recovers but not all.
- `...INSENSITIVE` if no previously failing perturbation block recovers.
- `...PROVIDER_BLOCKED` if required execution fails.

This is a numerical/approximation diagnostic only. It cannot promote K1/K4 and cannot constitute physical falsification.
