#!/usr/bin/env python3
"""K3D2 adapter entrypoint with exact-pin prospectively frozen recoveries.

The parent transformer remains the source of the qcf/qpf species equations.
This entrypoint applies only recovery mechanics that were frozen after
fail-closed diagnostics: exact source anchors, early input/budget binding, and
the z=5 IVP handoff needed to embed the already frozen K3C1/K3C2 realization
inside CLASS's earlier cosmological integration. No acceptance threshold or
post-handoff qcf/qpf equation is changed.
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
_original_patch_background_c = mod.patch_background_c
_original_patch_perturbations_c = mod.patch_perturbations_c


def replace_exact(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one recovery anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


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
    """Bind direct-field inputs before the upstream species-budget parser."""
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


def recovered_patch_background_c(root):
    """Apply parent qcf/qpf background patch then embed the z=5 IVP handoff."""
    _original_patch_background_c(root)
    path = Path(root) / "source/background.c"

    old_pressure = """  if (pba->has_qcf == _TRUE_) {
    pvecback[pba->index_bg_p_prime_qcf] = pvecback[pba->index_bg_phi_prime_qcf]*
      (-pvecback[pba->index_bg_phi_prime_qcf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_qcf]);
    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_qcf];
  }
  if (pba->has_qpf == _TRUE_) {
    pvecback[pba->index_bg_p_prime_qpf] = pvecback[pba->index_bg_psi_prime_qpf]*
      (pvecback[pba->index_bg_psi_prime_qpf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_qpf]);
    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_qpf];
  }
"""
    new_pressure = """  if (pba->has_qcf == _TRUE_) {
    /* KMDSB K3D2_Z5_HANDOFF: frozen K3C1 IVP before a=1/6. */
    if (a < 1./6.)
      pvecback[pba->index_bg_p_prime_qcf] = 0.;
    else
      pvecback[pba->index_bg_p_prime_qcf] = pvecback[pba->index_bg_phi_prime_qcf]*
        (-pvecback[pba->index_bg_phi_prime_qcf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_qcf]);
    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_qcf];
  }
  if (pba->has_qpf == _TRUE_) {
    /* KMDSB K3D2_Z5_HANDOFF: frozen K3C1 IVP before a=1/6. */
    if (a < 1./6.)
      pvecback[pba->index_bg_p_prime_qpf] = 0.;
    else
      pvecback[pba->index_bg_p_prime_qpf] = pvecback[pba->index_bg_psi_prime_qpf]*
        (pvecback[pba->index_bg_psi_prime_qpf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_qpf]);
    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_qpf];
  }
"""
    replace_exact(path, old_pressure, new_pressure, "K3D2 z5 pressure derivative handoff")

    old_rhs = """  if (pba->has_qcf == _TRUE_) {
    dy[pba->index_bi_phi_qcf] = y[pba->index_bi_phi_prime_qcf]/a/H;
    dy[pba->index_bi_phi_prime_qcf] = -2.*y[pba->index_bi_phi_prime_qcf] - a*dV_qcf(pba,y[pba->index_bi_phi_qcf])/H;
  }
  if (pba->has_qpf == _TRUE_) {
    dy[pba->index_bi_psi_qpf] = y[pba->index_bi_psi_prime_qpf]/a/H;
    dy[pba->index_bi_psi_prime_qpf] = -2.*y[pba->index_bi_psi_prime_qpf] + a*dV_qpf(pba,y[pba->index_bi_psi_qpf])/H;
  }
"""
    new_rhs = """  if (pba->has_qcf == _TRUE_) {
    /* KMDSB K3D2_Z5_HANDOFF: embed the frozen z=5 K3C1 IVP exactly. */
    if (a < 1./6.) {
      dy[pba->index_bi_phi_qcf] = 0.;
      dy[pba->index_bi_phi_prime_qcf] = 0.;
    }
    else {
      dy[pba->index_bi_phi_qcf] = y[pba->index_bi_phi_prime_qcf]/a/H;
      dy[pba->index_bi_phi_prime_qcf] = -2.*y[pba->index_bi_phi_prime_qcf] - a*dV_qcf(pba,y[pba->index_bi_phi_qcf])/H;
    }
  }
  if (pba->has_qpf == _TRUE_) {
    /* KMDSB K3D2_Z5_HANDOFF: embed the frozen z=5 K3C1 IVP exactly. */
    if (a < 1./6.) {
      dy[pba->index_bi_psi_qpf] = 0.;
      dy[pba->index_bi_psi_prime_qpf] = 0.;
    }
    else {
      dy[pba->index_bi_psi_qpf] = y[pba->index_bi_psi_prime_qpf]/a/H;
      dy[pba->index_bi_psi_prime_qpf] = -2.*y[pba->index_bi_psi_prime_qpf] + a*dV_qpf(pba,y[pba->index_bi_psi_qpf])/H;
    }
  }
