# W04 M20 SASHIMI-SIDM provider control preregistration v0.1

## Purpose
Establish whether the pinned nonlinear SIDM provider is executable, passes its own source-bound physics regression suite, and possesses a numerically safe exact zero-cross-section CDM boundary before KMDSB designs any M20 K1 convergence ladder.

No K1/K4/K6/K7 promotion is authorized by this provider-control test.

## Provider
`shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`

The provider README identifies the code as SASHIMI-SIDM, a semi-analytical subhalo implementation for self-interacting dark matter, and links arXiv:2403.16633 and arXiv:2305.16176.

## Frozen environment
Hosted Ubuntu runner, Python supplied by the runner, with pinned Python dependencies:
- numpy 2.3.3
- scipy 1.16.1
- numexpr 2.11.0
- tqdm 4.67.1
- pytest 8.4.1

No provider source patch is allowed.

## Control A — upstream physics suite
Run exactly:

`pytest -q test_sashimi.py`

Record pass/fail and complete stdout. This suite contains equation-level and end-to-end physics checks, including the upstream small-cross-section SIDM→CDM regression.

## Control B — exact sigma0_m = 0 smoke
Instantiate:

`subhalo_properties(sigma0_m=0.0, w=24.33)`

and run the reduced end-to-end catalog settings used by the upstream regression:

- M0 = 1e12 Msun
- redshift = 0
- M0_at_redshift = True
- dz = 0.2
- N_herm = 3
- zmax = 4
- logmamin = 9
- N_ma = 30

For entries with positive SIDM weight require:
- at least one surviving/weighted entry;
- all compared SIDM/CDM structural outputs finite;
- exact-zero SIDM `Vmax`, `rmax`, `rs`, `rhos` agree with simultaneously returned CDM counterparts to rtol <= 1e-10, unless floating-point propagation through a formally infinite collapse time prevents this; report the measured maximum residual rather than relaxing the threshold post hoc;
- `|rcSIDM|/rsSIDM <= 1e-10` for all retained entries;
- no exception or non-zero process exit.

Also record whether intermediate `tt_ratio` is finite. An infinite collapse time itself is physically expected at zero scattering; a non-finite internal diagnostic is acceptable only if all returned physical catalog outputs remain finite and exactly reduce to CDM. If physical outputs are contaminated, classify the exact-zero path as blocked.

## Classification
- `M20_PROVIDER_CONTROL_PASS_EXACT_ZERO_CDM_BOUNDARY` if Control A passes and Control B returns finite physical outputs satisfying the exact frozen identity/core conditions.
- `M20_PROVIDER_CONTROL_PASS_SMALL_SIGMA_EXACT_ZERO_BLOCKED` if the upstream suite passes but exact zero contaminates or aborts physical outputs.
- `M20_PROVIDER_CONTROL_BLOCKED` otherwise.

All classifications have `physical_falsification=false` and `K1_promoted=false`.

## Next step
Only after this control may KMDSB preregister a nonzero cross-section ladder and nonlinear multi-channel K1/K4 study.
