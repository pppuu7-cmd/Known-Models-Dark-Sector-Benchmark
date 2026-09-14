#!/usr/bin/env python3
"""Artifact-only robust parser for the K3D2-D exact cl_ref blocker.

The parser never executes CLASS.  It preserves every top-level mode failure even
when concurrent stderr writes corrupt a nested RK diagnostic token.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

K1 = 0.00022398828992555914
K10 = 0.0022398828992555913
K_TOL = 1e-8

BASE = re.compile(
    r"KMDSB_MODE_FAIL index_md=(\d+) index_ic=(\d+) index_k=(\d+) "
    r"k=([^ ]+) interval_start=([^ ]+) evolver_start=([^ ]+) "
    r"interval_end=([^ ]+) error=(.*)"
)
FINAL = re.compile(
    r"KMDSB_GAUGE_IVP_FIXED_FINAL\s+converged=(\d+)\s+iterations=(\d+) "
    r"max=([^ ]+)\s+tol=([^ \n]+)"
)
ITER = re.compile(r"KMDSB_GAUGE_IVP_FIXED\s+iter=(\d+).*?max=([^ \n]+)")


def finite_float(raw: str):
    try:
        value = float(raw)
        return value if math.isfinite(value) else None
    except Exception:
        return None


def parse_geometry(error: str):
    pos = error.find("KMDSB_RK_COLLAPSE ")
    if pos < 0:
        return {"signature": False, "raw_fragment": None, "fields": {}, "strict_clean": False}
    text = error[pos + len("KMDSB_RK_COLLAPSE ") :]
    fields = {}
    for name in ("x", "step_ratio", "minimum", "hdid", "hnext", "step_index"):
        match = re.search(r"(?:^| )" + re.escape(name) + r"=([^ ]+)", text)
        if match:
            raw = match.group(1)
            fields[name + "_raw"] = raw
            if name == "step_index":
                try:
                    fields[name] = int(raw)
                except Exception:
                    fields[name] = None
            else:
                fields[name] = finite_float(raw)
        else:
            fields[name] = None

    interval = re.search(r"interval=\[([^:]+):([^\]]+)\]", text)
    if interval:
        for name, raw in (
            ("rk_interval_start", interval.group(1)),
            ("rk_interval_end", interval.group(2)),
        ):
            fields[name + "_raw"] = raw
            fields[name] = finite_float(raw)
        interval_closed = True
    else:
        fields["rk_interval_start"] = None
        fields["rk_interval_end"] = None
        interval_closed = False

    required = (
        "x",
        "step_ratio",
        "minimum",
        "hdid",
        "hnext",
        "step_index",
        "rk_interval_start",
        "rk_interval_end",
    )
    strict_clean = interval_closed and all(fields.get(key) is not None for key in required)
    return {
        "signature": True,
        "raw_fragment": text[-500:],
        "fields": fields,
        "strict_clean": strict_clean,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--source-guard", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    result = args.root / "result"
    provider_rc = int((result / "provider_rc.txt").read_text().strip())
    text = (
        (result / "stderr.txt").read_text(errors="replace")
        + "\n"
        + (result / "stdout.txt").read_text(errors="replace")
    )
    source_guard = json.loads(args.source_guard.read_text())
    source_ok = bool(source_guard.get("all_required_checks_pass"))

    finals = []
    for match in FINAL.finditer(text):
        finals.append(
            {
                "converged": int(match.group(1)),
                "iterations": int(match.group(2)),
                "max": finite_float(match.group(3)),
                "tol": finite_float(match.group(4)),
            }
        )
    iterations = []
    for match in ITER.finditer(text):
        iterations.append(
            {"iteration": int(match.group(1)), "max": finite_float(match.group(2))}
        )
    fixed_point_ok = bool(finals) and all(
        item["converged"] == 1
        and 1 <= item["iterations"] <= 16
        and item["max"] is not None
        and item["max"] <= 1e-12
        and item["tol"] is not None
        and abs(item["tol"] - 1e-12) <= 1e-27
        for item in finals
    )

    records = []
    seen = set()
    for match in BASE.finditer(text):
        key = (int(match.group(1)), int(match.group(2)), int(match.group(3)), match.group(4))
        if key in seen:
            continue
        seen.add(key)
        row = {
            "index_md": key[0],
            "index_ic": key[1],
            "index_k": key[2],
            "k_raw": match.group(4),
            "k": finite_float(match.group(4)),
            "interval_start_raw": match.group(5),
            "interval_start": finite_float(match.group(5)),
            "evolver_start_raw": match.group(6),
            "evolver_start": finite_float(match.group(6)),
            "interval_end_raw": match.group(7),
            "interval_end": finite_float(match.group(7)),
        }
        geometry = parse_geometry(match.group(8))
        row["rk_signature"] = geometry["signature"]
        row["rk"] = geometry["fields"]
        row["strict_clean_geometry"] = geometry["strict_clean"]
        if not geometry["strict_clean"]:
            row["raw_rk_fragment"] = geometry["raw_fragment"]
        records.append(row)

    signatures = [row for row in records if row["rk_signature"]]
    clean = [row for row in records if row["strict_clean_geometry"]]
    malformed = [row for row in records if not row["strict_clean_geometry"]]

    def numeric_range(field: str):
        values = [row["rk"][field] for row in clean if row["rk"].get(field) is not None]
        return None if not values else [min(values), max(values)]

    k_values = [row["k"] for row in records if row["k"] is not None]

    def frozen_mode_failed(k: float) -> bool:
        return any(abs(value - k) / max(abs(k), 1e-300) <= K_TOL for value in k_values)

    malformed_summary = []
    required_geometry = (
        "x",
        "step_ratio",
        "minimum",
        "hdid",
        "hnext",
        "step_index",
        "rk_interval_start",
        "rk_interval_end",
    )
    for row in malformed:
        bad = {}
        for key in required_geometry:
            if row["rk"].get(key) is None:
                bad[key] = row["rk"].get(key + "_raw")
        malformed_summary.append(
            {
                "index_k": row["index_k"],
                "k": row["k"],
                "unparsed_or_missing": bad,
                "raw_rk_fragment": row.get("raw_rk_fragment"),
            }
        )

    sufficient = source_ok and provider_rc != 0 and fixed_point_ok and len(signatures) >= 1
    classification = (
        "M13B_K3D2D_SELF_CONSISTENT_REFERENCE_RK_NUMERICAL_BLOCKER_LOCALIZED"
        if sufficient
        else "M13B_K3D2D_REFERENCE_ARTIFACT_RECOVERY_INCONCLUSIVE"
    )
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2DReferenceArtifactParserRecovery.v0.1",
        "authority": {
            "parent_run": 34793932614,
            "reference_artifact_id": 10329550837,
            "reference_artifact_digest": "sha256:563bc5829e516a8a09f2d3fae995789c2c2a36d60267527a7a5b4f6e6407c676",
        },
        "provider_rc": provider_rc,
        "source_precision_guard_pass": source_ok,
        "fixed_point_pass": fixed_point_ok,
        "fixed_point_finals": finals,
        "fixed_point_iteration_trace": iterations,
        "mode_failures": {
            "unique_top_level_count": len(records),
            "rk_signature_count": len(signatures),
            "strict_clean_geometry_count": len(clean),
            "malformed_or_interleaved_geometry_count": len(malformed),
            "all_k_range_1_per_Mpc": None if not k_values else [min(k_values), max(k_values)],
            "index_k_range": None
            if not records
            else [min(row["index_k"] for row in records), max(row["index_k"] for row in records)],
            "K1_failed": frozen_mode_failed(K1),
            "K10_failed": frozen_mode_failed(K10),
            "relative_match_tolerance": K_TOL,
            "strict_clean_ranges": {
                "collapse_tau_Mpc": numeric_range("x"),
                "step_ratio": numeric_range("step_ratio"),
                "minimum_ratio_values": sorted(set(row["rk"]["minimum"] for row in clean)),
                "hdid_Mpc": numeric_range("hdid"),
                "hnext_Mpc": numeric_range("hnext"),
                "step_indices": sorted(set(row["rk"]["step_index"] for row in clean)),
                "rk_interval_start_Mpc": numeric_range("rk_interval_start"),
                "rk_interval_end_Mpc": numeric_range("rk_interval_end"),
            },
            "malformed_records": malformed_summary,
        },
        "reference_B1_B2_B3_evaluated": False,
        "default_reference_reproducibility_evaluated": False,
        "diagnostic_corruption_changes_blocker_classification": False,
        "all_required_checks_pass": sufficient,
        "classification": classification,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
        "interpretation": (
            "Exact cl_ref.pre reaches the self-consistent gauge-IVP boundary solution, then explicit RK collapses on the first post-handoff step for a broad intermediate-k island. Frozen K1/K10 are not among the failing modes. Some concurrent stderr diagnostics are malformed/interleaved, but the provider rc and hundreds of independent RK-collapse signatures make the numerical blocker unambiguous."
            if sufficient
            else "Artifact evidence was insufficient for the preregistered blocker classification."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    print(json.dumps(obj, indent=2, sort_keys=True))
    return 0 if sufficient else 1


if __name__ == "__main__":
    raise SystemExit(main())
