#!/usr/bin/env python3
"""Trace BEGIN/END of the inserted post-handoff perturbation interval per k mode."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--manifest'); args=ap.parse_args()
    p=Path(args.root)/'source/perturbations.c'; before=p.read_text()
    begin_anchor='''    class_call(generic_evolver(perturbations_derivs,\n                               interval_start_kmdsb,\n                               interval_limit[index_interval+1],'''
    if before.count(begin_anchor)!=1:
        raise RuntimeError(f'expected one recovered evolver call, found {before.count(begin_anchor)}')
    begin='''    if ((inserted_handoff_kmdsb == _TRUE_) &&\n        (interval_limit[index_interval] == tau_handoff_kmdsb))\n      fprintf(stderr,"KMDSB_MODE_BEGIN index_k=%d k=%.17g interval_start=%.17g evolver_start=%.17g interval_end=%.17g\\n",index_k,k,interval_limit[index_interval],interval_start_kmdsb,interval_limit[index_interval+1]);\n\n'''
    s=before.replace(begin_anchor,begin+begin_anchor,1)
    end_anchor='''               ppt->error_message,\n               ppt->error_message);\n\n  }\n\n  /** - if perturbations were printed in a file, close the file */'''
    if s.count(end_anchor)!=1:
        raise RuntimeError(f'expected one interval-loop tail, found {s.count(end_anchor)}')
    end='''               ppt->error_message,\n               ppt->error_message);\n\n    if ((inserted_handoff_kmdsb == _TRUE_) &&\n        (interval_limit[index_interval] == tau_handoff_kmdsb))\n      fprintf(stderr,"KMDSB_MODE_END index_k=%d k=%.17g interval_start=%.17g evolver_start=%.17g interval_end=%.17g\\n",index_k,k,interval_limit[index_interval],interval_start_kmdsb,interval_limit[index_interval+1]);\n\n  }\n\n  /** - if perturbations were printed in a file, close the file */'''
    after=s.replace(end_anchor,end,1); p.write_text(after)
    m={'schema':'KMDSB.W03.M13b.K3D2BModeIntervalTracePatch.v0.1','changed_files':['source/perturbations.c'],'diagnostic_only':True,'changes_equations':False,'changes_tolerances':False,'changes_solver_family':False,'changes_state_vector':False,'sha256_before':sha(before),'sha256_after':sha(after)}
    if args.manifest: Path(args.manifest).write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True)); return 0

if __name__=='__main__': raise SystemExit(main())
