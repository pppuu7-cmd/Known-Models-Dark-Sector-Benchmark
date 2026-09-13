# W03 M13b K3D2-B enabled qcf+qpf CLASS cosmology regression v0.1

Frozen: 2026-09-14 before the first enabled `qcf+qpf` CLASS execution.

Parent gate: `M13B_K3D2_CLASS_TWO_FIELD_SPECIES_ADAPTER_BUILD_AND_REDUCTION_PASS_WITH_SCOPE`.
Parent result: `waves/wave_03_expanded_dark_energy/M13B_K3D2_CLASS_TWO_FIELD_SPECIES_ADAPTER_RESULT.json`.
Provider base: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Independent realization: `qcf+qpf`; upstream `scf` remains a protected control and is not part of the realization.

## Purpose

K3D2-B is the first enabled full-Einstein-Boltzmann execution of the independent M13b direct-field realization. It asks whether the already validated K3C1/K3C2 canonical+phantom realization survives embedding in the exact CLASS photon/ultra-relativistic/recombination hierarchy without moving any frozen normalization or crossing criterion after seeing an enabled result.

A PASS is still **K3 PARTIAL**. It is not author-code reproduction, not a public-`V0` normalization claim, and does not authorize K4/K5.

## Frozen cosmological binding

Use exactly:

- `h = 0.6715` (`H0 = 67.15 km/s/Mpc`);
- `Omega_m0 = 0.3114` total;
- `omega_b = 0.0224`;
- `Omega_b = omega_b/h^2 = 0.04967707131487335`;
- `Omega_cdm = 0.26172292868512664` so `Omega_b+Omega_cdm=0.3114` exactly to recorded precision;
- `Omega_r0 = 9.23e-5` exactly;
- radiation split by the exact-pin CLASS massless-neutrino convention with `Neff=3.044` and `coeff=(1.70961e-05/2.47298e-05/3.044)=0.2271076677147105`:
  - `Omega_g = 5.4572897176151613e-05`,
  - `Omega_ur = 3.772710282384838e-05`,
  - their sum must equal `9.23e-5`;
- `Omega_Lambda = 0`, `Omega_fld = 0`, `Omega_scf = 0`, `Omega_k = 0`;
- no massive ncdm species in this gate;
- standard scalar adiabatic primordial control: `A_s=2.1e-9`, `n_s=0.965`, `tau_reio=0.054`;
- `qcf_U0=qpf_U0=0.3362232603714306`;
- `qcf_phi_ini=0.92`, `qcf_phi_prime_ini=0`;
- `qpf_psi_ini=1.02`, `qpf_psi_prime_ini=0`;
- potential shape `U(x)=U0[tanh(29(1-x))+1]` and CLASS map `V_class=3 H0^2 U` exactly as K3D2-A;
- runtime gauge remains synchronous for the qcf/qpf evolution.

No public Goh-Taylor amplitude is admitted. `published_V0_reproduced=false` and `author_normalization_map_claimed=false` are frozen.

## Frozen modes

Reuse the K3C2 mode labels exactly via

`k = k_hat * H0/c` in `1/Mpc`, with `c=299792.458 km/s`:

- `k_hat=1`: `k=0.00022398828992555914 1/Mpc`;
- `k_hat=10`: `k=0.0022398828992555913 1/Mpc`.

## Lane B1 — enabled background/crossing regression against K3C1

CLASS must write the background table with qcf/qpf diagnostic columns. Convert its direct-field derivatives to K3C1 variables by

- `p = phi'_qcf/(a H)`;
- `q = psi'_qpf/(a H)`;
- `D=p^2-q^2`.

Interpolate in `N=ln(a)` without fitting or rephasing.

K3C1 authorities are fixed to:

- crossing `z_x = 1.1978720736725847`;
- today `x=1.3910277872721561`;
- today `p=0.3117003532815687`;
- today `y=0.7979144626637236`;
- today `q=-0.02751848184245475`;
- today `Omega_DE=0.6885076999845492`;
- today `E=H/H0=0.9999999999923376`.

All B1 gates must pass:

1. execution finite from the CLASS initial epoch through today;
2. all sampled total and qcf/qpf background densities finite, total H positive;
3. at `z=5`, `|x-0.92| <= 2e-4` and `|y-1.02| <= 2e-4`;
4. at `z=5`, `|p| <= 2e-3` and `|q| <= 2e-3`;
5. exactly one negative-to-positive `D` crossing in `0<z<5`;
6. `|z_x_CLASS-z_x_K3C1| <= 0.02`;
7. at today, `|x-x_K3C1| <= 5e-3`;
8. at today, `|y-y_K3C1| <= 5e-3`;
9. at today, `|p-p_K3C1| <= 5e-3`;
10. at today, `|q-q_K3C1| <= 2e-3`;
11. `|E0-1| <= 3e-3`;
12. `|Omega_DE0-0.6885076999845492| <= 3e-3`;
13. `D(z=5)<0` after the initial transient tolerance and `D(z=0)>0`;
14. no denominator proportional to combined qcf+qpf `rho+p` is introduced.

These are regression tolerances for an independent CLASS embedding, not observational-fit tolerances.

## Lane B2 — full Boltzmann finiteness and precision reproducibility

The enabled realization must run the standard CLASS photon temperature/polarization hierarchy, massless ultra-relativistic hierarchy, recombination/thermodynamics, scalar transfer functions and linear matter spectrum.

Request at least `tCl,pCl,lCl,mPk,dTk` with `P_k_max_1/Mpc >= 1` and scalar `l_max_scalars >= 1200`.

Required default-run gates:

