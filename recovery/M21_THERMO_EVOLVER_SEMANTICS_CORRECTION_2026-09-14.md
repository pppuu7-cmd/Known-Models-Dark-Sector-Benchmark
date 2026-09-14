# M21 thermodynamics evolver semantics correction — 2026-09-14

Authoritative exact provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is a source-interpretation correction only; no executed input or scientific classification changes.

Current M21 profiles contain `evolver=0`, but thermodynamics uses the separate `thermo_evolver` control. Exact `include/precisions.h` defaults `thermo_evolver=ndf15`, and no current M21 baseline/stage-3/tolerance profile overrides it. Therefore the active `tol_thermo_integration` ladder acts on the default NDF15 thermodynamics solver, not on RK.

Exact `source/thermodynamics.c` passes `tol_thermo_integration` to the selected thermodynamics evolver. Exact `tools/evolver_ndf15.c` consumes it as `rtol` for initial-step choice, Newton convergence, integration-error rejection, step-size adaptation and order selection.

Durable detailed note: `models/mixed_cold_warm/m21_thermodynamics_tolerance_evolver_semantics_2026-09-14.md`.

The already-frozen tolerance-direction workflow remains scientifically valid because it varies only `tol_thermo_integration` and never asserted or changed `thermo_evolver` in its executed inputs. Its terminal aggregate remains the authority for direction/convergence behavior.

Claim ceiling unchanged: no CLASS bug claim, no production tuning, no K1/K3/K4 promotion, no physical M21 conclusion.
