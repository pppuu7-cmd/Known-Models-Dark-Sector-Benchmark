#!/usr/bin/env python3
"""Apply the prospectively frozen M13b K3D2 qcf+qpf adapter to exact-pin CLASS.

This is a deterministic fail-closed source transformer. It is intentionally
restricted to the five files authorized by the K3D2 preregistration/amendment.
Existing upstream scf-bearing lines must remain byte-identical as an ordered
sequence after the transformation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

CLASS_PIN = "64bbab707faf4de4779a9e04edd180fef18d98fa"
U0 = "0.3362232603714306"
ALLOWED = [
    "include/background.h",
    "source/background.c",
    "source/input.c",
    "include/perturbations.h",
    "source/perturbations.c",
]


def digest_scf_lines(root: Path, rel: str) -> str:
    text = (root / rel).read_text(encoding="utf-8")
    payload = "\n".join(line for line in text.splitlines() if "scf" in line) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def replace_once(root: Path, rel: str, old: str, new: str, label: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one source anchor, found {count} in {rel}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(root: Path, rel: str, marker: str, payload: str, label: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    if marker in text:
        raise RuntimeError(f"{label}: marker already present in {rel}")
    path.write_text(text.rstrip() + "\n\n" + payload.rstrip() + "\n", encoding="utf-8")


def patch_background_h(root: Path) -> None:
    rel = "include/background.h"
    old = """  double * scf_parameters; /**< list of parameters describing the scalar field potential */
  short attractor_ic_scf;  /**< whether the scalar field has attractor initial conditions */
  int scf_tuning_index;    /**< index in scf_parameters used for tuning */
  double phi_ini_scf;      /**< \\f$ \\phi(t_0) \\f$: scalar field initial value */
  double phi_prime_ini_scf;/**< \\f$ d\\phi(t_0)/d\\tau \\f$: scalar field initial derivative wrt conformal time */
  int scf_parameters_size; /**< size of scf_parameters */
"""
    new = old + """
  /* KMDSB K3D2 independent direct-field adapter parameters. */
  double qcf_U0;
  double phi_ini_qcf;
  double phi_prime_ini_qcf;
  double qpf_U0;
  double psi_ini_qpf;
  double psi_prime_ini_qpf;
"""
    replace_once(root, rel, old, new, "background.h adapter parameters")

    old = """  int index_bg_phi_scf;       /**< scalar field value */
  int index_bg_phi_prime_scf; /**< scalar field derivative wrt conformal time */
  int index_bg_V_scf;         /**< scalar field potential V */
  int index_bg_dV_scf;        /**< scalar field potential derivative V' */
  int index_bg_ddV_scf;       /**< scalar field potential second derivative V'' */
  int index_bg_rho_scf;       /**< scalar field energy density */
  int index_bg_p_scf;         /**< scalar field pressure */
  int index_bg_p_prime_scf;         /**< scalar field pressure */
"""
    new = old + """
  int index_bg_phi_qcf;
  int index_bg_phi_prime_qcf;
  int index_bg_V_qcf;
  int index_bg_dV_qcf;
  int index_bg_ddV_qcf;
  int index_bg_rho_qcf;
  int index_bg_p_qcf;
  int index_bg_p_prime_qcf;

  int index_bg_psi_qpf;
  int index_bg_psi_prime_qpf;
  int index_bg_V_qpf;
  int index_bg_dV_qpf;
  int index_bg_ddV_qpf;
  int index_bg_rho_qpf;
  int index_bg_p_qpf;
  int index_bg_p_prime_qpf;
"""
    replace_once(root, rel, old, new, "background.h normal indices")

    old = """  int index_bi_phi_scf;       /**< {B} scalar field value */
  int index_bi_phi_prime_scf; /**< {B} scalar field derivative wrt conformal time */
"""
    new = old + """
  int index_bi_phi_qcf;
  int index_bi_phi_prime_qcf;
  int index_bi_psi_qpf;
  int index_bi_psi_prime_qpf;
"""
    replace_once(root, rel, old, new, "background.h integration indices")

    old = """  short has_scf;       /**< presence of a scalar field? */
"""
    new = old + """  short has_qcf;       /**< KMDSB independent canonical direct field? */
  short has_qpf;       /**< KMDSB independent phantom direct field? */
"""
    replace_once(root, rel, old, new, "background.h flags")

    old = """  double ddV_scf(
                 struct background *pba,
                 double phi
                 );
"""
    new = old + """
  double V_qcf(struct background *pba,double phi);
  double dV_qcf(struct background *pba,double phi);
  double ddV_qcf(struct background *pba,double phi);
  double V_qpf(struct background *pba,double psi);
  double dV_qpf(struct background *pba,double psi);
  double ddV_qpf(struct background *pba,double psi);
"""
    replace_once(root, rel, old, new, "background.h potential prototypes")


def patch_background_c(root: Path) -> None:
    rel = "source/background.c"
    old = """  /* scalar field quantities */
  double phi, phi_prime;