"""
    replace_exact(path, old_rhs, new_rhs, "K3D2 z5 background RHS handoff")


def recovered_patch_perturbations_c(root):
    """Apply parent perturbation patch then freeze qcf/qpf modes before z=5."""
    _original_patch_perturbations_c(root)
    path = Path(root) / "source/perturbations.c"
    old_rhs = """    /** - ---> KMDSB K3D2 canonical qcf */
    if (pba->has_qcf == _TRUE_) {
      dy[pv->index_pt_phi_qcf] = y[pv->index_pt_phi_prime_qcf];
      dy[pv->index_pt_phi_prime_qcf] = -2.*a_prime_over_a*y[pv->index_pt_phi_prime_qcf]
        - metric_continuity*pvecback[pba->index_bg_phi_prime_qcf]
        - (k2 + a2*pvecback[pba->index_bg_ddV_qcf])*y[pv->index_pt_phi_qcf];
    }

    /** - ---> KMDSB K3D2 phantom qpf */
    if (pba->has_qpf == _TRUE_) {
      dy[pv->index_pt_psi_qpf] = y[pv->index_pt_psi_prime_qpf];
      dy[pv->index_pt_psi_prime_qpf] = -2.*a_prime_over_a*y[pv->index_pt_psi_prime_qpf]
        - metric_continuity*pvecback[pba->index_bg_psi_prime_qpf]
        - (k2 - a2*pvecback[pba->index_bg_ddV_qpf])*y[pv->index_pt_psi_qpf];
    }
"""
    new_rhs = """    /** - ---> KMDSB K3D2 canonical qcf */
    if (pba->has_qcf == _TRUE_) {
      /* KMDSB K3D2_Z5_HANDOFF: direct perturbations start at the K3C2 z=5 IVP. */
      if (a < 1./6.) {
        dy[pv->index_pt_phi_qcf] = 0.;
        dy[pv->index_pt_phi_prime_qcf] = 0.;
      }
      else {
        dy[pv->index_pt_phi_qcf] = y[pv->index_pt_phi_prime_qcf];
        dy[pv->index_pt_phi_prime_qcf] = -2.*a_prime_over_a*y[pv->index_pt_phi_prime_qcf]
          - metric_continuity*pvecback[pba->index_bg_phi_prime_qcf]
          - (k2 + a2*pvecback[pba->index_bg_ddV_qcf])*y[pv->index_pt_phi_qcf];
      }
    }

    /** - ---> KMDSB K3D2 phantom qpf */
    if (pba->has_qpf == _TRUE_) {
      /* KMDSB K3D2_Z5_HANDOFF: direct perturbations start at the K3C2 z=5 IVP. */
      if (a < 1./6.) {
        dy[pv->index_pt_psi_qpf] = 0.;
        dy[pv->index_pt_psi_prime_qpf] = 0.;
      }
      else {
        dy[pv->index_pt_psi_qpf] = y[pv->index_pt_psi_prime_qpf];
        dy[pv->index_pt_psi_prime_qpf] = -2.*a_prime_over_a*y[pv->index_pt_psi_prime_qpf]
          - metric_continuity*pvecback[pba->index_bg_psi_prime_qpf]
          - (k2 - a2*pvecback[pba->index_bg_ddV_qpf])*y[pv->index_pt_psi_qpf];
      }
    }
"""
    replace_exact(path, old_rhs, new_rhs, "K3D2 z5 perturbation RHS handoff")


def protected_upstream_scf_digest(root, rel):
    """Hash old upstream SCF-bearing lines, excluding new KMDSB marker lines."""
    text = (Path(root) / rel).read_text(encoding="utf-8")
    payload = "\n".join(
        line for line in text.splitlines()
        if "scf" in line and "KMDSB K3D2" not in line
    ) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


mod.replace_once = recovered_replace_once
mod.patch_input_c = recovered_patch_input_c
mod.patch_background_c = recovered_patch_background_c
mod.patch_perturbations_c = recovered_patch_perturbations_c
mod.digest_scf_lines = protected_upstream_scf_digest
mod.main()
