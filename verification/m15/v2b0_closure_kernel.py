#!/usr/bin/env python3
"""KMDSB M15 V2b0 preregistered closure-kernel algebra audit.

Authority:
  protocol/W03_M15_V2B0_CLOSURE_KERNEL_PREREGISTRATION_v0.2.md

This is deliberately NOT a Boltzmann solver and NOT author-code reproduction.
It tests the literal published M15 Eqs. (45),(46),(49),(50) mapping on
analytic smooth histories before a self-consistent V2b1 implementation.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


N = 4097
X_MIN = math.log(0.2)
X_MAX = 0.0
OMEGA_M = 0.3
OMEGA_L = 0.7
H0 = 1.0
K = 0.2
ALPHAS = [0.0, -0.05, 0.05, 0.25]
CS2S = [0.0, 0.5, 1.0]
DERIVATIVE_TOL = 2.0e-7
REFERENCE_ABS_TOL = 1.0e-14
AFFINITY_TOL = 1.0e-12


def max_symrel(a: np.ndarray, b: np.ndarray) -> float:
    """Frozen symmetric-style point metric with a tiny numerical floor."""
    den = np.maximum(np.maximum(np.abs(a), np.abs(b)), 1.0e-30)
    return float(np.max(np.abs(a - b) / den))


def maxabs(a: np.ndarray) -> float:
    return float(np.max(np.abs(a)))


def l2(a: np.ndarray) -> float:
    return float(np.linalg.norm(a))


def fd4_centered(y: np.ndarray, dx: float) -> np.ndarray:
    """Fourth-order centered d/dx on i=2..N-3."""
    return (y[:-4] - 8.0 * y[1:-3] + 8.0 * y[3:-1] - y[4:]) / (12.0 * dx)


def build_common_histories() -> dict[str, np.ndarray]:
    x = np.linspace(X_MIN, X_MAX, N)
    dx = float(x[1] - x[0])
    a = np.exp(x)

    e2 = OMEGA_M * np.exp(-3.0 * x) + OMEGA_L
    H = H0 * np.sqrt(e2)
    dlnH_dx = -1.5 * OMEGA_M * np.exp(-3.0 * x) / e2
    mathcalH = a * H
    dlnmathcalH_dx = 1.0 + dlnH_dx

    psi = 2.0e-5 * (1.0 + 0.15 * x + 0.03 * x * x)
    dpsi_dx = 2.0e-5 * (0.15 + 0.06 * x)
    d2psi_dx2 = np.full_like(x, 2.0e-5 * 0.06)

    phi = 1.7e-5 * (1.0 - 0.08 * x + 0.02 * x * x)
    dphi_dx = 1.7e-5 * (-0.08 + 0.04 * x)
    d2phi_dx2 = np.full_like(x, 1.7e-5 * 0.04)

    theta_tot = 3.0e-5 * mathcalH * np.exp(0.4 * x) * (1.0 + 0.1 * x)
    dtheta_dx = theta_tot * (
        dlnmathcalH_dx + 0.4 + 0.1 / (1.0 + 0.1 * x)
    )

    # Conformal derivatives: Y' = mathcalH dY/dx.
    psi_prime = mathcalH * dpsi_dx
    phi_prime = mathcalH * dphi_dx

    S = psi_prime + phi_prime + theta_tot
    theta_hat = S / a

    # dS/dx, then d[(S/a)]/dx = (dS/dx-S)/a because da/dx=a.
    dmathcalH_dx = mathcalH * dlnmathcalH_dx
    dS_dx = (
        dmathcalH_dx * (dpsi_dx + dphi_dx)
        + mathcalH * (d2psi_dx2 + d2phi_dx2)
        + dtheta_dx
    )
    dtheta_hat_dx = (dS_dx - S) / a

    return {
        "x": x,
        "dx": np.array(dx),
        "a": a,
        "H": H,
        "dlnH_dx": dlnH_dx,
        "mathcalH": mathcalH,
        "psi": psi,
        "phi": phi,
        "theta_tot": theta_tot,
        "theta_hat": theta_hat,
        "dtheta_hat_dx": dtheta_hat_dx,
    }


def evaluate_alpha(common: dict[str, np.ndarray], alpha: float) -> dict:
    x = common["x"]
    a = common["a"]
    H = common["H"]
    dlnH_dx = common["dlnH_dx"]
    mathcalH = common["mathcalH"]
    psi = common["psi"]
    theta_tot = common["theta_tot"]
    theta_hat = common["theta_hat"]
    dtheta_hat_dx = common["dtheta_hat_dx"]
    dx = float(common["dx"])

    rho_l = OMEGA_L * H ** (-2.0 * alpha)
    dlnrho_dx = -2.0 * alpha * dlnH_dx
    drho_dx = rho_l * dlnrho_dx
    Q = H * drho_dx

    A = -2.0 * alpha / (3.0 * H)
    dA_dx = A * (-dlnH_dx)
    delta_l = A * theta_hat
    ddelta_dx = dA_dx * theta_hat + A * dtheta_hat_dx
    delta_prime_analytic = mathcalH * ddelta_dx

    delta_prime_fd4 = mathcalH[2:-2] * fd4_centered(delta_l, dx)
    analytic_interior = delta_prime_analytic[2:-2]
    derivative_metric = max_symrel(analytic_interior, delta_prime_fd4)

    vhat = -theta_tot / (K * K)
    by_cs2: dict[str, dict] = {}
    qhats: dict[float, np.ndarray] = {}
    fhats: dict[float, np.ndarray] = {}

    for cs2 in CS2S:
        qhat = (
            rho_l / a * (delta_prime_analytic + 3.0 * mathcalH * (cs2 + 1.0) * delta_l)
            - Q * (psi - delta_l)
        )
        fhat = cs2 * rho_l * delta_l / a - Q * vhat
        qhats[cs2] = qhat
        fhats[cs2] = fhat
        by_cs2[f"{cs2:.1f}"] = {
            "finite": bool(np.all(np.isfinite(qhat)) and np.all(np.isfinite(fhat))),
            "qhat_maxabs": maxabs(qhat),
            "fhat_maxabs": maxabs(fhat),
            "qhat_l2": l2(qhat),
            "fhat_l2": l2(fhat),
        }

    qhat_mid_avg = 0.5 * (qhats[0.0] + qhats[1.0])
    fhat_mid_avg = 0.5 * (fhats[0.0] + fhats[1.0])
    qhat_affinity = max_symrel(qhats[0.5], qhat_mid_avg)
    fhat_affinity = max_symrel(fhats[0.5], fhat_mid_avg)
    qhat_endpoint_l2 = l2(qhats[1.0] - qhats[0.0])
    fhat_endpoint_l2 = l2(fhats[1.0] - fhats[0.0])

    domain_finite = bool(
        np.all(np.isfinite(rho_l))
        and np.all(np.isfinite(Q))
        and np.all(np.isfinite(delta_l))
        and np.all(np.isfinite(delta_prime_analytic))
        and np.all(rho_l > 0.0)
        and np.all(H > 0.0)
        and np.all(mathcalH > 0.0)
        and K > 0.0
        and all(v["finite"] for v in by_cs2.values())
    )

    reference = {
        "Q_maxabs": maxabs(Q),
        "delta_lambda_maxabs": maxabs(delta_l),
        "delta_lambda_prime_maxabs": maxabs(delta_prime_analytic),
        "qhat_maxabs_over_cs2": max(maxabs(qhats[c]) for c in CS2S),
        "fhat_maxabs_over_cs2": max(maxabs(fhats[c]) for c in CS2S),
    }
    reference_pass = all(v <= REFERENCE_ABS_TOL for v in reference.values()) if alpha == 0.0 else None

    affinity_pass = (
        qhat_affinity <= AFFINITY_TOL and fhat_affinity <= AFFINITY_TOL
    )
    endpoint_separation_pass = (
        (qhat_endpoint_l2 > 0.0 or fhat_endpoint_l2 > 0.0) if alpha != 0.0 else True
    )

    return {
        "alpha": alpha,
        "rho_lambda_min": float(np.min(rho_l)),
        "rho_lambda_max": float(np.max(rho_l)),
        "Q_min": float(np.min(Q)),
        "Q_max": float(np.max(Q)),
        "derivative": {
            "max_symrel": derivative_metric,
            "max_abs_difference": maxabs(analytic_interior - delta_prime_fd4),
            "tolerance": DERIVATIVE_TOL,
            "pass": derivative_metric <= DERIVATIVE_TOL,
        },
        "reference_null": {
            **reference,
            "tolerance": REFERENCE_ABS_TOL,
            "pass": reference_pass,
        },
        "sound_speed_affinity": {
            "qhat_max_symrel": qhat_affinity,
            "fhat_max_symrel": fhat_affinity,
            "tolerance": AFFINITY_TOL,
            "pass": affinity_pass,
        },
        "sound_speed_endpoint_separation": {
            "qhat_l2": qhat_endpoint_l2,
            "fhat_l2": fhat_endpoint_l2,
            "pass": endpoint_separation_pass,
        },
        "by_cs2": by_cs2,
        "domain_finite_positive": domain_finite,
    }


def main() -> None:
    common = build_common_histories()
    cases = [evaluate_alpha(common, alpha) for alpha in ALPHAS]

    derivative_pass = all(c["derivative"]["pass"] for c in cases)
    reference_case = next(c for c in cases if c["alpha"] == 0.0)
    reference_pass = bool(reference_case["reference_null"]["pass"])
    affinity_pass = all(c["sound_speed_affinity"]["pass"] for c in cases)
    endpoint_pass = all(c["sound_speed_endpoint_separation"]["pass"] for c in cases)
    domain_pass = all(c["domain_finite_positive"] for c in cases)

    if not domain_pass:
        classification = "M15_V2B0_CLOSURE_KERNEL_FAIL_DOMAIN"
    elif not reference_pass:
        classification = "M15_V2B0_CLOSURE_KERNEL_FAIL_REFERENCE"
    elif not derivative_pass:
        classification = "M15_V2B0_CLOSURE_KERNEL_FAIL_DERIVATIVE"
    elif not affinity_pass or not endpoint_pass:
        classification = "M15_V2B0_CLOSURE_KERNEL_FAIL_AFFINITY"
    else:
        classification = "M15_V2B0_CLOSURE_KERNEL_PASS"

    result = {
        "schema": "KMDSB.M15.V2B0.closure_kernel.v1",
        "preregistration": "protocol/W03_M15_V2B0_CLOSURE_KERNEL_PREREGISTRATION_v0.2.md",
        "source_authority": "models/generalized_chaplygin/m15_v2_equation_to_class_map.md",
        "scope": "pre-solver algebra audit; not author-code reproduction; no K3-K5 promotion",
        "coordinate": {
            "x": "ln(a)",
            "xmin": X_MIN,
            "xmax": X_MAX,
            "nodes": N,
            "conformal_derivative_rule": "Yprime=mathcalH*dY/dx",
        },
        "frozen_constants": {
            "H0": H0,
            "Omega_m": OMEGA_M,
            "Omega_Lambda": OMEGA_L,
            "k": K,
            "alphas": ALPHAS,
            "cs2_values": CS2S,
        },
        "equations": {
            "delta_lambda": "-(2 alpha/(3 H))*ThetaHat",
            "ThetaHat": "(psi_prime+phi_prime+theta_tot)/a",
            "Q": "H*d rho_lambda/d ln a",
            "Qhat": "rho_lambda/a*(delta_lambda_prime+3 mathcalH (cs2+1) delta_lambda)-Q*(psi-delta_lambda)",
            "fhat": "cs2*rho_lambda*delta_lambda/a-Q*vhat",
            "vhat": "-theta_tot/k^2",
        },
        "thresholds": {
            "derivative_max_symrel": DERIVATIVE_TOL,
            "reference_maxabs": REFERENCE_ABS_TOL,
            "affinity_max_symrel": AFFINITY_TOL,
        },
        "gates": {
            "derivative_pass": derivative_pass,
            "reference_pass": reference_pass,
            "affinity_pass": affinity_pass,
            "endpoint_separation_pass": endpoint_pass,
            "domain_pass": domain_pass,
        },
        "cases": cases,
        "classification": classification,
        "scientific_promotion": False,
        "next_if_pass": "preregister V2b1 self-consistent interacting perturbation evolution and IC audit",
    }

    canonical = Path("models/generalized_chaplygin/M15_V2B0_CLOSURE_KERNEL_RESULT.json")
    mirror = Path("waves/wave_03_expanded_dark_energy/M15_V2B0_CLOSURE_KERNEL_RESULT.json")
    canonical.parent.mkdir(parents=True, exist_ok=True)
    mirror.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    canonical.write_text(payload)
    mirror.write_text(payload)
    print(json.dumps({"classification": classification, "gates": result["gates"]}, indent=2))

    if classification != "M15_V2B0_CLOSURE_KERNEL_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
