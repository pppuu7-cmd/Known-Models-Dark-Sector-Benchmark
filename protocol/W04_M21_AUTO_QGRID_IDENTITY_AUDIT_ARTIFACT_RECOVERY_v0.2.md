# W04 M21 automatic ncdm q-grid identity audit — artifact-only implementation recovery v0.2

Frozen: 2026-09-14 after the v0.1 audit reached `M21_AUTO_QGRID_AUDIT_BLOCKED`, and before execution of the v0.2 recovery parser.

Family: F21 / M21 mixed cold+warm dark matter  
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Scope and governance

This is an **implementation recovery**, not a replacement physical experiment and not a post-hoc physics retune.

The original v0.1 result remains historically `M21_AUTO_QGRID_AUDIT_BLOCKED`. This v0.2 procedure does not alter any physical case, precision profile, q-grid values, numerical threshold, K1 threshold, or cosmological output. It only re-parses already-produced artifacts from the same frozen run after two implementation defects in the v0.1 orchestration were identified.

No CLASS provider execution is authorized by this recovery. Only artifact parsing is permitted.

`K1_promoted=false` and `physical_falsification=false` for every v0.2 outcome.

## Immutable source evidence

Original frozen protocol:

- `protocol/W04_M21_AUTO_QGRID_IDENTITY_AUDIT_v0.1.md`

Original workflow run:

- run `34864061202`
- head `261a0e38a3c3dedacf006bf3195b11495705e1ab`

Frozen source artifacts:

- `m21-qgrid-f2`: artifact `10357080247`, digest `sha256:1f2e464e1a68aec33ec3a0a9b8a19baeea82c69a0caf2e7eeb9d968e3862d674`
- `m21-qgrid-f3`: artifact `10356755518`, digest `sha256:10cf196b702f2566d8dddd6f7ac5dafdb177597ce4ceecd5c6ac070bd676b5e5`
- `m21-qgrid-f4`: artifact `10355554458`, digest `sha256:6aedea1ef11d8c5146e14d3532dacc4f388d47f9f9949b3b9bb624c6ab5f9b89`
- `m21-qgrid-f3_manual`: artifact `10357017735`, digest `sha256:661c454eef830e0d72bc8619fd2df466bedb16f4854e2dd8e418beed12cbcf5b`
- original aggregate `m21-auto-qgrid-identity-audit`: artifact `10357151669`, digest `sha256:0e17865f9963cccd27544170518a343cc47e3c2c25dbeffa353009e34d9b09d5`

## Defect A — negative-control completion was coupled to irrelevant cosmology completion

The v0.1 protocol says the `f3_manual` branch is a negative control only: its cosmological output is not interpreted; it exists solely to verify that the output-only instrumentation detects a deliberately changed q-grid.

The v0.1 workflow nevertheless required `provider_rc == 0` **before** parsing the q-grid record. In run `34864061202`, the manual branch emitted a complete `KMDSB_QGRID_BEGIN ... KMDSB_QGRID_END` record for the deliberately changed grid and was later terminated by the provider timeout (`rc=124`) while continuing the expensive cosmological calculation. The already-emitted grid was therefore discarded and the lane became `null` in the aggregate.

v0.2 correction: for the **manual negative control only**, validity is determined at the q-grid observation boundary. A complete finite begin/point/end record, valid output-only instrumentation, and the exact frozen manual controls are required. Provider return code is recorded but is not a validity condition after a complete q-grid record has been emitted. Physical `f2/f3/f4` lanes still require `provider_rc == 0`.

## Defect B — v0.1 abundance-distinction witness was sampled before CLASS applies omega normalization

The v0.1 protocol attempted to prove the physical lanes were not identical by requiring `deg_ncdm` or `factor_ncdm` to differ in the q-grid printout.

At the exact provider pin, `background_ncdm_init()` constructs the q-grid and computes the initial `factor_ncdm` from `deg_ncdm`, `T_cmb`, and `T_ncdm`. Only **after** `background_ncdm_init()` returns, `input.c` uses the requested `Omega0_ncdm`/`omega_ncdm` to compute `fnu_factor` and rescales both `factor_ncdm` and `deg_ncdm`. Therefore the v0.1 print location is upstream of the abundance normalization it intended to witness.

v0.2 correction: input distinctness is certified directly from the immutable generated `lane.ini` files produced by `verification/m21/mixed_cold_warm_k1_reference.py`. The exact required values are:

- `f2`: `omega_ncdm = 0.0012` (`f_w=0.01`)
- `f3`: `omega_ncdm = 0.00036` (`f_w=0.003`)
- `f4`: `omega_ncdm = 0.00012` (`f_w=0.001`)

These values are fixed by `OMEGA_DM=0.12` and the pre-existing frozen fraction list. No output-dependent choice is introduced.

## Frozen artifact-only checks

For each physical lane `f2/f3/f4`:

1. exactly one complete finite q-grid record must be recoverable from the saved run log;
2. saved instrumentation manifest must certify one output-only insertion and no changes to arrays, equations, inputs, or tolerances;
3. `provider_rc == 0`;
4. `lane.ini` must contain the exact `omega_ncdm` value listed above.

For `f3_manual`:

1. exactly one complete finite q-grid record must be recoverable from the saved run log;
2. the same output-only instrumentation checks apply;
3. `lane.ini` must contain `omega_ncdm = 0.00036` and exactly the frozen manual controls `ncdm_quadrature_strategy=3`, `ncdm_N_momentum_bins=150`, `ncdm_maximum_q=15`;
4. provider return code is provenance only and is not a validity gate once the complete q-grid record is present.

Hash the canonical serialized `(strategy,q_size,q[],w[])` payload for each lane.

## Frozen classifications

### `M21_AUTO_QGRID_IDENTICAL_ACROSS_FRACTIONS_RECOVERED`

if all physical lanes are valid, their q-grid payloads are exactly identical, their frozen `omega_ncdm` inputs are the three exact distinct values above, and the manual negative-control q-grid hash differs from the automatic `f3` hash.

### `M21_AUTO_QGRID_FRACTION_DEPENDENT_RECOVERED`

if all physical lanes are valid, at least one physical automatic q-grid payload differs, the three exact distinct `omega_ncdm` inputs are present, and the manual negative control differs from automatic `f3`.

### `M21_AUTO_QGRID_ARTIFACT_RECOVERY_BLOCKED`

if any required saved artifact/record is missing or nonfinite, instrumentation is not output-only, a physical lane did not complete successfully, frozen input identity cannot be certified, or the negative control does not produce a different q-grid.

## Interpretation ceiling

A recovered identical-grid result rules out **fraction-dependent automatic perturbation-grid selection** as the direct cause of the isolated `f3` excursion. It does **not** rule out quadrature error on a common grid, transfer/source interpolation effects, precision sensitivity, or any other numerical layer.

A recovered fraction-dependent result would authorize a separately preregistered quadrature-resolution diagnostic.

Neither recovered outcome promotes K1, K3, or K4, and neither is a physical falsification of mixed WDM.
