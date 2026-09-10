# W03 M14 K1 decoupling regression preregistration v0.1

Date frozen: 2026-09-10
Family: M14 coupled quintessence / conformal scalar-DM coupling
Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`
Author workload anchor: `benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini`

## Source-bound decoupling map

The pinned provider has two interaction mechanisms that must both vanish for K1:

1. General scalar-DM coupling in `coupling_scf`, parameterized by q1-q4 (and associated exponents). The source has an early return to zero when q1=q2=q3=q4=0. The author workload already has q1-q4=0.
2. Hyperbolic field-dependent CDM mass selected by `model_cdm = i`, with `cdm_c` entering the CDM density through `1/(1+exp(2*cdm_c*phi))` normalized by its present-day value. At `cdm_c=0`, this ratio is identically one and its phi derivative vanishes.

Therefore the prospective total coupling-off point is:

- q1=q2=q3=q4=0 (unchanged from author workload);
- `model_cdm=i` retained in the decoupling-side case;
- `cdm_c=0` on the decoupling-side case.

The comparator is the identical scalar/cosmological workload with the interacting-CDM selector omitted, invoking provider-default standard CDM. No scalar-potential, initial-condition, density, primordial, neutrino, gauge or nonlinear parameter is changed.

## Cases

A. `idm_zero`: exact author workload except output plumbing, `write_background=yes`, and `cdm_c=0` while retaining `model_cdm=i`.

B. `standard_cdm`: exact same transformed workload, but both `model_cdm` and `cdm_c` lines are omitted so provider-default standard CDM is used.

Adding background output is diagnostic-only and identical between cases. Absolute output roots are plumbing-only.

## Frozen comparison

Both cases must exit 0 and produce fresh background and matter-power outputs.

For common finite numerical entries after dropping the first independent-coordinate column:

- background max symmetric relative difference <= 1e-8;
- every matched linear/nonlinear P(k) table max symmetric relative difference <= 1e-6.

Symmetric relative difference is `2|a-b|/(|a|+|b|+1e-300)`.

PASS requires both thresholds. A workflow green status alone is not PASS.

## Interpretation

PASS authorizes K1 for this provider/anchor only: the interacting implementation possesses the required source-exact uncoupled scalar+standard-CDM limit. It does not establish K2-K9, observational novelty, or superiority over M02.

FAIL with both cases executable is a scientific/reference-closure failure for this provider/anchor and must be separated from infrastructure failures. If either case does not execute or outputs are missing, classify as implementation/configuration blocked, not physical family failure.

No threshold or coupling-off transformation may be changed after viewing results.
