#!/usr/bin/env python3
import json, math, pathlib
import numpy as np

PIN='0009f51d89e6465c79e570b496c66fc90058fa77'
ROOTS={'parent':pathlib.Path('inputs/parent'),'fine':pathlib.Path('inputs/fine')}
HS={'parent':{'coarse':0.002,'fine':0.001},'fine':{'coarse':0.0005,'fine':0.00025}}
TAGS=['base','rp2','rm2','rp1','rm1','tp2','tm2','tp1','tm1']

def one(root,pattern):
    hits=list(root.rglob(pattern))
    if len(hits)!=1:
        raise RuntimeError(f'{root} {pattern}: expected one hit, got {len(hits)}')
    return hits[0]

def load(path):
    rows=[]
    for line in path.read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'):
            continue
        try:
            rows.append([float(x) for x in s.split()])
        except ValueError:
            pass
    a=np.asarray(rows,float)
    if a.ndim!=2 or len(a)<5 or a.shape[1]<2:
        raise RuntimeError(f'bad table {path}')
    return a

def geom(a,b):
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na==0 or nb==0:
        raise RuntimeError('zero derivative norm')
    c=float(np.dot(a,b)/(na*nb)); c=max(-1.0,min(1.0,c))
    ang=float(math.degrees(math.acos(abs(c))))
    mismatch=abs(na-nb)/max(na,nb)
    return {'principal_angle_deg':ang,'relative_norm_mismatch':mismatch,
            'absolute_cosine':abs(c),'norm_a':na,'norm_b':nb,
            'passes_5deg_025':bool(ang<=5.0 and mismatch<=0.25)}

out={'schema':'m31_immutable_block_localization_v0.1','model_id':'M31','family_id':'F31',
     'protocol':'protocol/W07_M31_IMMUTABLE_BLOCK_LOCALIZATION_AUDIT_v0.1.md',
     'inputs':{'parent':{'run':34694420359,'artifact':10298453048,'h_coarse':0.002,'h_fine':0.001},
               'fine':{'run':34695461864,'artifact':10298900445,'h_coarse':0.0005,'h_fine':0.00025}},
     'provider_commit_expected':PIN,'K2_promoted':False,'physical_falsification':False,'family_exclusion':False}
