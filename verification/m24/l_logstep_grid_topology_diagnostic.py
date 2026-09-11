#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

PROFILE_CASES = ["profile_ref", "profile_zero", "profile_a18k", "profile_a6k", "profile_a1p8k"]
CONTROL_CASES = ["default_ref", "default_zero", "default_a18k", "default_a6k", "default_a1p8k"]


def parse_grid(path: Path):
    lines = [x.strip() for x in path.read_text().splitlines() if x.strip()]
    if not lines or not lines[0].startswith("l_size_max\t"):
        raise ValueError(f"bad grid header: {path}")
    declared = int(lines[0].split("\t", 1)[1])
    vals = []
    for line in lines[1:]:
        i, ell = line.split("\t")
        if int(i) != len(vals):
            raise ValueError(f"non-contiguous grid index in {path}: {line}")
        vals.append(int(ell))
    if len(vals) != declared:
        raise ValueError(f"grid size mismatch in {path}: {len(vals)} != {declared}")
    digest = hashlib.sha256(",".join(map(str, vals)).encode()).hexdigest()
    return {"l_size_max": declared, "sha256": digest, "ells": vals}


def topology_delta(a, b):
    av, bv = a["ells"], b["ells"]
    n = min(len(av), len(bv))
    first = next((i for i in range(n) if av[i] != bv[i]), None)
    if first is None and len(av) != len(bv):
        first = n
    return {
        "grid_changed": a["sha256"] != b["sha256"],
        "symmetric_difference_size": len(set(av) ^ set(bv)),
        "first_differing_index": first,
        "first_a": None if first is None or first >= len(av) else av[first],
        "first_b": None if first is None or first >= len(bv) else bv[first],
        "changed_tail_nodes": 0 if first is None else max(len(av), len(bv)) - first,
        "size_a": len(av),
        "size_b": len(bv),
    }


def point(args):
    raw = json.loads(Path(args.raw).read_text())
    status = json.loads(Path(args.status).read_text())
    grids, missing = {}, []
    for case in PROFILE_CASES + CONTROL_CASES:
        p = Path(args.grids) / f"{case}.tsv"
        try:
            grids[case] = parse_grid(p)
        except Exception as exc:
            missing.append({"case": case, "error": str(exc)})
    failed_cases = {k: v for k, v in status.items() if int(v) != 0}
    profile_grids = {c: grids[c] for c in PROFILE_CASES if c in grids}
    control_grids = {c: grids[c] for c in CONTROL_CASES if c in grids}
    profile_digests = [g["sha256"] for g in profile_grids.values()]
    profile_uniform = len(profile_digests) == len(PROFILE_CASES) and len(set(profile_digests)) == 1
    out = {
        "schema": "KMDSB.M24.LLogstepGridTopology.Point.v1",
        "preregistration": "protocol/W04_M24_L_LOGSTEP_MULTIPOLE_GRID_TOPOLOGY_PREREGISTRATION_v0.1.md",
        "l_logstep": float(args.logstep),
        "parent_classification": raw.get("classification"),
        "Emax": raw.get("profile", {}).get("Emax"),
        "exact_identity_pass": raw.get("profile", {}).get("exact_identity_pass", False),
        "status": status,
        "failed_cases": failed_cases,
        "missing_grids": missing,
        "profile_grid_uniform_across_cases": profile_uniform,
        "profile_grid": profile_grids.get("profile_ref"),
        "profile_grids": profile_grids,
        "control_grids": control_grids,
        "provider_blocked": bool(failed_cases or missing or "profile_ref" not in profile_grids),
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def aggregate(args):
    points = [json.loads(p.read_text()) for p in Path(args.collected).glob("*/result.json")]
    points.sort(key=lambda x: x["l_logstep"])
    blocked = len(points) != 6 or any(p.get("provider_blocked") for p in points)
    adjacency, any_grid_change, aligned = [], False, False
    for a, b in zip(points[:-1], points[1:]):
        ea, eb = a.get("Emax"), b.get("Emax")
        ratio = None if ea is None or eb is None else max(ea, eb) / max(min(ea, eb), 1e-300)
        case_deltas = {}
        for case in PROFILE_CASES:
            ga = a.get("profile_grids", {}).get(case)
            gb = b.get("profile_grids", {}).get(case)
            if ga is not None and gb is not None:
                case_deltas[case] = topology_delta(ga, gb)
        changed = any(d["grid_changed"] for d in case_deltas.values()) if case_deltas else None
        if changed:
            any_grid_change = True
        if ratio is not None and ratio >= 5 and changed and a.get("exact_identity_pass") and b.get("exact_identity_pass"):
            aligned = True
        ref_delta = case_deltas.get("profile_ref", {})
        adjacency.append({
            "from": a["l_logstep"],
            "to": b["l_logstep"],
            "cmb_jump_ratio": ratio,
            "grid_changed": changed,
            "profile_ref_delta": ref_delta,
            "profile_case_deltas": case_deltas,
        })
    endpoint_expected = {1.1175: 0.6805779364469253, 1.12: 62.6449744969262}
    endpoint_reproduction = {}
    for x, expected in endpoint_expected.items():
        p = next((q for q in points if abs(q["l_logstep"] - x) < 1e-12), None)
        actual = None if p is None else p.get("Emax")
        rel = None if actual is None else abs(actual - expected) / max(abs(expected), 1e-300)
        endpoint_reproduction[str(x)] = {
            "expected_Emax": expected,
            "actual_Emax": actual,
            "relative_error": rel,
            "pass_1e-8": rel is not None and rel <= 1e-8,
        }
    instrumentation_reproduction_pass = all(v["pass_1e-8"] for v in endpoint_reproduction.values())
    if blocked:
        classification = "M24_L_LOGSTEP_TOPOLOGY_PROVIDER_BLOCKED"
    elif aligned:
        classification = "M24_L_LOGSTEP_CMB_JUMP_ALIGNED_WITH_GRID_TOPOLOGY_CHANGE"
    elif any_grid_change:
        classification = "M24_L_LOGSTEP_GRID_CHANGES_WITHOUT_ALIGNED_CMB_JUMP"
    else:
        classification = "M24_L_LOGSTEP_GRID_TOPOLOGY_INVARIANT_ACROSS_BRACKET"
    out = {
        "schema": "KMDSB.M24.LLogstepGridTopology.Summary.v1",
        "preregistration": "protocol/W04_M24_L_LOGSTEP_MULTIPOLE_GRID_TOPOLOGY_PREREGISTRATION_v0.1.md",
        "points": points,
        "adjacent_topology_deltas": adjacency,
        "aligned_discontinuity": aligned,
        "any_grid_change": any_grid_change,
        "endpoint_reproduction": endpoint_reproduction,
        "instrumentation_reproduction_pass": instrumentation_reproduction_pass,
        "classification": classification,
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("point")
    p.add_argument("--raw", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--grids", required=True)
    p.add_argument("--logstep", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=point)
    a = sub.add_parser("aggregate")
    a.add_argument("--collected", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=aggregate)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
