#!/usr/bin/env python3
import csv,json,pathlib

ROOT=pathlib.Path('.')

def rewrite_csv(path, updater):
    p=ROOT/path
    rows=list(csv.reader(p.open(newline='',encoding='utf-8')))
    rows=updater(rows)
    with p.open('w',newline='',encoding='utf-8') as f:
        csv.writer(f,lineterminator='\n').writerows(rows)

def update_census(rows):
    upd={
      'F26': ('K0_PASS_K1_NOT_ESTABLISHED_DUAL_CHANNEL_K2_K9_OPEN','PBH energy-injection K0 PASS_WITH_SCOPE. W06 dual-channel K1 run 34656476133 is PARTIAL/NOT_ESTABLISHED because evaporation and disk-accretion fraction-to-zero arms are provider/output blocked; discreteness/Poisson/isocurvature remains open; no physical falsification.'),
      'F30': ('K0_K1_HICLASS_DECOUPLING_PASS_K2_K9_OPEN','Horndeski/EFT-DE K0 PASS_WITH_SCOPE with two-provider support. W06 hi_class joint-alpha decoupling K1 PASS_WITH_SCOPE from source run 34656276938 plus parser-only recovery; D_finest/D_coarsest=0.0012228125, log-log r=0.9988840; K2-K9 open.'),
      'F31': ('K0_K1_EFFECTIVE_BH_DECOUPLING_PASS_K2_K9_OPEN','Beyond-Horndeski/DHOST effective-alpha K0 PASS_WITH_SCOPE. W06 decoupling K1 PASS_WITH_SCOPE; D_finest/D_coarsest=3.7468112e-05, log-log r=0.9930893. Covariant GLPV/DHOST closure remains open; K2-K9 open.'),
      'F33': ('K0_PASS_K1_REFERENCE_MAP_CONFIGURATION_BLOCKED_RECOVERY_RUNNING_K2_K9_OPEN','Pinned hi_class cubic Galileon K0 PASS_WITH_SCOPE. W06 reference-map discovery run 34657647905 was blocked at parser-level closure construction because nonnegative Omega_smg arms retained explicit Omega_Lambda/Omega_fld. This is configuration evidence only, not Galileon failure. Parser-compliant recovery is prospectively frozen and running; K1 not promoted.'),
      'F35': ('K0_K1_PINNED_CLASS_LVDM_AETHER_GRAVITY_PASS_K2_K9_OPEN','Pinned CLASS_LVDM preferred-frame/LV scalar-cosmology route: K0 PASS_WITH_SCOPE and frozen weak-coupling GR-limit K1 PASS_WITH_SCOPE. Canonical confirmation run 34657362639 artifact 10286581994 has TT and P(k) monotone contraction with finest/coarsest ratios 0.00116152 and 0.000992176. Full Einstein-Aether SVT closure is not claimed; K2-K9 open.'),
      'F40': ('K0_PASS_K1_IMPLEMENTATION_BLOCKED_K2_K9_OPEN','Pinned EFTCAMB native Horava K0 PASS_WITH_SCOPE. W06 K1 source run 34656276938 is BLOCKED_IMPLEMENTATION because the exact-pin native-zero/GR endpoint does not execute successfully; provider/endpoint boundary only, not physical Horava falsification; K2-K9 open.')
    }
    for r in rows[1:]:
        if r and r[0] in upd:
            r[5]=upd[r[0]][0]
            r[8]=upd[r[0]][1]
    return rows

def update_mandatory(rows):
    for r in rows[1:]:
        if r and r[0]=='F33':
            r[3]='BLOCKED_IMPLEMENTATION_CONFIGURATION_RECOVERY_RUNNING'
            r[12]='K0_PASS_K1_REFERENCE_MAP_CONFIGURATION_BLOCKED_RECOVERY_RUNNING_K2_K9_OPEN'
            r[13]='Covariant/cubic Galileon: pinned hi_class native arm gives K0 PASS_WITH_SCOPE. W06 run 34657647905 artifact 10286258353: all ten reference-map discovery arms stopped at input parsing because the harness retained explicit closure keys forbidden for nonnegative Omega_smg. K1 is not promoted; physical_falsification=false. Parser-compliant recovery is preregistered and running; K2-K9 open.'
    return rows

rewrite_csv(pathlib.Path('matrices/model_family_census.csv'),update_census)
rewrite_csv(pathlib.Path('matrices/mandatory_properties_matrix.csv'),update_mandatory)

# Recompute readiness from mandatory matrix.
rows=list(csv.reader((ROOT/'matrices/mandatory_properties_matrix.csv').open(encoding='utf-8')))
head=rows[0]; data=rows[1:]
OPEN={'OPEN','NOT_TESTED','QUEUED','PENDING'}
def snap(rr):
    gates=[r[2:12] for r in rr]
    vals=[x for g in gates for x in g]
    assessed=sum(x not in OPEN for x in vals)
    positive=sum(x.startswith('PASS') or x.startswith('SUPPORTED') for x in vals)
    k0=[r[2] for r in rr]
    return {'K0_assessed':sum(x not in OPEN for x in k0),'K0_positive':sum(x.startswith('PASS') or x.startswith('SUPPORTED') for x in k0),'assessed_cells':assessed,'assessed_fraction':assessed/len(vals),'families':len(rr),'gate_cells':len(vals),'positive_cells':positive,'positive_fraction':positive/len(vals)}
out={'all_rows_including_M00_control':snap(data),'definition_assessed':'status is not exact OPEN, NOT_TESTED, QUEUED, or PENDING; blocked/partial/not-established outcomes count as investigated, not as positive','definition_positive':'status begins PASS or SUPPORTED only','mechanism_rows_excluding_M00_control':snap([r for r in data if r[0]!='F00']),'schema':'kmdsb_readiness_snapshot_v0.1'}
(ROOT/'audits/KMDSB_READINESS_SNAPSHOT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')

marker='## 2026-09-12 W06 M33/M35 frontier sync'
block=f'''\n\n{marker}\n- M35: exact-pin CLASS_LVDM weak-coupling GR-limit K1 is PASS_WITH_SCOPE; run 34657362639, artifact 10286581994, digest sha256:2ffb54348c923579227c8e75a211fee54ced12e83221a69f00527daaab6edcc0. This is scalar-cosmology preferred-frame scope only, not full Einstein-Aether SVT closure.\n- M33: reference-map discovery run 34657647905, job 103453403141, artifact 10286258353, digest sha256:4b1e9028ba4fb896d722056f55278da4190cb4565e259b56934d2e346dd5e7fd is BLOCKED_IMPLEMENTATION_CONFIGURATION. All arms stopped at provider parser closure rules; no physical falsification. Parser-compliant recovery is prospectively frozen; K1 not promoted.\n- Census lag for F26/F30/F31/F35/F40 synchronized to already-canonical mandatory-matrix classifications.\n'''
for fn in ['recovery/STATE.md','recovery/RESTORE_FROM_NEW_CHAT.md','logs/research_log.md']:
    p=ROOT/fn
    txt=p.read_text(encoding='utf-8')
    if marker not in txt:
        p.write_text(txt.rstrip()+block+'\n',encoding='utf-8')
