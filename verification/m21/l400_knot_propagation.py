#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_L400_KNOT_PROPAGATION_DIAGNOSTIC_v0.1.md'
PAIRS={
 'A':('P400_ON_TAIL_OFF','P400_OFF_TAIL_OFF'),
 'B':('P400_EVEN_TAIL_OFF','P400_OFF_TAIL_OFF'),
}
CASES=('ref','f2','f3','f4')

def lgrid(logstep,linstep,lmax=2500):
    vals=[2]; cur=2; inc=max(int(cur*(logstep-1.0)),1)
    while ((cur+inc)<lmax) and (inc<linstep):
        cur+=inc; vals.append(cur); inc=max(int(cur*(logstep-1.0)),1)
    inc=linstep
    while cur+inc<=lmax: cur+=inc; vals.append(cur)
    if cur!=lmax: vals.append(lmax)
    return np.asarray(vals,int)

def sig(ls):
    return {'node_count':int(ls.size),'contains_l400':bool(400 in set(ls.tolist())),'contains_l2499':bool(2499 in set(ls.tolist())),'nodes_394_406':[int(x) for x in ls[(ls>=394)&(ls<=406)]],'tail_nodes':[int(x) for x in ls[-8:]]}

def loadcl(p):
    rows=[]
    for raw in p.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        try:r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if r and all(math.isfinite(x) for x in r): rows.append(r)
    a=np.asarray(rows,float)
    if a.shape[0]!=2499 or a.shape[1]<3 or not np.array_equal(a[:,0],np.arange(2,2501,dtype=float)): raise RuntimeError(f'bad cl {p} {a.shape}')
    return a

def locate(root,lane):
    hits=[]
    for mp in root.rglob('lane_meta.json'):
        m=json.load(open(mp))
        if m.get('lane')==lane: hits.append((mp.parent,m))
    if len(hits)!=1: raise RuntimeError(f'lane locate {lane}: {len(hits)}')
    d,m=hits[0]
    if m.get('provider_head')!=PIN or not m.get('exact_head') or not m.get('all_cases_rc0'): raise RuntimeError(f'authority {lane}')
    ls=lgrid(float(m['l_logstep']),int(m['l_linstep']))
    if sig(ls)!=m.get('sparse_l_signature'): raise RuntimeError(f'grid signature {lane}')
    tabs={}
    for c in CASES:
        xs=sorted(d.glob(f'output/{c}_*_cl.dat'))
        if len(xs)!=1: raise RuntimeError(f'cl count {lane}/{c}')
        tabs[c]=loadcl(xs[0])
    return ls,tabs

def E(tabs,ells):
    if len(ells)<3: raise RuntimeError('insufficient support')
    idx=np.asarray(sorted(set(int(x) for x in ells)),int)-2
    r=tabs['ref'][idx,2]
    ds={c:tabs[c][idx,2]-r for c in ('f2','f3','f4')}
    norms={c:float(np.linalg.norm(ds[c])) for c in ds}
    return float(norms['f3']/max(norms['f2'],norms['f4'],1e-300)), norms, int(len(idx))

def state(e): return 'HIGH' if e>3.0 else 'CALM'

def main(root,pair_id,out):
    res={'schema':'KMDSB.W04.M21.L400KnotPropagation.Pair.v0.1','protocol':PROTOCOL,'pair_id':pair_id,'provider':f'lesgourg/class_public@{PIN}','K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    try:
        hi,lo=PAIRS[pair_id]; hls,ht=locate(root,hi); lls,lt=locate(root,lo)
        if 400 not in set(hls.tolist()) or 400 in set(lls.tolist()): raise RuntimeError('frozen l400 membership contrast absent')
        h_no=hls[hls!=400]
        common=np.asarray(sorted((set(hls.tolist()) & set(lls.tolist()))-{400}),int)
        common_band=common[(common>=400)&(common<=800)]
        h_band=hls[(hls>=400)&(hls<=800)]; h_band_no=h_band[h_band!=400]
        vals={}
        for key,tabs,ells in [
            ('high_full',ht,hls),('high_without_l400',ht,h_no),('high_band',ht,h_band),('high_band_without_l400',ht,h_band_no),
            ('high_common',ht,common),('calm_common',lt,common),('high_common_band',ht,common_band),('calm_common_band',lt,common_band)]:
            e,n,k=E(tabs,ells); vals[key]={'E_EE':e,'state':state(e),'support_count':k,'norms':n}
        propagate=(vals['high_without_l400']['state']=='HIGH' and ((vals['high_common']['state']=='HIGH' and vals['calm_common']['state']=='CALM') or (vals['high_common_band']['state']=='HIGH' and vals['calm_common_band']['state']=='CALM')))
        single=(vals['high_without_l400']['state']=='CALM' and not ((vals['high_common']['state']=='HIGH' and vals['calm_common']['state']=='CALM') or (vals['high_common_band']['state']=='HIGH' and vals['calm_common_band']['state']=='CALM')))
        res.update({'high_lane':hi,'calm_lane':lo,'cross_lane_input_identity':True,'metrics':vals,'pair_propagates':bool(propagate),'pair_single_knot_sufficient':bool(single),'classification':'PAIR_PROPAGATES' if propagate else ('PAIR_SINGLE_KNOT_SUFFICIENT' if single else 'PAIR_MIXED')})
    except Exception as e:
        res.update({'classification':'PAIR_BLOCKED','cross_lane_input_identity':False,'error':repr(e)})
    out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
    if res['classification']=='PAIR_BLOCKED': raise SystemExit(1)
if __name__=='__main__':
    if len(sys.argv)!=4: raise SystemExit('usage: script LANES_ROOT PAIR_ID OUT')
    main(Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3]))
