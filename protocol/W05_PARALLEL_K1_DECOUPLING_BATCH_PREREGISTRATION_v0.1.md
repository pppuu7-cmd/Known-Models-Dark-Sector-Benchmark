# W05/W04 parallel K1 decoupling batch — preregistration v0.1

Purpose: deepen already executable provider routes without converting provider/provenance/numerical limitations into physical failures. This batch is prospectively frozen before its workflow is launched.

Independent lanes

- M24 ETHOS-like IDM–DR, pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`. Use the scalar ETHOS closure (`alpha_idm_dr=1.5`) and vary only `a_idm_dr`: reference 0; active ladder `1e6,1e5,1e4,1e3`.
- M35 Einstein-Aether/LV gravity, pinned `Michalychforever/CLASS_LVDM@d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`. Reference is the provider's committed `lcdm.ini`. Active ladder scales the committed Misha gravity parameters `(alpha,beta,lambda)=(0.05,0.25,-0.1)` by `s=1,0.1,0.01,0.001`; `Y_dm=0` throughout. This tests only the pinned scalar-sector aether/LV route, not full Einstein-Aether SVT closure.
- M37 f(T), pinned `Speeddemon5050/Modified-CLASS-fT-Exact-@74e6a8679cdc233fb339c67127ed0921ba547894`. Reference `n_fT=0`; active ladder `n_fT=0.1,0.01,0.001,0.0001`. M37 K0 provenance remains open/PARTIAL regardless of K1 numerical outcome.

Frozen observables: unlensed scalar TT and linear z=0 P(k) on each provider's native output grids, using the same cosmology within each lane. Undefined/missing outputs fail closed as provider/numerical BLOCKED, never as physical FAIL.

For each lane define `D(x)=max(d_TT(x),d_Pk(x))`, where each d is normalized L2 after interpolation to the overlapping reference grid. Order active points from largest to smallest absolute coupling/scale. A scoped K1 decoupling PASS requires all of:

1. exact provider pin matches;
2. reference and all four active arms exit zero and emit finite TT and P(k);
3. `D_finest < D_coarsest`;
4. no finer point exceeds 1.20 times the immediately coarser D;
5. `D_finest / D_coarsest <= 0.25`;
6. Pearson correlation of `log10(|x|)` and `log10(D)` is at least 0.90, with positive orientation.

Classification rules:

- all frozen criteria pass: `K1_PASS_WITH_SCOPE_DECOUPLING_LADDER` for the provider route;
- executable but convergence criteria fail: `K1_NOT_ESTABLISHED_DECOUPLING_LADDER` (not physical falsification);
- build/execution/output failure: `K1_BLOCKED_IMPLEMENTATION_OR_NUMERICAL`;
- M37 can at most establish a scoped numerical/reference-limit property while its K0 provenance remains PARTIAL; this batch must not upgrade M37 K0.

No thresholds or ladder points may be changed after seeing outputs. K2+ remain open and are not authorized by mere workflow success.