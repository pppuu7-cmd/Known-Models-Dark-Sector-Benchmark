# W05 M32 DGP K0 EFT-Ramses provider probe preregistration v0.1

Date: 2026-09-11
Family: M32 / F32 DGP braneworld.
Purpose: K0 provenance/infrastructure probe only. This run cannot promote K1-K9 and cannot physically falsify DGP.

## Frozen provider

Public provider: `nat-woodcock/EFT-Ramses`
Pinned commit: `849ddb716041316d0e223ba22badc0d630b72435`.
The provider README states that EFT-Ramses natively covers self-accelerating and normal-branch DGP and documents `cd bin && make` as the build path.

## Frozen checks

The probe runs on a clean GitHub-hosted Ubuntu runner and must:

1. clone the public provider and detach exactly at the pinned commit;
2. verify `git rev-parse HEAD` equals the pin;
3. preserve the provider README and repository file manifest as provenance artifacts;
4. verify the pinned README contains explicit DGP implementation claims for both self-accelerating and/or normal-branch DGP and the Vainshtein/master-equation context;
5. execute the provider-documented infrastructure build command `cd bin && make` without source modification;
6. record exit codes and the first causal build failure if compilation does not complete.

No compiler flags, source files, cosmological parameters, model equations or thresholds may be changed after observing the result.

## Frozen classification

- `M32_K0_PROVIDER_PROBE_PASS_WITH_SCOPE` iff the exact pin is verified, the DGP provenance tokens are present, and the documented build exits zero.
- `M32_K0_BLOCKED_PROVIDER_BUILD` iff provenance is present but the unmodified documented build fails.
- `M32_K0_BLOCKED_PROVENANCE` iff the exact pin or explicit DGP implementation provenance cannot be verified.

A PASS is scoped to provider provenance plus infrastructure executability only. It is not a DGP production cosmology run and therefore does not establish reference/decoupling closure, perturbation closure, numerical robustness, multichannel rank, observation-space discrimination, holdout success, or physical viability.

If this probe passes, the next allowed M32 step is a separately preregistered provider-native DGP production/control calculation using an author-documented DGP configuration or a minimally derived configuration whose equations and parameter mapping are fixed from provider source before execution.
