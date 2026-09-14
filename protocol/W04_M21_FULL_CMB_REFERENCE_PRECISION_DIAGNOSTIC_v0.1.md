# W04 M21 full CMB reference-precision diagnostic v0.1

Frozen: 2026-09-14 before any new `cl_ref.pre` execution.

Family: F21 / M21 mixed cold+warm dark matter  
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`  
Parent integrator result: `waves/wave_04_dark_matter/M21_INTEGRATOR_BRANCH_DIAGNOSTIC_RESULT.json`  
Parent raw artifact: run `34542162543`, artifact `10178334419`, digest `sha256:640472f79c7e55d9edf4ed39ed35d4ab692fcf4700fad4d50edbad0642f7c65c`  
Parent ell localization: `M21_CMB_ELL_BAND_LOCALIZATION_PASS_WITH_SCOPE`.

## Trigger

The f_w=0.003 CMB anomaly survives both NDF15 and RK. Artifact-only localization shows a consistent `MID_LOCALIZED` residual pattern in TT/EE/TE, with ell=501..1200 carrying roughly 74--85% of f3 residual energy, while low-ell has no isolated f3 excursion. H and P(k) remain smooth.

The next high-information numerical question is whether the anomaly survives the provider's own full CMB reference-precision profile, rather than only the previous `cl_permille.pre + m21_ncdm_tight.pre` profile.

## Frozen cases

Regenerate exactly the existing physical cases with

`verification/m21/mixed_cold_warm_k1_reference.py prepare`.

Execute independently:

- `ref`;
- `f2`: f_w=0.01;
- `f3`: f_w=0.003;
- `f4`: f_w=0.001.

No model, cosmology, mass, temperature, abundance, primordial, output, gauge, k-range or l_max change is allowed.

## Frozen precision change

Use the exact provider file `cl_ref.pre` from the pinned commit, with no appended M21 overrides. This is deliberate: `verification/m21/m21_ncdm_tight.pre` is a source-bound subset of this same `cl_ref.pre`, while the full file additionally tightens recombination, perturbation start/sampling, photon/UR hierarchy, k/q/l transfer sampling and CMB source-retention settings. `cl_ref.pre` also fixes `evolver=0` (RK); the parent diagnostic already established that RK alone does not remove the f3 excursion.

The scientific change in this gate is therefore one frozen object: the provider's complete reference CMB precision profile.

## Parallel execution

Run ref/f2/f3/f4 as four independent fresh-clone jobs. Each must record exact provider HEAD, SHA256 of `cl_ref.pre`, INI hash, provider return code, CMB Cl, P(k), background, and build/run logs. No lane may inspect another lane's substantive output before completion.

## Frozen metrics

Use the same whole-vector metrics as `verification/m21/integrator_branch_diagnostic.py`:

- TT, EE, TE normalized L2 against ref on identical ell grids;
- P(k) normalized L2 on common log-k overlap;
- H normalized L2 on common z overlap.

For each channel define f3 excursion factor

`E = R2(f3) / max(R2(f2), R2(f4), 1e-300)`.

Also compute the frozen four ell bands from `protocol/W04_M21_CMB_ELL_BAND_LOCALIZATION_v0.1.md` and f3 residual-energy shares, to verify whether the mid-ell localization persists.

Compare each new `cl_ref.pre` Cl and P(k) output directly against the corresponding parent **RK P2** raw output from immutable artifact `10178334419` using normalized L2 on identical/common support. This direct comparison diagnoses how much the full CMB precision profile changes each case.

## Controls

1. Exact provider HEAD required.
2. `cl_ref.pre` SHA256 must be identical in all four lanes.
3. All provider runs rc=0 and outputs finite.
4. Parent raw artifact identity recorded exactly.
5. f2/f3/f4 physical INIs must match the existing prepare script; no post-hoc lane-specific precision or physics changes.

## Frozen classifications

Let `Emax_ref = max(E_TT,E_EE,E_TE)` under full `cl_ref.pre`.
Let parent RK value be frozen from the canonical result: `Emax_parent_RK = 534.8355868817356`.

- `M21_FULL_CMB_REFERENCE_PRECISION_REMOVES_EXCURSION` if each TT/EE/TE excursion factor <=3.
- `M21_FULL_CMB_REFERENCE_PRECISION_REDUCES_EXCURSION` if the removal condition fails but `Emax_ref <= Emax_parent_RK/3`.
- `M21_FULL_CMB_REFERENCE_PRECISION_EXCURSION_PERSISTS` otherwise.
- malformed/nonfinite/missing evidence: `M21_FULL_CMB_REFERENCE_PRECISION_BLOCKED`.

No classification promotes K1. A reduction/removal localizes the problem to numerical CMB precision/sampling; persistence makes a generic insufficient-CMB-precision explanation much less plausible and shifts the next gate toward more specific source/transfer or phase-space mechanisms.

## Interpretation ceiling

`K1_promoted=false`, `physical_falsification=false`. This is a numerical localization diagnostic only; it is not a physical test of mixed warm dark matter.
