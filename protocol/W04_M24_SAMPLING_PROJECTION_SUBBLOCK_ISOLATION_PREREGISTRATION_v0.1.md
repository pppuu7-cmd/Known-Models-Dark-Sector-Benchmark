# W04 M24 sampling/projection sub-block isolation preregistration v0.1

## Trigger

The prospectively frozen six-block M24 `cl_ref` isolation found exactly one localizing block: `sampling_projection`, reducing the locked excursion from `Emax=62.6449744969` to `Emax=0.77181209775`. The `perturb_integrator` block was strongly sensitive in the opposite direction (`Emax=579.558659`), while thermo, hierarchy/streaming, k/start/TCA, and transfer/lensing did not localize.

The anomaly is therefore treated as a numerical sampling/projection problem until further isolation is complete. No ETHOS physical parameter may be changed.

## Frozen physical/control setup

Retain exactly the M24 physical cases and common compatibility control used in the parent block isolation:

- CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540`;
- omitted-interaction reference;
- exact `a_idm_dr=0` null;
- `a_idm_dr={18000,6000,1800} Mpc^-1`;
- `idr_streaming_trigger_tau_over_tau_k=49` on both control and tested branches;
- all other cosmology and ETHOS parameters unchanged.

## Four prospectively frozen sub-blocks

Test each one-at-a-time against the common compatibility control. The four jobs are independent and SHOULD run concurrently.

### A. `l_sampling`

- `l_logstep = 1.026`
- `l_linstep = 25`

### B. `hyper_sampling`

- `hyper_sampling_flat = 12`
- `hyper_sampling_curved_low_nu = 10`
- `hyper_sampling_curved_high_nu = 10`
- `hyper_nu_sampling_step = 10`
- `hyper_phi_min_abs = 1e-10`
- `hyper_x_tol = 1e-4`

### C. `hyper_flat_threshold`

- `hyper_flat_approximation_nu = 1e6`

### D. `q_sampling`

- `q_linstep = 0.20`
- `q_logstep_spline = 20`
- `q_logstep_trapzd = 0.5`
- `q_numstep_transition = 250`

## Execution and classification

Each sub-block runs the same ten control/test cases four-at-a-time and is analyzed with the unchanged parent excursion judge.

- `LOCALIZED`: parent frozen localization criterion is satisfied.
- `STRONGLY_SENSITIVE`, `INSENSITIVE`, `PROVIDER_BLOCKED`: unchanged parent definitions.

No sub-block combination may be introduced until all four one-at-a-time results are known. If no single sub-block localizes, a separately preregistered interaction/factorial test is required.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
