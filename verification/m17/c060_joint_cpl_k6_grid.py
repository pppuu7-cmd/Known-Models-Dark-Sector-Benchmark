#!/usr/bin/env python3
"""Prepare/analyze preregistered M17 c=0.6 joint H(a)+CMB CPL K6 coarse grid."""
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path

W0C=-1.299870066355541
WAC=+0.9082964747357177
DW0=[-0.20,-0.10,0.0,+0.10,+0.20]
DWA=[-0.40,-0.20,0.0,+0.20,+0.40]
LIKES=[
 'DEFAULT(batch3/plik_rd12_HM_v22_TTTEEE.ini)',
 'DEFAULT(batch3/lowl.ini)',
 'DEFAULT(batch3/lowE.ini)',
 'DEFAULT(batch3/lensing.ini)',
 'DEFAULT(batch3/BAO.ini)',
 'DEFAULT(batch3/Pantheon18.ini)',
]

def replace_one(s,old,new):
    n=s.count(old)
    if n!=1: raise RuntimeError(f'anchor {old!r} count={n}')
    return s.replace(old,new,1)

def replace_active_key(s,key,value):
    pat=re.compile(rf'(?m)^(\s*{re.escape(key)}\s*=).*?$')
    ms=list(pat.finditer(s))
    if len(ms)!=1: raise RuntimeError(f'active key {key} count={len(ms)}')
    return pat.sub(lambda m:f'{m.group(1)} {value}',s,count=1)

def cases():
    out={'r0':{'kind':'cpl','w0':-1.0,'w1':0.0},'h06':{'kind':'hde','c':0.6}}
    for i,d0 in enumerate(DW0):
        for j,da in enumerate(DWA):
            out[f'g{i}{j}']={'kind':'cpl','w0':W0C+d0,'w1':WAC+da,'dw0':d0,'dwa':da}
    return out

CASES=cases()

def prepare(base:Path,outdir:Path):
    raw=base.read_text()
    for x in LIKES: raw=replace_one(raw,x,'#'+x)
    raw=replace_one(raw,'DEFAULT(batch3/common.ini)','DEFAULT(batch3/common.ini)\nuse_nonlinear_lensing = F')
    raw=replace_one(raw,'#Use_PPF = F','Use_PPF = T')
    raw=replace_one(raw,'test_check_compare = 1820.775','#test_check_compare = 1820.775')
    raw=replace_one(raw,'#test_output_root = output_ide','test_output_root = PLACEHOLDER')
    outdir.mkdir(parents=True,exist_ok=True)
    for name,cfg in CASES.items():
        s=raw.replace('test_output_root = PLACEHOLDER',f'test_output_root = m17k6_{name}')
        s=replace_active_key(s,'param[beta_cf]','0')
        if cfg['kind']=='hde':
            s=replace_active_key(s,'WForm_CF','2')
            s=replace_active_key(s,'param[c_hde]',repr(cfg['c']))
        else:
            s=replace_active_key(s,'WForm_CF','1')
            s=replace_active_key(s,'param[w0]',repr(cfg['w0']))
            s=replace_active_key(s,'param[w1]',repr(cfg['w1']))
        (outdir/f'{name}.ini').write_text(s)
    (outdir/'manifest.json').write_text(json.dumps(CASES,indent=2,sort_keys=True)+'\n')

def _nums(line):
    return [float(x) for x in line.replace('D','E').replace('d','e').split()]

def parse_theory(path:Path):
    rows=[]
    for raw in path.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        try: xs=_nums(s)
        except ValueError: continue
        if len(xs)!=4: raise RuntimeError(f'{path}: expected 4 numeric columns, got {len(xs)}')
        if not all(math.isfinite(x) for x in xs): raise RuntimeError(f'{path}: nonfinite theory row')
        rows.append(xs)
    if len(rows)<2000: raise RuntimeError(f'{path}: only {len(rows)} theory rows')
    return rows

def parse_quantity(path:Path):
    rows=[]
    for raw in path.read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        try: xs=_nums(s)
        except ValueError: continue
        if len(xs)!=11: raise RuntimeError(f'{path}: expected 11 quantity columns, got {len(xs)}')
        if not all(math.isfinite(x) for x in xs[:7]):
            raise RuntimeError(f'{path}: nonfinite in HDE/CPL quantity columns 1-7')
        rows.append(xs[:7])
    if len(rows)!=2000: raise RuntimeError(f'{path}: expected 2000 quantity rows, got {len(rows)}')
    return rows

def norm(v): return math.sqrt(sum(x*x for x in v))

