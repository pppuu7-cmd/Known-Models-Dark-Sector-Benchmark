#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
import numpy as np

COV_SCALE = 1e-4
USE = ("LRG1", "LRG2", "LRG3", "ELG2", "QSO")
BINS = {
    "LRG1": {"z":0.51,"fid_ap":1.6858,"fid_g":0.4733,"cov":[[541.309833,48.425593,-4.652853,-37.707751],[48.425593,97.249820,-34.923265,-14.418597],[-4.652853,-34.923265,41.295470,15.405508],[-37.707751,-14.418597,15.405508,48.918910]]},
    "LRG2": {"z":0.71,"fid_ap":1.1399,"fid_g":0.4608,"cov":[[762.457717,39.781004,-1.896006,-62.812849],[39.781004,36.344098,-17.341350,-8.333900],[-1.896006,-17.341350,28.119682,8.865225],[-62.812849,-8.333900,8.865225,47.624520]]},
    "LRG3": {"z":0.92,"fid_ap":0.8162,"fid_g":0.4398,"cov":[[847.499793,26.038900,3.257324,-37.016091],[26.038900,16.251088,-10.044074,-3.698790],[3.257324,-10.044074,22.370314,6.467510],[-37.016091,-3.698790,6.467510,34.883220]]},
    "ELG2": {"z":1.32,"fid_ap":0.5029,"fid_g":0.3944,"cov":[[2342.506886,26.159601,13.521001,-95.336060],[26.159601,10.309303,-6.654663,-5.183903],[13.521001,-6.654663,13.997473,9.109619],[-95.336060,-5.183903,9.109619,43.575710]]},
    "QSO": {"z":1.49,"fid_ap":0.4228,"fid_g":0.3750,"cov":[[3013.788566,-2.205101,36.332110,-98.167826],[-2.205101,5.845806,-6.747133,-1.913326],[36.332110,-6.747133,19.785658,5.357546],[-98.167826,-1.913326,5.357546,26.266260]]},
}

COORD_ORDER = [f"{b}:{c}" for b in USE for c in ("DH_over_DM", "f_sigma_s8_control", "m_plus_n_control")]


def titles(path: Path) -> dict[int, str]:
    text = ""
    with path.open() as f:
        for _ in range(40):
            s = f.readline()
            if not s:
                break
            if s.startswith("#"):
                text += " " + s[1:].strip()
            else:
                break
    ms = list(re.finditer(r"(?:^|\s)(\d+):", text))
    out = {}
    for i, m in enumerate(ms):
        out[int(m.group(1)) - 1] = text[m.end():(ms[i+1].start() if i+1 < len(ms) else len(text))].strip()
    return out


def load_bg(path: Path) -> dict[str, np.ndarray]:
    tt = titles(path)
    a = np.loadtxt(path, comments="#")
    def col(prefix: str) -> int:
        hits = [i for i, t in tt.items() if t.startswith(prefix)]
        if len(hits) != 1:
            raise ValueError(f"column {prefix!r} in {path}: {hits}")
        return hits[0]
    iz = col("z")
    ih = col("H [1/Mpc]")
    idm = col("comov. dist.")
    iD = col("gr.fac. D")
    iff = col("gr.fac. f")
    order = np.argsort(a[:, iz])
    return {
        "z": a[order, iz],
        "H": a[order, ih],
        "DM": a[order, idm],
        "D": a[order, iD],
        "f": a[order, iff],
    }


def at(bg: dict[str, np.ndarray], key: str, z: float) -> float:
    return float(np.interp(z, bg["z"], bg[key]))


def response(bg: dict[str, np.ndarray], ref: dict[str, np.ndarray]) -> np.ndarray:
    vals = []
    for name in USE:
        b = BINS[name]
        z = b["z"]
        H, DM, D, f = (at(bg, k, z) for k in ("H", "DM", "D", "f"))
        Hr, DMr, Dr, fr = (at(ref, k, z) for k in ("H", "DM", "D", "f"))
        ap = b["fid_ap"] * (Hr / H) * (DMr / DM)
        growth = b["fid_g"] * (D * f) / (Dr * fr)
        vals.extend([ap - b["fid_ap"], growth - b["fid_g"], 0.0])
    return np.asarray(vals, float)


def covariance() -> np.ndarray:
    C = np.zeros((15, 15), float)
    for ib, name in enumerate(USE):
        full = np.asarray(BINS[name]["cov"], float) * COV_SCALE
        block = full[np.ix_([1, 2, 3], [1, 2, 3])]
        sl = slice(3*ib, 3*ib+3)
        C[sl, sl] = block
    return C


