#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import re
from decimal import Decimal

PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PROTOCOL = "protocol/W04_M21_AUTO_QGRID_IDENTITY_AUDIT_ARTIFACT_RECOVERY_v0.2.md"
SOURCE_RUN = 34864061202
SOURCE_HEAD = "261a0e38a3c3dedacf006bf3195b11495705e1ab"
EXPECTED_OMEGA = {
    "f2": Decimal("0.0012"),
    "f3": Decimal("0.00036"),
    "f4": Decimal("0.00012"),
    "f3_manual": Decimal("0.00036"),
}
SOURCE_ARTIFACTS = {
    "f2": {"id": 10357080247, "digest": "sha256:1f2e464e1a68aec33ec3a0a9b8a19baeea82c69a0caf2e7eeb9d968e3862d674"},
    "f3": {"id": 10356755518, "digest": "sha256:10cf196b702f2566d8dddd6f7ac5dafdb177597ce4ceecd5c6ac070bd676b5e5"},
    "f4": {"id": 10355554458, "digest": "sha256:6aedea1ef11d8c5146e14d3532dacc4f388d47f9f9949b3b9bb624c6ab5f9b89"},
    "f3_manual": {"id": 10357017735, "digest": "sha256:661c454eef830e0d72bc8619fd2df466bedb16f4854e2dd8e418beed12cbcf5b"},
}
ORIGINAL_AGGREGATE = {
    "id": 10357151669,
    "digest": "sha256:0e17865f9963cccd27544170518a343cc47e3c2c25dbeffa353009e34d9b09d5",
    "classification": "M21_AUTO_QGRID_AUDIT_BLOCKED",
}

BEGIN_RE = re.compile(r"^KMDSB_QGRID_BEGIN species=(\d+) strategy=(\d+) qsize=(\d+) deg=([^ ]+) factor=([^\s]+)$", re.M)
POINT_RE = re.compile(r"^KMDSB_QGRID_POINT species=(\d+) i=(\d+) q=([^ ]+) w=([^\s]+)$", re.M)
END_RE = re.compile(r"^KMDSB_QGRID_END species=(\d+)$", re.M)


def unique_file(root: pathlib.Path, artifact_name: str, filename: str) -> pathlib.Path:
    preferred = root / artifact_name / filename
    if preferred.is_file():
        return preferred
    matches = list(root.glob(f"**/{artifact_name}/{filename}")) + list(root.glob(f"**/{filename}"))
    matches = list(dict.fromkeys(p.resolve() for p in matches if p.is_file()))
    if len(matches) != 1:
        raise RuntimeError(f"{artifact_name}/{filename}: expected exactly one file, found {len(matches)}")
    return pathlib.Path(matches[0])


def ini_value(path: pathlib.Path, key: str) -> str | None:
    vals = []
    for raw in path.read_text(errors="replace").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == key:
            vals.append(v.strip())
    if not vals:
        return None
    if len(vals) != 1:
        raise RuntimeError(f"{path}: {key} appears {len(vals)} times")
    return vals[0]


def instrumentation_ok(obj: dict) -> bool:
    return bool(
        obj.get("schema") == "KMDSB.W04.M21.QGridInstrumentation.v0.2"
        and obj.get("changed_file") == "source/background.c"
        and obj.get("insertions") == 1
        and obj.get("output_only") is True
        and obj.get("changes_arrays") is False
        and obj.get("changes_equations") is False
        and obj.get("changes_inputs") is False
        and obj.get("changes_tolerances") is False
        and obj.get("factor_initialized_before_print") is True
    )


def parse_grid(log_path: pathlib.Path) -> dict:
    text = log_path.read_text(errors="replace")
    begins = BEGIN_RE.findall(text)
    ends = END_RE.findall(text)
    if len(begins) != 1 or len(ends) != 1:
        raise RuntimeError(f"{log_path}: begin={len(begins)} end={len(ends)}")
    sp, strategy, qsize, deg, factor = begins[0]
    if int(sp) != 0 or int(ends[0]) != 0:
        raise RuntimeError(f"{log_path}: unexpected species")
    n = int(qsize)
    pts = POINT_RE.findall(text)
    if len(pts) != n:
        raise RuntimeError(f"{log_path}: points={len(pts)} qsize={n}")
    rows = sorted(((int(s), int(i), float(q), float(w)) for s, i, q, w in pts), key=lambda x: x[1])
    if [r[1] for r in rows] != list(range(n)) or any(r[0] != 0 for r in rows):
        raise RuntimeError(f"{log_path}: invalid point indexing/species")
    q = [r[2] for r in rows]
    w = [r[3] for r in rows]
    finite = q + w + [float(deg), float(factor)]
    if not all(math.isfinite(x) for x in finite):
        raise RuntimeError(f"{log_path}: nonfinite q-grid record")
    payload = {"strategy": int(strategy), "q_size": n, "q": q, "w": w}
    canon = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {
        **payload,
        "deg_ncdm_at_print": float(deg),
        "factor_ncdm_at_print": float(factor),
        "qgrid_sha256": hashlib.sha256(canon).hexdigest(),
    }


