#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path
import numpy as np

FRACS=[0.10,0.03,0.01,0.003,0.001]
FILES=['scalCls.dat','matterpower.dat','transfer_out.dat']
AXPIN='891e779cc0bd422e49f97533e6c2fc761149737d'
CDMPIN='dc437acd8c90aa7e5595fcb25c615b03de8357a7'

def repl(s,k,v,required=True):
    p=re.compile(rf'(?m)^(\s*{re.escape(k)}\s*=).*?$')
    m=list(p.finditer(s))
    if not m:
        if required: raise RuntimeError(f'{k}: missing')
        return s
    if len(m)!=1: raise RuntimeError(f'{k}: active-count={len(m)}')
    return p.sub(lambda x:f'{x.group(1)} {v}',s,count=1)

def prepare(axbase:Path, cdmbase:Path, out:Path):
    out.mkdir(parents=True,exist_ok=True)
    ax=axbase.read_text(); cdm=cdmbase.read_text()
    shared={
      'get_scalar_cls':'T','get_vector_cls':'F','get_tensor_cls':'F','get_transfer':'T','do_lensing':'F','do_nonlinear':'0',
      'ombh2':'0.02222','omnuh2':'0.0006','omk':'0','hubble':'67.31','w':'-1','cs2_lam':'1',
      'temp_cmb':'2.725','helium_fraction':'0.24','massless_neutrinos':'2.04','massive_neutrinos':'1','share_delta_neff':'T',
      'nu_mass_eigenstates':'1','nu_mass_fractions':'1','initial_power_num':'1','pivot_scalar':'0.05','pivot_tensor':'0.05',
      'scalar_amp(1)':'2.196e-9','scalar_spectral_index(1)':'0.9655','scalar_nrun(1)':'0','tensor_spectral_index(1)':'0','initial_ratio(1)':'0',
      'reionization':'T','re_use_optical_depth':'T','re_optical_depth':'0.078','re_redshift':'11','re_delta_redshift':'1.5','re_ionization_frac':'-1',
      'RECFAST_fudge':'1.14','RECFAST_fudge_He':'0.86','RECFAST_Heswitch':'6','RECFAST_Hswitch':'T','initial_condition':'1',
      'COBE_normalize':'F','CMB_outputscale':'7.4311e12','transfer_high_precision':'F','transfer_kmax':'5','transfer_k_per_logint':'0',
      'transfer_num_redshifts':'1','transfer_interp_matterpower':'T','transfer_redshift(1)':'0','transfer_filename(1)':'transfer_out.dat',
      'transfer_matterpower(1)':'matterpower.dat','scalar_output_file':'scalCls.dat','l_max_scalar':'5000'
    }
    # Axion cases: fixed total dark matter split by fraction.
    for i,f in enumerate(FRACS):
        t=ax
        for k,v in shared.items(): t=repl(t,k,v,required=False)
        for k,v in {'output_root':f'a{i}','use_axfrac':'T','omdah2':'0.1200','axfrac':str(f),'m_ax':'1.e-27','axion_isocurvature':'F'}.items(): t=repl(t,k,v)
        (out/f'a{i}.ini').write_text(t)
    # Historical pure CDM: same total physical dark matter density entirely in CDM.
    t=cdm
    for k,v in shared.items(): t=repl(t,k,v,required=False)
    t=repl(t,'output_root','c0')
    t=repl(t,'omch2','0.1200')
    (out/'c0.ini').write_text(t)
    (out/'manifest.json').write_text(json.dumps({'fractions':FRACS,'axion_pin':AXPIN,'cdm_pin':CDMPIN,'shared':shared},indent=2,sort_keys=True)+'\n')

def load(path:Path):
    rows=[]
    for line in path.read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        try: r=[float(x.replace('D','E').replace('d','e')) for x in s.split()]
        except ValueError: continue
        if r and all(math.isfinite(x) for x in r): rows.append(r)
    a=np.asarray(rows,float)
    if a.ndim!=2 or a.shape[0]<3 or a.shape[1]<2: raise RuntimeError(f'invalid {path}')
    return a

