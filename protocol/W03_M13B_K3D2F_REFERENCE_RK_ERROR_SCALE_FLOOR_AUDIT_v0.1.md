# W03 M13b K3D2-F reference-RK error-scale-floor audit v0.1

Date frozen: 2026-09-14

## Trigger

K3D2-E localized the exact `cl_ref.pre` first-step collapse to standard Boltzmann variables rather than direct qcf/qpf fields: all 349 strict-clean first-attempt dominants are photon temperature hierarchy l>=3; final accepted-attempt dominants are photon hierarchy (335) or `ur_theta` (14); qfield dominance is zero.

## Purpose

Using only the immutable K3D2-E artifact, determine whether the terminal RK collapse is dominated by the absolute error-scale floor applied to near-zero standard Boltzmann variables. This is analysis-only: no CLASS execution and no physics/numerical branch changes are permitted.

## Immutable authority

Parent run `34797701252`, aggregate artifact `10329419715`, digest `sha256:d24eb2f57b3936a7c7fec2f6d5263320097a438966a62c375112d5a22e9d0d27`.

## Frozen metrics

For every strict-clean record, use the already-recorded final dominant component fields `final_yscal`, `final_y`, `final_yerr`, `final_start_dydx`, `final_raw_ratio`, `final_errmax` and component class.

Report:

1. fraction with `final_yscal <= 1.0000000001e-30`;
2. fraction with `|final_y| <= 1e-16`;
3. fraction with `|final_start_dydx| <= 1e-20`;
4. component-class split among floor records;
5. final raw-ratio and errmax min/median/max;
6. k-range of floor records;
7. whether qcf/qpf appears in any floor-dominant record.

## Frozen classifications

If at least 95% of strict-clean records satisfy both `final_yscal <= 1.0000000001e-30` and `|final_y| <= 1e-16`, with zero qcf/qpf floor-dominant records:

`M13B_K3D2F_REFERENCE_RK_STANDARD_BOLTZMANN_ABSOLUTE_SCALE_FLOOR_LOCALIZED`.

Otherwise, if fewer than 95% satisfy the joint floor criterion:

`M13B_K3D2F_REFERENCE_RK_SCALE_FLOOR_NOT_DOMINANT`.

If fewer than 100 strict-clean records contain all required fields:

`M13B_K3D2F_REFERENCE_RK_SCALE_FLOOR_AUDIT_IMPLEMENTATION_BLOCKED`.

## Claim ceiling

This audit is diagnostic only. It cannot authorize tolerance relaxation, changing `minimum_variation`, changing the RK error scale, solver replacement, seam movement, equation changes, K4 promotion, K5 promotion, or physical falsification. K3 remains at most PARTIAL and reference B1/B2/B3 remain NOT_EVALUATED while the exact provider returns nonzero rc.
