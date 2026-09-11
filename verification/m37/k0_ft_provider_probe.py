#!/usr/bin/env python3
import argparse, json, math, re
from pathlib import Path


def table(path, xcol=0, ycol=1):
    xs=[]; ys=[]
    for raw in Path(path).read_text(errors='replace').splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        parts=s.split()
        try:
            vals=[float(x) for x in parts]
        except Exception:
            continue
        if len(vals)<=max(xcol,ycol): continue
        x,y=vals[xcol],vals[ycol]
        if math.isfinite(x) and math.isfinite(y): xs.append(x); ys.append(y)
    return xs,ys


def interp(x, xs, ys):
    import bisect
    i=bisect.bisect_left(xs,x)
    if i==0: return ys[0]
    if i>=len(xs): return ys[-1]
    x0,x1=xs[i-1],xs[i]; y0,y1=ys[i-1],ys[i]
    if x1==x0: return y0
    t=(x-x0)/(x1-x0)
    return y0+t*(y1-y0)


def nl2(ref_path, active_path, ycol=1):
    xr,yr=table(ref_path,0,ycol); xa,ya=table(active_path,0,ycol)
    if len(xr)<5 or len(xa)<5: return None
    pairs=[]
    lo=max(min(xr),min(xa)); hi=min(max(xr),max(xa))
    for x,y in zip(xr,yr):
        if lo<=x<=hi:
            pairs.append((y,interp(x,xa,ya)))
    if len(pairs)<5: return None
    num=math.sqrt(sum((a-r)**2 for r,a in pairs)/len(pairs))
    den=max(math.sqrt(sum(r*r for r,a in pairs)/len(pairs)),1e-300)
    return num/den


def finite_table(path):
    xs,ys=table(path)
    return len(xs)>=5 and all(math.isfinite(v) for v in xs+ys)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--provider-dir',required=True)
    ap.add_argument('--reference-cl',required=True)
    ap.add_argument('--active-cl',required=True)
    ap.add_argument('--reference-pk',required=True)
    ap.add_argument('--active-pk',required=True)
    ap.add_argument('--provider-commit',required=True)
    ap.add_argument('--expected-commit',required=True)
    ap.add_argument('--reference-exit',type=int,required=True)
    ap.add_argument('--active-exit',type=int,required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()

    root=Path(args.provider_dir)
    inp=(root/'source/input.c').read_text(errors='replace')
    bg=(root/'source/background.c').read_text(errors='replace')
    pt=(root/'source/perturbations.c').read_text(errors='replace')
    markers={
      'input_n_fT': ('"n_fT"' in inp and 'pba->n_fT' in inp),
      'background_n_fT': ('pba->n_fT' in bg and 'alpha_ft' in bg and 'F_doubleprime_0' in bg),
      'perturbations_n_fT': ('pba->n_fT' in pt and 'alpha_ft' in pt and 'F_prime_0' in pt and 'F_doubleprime_0' in pt),
    }
    finite={
      'reference_cl':finite_table(args.reference_cl),
      'active_cl':finite_table(args.active_cl),
      'reference_pk':finite_table(args.reference_pk),
      'active_pk':finite_table(args.active_pk),
    }
    response={
      'tt_normalized_l2':nl2(args.reference_cl,args.active_cl,1),
      'pk_normalized_l2':nl2(args.reference_pk,args.active_pk,1),
      'threshold':1e-6,
    }
    active_response=any(v is not None and v>1e-6 for k,v in response.items() if k.endswith('_normalized_l2'))
    executable=(args.provider_commit==args.expected_commit and all(markers.values()) and args.reference_exit==0 and args.active_exit==0 and all(finite.values()) and active_response)
    if executable:
        cls='M37_K0_PARTIAL_EXECUTABLE_FT_PROVIDER_PROVENANCE_OPEN'
    elif args.reference_exit!=0 or args.active_exit!=0:
        cls='M37_K0_BLOCKED_IMPLEMENTATION_EXECUTION'
    else:
        cls='M37_K0_NOT_ESTABLISHED'
    out={
      'schema':'m37_k0_ft_provider_probe_v0.1',
      'provider':'Speeddemon5050/Modified-CLASS-fT-Exact-',
      'provider_commit':args.provider_commit,
      'expected_commit':args.expected_commit,
      'source_markers':markers,
      'exit_codes':{'reference':args.reference_exit,'active':args.active_exit},
      'finite_outputs':finite,
      'response':response,
      'executable_gate':executable,
      'classification':cls,
      'K0_promoted':False,
      'physical_falsification':False,
      'scope':'exact-pin executable f(T) provider probe only; publication/author provenance remains open; K1-K9 open'
    }
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
