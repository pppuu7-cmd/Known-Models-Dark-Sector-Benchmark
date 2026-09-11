#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from verification.m25.m25_k1_abundance_decoupling import ETAS

ORIGINAL_RUN_ID = 34548988620
ORIGINAL_ARTIFACT_ID = 10180157389
RECOVERY_PREREG = "protocol/W04_M25_K1_SUPPORT_ORDER_RECOVERY_PREREGISTRATION_v0.1.md"
ORIGINAL_PREREG = "protocol/W04_M25_RESONANT_STERILE_K1_ABUNDANCE_DECOUPLING_PREREGISTRATION_v0.1.md"


def locate_root(root: Path) -> Path:
    candidates = [root]
    candidates += [p for p in root.rglob("class_provider") if p.is_dir()]
    for p in candidates:
        if (p / "output").is_dir():
            return p
    raise RuntimeError(f"cannot locate class_provider/output under {root}")


def locate_file(root: Path, name: str) -> Path:
    hits = sorted(root.rglob(name))
    if len(hits) != 1:
        raise RuntimeError(f"expected one {name}, found {[str(x) for x in hits]}")
    return hits[0]


def order_label(x: np.ndarray) -> str:
    d = np.diff(x)
    if np.all(d > 0):
        return "strictly_increasing"
    if np.all(d < 0):
        return "strictly_decreasing"
    if np.any(d == 0):
        return "degenerate"
    return "nonmonotonic"


def load_table_sorted(path: Path, audit: dict, key: str) -> np.ndarray:
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
        raise RuntimeError(f"invalid table {path}: shape={a.shape}")
    x = a[:, 0]
    label = order_label(x)
    audit[key] = {
        "path": str(path),
        "rows": int(a.shape[0]),
        "columns": int(a.shape[1]),
        "original_order": label,
        "first_x": float(x[0]),
        "last_x": float(x[-1]),
        "min_x": float(np.min(x)),
        "max_x": float(np.max(x)),
    }
    idx = np.argsort(x, kind="mergesort")
    a = a[idx]
    if np.any(np.diff(a[:, 0]) <= 0):
        raise RuntimeError(f"non-unique interpolation support after sorting: {path}")
    return a


def resolve_output(root: Path, prefix: str, suffix: str) -> Path:
    outdir = root / "output"
    candidates = []
    exact = outdir / f"{prefix}_{suffix}.dat"
    if exact.exists():
        candidates.append(exact)
    for p in sorted(outdir.glob(f"{prefix}_*_{suffix}.dat")):
        if p not in candidates:
            candidates.append(p)
    if len(candidates) != 1:
        raise RuntimeError(f"output discovery {prefix}/{suffix}: {[str(p) for p in candidates]}")
    return candidates[0]


def channel(a: np.ndarray, col: int) -> np.ndarray:
    if col >= a.shape[1]:
        raise RuntimeError(f"missing column {col} in {a.shape}")
    return a[:, [0, col]]


def metric(model: np.ndarray, ref: np.ndarray) -> dict:
    if model.shape[1] != ref.shape[1]:
        raise RuntimeError(f"column mismatch model={model.shape[1]} ref={ref.shape[1]}")
    x = model[:, 0]
    xr = ref[:, 0]
    if np.any(np.diff(x) <= 0) or np.any(np.diff(xr) <= 0):
        raise RuntimeError("metric received non-increasing support")
    lo, hi = max(float(x.min()), float(xr.min())), min(float(x.max()), float(xr.max()))
    mask = (x >= lo) & (x <= hi)
    xq = x[mask]
    ym = model[mask, 1:]
    if xq.size < 3:
        raise RuntimeError("insufficient overlap")
    yr = np.column_stack([np.interp(xq, xr, ref[:, j]) for j in range(1, ref.shape[1])])
    scale = max(float(np.max(np.abs(ym))), float(np.max(np.abs(yr))), 1e-300)
    floor = 1e-12 * scale
    r = 2.0 * (ym - yr) / (np.abs(ym) + np.abs(yr) + floor)
    vals = np.abs(r).ravel()
    return {
        "median_abs": float(np.median(vals)),
        "rms": float(np.sqrt(np.mean(r * r))),
        "p95_abs": float(np.percentile(vals, 95)),
        "n": int(vals.size),
        "floor": float(floor),
    }


def judge(points: list[dict]) -> dict:
    r95 = [p["p95_abs"] for p in points]
    monotonic = all(r95[i + 1] <= r95[i] * 1.02 for i in range(len(r95) - 1))
    decreased = r95[-1] < r95[0]
    f = np.asarray(ETAS[-3:], dtype=float)
    r = np.asarray(r95[-3:], dtype=float)
    if np.any(r <= 0):
        fit = {"valid": False, "p": None}
        exponent = False
    else:
        p, logA = np.polyfit(np.log(f), np.log(r), 1)
        fit = {"valid": True, "p": float(p), "logA": float(logA)}
        exponent = bool(p > 0.5)
    return {
        "points": points,
        "r95": r95,
        "monotonic_with_2pct_slack": bool(monotonic),
        "smallest_lower_than_largest": bool(decreased),
        "fit_smallest3": fit,
        "exponent_gt_0p5": bool(exponent),
        "pass": bool(monotonic and decreased and exponent),
    }


