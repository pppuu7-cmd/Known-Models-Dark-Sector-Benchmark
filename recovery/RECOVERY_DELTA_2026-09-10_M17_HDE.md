# Recovery delta — 2026-09-10 — M17 holographic dark energy

Source of truth remains repository state plus validated Actions artifacts.

## New result
M17/F17 original future-event-horizon holographic dark energy has been opened as an explicit W03 benchmark.

K0: `PASS_WITH_SCOPE` for the original Miao Li 2004 OHDE model.

K1: `NO_NATIVE_LCDM_REFERENCE_INTERSECTION_WITH_SCOPE`.

Reason: the native equation of state is

`w_de(a) = -1/3 - 2 sqrt(Omega_de(a))/(3 c)`.

A single constant `c` can make `w=-1` only at an isolated epoch where `c=sqrt(Omega_de(a))`; because `Omega_de(a)` evolves, there is no full-history LambdaCDM intersection obtained by varying `c`.  Also `c -> infinity` yields `w -> -1/3`, not -1.  This is structural reference geometry, not HDE falsification.

Authority files:
- `models/holographic_dark_energy/audit.md`
- `waves/wave_03_expanded_dark_energy/M17_HDE_K1_RESULT.json`
- `waves/wave_03_expanded_dark_energy/M17_HDE_BACKGROUND_CPL_PREREG.md`
- `code/w03_m17_hde_background_cpl.py`
- `.github/workflows/w03-m17-hde-background-cpl.yml`

## Perturbation-provider search
Targeted public-source search found perturbation literature for HDE/IHDE but no pinned source-complete original-OHDE Boltzmann provider suitable for K3 promotion in this iteration. Do not substitute an effective background `w(a)` or a subhorizon growth-index prescription for source-complete event-horizon perturbation closure.

## Running process
Workflow: `W03 M17 HDE finite background CPL attack`
Run: `34495252497`
Head SHA: `416e1301b1e38514c14854357ddf03b8eb9b7059`
State at handoff: `in_progress`.

Frozen finite-background gate:
- HDE c = {0.60,0.80,1.00,1.20}
- Omega_m0=0.30, Omega_de0=0.70
- standard 7 DSIR late-z nodes
- ODE numerical-convergence gate: response norm mismatch <=1e-4 and angle <=0.02 deg
- full finite CPL fit bounds: w0 in [-2,0], wa in [-3,3]
- three frozen optimizer starts
- residual fraction <=0.10 => BACKGROUND_ABSORBED_BY_CPL_WITH_SCOPE
- residual fraction >=0.30 => BACKGROUND_SEPARATED_FROM_CPL_WITH_SCOPE
- otherwise BACKGROUND_INCONCLUSIVE.

No result from this background gate may close K3/K5/K7 or observational novelty.

## Next action
Consume run 34495252497 once terminal; inspect the machine JSON rather than workflow colour alone.  Preserve K1 result regardless of the K6-background outcome.  If PASS, update M17 audit/census/mandatory matrix/research log.  K3 then remains a source-complete provider problem.  Continue other independent W03 census families if no suitable OHDE provider is available.