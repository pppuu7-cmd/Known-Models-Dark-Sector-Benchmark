#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import numpy as np

BANDS = [(2, 30), (31, 500), (501, 1500), (1501, 2500)]


def load_cls(path):
    x = np.loadtxt(path)
    return {"ell": x[:, 0].astype(int), "TT": x[:, 1], "EE": x[:, 2], "TE": x[:, 3]}


def fisher_snr(ref, case):
    ell = ref["ell"]
    if not np.array_equal(ell, case["ell"]):
        raise ValueError("ell grids differ")
    mask = (ell >= 2) & (ell <= 2500)
    ell = ell[mask]
    totals = {f"{a}-{b}": 0.0 for a, b in BANDS}
    total = 0.0
    nonpositive = 0
    nonfinite = 0
    ill_conditioned = 0
    used = 0
    for idx, l in zip(np.where(mask)[0], ell):
        C = np.array([[ref["TT"][idx], ref["TE"][idx]], [ref["TE"][idx], ref["EE"][idx]]], dtype=float)
        D = np.array([[case["TT"][idx]-ref["TT"][idx], case["TE"][idx]-ref["TE"][idx]], [case["TE"][idx]-ref["TE"][idx], case["EE"][idx]-ref["EE"][idx]]], dtype=float)
        if not np.all(np.isfinite(C)) or not np.all(np.isfinite(D)):
            nonfinite += 1
            continue
        ev = np.linalg.eigvalsh(C)
        if ev[-1] <= 0 or ev[0] <= 0:
            nonpositive += 1
            continue
        if ev[-1] / ev[0] > 1e12:
            ill_conditioned += 1
        inv = np.linalg.pinv(C, rcond=1e-12, hermitian=True)
        A = inv @ D
        term = (2.0*l + 1.0) * 0.5 * float(np.trace(A @ A))
        if not math.isfinite(term):
            nonfinite += 1
            continue
        term = max(term, 0.0)
        total += term
        for a, b in BANDS:
            if a <= l <= b:
                totals[f"{a}-{b}"] += term
                break
        used += 1
    requested = int(np.sum(mask))
    bad_fraction = (nonpositive + nonfinite) / max(requested, 1)
    return {
        "snr": math.sqrt(total),
        "snr2": total,
        "band_snr": {k: math.sqrt(v) for k, v in totals.items()},
        "multipoles_requested": requested,
        "multipoles_used": used,
        "nonpositive_multipoles": nonpositive,
        "nonfinite_multipoles": nonfinite,
        "ill_conditioned_gt_1e12": ill_conditioned,
        "bad_fraction": bad_fraction,
        "numerically_valid": bad_fraction <= 0.05,
    }


def tier(snr):
    if snr < 1.0:
        return "BELOW_IDEAL_CV_1SIGMA"
    if snr < 5.0:
        return "IDEAL_CV_MARGINAL_1_TO_5SIGMA"
    return "IDEAL_CV_DETECTABLE_GE5SIGMA"


def five_sigma_bracket(fracs, snrs):
    pairs = sorted(zip(fracs, snrs))
    if all(s >= 5 for _, s in pairs):
        return {"type": "upper_bound", "threshold_fraction_lt_or_equal": pairs[0][0]}
    if all(s < 5 for _, s in pairs):
        return {"type": "lower_bound", "threshold_fraction_gt": pairs[-1][0]}
    for (f0, s0), (f1, s1) in zip(pairs[:-1], pairs[1:]):
        if s0 < 5 <= s1:
            return {"type": "bracket", "fraction_low_below_5": f0, "fraction_high_ge_5": f1, "snr_low": s0, "snr_high": s1}
    return {"type": "unresolved"}


