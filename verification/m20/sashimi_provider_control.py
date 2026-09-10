#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np

PIN = "e17d3664dac677b604fd4ff02fb2af105a6937fa"
PREREG = "protocol/W04_M20_SASHIMI_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md"
OUT_NAMES = [
    'ma200','z_acc','rsCDM_acc','rhosCDM_acc','rmaxCDM_acc','VmaxCDM_acc',
    'rsSIDM_acc','rhosSIDM_acc','rcSIDM_acc','rmaxSIDM_acc','VmaxSIDM_acc',
    'm_z0','rsCDM_z0','rhosCDM_z0','rmaxCDM_z0','VmaxCDM_z0','rsSIDM_z0',
    'rhosSIDM_z0','rcSIDM_z0','rmaxSIDM_z0','VmaxSIDM_z0','ctCDM_z0',
    'tt_ratio','weightCDM','weightSIDM','surviveCDM','surviveSIDM'
]
PAIRS = [
    ('VmaxSIDM_z0','VmaxCDM_z0'),
    ('rmaxSIDM_z0','rmaxCDM_z0'),
    ('rsSIDM_z0','rsCDM_z0'),
    ('rhosSIDM_z0','rhosCDM_z0'),
]


def main(provider: Path, pytest_status: int, out: Path):
    sys.path.insert(0, str(provider.resolve()))
    import sashimi_si

    result = {
        "schema": "KMDSB.M20.SashimiProviderControl.v1",
        "provider": "shinichiroando/sashimi-si",
        "pin": PIN,
        "preregistration": PREREG,
        "pytest_status": int(pytest_status),
        "K1_promoted": False,
        "physical_falsification": False,
        "exact_zero": {},
    }

    physical_ok = False
    try:
        sh = sashimi_si.subhalo_properties(sigma0_m=0.0, w=24.33)
        args = dict(M0=1.e12, redshift=0., M0_at_redshift=True,
                    dz=0.2, N_herm=3, zmax=4., logmamin=9, N_ma=30)
        raw = sh.subhalo_properties_calc(**args)
        if len(raw) != len(OUT_NAMES):
            raise RuntimeError(f"output length {len(raw)} != {len(OUT_NAMES)}")
        cat = dict(zip(OUT_NAMES, raw))
        weight = np.asarray(cat['weightSIDM'])
        alive = np.isfinite(weight) & (weight > 0.)
        if not alive.any():
            raise RuntimeError("no positive finite SIDM-weight entries")

        pair_stats = {}
        finite_physical = True
        max_pair_rel = 0.0
        for sidm, cdm in PAIRS:
            a = np.asarray(cat[sidm], dtype=float)[alive]
            b = np.asarray(cat[cdm], dtype=float)[alive]
            finite = bool(np.all(np.isfinite(a)) and np.all(np.isfinite(b)))
            finite_physical = finite_physical and finite
            den = np.maximum(np.maximum(np.abs(a), np.abs(b)), 1e-300)
            rel = np.abs(a-b)/den
            mx = float(np.max(rel)) if rel.size else math.inf
            max_pair_rel = max(max_pair_rel, mx)
            pair_stats[sidm + '_vs_' + cdm] = {
                "finite": finite,
                "max_relative_residual": mx,
                "n": int(rel.size),
            }

        rc = np.asarray(cat['rcSIDM_z0'], dtype=float)[alive]
        rs = np.asarray(cat['rsSIDM_z0'], dtype=float)[alive]
        core_ratio = np.abs(rc) / np.maximum(np.abs(rs), 1e-300)
        max_core = float(np.max(core_ratio)) if core_ratio.size else math.inf
        core_finite = bool(np.all(np.isfinite(core_ratio)))
        tt = np.asarray(cat['tt_ratio'], dtype=float)[alive]

        result['exact_zero'] = {
            "executed": True,
            "n_retained": int(alive.sum()),
            "pair_stats": pair_stats,
            "max_structural_relative_residual": max_pair_rel,
            "max_abs_core_over_rs": max_core,
            "tt_ratio_all_finite": bool(np.all(np.isfinite(tt))),
            "tt_ratio_nonfinite_count": int(np.size(tt)-np.isfinite(tt).sum()),
            "physical_outputs_finite": bool(finite_physical and core_finite),
            "identity_threshold": 1e-10,
            "core_threshold": 1e-10,
        }
        physical_ok = bool(finite_physical and core_finite and max_pair_rel <= 1e-10 and max_core <= 1e-10)
    except Exception as e:
        result['exact_zero'] = {"executed": False, "error": repr(e)}

    if pytest_status == 0 and physical_ok:
        result['classification'] = 'M20_PROVIDER_CONTROL_PASS_EXACT_ZERO_CDM_BOUNDARY'
    elif pytest_status == 0:
        result['classification'] = 'M20_PROVIDER_CONTROL_PASS_SMALL_SIGMA_EXACT_ZERO_BLOCKED'
    else:
        result['classification'] = 'M20_PROVIDER_CONTROL_BLOCKED'

    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: sashimi_provider_control.py PROVIDER PYTEST_STATUS OUT')
    main(Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]))
