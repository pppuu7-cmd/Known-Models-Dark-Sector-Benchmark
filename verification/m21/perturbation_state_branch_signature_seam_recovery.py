#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,math,re,sys
from pathlib import Path
import numpy as np

PROTOCOL='protocol/W04_M21_PERTURBATION_STATE_SEAM_PRESERVING_RECOVERY_v0.1.md'
PARENT_PROTOCOL='protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md'
PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PARENT_RUN=34895647832
PARENT_AGG_ARTIFACT=10369361506
PARENT_AGG_DIGEST='sha256:a7c26408e4c33a2fcda5de2ba5b7ebfed02bee041bbadcaa9b06ce3d2abe805c'
LANES=['NDF_T1E5','NDF_T1E6','NDF_T1E7','RK_T1E5','RK_T1E6','RK_T1E7']
CASES=['ref','f2','f3','f4']
COMMON=['delta_g','theta_g','shear_g','pol0_g','pol1_g','pol2_g','delta_b','theta_b','psi','phi','delta_ur','theta_ur','shear_ur','delta_cdm','theta_cdm']
NCDM=['delta_ncdm[0]','theta_ncdm[0]','shear_ncdm[0]','cs2_ncdm[0]']
BRANCH=[('NDF_T1E5','NDF_T1E6'),('NDF_T1E6','NDF_T1E7'),('RK_T1E5','RK_T1E6'),('NDF_T1E7','RK_T1E7')]
CONTROL=[('RK_T1E6','RK_T1E7'),('NDF_T1E5','RK_T1E5'),('NDF_T1E6','RK_T1E6')]
J_FLOOR=1e-12; J_THRESHOLD=3.0
A_LO=1.0/2501.0; A_HI=1.0/501.0
EXPECTED_SEAMS=3

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
    titles=[m.group(2).strip() for m in ms]; nums=[int(m.group(1)) for m in ms]
    if nums!=list(range(1,len(nums)+1)) or len(titles)!=a.shape[1]: raise RuntimeError(f'title/schema mismatch {p}: nums={nums} titles={titles} shape={a.shape}')
    if len(titles)!=len(set(titles)): raise RuntimeError(f'duplicate titles {p}')
    return titles,a

def segment_table(p:Path):
    titles,a=parse_table(p)
    if 'tau [Mpc]' not in titles or 'a' not in titles: raise RuntimeError(f'missing coordinates {p}')
    tau=a[:,titles.index('tau [Mpc]')]; sc=a[:,titles.index('a')]
    if np.any(~np.isfinite(tau)) or np.any(~np.isfinite(sc)) or np.any(tau<=0) or np.any(sc<=0): raise RuntimeError(f'nonfinite/nonpositive coordinates {p}')
    dt=np.diff(tau); da=np.diff(sc)
    if np.any(dt<0) or np.any(da<0): raise RuntimeError(f'negative coordinate step {p}')
    zt=(dt==0); za=(da==0)
    if not np.array_equal(zt,za): raise RuntimeError(f'tau/a duplicate topology mismatch {p}')
    seams=np.where(zt)[0]
    if len(seams)!=EXPECTED_SEAMS: raise RuntimeError(f'expected {EXPECTED_SEAMS} seams, got {len(seams)} in {p}: {seams.tolist()}')
    if any(int(seams[i+1])==int(seams[i])+1 for i in range(len(seams)-1)): raise RuntimeError(f'duplicate multiplicity >2 in {p}: {seams.tolist()}')
    starts=[0]+[int(i)+1 for i in seams]; stops=[int(i)+1 for i in seams]+[a.shape[0]]
    segments=[]
    for si,(s,e) in enumerate(zip(starts,stops)):
        seg=a[s:e]
        if seg.shape[0]<1: raise RuntimeError(f'empty segment {p}/{si}')
        t=seg[:,titles.index('tau [Mpc]')]; x=seg[:,titles.index('a')]
        if seg.shape[0]>1 and (np.any(np.diff(t)<=0) or np.any(np.diff(x)<=0)): raise RuntimeError(f'non-strict segment {p}/{si}')
        segments.append(seg)
    seam_meta=[]
    for i in seams:
        row0=a[int(i)]; row1=a[int(i)+1]
        state_delta=float(np.max(np.abs(row1[2:]-row0[2:]))) if a.shape[1]>2 else 0.0
        seam_meta.append({'left_row_index':int(i),'right_row_index':int(i)+1,'tau_Mpc':float(row0[titles.index('tau [Mpc]')]),'a':float(row0[titles.index('a')]),'max_abs_state_jump':state_delta})
    return titles,segments,seam_meta

def file_map(base:Path,meta:dict,case:str):
    out={}
    for rel in meta['perturbation_files'][case]:
        p=base/rel; m=re.search(r'perturbations_k(\d+)_s\.dat$',p.name)
        if not m: raise RuntimeError(f'unexpected perturbation filename {p}')
        idx=int(m.group(1))
        if idx in out: raise RuntimeError(f'duplicate k index {case}/{idx}')
        out[idx]=p
    if sorted(out)!=list(range(5)): raise RuntimeError(f'k index set {case}: {sorted(out)}')
    return out