"""
    new = old + """  double phi_qcf, phi_prime_qcf;
  double psi_qpf, psi_prime_qpf;
"""
    replace_once(root, rel, old, new, "background.c locals")

    old = """  /* Scalar field */
  if (pba->has_scf == _TRUE_) {
    phi = pvecback_B[pba->index_bi_phi_scf];
    phi_prime = pvecback_B[pba->index_bi_phi_prime_scf];
    pvecback[pba->index_bg_phi_scf] = phi; // value of the scalar field phi
    pvecback[pba->index_bg_phi_prime_scf] = phi_prime; // value of the scalar field phi derivative wrt conformal time
    pvecback[pba->index_bg_V_scf] = V_scf(pba,phi); //V_scf(pba,phi); //write here potential as function of phi
    pvecback[pba->index_bg_dV_scf] = dV_scf(pba,phi); // dV_scf(pba,phi); //potential' as function of phi
    pvecback[pba->index_bg_ddV_scf] = ddV_scf(pba,phi); // ddV_scf(pba,phi); //potential'' as function of phi
    pvecback[pba->index_bg_rho_scf] = (phi_prime*phi_prime/(2*a*a) + V_scf(pba,phi))/3.; // energy of the scalar field. The field units are set automatically by setting the initial conditions
    pvecback[pba->index_bg_p_scf] =(phi_prime*phi_prime/(2*a*a) - V_scf(pba,phi))/3.; // pressure of the scalar field
    rho_tot += pvecback[pba->index_bg_rho_scf];
    p_tot += pvecback[pba->index_bg_p_scf];
    dp_dloga += 0.0; /** <-- This depends on a_prime_over_a, so we cannot add it now! */
    //divide relativistic & nonrelativistic (not very meaningful for oscillatory models)
    rho_r += 3.*pvecback[pba->index_bg_p_scf]; //field pressure contributes radiation
    rho_m += pvecback[pba->index_bg_rho_scf] - 3.* pvecback[pba->index_bg_p_scf]; //the rest contributes matter
    //printf(" a= %e, Omega_scf = %f, \\n ",a, pvecback[pba->index_bg_rho_scf]/rho_tot );
  }
"""
    # The upstream printf comment is line-wrapped differently in the exact source; use a shorter exact anchor.
    old = """  /* Scalar field */
  if (pba->has_scf == _TRUE_) {
    phi = pvecback_B[pba->index_bi_phi_scf];
    phi_prime = pvecback_B[pba->index_bi_phi_prime_scf];
    pvecback[pba->index_bg_phi_scf] = phi; // value of the scalar field phi
    pvecback[pba->index_bg_phi_prime_scf] = phi_prime; // value of the scalar field phi derivative wrt conformal time
    pvecback[pba->index_bg_V_scf] = V_scf(pba,phi); //V_scf(pba,phi); //write here potential as function of phi
    pvecback[pba->index_bg_dV_scf] = dV_scf(pba,phi); // dV_scf(pba,phi); //potential' as function of phi
    pvecback[pba->index_bg_ddV_scf] = ddV_scf(pba,phi); // ddV_scf(pba,phi); //potential'' as function of phi
    pvecback[pba->index_bg_rho_scf] = (phi_prime*phi_prime/(2*a*a) + V_scf(pba,phi))/3.; // energy of the scalar field. The field units are set automatically by setting the initial conditions
    pvecback[pba->index_bg_p_scf] =(phi_prime*phi_prime/(2*a*a) - V_scf(pba,phi))/3.; // pressure of the scalar field
    rho_tot += pvecback[pba->index_bg_rho_scf];
    p_tot += pvecback[pba->index_bg_p_scf];
    dp_dloga += 0.0; /** <-- This depends on a_prime_over_a, so we cannot add it now! */
    //divide relativistic & nonrelativistic (not very meaningful for oscillatory models)
    rho_r += 3.*pvecback[pba->index_bg_p_scf]; //field pressure contributes radiation
    rho_m += pvecback[pba->index_bg_rho_scf] - 3.* pvecback[pba->index_bg_p_scf]; //the rest contributes matter
    //printf(" a= %e, Omega_scf = %f, \\n ",a, pvecback[pba->index_bg_rho_scf]/rho_tot );
  }

  /* ncdm */
