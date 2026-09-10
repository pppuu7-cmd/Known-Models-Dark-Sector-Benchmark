# M15 IDECAMB decomposed-NGCG candidate audit

Updated: 2026-09-10
Status: `CANDIDATE_BACKGROUND_EQUIVALENCE_PERTURBATION_BINDING_OPEN`
Scientific promotion: **NO**

## Candidate provenance

Exact provider already under independent M14 audit:

- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- intended overlay base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`

No M15 execution or threshold is authorized by this audit.

## Source-level NGCG branch

In `camb/equations_ppfi.f90`, `CoupledFluidModels%Coup_CF` defines a default interaction branch

`Q = -3 w_de beta H rho_de rho_c / (rho_de + rho_c)`

(up to the file's conformal/8-pi-G normalization), with an explicit source comment that this is the **NGCG model** and that `beta` represents the NGCG `alpha`. The same default branch sets perturbative coupling coefficients through `PerturCoupC_CF`; momentum-transfer closure remains controlled by `CovQForm_CF`.

## Family-identity audit

The original NGCG literature defines a single unified dark-sector fluid but also derives a dual interacting-XCDM decomposition. Later decomposed-NGCG work uses the interaction form

`Q = -3 alpha w H rho_de rho_c/(rho_de+rho_c)`

(or equivalently `Q=3 beta H rho_de rho_c/(rho_de+rho_c)` with `beta=-alpha w`, depending on parameter convention).

Therefore **being written as interacting DE+CDM is not by itself a representative mismatch** for M15. A mathematically exact decomposition can represent the same background response-family. KMDSB must test equivalence of the implemented perturbation closure rather than requiring a literal one-fluid code path.

However, background duality does not by itself prove perturbation-level equivalence. Different covariant momentum-transfer prescriptions/decompositions can yield different effective sound speeds and structure growth. M15 K3-K5 therefore remain open until the precise NGCG perturbation prescription is source-bound to a defined unified/decomposed model.

## Current scoped conclusion

- K0: candidate provenance identified, not yet promoted as M15 provider.
- background family identity: **supported with scope** by source form + published NGCG/XCDM duality.
- perturbation family identity: **OPEN**.
- K1 reference: not preregistered. Candidate expectation is `alpha/beta -> 0`, but the correct comparator depends on the frozen NGCG `w_X`/XCDM decomposition and must be source-bound before numerical testing.
- K2-K9: not tested.

## Next allowed M15 gate

Before running M15:

1. identify exactly how the IDECAMB input selects the source `default` QForm branch without inventing an undocumented selector;
2. bind `WForm_CF` and `CovQForm_CF` to a published decomposed-NGCG perturbation prescription;
3. freeze the parameter-convention map between IDECAMB `beta` and NGCG `alpha`;
4. freeze the `alpha/beta -> 0` reference comparator;
5. only then preregister provider execution/reference tests.

No result from the CQ (`Class_IDE=2`) branch may be reused as M15 scientific evidence; only build/provenance infrastructure may be shared.