def piecewise_dist(pA:Path,pB:Path,variables:list[str]):
    tA,segsA,seamsA=segment_table(pA); tB,segsB,seamsB=segment_table(pB)
    if len(segsA)!=4 or len(segsB)!=4: raise RuntimeError(f'segment topology mismatch {pA}/{pB}')
    for q in ['a']+variables:
        if q not in tA or q not in tB: raise RuntimeError(f'missing {q} in pair {pA}/{pB}')
    iaA=tA.index('a'); iaB=tB.index('a')
    accum={v:{'diff2':0.0,'a2':0.0,'b2':0.0,'n':0,'segments_used':0,'segments_skipped':0} for v in variables}
    for segA,segB in zip(segsA,segsB):
        xa=segA[:,iaA]; xb=segB[:,iaB]
        ma=(xa>=A_LO)&(xa<=A_HI); mb=(xb>=A_LO)&(xb<=A_HI)
        xa=xa[ma]; xb=xb[mb]; AA=segA[ma]; BB=segB[mb]
        if xa.size<2 or xb.size<2:
            for v in variables: accum[v]['segments_skipped']+=1
            continue
        lo=max(float(xa.min()),float(xb.min())); hi=min(float(xa.max()),float(xb.max()))
        keep=(xa>=lo)&(xa<=hi); x=xa[keep]; AA=AA[keep]
        if x.size<2:
            for v in variables: accum[v]['segments_skipped']+=1
            continue
        lx=np.log(x); lxb=np.log(xb)
        for v in variables:
            ya=AA[:,tA.index(v)]; yb=np.interp(lx,lxb,BB[:,tB.index(v)])
            ac=accum[v]; ac['diff2']+=float(np.dot(ya-yb,ya-yb)); ac['a2']+=float(np.dot(ya,ya)); ac['b2']+=float(np.dot(yb,yb)); ac['n']+=int(x.size); ac['segments_used']+=1
    out={}
    for v,ac in accum.items():
        if ac['n']<16: raise RuntimeError(f'insufficient piecewise overlap {v} in {pA}/{pB}: n={ac["n"]}')
        d=float(math.sqrt(ac['diff2'])/max(math.sqrt(ac['a2']),math.sqrt(ac['b2']),1e-300))
        out[v]={'D':d,'n':ac['n'],'segments_used':ac['segments_used'],'segments_skipped':ac['segments_skipped']}
    return out,{'A':seamsA,'B':seamsB}

def summarize_cells(cells):
    cells.sort(key=lambda x:x['J'],reverse=True)
    return {'Jmax':cells[0]['J'],'top_cell':cells[0],'localized_cell_count':sum(x['localized'] for x in cells),'cell_count':len(cells),'localized':any(x['localized'] for x in cells),'top10':cells[:10]}

def analyze_edge(edge,lane_dirs,metas):
    A,B=edge; maps={(lane,c):file_map(lane_dirs[lane],metas[lane],c) for lane in [A,B] for c in CASES}
    common_cells=[]; ncdm_cells=[]; seam_report={}
    for ki in range(5):
        common_by_case={}; ncdm_by_case={}
        for c in CASES:
            vars_here=COMMON+(NCDM if c!='ref' else [])
            ds,seams=piecewise_dist(maps[(A,c)][ki],maps[(B,c)][ki],vars_here)
            seam_report[f'{c}:k{ki}']=seams
            common_by_case[c]={v:ds[v] for v in COMMON}
            if c!='ref': ncdm_by_case[c]={v:ds[v] for v in NCDM}
        for v in COMMON:
            d={c:common_by_case[c][v]['D'] for c in CASES}; n={c:common_by_case[c][v]['n'] for c in CASES}
            J=float(d['f3']/max(d['ref'],d['f2'],d['f4'],J_FLOOR))
            common_cells.append({'k_index':ki,'title':v,'J':J,'distances':d,'n_overlap':n,'localized':J>=J_THRESHOLD})
        for v in NCDM:
            d={c:ncdm_by_case[c][v]['D'] for c in ['f2','f3','f4']}; n={c:ncdm_by_case[c][v]['n'] for c in ['f2','f3','f4']}
            J=float(d['f3']/max(d['f2'],d['f4'],J_FLOOR))
            ncdm_cells.append({'k_index':ki,'title':v,'J':J,'distances':d,'n_overlap':n,'localized':J>=J_THRESHOLD})
    return summarize_cells(common_cells),summarize_cells(ncdm_cells),seam_report