def analyze(workdir:Path,status_path:Path,out:Path):
    status=json.loads(status_path.read_text())
    theory={}; quant={}; problems=[]; isolation={}
    for name in CASES:
        log=workdir.parent/f'm17k6_{name}.log'
        txt=log.read_text(errors='replace') if log.exists() else ''
        isolation[name]='Doing non-linear lensing: F' in txt
        rc=int(status.get(name,999))
        if rc!=0: problems.append(f'{name}:exit={rc}')
        if not isolation[name]: problems.append(f'{name}:nonlinear-lensing-isolation-missing')
        try: theory[name]=parse_theory(workdir/f'm17k6_{name}.theory_cl')
        except Exception as e: problems.append(f'{name}:theory:{e}')
        try: quant[name]=parse_quantity(workdir/f'm17k6_{name}.quantity')
        except Exception as e: problems.append(f'{name}:quantity:{e}')
    if not problems:
        ell0=[int(round(r[0])) for r in theory['r0']]
        a0=[r[0] for r in quant['r0']]
        for name in CASES:
            if [int(round(r[0])) for r in theory[name]]!=ell0: problems.append(f'{name}:ell-grid-mismatch')
            aq=[r[0] for r in quant[name]]
            if len(aq)!=len(a0) or max(abs(x-y) for x,y in zip(aq,a0))>1e-14:
                problems.append(f'{name}:a-grid-mismatch')
    result={
      'schema':'KMDSB.M17.c060.jointCPLK6.coarse.v1',
      'provider':{'cosmomc':'eb08c2fe91d9711929802fede310ae58c020fcb4','idecamb':'4f1093d9efe46f28cf7e2acb4d07ae116ad5e075'},
      'target':{'model':'HDE','c':0.6},
      'grid':{'center':{'w0':W0C,'wa':WAC},'delta_w0':DW0,'delta_wa':DWA,'n':25},
      'status':status,'linear_isolation_flags':isolation,
      'physical_falsification':False,'observational_significance_claim':False,
      'preregistration':'protocol/W03_M17_C060_JOINT_CPL_K6_COARSE_GRID_PREREGISTRATION_v0.1.md'
    }
    if problems:
        result['classification']='M17_C060_K6_COARSE_OUTPUT_BLOCKED'; result['problems']=problems
        out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); return
    # Frozen four blocks. quantity column 5 is adotoa => Python index 4.
    blocks={
      'H':([r[4] for r in quant['h06']],[r[4] for r in quant['r0']]),
      'TT':([r[1] for r in theory['h06']],[r[1] for r in theory['r0']]),
      'TE':([r[2] for r in theory['h06']],[r[2] for r in theory['r0']]),
      'EE':([r[3] for r in theory['h06']],[r[3] for r in theory['r0']]),
    }
    targets={b:[x-y for x,y in zip(h,r)] for b,(h,r) in blocks.items()}
    tnorm={b:norm(v) for b,v in targets.items()}
    identifiable={b:(n>1e-20) for b,n in tnorm.items()}
    result['target_response_norms']=tnorm; result['identifiable_blocks']=identifiable
    cand=[]
    for name,cfg in CASES.items():
        if not name.startswith('g'): continue
        Rs={}
        for b in ('H','TT','TE','EE'):
            if not identifiable[b]: continue
            if b=='H': p=[r[4] for r in quant[name]]
            else:
                col={'TT':1,'TE':2,'EE':3}[b]; p=[r[col] for r in theory[name]]
            h=blocks[b][0]
            Rs[b]=norm([x-y for x,y in zip(h,p)])/tnorm[b]
        vals=list(Rs.values())
        rjoint=math.sqrt(sum(x*x for x in vals)/len(vals)); rmax=max(vals)
        cand.append({'case':name,'w0':cfg['w0'],'wa':cfg['w1'],'delta_w0':cfg['dw0'],'delta_wa':cfg['dwa'],'R_blocks':Rs,'R_joint':rjoint,'R_max':rmax})
    cand.sort(key=lambda x:(x['R_joint'],x['R_max'],x['case']))
    best=cand[0]; ties=[x for x in cand if abs(x['R_joint']-best['R_joint'])<=1e-12]
    if best['R_joint']<=0.10 and best['R_max']<=0.20:
        cl='M17_C060_K6_COARSE_STRONG_ABSORPTION'
    elif best['R_joint']<=0.30 and best['R_max']<=0.50:
        cl='M17_C060_K6_COARSE_PARTIAL_ABSORPTION'
    else:
        cl='M17_C060_K6_COARSE_SURVIVOR_CANDIDATE'
    result['classification']=cl; result['best']=best; result['ties_within_1e-12']=ties
    result['candidates']=cand
    result['next']='run preregistered 5x5 refinement centered on coarse p*; no K6 terminal promotion from coarse grid alone'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare'); p.add_argument('base',type=Path); p.add_argument('outdir',type=Path)
    a=sp.add_parser('analyze'); a.add_argument('workdir',type=Path); a.add_argument('status',type=Path); a.add_argument('output',type=Path)
    ns=ap.parse_args()
    prepare(ns.base,ns.outdir) if ns.cmd=='prepare' else analyze(ns.workdir,ns.status,ns.output)
