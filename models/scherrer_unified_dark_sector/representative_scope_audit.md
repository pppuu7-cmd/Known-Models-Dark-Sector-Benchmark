# Scherrer candidate representative-scope audit

Date: 2026-09-10
Provider: `Eladio-Moreno/k-essence-dynamics@f3f010e1ed74c86ce6a431a435fa93988f749ee2`
Subtree/input: `Cuadratico/hi.ini`

## Question
Can the executable author-supplied Scherrer example be promoted as the KMDSB M15 generalized-Chaplygin / unified-dark-fluid representative?

## Provider execution
The exact author input is executable after correcting the harness output-path assumption. Run `34430793576` produced fresh `output/test_background.dat`, `output/test_pk.dat`, transfer and perturbation outputs. This is an infrastructure/provider PASS only.

## Source-level model audit
The modified hi_class source implements the Scherrer kinetic structure

`G2 = -F0 + F2*(X-X0)^2 - 0.5*m_phi^2*phi^2`

with `y_sch = X-X0` and `G2_X=2 F2 y_sch`, `G2_XX=2 F2`.

However, the committed author example is not a unified DM+DE realization:

- `Omega_Lambda = 0.69` is explicitly nonzero;
- `Omega_cdm = 0`;
- `Omega_smg = -1` is inferred from closure;
- `DM_schm = 0.26` is supplied as the scalar matter-like target;
- in the modified input source, a local `f0_sch` is computed from the nominal scalar DE share but the stored model parameter is then explicitly overwritten with `pba->f0_schm=0`;
- therefore the accelerating vacuum component in the supplied executable configuration is the separate Lambda sector, not a scalar `-F0` contribution unifying DM and DE.

The code also reuses the `quintessence_monomial` enum as the Scherrer branch. That naming is implementation bookkeeping and must not be interpreted as canonical quintessence.

## Classification
`REPRESENTATIVE_MISMATCH_NO_M15_PROMOTION`

This is not a physical failure of Scherrer k-essence, generalized Chaplygin gas, or unified dark fluid. It means only that this exact provider/example does not instantiate the M15 target claimed by the census.

## Consequences
1. M15 remains untested and requires a genuine unified-dark-sector implementation in which the same stress-energy sector supplies both matter-like and accelerating behavior (or an explicitly scoped generalized-Chaplygin representative).
2. The current provider may later be useful as a scalar/k-essence dark-matter or Lambda+kinetic-scalar comparator, but it cannot be silently reused as M15.
3. It also cannot repair M11's covariant DE validation because its author example is not a DE-only branch.
4. No K1-K9 scientific promotion is authorized from the provider-control outputs.

## Next allowed gate
Search for and provenance-audit an independent generalized Chaplygin / unified-dark-fluid implementation with an explicit reference/decoupling limit, perturbation closure, stability conditions and reproducible author example before numerical benchmarking.
