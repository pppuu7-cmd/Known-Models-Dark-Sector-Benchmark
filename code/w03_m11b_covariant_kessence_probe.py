#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, re
from pathlib import Path
import numpy as np

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
K=np.array([0.001,0.003,0.01,0.03,0.1],float)
MS=[0.5,1.0,2.0,4.0]


def zhdr(path):
    with open(path) as f:
        for _ in range(30):
            s=f.readline()
            m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m:return float(m.group(1))
    raise ValueError(f'no redshift header: {path}')


def load_pk(d,prefix):
    rows=[]
    for p in glob.glob(str(Path(d)/f'{prefix}*pk.dat')):
        a=np.loadtxt(p,comments='#')
        rows.append((zhdr(p),np.exp(np.interp(np.log(K),np.log(a[:,0]),np.log(a[:,1])))))
    rows.sort(key=lambda x:x[0])
    if len(rows)!=len(Z) or not np.allclose([r[0] for r in rows],Z,atol=1e-9,rtol=0):
        raise ValueError(f'bad P grid {prefix}: {[r[0] for r in rows]}')
    return np.vstack([r[1] for r in rows])


def titles(path):
    txt=''
    with open(path) as f:
        for _ in range(80):
            s=f.readline()
            if not s or not s.startswith('#'):break
            txt+=' '+s[1:].strip()
    ms=list(re.finditer(r'(?:^|\s)(\d+):',txt)); out={}
    for i,m in enumerate(ms):
        out[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return out


def bg(d,prefix):
    hits=list(Path(d).glob(f'{prefix}*background.dat'))
    if len(hits)!=1:raise ValueError(f'background {prefix}: {hits}')
    t=titles(hits[0]); a=np.loadtxt(hits[0],comments='#')
    def idx(pred):return next(i for i,x in t.items() if pred(x))
    iz=idx(lambda x:x.startswith('z'))
    ih=idx(lambda x:'H [1/Mpc]' in x)
    cols={'z':a[:,iz],'H':a[:,ih]}
    for key,needle in [('w','w_gsf'),('cs2','cs2_gsf'),('Akin','A_gsf')]:
        matches=[i for i,x in t.items() if needle in x and 'gsf2' not in x]
        cols[key]=a[:,matches[0]] if matches else None
    return cols


def Hinterp(B):
    j=np.argsort(B['z']);return np.interp(Z,B['z'][j],B['H'][j])


def geo(a,b):
    na=np.linalg.norm(a);nb=np.linalg.norm(b)
    if na==0 or nb==0:return {'cosine':None,'acute_deg':None,'oriented_deg':None}
    c=float(np.dot(a,b)/(na*nb));c=max(-1,min(1,c))
    return {'cosine':c,'oriented_deg':float(np.degrees(np.arccos(c))),'acute_deg':float(np.degrees(np.arccos(abs(c))))}


def tag(m,cs):
    ms=str(m).replace('.','p');csn={1.0:'100',0.95:'095',0.90:'090'}[cs]
    return f'm{ms}_c{csn}'


def stability(B,expected_cs):
    if B['w'] is None or B['cs2'] is None or B['Akin'] is None:
        return {'pass':False,'reason':'required_gsf_background_columns_missing'}
    z=B['z'];j0=int(np.argmin(np.abs(z)))
    finite=bool(np.all(np.isfinite(B['w'])) and np.all(np.isfinite(B['cs2'])) and np.all(np.isfinite(B['Akin'])))
    minA=float(np.nanmin(B['Akin']));mincs=float(np.nanmin(B['cs2']));maxcs=float(np.nanmax(B['cs2']))
    w0=float(B['w'][j0]);cs0=float(B['cs2'][j0])
    cs_match=bool(abs(cs0-expected_cs)<=5e-3)
    ok=bool(finite and minA>0 and mincs>0 and cs_match)
    return {'pass':ok,'finite':finite,'min_A_gsf':minA,'min_cs2_gsf':mincs,'max_cs2_gsf':maxcs,'w_near_z0':w0,'cs2_near_z0':cs0,'expected_cs2':expected_cs,'cs2_match_5e-3':cs_match}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--directory',required=True);ap.add_argument('--effective-result',required=True);ap.add_argument('--json',required=True);x=ap.parse_args();d=Path(x.directory)
    tags=['lcdm','gsf_ref']+[tag(m,cs) for m in MS for cs in (1.0,.95,.90)]
    P={t:load_pk(d,t+'_') for t in tags};B={t:bg(d,t+'_') for t in tags};H={t:Hinterp(B[t]) for t in tags}
    refP=np.log(P['gsf_ref']/P['lcdm']).reshape(-1);refH=np.log(H['gsf_ref']/H['lcdm'])
    refpass=bool(np.max(np.abs(refP))<=1e-5 and np.max(np.abs(refH))<=1e-7)

    cand=[];diagnostics={}
    for m in MS:
        t=tag(m,1.0);s=stability(B[t],1.0);diagnostics[t]=s
        if s['pass'] and -0.99<=s['w_near_z0']<=-0.80:
            cand.append((abs(s['w_near_z0']+0.95),m))
    cand.sort(key=lambda q:(q[0],q[1]))
    selected=cand[0][1] if cand else None

    out={'schema':'KMDSB.W03.M11b.CovariantKessenceProbe.v0.1','solver':'KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7','model_gsf':6,'reference':{'max_abs_lnP':float(np.max(np.abs(refP))),'max_abs_lnH':float(np.max(np.abs(refH))),'passes':refpass},'anchor_scan':{'m_values':MS,'diagnostics_cs2_1':diagnostics,'selected_m':selected,'selection_rule':'usable stable w in [-.99,-.80], minimize |w+0.95|, tie lower m'}}

    if selected is None:
        out.update({'classification':'M11B_NO_USABLE_COVARIANT_ANCHOR_WITH_SCOPE','probe_pass':False,'interpretation':'implementation/geometry probe only; not a k-essence falsification'})
    else:
        ta=tag(selected,1.0);t05=tag(selected,.95);t10=tag(selected,.90)
        s05=stability(B[t05],.95);s10=stability(B[t10],.90)
        baseP=P[ta];baseH=H[ta]
        def resp(t):return np.log(P[t]/baseP).reshape(-1),np.log(H[t]/baseH)
        p05,h05=resp(t05);p10,h10=resp(t10)
        j05=np.r_[p05/.05,h05/.05];j10=np.r_[p10/.10,h10/.10]
        rel=float(np.linalg.norm(j05-j10)/max(np.linalg.norm(j05),1e-30));g=geo(j05,j10)
        nonnull=bool(np.linalg.norm(p05/.05)>1e-8)
        conv=bool(rel<=.25 and g['acute_deg'] is not None and g['acute_deg']<=5)
        stable=bool(diagnostics[ta]['pass'] and s05['pass'] and s10['pass'])
        eff=json.load(open(x.effective_result));e=eff['directions']['sound_speed_qs_h005'];je=np.r_[np.array(e['P']),np.array(e['H'])]
        eg=geo(j05,je)
        c=float(np.dot(je,j05)/np.dot(je,je)) if np.dot(je,je)>0 else None
        er=float(np.linalg.norm(j05-c*je)/np.linalg.norm(j05)) if c is not None and np.linalg.norm(j05)>0 else None
        passed=bool(refpass and stable and nonnull and conv)
        out.update({'selected_branch':{'m':selected,'anchor':diagnostics[ta],'cs2_095':s05,'cs2_090':s10},'sound_speed_direction':{'norm_P_h005':float(np.linalg.norm(p05/.05)),'norm_PH_h005':float(np.linalg.norm(j05)),'relative_step_difference':rel,'step_geometry':g,'nonnull_P':nonnull,'convergence_pass':conv},'diagnostic_vs_effective_M11':{'geometry':eg,'best_effective_line_coefficient':c,'covariant_residual_after_effective_line_projection':er,'classifying':False},'probe_pass':passed,'classification':'PROBE_PASS_READY_FOR_MATCHED_PRODUCTION' if passed else 'M11B_COVARIANT_PROBE_NOT_READY_WITH_SCOPE','interpretation':'covariant implementation probe only; no K7/K8 observational claim'})
    Path(x.json).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
