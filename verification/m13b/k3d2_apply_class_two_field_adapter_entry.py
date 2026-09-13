#!/usr/bin/env python3
"""K3D2 adapter entrypoint with one exact-pin anchor recovery.

The parent transformer remains the source of all physics/source edits. This
entrypoint changes only the matching strategy for the upstream SCF initial-
condition documentation block discovered by the first fail-closed CI run.
No frozen equation, sign, parameter, threshold, or scope gate is changed.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE / "k3d2_apply_class_two_field_adapter.py"
spec = importlib.util.spec_from_file_location("k3d2_parent", PARENT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)
_original_replace_once = mod.replace_once


def recovered_replace_once(root, rel, old, new, label):
    if label != "perturbations.c initial conditions":
        return _original_replace_once(root, rel, old, new, label)

    path = Path(root) / rel
    text = path.read_text(encoding="utf-8")
    marker = "      /* all relativistic relics: ur, early ncdm, dr */\n"
    count = text.count(marker)
    if count != 1:
        raise RuntimeError(f"{label}: recovery marker expected exactly once, found {count} in {rel}")
    insertion = """      /* KMDSB K3D2 independent field perturbations start unexcited. */
      if (pba->has_qcf == _TRUE_) {
        ppw->pv->y[ppw->pv->index_pt_phi_qcf] = 0.;
        ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf] = 0.;
      }
      if (pba->has_qpf == _TRUE_) {
        ppw->pv->y[ppw->pv->index_pt_psi_qpf] = 0.;
        ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf] = 0.;
      }

"""
    path.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")


mod.replace_once = recovered_replace_once
mod.main()
