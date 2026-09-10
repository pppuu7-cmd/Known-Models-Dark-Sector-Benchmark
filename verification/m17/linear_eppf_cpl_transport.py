#!/usr/bin/env python3
"""Prepare/analyze M17 preregistered linear-ePPF background-CPL transport attack."""
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path

CASES={
 'r0': {'kind':'cpl','w0':-1.0,'w1':0.0},
 'h06':{'kind':'hde','c':0.6}, 'c06':{'kind':'cpl','w0':-1.299870066355541,'w1':0.9082964747357177},
 'h08':{'kind':'hde','c':0.8}, 'c08':{'kind':'cpl','w0':-1.0616652253607164,'w1':0.5962733794216544},
 'h10':{'kind':'hde','c':1.0}, 'c10':{'kind':'cpl','w0':-0.9167034662101682,'w1':0.4297783543420696},
 'h12':{'kind':'hde','c':1.2}, 'c12':{'kind':'cpl','w0':-0.8194180077420152,'w1':0.3292670947586294},
}
PAIRS=[('06','h06','c06'),('08','h08','c08'),('10','h10','c10'),('12','h12','c12')]

LIKES=['DEFAULT(batch3/plik_rd12_HM_v22_TTTEEE.ini)','DEFAULT(batch3/lowl.ini)','DEFAULT(batch3/lowE.ini)','DEFAULT(batch3/lensing.ini)','DEFAULT(batch3/BAO.ini)','DEFAULT(batch3/Pantheon18.ini)']

def replace_one(s, old, new):
    n=s.count(old)
    if n!=1: raise RuntimeError(f'anchor {old!r} count={n}')
    return s.replace(old,new,1)

def replace_active_key(s,key,value):
    pat=re.compile(rf'(?m)^(\s*{re.escape(key)}\s*=).*?$')
    ms=list(pat.finditer(s))
    if len(ms)!=1: raise RuntimeError(f'active key {key} count={len(ms)}')
    return pat.sub(lambda m:f'{m.group(1)} {value}',s,count=1)

