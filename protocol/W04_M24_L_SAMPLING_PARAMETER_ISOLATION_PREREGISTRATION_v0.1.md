# W04 M24 l-sampling parameter isolation preregistration v0.1

## Trigger

The preregistered M24 sampling/projection sub-block isolation found that the `l_sampling` pair alone localizes the locked CMB excursion:

- control `Emax = 62.6449744969`;
- `l_logstep=1.026` + `l_linstep=25` gives `Emax = 0.8233792246`;
- exact a_idm_dr=0 identity remains exact;
- the matter P(k) response is unchanged while TT/EE/TE are regularized.

This sharply localizes the issue to CMB multipole sampling rather than ETHOS physics. The two settings must now be separated prospectively.

## Frozen setup

Retain exactly the parent M24 physical cases, CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540`, and the common compatibility control `idr_streaming_trigger_tau_over_tau_k=49` on both sides.

No physical, cosmological, transfer, hierarchy, integrator, q-sampling, hyper-sampling, or other precision setting may change.

## Independent parameter branches

Run two independent branches concurrently:

1. `l_logstep_only`: set only `l_logstep = 1.026`.
2. `l_linstep_only`: set only `l_linstep = 25`.

The already computed pair result is retained from run `34555463958` and must not be recomputed for attribution.

## Measurement

Run the same five control and five test cases and use the unchanged parent excursion classification from `global_numerical_precision_diagnostic.py`.

A single parameter is causal-localizing only if it satisfies the already frozen `LOCALIZED` criterion. If neither localizes individually, the pair is classified as an interaction requirement and no post-hoc parameter values may be introduced before a separately preregistered interaction/convergence ladder.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
