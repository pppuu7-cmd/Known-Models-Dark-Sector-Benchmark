# M13 — quintom / phantom-divide crossing coverage audit

Status: ACTIVE / COVERAGE SPLIT FROZEN
Wave: W03 dark-energy mechanism census
Family: F13

## Why M13 needs a scope split

The label "phantom-divide crossing" covers physically different objects.

### M13a — phenomenological smooth crossing

A smooth PPF/CLP history

`w(a)=w0+wa(1-a)`

that happens to cross `w=-1` is not a new response family relative to M08. It is literally a parameter subregion of the already benchmarked two-dimensional CPL/PPF manifold.

Therefore M13a is classified

`REPRESENTED_BY:M08_WITH_SCOPE`.

No additional solver run is scientifically justified merely to choose CPL parameters whose history crosses -1. Doing so would count parameter-region multiplicity as model-family multiplicity.

This representability statement is about the phenomenological smooth history only. It says nothing about the microphysical health of a single field attempting to cross the divide.

### M13b — covariant multi-DOF quintom

A true quintom construction introduces additional dynamical degree(s) of freedom, commonly a canonical/phantom or otherwise multi-field system, and can carry entropy/isocurvature/relative-field perturbations absent from the single effective CPL fluid.

M13b therefore remains an independent mandatory coverage subcase.

It must not be declared represented by M08 until a covariant implementation has been propagated through common DSIR response coordinates and its extra perturbation directions have been profiled against the full M08/CPL manifold.

## Mandatory M13b requirements before scoring

1. pin a public or reproducible covariant implementation and exact version/commit;
2. freeze the field content/action and physical/stability domain;
3. identify a recoverable LambdaCDM or smooth-DE reference/decoupling path;
4. separate physical parameters from closure/shooting nuisance parameters;
5. expose at least P+H and any additional entropy/metric channel naturally defined by the implementation;
6. test numerical and gauge/representation robustness;
7. attack the full M08 CPL manifold, not one constant-w ray;
8. if an extra response survives, bind it to an exact common observation operator before any observational claim.

## Current classification

- M13a smooth PPF/CPL crossing: `REPRESENTED_BY:M08_WITH_SCOPE`.
- M13b covariant multi-DOF quintom: `QUEUED_IMPLEMENTATION_PROVENANCE_SEARCH`.
- whole M13 family: `PARTIAL_COVERAGE`.

This split is deliberate: a crossing of an equation-of-state curve is not by itself a new DSIR mechanism; an additional propagating field can be.
