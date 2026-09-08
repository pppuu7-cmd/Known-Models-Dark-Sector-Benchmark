# Future Dark-Sector Model Construction Methodology v0.1

Updated: 2026-09-08
Status: LIVING / evidence-fed from KMDSB waves
Scientific authority: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Purpose

This document converts benchmark experience into a controlled methodology for constructing a future original dark-sector model. It is not itself a candidate theory and it does not assume that every design prior currently in the ledger will survive later adversarial waves.

The construction rule is:

> build only from requirements that survive repeated DSIR/KMDSB stress tests; keep tentative priors distinguishable from promoted core requirements.

The machine-readable source of current requirements is `matrices/design_prior_ledger.csv`.

## 1. Canonical DSIR target

The future model must admit an unambiguous embedding into the DSIR residual bookkeeping

`X_{mu nu} = M0^2 G_{mu nu} - T^{known}_{mu nu}`

under explicitly frozen conventions for background, perturbations, gauge/frame, known-sector content and solver authority.

The model is not judged by interpretive novelty alone. It must generate a controlled, physically admissible and observationally distinguishable residual response after quotienting reference identities, calibrations and comparator degeneracies.

## 2. Construction pipeline

### F0 — authority and provenance freeze

Before deriving or fitting a candidate:
- pin the DSIR authority commit;
- pin solver/code versions and parameter conventions;
- define the known-sector subtraction;
- define model domain, units, gauge/frame and reference cosmology;
- record which channels are implemented, unknown, undefined or solver-limited.

No result is allowed to mix authority snapshots silently.

### F1 — recoverable reference/decoupling limit

The candidate must possess a physically admissible path to the DSIR reference limit. Under matched bookkeeping its residual must approach the reference origin rather than retain an artificial offset.

Required checks:
- existence of the limit;
- physical admissibility of the path;
- numerical resolvability near the limit;
- cross-solver or independent calibration where possible;
- separation of true nonzero residuals from solver floors.

This requirement is supported by DP-0001, DP-0002, DP-0101 and DP-0503.

### F2 — physical parameter geometry before differentiation

Do not assume every parameter neighborhood is Euclidean and two-sided. Freeze the physical admissible set first.

If a reference point lies on a boundary, use a tangent cone or one-sided derivative. Never create a symmetric finite-difference tangent through a forbidden region.

For a response vector `r(p)` and admissible local direction `v`, use the physically valid directional derivative

`J_v = d r(p0 + epsilon v) / d epsilon |_{epsilon -> 0+}`

when only the positive ray in `epsilon` is admissible.

This rule is already required by the IDE benchmark and is encoded in DP-0102, DP-0201 and DP-0202.

### F3 — conservation, gauge and frame closure

The candidate must close the bookkeeping before interpretation:
- total stress-energy conservation must hold under the chosen decomposition;
- internal dark-sector exchange must not masquerade as creation/destruction of total stress-energy;
- gauge and frame transformations must be explicit;
- background and perturbation sectors must use compatible conventions.

A background fit cannot establish model equivalence if perturbation responses differ.

Supported by DP-0203 and DP-0204.

### F4 — multi-channel response architecture

The candidate must predict more than one potentially independent response channel whenever the physics permits. A single observable block is not sufficient as a general design strategy.

High-value axes identified so far include:
- background expansion;
- matter/growth response;
- metric/slip-like response;
- scale dependence and characteristic-scale motion;
- time evolution / temporal localization;
- sign and orientation of response directions.

Missing channels are masked, never filled with zeros.

The local response Jacobian must be rank-tested; parameter count is not identified rank. Near-collinearity must be quantified.

Supported by DP-0301..DP-0304, DP-0401..DP-0404, DP-0502 and DP-0604.

### F5 — observation-space identifiability before interpretation

Raw theory-space separation is necessary but not sufficient. The candidate response must be projected through a pinned observational operator `R` and covariance `C`.

For a local theory Jacobian `J`, define a whitened response schematically as

`J_white = C^{-1/2} R J`

and the corresponding nuisance-free Fisher block as

`F = J^T R^T C^{-1} R J`.

When nuisance parameters are present, use the profiled/marginalized block rather than the raw Fisher matrix.

A model that is theoretically clean but has a response far below the covariance scale is `NONIDENTIFIABLE` in that scope, not physically falsified.

Wave 0 M01/wCDM is the calibration example: a controlled local deformation exists, yet the corrected DESI DR1 ShapeFit control gives approximately `sigma(epsilon_w)=0.1782`; the frozen `epsilon_w=1e-4` step is only about `5.61e-4 sigma` in that limited test.

