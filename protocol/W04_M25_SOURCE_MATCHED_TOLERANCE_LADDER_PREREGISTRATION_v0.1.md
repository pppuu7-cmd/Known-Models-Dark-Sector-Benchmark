# W04 M25 source-matched tolerance ladder preregistration v0.1

## Trigger

The pinned sterile-dm provider uses `D_TOL = 1e-6`. Its rate tables support momentum only through `p/T = 20`; attempted support extension beyond that domain stops inside the provider. Meanwhile CLASS defaults are `tol_ncdm_bg = 1e-5` and `tol_ncdm = 1e-3`, while `cl_ref.pre`/`pk_ref.pre` impose `tol_ncdm_bg = 1e-10`, which the finite provider PSD cannot satisfy even with quadrature capacities raised to 4000.

## Frozen inputs

Reuse the exact M25 K1 cases and PSD files from run `34548988620`, artifact `10180157389`. No PSD value, support point, sterile-neutrino parameter, cosmology, eta value, or scientific response criterion may change.

CLASS remains pinned to `e85808324f51fc694d12e3ed7439552a3c3f9540`. The already audited capacity-only repair `_QUADRATURE_MAX_=4000`, `_QUADRATURE_MAX_BG_=4000` is allowed so that failure, if any, is due to the tolerance/support interface rather than the stock array ceiling.

## Prospective tolerance ladder

Three independent profiles are fixed before execution and SHOULD be run concurrently for each of the two provider models:

- `t1e6`: `tol_ncdm_bg=1e-6`, `tol_ncdm=1e-6` (source-matched to sterile-dm `D_TOL`).
- `t3e7`: `tol_ncdm_bg=3e-7`, `tol_ncdm=3e-7`.
- `t1e7`: `tol_ncdm_bg=1e-7`, `tol_ncdm=1e-7`.

No other CLASS precision parameter is changed.

## Cases and measurements

For each `(model, tolerance)` job execute the unchanged reference and the three smallest abundance points `eta = 0.01, 0.003, 0.001`. Measure the existing frozen response blocks H, P(k), CMB TT/EE/TE and the same tail-scaling diagnostics already implemented in `m25_k1_precision_floor_diagnostic.py`.

## Interpretation

- Execution failure is `PROVIDER_BLOCKED`, not physical falsification.
- A tolerance profile whose required blocks recover monotonic positive tail scaling is evidence that the previous strict-reference failure was a source/interface precision floor.
- The source-matched `t1e6` profile is the primary physically justified profile; tighter profiles are convergence diagnostics only.
- This diagnostic does not itself promote K1 or K4 and cannot constitute physical falsification.
- No tolerance may be introduced or changed after inspecting these results.
