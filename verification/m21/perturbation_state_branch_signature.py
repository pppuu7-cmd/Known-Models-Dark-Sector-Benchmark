#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math,re,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md'
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
LANES=['NDF_T1E5','NDF_T1E6','NDF_T1E7','RK_T1E5','RK_T1E6','RK_T1E7']
CASES=['ref','f2','f3','f4']
COMMON=['delta_g','theta_g','shear_g','pol0_g','pol1_g','pol2_g','delta_b','theta_b','psi','phi','delta_ur','theta_ur','shear_ur','delta_cdm','theta_cdm']
NCDM=['delta_ncdm[0]','theta_ncdm[0]','shear_ncdm[0]','cs2_ncdm[0]']
BRANCH=[('NDF_T1E5','NDF_T1E6'),('NDF_T1E6','NDF_T1E7'),('RK_T1E5','RK_T1E6'),('NDF_T1E7','RK_T1E7')]
CONTROL=[('RK_T1E6','RK_T1E7'),('NDF_T1E5','RK_T1E5'),('NDF_T1E6','RK_T1E6')]
J_FLOOR=1e-12; J_THRESHOLD=3.0
A_LO=1.0/2501.0; A_HI=1.0/501.0

def H(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()

def parse_table(p:Path):
    comments=[]; rows=[]
    for raw in p.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s: continue
        if s.startswith('#'):
            comments.append(raw.rstrip()); continue
        try: r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if r and all(math.isfinite(x) for x in r): rows.append(r)
    a=np.asarray(rows,float)
    if a.ndim!=2 or a.shape[0]<3: raise RuntimeError(f'invalid table {p}: {a.shape}')
    title_line=next((x for x in reversed(comments) if re.search(r'\b1:',x)),None)
    if title_line is None: raise RuntimeError(f'no numbered title line {p}')
    ms=list(re.finditer(r'(\d+):(.+?)(?=\s+\d+:|$)',title_line.lstrip('#').strip()))
    titles=[m.group(2).strip() for m in ms]
    nums=[int(m.group(1)) for m in ms]
    if nums!=list(range(1,len(nums)+1)) or len(titles)!=a.shape[1]: raise RuntimeError(f'title/schema mismatch {p}: nums={nums} titles={titles} shape={a.shape}')
    if len(titles)!=len(set(titles)): raise RuntimeError(f'duplicate titles {p}')
    return titles,a

def file_map(base:Path,meta:dict,case:str):
    out={}
    for rel in meta['perturbation_files'][case]:
        p=base/rel
        m=re.search(r'perturbations_k(\d+)_s\.dat$',p.name)
        if not m: raise RuntimeError(f'unexpected perturbation filename {p}')
        idx=int(m.group(1));
        if idx in out: raise RuntimeError(f'duplicate k index {case}/{idx}')
        out[idx]=p
    if sorted(out)!=list(range(5)): raise RuntimeError(f'k index set {case}: {sorted(out)}')
    return out

def unique_sorted(x,y):
    o=np.argsort(x); x=np.asarray(x)[o]; y=np.asarray(y)[o]
    ux,idx=np.unique(x,return_index=True)
    return ux,y[idx]

def dist(pA:Path,pB:Path,title:str):
    tA,aA=parse_table(pA); tB,aB=parse_table(pB)
    if title not in tA or title not in tB or 'a' not in tA or 'a' not in tB: raise RuntimeError(f'missing title {title} in {pA} / {pB}')
    xA,yA=unique_sorted(aA[:,tA.index('a')],aA[:,tA.index(title)])
    xB,yB=unique_sorted(aB[:,tB.index('a')],aB[:,tB.index(title)])
    goodA=np.isfinite(xA)&np.isfinite(yA)&(xA>0)&(xA>=A_LO)&(xA<=A_HI)
    goodB=np.isfinite(xB)&np.isfinite(yB)&(xB>0)&(xB>=A_LO)&(xB<=A_HI)
    xA,yA=xA[goodA],yA[goodA]; xB,yB=xB[goodB],yB[goodB]
    if xA.size<16 or xB.size<16: raise RuntimeError(f'insufficient window samples {title}: {xA.size}/{xB.size}')
    lo=max(float(xA.min()),float(xB.min())); hi=min(float(xA.max()),float(xB.max()))
    m=(xA>=lo)&(xA<=hi); x=xA[m]; y=yA[m]
    if x.size<16: raise RuntimeError(f'insufficient overlap samples {title}: {x.size}')
    yy=np.interp(np.log(x),np.log(xB),yB)
    d=float(np.linalg.norm(y-yy)/max(float(np.linalg.norm(y)),float(np.linalg.norm(yy)),1e-300))
    return d,int(x.size)

def top_family(edge, lane_dirs, metas, family, cases_for_den):
    A,B=edge; cells=[]
    maps={}
    for c in CASES:
        maps[(A,c)]=file_map(lane_dirs[A],metas[A],c); maps[(B,c)]=file_map(lane_dirs[B],metas[B],c)
    for ki in range(5):
        for v in family:
            ds={}; ns={}
            for c in cases_for_den:
                d,n=dist(maps[(A,c)][ki],maps[(B,c)][ki],v); ds[c]=d; ns[c]=n
            denom=max([ds[c] for c in cases_for_den if c!='f3']+[J_FLOOR])
            J=float(ds['f3']/denom)
            cells.append({'k_index':ki,'title':v,'J':J,'distances':ds,'n_overlap':ns,'localized':J>=J_THRESHOLD})
    cells.sort(key=lambda x:x['J'],reverse=True)
    return {'Jmax':cells[0]['J'],'top_cell':cells[0],'localized_cell_count':sum(x['localized'] for x in cells),'cell_count':len(cells),'localized':any(x['localized'] for x in cells),'top10':cells[:10]}

def main(root:Path,config_path:Path,out:Path):
    cfg=json.load(open(config_path)); result={'schema':'KMDSB.W04.M21.PerturbationStateBranchSignature.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','J_floor':J_FLOOR,'J_threshold':J_THRESHOLD,'a_window':[A_LO,A_HI],'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    try:
        if cfg.get('capability_classification')!='M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_PASS_WITH_SCOPE': raise RuntimeError('invalid capability config authority')
        metas={}; lane_dirs={}
        for mp in root.rglob('lane_meta.json'):
            m=json.load(open(mp)); lane=m.get('lane')
            if lane in metas: raise RuntimeError(f'duplicate lane meta {lane}')
            metas[lane]=m; lane_dirs[lane]=mp.parent
        if set(metas)!=set(LANES): raise RuntimeError(f'lane set mismatch {sorted(metas)}')
        csha=H(config_path)
        for lane,m in metas.items():
            if m.get('provider_head')!=PIN or not m.get('exact_head') or not m.get('all_cases_rc0') or not m.get('five_files_each') or not m.get('physical_lines_preserved'): raise RuntimeError(f'lane integrity failed {lane}')
            if m.get('config_sha256')!=csha: raise RuntimeError(f'config identity failed {lane}')
            if m.get('profile_manifest',{}).get('lane')!=lane: raise RuntimeError(f'profile identity failed {lane}')
        # Schema and actual-k identity checks before scientific distances.
        req=[float(x) for x in cfg['k_anchors_12sig_Mpc_inv']]
        schema={}
        for lane in LANES:
            for c in CASES:
                fm=file_map(lane_dirs[lane],metas[lane],c)
                actual=metas[lane]['actual_k_Mpc_inv'][c]
                if len(actual)!=5: raise RuntimeError(f'actual-k count {lane}/{c}')
                for ki in range(5):
                    if abs(float(actual[ki])-req[ki])/req[ki] > 0.05: raise RuntimeError(f'actual k too far from requested {lane}/{c}/{ki}')
                    titles,_=parse_table(fm[ki]); schema[(lane,c,ki)]=titles
                    needed=['tau [Mpc]','a']+COMMON+(NCDM if c!='ref' else [])
                    miss=[x for x in needed if x not in titles]
                    if miss: raise RuntimeError(f'missing required titles {lane}/{c}/{ki}: {miss}')
                # Numerical-lane changes must not move the selected native k for one physical case.
                if lane!=LANES[0]:
                    base=metas[LANES[0]]['actual_k_Mpc_inv'][c]
                    for ki,(x,y) in enumerate(zip(base,actual)):
                        if abs(float(x)-float(y))/max(abs(float(x)),1e-300)>1e-12: raise RuntimeError(f'cross-lane actual-k drift {c}/{ki}: {x}/{y}')
        edges={};
        for A,B in BRANCH+CONTROL:
            name=f'{A}__{B}'
            common=top_family((A,B),lane_dirs,metas,COMMON,CASES)
            ncdm=top_family((A,B),lane_dirs,metas,NCDM,['f2','f3','f4'])
            edges[name]={'kind':'branch_change' if (A,B) in BRANCH else 'same_branch_control','common':common,'ncdm':ncdm,'edge_localized':bool(common['localized'] or ncdm['localized'])}
        nb=sum(edges[f'{a}__{b}']['edge_localized'] for a,b in BRANCH); nc=sum(edges[f'{a}__{b}']['edge_localized'] for a,b in CONTROL)
        if nb==4 and nc==0: cls='M21_PERTURBATION_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE'
        elif nb>=2: cls='M21_PERTURBATION_STATE_BRANCH_SIGNATURE_PARTIAL'
        else: cls='M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES'
        result.update({'classification':cls,'cross_lane_input_identity':True,'branch_change_localized_count':int(nb),'same_branch_control_localized_count':int(nc),'branch_change_edges':[f'{a}__{b}' for a,b in BRANCH],'same_branch_control_edges':[f'{a}__{b}' for a,b in CONTROL],'edges':edges,'k_anchors_requested_Mpc_inv':req,'capability_artifact_id':cfg['capability_artifact_id'],'capability_digest':cfg['capability_digest']})
    except Exception as e:
        result.update({'classification':'M21_PERTURBATION_STATE_BRANCH_SIGNATURE_BLOCKED','error':repr(e),'cross_lane_input_identity':False})
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':result['classification'],'branch_change_localized_count':result.get('branch_change_localized_count'),'same_branch_control_localized_count':result.get('same_branch_control_localized_count'),'error':result.get('error')},indent=2,sort_keys=True))
    if result['classification'].endswith('BLOCKED'): raise SystemExit(1)

if __name__=='__main__':
    if len(sys.argv)!=4: raise SystemExit('usage: perturbation_state_branch_signature.py LANES_ROOT CONFIG OUT')
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
