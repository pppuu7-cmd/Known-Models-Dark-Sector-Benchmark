# W03 M13b K3D2-B z=5 IVP handoff recovery v0.1

Frozen: 2026-09-14 after run 34784844546 completed an enabled full-Boltzmann CLASS execution and before any z=5-handoff implementation is executed.

Parent protocol: `protocol/W03_M13B_K3D2B_ENABLED_TWO_FIELD_COSMOLOGY_REGRESSION_v0.1.md`.
Parent diagnostic: `waves/wave_03_expanded_dark_energy/M13B_K3D2B_FIRST_ENABLED_FULL_BOLTZMANN_DIAGNOSTIC.json`.
Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Trigger

The first correctly budget-bound enabled CLASS realization completed successfully, produced finite positive linear P(k) and finite CMB spectra, but failed the prospectively frozen K3C1 background-regression gates.

At z=5 CLASS had already evolved the direct fields from its primordial background initial epoch, giving approximately

- `x=0.9212361867`, `p=0.00376898185`;
- `y=0.9924888257`, `q=-0.09018622724`;

instead of the K3C1/K3C2 IVP boundary `x=0.92,p=0,y=1.02,q=0`. The crossing was consequently shifted to `z=1.507195...` rather than the K3C1 authority `z=1.197872...`.

This is an initial-epoch binding mismatch: K3C1/K3C2 define the independent realization at z=5, while CLASS normally initializes dynamical species much earlier. It is not an Einstein-Boltzmann runtime failure and not a physical falsification.

## Frozen recovery semantics

The independent qcf+qpf adapter shall reproduce the already frozen K3C1/K3C2 initial-value problem exactly inside CLASS by using a hard, deterministic handoff at

`a_handoff = 1/6` (`z_handoff = 5`).

Before the handoff (`a < 1/6`):

1. qcf background field is held exactly at `phi_qcf=0.92` with `phi_prime_qcf=0`;
2. qpf background field is held exactly at `psi_qpf=1.02` with `psi_prime_qpf=0`;
3. their potential stress-energy remains present and is evaluated at those frozen field values;
4. because the frozen fields are constant, `p_prime_qcf=p_prime_qpf=0` in this pre-handoff branch;
5. direct qcf/qpf perturbations remain exactly zero and their perturbation derivatives are set to zero;
6. no photon, polarization, ur/ncdm, metric, thermodynamics, primordial, transfer, harmonic, lensing or nonlinear evolution equation is modified.

At and after the handoff (`a >= 1/6`):

1. qcf background evolution uses the already frozen canonical KG equation unchanged;
2. qpf background evolution uses the already frozen phantom KG equation unchanged;
3. qcf/qpf direct perturbation evolution uses the already frozen K3D2-A equations unchanged;
4. no state reset, fit, rephasing, velocity kick or amplitude rescaling is applied at the handoff—the pre-handoff constant states are already exactly the desired IVP values.

The switch is a definition of the independent comparison realization, not a fitted physical transition. It simply embeds the K3C1/K3C2 z=5 IVP into a solver that integrates the rest of cosmology from an earlier epoch.

## Unchanged frozen quantities

This recovery MUST NOT change:

- `U0=0.3362232603714306`;
- `s=29`;
- `V_class=3 H0^2 U`;
- h, Omega_m, Omega_r, baryon/CDM split, radiation split, primordial parameters;
- qcf/qpf z=5 field values or zero velocities;
- the K3D2-B frozen modes;
- any B1/B2/B3 acceptance threshold;
- the synchronous runtime scope of qcf/qpf;
- public-V0/author-normalization guardrails.

## Required implementation audit

Before interpreting the recovered enabled result, machine checks must prove:

1. the only new physical-control constant is the literal `1./6.` handoff in qcf/qpf background and perturbation adapter blocks;
2. for `a<1./6.` all four qcf/qpf background state derivatives are zero;
3. for `a<1./6.` all four qcf/qpf perturbation state derivatives are zero;
4. qcf/qpf pressure derivatives are zero pre-handoff;
5. for `a>=1./6.` the exact previously frozen qcf/qpf KG RHS strings/signs remain present;
6. no upstream scf-bearing line changes;
7. no protected Boltzmann/Einstein/thermodynamics/primordial evolution line changes;
8. the K3D2-A null qcf=qpf-disabled P(k) regression remains exactly unchanged within its frozen `1e-10` normalized-L2 threshold.

## Interpretation

Run 34784844546 is retained as an immutable useful diagnostic: it demonstrates that the adapter can complete the full CLASS Einstein-Boltzmann stack and localizes the mismatch to the pre-z=5 direct-field history.

Only a recovered run satisfying the original B1 thresholds may proceed to B2 precision comparison and B3 mode-response interpretation.

Even a full recovery PASS remains K3 PARTIAL, with K4/K5 closed and `physical_falsification=false`.
