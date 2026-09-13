# W03 M13b K3D2-B certified default full B1+B2+B3 evidence v0.1

Date: 2026-09-14

## Purpose

Evaluate the already-frozen scientific B1+B2+B3 default-lane gates using the mapping-certified perturbation seam that has passed the exact source guard, strict disabled-null reduction, and enabled default NDF15 implementation gate.

This is **default-lane scientific evidence only**. It cannot establish the full K3D2-B two-precision regression while the frozen `cl_ref.pre` reference RK lane remains numerically blocked.

Provider remains exactly:

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Frozen implementation stack

Apply, without modification:

1. `verification/m13b/k3d2_apply_class_two_field_adapter_entry.py`;
2. conditional/floating-boundary background restart;
3. background U1 post-handoff seam;
4. native perturbation z=5 interval split;
5. mapping-certified perturbation tau seam requiring exactly 12 local tau ULP;
6. output-only diagnostics.

No diagnostic solver patch is allowed in the scientific run.

## Frozen cosmology/output request

Use exactly:

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
- exact K1/K10 direct perturbation trajectories.

## Frozen verifier

Run the existing unchanged:

`verification/m13b/k3d2b_verify_full_default.py`

against canonical:

`waves/wave_03_expanded_dark_energy/M13B_K3C2_INDEPENDENT_PERTURBATION_BRIDGE_RESULT.json`.

Do not modify any threshold.

The existing verifier freezes:

- B1 background/crossing/today/energy gates;
- B2 finite positive P(k), finite C_l, nonnegative TT/EE, hierarchy presence, and linearity gate;
- B3 K1/K10 gauge-converted endpoint sign and ratio gates against the existing K3C2 canonical perturbation bridge.

## Parallel lanes

### S — source audit

Independently verify the certified stack, exact signs, exact 12-ULP runtime implementation, and output-only nature of diagnostics.

### D — full scientific default run

Run full CLASS with default NDF15 and the frozen output request, then execute the unchanged B1+B2+B3 verifier.

## Classification

- S PASS + D verifier PASS -> `M13B_K3D2B_CERTIFIED_DEFAULT_FULL_B123_PASS_WITH_SCOPE`.
- Otherwise -> `M13B_K3D2B_CERTIFIED_DEFAULT_FULL_B123_GAP` with the first failed frozen gate recorded.

Even a PASS means only:

- B1/B2/B3 are established for the certified **default NDF15 lane**;
- reference precision robustness remains open/blocked;
- full K3D2-B regression is not yet established;
- K3 ceiling remains PARTIAL and K4/K5 are not promoted.

All outcomes preserve `author_model_reproduced=false`, `published_V0_reproduced=false`, `author_normalization_map_claimed=false`, and `physical_falsification=false`.