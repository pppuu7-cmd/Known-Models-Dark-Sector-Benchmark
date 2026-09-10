# W03 / M17 c=0.6 joint H(a)+CMB CPL K6 refinement execution v0.1

Date: 2026-09-10
Status: MECHANICALLY_ACTIVATED_FROM_PRIOR_PREREGISTRATION

This file introduces no new scientific threshold or search freedom. It executes the refinement rule already frozen in `W03_M17_C060_JOINT_CPL_K6_COARSE_GRID_PREREGISTRATION_v0.1.md` before the coarse result was exposed.

Consumed coarse result: `M17_C060_JOINT_CPL_K6_COARSE_RESULT.json`.

The unique coarse optimum is

- `w0* = -1.299870066355541`
- `wa* = +0.9082964747357177`
- `R_joint = 0.39778348134254315`
- `R_max = 0.45714456419534805`
- classification: `M17_C060_K6_COARSE_SURVIVOR_CANDIDATE`.

Per the prior frozen rule, execute all 25 Cartesian refinement points centered on that p*:

- `delta_w0 in {-0.10,-0.05,0,+0.05,+0.10}`
- `delta_wa in {-0.20,-0.10,0,+0.10,+0.20}`.

Use the identical provider pins, linear-ePPF isolation, R0/H06 targets, four equal-weight blocks H/TT/TE/EE, and identical `R_joint` and `R_max` definitions.

No new interpretation thresholds are introduced. For descriptive continuity only, apply the exact bins already frozen for the coarse stage:
- strong absorption iff `R_joint<=0.10` and `R_max<=0.20`;
- partial absorption iff not strong and `R_joint<=0.30` and `R_max<=0.50`;
- otherwise survivor.

This refinement remains K6 theory-space evidence only. It cannot establish observational significance or physical falsification and does not open K7 by itself unless the repository's gate policy is separately satisfied.
