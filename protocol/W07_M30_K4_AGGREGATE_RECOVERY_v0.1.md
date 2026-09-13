# W07 M30 / F30 K4 aggregate-only recovery v0.1

Status: FROZEN BEFORE RECOVERY EXECUTION

## Trigger
Authoritative production run `34719607382` completed all three frozen heavy point jobs (`base`, `radial`, `cT`) successfully and uploaded their point artifacts, but the downstream aggregate job failed before scientific classification with `ModuleNotFoundError: No module named 'numpy'` while importing the already-frozen analyzer `verification/m30/k4_local_2d_precision.py`.

## Scope lock
This recovery is execution-layer only. It MUST NOT rerun any provider calculation, alter any physical point, precision profile, observable, metric, threshold, analyzer logic, or frozen classification rule from `protocol/W07_M30_K4_LOCAL_2D_PRECISION_PREREGISTRATION_v0.1.md`.

The only permitted operations are:
1. download the three immutable point artifacts from run `34719607382`;
2. install the analyzer runtime dependency `python3-numpy`;
3. run the unchanged aggregate subcommand of `verification/m30/k4_local_2d_precision.py`;
4. upload the resulting aggregate JSON with provenance.

Expected immutable source artifacts:
- `m30-k4-base`, artifact `10305654365`, sha256 `d0e76d03a0b3929d01bffafa3e3ecd4f7e3185eb94a953c3a8c9820a32db60bb`;
- `m30-k4-radial`, artifact `10305053424`, sha256 `006a74d704115181b1e9815bcfdc1f17cd556e49b9b5f722470e8f6b6e83e976`;
- `m30-k4-cT`, artifact `10305993667`, sha256 `803f16fd978fbf24e1363b9fa0e9c44e754d2d2d97ea6aafedf3268cf264e0a0`.

Any inability to retrieve these exact run-scoped artifacts is `RECOVERY_BLOCKED`, not a scientific failure. Scientific classification is exactly the original frozen aggregate rule and remains `physical_falsification=false` for every outcome.
