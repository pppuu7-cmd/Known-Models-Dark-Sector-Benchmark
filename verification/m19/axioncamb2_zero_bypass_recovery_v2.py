#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path

TOL=1e-12
FILES=['scalCls.dat','matterpower.dat','transfer_out.dat']
PIN='891e779cc0bd422e49f97533e6c2fc761149737d'


def replace_once(text, old, new, label):
    n=text.count(old)
    if n!=1: raise RuntimeError(f'{label}: expected one anchor, found {n}')
    return text.replace(old,new,1)


def patch(src:Path):
    ini=src/'inidriver_axion.F90'
    s=ini.read_text()
    old='call   w_evolve(P, badflag)'
    new='''if (P%omegaax .eq. 0._dl) then
   P%a_osc = 0._dl
   P%drefp_hsq = 0._dl
   P%phiinit = 0._dl
   P%ainit = 0._dl
   P%aeq = 0._dl
   P%omegar = P%omegah2_rad / ((P%H0/100._dl)**2)
   badflag = 0
else
   call   w_evolve(P, badflag)
endif'''
    ini.write_text(replace_once(s,old,new,'inidriver zero bypass'))

    rec=src/'recfast_axion.f90'
    s=rec.read_text()
    old1='''deriv_eps=1.d-3*real(sfac)
call spline_out(loga_table,grhoax_table,grhoax_table_buff,ntable,dlog10(sfac+deriv_eps),gr)'''
    new1='''deriv_eps=1.d-3*real(sfac)
if (OmegaAx .eq. 0._dl) then
   dorpa=0._dl
else
call spline_out(loga_table,grhoax_table,grhoax_table_buff,ntable,dlog10(sfac+deriv_eps),gr)'''
    s=replace_once(s,old1,new1,'recfast zero derivative open')
    old2=''' dorpa=(dorpa-dorp)/(deriv_eps)
!above calculate derivative of dimensionless axion density'''
    new2=''' dorpa=(dorpa-dorp)/(deriv_eps)
endif
!above calculate derivative of dimensionless axion density'''
    rec.write_text(replace_once(s,old2,new2,'recfast zero derivative close'))

    eq=src/'equations_ppf.f90'
    s=eq.read_text()
    expr='dorp=grhom*CP%drefp_hsq*((CP%a_osc/a)**3.0d0)'
    n=s.count(expr)
    if n!=2: raise RuntimeError(f'equations zero-density anchors: expected 2, found {n}')
    repl='''if (CP%omegaax .eq. 0._dl) then
          dorp=0._dl
       else
          dorp=grhom*CP%drefp_hsq*((CP%a_osc/a)**3.0d0)
       endif'''
    eq.write_text(s.replace(expr,repl))


def rows(p:Path):
    out=[]
    for line in p.read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if r:
            if not all(math.isfinite(x) for x in r): raise RuntimeError(f'{p}: nonfinite')
            out.append(r)
    if not out: raise RuntimeError(f'{p}: no numeric rows')
    n=len(out[0])
    if any(len(r)!=n for r in out): raise RuntimeError(f'{p}: ragged')
    return out


def compare(a,b):
    if len(a)!=len(b) or len(a[0])!=len(b[0]):
        return {'pass':False,'shape_match':False,'shape_a':[len(a),len(a[0])],'shape_b':[len(b),len(b[0])]}
    scale=max(1e-30,max(abs(x) for r in a for x in r),max(abs(x) for r in b for x in r))
    md=max(abs(x-y) for ra,rb in zip(a,b) for x,y in zip(ra,rb))
    ss=sum((x-y)**2 for ra,rb in zip(a,b) for x,y in zip(ra,rb)); n=len(a)*len(a[0])
    d=md/scale
    return {'pass':d<=TOL,'shape_match':True,'D_inf':d,'max_abs_difference':md,'rms_normalized':math.sqrt(ss/n)/scale,'scale':scale,'rows':len(a),'cols':len(a[0]),'tolerance':TOL}


def load_case(root:Path,name:str):
    d={}; ok=True
    for f in FILES:
        p=root/(name+'_'+f)
        try:
            r=rows(p); d[f]={'finite':True,'rows':len(r),'cols':len(r[0]),'_rows':r}
        except Exception as e:
            d[f]={'finite':False,'error':str(e)}; ok=False
    return d,ok


def clean(d): return {f:{k:v for k,v in q.items() if k!='_rows'} for f,q in d.items()}


def analyze(patched:Path, original:Path, statusp:Path, out:Path):
    st=json.loads(statusp.read_text())
    res={'schema':'KMDSB.M19.axionCAMB2.zeroBypassRecovery.v2','provider_pin':PIN,'tolerance':TOL,'status':st,'physical_falsification':False,'scientific_promotion':{'K1':False,'K2_K9':False},'preregistration':'protocol/W04_M19_AXIONCAMB2_ZERO_BYPASS_RECOVERY_PREREGISTRATION_v0.2.md'}
    if st.get('build_orig')!=0 or st.get('build_patch')!=0 or st.get('build_debug')!=0:
        res['classification']='M19_ZERO_BYPASS_V2_EXECUTION_BLOCKED'; res['reason']='build'; out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); return
    parsed={}; contracts={}; cases={}
    for label,root,name,exitkey in [('zf',patched,'r0f','zf'),('zd',patched,'r0d','zd'),('pp',patched,'p1','pp'),('po',original,'p1','po')]:
        d,ok=load_case(root,name); parsed[label]=d; contracts[label]=ok and st.get(exitkey)==0; cases[label]={'exit':st.get(exitkey),'outputs':clean(d),'contract_pass':contracts[label]}
    res['cases']=cases
    if not contracts['zf'] or not contracts['zd']:
        cls='M19_ZERO_BYPASS_V2_EXECUTION_BLOCKED'
    elif not contracts['pp'] or not contracts['po']:
        cls='M19_ZERO_BYPASS_V2_EXECUTION_BLOCKED'
    else:
        zcmp={}; pcmp={}; zok=True; pok=True
        for f in FILES:
            q=compare(parsed['zf'][f]['_rows'],parsed['zd'][f]['_rows']); zcmp[f]=q; zok=zok and q['pass']
            q=compare(parsed['pp'][f]['_rows'],parsed['po'][f]['_rows']); pcmp[f]=q; pok=pok and q['pass']
        res['zero_parameterization_identity']=zcmp; res['finite_noninterference']=pcmp
        if not pok: cls='M19_ZERO_BYPASS_V2_REJECTED_FINITE_PATH_CHANGED'
        elif not zok: cls='M19_ZERO_BYPASS_V2_IDENTITY_BLOCKED'
        elif st.get('debug_zf')!=0: cls='M19_ZERO_BYPASS_V2_RUNTIME_CHECK_BLOCKED'
        else: cls='M19_AXIONCAMB2_ZERO_BYPASS_RECOVERY_V2_PASS_WITH_SCOPE'
    res['classification']=cls
    res['next_if_pass']='separately preregister historical pure-CAMB CDM comparator; K1 remains unpromoted by recovery alone'
    out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('patch'); p.add_argument('source',type=Path)
    a=sp.add_parser('analyze'); a.add_argument('patched',type=Path); a.add_argument('original',type=Path); a.add_argument('status',type=Path); a.add_argument('output',type=Path)
    ns=ap.parse_args(); patch(ns.source) if ns.cmd=='patch' else analyze(ns.patched,ns.original,ns.status,ns.output)
