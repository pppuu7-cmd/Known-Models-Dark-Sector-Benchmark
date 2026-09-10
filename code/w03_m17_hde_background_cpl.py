#!/usr/bin/env python3
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

Z=np.array([0.295,0.51,0.706,0.934,1.317,1.491,2.33],float)
OM=0.30
ODE0=0.70
CS=[0.60,0.80,1.00,1.20]
STARTS=[(-1.0,0.0),(-0.8,-0.5),(-1.2,0.5)]
BOUNDS=([-2.0,-3.0],[0.0,3.0])


def lcdm_E(z):
    return np.sqrt(OM*(1+z)**3 + (1-OM))


def hde_omega(z,c,rtol,atol):
    x_targets=-np.log1p(z)
    xmin=float(x_targets.min())
    def rhs(x,y):
        o=max(min(float(y[0]),1-1e-14),1e-14)
        return [o*(1-o)*(1+2*math.sqrt(o)/c)]
    sol=solve_ivp(rhs,(0.0,xmin),[ODE0],rtol=rtol,atol=atol,dense_output=True,max_step=0.01)
    if not sol.success:
        raise RuntimeError(sol.message)
    return np.array([sol.sol(float(x))[0] for x in x_targets])


def hde_resid(c,rtol,atol):
    o=hde_omega(Z,c,rtol,atol)
    a=1/(1+Z)
    E=np.sqrt(OM*a**-3/(1-o))
    return np.log(E/lcdm_E(Z)), o


def cpl_E(z,w0,wa):
    a=1/(1+z)
    ode=(1-OM)*a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
    return np.sqrt(OM*a**-3+ode)


def cpl_resid(w0,wa):
    return np.log(cpl_E(Z,w0,wa)/lcdm_E(Z))


def angle_deg(u,v):
    nu=np.linalg.norm(u); nv=np.linalg.norm(v)
    if nu==0 or nv==0: return 0.0
    c=float(np.clip(np.dot(u,v)/(nu*nv),-1,1))
    return float(np.degrees(np.arccos(c)))


def main():
    out={"benchmark_id":"M17","family_id":"F17","gate":"finite_background_vs_CPL","status":"PASS","z_nodes":Z.tolist(),"Omega_m0":OM,"Omega_de0":ODE0,"cases":[]}
    for c in CS:
        r1,o1=hde_resid(c,1e-11,1e-13)
        r2,o2=hde_resid(c,3e-12,3e-14)
        denom=max(np.linalg.norm(r2),1e-30)
        conv=float(np.linalg.norm(r1-r2)/denom)
        ang=angle_deg(r1,r2)
        fits=[]
        for st in STARTS:
            q=least_squares(lambda p: cpl_resid(p[0],p[1])-r2,np.array(st),bounds=BOUNDS,xtol=1e-13,ftol=1e-13,gtol=1e-13,max_nfev=10000)
            rr=cpl_resid(q.x[0],q.x[1])-r2
            fits.append({"start":list(st),"success":bool(q.success),"w0":float(q.x[0]),"wa":float(q.x[1]),"objective_norm":float(np.linalg.norm(rr))})
        best=min(fits,key=lambda x:x["objective_norm"])
        rbest=cpl_resid(best["w0"],best["wa"])
        frac=float(np.linalg.norm(r2-rbest)/max(np.linalg.norm(r2),1e-30))
        if frac<=0.10: cls="BACKGROUND_ABSORBED_BY_CPL_WITH_SCOPE"
        elif frac>=0.30: cls="BACKGROUND_SEPARATED_FROM_CPL_WITH_SCOPE"
        else: cls="BACKGROUND_INCONCLUSIVE"
        hard=conv<=1e-4 and ang<=0.02 and all(x["success"] for x in fits)
        if not hard: out["status"]="FAIL_HARD_GATE"
        out["cases"].append({"c":c,"Omega_de_nodes":o2.tolist(),"response":r2.tolist(),"response_norm":float(np.linalg.norm(r2)),"convergence_rel_norm":conv,"convergence_angle_deg":ang,"all_optimizer_success":all(x["success"] for x in fits),"fits":fits,"best_fit":{"w0":best["w0"],"wa":best["wa"],"residual_fraction":frac,"classification":cls}})
    p=Path("waves/wave_03_expanded_dark_energy/M17_HDE_BACKGROUND_CPL_RESULT.json")
    p.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if out["status"]!="PASS": raise SystemExit(2)

if __name__=="__main__": main()