""".replace('//printf(" a= %e, Omega_scf = %f, \\\n ",a, pvecback[pba->index_bg_rho_scf]/rho_tot );', '//printf(" a= %e, Omega_scf = %f, \\n ",a, pvecback[pba->index_bg_rho_scf]/rho_tot );')
    new = old.replace("\n\n  /* ncdm */\n", "") + """

  /* KMDSB K3D2 independent canonical qcf field. */
  if (pba->has_qcf == _TRUE_) {
    phi_qcf = pvecback_B[pba->index_bi_phi_qcf];
    phi_prime_qcf = pvecback_B[pba->index_bi_phi_prime_qcf];
    pvecback[pba->index_bg_phi_qcf] = phi_qcf;
    pvecback[pba->index_bg_phi_prime_qcf] = phi_prime_qcf;
    pvecback[pba->index_bg_V_qcf] = V_qcf(pba,phi_qcf);
    pvecback[pba->index_bg_dV_qcf] = dV_qcf(pba,phi_qcf);
    pvecback[pba->index_bg_ddV_qcf] = ddV_qcf(pba,phi_qcf);
    pvecback[pba->index_bg_rho_qcf] = (phi_prime_qcf*phi_prime_qcf/(2*a*a) + V_qcf(pba,phi_qcf))/3.;
    pvecback[pba->index_bg_p_qcf] = (phi_prime_qcf*phi_prime_qcf/(2*a*a) - V_qcf(pba,phi_qcf))/3.;
    rho_tot += pvecback[pba->index_bg_rho_qcf];
    p_tot += pvecback[pba->index_bg_p_qcf];
  }

  /* KMDSB K3D2 independent phantom qpf field. */
  if (pba->has_qpf == _TRUE_) {
    psi_qpf = pvecback_B[pba->index_bi_psi_qpf];
    psi_prime_qpf = pvecback_B[pba->index_bi_psi_prime_qpf];
    pvecback[pba->index_bg_psi_qpf] = psi_qpf;
    pvecback[pba->index_bg_psi_prime_qpf] = psi_prime_qpf;
    pvecback[pba->index_bg_V_qpf] = V_qpf(pba,psi_qpf);
    pvecback[pba->index_bg_dV_qpf] = dV_qpf(pba,psi_qpf);
    pvecback[pba->index_bg_ddV_qpf] = ddV_qpf(pba,psi_qpf);
    pvecback[pba->index_bg_rho_qpf] = (-psi_prime_qpf*psi_prime_qpf/(2*a*a) + V_qpf(pba,psi_qpf))/3.;
    pvecback[pba->index_bg_p_qpf] = (-psi_prime_qpf*psi_prime_qpf/(2*a*a) - V_qpf(pba,psi_qpf))/3.;
    rho_tot += pvecback[pba->index_bg_rho_qpf];
    p_tot += pvecback[pba->index_bg_p_qpf];
  }

  /* ncdm */
"""
    replace_once(root, rel, old, new, "background.c stress energy")

    old = """  if (pba->has_scf == _TRUE_) {
    /** The contribution of scf was not added to dp_dloga, add p_scf_prime here: */
    pvecback[pba->index_bg_p_prime_scf] = pvecback[pba->index_bg_phi_prime_scf]*
      (-pvecback[pba->index_bg_phi_prime_scf]*pvecback[pba->index_bg_H]/a-2./3.*pvecback[pba->index_bg_dV_scf]);
    pvecback[pba->index_bg_p_tot_prime] += pvecback[pba->index_bg_p_prime_scf];
  }
