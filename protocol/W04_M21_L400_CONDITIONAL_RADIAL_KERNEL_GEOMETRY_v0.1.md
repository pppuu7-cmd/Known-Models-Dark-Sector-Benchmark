# W04 M21 l=400 conditional radial-kernel geometry audit v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before its recovered source/radial/convolution classification is known.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Authorization

This gate is executable only if the terminal artifact from `W04 M21 l400 convolution successor router v0.1` authorizes `RADIAL_KERNEL_GEOMETRY`.

It performs no CLASS execution and may consume only the clean recovered case artifacts from run `34907528331`, the terminal recovered aggregate, and the immutable parent k-support authority already named by the parent protocol.

If the router does not authorize this successor, the workflow must skip without scientific output.

## Purpose

The parent transfer-convolution gate compares the scalar-E radial profile at common `u = tau0-tau`. In flat M21 the exact radial branch is `SCALAR_POLARISATION_E`, with `K=0`, `s2=1`, flat angular rescaling, and radial dependence through the Bessel/hyperspherical argument `x = k u` at fixed `l=400`.

This gate tests whether any f3-specific radial-profile response is merely a coordinate/geometry phase effect from comparing at common `u`, or remains after comparing the same radial function at common physical argument `x=k u`.

It is a numerical mechanism localization only.

## Frozen support and inputs

Use exactly the q-index set that passes all parent integrity gates. Do not repair, add, drop, rematch or interpolate q nodes across different q indices.

For each valid `(case,q)` block use only columns already frozen in the parent diagnostic:

- `k`;
- `u = tau0_minus_tau`;
- `radial`.

Define `x = k*u` row by row.

Use the immutable parent excess weights `W_q` exactly as reconstructed by the parent analyzer. The active q support, parent weight definition, and specificity boundary `E > 3` remain unchanged.

## Integrity

Before any classification require:

1. parent recovered classification is one that authorized `RADIAL_KERNEL_GEOMETRY`;
2. all parent diagnostic integrity checks are true;
3. same support q-index set across `ref,f2,f3,f4`;
4. relative same-q k difference from reference <= `1e-6`;
5. each `(case,q)` block has at least 20 rows;
6. `x` is finite and strictly monotonic after sorting/duplicate removal; duplicate-x rows, if any, are permitted only when their radial values agree to relative `1e-12`, otherwise BLOCK;
7. common x-overlap across all four cases contains at least 20 retained reference x nodes.

Any failure -> `M21_L400_RADIAL_GEOMETRY_BLOCKED`.

## Frozen comparison

For every q:

- take reference x nodes inside the strict four-case x-overlap;
- linearly interpolate each case radial profile `R(x)` onto those retained reference x nodes;
- define

`D_Rx(c,q) = ||R_c(x)-R_ref(x)||_2 / max(||R_ref(x)||_2,1e-300)`.

Define the frozen support-weighted amplitudes

`A_Rx(c) = sqrt(sum_q W_q D_Rx(c,q)^2 / sum_q W_q)`

and specificity

`E_Rx = A_Rx(f3) / max(A_Rx(f2),A_Rx(f4),1e-300)`.

Read the parent's already-frozen common-u radial specificity as `E_Ru`; do not recompute it with altered rules.

Also report without changing classification:

- per-q `D_Rx` and `E_Rx(q)`;
- common-x interval per q;
- max same-q relative k difference;
- reference and case x-range endpoints;
- `E_Rx/E_Ru` when finite.

## Frozen classification

- parent `E_Ru > 3` and `E_Rx <= 3` -> `M21_L400_RADIAL_SPECIFICITY_X_GEOMETRY_LOCALIZED_WITH_SCOPE`;
- parent `E_Ru > 3` and `E_Rx > 3` -> `M21_L400_RADIAL_SPECIFICITY_PERSISTS_AT_COMMON_X_WITH_SCOPE`;
- parent `E_Ru <= 3` despite router authorization -> `M21_L400_RADIAL_GEOMETRY_PARENT_INCONSISTENT_BLOCKED`;
- any integrity failure -> `M21_L400_RADIAL_GEOMETRY_BLOCKED`.

## Interpretation ceiling

`...X_GEOMETRY_LOCALIZED...` means the radial specificity disappears when the profiles are compared at the same native radial argument `x=k(tau0-tau)`. It does not establish a provider defect or physical scale.

`...PERSISTS_AT_COMMON_X...` means the radial-profile specificity is not explained by the u-to-x coordinate phase alone and requires a new prospectively frozen radial-evaluation/interpolation audit. It does not itself identify a defect.

This gate cannot promote K1, K3 or K4 and cannot physically validate or falsify M21.
