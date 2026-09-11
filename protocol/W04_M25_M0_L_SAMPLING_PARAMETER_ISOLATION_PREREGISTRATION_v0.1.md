# W04 M25 m0 l-sampling parameter isolation preregistration v0.1

## Trigger

The M25 m0 combined provider-defined multipole-sampling profile (`l_logstep=1.026`, `l_linstep=25`) reduced the eta=0.003 CMB excursion by factors ~16.9 (TT), ~141 (EE), and ~103 (TE), while strict tail-scaling recovery remained open and P(k) was not recovered. Independently, M24 isolated its analogous CMB excursion specifically to `l_logstep`, with `l_linstep` only partially sensitive.

This diagnostic determines whether the M25 m0 CMB improvement is likewise attributable to `l_logstep`, `l_linstep`, or both.

## Frozen branches

Use pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`, quadrature capacities 4000/4000, original M25 m0 ref/e2/e3/e4 cases, and the already source-matched common profile:

- `tol_ncdm_bg=1e-6`
- `tol_ncdm=1e-6`
- `ncdm_fluid_approximation=3`

Run two independent jobs in parallel:

1. `l_logstep_only`: add only `l_logstep=1.026`; provider default `l_linstep=40` remains unchanged.
2. `l_linstep_only`: add only `l_linstep=25`; provider default `l_logstep=1.12` remains unchanged.

No sterile-DM PSD, abundance, physical cosmology, eta ladder, or frozen scientific threshold is changed.

## Frozen analysis

Reuse `m25_k1_precision_floor_diagnostic.py`. Compare the eta=0.003 CMB p95 values against the source-matched no-fluid baseline from run `34551925134`.

For each CMB block TT/EE/TE record:

- baseline and isolated p95 at eta=0.003;
- improvement factor baseline/new;
- original frozen `tail_scaling_recovered` Boolean.

Classify a branch:

- `LOCALIZED` iff all three CMB blocks have improvement factor >=5 and all three recover frozen tail scaling;
- `PARTIALLY_LOCALIZED` iff at least one CMB block has improvement factor >=5 or recovers tail scaling;
- `INSENSITIVE` otherwise;
- provider/execution failures remain blocked, never physical failures.

P(k) is recorded but is not used to decide this CMB attribution gate. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
