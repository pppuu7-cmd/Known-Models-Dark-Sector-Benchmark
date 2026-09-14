#!/usr/bin/env python3
"""Frozen K3D2-D default/reference comparison.

Uses only the thresholds already frozen in
W03_M13B_K3D2B_ENABLED_TWO_FIELD_COSMOLOGY_REGRESSION_v0.1.md.
"""
from __future__ import annotations

import argparse
import bisect
import json
import math
from pathlib import Path

CROSSING_TOL = 2e-3
TODAY_FIELD_TOL = 1e-3
PK_L2_TOL = 5e-3
TT_L2_TOL = 5e-3


def one(root: Path, pattern: str) -> Path:
    hits = sorted(root.glob(pattern))
    if len(hits) != 1:
        raise RuntimeError((root, pattern, [str(x) for x in hits]))
    return hits[0]


def rows(path: Path):
    return [
        [float(x) for x in line.split()]
        for line in path.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def log_interp(xs, ys, x):
    i = bisect.bisect_left(xs, x)
    if i == 0:
        return ys[0]
    if i >= len(xs):
        return ys[-1]
    x0, x1 = xs[i - 1], xs[i]
    y0, y1 = ys[i - 1], ys[i]
    if x0 <= 0 or x1 <= 0 or x <= 0 or y0 <= 0 or y1 <= 0:
        f = (x - x0) / (x1 - x0)
        return y0 + f * (y1 - y0)
    f = (math.log(x) - math.log(x0)) / (math.log(x1) - math.log(x0))
    return math.exp(math.log(y0) + f * (math.log(y1) - math.log(y0)))


def pk_l2(default_file: Path, reference_file: Path):
    d = rows(default_file)
    r = rows(reference_file)
    if not d or not r:
        return math.inf, 0
    xr = [q[0] for q in r]
    yr = [q[1] for q in r]
    common = [q for q in d if xr[0] <= q[0] <= xr[-1]]
    if not common:
        return math.inf, 0
    num = sum((q[1] - log_interp(xr, yr, q[0])) ** 2 for q in common)
    den = sum(q[1] ** 2 for q in common)
    return math.sqrt(num / max(den, 1e-300)), len(common)


def tt_l2(default_file: Path, reference_file: Path):
    d = {int(round(q[0])): q[1] for q in rows(default_file) if len(q) >= 2 and 30 <= q[0] <= 1200}
    r = {int(round(q[0])): q[1] for q in rows(reference_file) if len(q) >= 2 and 30 <= q[0] <= 1200}
    ells = sorted(set(d) & set(r))
    if not ells:
        return math.inf, 0
    num = sum((d[l] - r[l]) ** 2 for l in ells)
    den = sum(d[l] ** 2 for l in ells)
    return math.sqrt(num / max(den, 1e-300)), len(ells)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--default-root", type=Path, required=True)
    ap.add_argument("--reference-root", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    dv = json.loads(one(a.default_root, "result/default_verify.json").read_text())
    rv = json.loads(one(a.reference_root, "result/reference/default_verify.json").read_text())

    dz = dv["B1"]["crossings"][0]
    rz = rv["B1"]["crossings"][0]
    crossing_diff = abs(dz - rz)

    today_diff = {
        key: abs(dv["B1"]["today"][key] - rv["B1"]["today"][key])
        for key in ("x", "p", "y", "q")
    }

    dpk = one(a.default_root, "out/default*_pk.dat")
    rpk = one(a.reference_root, "out/ref*_pk.dat")
    dcl = one(a.default_root, "out/default*_cl.dat")
    rcl = one(a.reference_root, "out/ref*_cl.dat")
    pk_norm, pk_rows = pk_l2(dpk, rpk)
    tt_norm, tt_rows = tt_l2(dcl, rcl)

    checks = {
        "default_B1_B2_B3_pass": bool(dv.get("all_default_required_checks_pass")),
        "reference_B1_B2_B3_pass": bool(rv.get("all_default_required_checks_pass")),
        "crossing_abs_diff_le_2e_3": crossing_diff <= CROSSING_TOL,
        "today_x_abs_diff_le_1e_3": today_diff["x"] <= TODAY_FIELD_TOL,
        "today_p_abs_diff_le_1e_3": today_diff["p"] <= TODAY_FIELD_TOL,
        "today_y_abs_diff_le_1e_3": today_diff["y"] <= TODAY_FIELD_TOL,
        "today_q_abs_diff_le_1e_3": today_diff["q"] <= TODAY_FIELD_TOL,
        "pk_normalized_L2_le_5e_3": pk_norm <= PK_L2_TOL,
        "tt_normalized_L2_ell30_1200_le_5e_3": tt_norm <= TT_L2_TOL,
        "pk_common_rows_nonzero": pk_rows > 0,
        "tt_common_ells_nonzero": tt_rows > 0,
    }
    ok = all(checks.values())
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2DSelfConsistentDefaultReferenceComparison.v0.1",
        "thresholds": {
            "crossing_abs": CROSSING_TOL,
            "today_x_p_y_q_abs_each": TODAY_FIELD_TOL,
            "pk_normalized_L2": PK_L2_TOL,
            "tt_normalized_L2_ell30_1200": TT_L2_TOL,
        },
        "values": {
            "default_crossing_z": dz,
            "reference_crossing_z": rz,
            "crossing_abs_difference": crossing_diff,
            "today_abs_differences": today_diff,
            "pk_normalized_L2": pk_norm,
            "pk_common_rows": pk_rows,
            "tt_normalized_L2_ell30_1200": tt_norm,
            "tt_common_ells": tt_rows,
        },
        "checks": checks,
        "all_required_checks_pass": ok,
        "classification": (
            "M13B_K3D2D_DEFAULT_REFERENCE_NUMERICAL_REPRODUCIBILITY_PASS"
            if ok
            else "M13B_K3D2D_DEFAULT_REFERENCE_NUMERICAL_REPRODUCIBILITY_GAP"
        ),
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    print(json.dumps(obj, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
