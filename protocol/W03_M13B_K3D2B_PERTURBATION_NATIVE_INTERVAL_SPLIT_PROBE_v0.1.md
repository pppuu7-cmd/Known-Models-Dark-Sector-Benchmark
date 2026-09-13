# W03 M13b K3D2-B perturbation native interval split probe v0.1

Frozen: 2026-09-14 after `M13B_K3D2B_PERTURBATION_NATIVE_INTERVAL_SPLIT_STRUCTURALLY_AUTHORIZED_WITH_SCOPE` and before patch execution.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Background stack: K3D2 adapter + conditional background restart + floating boundary ownership + authorized U1 post-handoff seam.

## Frozen implementation

Only when `has_qcf || has_qpf`:

1. obtain the physical handoff conformal time with the existing CLASS map `background_tau_of_z(pba,5.0,&tau_handoff)`;
2. after native approximation switches have been constructed, insert `tau_handoff` into the sorted mutable `interval_limit[]` when it lies strictly inside an existing native interval;
3. split that one native interval into two while duplicating its `interval_approx` row on both sides; all other native limits and approximation rows are copied byte-for-byte;
4. preserve `ppw->pv->y` and the existing `perturbations_vector_init` machinery;
5. assign the isolated perturbation handoff point to the frozen pre-handoff branch by changing only the two qfield perturbation guards from `a < 1./6.` to `a <= exp(log(1./6.))`;
6. for the interval whose lower boundary is the inserted `tau_handoff`, call the numerical evolver at `nextafter(tau_handoff, interval_limit[index_interval+1])` while keeping the state vector unchanged. `perturbations_vector_init` remains evaluated at the exact native interval boundary.

When qcf/qpf are absent, no extra interval is inserted, no start coordinate is shifted and upstream CLASS follows its original perturbation interval path.

No tolerance, solver family, approximation criterion, photon/polarization/neutrino hierarchy equation, Einstein source equation, primordial IC, or qfield open-interval equation is changed.

## Lane N — disabled exact-null

Compare exact-pin upstream CLASS with recovered adapter present but qcf/qpf disabled. Require:

- both provider return codes zero;
- finite positive P(k);
- normalized P(k) L2 <= `1e-10`;
- relative H0 difference <= `1e-10`.

## Lane E — enabled perturbation execution

Use the unchanged K3C1-normalized cosmology, U1 background recovery, synchronous gauge and requested `k/H0={1,10}` outputs. For this implementation probe request `mPk,dTk` plus direct perturbation dumps; full B1/B2/B3 is not evaluated.

Require:

- build and provider rc=0;
- no minimum-step/underflow diagnostic in stdout+stderr;
- finite positive P(k);
- exactly two requested scalar perturbation trajectory files;
- both contain finite photon and ultra-relativistic hierarchy variables plus finite qcf/qpf direct perturbations;
- qcf and qpf perturbations are dynamically nonzero after the handoff;
- direct qfield perturbations remain below absolute amplitude `0.1` before any B3 normalization.

Run default and `cl_ref.pre` enabled lanes independently. Both must pass.

## PASS

`M13B_K3D2B_PERTURBATION_NATIVE_INTERVAL_SPLIT_IMPLEMENTATION_PASS_WITH_SCOPE`.

PASS authorizes re-running the already frozen full B1/B2/B3 regression with this patch added. K3 remains PARTIAL until that regression passes. K4/K5 remain closed.

Any lane failure yields `M13B_K3D2B_PERTURBATION_NATIVE_INTERVAL_SPLIT_BLOCKED`. Thresholds may not be relaxed retrospectively. No result here is author-code reproduction or physical falsification.
