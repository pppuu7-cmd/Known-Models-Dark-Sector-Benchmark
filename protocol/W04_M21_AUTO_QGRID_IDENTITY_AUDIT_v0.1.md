# W04 M21 automatic ncdm q-grid identity audit v0.1

Frozen: 2026-09-14 before runtime q-grid inspection.

Family: F21 / M21 mixed cold+warm dark matter  
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Trigger

The prospectively frozen integrator-branch diagnostic is terminal `M21_INTEGRATOR_BRANCH_EXCURSION_PERSISTS`: the deterministic CMB excursion at `f_w=0.003` survives both default NDF15 and explicit RK, while direct RK-vs-NDF differences are much smaller than the excursion. The next candidate numerical layer is the ncdm phase-space discretization.

Before changing the quadrature method or resolution, this audit asks a narrower source/runtime question: does CLASS's default automatic ncdm momentum grid itself change between the already frozen `f_w={0.01,0.003,0.001}` cases when `m_ncdm/T_ncdm` is held fixed and abundance is changed through the provider's normalization path?

This is diagnostic only. It cannot promote K1 and cannot by itself authorize a quadrature-based K1 recovery.

## Frozen physical cases

Reuse without edits:

`verification/m21/mixed_cold_warm_k1_reference.py prepare`

and inspect only:

- `f2`: `f_w=0.01`;
- `f3`: `f_w=0.003`;
- `f4`: `f_w=0.001`.

The already frozen physics remains `m_ncdm=3000 eV`, `T_ncdm=0.71611`, total `omega_dm=0.12`, with abundance normalization as prepared by the existing script.

Use the same exact P2 precision profile as the previous integrator diagnostic:

- pinned `cl_permille.pre`;
- concatenated `verification/m21/m21_ncdm_tight.pre`.

## Diagnostic source modification

A fresh exact-pin clone may receive one output-only diagnostic insertion in `source/background.c`, immediately after perturbation q-sampling has been constructed and immediately before allocation of `dlnf0_dlnq_ncdm[k]`.

For every ncdm species record, at full binary64 precision where applicable:

- quadrature strategy integer;
- `q_size_ncdm[k]`;
- every `q_ncdm[k][i]`;
- every `w_ncdm[k][i]`;
- `deg_ncdm[k]`;
- `factor_ncdm[k]`.

The insertion may only print data. It must not modify arrays, inputs, tolerances, solver, physical equations or output values.

## Independent lanes

Run `f2`, `f3`, `f4` as separate GitHub Actions jobs from fresh exact-pin clones. A fourth negative-control lane uses a copy of `f3` with only the explicitly supported quadrature controls changed to:

- `ncdm_quadrature_strategy = 3` (`qm_trapz`);
- `ncdm_N_momentum_bins = 150`;
- `ncdm_maximum_q = 15`.

The negative-control branch is not a scientific alternative model and its cosmological output is not interpreted; it only verifies that the q-grid instrumentation can detect a deliberately changed grid construction.

## Frozen comparisons

Hash the serialized perturbation q-grid payload `(strategy,q_size,q[],w[])` for each lane.

Also compare `deg_ncdm` and `factor_ncdm` between physical lanes.

Classification:

### `M21_AUTO_QGRID_IDENTICAL_ACROSS_FRACTIONS`

if all are true:

1. f2/f3/f4 all execute far enough to emit a finite q-grid record;
2. their strategy, q_size, every q node and every q weight are exactly identical as parsed binary64 values;
3. at least one abundance-normalization quantity (`deg_ncdm` or `factor_ncdm`) differs across f2/f3/f4, proving the audit is not accidentally comparing identical physical inputs;
4. the manual-trapz negative control has a q-grid hash different from the auto f3 hash.

### `M21_AUTO_QGRID_FRACTION_DEPENDENT`

if all physical lanes emit valid records but any auto-grid object differs between f2/f3/f4.

### `M21_AUTO_QGRID_AUDIT_BLOCKED`

if a required physical record is missing/nonfinite, source instrumentation is not output-only, or the negative control fails to distinguish the changed grid.

## Interpretation ceiling

- Identical grids would rule out a **fraction-dependent automatic grid selection** as the direct cause of the isolated f3 excursion, but would not rule out phase-space quadrature error on a common grid.
- Fraction-dependent grids would authorize a separately preregistered manual/high-resolution quadrature diagnostic.
- Neither outcome promotes K1, K3 or K4.
- No physical mixed-WDM falsification is permitted.

`K1_promoted=false`, `physical_falsification=false` in all outcomes.
