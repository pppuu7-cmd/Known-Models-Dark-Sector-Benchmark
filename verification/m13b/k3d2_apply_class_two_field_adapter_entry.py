#!/usr/bin/env python3
"""K3D2 adapter entrypoint with exact-pin implementation-only recoveries.

The parent transformer remains the source of all physics/source edits. This
entrypoint changes only matching/guard/binding mechanics discovered by
fail-closed CI. No frozen equation, sign, parameter, threshold, or scope gate
is changed.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE / "k3d2_apply_class_two_field_adapter.py"
spec = importlib.util.spec_from_file_location("k3d2_parent", PARENT)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)
_original_replace_once = mod.replace_once
_original_patch_input_c = mod.patch_input_c


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


def recovered_patch_input_c(root):
    """Apply parent input patch, then bind direct-field reads before species budget.

    This is the prospectively frozen K3D2-B dynamic-budget recovery. Standard
    CLASS budget logic remains identical whenever qcf_U0=qpf_U0=0.
    """
    _original_patch_input_c(root)
    path = Path(root) / "source/input.c"
    text = path.read_text(encoding="utf-8")

    late_block = """  /* KMDSB K3D2 independent qcf+qpf input. */
  class_read_double("qcf_U0",pba->qcf_U0);
  class_read_double("qcf_phi_ini",pba->phi_ini_qcf);
  class_read_double("qcf_phi_prime_ini",pba->phi_prime_ini_qcf);
  class_read_double("qpf_U0",pba->qpf_U0);
  class_read_double("qpf_psi_ini",pba->psi_ini_qpf);
  class_read_double("qpf_psi_prime_ini",pba->psi_prime_ini_qpf);
  class_test(pba->qcf_U0 < 0.,errmsg,"qcf_U0 must be non-negative");
  class_test(pba->qpf_U0 < 0.,errmsg,"qpf_U0 must be non-negative");

"""
    if text.count(late_block) != 1:
        raise RuntimeError(f"K3D2 budget recovery: expected one late qcf/qpf read block, found {text.count(late_block)}")
    text = text.replace(late_block, "", 1)

    species_anchor = """  /** Read the parameters for each physical species (has to be called after the general read) */
  class_call(input_read_parameters_species(pfc,ppr,pba,pth,ppt,
                                           input_verbose,
                                           errmsg),
             errmsg,
             errmsg);
"""
    if text.count(species_anchor) != 1:
        raise RuntimeError(f"K3D2 budget recovery: expected one species-read anchor, found {text.count(species_anchor)}")
    early_block = """  /* KMDSB K3D2_DYNAMIC_BUDGET: direct-field inputs must be known before species budget. */
  class_read_double("qcf_U0",pba->qcf_U0);
  class_read_double("qcf_phi_ini",pba->phi_ini_qcf);
  class_read_double("qcf_phi_prime_ini",pba->phi_prime_ini_qcf);
  class_read_double("qpf_U0",pba->qpf_U0);
  class_read_double("qpf_psi_ini",pba->psi_ini_qpf);
  class_read_double("qpf_psi_prime_ini",pba->psi_prime_ini_qpf);
  class_test(pba->qcf_U0 < 0.,errmsg,"qcf_U0 must be non-negative");
  class_test(pba->qpf_U0 < 0.,errmsg,"qpf_U0 must be non-negative");

"""
    text = text.replace(species_anchor, early_block + species_anchor, 1)

    old_budget_test = """  class_test((flag1 == _TRUE_) && (flag2 == _TRUE_) && ((flag3 == _FALSE_) || (param3 >= 0.)),
             errmsg,
             "'Omega_Lambda' or 'Omega_fld' must be left unspecified, except if 'Omega_scf' is set and < 0.");
"""
    new_budget_test = """  class_test((flag1 == _TRUE_) && (flag2 == _TRUE_) && ((flag3 == _FALSE_) || (param3 >= 0.)) &&
             !((pba->qcf_U0 != 0.) || (pba->qpf_U0 != 0.)),
             errmsg,
             "'Omega_Lambda' or 'Omega_fld' must be left unspecified, except if 'Omega_scf' is set and < 0.");
"""
    if text.count(old_budget_test) != 1:
        raise RuntimeError(f"K3D2 budget recovery: expected one upstream budget guard, found {text.count(old_budget_test)}")
    text = text.replace(old_budget_test, new_budget_test, 1)
    path.write_text(text, encoding="utf-8")


def protected_upstream_scf_digest(root, rel):
    """Hash old upstream SCF-bearing lines, excluding newly added KMDSB marker lines."""
    text = (Path(root) / rel).read_text(encoding="utf-8")
    payload = "\n".join(
        line for line in text.splitlines()
        if "scf" in line and "KMDSB K3D2" not in line
    ) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


mod.replace_once = recovered_replace_once
mod.patch_input_c = recovered_patch_input_c
mod.digest_scf_lines = protected_upstream_scf_digest
mod.main()