1. provider return code zero;
2. CMB TT/EE and linear P(k) arrays present and finite;
3. TT/EE auto spectra are non-negative within ordinary floating-point roundoff where defined;
4. linear P(k)>0 on every reported positive-k row;
5. no NaN/Inf in the two requested mode diagnostic trajectories;
6. photon and `ur` hierarchy variables are present for both frozen modes;
7. qcf/qpf direct perturbations are dynamically sourced by today and remain in the linear domain (`max absolute direct-field perturbation < 0.1` after primordial normalization).

Independently repeat with the exact-pin `cl_ref.pre` precision profile. Between default and reference-precision runs require:

- background crossing redshift absolute difference `<=2e-3`;
- each today qcf/qpf background field/velocity absolute difference `<=1e-3`;
- linear P(k) normalized L2 on the common reported grid `<=5e-3`;
- TT normalized L2 for common `30<=ell<=1200` `<=5e-3`.

If a particular precision file is incompatible with the exact current output request for an infrastructure-only reason, the recovery may remove an irrelevant output request but may not loosen these numerical thresholds or change cosmology.

## Lane B3 — K3C2 mode-response bridge

K3C2 is an ideal-fluid Newtonian-gauge bridge beginning at `z=5` with `Phi_i=1e-5`; CLASS begins in the primordial era with an adiabatic spectrum and includes free-streaming radiation. Therefore raw amplitudes and raw synchronous direct-field perturbations are not comparable quantities.

The comparison is frozen as follows.

### Diagnostic transformation

For each frozen mode, output synchronous qcf/qpf direct perturbations and the CLASS synchronous metric gauge generator `alpha` and `alpha'`. Construct Newtonian direct-field variables using the exact scalar gauge transformation:

Canonical qcf:

- `delta_x_N = delta_x_S + alpha*phi'_qcf`;
- `delta_x_prime_N = delta_x_prime_S + (-2*aH*alpha*phi'_qcf - a^2*V_phi*alpha + phi'_qcf*alpha')`.

Phantom qpf:

- `delta_y_N = delta_y_S + alpha*psi'_qpf`;
- `delta_y_prime_N = delta_y_prime_S + (-2*aH*alpha*psi'_qpf + a^2*V_psi*alpha + psi'_qpf*alpha')`.

Convert derivatives to K3C2 e-fold variables:

- `r_N=delta_x_prime_N/(aH)`;
- `t_N=delta_y_prime_N/(aH)`.

Use CLASS's Newtonian potentials reconstructed from the same metric workspace:

- `Phi_N = eta-aH*alpha`;
- `Psi_N = aH*alpha+alpha'`.

### Amplitude bridge

At the first interpolated `z=5` sample define one scalar normalization per mode

`S_k = 1e-5 / Phi_N_CLASS(z=5)`.

Multiply all CLASS linear perturbations used in the comparison by this same `S_k`. No per-variable rescaling, phase fitting, sign flip, or endpoint fitting is allowed.

### Frozen K3C2 endpoint authorities

For `k_hat=1` at today:

- `Phi=8.083099993041364e-06`;
- `delta_x=1.9491236631664044e-06`;
- `r=-5.980153358981784e-06`;
- `delta_y=-4.5224999400478597e-07`;
- `t=5.889221469765459e-07`.

For `k_hat=10` at today, the values are taken verbatim from the canonical K3C2 result file at execution time; the verifier must hash that file before reading them and must not modify it.

Because CLASS contains physical radiation history absent from K3C2, B3 is a bridge/response test rather than equality. For each mode require:

1. finite `Phi_N,delta_x_N,r_N,delta_y_N,t_N` throughout `0<=z<=5`;
2. finite nonzero `Phi_N_CLASS(z=5)` so `S_k` is defined;
3. the signs of all five today quantities match the canonical K3C2 signs, excluding a variable only if its K3C2 magnitude is below `1e-12` (none is expected to be excluded);
4. today potential amplitude ratio after the one common rescaling lies in `[0.5,2.0]` relative to K3C2;
5. for each of `delta_x,r,delta_y,t`, the absolute-amplitude ratio after the one common rescaling lies in `[0.2,5.0]` relative to K3C2;
6. qcf and qpf perturbations are not identically zero;
7. no evolution or diagnostic transformation divides by combined qcf+qpf `rho+p`, `D`, or an effective `theta_DE`.

The broad field-amplitude ratios are frozen deliberately before execution because the two systems have different pre-z=5 radiation histories. Passing them establishes same-sign, same-order direct-field response on the same background/modes, not numerical identity.

## Diagnostic-only source extension

K3D2-B may add output-only diagnostic columns inside the already touched `source/perturbations.c` and/or `source/output.c`, provided:

- no photon, polarization, ur/ncdm, thermodynamics, primordial, Einstein, qcf or qpf evolution equation is changed from the K3D2-A adapter;
- an automated diff audit proves all changes outside diagnostic title/data blocks are absent;
- null qcf/qpf regression from K3D2-A remains unchanged when the adapter is disabled.

## Classification

PASS only if B1, B2 and B3 all pass prospectively frozen gates:

`M13B_K3D2B_ENABLED_FULL_BOLTZMANN_COSMOLOGY_REGRESSION_PASS_WITH_SCOPE`

Even on PASS:

- `K3_state_ceiling = PARTIAL`;
- `K4_promoted=false`;
- `K5_promoted=false`;
- `author_model_reproduced=false`;
- `published_V0_reproduced=false`;
- `author_normalization_map_claimed=false`;
- `physical_falsification=false`.

If B1 fails materially, do not interpret B2/B3 as model falsification until the normalization/background binding is audited. If only B3 fails while B1/B2 pass, classify it as a perturbation-regression gap and localize gauge/initial-history causes before any physics claim.
