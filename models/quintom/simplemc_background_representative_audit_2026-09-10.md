# M13b SimpleMC true-crossing background representative audit

Updated: 2026-09-10
Provider: `ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0`
Status: `BACKGROUND_TRUE_CROSSING_REPRESENTATIVE_K1_PASS_WITH_SCOPE_K3_BLOCKED`
Physical family falsification: **NO**

## 1. Provenance and runtime

The exact provider commit is pinned. Its package metadata identifies SimpleMC 0.9.8 and an older Python support era. The first modern-runtime control was blocked by an API change in `sklearn.neighbors.DistanceMetric`; this was resolved without editing provider physics by running the pinned code under a historically compatible Python 3.8 / sklearn 1.1.3 environment.

Provider control then passed through the public `ParseModel('Quintom')` route, returning `QuintomCosmology` with a finite 4x500 background solution.

K0 classification for the **background implementation**: `PASS_WITH_SCOPE`.

## 2. Source family identity

The provider source contains two scalar degrees of freedom:

- canonical field `phi`;
- phantom field `psi` with opposite-sign kinetic contribution.

Its potential is

`V(phi,psi) = 0.5 (mquin phi)^2 + 0.5 (mphan psi)^2 + beta (phi psi)^2`.

The energy density and equation of state depend on the kinetic combination

`x_phi^2 - x_psi^2`,

so a change of sign of that combination produces a genuine background crossing of the phantom divide rather than a smooth-fluid CPL bookkeeping crossing.

This therefore has the correct mechanism identity for the M13b **multifield quintom background family**.

Important limitation from the same source: the author comments `Still figuring out initial conditions for two fields.` This prevents promotion of the provider to a complete validated M13b implementation.

## 3. Prospective author-slice crossing test

To avoid post-hoc parameter hunting, the scan was preregistered before execution and used only parameter slices already present in the author's own `plot_Quintom_DR12.py`:

1. fixed `mphan=1.2`, scan `mquin` over the author's nine-point `0.1..2.5` grid;
2. fixed `mquin=1.2`, scan `mphan` over the same author grid;
3. `beta=0` throughout.

A robust crossing required both

`min(w+1) < -1e-6`

and

`max(w+1) > +1e-6`

on the same domain, excluding provider fallback states `phi_ini in {0,-1}`.

Result:

- 18/18 author-slice points were finite and nonfallback;
- 5/18 showed a robust strict `w=-1` crossing already on the author's `z<3` plotting domain;
- the same five also crossed on the full native `lna in [-10,0]` domain.

Representative crossing examples include:

- `mquin=1.4333333333`, `mphan=1.2`: `w_min=-1.1657356`, `w_max=-0.9682157`;
- `mquin=1.7`, `mphan=1.2`: `w_min=-1.1006426`, `w_max=-0.8879440`;
- `mquin=1.9666666667`, `mphan=1.2`: `w_min=-1.0523022`, `w_max=-0.7894821`;
- `mquin=2.2333333333`, `mphan=1.2`: `w_min=-1.0432609`, `w_max=-0.6857011`;
- `mquin=1.2`, `mphan=1.1666666667`: `w_min=-1.2038940`, `w_max=-0.9991329`.

Classification: `M13B_SIMPLEMC_AUTHOR_SLICE_CROSSING_FOUND_WITH_SCOPE`.

This establishes actual background true-crossing representability in the pinned author code. It is not an observational fit and it does not validate perturbations.

## 4. K1 reference/decoupling limit

The prospectively frozen internal reference test used

- `mquin=1.7`;
- `beta=0`;
- canonical one-field provider branch as reference;
- two-field branch with `mphan={0,1e-3,5e-4,2.5e-4}`.

At exact `mphan=0`, the two-field and one-field solutions agree identically on the native grid:

- `max |Delta H/H| = 0`;
- `max |Delta rho/rho| = 0`;
- `max |Delta w| = 0`;
- identical `phi_ini = 0.150390625`;
- finite, nonfallback solutions.

This passes the preregistered `1e-10` identity tolerances exactly.

The positive-mass continuity diagnostic is also smooth. Halving `mphan` from `1e-3 -> 5e-4 -> 2.5e-4` reduces the H, density and w discrepancies by approximately a factor of four each step:

- H: `4.6607e-7 -> 1.1652e-7 -> 2.9129e-8`;
- rho: `1.3437e-6 -> 3.3592e-7 -> 8.3979e-8`;
- w: `1.3333e-6 -> 3.3333e-7 -> 8.3331e-8`.

This is consistent with a regular leading dependence on `mphan^2`, as expected from the quadratic phantom mass term at this anchor.

K1 classification: `PASS_WITH_SCOPE`.

## 5. K2-K5 status

K2 mechanism geometry is now physically meaningful at background level because the provider has an executable true-crossing region and a clean one-field boundary. However, no K2 production geometry is promoted yet; the unfinished two-field IC prescription must be treated as a possible numerical nuisance coordinate.

K3 is the decisive blocker for this provider. SimpleMC here is a background cosmology implementation; no source-complete linear perturbation system for the two-field quintom sector has been validated in KMDSB. Therefore conservation/gauge/frame/closure is not established.

Consequently:

- K3: `BLOCKED_PROVIDER_PERTURBATION_CLOSURE`;
- K4: `NOT_PROMOTED_BEYOND_BACKGROUND_CONTINUITY`;
- K5: `BLOCKED_BY_K3`;
- K6-K9: not authorized from this provider.

## 6. Scientific conclusion

M13b can no longer be described as lacking an executable true-crossing background representative. The pinned SimpleMC implementation supplies one, and it has a clean exact reference limit to the provider's canonical one-field branch.

What remains missing is **source-complete perturbation-level validation** and a trustworthy multifield initial-condition prescription. Therefore M13b remains only partially covered in the strict DSIR/KMDSB funnel.

This result weakens any argument that M13b is merely a phenomenological CPL crossing, because a genuine extra-degree-of-freedom background branch is now explicitly demonstrated. It does not yet show that this branch contributes a new multichannel response direction after perturbations and observation operators are included.

## 7. Next allowed route

Priority order:

1. search for an independent public CAMB/CLASS/other Boltzmann implementation of a true two-field quintom with explicit perturbation equations and pinned source;
2. if no suitable provider exists, preregister an independent KMDSB verification implementation from published covariant field equations, with gauge, initial conditions and reference limits validated before response ranking;
3. only after K3 is closed, choose a prospectively frozen crossing anchor and run K4/K5/K6.

Do not use the SimpleMC background result as a substitute for perturbation closure or as evidence that the M13b family is observationally favored.