def parse_lane(root: pathlib.Path, lane: str) -> dict:
    artifact_name = f"m21-qgrid-{lane}"
    log = unique_file(root, artifact_name, f"run_{lane}.log")
    ini = unique_file(root, artifact_name, "lane.ini")
    rc_path = unique_file(root, artifact_name, "provider_rc.txt")
    manifest_path = unique_file(root, artifact_name, "instrumentation_manifest.json")

    grid = parse_grid(log)
    rc = int(rc_path.read_text().strip())
    manifest = json.loads(manifest_path.read_text())
    omega_raw = ini_value(ini, "omega_ncdm")
    if omega_raw is None:
        raise RuntimeError(f"{lane}: missing omega_ncdm")
    omega = Decimal(omega_raw)
    expected = EXPECTED_OMEGA[lane]
    omega_ok = omega == expected
    inst_ok = instrumentation_ok(manifest)

    manual_controls = None
    if lane == "f3_manual":
        manual_controls = {
            "ncdm_quadrature_strategy": ini_value(ini, "ncdm_quadrature_strategy"),
            "ncdm_N_momentum_bins": ini_value(ini, "ncdm_N_momentum_bins"),
            "ncdm_maximum_q": ini_value(ini, "ncdm_maximum_q"),
        }
        controls_ok = (
            manual_controls["ncdm_quadrature_strategy"] == "3"
            and Decimal(manual_controls["ncdm_N_momentum_bins"] or "NaN") == Decimal("150")
            and Decimal(manual_controls["ncdm_maximum_q"] or "NaN") == Decimal("15")
        )
        valid = bool(inst_ok and omega_ok and controls_ok)
        validity_rule = "complete_qgrid_record_plus_frozen_manual_controls; provider_rc_is_provenance_only_after_record"
    else:
        controls_ok = True
        valid = bool(inst_ok and omega_ok and rc == 0)
        validity_rule = "complete_qgrid_record_plus_output_only_instrumentation_plus_provider_rc_zero"

    return {
        "lane": lane,
        "provider": f"lesgourg/class_public@{PIN}",
        "source_artifact": SOURCE_ARTIFACTS[lane],
        "provider_rc": rc,
        "omega_ncdm": str(omega),
        "expected_omega_ncdm": str(expected),
        "omega_input_matches_frozen_case": omega_ok,
        "instrumentation_valid": inst_ok,
        "manual_controls": manual_controls,
        "manual_controls_valid": controls_ok,
        "valid_for_v02_recovery": valid,
        "validity_rule": validity_rule,
        **grid,
    }


def recover(root: pathlib.Path, out: pathlib.Path) -> dict:
    lanes = {lane: parse_lane(root, lane) for lane in ("f2", "f3", "f4", "f3_manual")}
    phys = [lanes[x] for x in ("f2", "f3", "f4")]
    physical_valid = all(x["valid_for_v02_recovery"] for x in phys)
    manual_valid = lanes["f3_manual"]["valid_for_v02_recovery"]
    distinct_frozen_inputs = (
        [Decimal(x["omega_ncdm"]) for x in phys] == [EXPECTED_OMEGA[x] for x in ("f2", "f3", "f4")]
        and len({x["omega_ncdm"] for x in phys}) == 3
    )
    physical_grids_identical = all(
        (x["strategy"], x["q_size"], x["q"], x["w"])
        == (phys[0]["strategy"], phys[0]["q_size"], phys[0]["q"], phys[0]["w"])
        for x in phys[1:]
    )
    negative_control_differs = lanes["f3_manual"]["qgrid_sha256"] != lanes["f3"]["qgrid_sha256"]

    common_ok = physical_valid and manual_valid and distinct_frozen_inputs and negative_control_differs
    if common_ok and physical_grids_identical:
        cls = "M21_AUTO_QGRID_IDENTICAL_ACROSS_FRACTIONS_RECOVERED"
    elif common_ok and not physical_grids_identical:
        cls = "M21_AUTO_QGRID_FRACTION_DEPENDENT_RECOVERED"
    else:
        cls = "M21_AUTO_QGRID_ARTIFACT_RECOVERY_BLOCKED"

    result = {
        "schema": "KMDSB.W04.M21.AutoQGridIdentityArtifactRecovery.v0.2",
        "date": "2026-09-14",
        "protocol": PROTOCOL,
        "provider": f"lesgourg/class_public@{PIN}",
        "source_run": SOURCE_RUN,
        "source_head": SOURCE_HEAD,
        "source_artifacts": SOURCE_ARTIFACTS,
        "original_v01_aggregate": ORIGINAL_AGGREGATE,
        "recovery_scope": "artifact_only_no_provider_execution",
        "lanes": lanes,
        "physical_lanes_valid": physical_valid,
        "manual_negative_control_valid_at_qgrid_boundary": manual_valid,
        "frozen_omega_inputs_exact_and_distinct": distinct_frozen_inputs,
        "physical_grids_exactly_identical": physical_grids_identical,
        "manual_negative_control_grid_differs": negative_control_differs,
        "classification": cls,
        "K1_promoted": False,
        "physical_falsification": False,
        "interpretation": (
            "The saved automatic perturbation q-grid is exactly identical across f_w=0.01, 0.003 and 0.001 while the immutable omega_ncdm inputs are distinct, and the saved manual-trapz negative control produces a different grid. Fraction-dependent automatic q-grid selection is therefore ruled out as the direct cause of the isolated f3 excursion. Common-grid quadrature error and later source/transfer/interpolation precision layers remain open."
            if cls == "M21_AUTO_QGRID_IDENTICAL_ACROSS_FRACTIONS_RECOVERED"
            else "Apply only the frozen v0.2 classification fields; no physical falsification is authorized."
        ),
    }
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "classification": cls,
        "physical_grids_exactly_identical": physical_grids_identical,
        "frozen_omega_inputs_exact_and_distinct": distinct_frozen_inputs,
        "manual_negative_control_grid_differs": negative_control_differs,
        "manual_provider_rc": lanes["f3_manual"]["provider_rc"],
    }, indent=2, sort_keys=True))
    if cls == "M21_AUTO_QGRID_ARTIFACT_RECOVERY_BLOCKED":
        raise SystemExit(1)
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("evidence", type=pathlib.Path)
    ap.add_argument("output", type=pathlib.Path)
    args = ap.parse_args()
    recover(args.evidence, args.output)


if __name__ == "__main__":
    main()