def geom(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
    na = float(np.linalg.norm(a)); nb = float(np.linalg.norm(b))
    c = float(np.dot(a, b) / max(na * nb, 1e-300))
    c = max(-1.0, min(1.0, c))
    return {
        "cosine": c,
        "angle_deg": float(np.degrees(np.arccos(c))),
        "acute_deg": float(np.degrees(np.arccos(abs(c)))),
        "relative_l2_difference": float(np.linalg.norm(a-b) / max(na, nb, 1e-300)),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True)
    ap.add_argument("--m07-0025", required=True)
    ap.add_argument("--m07-0075", required=True)
    ap.add_argument("--m08-e0p", required=True)
    ap.add_argument("--m08-e0m", required=True)
    ap.add_argument("--m08-wap", required=True)
    ap.add_argument("--m08-wam", required=True)
    ap.add_argument("--m08-step", type=float, default=1e-3)
    ap.add_argument("--json", required=True)
    args = ap.parse_args()

    ref = load_bg(Path(args.ref))
    r25 = response(load_bg(Path(args.m07_0025)), ref)
    r75 = response(load_bg(Path(args.m07_0075)), ref)
    q25 = 0.025**2
    q75 = 0.075**2
    jq25 = r25 / q25
    jq75 = r75 / q75
    jq = 0.5 * (jq25 + jq75)

    re0p = response(load_bg(Path(args.m08_e0p)), ref)
    re0m = response(load_bg(Path(args.m08_e0m)), ref)
    rwap = response(load_bg(Path(args.m08_wap)), ref)
    rwam = response(load_bg(Path(args.m08_wam)), ref)
    h = args.m08_step
    j0 = (re0p - re0m) / (2*h)
    ja = (rwap - rwam) / (2*h)
    J = np.column_stack([j0, ja])

    C = covariance()
    if C.shape != (15, 15):
        raise RuntimeError(f"bad covariance shape {C.shape}")
    sym = float(np.max(np.abs(C-C.T)))
    L = np.linalg.cholesky(C)
    recon = float(np.linalg.norm(L@L.T-C) / np.linalg.norm(C))
    cond = float(np.linalg.cond(C))

    jqw = np.linalg.solve(L, jq)
    Jw = np.linalg.solve(L, J)
    coeff, *_ = np.linalg.lstsq(Jw, jqw, rcond=None)
    predw = Jw @ coeff
    residw = jqw - predw

    Fqq = float(jqw @ jqw)
    Fqm = jqw @ Jw
    Fmm = Jw.T @ Jw
    if np.linalg.matrix_rank(Fmm) != 2:
        raise RuntimeError("CPL Fisher block is singular")
    prof = float(Fqq - Fqm @ np.linalg.solve(Fmm, Fqm.T))
    if prof <= 0:
        raise RuntimeError(f"non-positive profiled F_q {prof}")

    sigma_un = 1.0 / math.sqrt(Fqq)
    sigma_prof = 1.0 / math.sqrt(prof)
    residual_fraction = float(np.linalg.norm(residw) / np.linalg.norm(jqw))
    subspace_angle = float(np.degrees(np.arcsin(min(1.0, max(0.0, residual_fraction)))))
    s_cpl = np.linalg.svd(Jw, compute_uv=False)

    q_probe = 0.09
    significance = q_probe / sigma_prof
    classification = (
        "NONIDENTIFIABLE_AFTER_CPL_PROFILING_IN_COMMON_SHAPEFIT_CONTROL"
        if significance < 1.0 else
        "IDENTIFIABLE_AT_Q_0P09_AFTER_CPL_PROFILING_IN_COMMON_SHAPEFIT_CONTROL"
    )

    fullF = np.empty((3,3), float)
    fullF[0,0] = Fqq
    fullF[0,1:] = Fqm
    fullF[1:,0] = Fqm
    fullF[1:,1:] = Fmm

    out = {
        "schema": "KMDSB.W03.M07M08.CommonShapeFit.v0.1",
        "contract": "protocol/W03_M07_M08_COMMON_SHAPEFIT_OPERATOR_V0_1.md",
        "coordinate_order": COORD_ORDER,
        "covariance": {
            "shape": list(C.shape),
            "max_asymmetry": sym,
            "condition_number_2": cond,
            "cholesky_roundtrip_relative_l2": recon,
            "source_semantics": "corrected DESI DR1 ShapeFit control; five independent 3x3 blocks from 4x4 tables indices [1,2,3] times 1e-4"
        },
        "m07_q_direction": {
            "qscaled_0025_vs_0075": geom(jq25, jq75),
            "unwhitened_norm_mean_direction": float(np.linalg.norm(jq)),
            "whitened_norm": float(np.linalg.norm(jqw)),
            "unprofiled_F_q": Fqq,
            "unprofiled_sigma_q": sigma_un
        },
        "m08_whitened_local_span": {
            "singular_values": s_cpl.tolist(),
            "sigma2_over_sigma1": float(s_cpl[1]/s_cpl[0]),
            "F_mm": Fmm.tolist()
        },
        "profile_over_m08": {
            "coefficients_per_unit_q": {"epsilon0": float(coeff[0]), "wa": float(coeff[1])},
            "whitened_residual_norm": float(np.linalg.norm(residw)),
            "whitened_residual_fraction": residual_fraction,
            "subspace_angle_deg": subspace_angle,
            "profiled_F_q": prof,
            "profiled_sigma_q": sigma_prof,
            "sigma_degradation_factor": float(sigma_prof/sigma_un),
            "full_F_q_e0_wa": fullF.tolist(),
            "q_0p09_profiled_significance_sigma": significance
        },
        "classification": classification,
        "anti_overclaim": [
            "This is a scoped common-operator ShapeFit control, not a full DESI likelihood.",
            "This is not DSIR Article-2 G5 closure and does not implement the full multi-family weighting/bootstrap stress suite.",
            "The m_plus_n response is frozen to zero for both families in this late-time control.",
            "A sub-1-sigma classification is observational non-identifiability in this control, not physical falsification.",
            "Local CPL profiling does not establish global equivalence of CPL and canonical quintessence."
        ]
    }
    Path(args.json).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
