#!/usr/bin/env python3
"""KMDSB W03/M07 canonical scalar-field implementation/reference probe.

This analyzer is intentionally calibration-only. It compares a pure LambdaCDM
reference with a lambda=0 constant scalar split-reference and records finite-
lambda behavior descriptively. It does NOT freeze a discovery/holdout relation.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import re
from pathlib import Path

import numpy as np

Z_NODES = np.array([0.295, 0.51, 0.706, 0.934, 1.317, 1.491, 2.33], float)
K_NODES = np.array([0.001, 0.003, 0.01, 0.03, 0.1], float)


def pk_redshift(path: str) -> float:
    with open(path) as f:
        for _ in range(30):
            line = f.readline()
            if not line:
                break
            m = re.search(r"redshift\s+z\s*=\s*([+\-0-9.eE]+)", line, re.I)
            if m:
                return float(m.group(1))
    raise ValueError(f"no explicit redshift header in {path}")


def load_pk_matrix(directory: Path, prefix: str):
    hits = sorted(glob.glob(str(directory / f"{prefix}*pk.dat")))
    if not hits:
        raise FileNotFoundError(f"no P(k) files for {prefix}")
    rows = []
    for path in hits:
        z = pk_redshift(path)
        a = np.loadtxt(path, comments="#")
        k, p = np.asarray(a[:, 0], float), np.asarray(a[:, 1], float)
        mask = np.isfinite(k) & np.isfinite(p) & (k > 0) & (p > 0)
        k, p = k[mask], p[mask]
        order = np.argsort(k)
        k, p = k[order], p[order]
        if K_NODES[0] < k[0] or K_NODES[-1] > k[-1]:
            raise ValueError(f"frozen k nodes outside {path}: {k[0]}..{k[-1]}")
        core = np.exp(np.interp(np.log(K_NODES), np.log(k), np.log(p)))
        rows.append((z, core, Path(path).name))
    rows.sort(key=lambda x: x[0])
    z = np.array([r[0] for r in rows], float)
    if len(z) != len(Z_NODES) or not np.allclose(z, Z_NODES, rtol=0, atol=1e-10):
        raise ValueError(f"unexpected z nodes for {prefix}: {z}")
    return np.vstack([r[1] for r in rows]), [r[2] for r in rows]


def parse_background_titles(path: Path):
    text = ""
    with path.open() as f:
        for _ in range(30):
            line = f.readline()
            if not line:
                break
            if line.startswith("#"):
                text += " " + line[1:].strip()
            else:
                break
    # CLASS title line is normally tab-separated: 1:z  2:proper time ...
    matches = list(re.finditer(r"(?:^|\s)(\d+):", text))
    titles = {}
    for i, m in enumerate(matches):
        idx = int(m.group(1)) - 1
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        titles[idx] = text[start:end].strip()
    return titles


def find_col(titles, predicates):
    for idx, title in titles.items():
        low = title.lower().replace(" ", "")
        if all(p in low for p in predicates):
            return idx
    return None


def load_background(directory: Path, prefix: str):
    hits = sorted(directory.glob(f"{prefix}*background.dat"))
    if len(hits) != 1:
        raise FileNotFoundError(f"expected one background file for {prefix}, got {hits}")
    path = hits[0]
    titles = parse_background_titles(path)
    arr = np.loadtxt(path, comments="#")
    if arr.ndim != 2:
        raise ValueError(f"bad background table {path}")

    iz = find_col(titles, ["z"])
    ih = find_col(titles, ["h", "[1/mpc]"])
    irhoc = find_col(titles, ["rho_crit"])
    irhos = find_col(titles, ["rho_scf"])
    ips = find_col(titles, ["p_scf"])
    iphi = find_col(titles, ["phi_scf"])
    iphip = find_col(titles, ["phi'_scf"])
    if iz is None or ih is None:
        raise ValueError(f"could not identify z/H columns in {path}; titles={titles}")

    z = np.asarray(arr[:, iz], float)
    H = np.asarray(arr[:, ih], float)
    order = np.argsort(z)
    z, H = z[order], H[order]

    def interp(col):
        if col is None:
            return None
        y = np.asarray(arr[:, col], float)[order]
        return np.interp(Z_NODES, z, y)

    result = {
        "file": path.name,
        "H": np.interp(Z_NODES, z, H).tolist(),
        "z": Z_NODES.tolist(),
    }

    # Today is the row with minimum |z|.
    i0_orig = int(np.argmin(np.abs(np.asarray(arr[:, iz], float))))
    if irhos is not None and irhoc is not None:
        rho_s0 = float(arr[i0_orig, irhos])
        rho_c0 = float(arr[i0_orig, irhoc])
        result["Omega_scf_today"] = rho_s0 / rho_c0
        p0 = float(arr[i0_orig, ips]) if ips is not None else None
        result["w_scf_today"] = (p0 / rho_s0) if (p0 is not None and rho_s0 != 0) else None
        rho_z = interp(irhos)
        p_z = interp(ips)
        if rho_z is not None and p_z is not None:
            with np.errstate(divide="ignore", invalid="ignore"):
                w_z = p_z / rho_z
            result["w_scf_z"] = w_z.tolist()
    else:
        result["Omega_scf_today"] = 0.0
        result["w_scf_today"] = None

    if iphi is not None:
        result["phi_z"] = interp(iphi).tolist()
    if iphip is not None:
        result["phi_prime_z"] = interp(iphip).tolist()
    return result


def parse_parameters(directory: Path, prefix: str):
    hits = sorted(directory.glob(f"{prefix}*parameters.ini"))
    if not hits:
        return {"file": None}
    path = hits[0]
    data = {"file": path.name}
    for line in path.read_text(errors="replace").splitlines():
        if "=" not in line or line.lstrip().startswith("#"):
            continue
        key, val = [x.strip() for x in line.split("=", 1)]
        if key in {"scf_parameters", "scf_shooting_parameter", "Omega_scf", "scf_tuning_index", "attractor_ic_scf"}:
            data[key] = val
    return data


def safe_log_ratio(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.any(a <= 0) or np.any(b <= 0):
        raise ValueError("non-positive quantity in log ratio")
    return np.log(a / b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", required=True)
    ap.add_argument("--case", action="append", required=True,
                    help="label:prefix:lambda; use lambda=nan for reference")
    ap.add_argument("--json", required=True)
    args = ap.parse_args()
    directory = Path(args.directory)

    cases = []
    for spec in args.case:
        label, prefix, lam = spec.split(":", 2)
        lamv = None if lam.lower() == "nan" else float(lam)
        try:
            pk, pkfiles = load_pk_matrix(directory, prefix)
            bg = load_background(directory, prefix)
            params = parse_parameters(directory, prefix)
            cases.append({
                "label": label,
                "prefix": prefix,
                "lambda": lamv,
                "status": "AVAILABLE",
                "pk": pk,
                "pk_files": pkfiles,
                "background": bg,
                "parameters": params,
            })
        except Exception as exc:
            cases.append({
                "label": label, "prefix": prefix, "lambda": lamv,
                "status": "MISSING_OR_INVALID", "error": str(exc)
            })

    ref = next((c for c in cases if c["label"] == "REF_LCDM" and c["status"] == "AVAILABLE"), None)
    l0 = next((c for c in cases if c["label"] == "SCF_SPLIT_L0" and c["status"] == "AVAILABLE"), None)
    if ref is None or l0 is None:
        raise SystemExit("reference and lambda=0 split-reference must both be available")

    ref_pk = ref["pk"]
    ref_H = np.asarray(ref["background"]["H"], float)
    comparisons = []
    for c in cases:
        if c["status"] != "AVAILABLE" or c is ref:
            continue
        rpk = safe_log_ratio(c["pk"], ref_pk)
        rH = safe_log_ratio(c["background"]["H"], ref_H)
        comparisons.append({
            "label": c["label"],
            "lambda": c["lambda"],
            "max_abs_lnP": float(np.max(np.abs(rpk))),
            "l2_lnP": float(np.linalg.norm(rpk)),
            "max_abs_lnH": float(np.max(np.abs(rH))),
            "l2_lnH": float(np.linalg.norm(rH)),
            "response_vector_lnP": rpk.reshape(-1).tolist(),
            "response_lnH": rH.tolist(),
        })

    # Drop bulky arrays from case records after extracting comparisons.
    serial_cases = []
    for c in cases:
        cc = dict(c)
        cc.pop("pk", None)
        serial_cases.append(cc)

    split_cmp = next(x for x in comparisons if x["label"] == "SCF_SPLIT_L0")
    out = {
        "schema_version": "KMDSB-W03-M07-probe-v0.1",
        "scope": "implementation/reference probe only; finite-lambda outputs are descriptive and not prospective evidence",
        "frozen_grid": {"z": Z_NODES.tolist(), "k_h_mpc": K_NODES.tolist()},
        "cases": serial_cases,
        "comparisons_to_LCDM": comparisons,
        "lambda0_reference_control": {
            "max_abs_lnP": split_cmp["max_abs_lnP"],
            "max_abs_lnH": split_cmp["max_abs_lnH"],
            "interpretation": "numerical diagnostic only; hard production tolerance must be frozen after this infrastructure probe and before production science",
        },
    }
    Path(args.json).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
