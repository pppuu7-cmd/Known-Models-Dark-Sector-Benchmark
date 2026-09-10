#!/usr/bin/env python3
"""Harness/analyzer for preregistered KMDSB M19 AxiECAMB K0-K1 control.

Uses only the Python standard library so the provider workflow does not depend
on NumPy.  Preparation changes only frozen input keys; analysis never edits the
external source tree.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

PIN = "b7ca9ba80aca178da5003d864b8e20cb5905555b"
REQUIRED_SUFFIXES = ["scalCls.dat", "lensedCls.dat", "matterpower.dat", "transfer_out.dat"]
REFERENCE_TOL = 1.0e-10

CASES = {
    "r0f": {
        "output_root": "r0f",
        "m_ax": "1.e-27",
        "use_axfrac": "T",
        "omdah2": "0.1200",
        "axfrac": "0.0",
        "do_nonlinear": "0",
        "axion_isocurvature": "F",
        "movH_switch": "10",
        "accuracy_boost": "1",
    },
    "r0d": {
        "output_root": "r0d",
        "m_ax": "1.e-27",
        "use_axfrac": "F",
        "omch2": "0.1200",
        "omaxh2": "0.0",
        "do_nonlinear": "0",
        "axion_isocurvature": "F",
        "movH_switch": "10",
        "accuracy_boost": "1",
    },
    "p1": {
        "output_root": "p1",
        "m_ax": "1.e-27",
        "use_axfrac": "T",
        "omdah2": "0.1200",
        "axfrac": "0.10",
        "do_nonlinear": "0",
        "axion_isocurvature": "F",
        "movH_switch": "10",
        "accuracy_boost": "1",
    },
}


def replace_key(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^(\s*{re.escape(key)}\s*=).*?$")
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one active key {key!r}, found {len(matches)}")
    return pattern.sub(lambda m: f"{m.group(1)} {value}", text, count=1)


def prepare(base: Path, outdir: Path) -> None:
    original = base.read_text()
    outdir.mkdir(parents=True, exist_ok=True)
    manifest = {"provider_pin": PIN, "cases": {}}
    for name, edits in CASES.items():
        text = original
        for key, value in edits.items():
            text = replace_key(text, key, value)
        path = outdir / f"{name}.ini"
        path.write_text(text)
        manifest["cases"][name] = {"ini": str(path), "edits": edits}
    (outdir / "case_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def parse_numeric_file(path: Path) -> List[List[float]]:
    rows: List[List[float]] = []
    for line_no, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        parts = s.replace("D", "E").replace("d", "e").split()
        try:
            row = [float(x) for x in parts]
        except ValueError as exc:
            raise RuntimeError(f"{path}:{line_no}: non-numeric data: {s[:120]}") from exc
        if not row:
            continue
        if not all(math.isfinite(x) for x in row):
            raise RuntimeError(f"{path}:{line_no}: NaN/Inf encountered")
        rows.append(row)
    if not rows:
        raise RuntimeError(f"{path}: no numeric rows")
    width = len(rows[0])
    if width == 0 or any(len(r) != width for r in rows):
        raise RuntimeError(f"{path}: ragged numeric table")
    return rows


def compare_tables(a: List[List[float]], b: List[List[float]]) -> dict:
    if len(a) != len(b):
        return {"shape_match": False, "rows_a": len(a), "rows_b": len(b), "pass": False}
    if not a or not b or len(a[0]) != len(b[0]):
        return {
            "shape_match": False,
            "rows_a": len(a),
            "rows_b": len(b),
            "cols_a": len(a[0]) if a else 0,
            "cols_b": len(b[0]) if b else 0,
            "pass": False,
        }
    n = 0
    sumsq = 0.0
    max_abs = 0.0
    max_scale = 1.0e-30
    for ra, rb in zip(a, b):
        if len(ra) != len(rb):
            return {"shape_match": False, "pass": False}
        for xa, xb in zip(ra, rb):
            d = abs(xa - xb)
            max_abs = max(max_abs, d)
            max_scale = max(max_scale, abs(xa), abs(xb))
            sumsq += d * d
            n += 1
    dinf = max_abs / max_scale
    rms_norm = math.sqrt(sumsq / max(n, 1)) / max_scale
    return {
        "shape_match": True,
        "rows": len(a),
        "cols": len(a[0]),
        "entries": n,
        "max_abs_difference": max_abs,
        "normalization_scale": max_scale,
        "D_inf": dinf,
        "rms_normalized": rms_norm,
        "tolerance": REFERENCE_TOL,
        "pass": dinf <= REFERENCE_TOL,
    }


def case_output_path(workdir: Path, case: str, suffix: str) -> Path:
    return workdir / f"{case}_{suffix}"


def analyze(workdir: Path, status_path: Path, out_path: Path) -> None:
    status = json.loads(status_path.read_text())
    build_exit = int(status.get("build_exit", 999))
    exits = {k: status.get(f"{k}_exit") for k in CASES}

    result = {
        "schema": "KMDSB.M19.AxiECAMB.K0K1.v1",
        "provider": "Ra-yne/AxiECAMB",
        "provider_pin": PIN,
        "preregistration": "protocol/W04_M19_AXIECAMB_K0_K1_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md",
        "scope": "linear scalar provider execution and zero-ULA reference only",
        "build_exit": build_exit,
        "case_exits": exits,
        "required_suffixes": REQUIRED_SUFFIXES,
        "reference_tolerance": REFERENCE_TOL,
        "cases": {},
        "reference_comparisons": {},
        "scientific_promotion": {"K0": False, "K1": False, "K2_K9": False},
    }

    if build_exit != 0:
        result["classification"] = "M19_AXIECAMB_BLOCKED_BUILD"
        out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return

    output_contract = True
    for case in CASES:
        c = {"exit": exits[case], "outputs": {}}
        if exits[case] != 0:
            output_contract = False
        for suffix in REQUIRED_SUFFIXES:
            p = case_output_path(workdir, case, suffix)
            info = {"path": str(p), "exists": p.exists(), "size": p.stat().st_size if p.exists() else 0}
            if p.exists() and p.stat().st_size > 0:
                try:
                    rows = parse_numeric_file(p)
                    info.update({"parse_finite": True, "rows": len(rows), "cols": len(rows[0])})
                except Exception as exc:
                    info.update({"parse_finite": False, "error": str(exc)})
                    output_contract = False
            else:
                info["parse_finite"] = False
                output_contract = False
            c["outputs"][suffix] = info
        result["cases"][case] = c

    zero_exec_ok = exits["r0f"] == 0 and exits["r0d"] == 0
    finite_exec_ok = exits["p1"] == 0
    identity_pass = True

    if zero_exec_ok:
        for suffix in REQUIRED_SUFFIXES:
            pa = case_output_path(workdir, "r0f", suffix)
            pb = case_output_path(workdir, "r0d", suffix)
            if not (pa.exists() and pb.exists() and pa.stat().st_size and pb.stat().st_size):
                result["reference_comparisons"][suffix] = {"pass": False, "error": "missing/empty output"}
                identity_pass = False
                continue
            try:
                cmp = compare_tables(parse_numeric_file(pa), parse_numeric_file(pb))
            except Exception as exc:
                cmp = {"pass": False, "error": str(exc)}
            result["reference_comparisons"][suffix] = cmp
            identity_pass = identity_pass and bool(cmp.get("pass", False))
    else:
        identity_pass = False

    if not zero_exec_ok:
        classification = "M19_AXIECAMB_BLOCKED_ZERO_REFERENCE_EXECUTION"
    elif not finite_exec_ok:
        classification = "M19_AXIECAMB_BLOCKED_FINITE_PROVIDER_CONTROL"
    elif not output_contract:
        classification = "M19_AXIECAMB_OUTPUT_CONTRACT_FAIL"
    elif not identity_pass:
        classification = "M19_AXIECAMB_K1_REFERENCE_IDENTITY_FAIL"
    else:
        classification = "M19_AXIECAMB_K0_K1_PASS_WITH_SCOPE"
        result["scientific_promotion"]["K0"] = True
        result["scientific_promotion"]["K1"] = True

    result["gates"] = {
        "build_pass": build_exit == 0,
        "zero_reference_execution_pass": zero_exec_ok,
        "finite_provider_control_pass": finite_exec_ok,
        "output_contract_pass": output_contract,
        "reference_identity_pass": identity_pass,
    }
    result["classification"] = classification
    result["physical_falsification"] = False
    result["next_if_pass"] = "preregister M19 K2-K5 finite fraction/mass geometry and thermal-WDM suppression attack"
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("base", type=Path)
    p.add_argument("outdir", type=Path)
    a = sub.add_parser("analyze")
    a.add_argument("workdir", type=Path)
    a.add_argument("status", type=Path)
    a.add_argument("output", type=Path)
    ns = ap.parse_args()
    if ns.cmd == "prepare":
        prepare(ns.base, ns.outdir)
    else:
        analyze(ns.workdir, ns.status, ns.output)
