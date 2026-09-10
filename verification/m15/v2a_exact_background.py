#!/usr/bin/env python3
import json, math
from pathlib import Path

OMEGA_B=0.049
OMEGA_R=9.0e-5
A_NODES=[1.0,0.8,0.5,0.2,0.1,0.03,0.01,0.003,0.001,0.0003,0.0001]
RESOLUTIONS=[20000,40000,80000]
CASES=[
    ('alpha_m050',-0.50,0.3075),
    ('alpha_m025',-0.25,0.2745),
    ('alpha_m005',-0.05,0.2505),
    ('alpha_0',0.0,0.2500),
    ('alpha_p005',0.05,0.2385),
    ('alpha_p025',0.25,0.2165),
]


def rhs(x,E,alpha,ol):
    a=math.exp(x)
    if not math.isfinite(E) or E<=0:
        raise ValueError(f'nonpositive/nonfinite E at a={a}: {E}')
    return (-3*E*E + 3*ol*(E**(-2*alpha)) - OMEGA_R*a**-4)/(2*E)


def rk4_step(x,E,h,alpha,ol):
    k1=rhs(x,E,alpha,ol)
    k2=rhs(x+h/2,E+h*k1/2,alpha,ol)
    k3=rhs(x+h/2,E+h*k2/2,alpha,ol)
    k4=rhs(x+h,E+h*k3,alpha,ol)
    return E+h*(k1+2*k2+2*k3+k4)/6


def integrate(alpha,oc,N):
    ol=1-OMEGA_B-OMEGA_R-oc
    if ol<=0: raise ValueError('Omega_Lambda0 <=0')
    targets=sorted([(math.log(a),a) for a in A_NODES], reverse=True)
    x=0.0; E=1.0
    hmax=abs(math.log(min(A_NODES)))/N
    out={}
    for xt,a in targets:
        while x-xt>1e-15:
            h=-min(hmax,x-xt)
            E=rk4_step(x,E,h,alpha,ol)
            x+=h
        dEdx=rhs(x,E,alpha,ol)
        lam=ol*E**(-2*alpha)
        cdm=E*E-OMEGA_B*a**-3-OMEGA_R*a**-4-lam
        qdim=(-2*alpha*lam/E)*dEdx if alpha!=0 else 0.0
        om=OMEGA_B+oc
        base=(1-om)+om*a**(-3*(1+alpha))
        if base<=0: Eapprox=float('nan')
        else: Eapprox=math.sqrt(base**(1/(1+alpha))+OMEGA_R*a**-4)
        dev=(E-Eapprox)/E if math.isfinite(Eapprox) else float('nan')
        out[f'{a:.10g}']={'a':a,'E':E,'rhoLambda_over_rhocrit0':lam,'rhoC_over_rhocrit0':cdm,
                          'Q_over_H_rhocrit0':qdim,'E_approx_eq26':Eapprox,'deviation_eq26':dev}
    return {'alpha':alpha,'Omega_c0':oc,'Omega_b0':OMEGA_B,'Omega_r0':OMEGA_R,'Omega_Lambda0':ol,'nodes':out}


def symrel(x,y):
    return 2*abs(x-y)/max(abs(x)+abs(y),1e-300)


def compare(case40,case80):
    e=[]; c=[]; l=[]
    for key in case80['nodes']:
        a=case40['nodes'][key]; b=case80['nodes'][key]
        e.append(symrel(a['E'],b['E']))
        if a['rhoC_over_rhocrit0']>0 and b['rhoC_over_rhocrit0']>0:
            c.append(symrel(a['rhoC_over_rhocrit0'],b['rhoC_over_rhocrit0']))
        else: c.append(float('inf'))
        if a['rhoLambda_over_rhocrit0']>0 and b['rhoLambda_over_rhocrit0']>0:
            l.append(symrel(a['rhoLambda_over_rhocrit0'],b['rhoLambda_over_rhocrit0']))
        else: l.append(float('inf'))
    return {'E_max_symrel':max(e),'rhoC_max_symrel':max(c),'rhoLambda_max_symrel':max(l)}


