#!/usr/bin/env python3
"""Parse K3D2-E reference-RK component-attribution diagnostics robustly."""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
from pathlib import Path

BASE = re.compile(
    r"KMDSB_MODE_FAIL index_md=(\d+) index_ic=(\d+) index_k=(\d+) k=([^ ]+) "
    r"interval_start=([^ ]+) evolver_start=([^ ]+) interval_end=([^ ]+) "
    r"pt_size=(\d+) eta_i=(-?\d+) dg_i=(-?\d+) tg_i=(-?\d+) sg_i=(-?\d+) "
    r"l3g_i=(-?\d+) lmax_g=(-?\d+) pol0g_i=(-?\d+) lmax_pol_g=(-?\d+) "
    r"db_i=(-?\d+) tb_i=(-?\d+) dcdm_i=(-?\d+) tcdm_i=(-?\d+) "
    r"dur_i=(-?\d+) tur_i=(-?\d+) sur_i=(-?\d+) l3ur_i=(-?\d+) lmax_ur=(-?\d+) "
    r"qcf_i=(-?\d+) qcfp_i=(-?\d+) qpf_i=(-?\d+) qpfp_i=(-?\d+) error=(.*)"
)
FINAL = re.compile(
    r"KMDSB_GAUGE_IVP_FIXED_FINAL\s+converged=(\d+)\s+iterations=(\d+) "
    r"max=([^ ]+)\s+tol=([^ \n]+)"
)


def fval(raw):
    try:
        value = float(raw)
        return value if math.isfinite(value) else None
    except Exception:
        return None


def parse_rk(error: str):
    pos = error.find("KMDSB_RK_COLLAPSE ")
    if pos < 0:
        return None
    text = error[pos + len("KMDSB_RK_COLLAPSE ") :]
    names = (
        "attempts",
        "first_max_index",
        "first_raw_ratio",
        "first_errmax",
        "final_max_index",
        "final_raw_ratio",
        "final_errmax",
        "final_yerr",
        "final_yscal",
        "final_y",
        "final_start_dydx",
        "step_index",
        "step_ratio",
        "minimum",
        "hdid",
        "hnext",
        "x",
    )
    out = {"raw_fragment": text[-700:]}
    for name in names:
        match = re.search(r"(?:^| )" + re.escape(name) + r"=([^ ]+)", text)
        if not match:
            out[name] = None
            continue
        raw = match.group(1)
        out[name + "_raw"] = raw
        if name in ("attempts", "first_max_index", "final_max_index", "step_index"):
            try:
                out[name] = int(raw)
            except Exception:
                out[name] = None
        else:
            out[name] = fval(raw)
    required = names
    out["strict_clean"] = all(out.get(name) is not None for name in required)
    return out


