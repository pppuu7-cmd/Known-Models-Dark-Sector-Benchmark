#!/usr/bin/env python3
"""Replace the provisional native tau-ULP perturbation seam by the certified one.

The certified lower bound is the first representable tau > tau_handoff for
which the same `background_at_tau(..., normal_info, inter_normal, ...)` path
used by the perturbation RHS returns a strictly right-owned scale factor.
For the frozen exact-pin realization the prospectively certified count is 12
local tau ULP.  Vector initialization remains at the exact native boundary and
the state vector is unchanged.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--manifest'); args=ap.parse_args()
    p=Path(args.root)/'source/perturbations.c'; before=p.read_text()
    old='''    double interval_start_kmdsb = interval_limit[index_interval];
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb))
      interval_start_kmdsb = nextafter(tau_handoff_kmdsb,interval_limit[index_interval+1]);
'''
    if before.count(old)!=1:
        raise RuntimeError(f'expected one provisional native tau seam, found {before.count(old)}')
    new=r'''    double interval_start_kmdsb = interval_limit[index_interval];
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb)) {
      const int expected_cert_ulps_kmdsb = 12;
      const int max_cert_ulps_kmdsb = 4096;
      double a_handoff_cert_kmdsb = exp(log(1./6.));
      double tau_candidate_kmdsb = tau_handoff_kmdsb;
      double tau_predecessor_kmdsb;
      double a_candidate_kmdsb = -1.;
      double a_predecessor_kmdsb = -1.;
      double * pvecback_cert_kmdsb;
      int last_cert_kmdsb = 0;
      int cert_ulps_kmdsb = 0;
      int cert_found_kmdsb = _FALSE_;

      class_alloc(pvecback_cert_kmdsb,pba->bg_size_normal*sizeof(double),ppt->error_message);
      while (cert_ulps_kmdsb < max_cert_ulps_kmdsb) {
        tau_candidate_kmdsb = nextafter(tau_candidate_kmdsb,interval_limit[index_interval+1]);
        cert_ulps_kmdsb++;
        last_cert_kmdsb = 0;
        class_call(background_at_tau(pba,
                                     tau_candidate_kmdsb,
                                     normal_info,
                                     inter_normal,
                                     &last_cert_kmdsb,
                                     pvecback_cert_kmdsb),
                   pba->error_message,
                   ppt->error_message);
        a_candidate_kmdsb = pvecback_cert_kmdsb[pba->index_bg_a];
        if (a_candidate_kmdsb > a_handoff_cert_kmdsb) {
          cert_found_kmdsb = _TRUE_;
          break;
        }
      }

      class_test(cert_found_kmdsb == _FALSE_,
                 ppt->error_message,
                 "KMDSB certified perturbation seam not found within %d tau ULP",
                 max_cert_ulps_kmdsb);

      tau_predecessor_kmdsb = nextafter(tau_candidate_kmdsb,tau_handoff_kmdsb);
      last_cert_kmdsb = 0;
      class_call(background_at_tau(pba,
                                   tau_predecessor_kmdsb,
                                   normal_info,
                                   inter_normal,
                                   &last_cert_kmdsb,
                                   pvecback_cert_kmdsb),
                 pba->error_message,
                 ppt->error_message);
      a_predecessor_kmdsb = pvecback_cert_kmdsb[pba->index_bg_a];

      class_test(cert_ulps_kmdsb != expected_cert_ulps_kmdsb,
                 ppt->error_message,
                 "KMDSB certified perturbation seam changed: got %d tau ULP, expected %d",
                 cert_ulps_kmdsb,expected_cert_ulps_kmdsb);
      class_test(a_predecessor_kmdsb > a_handoff_cert_kmdsb,
                 ppt->error_message,
                 "KMDSB certified perturbation predecessor is already right-owned");
      class_test(a_candidate_kmdsb <= a_handoff_cert_kmdsb,
                 ppt->error_message,
                 "KMDSB certified perturbation candidate is not right-owned");

      interval_start_kmdsb = tau_candidate_kmdsb;
      if ((index_k == 0) && (index_ic == 0))
        fprintf(stderr,
                "KMDSB_CERT_TAU ulps=%d tau0=%.17g tau_prev=%.17g a_prev=%.17g tau_cert=%.17g a_cert=%.17g a_handoff=%.17g\n",
                cert_ulps_kmdsb,tau_handoff_kmdsb,tau_predecessor_kmdsb,a_predecessor_kmdsb,
                interval_start_kmdsb,a_candidate_kmdsb,a_handoff_cert_kmdsb);
      free(pvecback_cert_kmdsb);
    }
'''
    after=before.replace(old,new,1)
    p.write_text(after)
    manifest={
      'schema':'KMDSB.W03.M13b.K3D2BMappingCertifiedTauSeamPatch.v0.1',
      'changed_files':['source/perturbations.c'],
      'conditional_qfields':True,
      'expected_certified_tau_ulps':12,
      'search_guard_tau_ulps':4096,
      'certification_uses_background_at_tau':True,
      'requires_predecessor_not_right_owned':True,
      'requires_candidate_right_owned':True,
      'vector_init_boundary_unchanged':True,
      'state_vector_unchanged':True,
      'changes_open_interval_equations':False,
      'changes_tolerances':False,
      'changes_solver_family':False,
      'changes_boltzmann_hierarchy_equations':False,
      'changes_einstein_sources':False,
      'sha256_before':sha(before),'sha256_after':sha(after),
    }
    if args.manifest: Path(args.manifest).write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps(manifest,indent=2,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
