#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

PROFILE_CASES = ["profile_ref", "profile_zero", "profile_a18k", "profile_a6k", "profile_a1p8k"]
EXPECTED = {"native_1195": 0.6244612907744809, "native_1200": 62.644974496926224}


def parse_grid(path: Path):
    lines = [x.strip() for x in path.read_text().splitlines() if x.strip()]
    if not lines or not lines[0].startswith("l_size_max\t"):
        raise ValueError(f"bad grid header: {path}")
    n = int(lines[0].split("\t", 1)[1])
    vals = []
    for line in lines[1:]:
        i, ell = line.split("\t")
        if int(i) != len(vals):
            raise ValueError(f"non-contiguous grid index in {path}: {line}")
        vals.append(int(ell))
    if len(vals) != n:
        raise ValueError(f"grid size mismatch: {len(vals)} != {n}")
    return {
        "l_size_max": n,
        "ells": vals,
        "sha256": hashlib.sha256(",".join(map(str, vals)).encode()).hexdigest(),
    }


def arm(args):
    raw = json.loads(Path(args.raw).read_text())
    status = json.loads(Path(args.status).read_text())
    failed = {k: int(v) for k, v in status.items() if int(v) != 0}
    actual, actual_errors = {}, []
    for c in PROFILE_CASES:
        try:
            actual[c] = parse_grid(Path(args.grids) / f"{c}.tsv")
        except Exception as exc:
            actual_errors.append({"case": c, "error": str(exc)})

    target = {}
    target_errors = []
    target_match = None
    if args.target != "none":
        for c in PROFILE_CASES:
            try:
                target[c] = parse_grid(Path(args.target_grids) / f"{c}.tsv")
            except Exception as exc:
                target_errors.append({"case": c, "error": str(exc)})
        target_match = (
            not target_errors
            and len(actual) == len(PROFILE_CASES)
            and all(
                actual[c]["sha256"] == target[c]["sha256"]
                and actual[c]["ells"] == target[c]["ells"]
                for c in PROFILE_CASES
            )
        )

    emax = raw.get("profile", {}).get("Emax")
    identity = bool(raw.get("profile", {}).get("exact_identity_pass", False))
    reproduction = None
    if args.arm in EXPECTED and emax is not None:
        exp = EXPECTED[args.arm]
        rel = abs(float(emax) - exp) / max(abs(exp), 1e-300)
        reproduction = {
            "expected_Emax": exp,
            "actual_Emax": float(emax),
            "relative_error": rel,
            "pass_1e-8": rel <= 1e-8,
        }

    integrity = (
        not failed
        and not actual_errors
        and identity
        and (target_match is not False)
        and not target_errors
        and (reproduction is None or reproduction["pass_1e-8"])
    )
    out = {
        "schema": "KMDSB.M24.CausalGridSwap.Arm.v1",
        "preregistration": "protocol/W04_M24_L_LOGSTEP_CAUSAL_GRID_SWAP_PREREGISTRATION_v0.1.md",
        "arm": args.arm,
        "l_logstep": float(args.logstep),
        "forced_target": args.target,
        "Emax": emax,
        "exact_identity_pass": identity,
        "status": status,
        "failed_cases": failed,
        "actual_profile_grids": actual,
        "actual_grid_errors": actual_errors,
        "target_grid_errors": target_errors,
        "forced_target_exact_match": target_match,
        "native_reproduction": reproduction,
        "integrity_pass": integrity,
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def aggregate(args):
    rows = [json.loads(p.read_text()) for p in Path(args.collected).glob("*/result.json")]
    by = {r["arm"]: r for r in rows}
    required = {"native_1195", "force_1200_on_1195", "native_1200", "force_1195_on_1200"}
    integrity = set(by) == required and all(by[a].get("integrity_pass") for a in required)
    metrics = {}
    induction_pass = rescue_pass = False
    if integrity:
        e1195 = float(by["native_1195"]["Emax"])
        e1200 = float(by["native_1200"]["Emax"])
        eind = float(by["force_1200_on_1195"]["Emax"])
        eresc = float(by["force_1195_on_1200"]["Emax"])
        induction_ratio = eind / max(e1195, 1e-300)
        rescue_ratio = e1200 / max(eresc, 1e-300)
        induction_pass = induction_ratio >= 10.0
        rescue_pass = rescue_ratio >= 10.0
        metrics = {
            "E1195": e1195,
            "E1200": e1200,
            "E1200grid_on_1195": eind,
            "E1195grid_on_1200": eresc,
            "induction_ratio": induction_ratio,
            "rescue_ratio": rescue_ratio,
            "induction_pass_ge10": induction_pass,
            "rescue_pass_ge10": rescue_pass,
            "forward_target_ratio": eind / max(e1200, 1e-300),
            "reverse_target_ratio": eresc / max(e1195, 1e-300),
        }

    if not integrity:
        classification = "M24_CAUSAL_GRID_SWAP_PROVIDER_OR_INSTRUMENTATION_BLOCKED"
    elif induction_pass and rescue_pass:
        classification = "M24_L_LOGSTEP_CMB_CATASTROPHE_CAUSALLY_TRANSFERS_WITH_MULTIPOLE_GRID"
    elif rescue_pass:
        classification = "M24_L_LOGSTEP_CMB_CATASTROPHE_GRID_NECESSARY_NOT_SUFFICIENT"
    elif induction_pass:
        classification = "M24_L_LOGSTEP_CMB_CATASTROPHE_GRID_SUFFICIENT_NOT_NECESSARY"
    else:
        classification = "M24_L_LOGSTEP_CMB_CATASTROPHE_NOT_CAUSALLY_ASSIGNED_TO_GRID_BY_SWAP"

    out = {
        "schema": "KMDSB.M24.CausalGridSwap.Summary.v1",
        "preregistration": "protocol/W04_M24_L_LOGSTEP_CAUSAL_GRID_SWAP_PREREGISTRATION_v0.1.md",
        "parent_topology_run_id": 34626787237,
        "arms": rows,
        "integrity_pass": integrity,
        "causal_metrics": metrics,
        "classification": classification,
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
        "interpretation": "Bidirectional grid intervention is numerical attribution only; no physical ETHOS falsification or K-gate promotion.",
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("arm")
    p.add_argument("--raw", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--grids", required=True)
    p.add_argument("--arm", required=True)
    p.add_argument("--logstep", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--target-grids", default=".")
    p.add_argument("--output", required=True)
    p.set_defaults(func=arm)
    a = sub.add_parser("aggregate")
    a.add_argument("--collected", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=aggregate)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