def interp_reference(model,ref):
    x=model[:,0]; xr=ref[:,0]
    lo=max(x.min(),xr.min()); hi=min(x.max(),xr.max())
    mask=(x>=lo)&(x<=hi)
    x=x[mask]; ym=model[mask,1:]
    if len(x)<3: raise RuntimeError('insufficient overlap')
    if model.shape[1]!=ref.shape[1]: raise RuntimeError('column mismatch')
    # CMB ell grids are integer: linear interpolation is exact on shared nodes.
    yr=np.column_stack([np.interp(x,xr,ref[:,j]) for j in range(1,ref.shape[1])])
    return x,ym,yr

def metrics(model,ref):
    _,a,b=interp_reference(model,ref)
    scale=max(float(np.max(np.abs(a))),float(np.max(np.abs(b))),1e-300)
    floor=1e-12*scale
    den=np.abs(a)+np.abs(b)+floor
    r=2*(a-b)/den
    vals=np.abs(r).ravel()
    return {'median_abs':float(np.median(vals)),'rms':float(np.sqrt(np.mean(r*r))),'p95_abs':float(np.percentile(vals,95)),'n':int(vals.size),'floor':floor}

def fit_exp(fs,rs):
    f=np.asarray(fs[-3:],float); r=np.asarray(rs[-3:],float)
    if np.any(r<=0): return {'p':None,'valid':False}
    p,b=np.polyfit(np.log(f),np.log(r),1)
    return {'p':float(p),'logA':float(b),'valid':True}

def analyze(axroot:Path,cdmroot:Path,statusp:Path,out:Path):
    st=json.loads(statusp.read_text())
    res={'schema':'KMDSB.M19.externalCDMConvergence.v1','axion_pin':AXPIN,'cdm_pin':CDMPIN,'fractions':FRACS,'status':st,'physical_falsification':False,'K1_promoted':False,'blocks':{}}
    if st.get('build_ax')!=0 or st.get('build_cdm')!=0 or st.get('c0')!=0 or any(st.get(f'a{i}')!=0 for i in range(len(FRACS))):
        res['classification']='M19_EXTERNAL_CDM_REFERENCE_EXECUTION_BLOCKED'; out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); return
    cfiles={f:load(cdmroot/('c0'+('_' if f!='scalCls.dat' else '_')+f)) for f in FILES}
    # Both classic providers prefix output_root directly; generated files are c0_scalCls.dat etc.
    allpass=True
    for f in FILES:
        vals=[]
        for i,frac in enumerate(FRACS):
            q=metrics(load(axroot/(f'a{i}_'+f)),cfiles[f]); q['fraction']=frac; vals.append(q)
        r95=[q['p95_abs'] for q in vals]
        monotonic=all(r95[i+1] <= r95[i]*1.02 for i in range(len(r95)-1))
        decreased=r95[-1] < r95[0]
        fit=fit_exp(FRACS,r95)
        exponent=bool(fit.get('valid') and fit.get('p') is not None and fit['p']>0)
        bp=monotonic and decreased and exponent
        res['blocks'][f]={'points':vals,'r95':r95,'monotonic_with_2pct_slack':monotonic,'smallest_lower_than_largest':decreased,'fit_smallest3':fit,'pass':bp}
        allpass=allpass and bp
    res['classification']='M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_PASS_WITH_SCOPE' if allpass else 'M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_NOT_ESTABLISHED'
    res['K1_promoted']=allpass
    res['K1_scope']='PASS_WITH_SCOPE_EXTERNAL_LIMIT_CONVERGENCE' if allpass else 'NOT_PROMOTED'
    out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    p=sp.add_parser('prepare'); p.add_argument('axbase',type=Path); p.add_argument('cdmbase',type=Path); p.add_argument('out',type=Path)
    a=sp.add_parser('analyze'); a.add_argument('axroot',type=Path); a.add_argument('cdmroot',type=Path); a.add_argument('status',type=Path); a.add_argument('out',type=Path)
    n=ap.parse_args(); prepare(n.axbase,n.cdmbase,n.out) if n.cmd=='prepare' else analyze(n.axroot,n.cdmroot,n.status,n.out)
