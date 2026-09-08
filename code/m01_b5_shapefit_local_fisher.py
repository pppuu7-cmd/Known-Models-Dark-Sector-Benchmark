"""KMDSB M01/B5: local one-sided wCDM identifiability in DESI DR1 ShapeFit.

Purpose
-------
Project the frozen DSIR C1 constant-w phenomenological control into the corrected
DESI DR1 ShapeFit [DH/DM, f*sigma_s8, m+n] covariance used by DSIR Experiment 009.
This is a scoped identifiability control, not a full DESI likelihood and not a
precision CLASS/CAMB replacement.

Frozen assumptions
------------------
- flat constant-w control with Omega_m=0.3 (matching DSIR linear_controls.py);
- epsilon_w = 1+w is one-sided, epsilon_w >= 0;
- present-day fluctuation normalization held fixed, so f*sigma8 ratio is
  approximated by (f D)_w/(f D)_LCDM;
- late smooth-w deformation leaves the early transfer-shape coordinate m+n fixed
  in this local control, hence d(m+n)/d epsilon_w = 0;
- BGS excluded, matching DSIR Exp009 AP/growth control usage;
- no nuisance marginalization. Therefore the derived sigma(epsilon_w) is an
  optimistic sensitivity; adding nuisance freedom cannot improve it.

Provenance
----------
DSIR authority: e3276e2193f6a5200b541a194e3175356ae5a1c1
DSIR experiment: experiments/009_desi_dr1_multichannel_identifiability.py
DSIR covariance: data/observations/desi_dr1_shapefit_erratum_2026.json
DSIR control equations: src/dsir/linear_controls.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp

OMEGA_M = 0.3
COV_SCALE = 1e-4
USE = ("LRG1", "LRG2", "LRG3", "ELG2", "QSO")

# Corrected 2026 erratum values copied verbatim from the pinned DSIR JSON.
BINS = {
    "LRG1": {"z":0.51,"fid_ap":1.6858,"fid_g":0.4733,"cov":[[541.309833,48.425593,-4.652853,-37.707751],[48.425593,97.249820,-34.923265,-14.418597],[-4.652853,-34.923265,41.295470,15.405508],[-37.707751,-14.418597,15.405508,48.918910]]},
    "LRG2": {"z":0.71,"fid_ap":1.1399,"fid_g":0.4608,"cov":[[762.457717,39.781004,-1.896006,-62.812849],[39.781004,36.344098,-17.341350,-8.333900],[-1.896006,-17.341350,28.119682,8.865225],[-62.812849,-8.333900,8.865225,47.624520]]},
    "LRG3": {"z":0.92,"fid_ap":0.8162,"fid_g":0.4398,"cov":[[847.499793,26.038900,3.257324,-37.016091],[26.038900,16.251088,-10.044074,-3.698790],[3.257324,-10.044074,22.370314,6.467510],[-37.016091,-3.698790,6.467510,34.883220]]},
    "ELG2": {"z":1.32,"fid_ap":0.5029,"fid_g":0.3944,"cov":[[2342.506886,26.159601,13.521001,-95.336060],[26.159601,10.309303,-6.654663,-5.183903],[13.521001,-6.654663,13.997473,9.109619],[-95.336060,-5.183903,9.109619,43.575710]]},
    "QSO": {"z":1.49,"fid_ap":0.4228,"fid_g":0.3750,"cov":[[3013.788566,-2.205101,36.332110,-98.167826],[-2.205101,5.845806,-6.747133,-1.913326],[36.332110,-6.747133,19.785658,5.357546],[-98.167826,-1.913326,5.357546,26.266260]]},
}


def e2(z: float, w: float) -> float:
    a = 1.0 / (1.0 + z)
    return OMEGA_M * a**-3 + (1.0 - OMEGA_M) * a**(-3.0 * (1.0 + w))


def E(z: float, w: float) -> float:
    return math.sqrt(e2(z, w))


def dh_over_dm(z: float, w: float) -> float:
    # H0 and c cancel in DH/DM = [1/E(z)] / integral_0^z dz'/E(z').
    integral = quad(lambda zp: 1.0 / E(zp, w), 0.0, z, epsabs=1e-12, epsrel=1e-12)[0]
    return 1.0 / (E(z, w) * integral)


def dlnh_dlna(a: float, w: float) -> float:
    m = OMEGA_M * a**-3
    de = (1.0 - OMEGA_M) * a**(-3.0 * (1.0 + w))
    return -1.5 * (m + (1.0 + w) * de) / (m + de)


def omega_m_a(a: float, w: float) -> float:
    m = OMEGA_M * a**-3
    de = (1.0 - OMEGA_M) * a**(-3.0 * (1.0 + w))
    return m / (m + de)


def growth_D_f(z: float, w: float) -> tuple[float, float]:
    a_eval = 1.0 / (1.0 + z)
    a_ini = 1e-3
    x_ini = math.log(a_ini)

    def rhs(x, y):
        a = math.exp(x)
        d, v = y
        return [v, -(2.0 + dlnh_dlna(a, w)) * v + 1.5 * omega_m_a(a, w) * d]

    sol = solve_ivp(rhs, (x_ini, 0.0), [a_ini, a_ini], rtol=2e-10, atol=1e-12, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    d_today = float(sol.sol(0.0)[0])
    d_raw, v_raw = sol.sol(math.log(a_eval))
    D = float(d_raw / d_today)
    f = float(v_raw / d_raw)
    return D, f


def prediction(name: str, epsilon_w: float) -> np.ndarray:
    rec = BINS[name]
    z = rec["z"]
    w = -1.0 + epsilon_w
    ap_ratio = dh_over_dm(z, w) / dh_over_dm(z, -1.0)
    D0, f0 = growth_D_f(z, -1.0)
    D, f = growth_D_f(z, w)
    growth_ratio = (D * f) / (D0 * f0)
    return np.array([rec["fid_ap"] * ap_ratio, rec["fid_g"] * growth_ratio, 0.0])


def cov3(name: str) -> np.ndarray:
    full = np.asarray(BINS[name]["cov"], dtype=float) * COV_SCALE
    idx = [1, 2, 3]
    return full[np.ix_(idx, idx)]


def fisher(step: float) -> tuple[float, dict]:
    total = 0.0
    per_bin = {}
    for name in USE:
        p0 = prediction(name, 0.0)
        p1 = prediction(name, step)
        derivative = (p1 - p0) / step
        c = cov3(name)
        fi = float(derivative @ np.linalg.solve(c, derivative))
        total += fi
        per_bin[name] = {"derivative": derivative.tolist(), "fisher": fi}
    return total, per_bin


def exact_delta_chi2(epsilon_w: float) -> float:
    total = 0.0
    for name in USE:
        r = prediction(name, epsilon_w) - prediction(name, 0.0)
        c = cov3(name)
        total += float(r @ np.linalg.solve(c, r))
    return total


def main() -> None:
    steps = [1e-5, 1e-4, 1e-3, 1e-2]
    robustness = []
    for step in steps:
        F, _ = fisher(step)
        robustness.append({"finite_difference_step": step, "F": F, "sigma_epsilon": 1.0 / math.sqrt(F)})

    F, per_bin = fisher(1e-4)
    sigma = 1.0 / math.sqrt(F)
    probes = []
    for eps in [1e-4, 1e-3, 1e-2, 5e-2, 1e-1]:
        c2 = exact_delta_chi2(eps)
        probes.append({"epsilon_w": eps, "delta_chi2": c2, "sqrt_delta_chi2": math.sqrt(c2)})

    result = {
        "schema": "KMDSB.M01.B5.ShapeFitLocalFisher.v0.1",
        "classification": "NONIDENTIFIABLE_IN_FROZEN_LOCAL_CONTROL_SCOPE",
        "fisher_step": 1e-4,
        "F_epsilon_epsilon": F,
        "sigma_epsilon_optimistic_unmarginalized": sigma,
        "per_bin": per_bin,
        "finite_difference_robustness": robustness,
        "exact_probe_significances": probes,
        "interpretation": {
            "supported": "The frozen local C1 epsilon_w=1e-4 deformation is far below corrected DESI DR1 ShapeFit AP+growth+shape covariance sensitivity in this scoped control projection.",
            "conservative_logic": "No nuisance marginalization was included, so the reported sigma_epsilon is optimistic; adding nuisance freedom cannot turn the tiny local-step significance into a detection within this same mapping.",
            "not_supported": [
                "full DESI likelihood constraint on w",
                "all smooth-DE models are observationally nonidentifiable",
                "physical falsification of wCDM",
                "precision CLASS/CAMB prediction equivalence"
            ]
        }
    }
    out = Path(__file__).resolve().parents[1] / "models" / "smooth_nonphantom_de" / "b5_shapefit_local_fisher_result.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
