# W06 M33 cubic Galileon K1 reference-map discovery preregistration v0.1

## Purpose
Map executable routes from the pinned native cubic covariant Galileon example toward a ΛCDM-like reference before any K1 claim is allowed.

The pinned hi_class example states that cubic-model parameters are fixed by `Omega_smg` and the tracker condition and exposes no free `parameters_smg`. Therefore the M30/M31 alpha-scaling coordinate must **not** be reused.

## Provider
- `hiclass-code/hi_class_public`
- exact commit `0009f51d89e6465c79e570b496c66fc90058fa77`
- native example `gravity_models/galileon_3.ini`
- no provider source modification.

## Frozen exploratory arms
Starting from the native example cosmological parameters, test these configuration families independently:

A. Explicit Galileon density with Λ fixed to zero:
`Omega_smg = {0.5, 0.1, 0.01, 0.001}`, `Omega_Lambda = 0`.

B. Explicit Galileon density with Λ closure requested through CLASS sentinel:
`Omega_smg = {0.5, 0.1, 0.01, 0.001}`, `Omega_Lambda = -1`.

C. Exact zero Galileon density with Λ closure:
`Omega_smg = 0`, `Omega_Lambda = -1`.

D. Plain ΛCDM endpoint using the same H0/omega_cdm/omega_b/A_s/n_s/tau_reio and `Omega_smg = 0`, `Omega_Lambda = -1`, with the Galileon gravity-model lines removed from the *input file only*; provider source remains untouched.

## Outputs
For each arm record exit code, stderr tail, and presence/finite status of CMB TT and P(k) outputs.

## Classification
This workflow is discovery-only. Allowed conclusions:
- `REFERENCE_MAP_CANDIDATE_FOUND_REQUIRES_PREREGISTERED_K1`
- `REFERENCE_MAP_PARTIAL_EXECUTABLE`
- `REFERENCE_MAP_BLOCKED_IMPLEMENTATION`

It **cannot** promote K1 and cannot issue a physical FAIL. A follow-up K1 ladder must be separately preregistered after the executable coordinate is identified.
