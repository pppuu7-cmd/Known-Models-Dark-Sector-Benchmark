# W04 / M19 AxiECAMB K0-K1 provider-control preregistration v0.1

Frozen: 2026-09-10
Status: PREREGISTERED
Family: F19/M19 fuzzy / ultralight-axion dark matter
Provider: `Ra-yne/AxiECAMB@b7ca9ba80aca178da5003d864b8e20cb5905555b`
Scientific promotion scope: K0 provider execution + K1 zero-ULA reference only

## 1. Purpose

Open W04 without waiting for all W03 provider-blocked branches to resolve. This gate asks only whether the pinned AxiECAMB source:

1. builds and traverses the scalar linear CMB + matter-transfer path on an explicit finite ULA-DM control;
2. exposes a numerically clean cold-DM reference through the source-bound fraction coordinate `axfrac -> 0`;
3. gives the same zero-ULA outputs through its independent density parameterization (`omaxh2=0`, `omch2=total DM`).

No finite-deformation geometry, response-rank, nearest-family discrimination or observation-space novelty is authorized by this gate.

## 2. Source/provenance authority

KMDSB audit:
`models/fuzzy_ultralight_axion/m19_axiecamb_provider_provenance_2026-09-10.md`

Frozen external source:
`Ra-yne/AxiECAMB@b7ca9ba80aca178da5003d864b8e20cb5905555b`

At this pin the provider documents:

- exact KG evolution followed by an effective-fluid approximation;
- quadratic ULA potential;
- scalar linear CMB/matter observables;
- verified baseline `movH_switch=10`, `accuracy_boost=1`;
- explicit warning that nonlinear/Halofit treatment is not recalibrated for axions.

The present gate therefore sets `do_nonlinear=0`, adiabatic scalars only, and does not claim tensor/nonlinear support.

## 3. Frozen cosmology/input base

Start from the provider's committed `params.ini` at the frozen commit. Preserve every line except the fields explicitly changed below.

Common changes/cases:

- `m_ax = 1e-27 eV`;
- `axion_isocurvature = F`;
- `do_nonlinear = 0`;
- `movH_switch = 10` (provider default if absent; explicitly set if needed);
- `accuracy_boost = 1`;
- scalar CMB and transfer outputs remain enabled;
- `OMP_NUM_THREADS=1` for deterministic reference comparison.

The provider's committed `ombh2`, neutrino sector, Hubble parameter, primordial spectrum, reionization, `l_max_scalar=2700`, `transfer_kmax=5` and all other common settings are retained.

## 4. Frozen cases

### R0-F — fraction-interface zero-ULA reference

`use_axfrac = T`

`omdah2 = 0.1200`

`axfrac = 0`

The source map predicts `omegaax=0`, `omegac=omdah2/h^2` in the DM-mass regime.

### R0-D — density-interface zero-ULA comparator

`use_axfrac = F`

`omch2 = 0.1200`

`omaxh2 = 0`

At the same mass this independently parameterizes the same zero-ULA state in the same executable.

### P1 — finite provider traversal control

`use_axfrac = T`

`omdah2 = 0.1200`

`axfrac = 0.10`

This case only establishes that the finite ULA-DM code path produces outputs at the frozen anchor. It is not yet a K2/K5 science point and its response is not interpreted in this gate.

## 5. Required outputs

All three cases must exit zero and produce non-empty, parseable, finite numeric files for the common supported blocks:

- scalar CMB spectrum (`scalCls.dat` under the case output root);
- lensed scalar spectrum (`lensedCls.dat`);
- linear matter power at z=0 (`matterpower.dat`);
- transfer output at z=0 (`transfer_out.dat`).

If the provider writes additional common scalar files, they may be archived but are not added post hoc to the pass/fail definition.

No tensor file is required.

## 6. Zero-reference identity metric

For each required output file compare R0-F vs R0-D.

Requirements:

1. same number of numeric rows;
2. same number of numeric columns in every matched row;
3. every parsed entry finite;
4. normalized max absolute difference

`D_inf = max(|A-B|) / max(max(|A|), max(|B|), 1e-30)`

must satisfy

`D_inf <= 1e-10`

for each required file.

Also record raw `max_abs_difference` and RMS normalized difference.

This is deliberately tighter than any science-response threshold because the two inputs are intended to resolve to the same physical zero-ULA state inside the same executable. Failure is retained as a K1/provider/reference issue; the tolerance is not relaxed after seeing results.

## 7. Build/execution gate

Build with the provider Makefile and system `gfortran` on `ubuntu-latest`. A compatibility-only compiler flag may be added only if required to compile legacy Fortran syntax and only if it does not edit source physics; any such change must be recorded in the result.

No external solver-source patch is authorized in this gate.

P1 must produce all required finite outputs. Its values need not differ by a preregistered amount from R0 because response significance belongs to K2-K5.

## 8. Classification

Allowed terminal classifications for this gate:

- `M19_AXIECAMB_K0_K1_PASS_WITH_SCOPE`;
- `M19_AXIECAMB_BLOCKED_BUILD`;
- `M19_AXIECAMB_BLOCKED_ZERO_REFERENCE_EXECUTION`;
- `M19_AXIECAMB_BLOCKED_FINITE_PROVIDER_CONTROL`;
- `M19_AXIECAMB_K1_REFERENCE_IDENTITY_FAIL`;
- `M19_AXIECAMB_OUTPUT_CONTRACT_FAIL`.

A provider/build/reference failure is not physical falsification of ULA/FDM.

## 9. Output contract

Canonical machine result:
`models/fuzzy_ultralight_axion/M19_AXIECAMB_K0_K1_RESULT.json`

Wave mirror:
`waves/wave_04_dark_matter/M19_AXIECAMB_K0_K1_RESULT.json`

Immutable workflow artifact shall contain:

- exact external commit ID;
- generated case ini files;
- build log;
- three execution logs;
- required numeric outputs;
- comparison/result JSON;
- this preregistration and provider audit.

## 10. Next gate if PASS

Only after `M19_AXIECAMB_K0_K1_PASS_WITH_SCOPE` may K2-K5 be preregistered. The next gate must freeze a physical coordinate chart away from the unidentifiable `m_ax` direction at `f_ax=0`, finite fraction/mass anchors, convergence in both fraction and mass/Jeans scale, and a direct common-grid attack against thermal WDM plus at least one additional suppression mechanism before any mechanism-attribution claim.
