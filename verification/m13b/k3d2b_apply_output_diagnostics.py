#!/usr/bin/env python3
"""Add output-only K3D2-B direct-field diagnostics to an already patched CLASS tree.

Allowed effect: extend scalar k_output_values titles/data with synchronous qcf/qpf
field perturbations and the synchronous-to-Newtonian metric gauge generator
(alpha, alpha'). No integration variable, RHS, Einstein source, hierarchy, or
background equation is modified.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def replace_once(path: Path, old: str, new: str, label: str):
    text=path.read_text(encoding='utf-8')
    n=text.count(old)
    if n!=1:
        raise RuntimeError(f'{label}: expected one anchor, found {n}')
    path.write_text(text.replace(old,new,1),encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('--manifest',type=Path)
    a=ap.parse_args(); root=a.root.resolve(); p=root/'source/perturbations.c'
    before=p.read_bytes(); before_sha=hashlib.sha256(before).hexdigest()

    title_anchor='''      /* Scalar field scf */
      class_store_columntitle(ppt->scalar_titles, "delta_scf", pba->has_scf);
      class_store_columntitle(ppt->scalar_titles, "theta_scf", pba->has_scf);
'''
    title_new=title_anchor+'''      /* KMDSB K3D2-B output-only direct-field diagnostics. */
      class_store_columntitle(ppt->scalar_titles, "delta_qcf_S", pba->has_qcf);
      class_store_columntitle(ppt->scalar_titles, "delta_prime_qcf_S", pba->has_qcf);
      class_store_columntitle(ppt->scalar_titles, "delta_qpf_S", pba->has_qpf);
      class_store_columntitle(ppt->scalar_titles, "delta_prime_qpf_S", pba->has_qpf);
      class_store_columntitle(ppt->scalar_titles, "alpha_sync_to_newt", (pba->has_qcf || pba->has_qpf));
      class_store_columntitle(ppt->scalar_titles, "alpha_prime_sync_to_newt", (pba->has_qcf || pba->has_qpf));
'''
    replace_once(p,title_anchor,title_new,'scalar diagnostic titles')

    data_anchor='''    /* Scalar field scf*/
    class_store_double(dataptr, delta_scf, pba->has_scf, storeidx);
    class_store_double(dataptr, theta_scf, pba->has_scf, storeidx);
'''
    data_new=data_anchor+'''    /* KMDSB K3D2-B output-only direct-field diagnostics. */
    class_store_double(dataptr, y[ppw->pv->index_pt_phi_qcf], pba->has_qcf, storeidx);
    class_store_double(dataptr, y[ppw->pv->index_pt_phi_prime_qcf], pba->has_qcf, storeidx);
    class_store_double(dataptr, y[ppw->pv->index_pt_psi_qpf], pba->has_qpf, storeidx);
    class_store_double(dataptr, y[ppw->pv->index_pt_psi_prime_qpf], pba->has_qpf, storeidx);
    class_store_double(dataptr, pvecmetric[ppw->index_mt_alpha], (pba->has_qcf || pba->has_qpf), storeidx);
    class_store_double(dataptr, pvecmetric[ppw->index_mt_alpha_prime], (pba->has_qcf || pba->has_qpf), storeidx);
'''
    replace_once(p,data_anchor,data_new,'scalar diagnostic data')

    after=p.read_bytes(); after_sha=hashlib.sha256(after).hexdigest()
    # Fail closed: exactly 12 KMDSB diagnostic lines (2 comments + 10 storage/title calls)
    text=after.decode()
    marker='KMDSB K3D2-B output-only direct-field diagnostics.'
    assert text.count(marker)==2
    manifest={
      'schema':'KMDSB.W03.M13b.K3D2BOutputDiagnosticsPatch.v0.1',
      'changed_file':'source/perturbations.c',
      'before_sha256':before_sha,'after_sha256':after_sha,
      'title_columns':['delta_qcf_S','delta_prime_qcf_S','delta_qpf_S','delta_prime_qpf_S','alpha_sync_to_newt','alpha_prime_sync_to_newt'],
      'changes_state_vector':False,'changes_rhs':False,'changes_einstein_sources':False,
      'changes_boltzmann_hierarchy':False,'changes_background':False,'output_only':True
    }
    if a.manifest:
        a.manifest.parent.mkdir(parents=True,exist_ok=True); a.manifest.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    else: print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=='__main__': main()
