#!/usr/bin/env python3
"""Inject a diagnostic mapping certificate into exact-pin patched CLASS.

This transformer changes no physical equation, tolerance, solver family, or
state vector. It runs after the frozen native perturbation interval split and
prints the minimal local conformal-time displacement whose *actual*
background_at_tau() result is right-owned by the z=5 qfield handoff.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--manifest'); args=ap.parse_args()
    p=Path(args.root)/'source/perturbations.c'; before=p.read_text()
    if 'inserted_handoff_kmdsb' not in before:
        raise RuntimeError('native perturbation interval split must be applied first')
    anchor='  /** - fill the structure containing all fixed parameters, indices\n      and workspaces needed by perturbations_derivs */'
    if before.count(anchor)!=1:
        raise RuntimeError(f'expected one ppaw anchor, found {before.count(anchor)}')
    block=r'''  /* KMDSB K3D2-B mapping certificate; diagnostics only. */
  if ((inserted_handoff_kmdsb == _TRUE_) && (index_k == 0) && (index_ic == 0)) {
    const unsigned long long max_ulps_kmdsb = 1073741824ULL;
    double a_handoff_cert_kmdsb = exp(log(1./6.));
    double tau_ulp_cert_kmdsb = nextafter(tau_handoff_kmdsb,INFINITY)-tau_handoff_kmdsb;
    unsigned long long lo_ulps_kmdsb = 0ULL;
    unsigned long long hi_ulps_kmdsb = 1ULL;
    unsigned long long mid_ulps_kmdsb;
    double tau_try_kmdsb = tau_handoff_kmdsb;
    double a_try_kmdsb = -1.;
    double * pvecback_cert_kmdsb;
    int last_cert_kmdsb = 0;
    int found_cert_kmdsb = _FALSE_;
    class_alloc(pvecback_cert_kmdsb,pba->bg_size_normal*sizeof(double),ppt->error_message);
    while (hi_ulps_kmdsb <= max_ulps_kmdsb) {
      tau_try_kmdsb = tau_handoff_kmdsb + ((double)hi_ulps_kmdsb)*tau_ulp_cert_kmdsb;
      last_cert_kmdsb = 0;
      class_call(background_at_tau(pba,tau_try_kmdsb,normal_info,inter_normal,&last_cert_kmdsb,pvecback_cert_kmdsb),pba->error_message,ppt->error_message);
      a_try_kmdsb = pvecback_cert_kmdsb[pba->index_bg_a];
      if (a_try_kmdsb > a_handoff_cert_kmdsb) { found_cert_kmdsb = _TRUE_; break; }
      lo_ulps_kmdsb = hi_ulps_kmdsb;
      hi_ulps_kmdsb *= 2ULL;
    }
    if (found_cert_kmdsb == _TRUE_) {
      while (hi_ulps_kmdsb-lo_ulps_kmdsb > 1ULL) {
        mid_ulps_kmdsb = lo_ulps_kmdsb + (hi_ulps_kmdsb-lo_ulps_kmdsb)/2ULL;
        tau_try_kmdsb = tau_handoff_kmdsb + ((double)mid_ulps_kmdsb)*tau_ulp_cert_kmdsb;
        last_cert_kmdsb = 0;
        class_call(background_at_tau(pba,tau_try_kmdsb,normal_info,inter_normal,&last_cert_kmdsb,pvecback_cert_kmdsb),pba->error_message,ppt->error_message);
        a_try_kmdsb = pvecback_cert_kmdsb[pba->index_bg_a];
        if (a_try_kmdsb > a_handoff_cert_kmdsb) hi_ulps_kmdsb = mid_ulps_kmdsb;
        else lo_ulps_kmdsb = mid_ulps_kmdsb;
      }
      double tau_cert_kmdsb = tau_handoff_kmdsb + ((double)hi_ulps_kmdsb)*tau_ulp_cert_kmdsb;
      double tau_prev_kmdsb = nextafter(tau_cert_kmdsb,tau_handoff_kmdsb);
      double a_cert_kmdsb, a_prev_kmdsb, z_cert_kmdsb, z_prev_kmdsb;
      last_cert_kmdsb = 0;
      class_call(background_at_tau(pba,tau_cert_kmdsb,normal_info,inter_normal,&last_cert_kmdsb,pvecback_cert_kmdsb),pba->error_message,ppt->error_message);
      a_cert_kmdsb = pvecback_cert_kmdsb[pba->index_bg_a];
      class_call(background_z_of_tau(pba,tau_cert_kmdsb,&z_cert_kmdsb),pba->error_message,ppt->error_message);
      last_cert_kmdsb = 0;
      class_call(background_at_tau(pba,tau_prev_kmdsb,normal_info,inter_normal,&last_cert_kmdsb,pvecback_cert_kmdsb),pba->error_message,ppt->error_message);
      a_prev_kmdsb = pvecback_cert_kmdsb[pba->index_bg_a];
      class_call(background_z_of_tau(pba,tau_prev_kmdsb,&z_prev_kmdsb),pba->error_message,ppt->error_message);
      fprintf(stderr,"KMDSB_MAP_CERT found=1 ulps=%llu tau0=%.17g tau_ulp=%.17g tau_prev=%.17g a_prev=%.17g z_prev=%.17g tau_cert=%.17g a_cert=%.17g z_cert=%.17g a_handoff=%.17g\n",hi_ulps_kmdsb,tau_handoff_kmdsb,tau_ulp_cert_kmdsb,tau_prev_kmdsb,a_prev_kmdsb,z_prev_kmdsb,tau_cert_kmdsb,a_cert_kmdsb,z_cert_kmdsb,a_handoff_cert_kmdsb);
    }
    else {
      fprintf(stderr,"KMDSB_MAP_CERT found=0 max_ulps=%llu tau0=%.17g tau_ulp=%.17g a_last=%.17g a_handoff=%.17g\n",max_ulps_kmdsb,tau_handoff_kmdsb,tau_ulp_cert_kmdsb,a_try_kmdsb,a_handoff_cert_kmdsb);
    }
    free(pvecback_cert_kmdsb);
  }

'''
    after=before.replace(anchor,block+anchor,1); p.write_text(after)
    m={'schema':'KMDSB.W03.M13b.K3D2BMappingCertificateProbePatch.v0.1','changed_files':['source/perturbations.c'],'diagnostic_only':True,'changes_equations':False,'changes_tolerances':False,'changes_solver_family':False,'changes_state_vector':False,'sha256_before':sha(before),'sha256_after':sha(after)}
    if args.manifest: Path(args.manifest).write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