def analyze(args):
    root = Path(args.artifact)
    manifest = json.loads((root / "cases/manifest.json").read_text())
    mass = float(manifest["mass_Msun"])
    if abs(mass - float(args.mass)) > 1e-9 * max(abs(mass), 1.0):
        raise ValueError(f"mass mismatch: manifest {mass}, requested {args.mass}")
    fracs = [float(x) for x in manifest["fractions"]]
    if len(fracs) != 4 or any(abs(a-b) > 1e-12 for a,b in zip(fracs, [1.0,0.1,0.01,0.001])):
        raise ValueError(f"unexpected frozen fractions: {fracs}")
    ref = load_cls(root / "class/output/ref_00_cl.dat")
    results = []
    for i, frac in enumerate(fracs):
        case = load_cls(root / f"class/output/f{i}_00_cl.dat")
        r = fisher_snr(ref, case)
        r.update({"case": f"f{i}", "fraction": frac, "tier": tier(r["snr"])})
        results.append(r)
    finite = [(r["fraction"], r["snr"]) for r in results if r["snr"] > 0 and math.isfinite(r["snr"])]
    if len(finite) >= 2:
        x = np.log([p[0] for p in finite]); y = np.log([p[1] for p in finite])
        slope = float(np.polyfit(x, y, 1)[0])
    else:
        slope = None
    scaling_pass = slope is not None and abs(slope - 1.0) <= 0.05
    valid = all(r["numerically_valid"] for r in results)
    out = {
        "schema": "KMDSB.M26.PBHCDIIdealCVObservabilityProxy.v1",
        "preregistration": "protocol/W04_M26_PBH_CDI_IDEAL_CV_OBSERVABILITY_PROXY_PREREGISTRATION_v0.1.md",
        "parent_run_id": 34555112732,
        "mass_Msun": mass,
        "fractions": fracs,
        "results": results,
        "fraction_loglog_snr_slope": slope,
        "fraction_scaling_pass": scaling_pass,
        "numerically_valid": valid,
        "five_sigma_sampled_constraint": five_sigma_bracket(fracs, [r["snr"] for r in results]),
        "classification": "M26_PBH_CDI_IDEAL_CV_MASS_PROXY_VALID" if valid and scaling_pass else "M26_PBH_CDI_IDEAL_CV_MASS_PROXY_UNRESOLVED",
        "observation_likelihood_gate": "OPEN",
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def aggregate(args):
    rows = [json.loads(p.read_text()) for p in Path(args.collected).glob("*/result.json")]
    rows.sort(key=lambda r: r["mass_Msun"])
    all_valid = len(rows) == 3 and all(r.get("numerically_valid") for r in rows)
    all_scaling = len(rows) == 3 and all(r.get("fraction_scaling_pass") for r in rows)
    classification = "M26_PBH_CDI_IDEAL_CV_OBSERVABILITY_PROXY_ESTABLISHED" if all_valid and all_scaling else "M26_PBH_CDI_IDEAL_CV_PROXY_NONLINEAR_OR_NUMERICALLY_UNRESOLVED"
    out = {
        "schema": "KMDSB.M26.PBHCDIIdealCVObservabilityProxy.Summary.v1",
        "preregistration": "protocol/W04_M26_PBH_CDI_IDEAL_CV_OBSERVABILITY_PROXY_PREREGISTRATION_v0.1.md",
        "parent_run_id": 34555112732,
        "masses": rows,
        "all_masses_numerically_valid": all_valid,
        "all_masses_fraction_scaling_pass": all_scaling,
        "classification": classification,
        "observation_likelihood_gate": "OPEN",
        "interpretation": "Optimistic full-sky noise-free fixed-parameter Gaussian CMB cosmic-variance proxy only; not a survey likelihood or exclusion.",
        "K1_promoted": False,
        "K4_promoted": False,
        "physical_falsification": False,
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("analyze")
    p.add_argument("--artifact", required=True)
    p.add_argument("--mass", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=analyze)
    a = sub.add_parser("aggregate")
    a.add_argument("--collected", required=True)
    a.add_argument("--output", required=True)
    a.set_defaults(func=aggregate)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
