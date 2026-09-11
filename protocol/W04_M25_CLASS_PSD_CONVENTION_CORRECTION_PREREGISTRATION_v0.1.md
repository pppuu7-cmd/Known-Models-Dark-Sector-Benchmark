# W04 M25 CLASS PSD convention correction preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE CORRECTED EXECUTION
Family: F25 / M25 resonantly produced sterile-neutrino-like WDM
Sterile provider: `ntveem/sterile-dm@e4486265e8207aa0dd28decc8c8d897266c0a52a`
CLASS provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Parent provider-control run: `34544624039`
Parent bridge run: `34545741673`
Parent qmax4000 recovery run: `34546960152`
Parent classification: `M25_CLASS_BRIDGE_QMAX4000_DENSITY_NOT_VALIDATED`

## Source-derived correction
The parent bridge used `f0_wrong=(f_s+f_sbar)/2`, treating CLASS tabulated `f0` as an occupation-number average. This is not CLASS's native convention.

At the pinned CLASS source, the analytic zero-chemical-potential ncdm distribution is

`f0_CLASS = (1/(2*pi)^3) * [1/(exp(q)+1) + 1/(exp(q)+1)]`,

and the shipped `psd_FD_single.dat` follows the same convention. Therefore, for the sterile provider's separately tabulated particle and antiparticle occupation functions, the source-matched file convention is

`f0_correct(q) = (f_s(q) + f_sbar(q)) / (2*pi)^3`.

This is a convention correction derived from provider source, not a fitted renormalization. The old-to-correct multiplicative ratio is frozen analytically as

`f0_wrong/f0_correct = (2*pi)^3/2 = 124.02510672119926`,

which independently explains the approximately 124-fold density excess seen in the parent qmax4000 run.

## Frozen unchanged physics and mapping
Keep unchanged:
- snapshot: `Snapshot100.dat` from immutable provider-control run `34544624039`;
- final snapshot temperature check: `T_snapshot=10 MeV` within relative `1e-10`;
- `q=p_snapshot/T_snapshot`;
- `T_ncdm/T_gamma=(4/11)^(1/3)`;
- `m_ncdm=7115 eV`;
- `deg_ncdm=1`;
- same background cosmology;
- do not pass `omega_ncdm` or `Omega_ncdm`;
- no smoothing, clipping, interpolation change, tail edit, resampling, or fitted normalization of the sterile PSD.

Because the parent automatic CLASS background quadrature hit the compiled 800-point ceiling before the convention error could be measured, retain the already-preregistered capacity-only compile change `_QUADRATURE_MAX_BG_: 800 -> 4000`, with the provider accuracy tolerance `tol_ncdm_bg=1e-5` unchanged. No further cap increase is authorized here.

## Frozen controls and gates
For each of the same two stock sterile-DM models:
1. transformed q must be finite, positive, and strictly increasing;
2. corrected `f0_CLASS` must be finite and nonnegative;
3. CLASS must infer the ncdm density without `omega_ncdm`/`Omega_ncdm` input;
4. density agreement gate: `|omega_CLASS-omega_provider|/omega_provider <= 0.01`;
5. deliberate amplitude-times-two negative control must give `1.98 <= omega_2x/omega_correct <= 2.02`;
6. both stock models must satisfy all gates.

The workflow must also record the analytic convention factor `124.02510672119926` and the historical parent density ratio for comparison, but the historical agreement is explanatory only and is not an acceptance gate.

## Frozen classification
- CLASS cannot execute/converge with the unchanged qmax4000 capacity profile: `M25_CLASS_CONVENTION_CORRECTED_BLOCKED`.
- execution succeeds but either stock model fails density or factor-two control: `M25_CLASS_CONVENTION_CORRECTED_DENSITY_NOT_VALIDATED`.
- both stock models pass: `M25_CLASS_CONVENTION_CORRECTED_DENSITY_VALIDATED`.

Always:
- `physical_falsification=false`;
- `K1_promoted=false` in this bridge result;
- this result alone is not family-terminal coverage.

Only `M25_CLASS_CONVENTION_CORRECTED_DENSITY_VALIDATED` authorizes a separate prospective K1/reference-limit test using this corrected source convention.

## Interpretation guardrail
A PASS validates transport of the sterile provider's nonthermal phase-space density into CLASS at the background-density level. It does not establish observational preference, thermal-WDM discrimination, perturbation convergence, or K1/K4/K5 closure.