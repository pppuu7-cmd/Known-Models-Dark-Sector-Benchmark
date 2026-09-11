#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from verification.m25.m25_k1_precision_floor_diagnostic import load_table,output,metric,judge

PREREG='protocol/W04_M25_M0_PK_MANUAL_MOMENTUM_QUADRATURE_PREREGISTRATION_v0.1.md'
ETAS=[0.01,0.003,0.001]

def analyze(root:Path,status_path:Path,bins:int,baseline_path:Path,out:Path):
    st=json.loads(status_path.read_text())
    r={'schema':'KMDSB.M25.M0PkManualMomentumQuadrature.v1','preregistration':PREREG,'original_run_id':34548988620,'baseline_run_id':34551925134,'ncdm_quadrature_strategy':3,'ncdm_maximum_q':10.0,'ncdm_N_momentum_bins':bins,'status':st,'K1_promoted':False,'K4_promoted':False,'physical_falsification':False}
    req=['build','ref','e2','e3','e4']
    if any(st.get(k)!=0 for k in req):
        r['classification']='M25_M0_PK_MANUAL_QUADRATURE_PROVIDER_BLOCKED'; r['failed_status_keys']=[k for k in req if st.get(k)!=0]; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); return
    ref_pk=load_table(output(root,'ref','pk')); ref_bg=load_table(output(root,'ref','background'))[:,[0,3]]
    pk=[]; bg=[]
    for i in (2,3,4):
        pk.append(load_table(output(root,f'm0_e{i}','pk'))); bg.append(load_table(output(root,f'm0_e{i}','background'))[:,[0,3]])
    ppts=[]; hpts=[]
    for eta,a,h in zip(ETAS,pk,bg):
        q=metric(a,ref_pk); q['eta']=eta; ppts.append(q)
        q=metric(h,ref_bg); q['eta']=eta; hpts.append(q)
    Pk=judge(ppts); H=judge(hpts)
    baseline=json.loads(baseline_path.read_text()); base=[float(x) for x in baseline['blocks']['Pk']['r95']]
    r.update({'H':H,'Pk':Pk,'baseline_auto_Pk_r95':base,'admissible':bool(H['tail_scaling_recovered']),'classification':'M25_M0_PK_MANUAL_QUADRATURE_POINT_MEASURED' if H['tail_scaling_recovered'] else 'M25_M0_PK_MANUAL_QUADRATURE_BACKGROUND_NOT_ADMISSIBLE'})
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('root',type=Path); ap.add_argument('status',type=Path); ap.add_argument('bins',type=int); ap.add_argument('baseline',type=Path); ap.add_argument('out',type=Path); a=ap.parse_args(); analyze(a.root,a.status,a.bins,a.baseline,a.out)
