# W04 M27 N=1 reference conditioning audit preregistration v0.1

## Trigger

After the JSON-only recovery, the first completed branch of run `34555747835` passes all N=64 ensemble positivity/monotonicity/source-integral gates. Its N=1 comparison has `H_p95 ~ 1.3e-10` and parent `p95 ~ 3.5e-10`, but daughter-radiation `p95 ~ 3.4e-5`, above the frozen `1e-7` reference gate. The direct N=1 control integrates physical densities starting from `rho_parent(a_i)=Omega_DDM a_i^-3 ~ 2.6e14` while `rho_dr(a_i)=0`, creating a severe dynamic-range conditioning problem absent from H and the parent solution.

This audit tests numerical conditioning only. It does not alter the physical equations or acceptance threshold.

## Frozen physics

Use the same N=1 DCDM system, cosmological normalization, `a_i=1e-5`, DOP853, `rtol=1e-10`, `atol=1e-12`, and 4001 log-a points as the parent M27 energy-transfer preregistration.

Test independently `Gamma0/H* in {0.03,0.3,3.0}`.

## Alternative but algebraically identical variables

Instead of integrating physical densities `[rho_parent,rho_dr]`, integrate the comoving variables

- `R = a^3 rho_parent`
- `D = a^4 rho_dr`

with exact transformed equations

`dt/dx = 1/H`

`dR/dx = -(Gamma/H) R`

`dD/dx = a (Gamma/H) R`

and

`H^2 = Omega_r a^-4 + Omega_b a^-3 + Omega_Lambda + R a^-3 + D a^-4`.

Initial conditions are `t=0`, `R=Omega_DDM`, `D=0`.

No rescaling, floor, smoothing, or tolerance adjustment is permitted.

## Reference

Compare the comoving direct system with the existing exact-survival N=1 representation specialized from the ensemble code. Reconstruct physical densities only after integration.

Retain the frozen p95 symmetric-relative thresholds `<=1e-7` for H, parent and daughter radiation. For daughter radiation, use the same support mask as the parent comparison.

## Decision

- `M27_N1_COMOVING_REFERENCE_PASS` iff all three channels pass at a tested Gamma0.
- Aggregate `M27_N1_COMOVING_REFERENCE_CONDITIONING_RECOVERED` iff all three Gamma0 values pass.

A pass permits a separately preregistered analysis-only recovery of the 27 branch results using the algebraically identical comoving N=1 reference. A failure requires further numerical audit and cannot be interpreted as DDM physics failure.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