def analyze(artifact_root: Path, out: Path) -> None:
    class_root = locate_root(artifact_root)
    status_path = locate_file(artifact_root, "m25_k1_status.json")
    manifest_path = locate_file(artifact_root, "manifest.json")
    original_result_path = locate_file(artifact_root, "m25_k1_result.json")
    status = json.loads(status_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    original = json.loads(original_result_path.read_text())
    audit: dict[str, dict] = {}

    result = {
        "schema": "KMDSB.M25.K1SupportOrderRecovery.v1",
        "recovery_preregistration": RECOVERY_PREREG,
        "original_preregistration": ORIGINAL_PREREG,
        "original_run_id": ORIGINAL_RUN_ID,
        "original_artifact_id": ORIGINAL_ARTIFACT_ID,
        "original_classification": original.get("classification"),
        "class_pin": original.get("class_pin"),
        "sterile_provider_pin": original.get("sterile_provider_pin"),
        "etas": ETAS,
        "K1_reference_limit": "NOT_PROMOTED",
        "K2_physical_geometry": "ONE_SIDED_ETA_GE_0",
        "K4_promoted": False,
        "physical_falsification": False,
        "status": status,
        "support_order_audit": audit,
        "models": {},
    }
    required = ["build", "ref"] + [f"m{m}_e{i}" for m in range(2) for i in range(len(ETAS))]
    if any(status.get(k) != 0 for k in required):
        result["classification"] = "M25_K1_SUPPORT_ORDER_RECOVERY_BLOCKED"
        result["failed_status_keys"] = [k for k in required if status.get(k) != 0]
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    ref_cl = load_table_sorted(resolve_output(class_root, "ref", "cl"), audit, "ref/cl")
    ref_pk = load_table_sorted(resolve_output(class_root, "ref", "pk"), audit, "ref/pk")
    ref_bg_raw = load_table_sorted(resolve_output(class_root, "ref", "background"), audit, "ref/background")
    ref_bg = ref_bg_raw[:, [0, 3]]
    all_pass = True

    for mi in range(2):
        finite = []
        for i in range(len(ETAS)):
            prefix = f"m{mi}_e{i}"
            cl = load_table_sorted(resolve_output(class_root, prefix, "cl"), audit, f"{prefix}/cl")
            pk = load_table_sorted(resolve_output(class_root, prefix, "pk"), audit, f"{prefix}/pk")
            bgraw = load_table_sorted(resolve_output(class_root, prefix, "background"), audit, f"{prefix}/background")
            finite.append({"cl": cl, "pk": pk, "bg": bgraw[:, [0, 3]]})
        specs = {
            "H": ([x["bg"] for x in finite], ref_bg),
            "Pk": ([x["pk"] for x in finite], ref_pk),
            "CMB_TT": ([channel(x["cl"], 1) for x in finite], channel(ref_cl, 1)),
            "CMB_EE": ([channel(x["cl"], 2) for x in finite], channel(ref_cl, 2)),
            "CMB_TE": ([channel(x["cl"], 3) for x in finite], channel(ref_cl, 3)),
        }
        mr = {
            "provider_directory": manifest["models"][f"m{mi}"]["provider_directory"],
            "blocks": {},
        }
        for block, (models, ref) in specs.items():
            pts = []
            for eta, arr in zip(ETAS, models):
                q = metric(arr, ref)
                q["eta"] = eta
                pts.append(q)
            mr["blocks"][block] = judge(pts)
            all_pass = all_pass and mr["blocks"][block]["pass"]
        mr["failing_blocks"] = [k for k, v in mr["blocks"].items() if not v["pass"]]
        result["models"][f"m{mi}"] = mr

    if all_pass:
        result["classification"] = "M25_K1_ABUNDANCE_DECOUPLING_PASS_WITH_SCOPE_ORDER_RECOVERED"
        result["K1_reference_limit"] = "PASS_WITH_SCOPE_ABUNDANCE_TO_ZERO_MIXED_CDM_EMBEDDING"
    else:
        result["classification"] = "M25_K1_ABUNDANCE_DECOUPLING_NOT_ESTABLISHED_ORDER_RECOVERED"
    result["classification_changed"] = result["classification"] != original.get("classification")
    result["reanalysis_only_no_class_recompute"] = True
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("artifact_root", type=Path)
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    analyze(args.artifact_root, args.out)
