# W03 M13b K3D2-C gauge-mapped z=5 IVP successor v0.1

Date frozen: 2026-09-14

## Authorization

This successor is authorized only by the terminal source/IVP audit:

`M13B_K3D2B_EQUATIONS_CONSISTENT_IVP_GAUGE_MISMATCH_CONFIRMED`

from workflow run `34792651978`.

The historical parent full result

`M13B_K3D2B_CERTIFIED_DEFAULT_FULL_B123_GAP`

remains immutable evidence for the previously executed synchronous-zero qfield initialization. It is not rewritten or reclassified by this successor.

## Purpose

Repeat the already-frozen default-lane B1+B2+B3 scientific regression on the **same physical K3C2 initial surface** by expressing the frozen K3C2 Newtonian-gauge zero qfield seed in CLASS synchronous-gauge direct-field coordinates at the exact native `z=5` handoff.

This is an initial-coordinate correction only. It is not a late-time sign fix and is not allowed to inspect or fit the desired endpoint sign.

## Exact provider and frozen stack

Provider remains exactly:

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

Apply, without modification, in this order:

1. `verification/m13b/k3d2_apply_class_two_field_adapter_entry.py`;
2. conditional/floating-boundary background restart;
3. background U1 post-handoff seam;
4. native perturbation `z=5` interval split;
5. mapping-certified perturbation tau seam requiring exactly 12 local tau ULP;
6. the new gauge-mapped z=5 IVP transformer frozen by this protocol;
7. output-only diagnostics.

The new transformer may modify only the four direct qfield entries of the mode-local perturbation state at the exact native `z=5` boundary after `perturbations_vector_init()` and before the right-owned `generic_evolver()` begins.

It MUST NOT change:

- background equations;
- qcf/qpf perturbation RHS equations;
- qcf/qpf stress-energy signs;
- Einstein equations/sources;
- photon/polarization hierarchy;
- ur/ncdm hierarchy;
- thermodynamics/recombination;
- primordial module;
- Fourier/nonlinear/lensing physics;
- solver family or integration tolerances;
- the certified 12-ULP perturbation seam;
- any cosmological/model parameter.

## Frozen inverse gauge-map initial condition

The already-frozen B3 transform is

- `delta_x_N = delta_x_S + alpha*phi'`;
- `delta_x_prime_N = delta_x_prime_S + (-2*aH*alpha*phi' - a^2*V_phi*alpha + phi'*alpha')`;
- `delta_y_N = delta_y_S + alpha*psi'`;
- `delta_y_prime_N = delta_y_prime_S + (-2*aH*alpha*psi' + a^2*V_psi*alpha + psi'*alpha')`;
- `r_N = delta_x_prime_N/(aH)`;
- `t_N = delta_y_prime_N/(aH)`.

The frozen K3C2 target at the exact handoff is

`delta_x_N = r_N = delta_y_N = t_N = 0`.

Therefore the synchronous direct-field seed is uniquely fixed, mode by mode, by algebraic inversion:

- `delta_x_S = -alpha*phi'`;
- `delta_x_prime_S = 2*aH*alpha*phi' + a^2*V_phi*alpha - phi'*alpha'`;
- `delta_y_S = -alpha*psi'`;
- `delta_y_prime_S = 2*aH*alpha*psi' - a^2*V_psi*alpha - psi'*alpha'`.

No coefficient, sign, phase, amplitude, or endpoint quantity may be fitted.

At the exact frozen handoff, the left-owned K3C1 background is expected to have `phi'=psi'=0`; this must be measured, not assumed. Because the qfield stress-energy perturbations then vanish on the exact initial surface, the metric used to obtain `alpha,alpha'` should remain unchanged after assigning the four mapped qfield entries. This is a required implementation identity check.

## Boundary implementation identity gate

At the native `z=5` interval boundary, for every scalar mode:

1. refresh exact-boundary background/thermodynamic quantities through existing CLASS functions;
2. evaluate existing `perturbations_einstein()` on the copied pre-map state;
3. read `alpha`, `alpha'`, `a`, `H`, `phi'`, `psi'`, `V_phi`, `V_psi`;
4. assign exactly the four direct qfield entries using the frozen formulas above;
5. reevaluate existing `perturbations_einstein()` without changing any equation;
6. reconstruct the four Newtonian qfield seed quantities with the same frozen formulas.

Frozen raw identity tolerance for this **implementation-only** boundary check:

`max(|delta_x_N|, |r_N|, |delta_y_N|, |t_N|) <= 1e-12`.