def alpha0_identity(case):
    om=case['Omega_b0']+case['Omega_c0']
    ol=case['Omega_Lambda0']
    vals=[]
    for row in case['nodes'].values():
        a=row['a']
        exact=math.sqrt(OMEGA_R*a**-4+om*a**-3+ol)
        vals.append(symrel(row['E'],exact))
    return max(vals)


def approx_stats(case):
    rows=list(case['nodes'].values())
    def mx(amin):
        vals=[abs(r['deviation_eq26']) for r in rows if r['a']>=amin and math.isfinite(r['deviation_eq26'])]
        return max(vals) if vals else None
    return {'max_abs_deviation_a_ge_0p1':mx(0.1),'max_abs_deviation_a_ge_1e_3':mx(1e-3),'max_abs_deviation_a_ge_1e_4':mx(1e-4)}


def main():
    all_runs={}
    error=None
    try:
        for tag,alpha,oc in CASES:
            all_runs[tag]={str(N):integrate(alpha,oc,N) for N in RESOLUTIONS}
    except Exception as e:
        error=repr(e)

    result={'schema':'KMDSB.W03.M15.V2aExactBackground.v0.1','benchmark_constants':{'Omega_b0':OMEGA_B,'Omega_r0':OMEGA_R},
            'a_nodes':A_NODES,'resolutions':RESOLUTIONS,'cases':{},'error':error}
    if error is not None:
        result['classification']='M15_V2A_NUMERICAL_ERROR'
    else:
        convergence_pass=True; positivity_pass=True; sign_pass=True
        ref_err=None
        for tag,alpha,oc in CASES:
            c20=all_runs[tag]['20000']; c40=all_runs[tag]['40000']; c80=all_runs[tag]['80000']
            conv=compare(c40,c80)
            conv_ok=(conv['E_max_symrel']<=2e-7 and conv['rhoC_max_symrel']<=2e-6 and conv['rhoLambda_max_symrel']<=2e-6)
            convergence_pass &= conv_ok
            pos=all(math.isfinite(r['rhoC_over_rhocrit0']) and r['rhoC_over_rhocrit0']>0 and
                    math.isfinite(r['rhoLambda_over_rhocrit0']) and r['rhoLambda_over_rhocrit0']>0 for r in c80['nodes'].values())
            positivity_pass &= pos
            signs=[]
            if alpha!=0:
                for r in c80['nodes'].values():
                    if r['a']>=0.01:
                        signs.append((r['Q_over_H_rhocrit0']>0) if alpha>0 else (r['Q_over_H_rhocrit0']<0))
                sign_ok=all(signs)
                sign_pass &= sign_ok
            else:
                sign_ok=all(r['Q_over_H_rhocrit0']==0.0 for r in c80['nodes'].values())
                ref_err=alpha0_identity(c80)
            result['cases'][tag]={'alpha':alpha,'Omega_c0':oc,'convergence_40k_80k':conv,'convergence_pass':conv_ok,
                                  'positivity_pass':pos,'interaction_sign_pass':sign_ok,'eq26_approximation':approx_stats(c80),
                                  'finest':c80,'coarse_20k':c20}
        reference_pass=(ref_err is not None and ref_err<=2e-7)
        result['alpha0_max_symrel_vs_LCDM']=ref_err
        result['gates']={'reference_pass':reference_pass,'convergence_pass':convergence_pass,'positivity_pass':positivity_pass,'interaction_sign_pass':sign_pass}
        if not reference_pass: cls='M15_V2A_REFERENCE_FAIL'
        elif not convergence_pass: cls='M15_V2A_CONVERGENCE_FAIL'
        elif not positivity_pass: cls='M15_V2A_PHYSICAL_DOMAIN_FAIL_WITH_SCOPE'
        elif not sign_pass: cls='M15_V2A_INTERACTION_SIGN_FAIL'
        else: cls='M15_V2A_EXACT_BACKGROUND_PASS'
        result['classification']=cls
        result['scientific_promotion']='BACKGROUND_ONLY' if cls=='M15_V2A_EXACT_BACKGROUND_PASS' else False
        result['perturbation_sound_speed_resolved']=False
        result['physical_family_falsification']=False
    Path('m15_v2a_background_result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    for tag,c in result.get('cases',{}).items():
        print(tag,c['convergence_40k_80k'],c['eq26_approximation'],c['positivity_pass'],c['interaction_sign_pass'])

if __name__=='__main__': main()
