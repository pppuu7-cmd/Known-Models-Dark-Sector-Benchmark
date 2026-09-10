# F19/M19 fuzzy / ultralight-axion DM — AxiECAMB provider provenance

Updated: 2026-09-10
Status: `PROVIDER_PINNED_K1_CONTROL_AUTHORIZED`
Family: F19/M19
Planned wave: W04
Physical falsification: **NO**

## 1. Target response family

M19 represents fuzzy/ultralight scalar dark matter whose coherent field dynamics generate a wave/Jeans scale and scale-dependent small-scale suppression distinct in origin and transfer-shape evolution from thermal free streaming.

The immediate W04 goal is a source-complete **linear** Einstein-Boltzmann representative with an explicit cold-DM reference limit. Nonlinear halo claims are deferred to a separate provider/calibration because the primary provider below explicitly warns that its inherited nonlinear prescription is not recalibrated for axions.

## 2. Primary provider

Repository: `Ra-yne/AxiECAMB`

Frozen commit:

`b7ca9ba80aca178da5003d864b8e20cb5905555b`

Provider identity at this pin:

- AxiECAMB, a CAMB-based Boltzmann code for ultralight-axion observables in linear theory;
- implements a quadratic ULA potential;
- evolves the exact Klein-Gordon system initially and switches to an effective-fluid approximation after a controlled `m/H` threshold;
- published method authority identified by the provider README as arXiv:2412.15192, extending Passaglia & Hu (2022, arXiv:2201.10238);
- synchronous-gauge scalar perturbations and CMB/matter-power outputs are supported;
- provider README identifies `movH_switch=10`, `accuracy_boost=1` as the verified baseline configuration;
- provider README states default settings target sub-percent ULA linear observables for the intended regime and warns that inherited nonlinear/Halofit treatment is not extensively tested/recalibrated for axions.

Therefore the first KMDSB M19 route is explicitly scoped to linear scalar observables. No nonlinear K5/K8 claim will be imported from this provider.

## 3. Exact source-bound DM/reference coordinate

At the frozen pin, `inidriver_axion.F90` reads, for `use_physical=T` and `use_axfrac=T`:

`omegada = omdah2/h^2`

and for the ULA-DM regime `m_ax >= 1.44e-32 eV`:

`omegaax = axfrac * omegada`

`omegac = (1-axfrac) * omegada`.

Hence at fixed `omdah2`:

- `axfrac=0` gives `omegaax=0` and the full requested dark-matter density as CDM;
- `axfrac>0` continuously transfers a fixed fraction of the same total dark-matter budget from CDM to ULA;
- `axfrac=1` is pure ULA dark matter within that requested dark-matter budget.

The same source computes the remaining cosmological-constant budget after including `omegaax`, so the fraction coordinate does not intentionally alter the total dark-matter budget.

This provides a direct prospective K1 path:

`f_ax = axfrac -> 0`.

The mass remains a physical scale for finite `f_ax` but is unidentifiable at the exact `f_ax=0` reference. KMDSB will not differentiate with respect to mass at `f_ax=0` as if it were an identified coordinate.

## 4. Independent reference interface inside the same executable

The same input source also supports `use_axfrac=F`, in which

`omegac = omch2/h^2`

`omegaax = omaxh2/h^2`.

Thus a same-executable null comparator exists:

- fraction interface: `use_axfrac=T`, `omdah2=0.1200`, `axfrac=0`;
- density interface: `use_axfrac=F`, `omch2=0.1200`, `omaxh2=0`;
- identical remaining cosmological, mass, accuracy and output settings.

These two parameterizations should represent the same physical zero-ULA state. Their numerical identity is not assumed; it must be executed as the first K1 regression.

## 5. Frozen initial M19 anchor

For provider-control/K1 use:

- `m_ax=1e-27 eV` — the provider's committed example mass, safely above its fixed `1.44e-32 eV` DM/DE classification threshold and within its advertised linear-method regime;
- `omdah2=0.1200` / corresponding `omch2=0.1200`;
- adiabatic scalar mode only;
- `axion_isocurvature=F`;
- `do_nonlinear=0`;
- `movH_switch=10`;
- `accuracy_boost=1`;
- transfer and scalar CMB outputs enabled.

Finite-deformation science points are **not frozen in this provenance note**. They require successful provider-control/K1 and a separate K2-K5 preregistration.

## 6. Numerical/provenance cautions retained

Recent commits at the frozen source line include explicit corrections to recombination tolerance, photon-density/background consistency, radiation closure and physical constants. This is a reason to prefer a modern immutable AxiECAMB pin over silently inheriting an older AxionCAMB result.

It also means that comparison with a legacy CAMB/AxionCAMB binary is a cross-provider validation problem, not an exact same-code K1 identity gate.

The provider README warns:

- tensors are not supported in this version;
- growth-rate outputs are disabled;
- z>0 transfer interpretation requires care around the KG-to-effective-fluid switch;
- nonlinear/Halofit mode is not extensively tested for axions.

KMDSB therefore freezes the first M19 scientific scope to scalar linear CMB + `P(k,z=0)` + transfer outputs. Tensor/nonlinear absence is masked as unsupported, never zero-imputed.

## 7. Current authorization

K0 source/provenance: `PASS_WITH_SCOPE_PROVIDER_PINNED` pending build/executable control.

K1 execution: **AUTHORIZED** under a dedicated preregistration.

K2-K9 scientific promotion: **NOT YET AUTHORIZED**.

A failed build or zero-abundance execution is a provider/infrastructure result, not a physical failure of fuzzy/ULA dark matter.
