# W04 M19 external CDM reference convergence preregistration v0.1

## Question
Does the finite fuzzy/ultralight-axion implementation approach an independently executable pure-CDM reference as the axion fraction tends to zero, despite the legacy axionCAMB exact-zero crash?

## Providers
- finite ULA branch: `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`;
- external zero reference: historical `cmbant/CAMB@dc437acd8c90aa7e5595fcb25c615b03de8357a7`.

The historical CAMB reference is chosen because it is contemporaneous with the axionCAMB lineage and retains the same classic CAMB parameter/output conventions.

## Frozen cosmology
Match the axionCAMB control cosmology in physical-density coordinates wherever both providers expose the same parameter:

- `ombh2 = 0.02222`;
- total dark-matter physical density `omega_dm h^2 = 0.1200`;
- `omnuh2 = 0.00060`;
- `H0 = 67.31 km/s/Mpc`;
- flat geometry;
- `w=-1`;
- adiabatic scalar initial conditions;
- same CMB temperature, helium fraction, primordial scalar amplitude/index/running and reionization settings copied from the pinned axionCAMB base file into the historical-CAMB case when keys exist.

For axionCAMB, total dark-matter density is held fixed and split into CDM+axion using `use_axfrac=T`, `omdah2=0.1200`.

## Frozen finite sequence
At fixed axion mass `m_ax=1e-27 eV`, run

`f_ax = {0.10, 0.03, 0.01, 0.003, 0.001}`.

No exact-zero axionCAMB execution is used in this test.

## Outputs
Require finite:
- scalar CMB spectra;
- linear matter power;
- transfer functions.

Provider-specific grids may differ. Comparison therefore uses common physical coordinates and interpolation only over the strict overlap domain. No extrapolation is allowed.

## Residuals
For each product define a symmetric relative residual against historical pure CAMB on the common grid,

`r = 2 (X_ax - X_cdm) / (|X_ax| + |X_cdm| + floor)`.

Report robust norms separately for CMB TT/TE/EE, P(k), and transfer columns. TE points where both numerator and denominator are near zero are masked by a frozen numerical floor tied to the maximum absolute channel amplitude (`1e-12 * max|X|`).

For each block report median absolute residual, RMS residual, and 95th-percentile absolute residual.

## Convergence gates
A block is `CONVERGENT_WITH_SCOPE` only if all are true:

1. the 95th-percentile absolute residual is non-increasing for every consecutive decrease in `f_ax`, allowing at most a relative numerical slack of 2%;
2. the smallest-fraction residual is lower than the `f_ax=0.10` residual;
3. a log-log fit over the three smallest fractions has positive convergence exponent `p>0` in `R95 ~ f_ax^p`;
4. the fitted intercept does not require a non-zero residual floor larger than the smallest measured residual. The fit is diagnostic and must not be used to force zero intercept.

Overall classification is `M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_PASS_WITH_SCOPE` only if every retained block passes. Otherwise preserve the failing block(s) explicitly.

## Scientific interpretation
A PASS establishes an independently anchored approach to the pure-CDM boundary and may support K1 as `PASS_WITH_SCOPE_EXTERNAL_LIMIT_CONVERGENCE`; it does not prove that the legacy axionCAMB exact-zero executable path is correct. The exact-zero provider crash remains documented as an implementation defect.

A failure is not automatically physical falsification: cross-provider baseline mismatch must first be separated from non-convergence by running a matched pure-CDM cross-solver calibration case when possible.
