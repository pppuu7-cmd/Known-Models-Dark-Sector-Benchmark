# W04 M25 m0 perturb-integrator factor isolation preregistration v0.1

## Trigger

The frozen M25 `perturb_integrator` cl_ref sub-block produced a model-dependent result:

- m1: all H/P(k)/TT/EE/TE tail-scaling gates recover;
- m0: H recovers and the eta=0.01/0.001 endpoints improve, but the deterministic eta=0.003 CMB excursion persists and the full gate remains insensitive.

The full m0 three-setting result is immutable evidence from run `34555169307` and must not be recomputed. This diagnostic isolates which integrator setting(s), or interaction between them, control the residual m0 excursion.

## Frozen common inputs

- CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Immutable M25 cases/PSD from run `34548988620`.
- m0 only; reference plus eta=0.01,0.003,0.001.
- `tol_ncdm_bg=1e-6`, `tol_ncdm=1e-6`.
- `ncdm_fluid_approximation=3`.
- synchronous gauge.
- quadrature-capacity repair 4000/4000.

The three parent settings are:

- E: `evolver=0`
- T: `tol_perturbations_integration=1e-6`
- S: `perturbations_sampling_stepsize=0.01`

## Prospective factor profiles

Run six independent profiles concurrently:

- `E`
- `T`
- `S`
- `ET`
- `ES`
- `TS`

The already computed `ETS` full parent result is retained as the seventh factorial corner. No post-hoc values are permitted.

## Measurements

Use the unchanged frozen tail-scaling analyzer for H, P(k), TT, EE, TE. Additionally record the eta=0.003 p95 response in TT/EE/TE for direct excursion attribution.

## Interpretation

A profile is `LOCALIZED` only if all previously failing perturbation blocks recover under the existing gate; `PARTIAL` if at least one recovers; otherwise `INSENSITIVE`. Provider execution failure remains non-physical.

The goal is attribution of the m0 numerical excursion, not physical model rejection. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
