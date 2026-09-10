# W03 / M17 linear-ePPF background-CPL transport attack v0.1

Frozen: 2026-09-10
Status: PREREGISTERED
Family: F17/M17 original future-event-horizon holographic dark energy
Provider: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075` over `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
Entry evidence: `M17_IDECAMB_LINEAR_EPPF_PROVIDER_PASS_WITH_SCOPE`

## 1. Question

The already frozen M17 background attack found that finite HDE points `c={0.6,0.8,1.0,1.2}` are 96.7--98.9% absorbed by a two-parameter CPL background fit. The present test asks a stricter prospective question:

> If the CPL parameters are frozen **only from that background fit**, do they also reproduce the linear scalar CMB response of the HDE/ePPF provider?

CPL parameters are not re-fitted to CMB spectra in this gate. This is a transport/predictivity test of the background mapping, not an optimized perturbation-level CPL manifold fit.

No covariance-weighted significance or K7/K8 observational novelty is claimed here.

## 2. Provider route

Use exactly the recovered linear route:

- same pinned CosmoMC + IDECAMB overlay;
- `Class_IDE=1`;
- `Use_PPF=T`;
- `param[beta_cf]=0`;
- `CMB_lensing=T`;
- `use_nonlinear_lensing=F`;
- `nonlinear_pk=F` from the frozen parent common configuration;
- action=4 theory-output mode;
- external likelihood DEFAULTs disabled as in the successful recovery.

No HDE/ePPF equations, precision settings or initial conditions may change.

## 3. Frozen cases

### Reference R0

CPL fluid with

`WForm_CF=1`, `w0=-1`, `w1=0`, `beta=0`.

This is the same-provider linear reference used only to form response vectors. It does not manufacture an HDE native LambdaCDM intersection.

### HDE cases

`WForm_CF=2`, `beta=0`, with

- H06: `c=0.6`
- H08: `c=0.8`
- H10: `c=1.0`
- H12: `c=1.2`

### Background-fitted CPL transport comparators

The following values are copied unchanged from the canonical pre-existing file `waves/wave_03_expanded_dark_energy/M17_HDE_BACKGROUND_CPL_RESULT.json`:

- C06: `w0=-1.299870066355541`, `w1=+0.9082964747357177`
- C08: `w0=-1.0616652253607164`, `w1=+0.5962733794216544`
- C10: `w0=-0.9167034662101682`, `w1=+0.4297783543420696`
- C12: `w0=-0.8194180077420152`, `w1=+0.3292670947586294`

No perturbation/CMB refit is authorized.

## 4. Output gate

Each of the 9 cases must exit zero and produce a non-empty `.theory_cl` table with exactly the common columns

`L, TT, TE, EE`

for the same multipoles. Require:

- at least 2000 matched rows;
- exact integer `L` agreement across all cases;
- every TT/TE/EE value finite;
- runtime log confirms `Doing non-linear lensing: F` for every case.

A missing/nonfinite/misaligned case is an execution/output failure, not a physical HDE verdict.

## 5. Frozen response metrics

For each HDE point `i` and channel `j in {TT,TE,EE}` define vectors on the common multipole grid:

`h_ij = C_ell(HDE_i,j) - C_ell(R0,j)`

`p_ij = C_ell(CPLfit_i,j) - C_ell(R0,j)`

`e_ij = C_ell(HDE_i,j) - C_ell(CPLfit_i,j) = h_ij-p_ij`.

No elementwise division by `C_ell` is used, so TE zero crossings do not create artificial singularities.

For each channel record:

`R_ij = ||e_ij||_2 / ||h_ij||_2`.

If `||h_ij||_2 <= 1e-20`, the channel is classified nonidentifiable for that case and is excluded from the equal-channel summary rather than zero-imputed.

Also record the signed response angle

`angle_ij = arccos( <h_ij,p_ij> / (||h_ij|| ||p_ij||) )`

in degrees when both vectors are identifiable.

Equal-channel residual summary:

`R_equal_i = sqrt(mean_j R_ij^2)`

over identifiable channels only.

Maximum channel residual:

`R_max_i = max_j R_ij`.

These metrics test transport of the already-frozen background mapping, not the strongest possible CPL perturbation manifold.

## 6. Prospective descriptive bins

For each HDE point, freeze these labels before exposure:

- `PERTURBATION_TRANSPORT_STRONGLY_ABSORBED_BY_BACKGROUND_CPL` if `R_equal <= 0.10` and `R_max <= 0.20`;
- `PERTURBATION_TRANSPORT_PARTIALLY_ABSORBED_BY_BACKGROUND_CPL` if the strong condition fails but `R_equal <= 0.30` and `R_max <= 0.50`;
- `PERTURBATION_RESPONSE_SURVIVES_BACKGROUND_CPL_TRANSPORT_ATTACK` otherwise.

These are theory-space transport labels only. They are not probabilities and not observational significance statements.

## 7. Global M17 interpretation

Possible aggregate classifications:

- `M17_LINEAR_EPPF_BACKGROUND_CPL_TRANSPORT_STRONG` if all four points are strongly absorbed;
- `M17_LINEAR_EPPF_BACKGROUND_CPL_TRANSPORT_MIXED` if at least one is strong/partial and at least one survives, or if all are partial without a survivor;
- `M17_LINEAR_EPPF_PERTURBATION_RESPONSE_SURVIVES_BACKGROUND_CPL_TRANSPORT` if all four survive;
- `M17_LINEAR_EPPF_TRANSPORT_OUTPUT_BLOCKED` for execution/output failure.

A survivor does **not** yet establish quotient novelty: the next stronger K6 attack may re-fit the full CPL perturbation manifold under one shared response objective. Conversely, strong transport absorption would be stronger evidence that original HDE contributes little response-distinct structure beyond smooth DE on these channels.

## 8. Output contract

Canonical machine result:
`models/holographic_dark_energy/M17_LINEAR_EPPF_BACKGROUND_CPL_TRANSPORT_RESULT.json`

Wave mirror:
`waves/wave_03_expanded_dark_energy/M17_LINEAR_EPPF_BACKGROUND_CPL_TRANSPORT_RESULT.json`

Immutable artifact must retain all 9 generated ini files, runtime logs, theory spectra, exact provider pins, analyzer output and this preregistration.
