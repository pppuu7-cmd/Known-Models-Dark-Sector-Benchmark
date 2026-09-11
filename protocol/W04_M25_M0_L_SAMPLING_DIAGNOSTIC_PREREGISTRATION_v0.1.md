# W04 M25 m0 CMB l-sampling diagnostic preregistration v0.1

## Motivation

The complete m0 perturbation-integrator factorial isolation (`E,T,S,ET,ES,TS`, plus the previously computed full `ETS` parent) leaves the deterministic eta=0.003 CMB excursion essentially unchanged. Independently, the M24 ETHOS benchmark has prospectively localized an analogous isolated CMB excursion to the provider-defined CLASS multipole-sampling pair `l_logstep=1.026`, `l_linstep=25`, with P(k) unchanged.

This creates a new, independently discovered numerical failure mode that should be tested against M25 m0 before any physical interpretation.

## Frozen M25 inputs

- CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Immutable M25 PSD/cases from run `34548988620`, artifact `10180157389`.
- m0 only.
- reference plus eta = 0.01, 0.003, 0.001.
- synchronous gauge.
- `tol_ncdm_bg=1e-6`, `tol_ncdm=1e-6`.
- `ncdm_fluid_approximation=3`.
- quadrature capacity repair 4000/4000.
- no perturbation-integrator cl_ref settings in this diagnostic.

## Frozen intervention

Set only the provider-defined multipole-sampling pair:

- `l_logstep = 1.026`
- `l_linstep = 25`

No PSD, abundance, cosmology, eta, transfer, q-sampling, or other precision value may change.

## Measurements

Run the unchanged tail-scaling analyzer for H, P(k), TT, EE, TE. In addition record the eta=0.003 CMB p95 residuals and their ratio versus the existing source-matched/no-fluid baseline.

## Classification

- `M25_M0_L_SAMPLING_CMB_EXCURSION_LOCALIZED` if TT, EE, and TE all recover tail scaling and their eta=0.003 p95 residuals each decrease by at least 5x.
- `...PARTIALLY_LOCALIZED` if one or two CMB blocks recover or decrease by >=5x.
- `...INSENSITIVE` otherwise.
- `...PROVIDER_BLOCKED` on execution failure.

P(k) is reported independently and is not required for the CMB-localization label, because M24 evidence indicates this intervention specifically affects CMB multipole sampling rather than matter-power output.

Diagnostic only: `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
