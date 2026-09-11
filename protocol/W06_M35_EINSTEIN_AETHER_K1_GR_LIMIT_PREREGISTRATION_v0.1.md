# W06 M35 Einstein–Aether / LV gravity K1 GR-limit preregistration v0.1

## Purpose
Test K1 continuity toward the weak-coupling/GR-like limit using the already K0-qualified pinned `CLASS_LVDM` provider. This is a numerical continuity gate, not a claim of complete Einstein–Aether scalar/vector/tensor closure.

## Frozen provider
- Repository: `Michalychforever/CLASS_LVDM`
- Branch: `LVDM`
- Exact commit: `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`
- No source-code modification is allowed.

## Frozen control
Use the provider's `lcdm.ini`, changing only output root. The control therefore preserves the provider's own weak-gravity reference configuration.

## Frozen K1 ladder
Start from the gravity-sector ratios in `Misha.ini` and scale the LV/aether couplings together while preserving their ratios:

| scale s | alpha | beta | lambda | Y_dm |
|---:|---:|---:|---:|---:|
| 1 | 0.05 | 0.25 | -0.10 | 0 |
| 0.1 | 0.005 | 0.025 | -0.010 | 0 |
| 0.01 | 0.0005 | 0.0025 | -0.0010 | 0 |
| 0.001 | 0.00005 | 0.00025 | -0.00010 | 0 |

All other parameters remain those of `Misha.ini`.

## Observables
For every arm require finite provider outputs for:
- TT spectrum (`*_cl.dat`),
- matter power spectrum (`*_pk.dat`).

Compute normalized L2 response of each ladder arm relative to the frozen control over the common output domain.

## Acceptance rule
K1 may be promoted to `PASS_WITH_SCOPE` only if all conditions hold:
1. exact provider commit matches the preregistered pin;
2. control and all four ladder arms exit successfully and produce finite TT/P(k);
3. both TT and P(k) response sequences are monotonically non-increasing as `s` decreases, allowing relative numerical slack of 2%;
4. the smallest-coupling response is at most 20% of the full-coupling response in both TT and P(k).

If execution/build fails: `BLOCKED_IMPLEMENTATION`.
If outputs are finite but continuity criteria are not established: `PARTIAL` / numerical non-establishment, **not** physical falsification.

## Scope guard
A positive result establishes only a provider-specific weak-coupling continuity check for the scalar cosmological implementation in this pinned CLASS_LVDM realization. K2–K9 remain open, and no complete Einstein–Aether SVT claim is licensed.
