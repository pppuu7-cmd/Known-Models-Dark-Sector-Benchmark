#!/usr/bin/env python3
"""Move only the second qfield perturbation numerical interval start by A-ULPs.

Requires the frozen native-interval split patch to be applied first.  The exact
z=5 interval boundary and perturbation vector initialization remain unchanged;
only the lower bound supplied to the second numerical evolver is mapped from
a_post=nextafter^N(1/6,1) through background_tau_of_z().
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--ulps', type=int, choices=(1,2), required=True)
    ap.add_argument('--manifest')
    a = ap.parse_args()
    p = Path(a.root) / 'source/perturbations.c'
    before = p.read_text()
    old = '''    double interval_start_kmdsb = interval_limit[index_interval];
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb))
      interval_start_kmdsb = nextafter(tau_handoff_kmdsb,interval_limit[index_interval+1]);
'''
    if before.count(old) != 1:
        raise RuntimeError('expected exactly one native tau-ULP seam anchor')
    loops = '\n'.join('      a_post_kmdsb = nextafter(a_post_kmdsb,1.0);' for _ in range(a.ulps))
    new = f'''    double interval_start_kmdsb = interval_limit[index_interval];
    if ((inserted_handoff_kmdsb == _TRUE_) &&
        (interval_limit[index_interval] == tau_handoff_kmdsb)) {{
      double a_post_kmdsb = exp(log(1./6.));
      double z_post_kmdsb;
{loops}
      z_post_kmdsb = 1./a_post_kmdsb - 1.;
      class_call(background_tau_of_z(pba,z_post_kmdsb,&interval_start_kmdsb),
                 pba->error_message,
                 ppt->error_message);
    }}
'''
    after = before.replace(old,new,1)
    if 'nextafter(tau_handoff_kmdsb' in after:
        raise RuntimeError('tau-ULP seam unexpectedly remains')
    if after.count('background_tau_of_z(pba,z_post_kmdsb,&interval_start_kmdsb)') != 1:
        raise RuntimeError('a-ULP tau mapping missing')
    p.write_text(after)
    m = {
      'schema':'KMDSB.W03.M13b.K3D2BPerturbationAULPSeamPatch.v0.1',
      'a_ulps':a.ulps,
      'changed_files':['source/perturbations.c'],
      'exact_interval_boundary_unchanged':True,
      'vector_init_boundary_unchanged':True,
      'state_vector_unchanged':True,
      'tau_post_via_background_tau_of_z':True,
      'changes_open_interval_equations':False,
      'changes_tolerances':False,
      'changes_solver_family':False,
      'changes_boltzmann_hierarchy_equations':False,
      'changes_einstein_sources':False,
      'sha256_before':sha(before),'sha256_after':sha(after)
    }
    if a.manifest:
        Path(a.manifest).write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