try:
    records={}
    for key,root in ROOTS.items():
        commit=one(root,'provider_commit.txt').read_text().strip()
        if commit!=PIN:
            raise RuntimeError(f'{key} provider pin mismatch {commit}')
        exits={t:int(one(root,f'{t}.exit').read_text()) for t in TAGS}
        if any(v!=0 for v in exits.values()):
            raise RuntimeError(f'{key} nonzero exits {exits}')
        cls={t:load(one(root,f'{t}_00_cl.dat')) for t in TAGS}
        pk={t:load(one(root,f'{t}_00_pk.dat')) for t in TAGS}
        records[key]={'commit':commit,'exits':exits,'cl':cls,'pk':pk}

    maps={key:{t:{int(r[0]):np.asarray(r[1:],float) for r in records[key]['cl'][t] if np.isfinite(r[0])} for t in TAGS} for key in records}
    common_ell=sorted(set.intersection(*[set(maps[key][t]) for key in maps for t in TAGS]))
    cmb={key:{t:[] for t in TAGS} for key in records}
    for ell in common_ell:
        n=min(len(maps[key][t][ell]) for key in maps for t in TAGS)
        for j in range(n):
            vals={(key,t):maps[key][t][ell][j] for key in maps for t in TAGS}
            if all(np.isfinite(v) for v in vals.values()):
                for (key,t),v in vals.items(): cmb[key][t].append(v)
    cmb={key:{t:np.asarray(v,float) for t,v in d.items()} for key,d in cmb.items()}
    if len(cmb['fine']['base'])<5:
        raise RuntimeError('insufficient common CMB support')

    allpk=[records[key]['pk'][t] for key in records for t in TAGS]
    lo=max(float(np.nanmin(a[:,0])) for a in allpk); hi=min(float(np.nanmax(a[:,0])) for a in allpk)
    bp=records['fine']['pk']['base']; mask=(bp[:,0]>=lo)&(bp[:,0]<=hi)&np.isfinite(bp[:,0])&np.isfinite(bp[:,1]); x=bp[mask,0]
    pki={key:{} for key in records}
    for key in records:
        for t in TAGS:
            a=records[key]['pk'][t]; pki[key][t]=np.interp(x,a[:,0],a[:,1])
    good=np.ones(len(x),dtype=bool)
    for key in records:
        for t in TAGS: good &= np.isfinite(pki[key][t])
    x=x[good]; pki={key:{t:v[good] for t,v in d.items()} for key,d in pki.items()}
    if len(x)<5:
        raise RuntimeError('insufficient common P(k) support')

    base_consistency={}
    for block,vals in [('cmb',cmb),('pk',pki)]:
        a=vals['parent']['base']; b=vals['fine']['base']; scale=np.maximum(np.maximum(np.abs(a),np.abs(b)),1e-30)
        base_consistency[block+'_max_sym_rel']=float(np.max(np.abs(a-b)/scale))
    out['base_consistency']=base_consistency
    out['global_support']={'cmb_values':int(len(cmb['fine']['base'])),'ell_count':int(len(common_ell)),
                           'pk_values':int(len(x)),'pk_k_min':float(x.min()),'pk_k_max':float(x.max())}

    def deriv(vals,key,plus,minus,h):
        norm=float(np.linalg.norm(vals[key]['base']))
        if norm==0: raise RuntimeError(f'zero base norm {key}')
        return (vals[key][plus]-vals[key][minus])/(2*h*norm)

    metrics={}; adjacent_pass={}
    for block,vals in [('cmb',cmb),('pk',pki)]:
        prc=deriv(vals,'parent','rp2','rm2',HS['parent']['coarse']); prf=deriv(vals,'parent','rp1','rm1',HS['parent']['fine'])
        frc=deriv(vals,'fine','rp2','rm2',HS['fine']['coarse']); frf=deriv(vals,'fine','rp1','rm1',HS['fine']['fine'])
        ptc=deriv(vals,'parent','tp2','tm2',HS['parent']['coarse']); ptf=deriv(vals,'parent','tp1','tm1',HS['parent']['fine'])
        ftc=deriv(vals,'fine','tp2','tm2',HS['fine']['coarse']); ftf=deriv(vals,'fine','tp1','tm1',HS['fine']['fine'])
        metrics[block]={
          'parent_radial_coarse_vs_fine':geom(prc,prf),
          'fine_run_radial_coarse_vs_fine':geom(frc,frf),
          'adjacent_radial_h001_vs_h0005':geom(prf,frc),
          'adjacent_radial_h0005_vs_h00025':geom(frc,frf),
          'parent_cT_coarse_vs_fine':geom(ptc,ptf),
          'fine_run_cT_coarse_vs_fine':geom(ftc,ftf),
          'adjacent_cT_h001_vs_h0005':geom(ptf,ftc),
          'adjacent_cT_h0005_vs_h00025':geom(ftc,ftf),
        }
        adjacent_pass[block]=bool(metrics[block]['adjacent_radial_h001_vs_h0005']['passes_5deg_025'] and metrics[block]['adjacent_radial_h0005_vs_h00025']['passes_5deg_025'])
    out['block_metrics']=metrics; out['radial_adjacent_scale_converged']=adjacent_pass
    if adjacent_pass['pk'] and not adjacent_pass['cmb']:
        cls='M31_RADIAL_NONCONVERGENCE_CMB_LOCALIZED'
    elif adjacent_pass['cmb'] and not adjacent_pass['pk']:
        cls='M31_RADIAL_NONCONVERGENCE_PK_LOCALIZED'
    elif (not adjacent_pass['cmb']) and (not adjacent_pass['pk']):
        cls='M31_RADIAL_NONCONVERGENCE_BOTH_BLOCKS'
    else:
        cls='M31_RADIAL_NONCONVERGENCE_NOT_REPRODUCED_BY_BLOCK_AUDIT'
    out['classification']=cls
    out['interpretation']='Analysis-only localization of immutable numerical response. No K2 promotion, family exclusion, k-cut retuning, threshold retuning or additional step shrinking is authorized.'
except Exception as e:
    out['classification']='M31_BLOCK_LOCALIZATION_INTEGRITY_BLOCKED'; out['error']=repr(e)

pathlib.Path('out').mkdir(exist_ok=True)
pathlib.Path('out/M31_IMMUTABLE_BLOCK_LOCALIZATION.json').write_text(json.dumps(out,indent=2)+'\n')
with open('out/M31_IMMUTABLE_BLOCK_LOCALIZATION.md','w') as f:
    f.write('# M31 immutable block-localization audit\n\n')
    f.write(f"Classification: `{out['classification']}`  \n")
    if out.get('radial_adjacent_scale_converged'):
        f.write(f"Radial adjacent-scale convergence: `{out['radial_adjacent_scale_converged']}`  \n")
    f.write('\nThis is a numerical-localization result only. K2 is not promoted and no physical family failure is assigned.\n')
print(pathlib.Path('out/M31_IMMUTABLE_BLOCK_LOCALIZATION.json').read_text())