def classify_index(index: int, m: dict) -> str:
    if index == m["qcf_i"]:
        return "qcf_field"
    if index == m["qcfp_i"]:
        return "qcf_field_prime"
    if index == m["qpf_i"]:
        return "qpf_field"
    if index == m["qpfp_i"]:
        return "qpf_field_prime"
    if index == m["eta_i"]:
        return "metric_eta"
    exact = {
        m["dg_i"]: "photon_delta",
        m["tg_i"]: "photon_theta",
        m["sg_i"]: "photon_shear",
        m["db_i"]: "baryon_delta",
        m["tb_i"]: "baryon_theta",
        m["dcdm_i"]: "cdm_delta",
        m["tcdm_i"]: "cdm_theta",
        m["dur_i"]: "ur_delta",
        m["tur_i"]: "ur_theta",
        m["sur_i"]: "ur_shear",
    }
    if index in exact:
        return exact[index]
    if m["l3g_i"] >= 0 and m["lmax_g"] >= 3:
        if m["l3g_i"] <= index <= m["l3g_i"] + (m["lmax_g"] - 3):
            return "photon_temperature_hierarchy_l3plus"
    if m["pol0g_i"] >= 0 and m["lmax_pol_g"] >= 0:
        if m["pol0g_i"] <= index <= m["pol0g_i"] + m["lmax_pol_g"]:
            return "photon_polarization_hierarchy"
    if m["l3ur_i"] >= 0 and m["lmax_ur"] >= 3:
        if m["l3ur_i"] <= index <= m["l3ur_i"] + (m["lmax_ur"] - 3):
            return "ur_hierarchy_l3plus"
    return "other_or_dynamic_hierarchy"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", type=Path, required=True)
    ap.add_argument("--source-guard", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    rc = int((args.result / "provider_rc.txt").read_text().strip())
    text = (
        (args.result / "stderr.txt").read_text(errors="replace")
        + "\n"
        + (args.result / "stdout.txt").read_text(errors="replace")
    )
    source_guard = json.loads(args.source_guard.read_text())
    source_ok = bool(source_guard.get("all_required_checks_pass"))

    finals = []
    for match in FINAL.finditer(text):
        finals.append(
            {
                "converged": int(match.group(1)),
                "iterations": int(match.group(2)),
                "max": fval(match.group(3)),
                "tol": fval(match.group(4)),
            }
        )
    fixed_ok = bool(finals) and all(
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
        names = (
            "pt_size",
            "eta_i",
            "dg_i",
            "tg_i",
            "sg_i",
            "l3g_i",
            "lmax_g",
            "pol0g_i",
            "lmax_pol_g",
            "db_i",
            "tb_i",
            "dcdm_i",
            "tcdm_i",
            "dur_i",
            "tur_i",
            "sur_i",
            "l3ur_i",
            "lmax_ur",
            "qcf_i",
            "qcfp_i",
            "qpf_i",
            "qpfp_i",
        )
        values = [int(match.group(i)) for i in range(8, 30)]
        mapping = dict(zip(names, values))
        rk = parse_rk(match.group(30))
        row = {
            "index_k": key[2],
            "k": fval(match.group(4)),
            "mapping": mapping,
            "rk": rk,
        }
        if rk and rk.get("strict_clean"):
            row["first_component"] = classify_index(rk["first_max_index"], mapping)
            row["final_component"] = classify_index(rk["final_max_index"], mapping)
            row["component_changed"] = rk["first_max_index"] != rk["final_max_index"]
        records.append(row)

    clean = [row for row in records if row.get("rk") and row["rk"].get("strict_clean")]
    first_counts = collections.Counter(row["first_component"] for row in clean)
    final_counts = collections.Counter(row["final_component"] for row in clean)
    first_index_counts = collections.Counter(str(row["rk"]["first_max_index"]) for row in clean)
    final_index_counts = collections.Counter(str(row["rk"]["final_max_index"]) for row in clean)

    def rng(name):
        values = [row["rk"][name] for row in clean]
        return None if not values else [min(values), max(values)]

    qfield_labels = {"qcf_field", "qcf_field_prime", "qpf_field", "qpf_field_prime"}
    qfield_first = sum(1 for row in clean if row["first_component"] in qfield_labels)
    qfield_final = sum(1 for row in clean if row["final_component"] in qfield_labels)
    changed = sum(1 for row in clean if row["component_changed"])
    sufficient = source_ok and rc != 0 and fixed_ok and len(clean) >= 100
    classification = (
        "M13B_K3D2E_REFERENCE_RK_ERROR_COMPONENTS_LOCALIZED"
        if sufficient
        else (
            "M13B_K3D2E_REFERENCE_DIAGNOSTIC_EXECUTION_CHANGED_UNEXPECTEDLY"
            if source_ok and rc == 0
            else "M13B_K3D2E_REFERENCE_RK_COMPONENT_AUDIT_IMPLEMENTATION_BLOCKED"
        )
    )
    obj = {
        "schema": "KMDSB.W03.M13b.K3D2ERKErrorComponentAuditResult.v0.1",
        "provider_rc": rc,
        "source_guard_pass": source_ok,
        "fixed_point_pass": fixed_ok,
        "fixed_point_finals": finals,
        "unique_mode_failure_records": len(records),
        "strict_clean_component_records": len(clean),
        "malformed_or_unparseable_component_records": len(records) - len(clean),
        "first_attempt_component_distribution": dict(first_counts.most_common()),
        "final_accepted_component_distribution": dict(final_counts.most_common()),
        "first_attempt_index_distribution": dict(first_index_counts.most_common()),
        "final_accepted_index_distribution": dict(final_index_counts.most_common()),
        "qfield_dominance": {
            "first_attempt_count": qfield_first,
            "first_attempt_fraction": qfield_first / len(clean) if clean else None,
            "final_attempt_count": qfield_final,
            "final_attempt_fraction": qfield_final / len(clean) if clean else None,
        },
        "component_changed_during_shrinkage": {
            "count": changed,
            "fraction": changed / len(clean) if clean else None,
        },
        "rk_error_control_ranges": {
            "attempt_count": rng("attempts"),
            "first_raw_ratio": rng("first_raw_ratio"),
            "first_normalized_errmax": rng("first_errmax"),
            "final_raw_ratio": rng("final_raw_ratio"),
            "final_normalized_errmax": rng("final_errmax"),
            "step_ratio": rng("step_ratio"),
            "minimum_ratio": rng("minimum"),
            "hdid_Mpc": rng("hdid"),
            "hnext_Mpc": rng("hnext"),
        },
        "records": clean,
        "reference_B1_B2_B3_evaluated": False,
        "default_reference_reproducibility_evaluated": False,
        "all_required_checks_pass": sufficient,
        "classification": classification,
        "K3_state_ceiling": "PARTIAL",
        "K4_promoted": False,
        "K5_promoted": False,
        "physical_falsification": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "classification": classification,
        "provider_rc": rc,
        "fixed_point_pass": fixed_ok,
        "unique_mode_failure_records": len(records),
        "strict_clean_component_records": len(clean),
        "first_attempt_component_distribution": dict(first_counts.most_common()),
        "final_accepted_component_distribution": dict(final_counts.most_common()),
        "qfield_dominance": obj["qfield_dominance"],
        "component_changed_during_shrinkage": obj["component_changed_during_shrinkage"],
        "rk_error_control_ranges": obj["rk_error_control_ranges"],
    }, indent=2, sort_keys=True))
    return 0 if sufficient else 1


if __name__ == "__main__":
    raise SystemExit(main())
