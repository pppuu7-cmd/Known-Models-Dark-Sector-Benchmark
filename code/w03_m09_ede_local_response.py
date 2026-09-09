#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math, re
from pathlib import Path
import numpy as np

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
KLOW=np.array([0.001,0.003,0.01,0.03,0.1],float)
KSHAPE=np.array([0.001,0.003,0.006,0.01,0.02,0.03,0.05,0.08,0.1,0.2,0.3,0.5,0.8,1.0],float)
ZSHAPE=0.51
BRIDGE_TOL=1e-6
REL_GATE=0.05
ANGLE_GATE=2.0


def zhdr(path: Path) -> float:
    with path.open() as f:
        for _ in range(30):
            s=f.readline()
            m=re.search(r'redshift\s+z\s*=\s*([+\-0-9.eE]+)',s,re.I)
            if m:
                return float(m.group(1))
    raise ValueError(f'no redshift header in {path}')


def load_pk(directory: Path, prefix: str, kvals: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    rows=[]
    for pstr in glob.glob(str(directory/f'{prefix}*pk.dat')):
        p=Path(pstr); z=zhdr(p); a=np.loadtxt(p,comments='#')
        k,y=a[:,0],a[:,1]
        if kvals.min()<k.min() or kvals.max()>k.max():
            raise ValueError(f'k grid outside output range for {p}: [{k.min()},{k.max()}]')
        yi=np.exp(np.interp(np.log(kvals),np.log(k),np.log(y)))
        rows.append((z,yi))
    rows.sort(key=lambda x:x[0])
    zs=np.array([r[0] for r in rows],float)
    vals=np.vstack([r[1] for r in rows]) if rows else np.empty((0,len(kvals)))
    return zs,vals


def titles(path: Path):
    txt=''
    with path.open() as f:
        for _ in range(40):
            s=f.readline()
            if not s: break
            if s.startswith('#'): txt+=' '+s[1:].strip()
            else: break
    ms=list(re.finditer(r'(?:^|\s)(\d+):',txt)); out={}
    for i,m in enumerate(ms):
        out[int(m.group(1))-1]=txt[m.end():(ms[i+1].start() if i+1<len(ms) else len(txt))].strip()
    return out


def load_H(directory: Path, prefix: str) -> np.ndarray:
    hits=list(directory.glob(f'{prefix}*background.dat'))
    if len(hits)!=1:
        raise ValueError(f'background {prefix}: {hits}')
    t=titles(hits[0]); a=np.loadtxt(hits[0],comments='#')
    iz=next(i for i,x in t.items() if x.startswith('z'))
    ih=next(i for i,x in t.items() if x.startswith('H [1/Mpc]'))
    order=np.argsort(a[:,iz])
    return np.interp(Z,a[order,iz],a[order,ih])


def pk_on_frozen_z(directory: Path,prefix: str,kvals: np.ndarray) -> np.ndarray:
    zs,p=load_pk(directory,prefix,kvals)
    if len(zs)!=len(Z) or not np.allclose(zs,Z,rtol=0,atol=5e-6):
        raise ValueError(f'bad z grid for {prefix}: {zs}')
    return p


def response_L(directory: Path,prefix: str,base_prefix: str):
    P=pk_on_frozen_z(directory,prefix,KLOW); P0=pk_on_frozen_z(directory,base_prefix,KLOW)
    H=load_H(directory,prefix); H0=load_H(directory,base_prefix)
    return np.log(P/P0).reshape(-1),np.log(H/H0)


def response_shape(directory: Path,prefix: str,base_prefix: str):
    zs,P=load_pk(directory,prefix,KSHAPE); zs0,P0=load_pk(directory,base_prefix,KSHAPE)
    if not np.allclose(zs,zs0,rtol=0,atol=5e-6):
        raise ValueError('shape z grids differ')
    i=int(np.argmin(np.abs(zs-ZSHAPE)))
    if abs(zs[i]-ZSHAPE)>5e-6:
        raise ValueError(f'missing z={ZSHAPE} shape output for {prefix}')
    r=np.log(P[i]/P0[i])
    return r-float(np.mean(r[:2]))


def geom(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na<1e-30 or nb<1e-30:
        return {'norm_a':na,'norm_b':nb,'relative_l2':None,'angle_deg':None,'state':'NEAR_NULL'}
    rel=float(np.linalg.norm(a-b)/max(na,nb))
    c=float(np.dot(a,b)/(na*nb)); c=max(-1.0,min(1.0,c))
    ang=float(np.degrees(np.arccos(c)))
    return {'norm_a':na,'norm_b':nb,'relative_l2':rel,'angle_deg':ang,'state':'DEFINED'}


def block_pass(g):
    if g['state']=='NEAR_NULL': return True
    return g['relative_l2']<=REL_GATE and g['angle_deg']<=ANGLE_GATE


def finite_prediction(actual,deriv,e):
    pred=np.asarray(deriv,float)*e; actual=np.asarray(actual,float)
    na=float(np.linalg.norm(actual))
    if na<1e-30:
        return {'relative_l2_error':None,'angle_deg':None,'state':'NEAR_NULL'}
    err=float(np.linalg.norm(actual-pred)/na)
    npred=float(np.linalg.norm(pred))
    if npred<1e-30:
        ang=None
    else:
        c=float(np.dot(actual,pred)/(na*npred)); c=max(-1,min(1,c)); ang=float(np.degrees(np.arccos(c)))
    return {'relative_l2_error':err,'angle_deg':ang,'state':'DEFINED'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--directory',required=True)
    ap.add_argument('--json',required=True)
    args=ap.parse_args(); d=Path(args.directory)

    # Explicit external bridge: solver-native EDE zero point versus pure LambdaCDM.
    bridgeP,bridgeH=response_L(d,'ede0_','lcdm_')
    bridgeS=response_shape(d,'ede0_','lcdm_')
    bridge={
      'max_abs_lnP_lowk':float(np.max(np.abs(bridgeP))),
      'max_abs_lnH':float(np.max(np.abs(bridgeH))),
      'max_abs_shape':float(np.max(np.abs(bridgeS))),
    }
    bridge['lambda_intersection_pass']=bool(bridge['max_abs_lnP_lowk']<=BRIDGE_TOL and bridge['max_abs_lnH']<=BRIDGE_TOL)

    vals=[1e-4,3e-4,1e-3,3e-3]
    tags=['e1e4','e3e4','e1e3','e3e3']
    resp={}
    for e,tag in zip(vals,tags):
        P,H=response_L(d,tag+'_','ede0_')
        S=response_shape(d,tag+'_','ede0_')
        resp[tag]={'e':e,'P':P,'H':H,'S':S}

    d1={k:resp['e1e4'][k]/1e-4 for k in ('P','H','S')}
    d2={k:resp['e3e4'][k]/3e-4 for k in ('P','H','S')}
    conv={k:geom(d1[k],d2[k]) for k in ('P','H','S')}
    tangent_pass=all(block_pass(conv[k]) for k in conv)
    dbar={k:0.5*(d1[k]+d2[k]) for k in ('P','H','S')}

    finite={}
    for tag in ('e1e3','e3e3'):
        e=resp[tag]['e']
        finite[tag]={k:finite_prediction(resp[tag][k],dbar[k],e) for k in ('P','H','S')}

    shape_norm=float(np.linalg.norm(dbar['S']))
    lowk_norm=float(np.linalg.norm(dbar['P']))
    h_norm=float(np.linalg.norm(dbar['H']))

    out={
      'schema':'KMDSB.W03.M09.EDELocalResponse.v0.1',
      'coordinate':'e=Omega_EDE, one-sided e>=0',
      'solver_reference_policy':{'external':'pure LambdaCDM','internal':'EDE e=0'},
      'frozen_grids':{'z':Z.tolist(),'k_low_h_mpc':KLOW.tolist(),'z_shape':ZSHAPE,'k_shape_h_mpc':KSHAPE.tolist(),'shape_anchor':'mean of first two low-k lnP ratios'},
      'ede0_to_lcdm_bridge':bridge,
      'local_tangent':{
        'pair':[1e-4,3e-4],
        'convergence':conv,
        'pass_with_scope':bool(tangent_pass),
        'mean_derivative_per_e':{k:dbar[k].tolist() for k in ('P','H','S')},
        'norms':{'P':lowk_norm,'H':h_norm,'S':shape_norm,'S_over_P':shape_norm/max(lowk_norm,1e-30)}
      },
      'finite_deformation_linearity_checks':finite,
      'finite_response_maxima':{
        tag:{
          'e':resp[tag]['e'],
          'max_abs_lnP_lowk':float(np.max(np.abs(resp[tag]['P']))),
          'max_abs_lnH':float(np.max(np.abs(resp[tag]['H']))),
          'max_abs_shape':float(np.max(np.abs(resp[tag]['S'])))
        } for tag in tags
      },
      'classification':('PASS_WITH_SCOPE' if bridge['lambda_intersection_pass'] and tangent_pass else ('PARTIAL_REFERENCE_BRIDGE' if tangent_pass else 'INCONCLUSIVE_LOCAL_TANGENT')),
      'anti_overclaim':[
        'shape block is unwhitened theory-response geometry, not a likelihood coordinate',
        'finite e probes are not B8 holdouts',
        'solver-native EDE is not all EDE microphysics'
      ]
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
