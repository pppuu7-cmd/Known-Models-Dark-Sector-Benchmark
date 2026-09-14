#!/usr/bin/env python3
from __future__ import annotations
import json,math,re,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_TRANSFER_L_KNOT_ONLY_PHASE_REANALYSIS_v0.1.md'
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
LANES=['P400_OFF_TAIL_ON','P400_OFF_TAIL_OFF','P400_EVEN_TAIL_OFF','P400_ON_TAIL_OFF']
CASES=['ref','f2','f3','f4']
CHANNELS={'TT':1,'EE':2,'TE':3}
BANDS=[(2,399),(400,800),(801,1500),(1501,2500)]
PARENT_CLASS='M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE'

def lgrid(logstep:float,linstep:int,lmax:int=2500):
    vals=[2]; cur=2
    inc=max(int(cur*(logstep-1.0)),1)
    while ((cur+inc)<lmax) and (inc<linstep):
        cur+=inc; vals.append(cur); inc=max(int(cur*(logstep-1.0)),1)
    inc=linstep
    while (cur+inc)<=lmax:
        cur+=inc; vals.append(cur)
    if cur!=lmax: vals.append(lmax)
    return np.asarray(vals,dtype=int)

def signature(ls):
    return {'node_count':int(ls.size),'contains_l400':bool(400 in set(ls.tolist())),'contains_l2499':bool(2499 in set(ls.tolist())),'nodes_394_406':[int(x) for x in ls[(ls>=394)&(ls<=406)]],'tail_nodes':[int(x) for x in ls[-8:]]}

def load_cl(p:Path):
    rows=[]
    for raw in p.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        try: r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if r and all(math.isfinite(x) for x in r): rows.append(r)
    a=np.asarray(rows,float)
    if a.ndim!=2 or a.shape[0]!=2499 or a.shape[1]<4: raise RuntimeError(f'invalid cl table {p}: {a.shape}')
    ell=a[:,0]
    if not np.array_equal(ell,np.arange(2,2501,dtype=float)): raise RuntimeError(f'ell grid mismatch {p}')
    return a

def exactly_one(root:Path,case:str):
    xs=sorted(root.glob(f'output/{case}_*_cl.dat'))
    if len(xs)!=1: raise RuntimeError(f'expected one cl table {root}/{case}: {xs}')
    return xs[0]

def nl2(y,r): return float(np.linalg.norm(y-r)/max(float(np.linalg.norm(r)),1e-300))
def responses(tabs,inds):
    out={}
    for ch,col in CHANNELS.items():
        rr=tabs['ref'][inds,col]
        R={c:nl2(tabs[c][inds,col],rr) for c in ['f2','f3','f4']}
        out[ch]={'R2':R,'excursion_factor':float(R['f3']/max(R['f2'],R['f4'],1e-300))}
    return out

def main(root:Path,parent_path:Path,out:Path):
    parent=json.load(open(parent_path))
    result={'schema':'KMDSB.W04.M21.LGridKnotOnlyPhaseReanalysis.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','parent_run_id':34887488405,'parent_classification':parent.get('classification'),'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    try:
        if parent.get('classification')!=PARENT_CLASS or parent.get('cross_lane_input_identity') is not True: raise RuntimeError('invalid parent authority')
        dirs={}; metas={}
        for mp in root.rglob('lane_meta.json'):
            m=json.load(open(mp)); lane=m.get('lane')
            if lane in LANES:
                if lane in dirs: raise RuntimeError(f'duplicate lane {lane}')
                dirs[lane]=mp.parent; metas[lane]=m
        if set(dirs)!=set(LANES): raise RuntimeError(f'lane set mismatch {sorted(dirs)}')
        lanes={}; states={}
        for lane in LANES:
            m=metas[lane]
            if m.get('provider_head')!=PIN or not m.get('exact_head') or not m.get('all_cases_rc0') or m.get('varied_keys')!=['l_logstep','l_linstep']: raise RuntimeError(f'lane identity failed {lane}')
            lg=float(m['l_logstep']); li=int(m['l_linstep']); ls=lgrid(lg,li); sig=signature(ls)
            if sig!=m.get('sparse_l_signature'): raise RuntimeError(f'sparse-l signature mismatch {lane}: generated={sig} manifest={m.get("sparse_l_signature")}')
            tabs={c:load_cl(exactly_one(dirs[lane],c)) for c in CASES}; inds=ls-2
            resp=responses(tabs,inds); E=resp['EE']['excursion_factor']; state='HIGH' if E>3.0 else 'CALM'; states[lane]=state
            bands=[]
            for lo,hi in BANDS:
                mask=(ls>=lo)&(ls<=hi)
                if int(mask.sum())<3: raise RuntimeError(f'insufficient knots in band {lane}/{lo}-{hi}')
                bi=ls[mask]-2; br=responses(tabs,bi)['EE']
                bands.append({'l_min':lo,'l_max':hi,'knot_count':int(mask.sum()),'EE_R2':br['R2'],'EE_excursion_factor':br['excursion_factor']})
            lanes[lane]={'l_logstep':lg,'l_linstep':li,'sparse_l_signature':sig,'knot_only_response':resp,'EE_knot_excursion_factor':E,'EE_knot_state':state,'EE_knot_bands_report_only':bands}
        exact=(states['P400_ON_TAIL_OFF']=='HIGH' and states['P400_EVEN_TAIL_OFF']=='HIGH' and states['P400_OFF_TAIL_ON']=='CALM' and states['P400_OFF_TAIL_OFF']=='CALM')
        cls='M21_L_GRID_KNOT_VALUES_CARRY_L400_SIGNATURE_WITH_SCOPE' if exact else 'M21_L_GRID_PHASE_SIGNATURE_EMERGES_OR_CHANGES_BETWEEN_KNOTS'
        result.update({'classification':cls,'cross_lane_input_identity':True,'EE_knot_states':states,'lanes':lanes,'parent_full_output_EE_states':parent.get('EE_states'),'exact_l400_knot_pattern':bool(exact)})
    except Exception as e:
        result.update({'classification':'M21_L_GRID_KNOT_ONLY_REANALYSIS_BLOCKED','cross_lane_input_identity':False,'error':repr(e)})
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'classification':result['classification'],'EE_knot_states':result.get('EE_knot_states'),'error':result.get('error')},indent=2,sort_keys=True))
    if result['classification'].endswith('BLOCKED'): raise SystemExit(1)
if __name__=='__main__':
    if len(sys.argv)!=4: raise SystemExit('usage: l_grid_knot_only_phase_reanalysis.py LANES_ROOT PARENT_JSON OUT')
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
