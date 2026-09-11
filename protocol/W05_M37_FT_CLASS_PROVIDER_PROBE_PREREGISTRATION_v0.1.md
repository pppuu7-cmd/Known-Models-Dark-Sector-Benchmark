# W05 M37 f(T) exact-pin CLASS provider probe preregistration v0.1

## Purpose

Audit whether the public `Speeddemon5050/Modified-CLASS-fT-Exact-` fork provides an executable, response-active implementation of the M37 f(T) family. This is a **K0 provider/provenance probe only**. It cannot by itself establish publication-grade authority, complete teleparallel perturbation correctness, or K1-K9.

## Frozen provider

- repository: `Speeddemon5050/Modified-CLASS-fT-Exact-`
- commit: `74e6a8679cdc233fb339c67127ed0921ba547894`
- no source patching is permitted before build/execution.

The source audit must verify all of the following at the exact pin:

1. `source/input.c` reads `n_fT` and defaults it to `0.0`;
2. `source/background.c` contains an n_fT-dependent background equation and f(T)-dependent H' correction;
3. `source/perturbations.c` contains explicit n_fT-dependent `alpha_ft`, first-derivative and second-derivative terms.

## Frozen numerical arms

Keep the same baseline cosmology and solver settings in both arms. Only `n_fT` changes:

- `reference`: `n_fT = 0.0` (the source equations reduce the f(T) dark-energy power to the constant term at this coordinate);
- `active`: `n_fT = 0.10`.

Use linear scalar outputs `tCl,mPk`, z=0 P(k), `P_k_max_h/Mpc = 1.0`, no nonlinear correction.

## Frozen gates

The probe is executable if and only if:

1. checked-out commit equals the frozen pin;
2. source-audit markers above are present;
3. provider builds without source modification;
4. both arms exit 0;
5. TT and P(k) tables for both arms contain finite numerical data;
6. at least one common observable has normalized-L2 response > `1e-6` between active and reference.

Normalized-L2 uses interpolation of the active table onto the reference coordinate over the common domain and `sqrt(mean((a-r)^2))/max(sqrt(mean(r^2)),1e-300)`.

## Classification rule

Even if every executable gate passes, **do not promote M37 to PASS_WITH_SCOPE in this probe** unless independent model-author/publication provenance is established separately. The strongest authorized classification is:

`M37_K0_PARTIAL_EXECUTABLE_FT_PROVIDER_PROVENANCE_OPEN`

If build/execution fails, classify the concrete implementation boundary (`BLOCKED_IMPLEMENTATION`). If the response is inactive, classify `NOT_ESTABLISHED`. None of these outcomes is a physical falsification of f(T).
