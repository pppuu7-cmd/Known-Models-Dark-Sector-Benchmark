#!/usr/bin/env python3
"""Inject diagnostic first post-handoff qfield RHS tracing.

Run after the frozen K3D2 adapter/recovery stack. The injected statements only
print tau/background-a and the direct qcf/qpf state/derivative components for
the first post-handoff RHS calls of the first k/ic lane. They do not alter dy,
y, tolerances, solver choice, or any source equation.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--manifest'); args=ap.parse_args()
    p=Path(args.root)/'source/perturbations.c'; before=p.read_text()
    old='''        dy[pv->index_pt_psi_prime_qpf] = -2.*a_prime_over_a*y[pv->index_pt_psi_prime_qpf]\n          - metric_continuity*pvecback[pba->index_bg_psi_prime_qpf]\n          - (k2 - a2*pvecback[pba->index_bg_ddV_qpf])*y[pv->index_pt_psi_qpf];\n'''
    if before.count(old)!=1:
        raise RuntimeError(f'expected one post-handoff qpf RHS tail, found {before.count(old)}')
    new=old+'''        static int kmdsb_rhs_trace_count = 0;\n        if ((kmdsb_rhs_trace_count < 24) && (pppaw->index_k == 0) && (pppaw->index_ic == 0)) {\n          fprintf(stderr,"KMDSB_RHS_TRACE tau=%.17g a=%.17g yqcf=%.17g yqcfp=%.17g dyqcf=%.17g dyqcfp=%.17g yqpf=%.17g yqpfp=%.17g dyqpf=%.17g dyqpfp=%.17g\\n",\n                  tau,pvecback[pba->index_bg_a],\n                  y[pv->index_pt_phi_qcf],y[pv->index_pt_phi_prime_qcf],\n                  dy[pv->index_pt_phi_qcf],dy[pv->index_pt_phi_prime_qcf],\n                  y[pv->index_pt_psi_qpf],y[pv->index_pt_psi_prime_qpf],\n                  dy[pv->index_pt_psi_qpf],dy[pv->index_pt_psi_prime_qpf]);\n          kmdsb_rhs_trace_count++;\n        }\n'''
    after=before.replace(old,new,1); p.write_text(after)
    m={'schema':'KMDSB.W03.M13b.K3D2BFirstRHSTraceProbePatch.v0.1','changed_files':['source/perturbations.c'],'diagnostic_only':True,'max_trace_rows':24,'changes_equations':False,'changes_tolerances':False,'changes_solver_family':False,'changes_state_vector':False,'sha256_before':sha(before),'sha256_after':sha(after)}
    if args.manifest: Path(args.manifest).write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
