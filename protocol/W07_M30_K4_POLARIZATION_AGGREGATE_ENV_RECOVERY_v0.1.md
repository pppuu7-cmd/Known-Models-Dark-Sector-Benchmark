# W07 M30 K4 polarization aggregate environment recovery v0.1

Status: prospectively frozen before recovery execution.

Parent scientific run: `34750957481` (`W07 M30 K4 polarization-output recovery`).

Immutable scientific evidence:
- base artifact `10316090546`, digest `sha256:9a7e8ac262a876035731a2ef1989dfe02e224a084a85698bb19afe8ac5673e73`;
- radial artifact `10315464758`, digest `sha256:0ed59e7bb7ce1480ba19d3ea60d2f8c35af20705a5e38554de4ec42d8123e7d0`;
- cT artifact `10315676707`, digest `sha256:4d087fff86496b8f036a3ed773b947c682b21ec171c23068865691fec7ea60b9`.

All three parent scientific point jobs completed successfully. The parent aggregate failed before scientific classification solely because `verification/m30/k4_local_2d_precision.py` imports NumPy and the aggregate runner lacked NumPy (`ModuleNotFoundError: No module named 'numpy'`).

## Frozen recovery

Recovery is analysis-only. It MUST NOT rebuild hi_class, rerun any cosmology, alter the exact provider pin, local points, precision profiles, observables, grids, thresholds, statistic, or classification logic.

Allowed changes only:
1. download the three immutable parent artifacts from run `34750957481`;
2. install `numpy==2.3.3` for the aggregate analysis environment;
3. execute the unchanged command:
   `python3 verification/m30/k4_local_2d_precision.py aggregate m30-k4-artifacts M30_K4_LOCAL_2D_PRECISION_RESULT.json`;
4. upload the resulting JSON unchanged.

A green recovery workflow is not itself K4 PASS. Scientific classification is the machine result emitted by the unchanged frozen analyzer.
