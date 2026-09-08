# M01 — Smooth non-phantom dark energy / wCDM local-family audit

Date: 2026-09-08  
Wave: `wave_00_calibration`  
KMDSB protocol: `DSIR_BENCHMARK_PROTOCOL_v0.1`  
DSIR authority snapshot: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Tested scope

This audit uses the frozen DSIR C1 smooth non-phantom local ray, not the whole space of scalar-field dark-energy theories.

`epsilon_w = 1 + w -> 0+`

The tested side is one-sided around the LambdaCDM intersection. The smallest frozen C1 step is `epsilon_w=1e-4` at p8 precision.

## Frozen DSIR compatibility evidence

- reference intersection: `w=-1` / `epsilon_w=0`;
- smallest production step: `epsilon_w=1e-4`;
- finite-difference change at `epsilon_w=1e-3`: about `0.12%` L2 and `0.014 deg` direction change;
- cross-solver smooth-w bridge hard threshold `1e-9` passes;
- matched-p8 calibration mismatch: `2.3747404043e-10`.

These establish a controlled Theory->Response deformation, not observational detectability.

## B5 observation-space test

Wave 00 recovered the pinned observation product used by DSIR Experiment 009:

- corrected DESI DR1 ShapeFit erratum covariance;
- channels `[DH/DM, f sigma_s8, m+n]`;
- informative bins `LRG1, LRG2, LRG3, ELG2, QSO`;
- BGS excluded, matching the DSIR AP/growth control because its AP coordinate is prior dominated.

KMDSB then projected the frozen *phenomenological* constant-w control into the same 3-channel covariance using:

- flat `Omega_m=0.3`, matching `src/dsir/linear_controls.py`;
- one-sided `epsilon_w>=0`;
- `DH/DM` from the flat-wCDM background;
- growth response from the frozen sub-horizon DSIR growth equation;
- fixed present-day fluctuation normalization, so the local growth observable scales as `(fD)_w/(fD)_LCDM`;
- local smooth-w shape derivative `d(m+n)/d epsilon_w = 0` in this control;
- no nuisance marginalization.

Reproducible code: `code/m01_b5_shapefit_local_fisher.py`.
Result record: `models/smooth_nonphantom_de/b5_shapefit_local_fisher_result.json`.

### B5 numerical result

Using a one-sided finite-difference step `1e-4`:

- `F_epsilon_epsilon = 31.4928446382`;
- optimistic unmarginalized `sigma(epsilon_w) = 0.1781944012`.

Finite-difference robustness is stable:

- step `1e-5`: sigma `0.1782088584`;
- step `1e-4`: sigma `0.1781944012`;
- step `1e-3`: sigma `0.1780498440`;
- step `1e-2`: sigma `0.1766057237`.

Exact scoped displacement relative to the LambdaCDM origin gives:

- `epsilon_w=1e-4`: sqrt(Delta chi2) = `5.61185e-4`;
- `epsilon_w=1e-3`: `0.0056164`;
- `epsilon_w=1e-2`: `0.0566233`;
- `epsilon_w=0.05`: `0.293732`;
- `epsilon_w=0.1` (`w=-0.9`): `0.615964`.

Thus the smallest frozen C1 ray is overwhelmingly below the corrected ShapeFit covariance sensitivity in this scoped projection. Even `w=-0.9` remains below 1 sigma in this deliberately limited AP+growth+shape control.

Because nuisance parameters were **not** marginalized, the local Fisher sensitivity is optimistic: adding nuisance freedom cannot make the tiny `epsilon_w=1e-4` displacement more identifiable within the same mapping.

This is **not** a full DESI likelihood constraint on w and is not a statement that every smooth-DE realization is unidentifiable.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | Tested object is explicitly restricted to the frozen DSIR C1 smooth non-phantom local ray. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | Exact intersection at `w=-1`; response map frozen in C1 scope. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Uses frozen DSIR v0.1.1 bookkeeping. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | One-sided non-phantom domain, convergence diagnostics and cross-solver bridge pass. |
| B4 Response coverage/masks | PASS_WITH_SCOPE | Background/AP and growth response are represented; missing channels remain masked. |
| B5 Reference identifiability | NONIDENTIFIABLE | Corrected DESI DR1 ShapeFit local Fisher control gives `sigma(epsilon_w)=0.1782`; the frozen `epsilon_w=1e-4` ray is only `5.6e-4 sigma`. Scope is the explicit phenomenological mapping above, not a full likelihood. |
| B6 Nearest-comparator discrimination | OPEN | Alternative smooth-DE/mimic comparator not yet tested in the same observation space. |
| B7 Quotient-surviving novelty | OPEN | Controlled deformation is not a residual law. |
| B8 Prospective withheld prediction | OPEN | No M01-specific prospective novelty claim has been frozen/tested. |
| B9 Synthesis/design prior | PASS | Compatibility and non-identifiability now produce a concrete design constraint. |

## Overall verdict

`DSIR_COMPATIBLE_NONIDENTIFIABLE`

Within the frozen C1 + corrected ShapeFit control scope, M01 is physically/bookkeeping compatible but its local deformation is not identifiable against the LambdaCDM origin at the tested amplitudes.

This is not theory falsification. It is a concrete example of **data blindness to a valid model direction**.

## Design-prior delta

DP-0101 — controlled physical path to the reference limit.

DP-0102 — respect one-sided local geometry/tangent cones.

DP-0103 — optimize for covariance-whitened observable directions, not raw theory distance.

DP-0104 — small residuals must dominate and survive cross-solver calibration systematics.

DP-0105 — **local response amplitude must be compared to a real covariance scale.** A numerically clean response can still be observationally invisible by orders of magnitude.

DP-0106 — **nuisance-free Fisher information is an optimistic ceiling.** A future model whose signature already fails this ceiling needs a new/orthogonal observable channel rather than more interpretive complexity.

## Next M01 task

B6 comparator attack moves to Wave 02: test smooth-w against the nearest smooth-DE/background-growth mimics in the same whitened observation space.
