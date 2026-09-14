#!/usr/bin/env python3
from __future__ import annotations
import json, math, re, sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_v0.1.md'
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
L_ANCHORS=[100,400,800,1200,2000]

def load_numeric(p: Path) -> np.ndarray:
    rows=[]
    for raw in p.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        try: row=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if row and all(math.isfinite(x) for x in row): rows.append(row)
    a=np.asarray(rows,float)
    if a.ndim!=2 or a.shape[0]<3 or a.shape[1]<2: raise RuntimeError(f'invalid numeric table {p}: {a.shape}')
    return a

def comments(p: Path):
    return [x.rstrip() for x in p.read_text(errors='replace').splitlines() if x.lstrip().startswith('#')]

def exactly_one(out: Path, pattern: str) -> Path:
    xs=sorted(out.glob(pattern))
    if len(xs)!=1: raise RuntimeError(f'expected one {pattern}, got {[str(x) for x in xs]}')
    return xs[0]

def main(root: Path, meta_path: Path, case_manifest_path: Path, profile_manifest_path: Path, outpath: Path):
    meta=json.load(open(meta_path)); cm=json.load(open(case_manifest_path)); pm=json.load(open(profile_manifest_path))
    result={'schema':'KMDSB.W04.M21.PerturbationOutputCapabilityRecon.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    try:
        if meta.get('provider_head')!=PIN or not meta.get('exact_head'): raise RuntimeError('provider HEAD mismatch')
        if meta.get('class_rc')!=0: raise RuntimeError(f"CLASS rc={meta.get('class_rc')}")
        if not cm.get('physical_lines_preserved'): raise RuntimeError('ref case preservation failed')
        if pm.get('provider')!=f'lesgourg/class_public@{PIN}' or not pm.get('duplicate_free_serialization'): raise RuntimeError('baseline identity failed')
        outdir=root/'output'
        pert=exactly_one(outdir,'ref_*perturbations_k0_s.dat')
        bg=exactly_one(outdir,'ref_*background.dat')
        th=exactly_one(outdir,'ref_*thermodynamics.dat')
        pa=load_numeric(pert); ba=load_numeric(bg); ta=load_numeric(th)
        pc=comments(pert); bc=comments(bg); tc=comments(th)
        kline=next((x for x in pc if 'scalar perturbations for mode k' in x),None)
        if kline is None: raise RuntimeError('missing scalar perturbation k header')
        m=re.search(r'k\s*=\s*([0-9eE+\-.]+)',kline)
        if not m: raise RuntimeError(f'unparseable k header {kline!r}')
        actual_k=float(m.group(1))
        if not math.isfinite(actual_k) or actual_k<=0: raise RuntimeError('invalid actual k')
        # Exact pinned table schemas are also frozen in the protocol/source authority.
        if ba.shape[1] < 3 or ta.shape[1] < 7: raise RuntimeError('background/thermodynamics schema too small')
        if not any('3:conf. time [Mpc]' in x for x in bc): raise RuntimeError('background conformal-time header mismatch')
        if not any('3:conf. time [Mpc]' in x and '7:g [Mpc^-1]' in x for x in tc): raise RuntimeError('thermodynamics title header mismatch')
        iz0=int(np.argmin(np.abs(ba[:,0])))
        if abs(float(ba[iz0,0]))>1e-8: raise RuntimeError(f'no z=0 background row: nearest {ba[iz0,0]}')
        tau0=float(ba[iz0,2])
        ig=int(np.argmax(ta[:,6])); tau_star=float(ta[ig,2]); z_star=float(ta[ig,1]); gmax=float(ta[ig,6])
        D=tau0-tau_star
        if not all(math.isfinite(x) for x in [tau0,tau_star,z_star,gmax,D]) or D<=0 or gmax<=0: raise RuntimeError('invalid reference geometry')
        kunrounded=[ell/D for ell in L_ANCHORS]
        if not all(math.isfinite(x) and x>0 for x in kunrounded) or not all(kunrounded[i]<kunrounded[i+1] for i in range(len(kunrounded)-1)): raise RuntimeError('invalid k anchors')
        title_line=next((x for x in pc if re.search(r'#\s*1:',x)),None)
        result.update({'classification':'M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_PASS_WITH_SCOPE','perturbation_file':str(pert),'perturbation_numeric_shape':[int(x) for x in pa.shape],'perturbation_header_lines':pc,'perturbation_title_line':title_line,'actual_capability_k_Mpc_inv':actual_k,'background_file':str(bg),'thermodynamics_file':str(th),'tau0_Mpc':tau0,'tau_star_Mpc':tau_star,'z_star_visibility_max':z_star,'visibility_max_Mpc_inv':gmax,'D_star_Mpc':D,'l_anchors':L_ANCHORS,'k_anchors_unrounded_Mpc_inv':kunrounded,'k_anchors_12sig_Mpc_inv':[float(f'{x:.12g}') for x in kunrounded],'successor_scientific_gate_authorized':True})
    except Exception as e:
        result.update({'classification':'M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_BLOCKED','error':repr(e),'successor_scientific_gate_authorized':False})
    outpath.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    if result['classification'].endswith('BLOCKED'): raise SystemExit(1)

if __name__=='__main__':
    if len(sys.argv)!=6: raise SystemExit('usage: perturbation_output_capability_recon.py ROOT LANE_META CASE_MANIFEST PROFILE_MANIFEST OUT')
    main(*(Path(x) for x in sys.argv[1:]))