This tolerance does not replace or relax any B1/B2/B3 threshold. It is a new preregistered source-implementation identity condition on an exact algebraic zero target.

The implementation must emit a compact `KMDSB_GAUGE_IVP` diagnostic line containing the four residuals for at least the first scalar mode. The diagnostic is output-only.

If the identity gate fails, the scientific result is `IMPLEMENTATION_BLOCKED`; no B3 interpretation is allowed.

## Frozen cosmology and outputs

Exactly preserve the parent certified-default scientific configuration:

- `h = 0.6715`
- `omega_b = 0.0224`
- `Omega_cdm = 0.26172292868512664`
- `Omega_g = 5.4572897176151613e-05`
- `Omega_ur = 3.772710282384838e-05`
- `N_ncdm = 0`
- `Omega_Lambda = Omega_fld = Omega_scf = Omega_k = 0`
- `qcf_U0 = qpf_U0 = 0.3362232603714306`
- `qcf_phi_ini = 0.92`, `qcf_phi_prime_ini = 0`
- `qpf_psi_ini = 1.02`, `qpf_psi_prime_ini = 0`
- synchronous gauge
- `A_s = 2.1e-9`, `n_s = 0.965`, `tau_reio = 0.054`
- `output = tCl,pCl,lCl,mPk,dTk`
- `lensing = yes`
- `l_max_scalars = 1200`
- `P_k_max_1/Mpc = 1.0`
- `z_pk = 0`
- exact frozen direct trajectories `K1=0.00022398828992555914` and `K10=0.0022398828992555913` 1/Mpc.

## Frozen scientific verifier

Use the existing unchanged:

`verification/m13b/k3d2b_verify_full_default.py`

against

`waves/wave_03_expanded_dark_energy/M13B_K3C2_INDEPENDENT_PERTURBATION_BRIDGE_RESULT.json`.

All historical B1/B2/B3 thresholds and the one common mode normalization

`S_k = 1e-5 / Phi_N(z=5)`

remain unchanged.

No per-variable normalization, sign rephasing, endpoint fit, target-dependent adjustment, or post-hoc threshold change is allowed.

## Parallel execution lanes

The following lanes are independent and may be launched simultaneously after this protocol and the transformer are committed:

### S — source/identity guard

Static source audit plus exact-pin compile. Require:

- only the authorized boundary state-assignment block is added beyond the already frozen stack;
- inverse gauge-map formulas appear with the exact signs frozen above;
- no protected equation/tolerance is changed;
- exact provider pin and exact 12-ULP certified seam remain.

### N — strict disabled-null regression

Run identical LambdaCDM controls with qcf/qpf disabled on exact upstream CLASS and the full transformed adapter stack. Require the existing strict null standard:

- provider rc = 0 both sides;
- finite positive P(k);
- normalized P(k) L2 <= `1e-10`;
- relative `H0` difference <= `1e-12`.

The new boundary assignment must be unreachable when qcf/qpf are disabled.

### D — enabled default full B1+B2+B3

Run the frozen default NDF15 full Boltzmann cosmology and the unchanged historical verifier. Also require the boundary implementation identity diagnostic to pass `1e-12`.

These three lanes may execute concurrently for efficiency; no scientific promotion occurs until the aggregate verdict sees all three terminal artifacts.

## Aggregate classifications

If S PASS, N PASS, boundary identity PASS, and unchanged verifier B1+B2+B3 all PASS:

`M13B_K3D2C_GAUGE_MAPPED_Z5_IVP_DEFAULT_B123_PASS_WITH_SCOPE`.

If implementation/source/null guard fails before a valid scientific comparison:

`M13B_K3D2C_GAUGE_MAPPED_Z5_IVP_IMPLEMENTATION_BLOCKED`.

If guards pass and B1/B2/B3 executes but any historical scientific gate fails:

`M13B_K3D2C_GAUGE_MAPPED_Z5_IVP_SCIENTIFIC_GAP`.

Even PASS means only:

- same-initial-surface B1/B2/B3 is established for the certified default NDF15 lane;
- reference precision robustness remains open/blocked by its separately localized non-frozen-mode stiffness issue;
- K3 remains at most `PARTIAL` until the repository's broader K3 closure requirements are explicitly satisfied;
- K4 and K5 are not promoted.

All outcomes preserve:

- `historical_parent_B3_rewritten=false`;
- `author_model_reproduced=false`;
- `published_V0_reproduced=false`;
- `author_normalization_map_claimed=false`;
- `physical_falsification=false`.
