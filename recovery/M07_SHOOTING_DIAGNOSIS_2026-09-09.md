# M07 scalar-field shooting diagnosis — 2026-09-09

Status: ACTIVE DIAGNOSTIC HANDOFF
Wave: W03 Expanded dark-energy mechanisms
Model: M07 canonical scalar-field / quintessence
W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`
Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Why this file exists

This record prevents a fresh chat from interpreting failed M07 implementation probes as physical evidence against quintessence. The observed failure is in normalization shooting / numerical initialization.

## Run #4 evidence

GitHub Actions run: `34320181943`
Head: `23cae745230aeec235528beeac64316e5bfac910`
Artifact: `w03-m07-quintessence-probe`, artifact id `10091829523`, digest `sha256:72b277bf6976eda9b00332c13b183e4c0bccaecf2132cfcfd2d4eb7bd7641d6e`.

The pinned CLASS build succeeded. The pure LambdaCDM case exited 0. Every scalar case (`lambda=0,0.05,0.10,0.20`) exited 1 with the same background shooting failure ending in an NDF15 `Step size too small` error. Therefore the shared failure mode is upstream of any scientific finite-lambda comparison.

## Frozen branch and failed seed

M07 uses

`V(phi) = (1+A) exp(-lambda phi)`

with `alpha=0`, `B=0`, explicit `phi_ini=1`, `phi_prime_ini=0`, physical `lambda`, and `scf_tuning_index=2` so `A` is the normalization/shooting nuisance.

Run #4 seeded `A=0` for all scalar cases.

For a constant-field lambda-zero control,

`rho_phi = V/3`, `p_phi=-rho_phi`.

For target `Omega_scf=0.10`, CLASS background normalization implies the required late-time potential scale is of order

`V_target = 3 Omega_scf H0^2`,

with `H0 = 100 h / c` in `Mpc^-1`.

At `h=0.67`, this is approximately `1.50e-8 Mpc^-2`, so for lambda=0

`A_seed ~= V_target - 1 ~= -0.999999985`.

For finite lambda and the initial `phi=1`, the scale-matched seed is

`A_seed(lambda) = 3 Omega_scf H0^2 exp(lambda phi_ini) - 1`.

Thus the old `A=0` starting point puts the scalar potential about eight orders of magnitude above the desired late-time density scale before the root finder reaches its target. This provides a concrete numerical explanation for the stiff background/shooting failure.

## Source-level semantic checks

Pinned CLASS `input.c` treats `Omega_scf` as a shooting target and maps it to `scf_shooting_parameter`. The selected `scf_tuning_index` controls which entry of `scf_parameters` is adjusted. KMDSB keeps index 2 (`A`) so the physical slope `lambda` is not tuned away.

The official explanatory input also documents `scf_tuning_index` as the scalar-field shooting parameter selector. This separation remains a non-negotiable M07 provenance rule.

## Repair chronology

1. Commit `52c4f3e523f32d033cacf130b0f2cda384a682ba` changed the workflow to compute an analytic near-target `A` seed. Its run #5 failed at workflow parsing before any job was created; this is a YAML-only failure and has no scientific meaning.
2. Commit `e74f798a685f8b92f75ef3afe0b4be03eb51a576` fixed the YAML while retaining the same analytic seed formula.
3. Actions run #6: `34325977559`. At this checkpoint it is queued.

## Interpretation rules

- Do NOT label M07 `PHYSICAL_DOMAIN_FAIL` from runs #1-#5.
- Do NOT use finite-lambda infrastructure samples as B8 evidence.
- If run #6 succeeds, first measure the lambda-zero reference residual floor and only then preregister the production B1 tolerance.
- If run #6 still fails, inspect the preserved scalar logs and achieved/tuned parameter semantics before altering the physical branch.
- Any change to lambda, kinetic sign, potential family, or initial-condition physics is a scientific branch change and must not be disguised as a numerical repair.

## Immediate continuation

Inspect Actions run `34325977559` and its artifact. Required sequence:

1. REF exit must be 0.
2. SCF_SPLIT_L0 exit must be 0 before B1 can advance.
3. Analyze `max_abs_lnH` and `max_abs_lnP` of lambda-zero versus LambdaCDM.
4. Freeze a numerical tolerance with explicit safety margin before production finite-lambda science.
5. Only then advance M07 B1-B4 and comparator attacks against M01 and M05.