def main(root:Path,config_path:Path,out:Path):
    cfg=json.load(open(config_path)); result={'schema':'KMDSB.W04.M21.PerturbationStateSeamRecovery.v0.1','protocol':PROTOCOL,'parent_protocol':PARENT_PROTOCOL,'parent_run_id':PARENT_RUN,'parent_aggregate_artifact_id':PARENT_AGG_ARTIFACT,'parent_aggregate_digest':PARENT_AGG_DIGEST,'provider':f'lesgourg/class_public@{PIN}','J_floor':J_FLOOR,'J_threshold':J_THRESHOLD,'a_window':[A_LO,A_HI],'expected_seams_per_table':EXPECTED_SEAMS,'K1_promoted':False,'K3_promoted':False,'K4_promoted':False,'physical_falsification':False}
    try:
        metas={}; lane_dirs={}
        for mp in root.rglob('lane_meta.json'):
            m=json.load(open(mp)); lane=m.get('lane')
            if lane in metas: raise RuntimeError(f'duplicate lane meta {lane}')
            metas[lane]=m; lane_dirs[lane]=mp.parent
        if set(metas)!=set(LANES): raise RuntimeError(f'lane set mismatch {sorted(metas)}')
        csha=H(config_path)
        req=[float(x) for x in cfg['k_anchors_12sig_Mpc_inv']]
        for lane,m in metas.items():
            if m.get('provider_head')!=PIN or not m.get('exact_head') or not m.get('all_cases_rc0') or not m.get('five_files_each') or not m.get('physical_lines_preserved'): raise RuntimeError(f'lane integrity failed {lane}')
            if m.get('config_sha256')!=csha or m.get('profile_manifest',{}).get('lane')!=lane: raise RuntimeError(f'input identity failed {lane}')
            for c in CASES:
                fm=file_map(lane_dirs[lane],m,c); actual=m['actual_k_Mpc_inv'][c]
                if len(actual)!=5: raise RuntimeError(f'actual-k count {lane}/{c}')
                for ki in range(5):
                    if abs(float(actual[ki])-req[ki])/req[ki]>0.05: raise RuntimeError(f'actual-k mismatch {lane}/{c}/{ki}')
                    titles,segs,seams=segment_table(fm[ki]); needed=['tau [Mpc]','a']+COMMON+(NCDM if c!='ref' else [])
                    miss=[x for x in needed if x not in titles]
                    if miss: raise RuntimeError(f'missing titles {lane}/{c}/{ki}: {miss}')
                    if len(segs)!=4 or len(seams)!=3: raise RuntimeError(f'seam topology failed {lane}/{c}/{ki}')
                if lane!=LANES[0]:
                    base=metas[LANES[0]]['actual_k_Mpc_inv'][c]
                    for ki,(x,y) in enumerate(zip(base,actual)):
                        if abs(float(x)-float(y))/max(abs(float(x)),1e-300)>1e-12: raise RuntimeError(f'cross-lane actual-k drift {c}/{ki}: {x}/{y}')
        edges={}
        for A,B in BRANCH+CONTROL:
            common,ncdm,seams=analyze_edge((A,B),lane_dirs,metas); name=f'{A}__{B}'
            edges[name]={'kind':'branch_change' if (A,B) in BRANCH else 'same_branch_control','common':common,'ncdm':ncdm,'edge_localized':bool(common['localized'] or ncdm['localized']),'seam_report':seams}
        nb=sum(edges[f'{a}__{b}']['edge_localized'] for a,b in BRANCH); nc=sum(edges[f'{a}__{b}']['edge_localized'] for a,b in CONTROL)
        if nb==4 and nc==0: cls='M21_PERTURBATION_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE'
        elif nb>=2: cls='M21_PERTURBATION_STATE_BRANCH_SIGNATURE_PARTIAL'
        else: cls='M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES'
        result.update({'classification':cls,'seam_recovery_passed':True,'cross_lane_input_identity':True,'branch_change_localized_count':int(nb),'same_branch_control_localized_count':int(nc),'branch_change_edges':[f'{a}__{b}' for a,b in BRANCH],'same_branch_control_edges':[f'{a}__{b}' for a,b in CONTROL],'edges':edges,'k_anchors_requested_Mpc_inv':req,'capability_artifact_id':cfg['capability_artifact_id'],'capability_digest':cfg['capability_digest']})
    except Exception as e:
        result.update({'classification':'M21_PERTURBATION_STATE_SEAM_RECOVERY_BLOCKED','seam_recovery_passed':False,'cross_lane_input_identity':False,'error':repr(e)})
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'classification':result['classification'],'branch_change_localized_count':result.get('branch_change_localized_count'),'same_branch_control_localized_count':result.get('same_branch_control_localized_count'),'error':result.get('error')},indent=2,sort_keys=True))
    if result['classification'].endswith('BLOCKED'): raise SystemExit(1)

if __name__=='__main__':
    if len(sys.argv)!=4: raise SystemExit('usage: perturbation_state_branch_signature_seam_recovery.py LANES_ROOT CONFIG OUT')
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
