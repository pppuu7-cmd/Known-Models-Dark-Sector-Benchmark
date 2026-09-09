#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
M07 = ROOT / "waves/wave_03_expanded_dark_energy/M07_LOCAL_Q_DIRECTION.json"
M08 = ROOT / "waves/wave_03_expanded_dark_energy/M08_CPL_LOCAL_BASIS.json"
OUT = ROOT / "waves/wave_03_expanded_dark_energy/M08_M07_ABSORPTION_RESULT.json"


def residual_fraction(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(a), 1e-30))


def main() -> None:
    m07 = json.loads(M07.read_text())
    m08 = json.loads(M08.read_text())

    tP = np.asarray(m07["local_q_response_vector_lnP"], float)
    tH = np.asarray(m07["local_q_response_lnH"], float)
    j0P = np.asarray(m08["directions"]["epsilon0"]["P"], float)
    j0H = np.asarray(m08["directions"]["epsilon0"]["H"], float)
    jaP = np.asarray(m08["directions"]["wa"]["P"], float)
    jaH = np.asarray(m08["directions"]["wa"]["H"], float)

    target = np.r_[tP, tH]
    J = np.column_stack([np.r_[j0P, j0H], np.r_[jaP, jaH]])

    coeff, *_ = np.linalg.lstsq(J, target, rcond=None)
    pred = J @ coeff
    predP = np.column_stack([j0P, jaP]) @ coeff
    predH = np.column_stack([j0H, jaH]) @ coeff

    # Same-solver constant-w-like baseline: epsilon0 direction only.
    c0 = float(np.dot(J[:,0], target) / np.dot(J[:,0], J[:,0]))
    pred0 = J[:,0] * c0
    pred0P = j0P * c0
    pred0H = j0H * c0

    out = {
        "schema": "KMDSB.W03.M08.M07Absorption.v0.1",
        "scope": "unwhitened common 35-node lnP + 7-node lnH local theory-response geometry",
        "target": "M07 local dr/dq with q=lambda^2",
        "comparator": "M08 CPL local span {d/depsilon0,d/dwa}",
        "fit_rule": "one shared parameter vector across P and H blocks",
        "cpl_fit_coefficients_per_unit_q": {
            "epsilon0": float(coeff[0]),
            "wa": float(coeff[1])
        },
        "cpl_residual_fractions": {
            "combined_PH": residual_fraction(target, pred),
            "P": residual_fraction(tP, predP),
            "H": residual_fraction(tH, predH)
        },
        "same_solver_constant_w_baseline": {
            "epsilon0_per_unit_q": c0,
            "residual_fractions": {
                "combined_PH": residual_fraction(target, pred0),
                "P": residual_fraction(tP, pred0P),
                "H": residual_fraction(tH, pred0H)
            }
        },
        "improvement_factor_constant_w_residual_over_CPL_residual": {
            "combined_PH": residual_fraction(target, pred0)/residual_fraction(target, pred),
            "P": residual_fraction(tP, pred0P)/residual_fraction(tP, predP),
            "H": residual_fraction(tH, pred0H)/residual_fraction(tH, predH)
        },
        "example_mapping": {
            "lambda_0p30_q_0p09": {
                "epsilon0": float(coeff[0]*0.09),
                "w0": float(-1 + coeff[0]*0.09),
                "wa": float(coeff[1]*0.09)
            },
            "lambda_0p225_q_0p050625": {
                "epsilon0": float(coeff[0]*0.050625),
                "w0": float(-1 + coeff[0]*0.050625),
                "wa": float(coeff[1]*0.050625)
            }
        },
        "classification": "CPL_ABSORBS_M07_CROSSCHANNEL_SEPARATOR_WITH_SCOPE",
        "B7_implication_for_M07": "The previously identified constant-w P/H separator does not survive a stronger 2D CPL smooth-DE comparator in this unwhitened local theory-response scope.",
        "anti_overclaim": [
            "This is a local linear theory-space absorption test, not observational discrimination.",
            "CPL absorption does not prove CPL is the physical dark-energy mechanism.",
            "M07 remains predictive within its own tested family; this result specifically weakens mechanism-level novelty of the P/H separator.",
            "Observation-space promotion must obey AD-002 and use one frozen common observation operator and covariance vector for both families."
        ]
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