"""
    new = old + """  if (pba->has_qcf == _TRUE_) {
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
    replace_once(root, rel, old, new, "background.c pressure derivative")

    old = """  pba->has_scf = _FALSE_;
"""
    new = old + """  pba->has_qcf = _FALSE_;
  pba->has_qpf = _FALSE_;
"""
    replace_once(root, rel, old, new, "background.c flag defaults")

    old = """  if (pba->Omega0_scf != 0.)
    pba->has_scf = _TRUE_;
"""
    new = old + """
  if (pba->qcf_U0 != 0.)
    pba->has_qcf = _TRUE_;

  if (pba->qpf_U0 != 0.)
    pba->has_qpf = _TRUE_;
"""
    replace_once(root, rel, old, new, "background.c active flags")

    old = """  class_define_index(pba->index_bg_phi_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_phi_prime_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_V_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_dV_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_ddV_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_rho_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_p_scf,pba->has_scf,index_bg,1);
  class_define_index(pba->index_bg_p_prime_scf,pba->has_scf,index_bg,1);
"""
    new = old + """
  class_define_index(pba->index_bg_phi_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_phi_prime_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_V_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_dV_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_ddV_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_rho_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_p_qcf,pba->has_qcf,index_bg,1);
  class_define_index(pba->index_bg_p_prime_qcf,pba->has_qcf,index_bg,1);

  class_define_index(pba->index_bg_psi_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_psi_prime_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_V_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_dV_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_ddV_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_rho_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_p_qpf,pba->has_qpf,index_bg,1);
  class_define_index(pba->index_bg_p_prime_qpf,pba->has_qpf,index_bg,1);
"""
    replace_once(root, rel, old, new, "background.c normal indices")

    old = """  class_define_index(pba->index_bi_phi_scf,pba->has_scf,index_bi,1);
  class_define_index(pba->index_bi_phi_prime_scf,pba->has_scf,index_bi,1);
"""
    new = old + """  class_define_index(pba->index_bi_phi_qcf,pba->has_qcf,index_bi,1);
  class_define_index(pba->index_bi_phi_prime_qcf,pba->has_qcf,index_bi,1);
  class_define_index(pba->index_bi_psi_qpf,pba->has_qpf,index_bi,1);
  class_define_index(pba->index_bi_psi_prime_qpf,pba->has_qpf,index_bi,1);
"""
    replace_once(root, rel, old, new, "background.c integration indices")

    old = """  if (pba->has_scf == _TRUE_) {
    scf_lambda = pba->scf_parameters[0];
    if (pba->attractor_ic_scf == _TRUE_) {
      pvecback_integration[pba->index_bi_phi_scf] = -1/scf_lambda*
        log(rho_rad*4./(3*pow(scf_lambda,2)-12))*pba->phi_ini_scf;
      if (3.*pow(scf_lambda,2)-12. < 0) {
        /** - --> If there is no attractor solution for scf_lambda, assign some value. Otherwise would give a nan.*/
        pvecback_integration[pba->index_bi_phi_scf] = 1./scf_lambda;//seems to do the work
        if (pba->background_verbose > 0) {
          printf(" No attractor IC for lambda = %.3e ! \\n ",scf_lambda);
        }
      }
      pvecback_integration[pba->index_bi_phi_prime_scf] = 2.*a*sqrt(V_scf(pba,pvecback_integration[pba->index_bi_phi_scf]))*pba->phi_prime_ini_scf;
    }
    else {
      printf("Not using attractor initial conditions\\n");
      /** - --> If no attractor initial conditions are assigned, gets the provided ones. */
      pvecback_integration[pba->index_bi_phi_scf] = pba->phi_ini_scf;
      pvecback_integration[pba->index_bi_phi_prime_scf] = pba->phi_prime_ini_scf;
    }
    class_test(!isfinite(pvecback_integration[pba->index_bi_phi_scf]) ||
               !isfinite(pvecback_integration[pba->index_bi_phi_scf]),
               pba->error_message,
               "initial phi = %e phi_prime = %e -> check initial conditions",
               pvecback_integration[pba->index_bi_phi_scf],
               pvecback_integration[pba->index_bi_phi_scf]);
  }
""".replace('printf(" No attractor IC for lambda = %.3e ! \\\n ",scf_lambda);','printf(" No attractor IC for lambda = %.3e ! \\n ",scf_lambda);')
    new = old + """
  if (pba->has_qcf == _TRUE_) {
    pvecback_integration[pba->index_bi_phi_qcf] = pba->phi_ini_qcf;
    pvecback_integration[pba->index_bi_phi_prime_qcf] = pba->phi_prime_ini_qcf;
  }
  if (pba->has_qpf == _TRUE_) {
    pvecback_integration[pba->index_bi_psi_qpf] = pba->psi_ini_qpf;
    pvecback_integration[pba->index_bi_psi_prime_qpf] = pba->psi_prime_ini_qpf;
  }
"""
    replace_once(root, rel, old, new, "background.c independent initial conditions")

    old = """  if (pba->has_scf == _TRUE_) {
    /** - Scalar field equation: \\f$ \\phi'' + 2 a H \\phi' + a^2 dV = 0 \\f$  (note H is wrt cosmological time)
        written as \\f$ d\\phi/dlna = phi' / (aH) \\f$ and \\f$ d\\phi'/dlna = -2*phi' - (a/H) dV \\f$ */
    dy[pba->index_bi_phi_scf] = y[pba->index_bi_phi_prime_scf]/a/H;
    dy[pba->index_bi_phi_prime_scf] = - 2*y[pba->index_bi_phi_prime_scf] - a*dV_scf(pba,y[pba->index_bi_phi_scf])/H ;
  }
"""
    new = old + """
  if (pba->has_qcf == _TRUE_) {
    dy[pba->index_bi_phi_qcf] = y[pba->index_bi_phi_prime_qcf]/a/H;
    dy[pba->index_bi_phi_prime_qcf] = -2.*y[pba->index_bi_phi_prime_qcf] - a*dV_qcf(pba,y[pba->index_bi_phi_qcf])/H;
  }
  if (pba->has_qpf == _TRUE_) {
    dy[pba->index_bi_psi_qpf] = y[pba->index_bi_psi_prime_qpf]/a/H;
    dy[pba->index_bi_psi_prime_qpf] = -2.*y[pba->index_bi_psi_prime_qpf] + a*dV_qpf(pba,y[pba->index_bi_psi_qpf])/H;
  }
"""
    replace_once(root, rel, old, new, "background.c field derivatives")

    old = """  class_store_columntitle(titles,"(.)rho_scf",pba->has_scf);
  class_store_columntitle(titles,"(.)p_scf",pba->has_scf);
  class_store_columntitle(titles,"(.)p_prime_scf",pba->has_scf);
  class_store_columntitle(titles,"phi_scf",pba->has_scf);
  class_store_columntitle(titles,"phi'_scf",pba->has_scf);
  class_store_columntitle(titles,"V_scf",pba->has_scf);
  class_store_columntitle(titles,"V'_scf",pba->has_scf);
  class_store_columntitle(titles,"V''_scf",pba->has_scf);
"""
    new = old + """  class_store_columntitle(titles,"(.)rho_qcf",pba->has_qcf);
  class_store_columntitle(titles,"(.)p_qcf",pba->has_qcf);
  class_store_columntitle(titles,"(.)p_prime_qcf",pba->has_qcf);
  class_store_columntitle(titles,"phi_qcf",pba->has_qcf);
  class_store_columntitle(titles,"phi'_qcf",pba->has_qcf);
  class_store_columntitle(titles,"V_qcf",pba->has_qcf);
  class_store_columntitle(titles,"V'_qcf",pba->has_qcf);
  class_store_columntitle(titles,"V''_qcf",pba->has_qcf);
  class_store_columntitle(titles,"(.)rho_qpf",pba->has_qpf);
  class_store_columntitle(titles,"(.)p_qpf",pba->has_qpf);
  class_store_columntitle(titles,"(.)p_prime_qpf",pba->has_qpf);
  class_store_columntitle(titles,"psi_qpf",pba->has_qpf);
  class_store_columntitle(titles,"psi'_qpf",pba->has_qpf);
  class_store_columntitle(titles,"V_qpf",pba->has_qpf);
  class_store_columntitle(titles,"V'_qpf",pba->has_qpf);
  class_store_columntitle(titles,"V''_qpf",pba->has_qpf);
"""
    replace_once(root, rel, old, new, "background.c output titles")

    old = """    class_store_double(dataptr,pvecback[pba->index_bg_rho_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_p_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_p_prime_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_phi_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_phi_prime_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_V_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_dV_scf],pba->has_scf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_ddV_scf],pba->has_scf,storeidx);
"""
    new = old + """    class_store_double(dataptr,pvecback[pba->index_bg_rho_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_p_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_p_prime_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_phi_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_phi_prime_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_V_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_dV_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_ddV_qcf],pba->has_qcf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_rho_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_p_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_p_prime_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_psi_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_psi_prime_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_V_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_dV_qpf],pba->has_qpf,storeidx);
    class_store_double(dataptr,pvecback[pba->index_bg_ddV_qpf],pba->has_qpf,storeidx);
"""
    replace_once(root, rel, old, new, "background.c output values")

    payload = f"""/* KMDSB K3D2 independent qcf+qpf tanh potentials.
   Frozen map: V_class=3 H0^2 U and U0={U0}. */
static double k3d2_tanh_V(struct background *pba,double x,double u0) {{
  double th=tanh(29.*(1.-x));
  return 3.*pba->H0*pba->H0*u0*(th+1.);
}}
static double k3d2_tanh_dV(struct background *pba,double x,double u0) {{
  double th=tanh(29.*(1.-x));
  double sech2=1.-th*th;
  return -3.*pba->H0*pba->H0*u0*29.*sech2;
}}
static double k3d2_tanh_ddV(struct background *pba,double x,double u0) {{
  double th=tanh(29.*(1.-x));
  double sech2=1.-th*th;
  return -6.*pba->H0*pba->H0*u0*29.*29.*sech2*th;
}}
double V_qcf(struct background *pba,double phi) {{ return k3d2_tanh_V(pba,phi,pba->qcf_U0); }}
double dV_qcf(struct background *pba,double phi) {{ return k3d2_tanh_dV(pba,phi,pba->qcf_U0); }}
double ddV_qcf(struct background *pba,double phi) {{ return k3d2_tanh_ddV(pba,phi,pba->qcf_U0); }}
double V_qpf(struct background *pba,double psi) {{ return k3d2_tanh_V(pba,psi,pba->qpf_U0); }}
double dV_qpf(struct background *pba,double psi) {{ return k3d2_tanh_dV(pba,psi,pba->qpf_U0); }}
double ddV_qpf(struct background *pba,double psi) {{ return k3d2_tanh_ddV(pba,psi,pba->qpf_U0); }}
"""
    append_once(root, rel, "KMDSB K3D2 independent qcf+qpf tanh potentials", payload, "background.c potential append")


def patch_input_c(root: Path) -> None:
    rel = "source/input.c"
    old = """  /** 9.b.3) Tuning parameter */
  pba->scf_tuning_index = 0;
"""
    new = old + f"""
  /* KMDSB K3D2 independent adapter defaults: absent unless U0 is nonzero. */
  pba->qcf_U0 = 0.;
  pba->phi_ini_qcf = 0.92;
  pba->phi_prime_ini_qcf = 0.;
  pba->qpf_U0 = 0.;
  pba->psi_ini_qpf = 1.02;
  pba->psi_prime_ini_qpf = 0.;
"""
    replace_once(root, rel, old, new, "input.c defaults")

    anchor = """  return _SUCCESS_;

}


/**
 * Read the parameters of injection structure
"""
    insert = """  /* KMDSB K3D2 independent qcf+qpf input. */
  class_read_double("qcf_U0",pba->qcf_U0);
  class_read_double("qcf_phi_ini",pba->phi_ini_qcf);
  class_read_double("qcf_phi_prime_ini",pba->phi_prime_ini_qcf);
  class_read_double("qpf_U0",pba->qpf_U0);
  class_read_double("qpf_psi_ini",pba->psi_ini_qpf);
  class_read_double("qpf_psi_prime_ini",pba->psi_prime_ini_qpf);
  class_test(pba->qcf_U0 < 0.,errmsg,"qcf_U0 must be non-negative");
  class_test(pba->qpf_U0 < 0.,errmsg,"qpf_U0 must be non-negative");

"""
    replace_once(root, rel, anchor, insert + anchor, "input.c reads")


def patch_perturbations_h(root: Path) -> None:
    rel = "include/perturbations.h"
    old = """  int index_pt_phi_scf;  /**< scalar field density */
  int index_pt_phi_prime_scf;  /**< scalar field velocity */
"""
    new = old + """  int index_pt_phi_qcf;
  int index_pt_phi_prime_qcf;
  int index_pt_psi_qpf;
  int index_pt_psi_prime_qpf;
"""
    replace_once(root, rel, old, new, "perturbations.h state indices")


def patch_perturbations_c(root: Path) -> None:
    rel = "source/perturbations.c"

    old = """  class_test((ppt->gauge == synchronous) && (pba->has_cdm == _FALSE_),
             ppt->error_message,
             "In the synchronous gauge, it is not self-consistent to assume no CDM: the later is used to define the initial timelike hypersurface. You can either add a negligible amount of CDM, or switch to newtonian gauge");
"""
    new = old + """
  class_test(((pba->has_qcf == _TRUE_) || (pba->has_qpf == _TRUE_)) && (ppt->gauge != synchronous),
             ppt->error_message,
             "KMDSB K3D2 qcf/qpf adapter is prospectively restricted to synchronous evolution; upstream newtonian scf is not reused as authority");
"""
    replace_once(root, rel, old, new, "perturbations.c gauge guard")

    old = """    class_define_index(ppv->index_pt_phi_scf,pba->has_scf,index_pt,1); /* scalar field density */
    class_define_index(ppv->index_pt_phi_prime_scf,pba->has_scf,index_pt,1); /* scalar field velocity */
"""
    new = old + """    class_define_index(ppv->index_pt_phi_qcf,pba->has_qcf,index_pt,1);
    class_define_index(ppv->index_pt_phi_prime_qcf,pba->has_qcf,index_pt,1);
    class_define_index(ppv->index_pt_psi_qpf,pba->has_qpf,index_pt,1);
    class_define_index(ppv->index_pt_psi_prime_qpf,pba->has_qpf,index_pt,1);
"""
    replace_once(root, rel, old, new, "perturbations.c state indices")

    old = """      if (pba->has_scf == _TRUE_) {

        ppv->y[ppv->index_pt_phi_scf] =
          ppw->pv->y[ppw->pv->index_pt_phi_scf];

        ppv->y[ppv->index_pt_phi_prime_scf] =
          ppw->pv->y[ppw->pv->index_pt_phi_prime_scf];
      }
"""
    new = old + """      if (pba->has_qcf == _TRUE_) {
        ppv->y[ppv->index_pt_phi_qcf] = ppw->pv->y[ppw->pv->index_pt_phi_qcf];
        ppv->y[ppv->index_pt_phi_prime_qcf] = ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf];
      }
      if (pba->has_qpf == _TRUE_) {
        ppv->y[ppv->index_pt_psi_qpf] = ppw->pv->y[ppw->pv->index_pt_psi_qpf];
        ppv->y[ppv->index_pt_psi_prime_qpf] = ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf];
      }
"""
    replace_once(root, rel, old, new, "perturbations.c approximation copy")

    old = """      if (pba->has_scf == _TRUE_) {
        /** - ---> Canonical field (solving for the perturbations):
         *  initial perturbations set to zero, they should reach the attractor soon enough.
         *  - --->  TODO: Incorporate the attractor IC from 1004.5509.
         *
         *  The field perturbations can in principle be obtained here via
         *  with \\f$ c_s^2 = 1 \\f$ and w = 1/3 (ASSUMES radiation TRACKING)
         */

        ppw->pv->y[ppw->pv->index_pt_phi_scf] = 0.;
        /*  a*a/k/k/ppw->pvecback[pba->index_bg_phi_prime_scf]*k*ktau_three/4.*1./(4.-6.*(1./3.)+3.*1.) * (ppw->pvecback[pba->index_bg_rho_scf] + ppw->pvecback[pba->index_bg_p_scf])* ppr->curvature_ini * s2_squared; */

        ppw->pv->y[ppw->pv->index_pt_phi_prime_scf] = 0.;
        /* delta_fld expression * rho_scf with the w = 1/3, c_s = 1
           a*a/ppw->pvecback[pba->index_bg_phi_prime_scf]*( - ktau_two/4.*(1.+1./3.)*(4.-3.*1.)/(4.-6.*(1/3.)+3.*1.)*ppw->pvecback[pba->index_bg_rho_scf] - ppw->pvecback[pba->index_bg_dV_scf]*ppw->pv->y[ppw->pv->index_pt_phi_scf])* ppr->curvature_ini * s2_squared; */
      }
"""
    new = old + """      if (pba->has_qcf == _TRUE_) {
        ppw->pv->y[ppw->pv->index_pt_phi_qcf] = 0.;
        ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf] = 0.;
      }
      if (pba->has_qpf == _TRUE_) {
        ppw->pv->y[ppw->pv->index_pt_psi_qpf] = 0.;
        ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf] = 0.;
      }
"""
    replace_once(root, rel, old, new, "perturbations.c initial conditions")

    old = """      /* scalar field: check */
      if (pba->has_scf == _TRUE_) {
        alpha_prime = 0.0;
        /* - 2. * a_prime_over_a * alpha + eta
           - 4.5 * (a2/k2) * ppw->rho_plus_p_shear; */

        ppw->pv->y[ppw->pv->index_pt_phi_scf] += alpha*ppw->pvecback[pba->index_bg_phi_prime_scf];
        ppw->pv->y[ppw->pv->index_pt_phi_prime_scf] +=
          (-2.*a_prime_over_a*alpha*ppw->pvecback[pba->index_bg_phi_prime_scf]
           -a*a* dV_scf(pba,ppw->pvecback[pba->index_bg_phi_scf])*alpha
           +ppw->pvecback[pba->index_bg_phi_prime_scf]*alpha_prime);
      }
"""
    new = old + """      if (pba->has_qcf == _TRUE_) {
        alpha_prime = 0.0;
        ppw->pv->y[ppw->pv->index_pt_phi_qcf] += alpha*ppw->pvecback[pba->index_bg_phi_prime_qcf];
        ppw->pv->y[ppw->pv->index_pt_phi_prime_qcf] +=
          (-2.*a_prime_over_a*alpha*ppw->pvecback[pba->index_bg_phi_prime_qcf]
           -a*a*dV_qcf(pba,ppw->pvecback[pba->index_bg_phi_qcf])*alpha
           +ppw->pvecback[pba->index_bg_phi_prime_qcf]*alpha_prime);
      }
      if (pba->has_qpf == _TRUE_) {
        alpha_prime = 0.0;
        ppw->pv->y[ppw->pv->index_pt_psi_qpf] += alpha*ppw->pvecback[pba->index_bg_psi_prime_qpf];
        ppw->pv->y[ppw->pv->index_pt_psi_prime_qpf] +=
          (-2.*a_prime_over_a*alpha*ppw->pvecback[pba->index_bg_psi_prime_qpf]
           +a*a*dV_qpf(pba,ppw->pvecback[pba->index_bg_psi_qpf])*alpha
           +ppw->pvecback[pba->index_bg_psi_prime_qpf]*alpha_prime);
      }
"""
    replace_once(root, rel, old, new, "perturbations.c gauge transform")

    old = """  double delta_rho_scf, delta_p_scf, psi;
"""
    new = old + """  double delta_rho_qcf, delta_p_qcf;
  double delta_rho_qpf, delta_p_qpf;
"""
    replace_once(root, rel, old, new, "perturbations.c stress locals")

    old = """      ppw->rho_plus_p_tot += ppw->pvecback[pba->index_bg_rho_scf]+ppw->pvecback[pba->index_bg_p_scf];

    }

    /* add your extra species here */
"""
    new = old.replace("\n    /* add your extra species here */\n", "") + """
    /* KMDSB K3D2 canonical qcf contribution. */
    if (pba->has_qcf == _TRUE_) {
      if (ppt->gauge == synchronous) {
        delta_rho_qcf = 1./3.*(ppw->pvecback[pba->index_bg_phi_prime_qcf]*y[ppw->pv->index_pt_phi_prime_qcf]/a2
                               +ppw->pvecback[pba->index_bg_dV_qcf]*y[ppw->pv->index_pt_phi_qcf]);
        delta_p_qcf = 1./3.*(ppw->pvecback[pba->index_bg_phi_prime_qcf]*y[ppw->pv->index_pt_phi_prime_qcf]/a2
                             -ppw->pvecback[pba->index_bg_dV_qcf]*y[ppw->pv->index_pt_phi_qcf]);
      }
      else {
        psi = y[ppw->pv->index_pt_phi] - 4.5*(a2/k/k)*ppw->rho_plus_p_shear;
        delta_rho_qcf = 1./3.*(ppw->pvecback[pba->index_bg_phi_prime_qcf]*y[ppw->pv->index_pt_phi_prime_qcf]/a2
                               +ppw->pvecback[pba->index_bg_dV_qcf]*y[ppw->pv->index_pt_phi_qcf]
                               -pow(ppw->pvecback[pba->index_bg_phi_prime_qcf],2)*psi/a2);
        delta_p_qcf = 1./3.*(ppw->pvecback[pba->index_bg_phi_prime_qcf]*y[ppw->pv->index_pt_phi_prime_qcf]/a2
                             -ppw->pvecback[pba->index_bg_dV_qcf]*y[ppw->pv->index_pt_phi_qcf]
                             -pow(ppw->pvecback[pba->index_bg_phi_prime_qcf],2)*psi/a2);
      }
      ppw->delta_rho += delta_rho_qcf;
      ppw->rho_plus_p_theta += 1./3.*k*k/a2*ppw->pvecback[pba->index_bg_phi_prime_qcf]*y[ppw->pv->index_pt_phi_qcf];
      ppw->delta_p += delta_p_qcf;
      ppw->rho_plus_p_tot += ppw->pvecback[pba->index_bg_rho_qcf]+ppw->pvecback[pba->index_bg_p_qcf];
    }

    /* KMDSB K3D2 phantom qpf contribution. */
    if (pba->has_qpf == _TRUE_) {
      if (ppt->gauge == synchronous) {
        delta_rho_qpf = 1./3.*(-ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_prime_qpf]/a2
                               +ppw->pvecback[pba->index_bg_dV_qpf]*y[ppw->pv->index_pt_psi_qpf]);
        delta_p_qpf = 1./3.*(-ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_prime_qpf]/a2
                             -ppw->pvecback[pba->index_bg_dV_qpf]*y[ppw->pv->index_pt_psi_qpf]);
      }
      else {
        psi = y[ppw->pv->index_pt_phi] - 4.5*(a2/k/k)*ppw->rho_plus_p_shear;
        delta_rho_qpf = 1./3.*(-ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_prime_qpf]/a2
                               +pow(ppw->pvecback[pba->index_bg_psi_prime_qpf],2)*psi/a2
                               +ppw->pvecback[pba->index_bg_dV_qpf]*y[ppw->pv->index_pt_psi_qpf]);
        delta_p_qpf = 1./3.*(-ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_prime_qpf]/a2
                             +pow(ppw->pvecback[pba->index_bg_psi_prime_qpf],2)*psi/a2
                             -ppw->pvecback[pba->index_bg_dV_qpf]*y[ppw->pv->index_pt_psi_qpf]);
      }
      ppw->delta_rho += delta_rho_qpf;
      ppw->rho_plus_p_theta -= 1./3.*k*k/a2*ppw->pvecback[pba->index_bg_psi_prime_qpf]*y[ppw->pv->index_pt_psi_qpf];
      ppw->delta_p += delta_p_qpf;
      ppw->rho_plus_p_tot += ppw->pvecback[pba->index_bg_rho_qpf]+ppw->pvecback[pba->index_bg_p_qpf];
    }

    /* add your extra species here */
"""
    replace_once(root, rel, old, new, "perturbations.c total stress energy")

    old = """    /** - ---> scalar field (scf) */

    if (pba->has_scf == _TRUE_) {

      /** - ----> field value */

      dy[pv->index_pt_phi_scf] = y[pv->index_pt_phi_prime_scf];

      /** - ----> Klein Gordon equation */

      dy[pv->index_pt_phi_prime_scf] =  - 2.*a_prime_over_a*y[pv->index_pt_phi_prime_scf]
        - metric_continuity*pvecback[pba->index_bg_phi_prime_scf] //  metric_continuity = h'/2
        - (k2 + a2*pvecback[pba->index_bg_ddV_scf])*y[pv->index_pt_phi_scf]; //checked

    }
"""
    new = old + """
    /** - ---> KMDSB K3D2 canonical qcf */
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
    replace_once(root, rel, old, new, "perturbations.c KG equations")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--manifest", type=Path)
    args = ap.parse_args()
    root = args.root.resolve()
    for rel in ALLOWED:
        if not (root / rel).is_file():
            raise SystemExit(f"missing exact-pin source file: {rel}")

    before = {rel: digest_scf_lines(root, rel) for rel in ALLOWED}
    patch_background_h(root)
    patch_background_c(root)
    patch_input_c(root)
    patch_perturbations_h(root)
    patch_perturbations_c(root)
    after = {rel: digest_scf_lines(root, rel) for rel in ALLOWED}
    if before != after:
        bad = [rel for rel in ALLOWED if before[rel] != after[rel]]
        raise SystemExit(f"protected upstream scf-bearing lines changed: {bad}")

    manifest = {
        "schema": "KMDSB.W03.M13b.K3D2AdapterPatchManifest.v0.1",
        "provider_commit_required": CLASS_PIN,
        "allowed_files": ALLOWED,
        "upstream_scf_line_digests_before": before,
        "upstream_scf_line_digests_after": after,
        "upstream_scf_lines_byte_sequence_preserved": True,
        "independent_species": ["qcf", "qpf"],
        "qcf_sign": "canonical",
        "qpf_sign": "phantom",
        "U0": float(U0),
        "s": 29.0,
        "normalization": "V_class=3*H0^2*U",
        "published_V0_reproduced": False,
        "author_normalization_map_claimed": False,
        "runtime_gauge_scope": "synchronous_only_when_qcf_or_qpf_enabled",
    }
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
