# W03 M13b K3D2-C self-consistent gauge-IVP recovery v0.1

Date frozen: 2026-09-14

## Trigger

The prospectively frozen one-step K3D2-C gauge-mapped z=5 IVP run `34793111419` terminated as

`M13B_K3D2C_GAUGE_MAPPED_Z5_IVP_IMPLEMENTATION_BLOCKED`.

The immutable enabled artifact showed that the exact-boundary background interpolant has small nonzero field velocities and that a single inverse gauge-map assignment weakly changes the Einstein metric:

- `phi' = 4.563712872814291e-10`;
- `psi' = -8.753067993605835e-09`;
- first one-step maximum Newtonian zero-target residual `1.3888839265511165e-07`;
- frozen identity tolerance `1e-12`.

The scientific B1/B2/B3 verifier was not evaluated in that run. The independent strict disabled-null control passed with P(k) normalized L2 `4.2828210457354356e-16`.

## Purpose

Solve the **same** already-frozen inverse gauge-map initial condition self-consistently with the **unchanged** CLASS Einstein constraints at the exact native z=5 boundary.

This recovery changes only the numerical method used to satisfy the boundary coordinate/constraint identity. It does not change the physical target, gauge transform, equations, cosmology, scientific thresholds, solver family, integration tolerances, certified seam, or endpoint interpretation.

## Exact fixed-point map

The target remains exactly

`delta_x_N = r_N = delta_y_N = t_N = 0`.

At each iteration, using the current unmodified CLASS synchronous metric values `alpha, alpha'` at the exact boundary, overwrite only:

- `delta_x_S = -alpha*phi'`;
- `delta_x_prime_S = 2*aH*alpha*phi' + a^2*V_phi*alpha - phi'*alpha'`;
- `delta_y_S = -alpha*psi'`;
- `delta_y_prime_S = 2*aH*alpha*psi' - a^2*V_psi*alpha - psi'*alpha'`.

Then reevaluate the existing unmodified `perturbations_einstein()` and reconstruct the same four Newtonian residuals.

The next iteration, if needed, uses the newly returned `alpha,alpha'` with the same algebraic map.

## Frozen iteration algorithm

- pure Picard/fixed-point iteration;
- no damping;
- no relaxation coefficient;
- no line search;
- no Newton/Jacobian fit;
- no endpoint data;
- no per-mode fitted parameter;
- maximum `16` assignment/Einstein iterations;
- terminate at the first iteration satisfying
  `max(|delta_x_N|,|r_N|,|delta_y_N|,|t_N|) <= 1e-12`;
- all residuals and metric values must remain finite;
- if the tolerance is not reached within 16 iterations, classify implementation blocked and do not run/interpret B1/B2/B3.

The `1e-12` target is exactly the already-preregistered K3D2-C boundary identity tolerance; it is not relaxed.

Emit output-only diagnostics for the first scalar mode:

`KMDSB_GAUGE_IVP_FIXED iter=<n> ... max=<residual>`

and a final line with the number of iterations and final residual.

## Frozen provider/stack and science target

Preserve exactly the K3D2-C preregistration:

- provider `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`;
- independent qcf+qpf adapter equations/signs;
- conditional background restart;
- background U1 seam;
- native perturbation z=5 interval split;
- mapping-certified perturbation tau seam requiring exactly 12 local tau ULP;
- same model/cosmology parameters;
- same synchronous gauge;
- same full outputs and lensing settings;
- same frozen K1/K10 trajectories;
- same common `S_k=1e-5/Phi_N(z=5)` normalization;
- same unchanged `verification/m13b/k3d2b_verify_full_default.py`;
- all historical B1/B2/B3 thresholds unchanged.

## Protected code

The recovery may modify only the boundary assignment block in `source/perturbations.c` after the native `perturbations_vector_init()` and before the right-owned evolver. It must not modify any background/qfield RHS, stress-energy, Einstein equation, Boltzmann hierarchy, thermodynamics, primordial/Fourier/lensing physics, solver/tolerance, or model/cosmology parameter.

## Parallel lanes

Launch independently in one workflow:

### S — source + compile guard

Require exact 16-iteration cap, undamped update, exact inverse-map formulas, original `1e-12` target, exact 12-ULP seam, no protected code change, and compile success.

### N — strict disabled-null

Repeat exact upstream versus full transformed stack with qfields disabled. Require:

- both rc=0;
- finite positive P(k);
- normalized P(k) L2 <= `1e-10`;
- relative H0 difference <= `1e-12`.

### D — enabled default science

Run the frozen full default NDF15 cosmology. The boundary fixed point must converge before the historical verifier is executed. If converged, run the unchanged B1/B2/B3 verifier.

The three jobs may run concurrently. Aggregate only after all three artifacts are terminal.

## Classification

If S and N pass, the boundary fixed point converges within 16 undamped iterations to <=1e-12, and unchanged B1/B2/B3 all pass:

`M13B_K3D2C_SELF_CONSISTENT_GAUGE_IVP_DEFAULT_B123_PASS_WITH_SCOPE`.

If S/N/fixed-point implementation fails:

`M13B_K3D2C_SELF_CONSISTENT_GAUGE_IVP_IMPLEMENTATION_BLOCKED`.

If implementation passes and B1/B2/B3 executes but any historical scientific gate fails:

`M13B_K3D2C_SELF_CONSISTENT_GAUGE_IVP_SCIENTIFIC_GAP`.

No outcome rewrites the historical synchronous-zero B3 result or the one-step implementation blocker.

Even PASS retains:

- `K3_state_ceiling=PARTIAL` pending explicit broader K3 closure;
- `K4_promoted=false`;
- `K5_promoted=false`;
- reference precision robustness remains open/blocked by its separately localized non-frozen-mode RK stiffness issue;
- `author_model_reproduced=false`;
- `published_V0_reproduced=false`;
- `author_normalization_map_claimed=false`;
- `physical_falsification=false`.