Supported by DP-0103, DP-0105 and DP-0106.

### F6 — nearest-comparator attack

Every candidate must be attacked by the closest alternative mechanisms in the smallest valid common observable block.

Do not compare interpretations; compare response geometry under identical masks, grids, baselines and conventions.

For two local response directions `u` and `v`, use normalized geometry only as a theory-space diagnostic:

`cos(theta) = (u . v) / (||u|| ||v||)`.

Exact collinearity may be rejected in theory space, but observational discrimination is not promoted until covariance-aware whitening is performed.

Current Wave 2 examples:
- IDE vs GDM: closest frozen low-k pair has acute angle about 24.79 deg; exact directional equivalence is rejected within scope.
- IDE vs designer f(R): acute angles about 42.45 deg and 59.40 deg for the frozen IDE rays against the minimum resolved f(R) production ray; exact directional equivalence is rejected within scope.

These are theory-space results only.

Supported by DP-0403, DP-0501 and DP-0504.

### F7 — quotient-surviving novelty

After reference subtraction and comparator attacks, ask what remains that cannot be removed by:
- reparameterization;
- known calibration/systematic freedom;
- solver floor;
- observational projection degeneracy;
- nearest known mechanism;
- identity imposed by the bookkeeping itself.

A new microphysical story without a surviving observable direction is not sufficient for model promotion.

### F8 — prospective holdout prediction

The future model must predict at least one relation, scale, epoch, sign change, response orientation or cross-channel relation before the relevant holdout is examined.

Retrospective interpolation is not B8 support. Within-family holdout is useful but weaker than cross-family or regime-level prospective validation.

Supported by DP-0304 and DP-0601..DP-0603.

### F9 — synthesis and candidate promotion

Only after F0-F8 should an original candidate be promoted for dedicated model development.

Minimum promotion package:
1. explicit equations and degrees of freedom;
2. reference/decoupling limit;
3. physical domain and stability conditions;
4. conservation/gauge/frame closure;
5. reproducible multi-channel DSIR response map;
6. covariance-aware identifiability estimate;
7. nearest-comparator graph;
8. at least one prospective holdout prediction;
9. machine-readable provenance and solver controls;
10. explicit list of which KMDSB design priors the candidate satisfies, violates or makes obsolete.

## 3. Design-prior promotion policy

The ledger in `matrices/design_prior_ledger.csv` is evidence, not doctrine.

Use four conceptual levels:
- `ACTIVE`: extracted from at least one controlled benchmark result;
- `REINFORCED`: independently supported by multiple model families or waves;
- `CORE`: survives a dedicated adversarial wave and is required for candidate construction;
- `RETIRED`: contradicted, redundant or shown to be scope-specific.

Until the CSV schema is upgraded, keep its stored status unchanged and record promotion evidence in methodology/research logs rather than silently rewriting historical meaning.

## 4. Current provisional architecture implied by Waves 0-2

A promising future model should preferentially have:
- a clean LambdaCDM/reference intersection;
- non-pathological admissible local geometry;
- multiple independent response channels;
- a characteristic scale and/or time structure that can move in a predictive way;
- at least one metric/slip or temporal discriminator where available;
- signatures that survive comparison with both dark-sector and modified-gravity alternatives;
- amplitudes large enough to be observable in at least one realistic covariance-whitened channel without violating physical constraints;
- prospective predictions not used to tune the model.

This list is provisional. No new model should yet be built by hard-coding all 30 current priors as axioms.

## 5. Anti-patterns forbidden by the benchmark

- zero-imputing unknown channels;
- symmetric derivatives through a forbidden parameter region;
- declaring theory-space angle to be observational evidence;
- calling non-identifiability a physical falsification;
- using a background match as proof of full equivalence;
- comparing models on different grids/baselines without an explicit map;
- defining a holdout relation after looking at the holdout;
- interpreting solver thresholds as physical tangents;
- calling a new interpretation a new observable direction;
- promoting a design prior without recording the benchmark evidence that generated it.

## 6. Update rule

After every completed benchmark wave:
1. update `matrices/design_prior_ledger.csv` with newly extracted requirements;
2. update this document with only the methodology changes that survived the wave;
3. update `recovery/STATE.md` and `recovery/RESTORE_FROM_NEW_CHAT.md`;
4. append the chronology to `logs/research_log.md`;
5. keep unresolved/blocked evidence explicit rather than deleting it.

The future original model should be created in a separate repository when the promoted requirements are mature enough; KMDSB remains the evidence-producing benchmark and DSIR remains the formal reconstruction authority.
