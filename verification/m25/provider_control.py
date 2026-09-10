#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

PIN = "e4486265e8207aa0dd28decc8c8d897266c0a52a"
PREREG = "protocol/W04_M25_RESONANT_STERILE_DM_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md"
FLOAT_RE = re.compile(r"^[ \t]*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][+-]?\d+)?)")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def numeric_rows(path: Path) -> list[list[float]]:
    rows: list[list[float]] = []
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("!"):
            continue
        vals = []
        for tok in s.split():
            try:
                vals.append(float(tok.replace("D", "E").replace("d", "e")))
            except ValueError:
                break
        if vals and all(math.isfinite(x) for x in vals):
            rows.append(vals)
    return rows


def params_values(path: Path) -> list[float]:
    vals = []
    for line in path.read_text(errors="replace").splitlines():
        m = FLOAT_RE.match(line)
        if m:
            vals.append(float(m.group(1).replace("D", "E").replace("d", "e")))
    return vals


def validate_model(d: Path, reference_root: Path) -> dict:
    p = d / "params.dat"
    s = d / "state.dat"
    snap = d / "Snapshot100.dat"
    out = {
        "directory": d.name,
        "files_present": {"params.dat": p.exists(), "state.dat": s.exists(), "Snapshot100.dat": snap.exists()},
        "valid": False,
        "checks": {},
        "generated_sha256": {},
        "committed_reference_sha256": {},
    }
    if not all((p.exists(), s.exists(), snap.exists())):
        return out

    pv = params_values(p)
    sr = numeric_rows(s)
    rr = numeric_rows(snap)
    out["params_values"] = pv[:6]
    out["state_rows"] = len(sr)
    out["snapshot_rows"] = len(rr)

    checks = {}
    checks["params_six_finite"] = len(pv) >= 6 and all(math.isfinite(x) for x in pv[:6])
    checks["state_shape"] = len(sr) >= 2 and all(len(r) >= 5 for r in sr)
    checks["snapshot_shape"] = len(rr) >= 100 and all(len(r) >= 3 for r in rr)
    if checks["snapshot_shape"]:
        mom = [r[0] for r in rr]
        fs = [r[1] for r in rr]
        fb = [r[2] for r in rr]
        checks["momentum_positive_strict"] = all(x > 0 for x in mom) and all(b > a for a, b in zip(mom, mom[1:]))
        checks["psd_nonnegative"] = all(x >= 0 for x in fs) and all(x >= 0 for x in fb)
        out["snapshot_summary"] = {
            "p_min_MeV": min(mom), "p_max_MeV": max(mom),
            "f_nu_min": min(fs), "f_nu_max": max(fs),
            "f_nubar_min": min(fb), "f_nubar_max": max(fb),
        }
    else:
        checks["momentum_positive_strict"] = False
        checks["psd_nonnegative"] = False

    if checks["params_six_finite"]:
        omega, os, osb = pv[3], pv[4], pv[5]
        out["density_summary"] = {
            "omega_wdm_h2": omega, "omega_s_h2": os, "omega_sbar_h2": osb,
            "sum_residual": abs(omega - (os + osb)),
            "target_residual": abs(omega - 0.1188),
        }
        checks["density_sum"] = abs(omega - (os + osb)) <= 5e-8
        checks["closure_target"] = abs(omega - 0.1188) <= 5e-4
    else:
        checks["density_sum"] = False
        checks["closure_target"] = False

    for f in (p, s, snap):
        out["generated_sha256"][f.name] = sha256(f)
        rp = reference_root / d.name / f.name
        if rp.exists():
            out["committed_reference_sha256"][f.name] = sha256(rp)

    out["checks"] = checks
    out["valid"] = all(checks.values())
    return out


def main(status_path: Path, generated: Path, reference: Path, out_path: Path) -> None:
    status = json.loads(status_path.read_text())
    build_rc = int(status.get("build_rc", 999))
    run_rc = int(status.get("run_rc", 999))
    timed_out = bool(status.get("timed_out", False)) or run_rc == 124

    result = {
        "schema": "KMDSB.M25.ProviderControl.v1",
        "provider": "ntveem/sterile-dm",
        "provider_pin": PIN,
        "preregistration": PREREG,
        "K1_promoted": False,
        "physical_falsification": False,
        "status": status,
        "models": [],
    }

    if build_rc != 0:
        result["classification"] = "M25_PROVIDER_CONTROL_BLOCKED_BUILD"
    elif timed_out:
        result["classification"] = "M25_PROVIDER_CONTROL_BLOCKED_RUNTIME"
    elif run_rc != 0:
        result["classification"] = "M25_PROVIDER_CONTROL_OUTPUT_INVALID"
    else:
        if generated.exists():
            for d in sorted(x for x in generated.iterdir() if x.is_dir()):
                if (d / "params.dat").exists() or (d / "state.dat").exists():
                    result["models"].append(validate_model(d, reference))
        valid = [m for m in result["models"] if m.get("valid")]
        result["valid_model_count"] = len(valid)
        result["classification"] = (
            "M25_PROVIDER_CONTROL_PASS_STOCK_RESONANT_PSD"
            if len(valid) >= 2
            else "M25_PROVIDER_CONTROL_OUTPUT_INVALID"
        )

    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("status", type=Path)
    ap.add_argument("generated", type=Path)
    ap.add_argument("reference", type=Path)
    ap.add_argument("out", type=Path)
    a = ap.parse_args()
    main(a.status, a.generated, a.reference, a.out)
