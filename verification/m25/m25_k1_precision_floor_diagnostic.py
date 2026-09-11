#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

ETAS = [0.01, 0.003, 0.001]


def load_table(path: Path) -> np.ndarray:
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        try:
            row = [float(v.replace("D", "E").replace("d", "e")) for v in s.split()]
        except ValueError:
            continue
        if row and all(math.isfinite(v) for v in row):
            rows.append(row)
    a = np.asarray(rows, dtype=float)
    if a.ndim != 2 or a.shape[0] < 3 or a.shape[1] < 2:
        raise RuntimeError(f"invalid table {path}: {a.shape}")
    a = a[np.argsort(a[:, 0], kind="mergesort")]
    if np.any(np.diff(a[:, 0]) <= 0):
        raise RuntimeError(f"non-unique support in {path}")
    return a


def output(root: Path, prefix: str, suffix: str) -> Path:
    out = root / "output"
    hits = []
    exact = out / f"{prefix}_{suffix}.dat"
    if exact.exists():
        hits.append(exact)
    for p in sorted(out.glob(f"{prefix}_*_{suffix}.dat")):
        if p not in hits:
            hits.append(p)
    if len(hits) != 1:
        raise RuntimeError(f"output discovery {prefix}/{suffix}: {[str(p) for p in hits]}")
    return hits[0]


def ch(a: np.ndarray, col: int) -> np.ndarray:
    return a[:, [0, col]]


def metric(model: np.ndarray, ref: np.ndarray) -> dict:
    lo = max(float(model[:, 0].min()), float(ref[:, 0].min()))
    hi = min(float(model[:, 0].max()), float(ref[:, 0].max()))
    mask = (model[:, 0] >= lo) & (model[:, 0] <= hi)
    x = model[mask, 0]
    ym = model[mask, 1:]
    if x.size < 3:
        raise RuntimeError("insufficient overlap")
    yr = np.column_stack([np.interp(x, ref[:, 0], ref[:, j]) for j in range(1, ref.shape[1])])
    scale = max(float(np.max(np.abs(ym))), float(np.max(np.abs(yr))), 1e-300)
    floor = 1e-12 * scale
    r = 2.0 * (ym - yr) / (np.abs(ym) + np.abs(yr) + floor)
    vals = np.abs(r).ravel()
    return {
        "p95_abs": float(np.percentile(vals, 95)),
        "median_abs": float(np.median(vals)),
        "rms": float(np.sqrt(np.mean(r * r))),
        "n": int(vals.size),
    }


def judge(points: list[dict]) -> dict:
    r95 = [p["p95_abs"] for p in points]
    mono = all(r95[i + 1] <= 1.02 * r95[i] for i in range(2))
    lower = r95[-1] < r95[0]
    if any(v <= 0 for v in r95):
        p = None
        exp = False
    else:
        p = float(np.polyfit(np.log(np.asarray(ETAS)), np.log(np.asarray(r95)), 1)[0])
        exp = p > 0.5
    return {
        "points": points,
        "r95": r95,
        "monotonic_with_2pct_slack": bool(mono),
        "smallest_lower_than_largest": bool(lower),
        "tail_exponent_p": p,
        "exponent_gt_0p5": bool(exp),
        "tail_scaling_recovered": bool(mono and lower and exp),
    }


def analyze(root: Path, model: str, profile: str, status_path: Path, out: Path) -> None:
    status = json.loads(status_path.read_text())
    result = {
        "schema": "KMDSB.M25.K1PrecisionFloorDiagnostic.v1",
        "preregistration": "protocol/W04_M25_K1_PRECISION_FLOOR_DIAGNOSTIC_PREREGISTRATION_v0.1.md",
        "original_run_id": 34548988620,
        "original_artifact_id": 10180157389,
        "model": model,
        "precision_profile": profile,
        "etas": ETAS,
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
        "status": status,
    }
    required = ["build", "ref", "e2", "e3", "e4"]
    if any(status.get(k) != 0 for k in required):
        result["classification"] = "M25_PRECISION_FLOOR_DIAGNOSTIC_PROVIDER_BLOCKED"
        result["failed_status_keys"] = [k for k in required if status.get(k) != 0]
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ref_cl = load_table(output(root, "ref", "cl"))
    ref_pk = load_table(output(root, "ref", "pk"))
    ref_bg = load_table(output(root, "ref", "background"))[:, [0, 3]]
    cases = []
    for i in (2, 3, 4):
        prefix = f"{model}_e{i}"
        cases.append({
            "cl": load_table(output(root, prefix, "cl")),
            "pk": load_table(output(root, prefix, "pk")),
            "bg": load_table(output(root, prefix, "background"))[:, [0, 3]],
        })

    specs = {
        "H": ([c["bg"] for c in cases], ref_bg),
        "Pk": ([c["pk"] for c in cases], ref_pk),
        "CMB_TT": ([ch(c["cl"], 1) for c in cases], ch(ref_cl, 1)),
        "CMB_EE": ([ch(c["cl"], 2) for c in cases], ch(ref_cl, 2)),
        "CMB_TE": ([ch(c["cl"], 3) for c in cases], ch(ref_cl, 3)),
    }
    blocks = {}
    for name, (arrs, ref) in specs.items():
        pts = []
        for eta, arr in zip(ETAS, arrs):
            q = metric(arr, ref)
            q["eta"] = eta
            pts.append(q)
        blocks[name] = judge(pts)
    result["blocks"] = blocks
    h_ok = blocks["H"]["tail_scaling_recovered"]
    targets = ["CMB_TT", "CMB_EE", "CMB_TE"] if profile == "cl_ref" else ["Pk", "CMB_TT", "CMB_EE", "CMB_TE"]
    n_ok = sum(blocks[k]["tail_scaling_recovered"] for k in targets)
    result["target_blocks"] = targets
    result["target_blocks_recovered"] = int(n_ok)
    result["target_blocks_total"] = len(targets)
    if h_ok and n_ok == len(targets):
        cls = "M25_PRECISION_FLOOR_TAIL_SCALING_RECOVERED"
    elif n_ok > 0:
        cls = "M25_PRECISION_FLOOR_TAIL_SCALING_PARTIAL"
    else:
        cls = "M25_PRECISION_FLOOR_TAIL_SCALING_NOT_RECOVERED"
    result["classification"] = cls
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("model", choices=["m0", "m1"])
    ap.add_argument("profile", choices=["cl_ref", "pk_ref"])
    ap.add_argument("status", type=Path)
    ap.add_argument("out", type=Path)
    a = ap.parse_args()
    analyze(a.root, a.model, a.profile, a.status, a.out)