def prepare(base:Path,outdir:Path):
    raw=base.read_text()
    for x in LIKES:
        raw=replace_one(raw,x,'#'+x)
    raw=replace_one(raw,'DEFAULT(batch3/common.ini)','DEFAULT(batch3/common.ini)\nuse_nonlinear_lensing = F')
    raw=replace_one(raw,'#Use_PPF = F','Use_PPF = T')
    raw=replace_one(raw,'test_check_compare = 1820.775','#test_check_compare = 1820.775')
    raw=replace_one(raw,'#test_output_root = output_ide','test_output_root = PLACEHOLDER')
    outdir.mkdir(parents=True,exist_ok=True)
    manifest={}
    for name,cfg in CASES.items():
        s=raw.replace('test_output_root = PLACEHOLDER',f'test_output_root = m17tr_{name}')
        s=replace_active_key(s,'param[beta_cf]','0')
        if cfg['kind']=='hde':
            s=replace_active_key(s,'WForm_CF','2')
            s=replace_active_key(s,'param[c_hde]',repr(cfg['c']))
        else:
            s=replace_active_key(s,'WForm_CF','1')
            s=replace_active_key(s,'param[w0]',repr(cfg['w0']))
            s=replace_active_key(s,'param[w1]',repr(cfg['w1']))
        p=outdir/f'{name}.ini'; p.write_text(s)
        manifest[name]=cfg
    (outdir/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')

def parse_theory(path:Path):
    rows=[]
    for raw in path.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        parts=s.replace('D','E').replace('d','e').split()
        try: xs=[float(x) for x in parts]
        except ValueError: continue
        if len(xs)!=4: raise RuntimeError(f'{path}: expected 4 numeric columns, got {len(xs)}')
        if not all(math.isfinite(x) for x in xs): raise RuntimeError(f'{path}: nonfinite row')
        rows.append(xs)
    if len(rows)<2000: raise RuntimeError(f'{path}: only {len(rows)} rows')
    return rows

def norm(v): return math.sqrt(sum(x*x for x in v))
def angle(a,b):
    na,nb=norm(a),norm(b)
    if na<=1e-20 or nb<=1e-20: return None
    c=sum(x*y for x,y in zip(a,b))/(na*nb); c=max(-1.0,min(1.0,c))
    return math.degrees(math.acos(c))

def analyze(workdir:Path,status_path:Path,out:Path):
    status=json.loads(status_path.read_text())
    tables={}; problems=[]; flags={}
    for name in CASES:
        log=(workdir.parent/f'm17tr_{name}.log')
        txt=log.read_text(errors='replace') if log.exists() else ''
        flags[name]='Doing non-linear lensing: F' in txt
        rc=int(status.get(name,999))
        if rc!=0: problems.append(f'{name}:exit={rc}')
        if not flags[name]: problems.append(f'{name}:nonlinear-lensing-isolation-missing')
        p=workdir/f'm17tr_{name}.theory_cl'
        try: tables[name]=parse_theory(p)
        except Exception as e: problems.append(f'{name}:{e}')
    if not problems:
        L0=[int(round(r[0])) for r in tables['r0']]
        for name,t in tables.items():
            if [int(round(r[0])) for r in t]!=L0: problems.append(f'{name}:ell-grid-mismatch')
    result={'schema':'KMDSB.M17.linearEPPF.backgroundCPLtransport.v1','provider':{'cosmomc':'eb08c2fe91d9711929802fede310ae58c020fcb4','idecamb':'4f1093d9efe46f28cf7e2acb4d07ae116ad5e075'},'status':status,'linear_isolation_flags':flags,'pairs':{},'physical_falsification':False,'observational_significance_claim':False}
    if problems:
        result['classification']='M17_LINEAR_EPPF_TRANSPORT_OUTPUT_BLOCKED'; result['problems']=problems
        out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); return
    channels={'TT':1,'TE':2,'EE':3}; labels=[]
    for lab,hname,pname in PAIRS:
        chres={}; Rs=[]
        for ch,col in channels.items():
            h=[rh[col]-rr[col] for rh,rr in zip(tables[hname],tables['r0'])]
            p=[rp[col]-rr[col] for rp,rr in zip(tables[pname],tables['r0'])]
            e=[rh[col]-rp[col] for rh,rp in zip(tables[hname],tables[pname])]
            hn,pn,en=norm(h),norm(p),norm(e)
            if hn<=1e-20:
                chres[ch]={'identifiable':False,'hde_response_norm':hn}
                continue
            R=en/hn; Rs.append(R)
            chres[ch]={'identifiable':True,'hde_response_norm':hn,'cpl_response_norm':pn,'residual_norm':en,'residual_fraction':R,'response_angle_deg':angle(h,p)}
        req=math.sqrt(sum(r*r for r in Rs)/len(Rs)) if Rs else None
        rmax=max(Rs) if Rs else None
        if req is None:
            label='NONIDENTIFIABLE'
        elif req<=0.10 and rmax<=0.20:
            label='PERTURBATION_TRANSPORT_STRONGLY_ABSORBED_BY_BACKGROUND_CPL'
        elif req<=0.30 and rmax<=0.50:
            label='PERTURBATION_TRANSPORT_PARTIALLY_ABSORBED_BY_BACKGROUND_CPL'
        else:
            label='PERTURBATION_RESPONSE_SURVIVES_BACKGROUND_CPL_TRANSPORT_ATTACK'
        labels.append(label)
        result['pairs'][lab]={'hde_case':hname,'cpl_case':pname,'channels':chres,'R_equal':req,'R_max':rmax,'classification':label}
    strong='PERTURBATION_TRANSPORT_STRONGLY_ABSORBED_BY_BACKGROUND_CPL'; survive='PERTURBATION_RESPONSE_SURVIVES_BACKGROUND_CPL_TRANSPORT_ATTACK'
    if labels and all(x==strong for x in labels): agg='M17_LINEAR_EPPF_BACKGROUND_CPL_TRANSPORT_STRONG'
    elif labels and all(x==survive for x in labels): agg='M17_LINEAR_EPPF_PERTURBATION_RESPONSE_SURVIVES_BACKGROUND_CPL_TRANSPORT'
    else: agg='M17_LINEAR_EPPF_BACKGROUND_CPL_TRANSPORT_MIXED'
    result['classification']=agg
    result['interpretation']='fixed background-derived CPL mapping only; full perturbation-manifold refit and covariance K7 remain open'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare'); p.add_argument('base',type=Path); p.add_argument('outdir',type=Path)
    a=sp.add_parser('analyze'); a.add_argument('workdir',type=Path); a.add_argument('status',type=Path); a.add_argument('output',type=Path)
    ns=ap.parse_args()
    prepare(ns.base,ns.outdir) if ns.cmd=='prepare' else analyze(ns.workdir,ns.status,ns.output)
