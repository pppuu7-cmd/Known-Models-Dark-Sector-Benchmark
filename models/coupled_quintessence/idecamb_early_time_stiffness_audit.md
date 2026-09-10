# M14 IDECAMB early-time stiffness / local-scale audit

Updated: 2026-09-10
Status: `SOURCE_DERIVED_LOCAL_SCALE_IDENTIFIED`

## Why the previous small-step ladder still failed

The pinned coupled-quintessence background equation contains

`dy(i_pdot2) = (-a^2*dU + gQ/gphidot) * a/adotoa`

with exponential coupling

`gQ = beta * grhoc_t * gphidot`.

Therefore the actual interaction force in the scalar equation is

`gQ/gphidot = beta * grhoc_t`.

At early times `grhoc_t` is large. Thus the parameter `beta` can be numerically tiny while the force ratio is not perturbatively tiny over the full history. This is a physical stiffness / scale-localization issue in the chosen full-history tangent, not by itself evidence of a solver branch jump.

## Source-derived crossover from the already validated beta=0 reference

At the earliest author diagnostic point `a=1e-4` of the previously validated beta=0 theory output:

- `grhoc_t = 4.0055e-4`;
- `dU = -3.1296e-2`;
- potential force magnitude entering the same equation is `a^2 |dU| = 3.1296e-10`.

Define the local crossover by

`beta_* grhoc_t = a^2 |dU|`.

This gives

`beta_* = 7.813256771938583e-7`.

The smallest point in the prior prospectively fixed recovery ladder, `beta=5e-5`, is about 64 times larger than this earliest-time crossover. Hence its order-unity early-DE response does not establish discontinuity at beta=0; it shows that the prior ladder remained outside the force-linear regime at the earliest included epoch.

## Consequence

A single source-scaled local gate is authorized before declaring branch/shooting pathology:

- choose both finite-difference steps safely below `beta_*`;
- keep the same response vector and K4 thresholds;
- do not extend into an open-ended sequence of ever-smaller post-hoc steps.

If the source-scaled gate still fails, then branch/root/initial-condition continuity becomes the next mandatory audit. If it passes, retain all earlier failed grids as evidence that the usable tangent neighborhood is extremely narrow and history-dependent.

This scale lesson is provider/anchor/history-window specific; it is not a universal bound on coupled-quintessence beta.
