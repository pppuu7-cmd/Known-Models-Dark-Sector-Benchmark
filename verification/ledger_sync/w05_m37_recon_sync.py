#!/usr/bin/env python3
import csv
from pathlib import Path

RECON = {'F34','F36','F38','F39','F41','F42','F43'}


def patch_csv(path, kind):
    p = Path(path)
    rows = list(csv.DictReader(p.open(newline='', encoding='utf-8')))
    fields = list(rows[0].keys())
    for r in rows:
        fid = r['family_id']
        if kind == 'census':
            if fid == 'F37':
                r['status'] = 'K0_PARTIAL_EXECUTABLE_PROVIDER_PROVENANCE_OPEN'
                r['notes'] = (
                    'Exact-pin Speeddemon5050/Modified-CLASS-fT-Exact-@74e6a8679cdc233fb339c67127ed0921ba547894 builds and both frozen n_fT=0 and n_fT=0.10 arms execute with finite TT/P(k). '
                    'Active response is nonzero (TT normalized L2 0.0114841754; P(k) 0.0157569608). Publication/author provenance remains open, so K0 is PARTIAL rather than PASS; K1-K9 open; no physical falsification. Canonical recovery run 34652066337 artifact 10284291219.'
                )
            elif fid in RECON and r['status'] == 'QUEUED':
                r['status'] = 'PROVIDER_RECON_NO_GRADE_CANDIDATE_K0_OPEN'
                r['notes'] = (r.get('notes','') + ' Frozen seven-lane public-GitHub reconnaissance run 34650903154 found no provider-grade candidate in the preregistered keyword tranche. This is an open provider/provenance boundary, not physical falsification; do not repeat the same keyword tranche.').strip()
        else:
            if fid == 'F37':
                r['K0'] = 'PARTIAL'
                for i in range(1,10):
                    k=f'K{i}'
                    if r[k] == 'NOT_TESTED':
                        r[k] = 'OPEN'
                r['overall_status'] = 'K0_PARTIAL_EXECUTABLE_PROVIDER_PROVENANCE_OPEN_K1_K9_OPEN'
                r['notes'] = (
                    'f(T): exact-pin provider build and two frozen arms execute with finite TT/P(k) and active response in run 34652066337, artifact 10284291219, digest sha256:e885cda93e26c13268f86e58e667aa8596d0cbeff4e26ff8f80a4edece32f4b5. '
                    'K0 remains PARTIAL because publication/author provenance is unresolved; K1-K9 OPEN; no physical falsification.'
                )
            elif fid in RECON:
                if r['K0'] == 'NOT_TESTED':
                    r['K0'] = 'OPEN'
                r['overall_status'] = 'PROVIDER_RECON_NO_GRADE_CANDIDATE_K0_OPEN'
                r['notes'] = (r.get('notes','') + ' Public-provider reconnaissance run 34650903154 returned zero provider-grade candidates in the frozen search tranche. Coverage remains OPEN; absence of a search hit is not a family failure.').strip()
    with p.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def append_once(path, marker, text):
    p=Path(path)
    old=p.read_text(encoding='utf-8')
    if marker not in old:
        p.write_text(old.rstrip() + '\n\n' + text.strip() + '\n', encoding='utf-8')

patch_csv('matrices/model_family_census.csv','census')
patch_csv('matrices/mandatory_properties_matrix.csv','mandatory')

append_once('recovery/STATE.md','W05 M37 f(T) executable provider partial K0 evidence', r'''
## 2026-09-12 — W05 M37 f(T) executable provider partial K0 evidence
Run `34652066337` (artifact `10284291219`, digest `sha256:e885cda93e26c13268f86e58e667aa8596d0cbeff4e26ff8f80a4edece32f4b5`) repaired only the output-root harness path after preregistration `protocol/W05_M37_K0_OUTPUT_ROOT_RECOVERY_v0.1.md`. Exact provider `Speeddemon5050/Modified-CLASS-fT-Exact-@74e6a8679cdc233fb339c67127ed0921ba547894` builds; n_fT=0 and n_fT=0.10 both exit 0 with finite TT/P(k). Active response: TT normalized-L2 `0.011484175401063655`, P(k) `0.015756960779908492` > frozen 1e-6 activity threshold. Analyzer classification: `M37_K0_PARTIAL_EXECUTABLE_FT_PROVIDER_PROVENANCE_OPEN`; K0 remains PARTIAL because publication/author provenance is open. K1-K9 open. No physical falsification.

Seven-lane provider reconnaissance run `34650903154` returned zero provider-grade candidates for M34/M36/M38/M39/M41/M42/M43 in the frozen keyword tranche. This is a provider-search boundary only; no K0 promotion and no physical failure. Do not repeat the same keyword tranche.
''')

append_once('recovery/RESTORE_FROM_NEW_CHAT.md','W05 current provider frontier (2026-09-12)', r'''
### W05 current provider frontier (2026-09-12)
- M37 f(T): exact-pin executable provider evidence is positive but K0 is only PARTIAL pending publication/author provenance. Canonical run 34652066337, artifact 10284291219.
- M34/M36/M38/M39/M41/M42/M43: frozen seven-lane GitHub reconnaissance run 34650903154 found no provider-grade candidate; coverage stays OPEN, not failed. Use literature-linked provider routes or preregistered verification implementations rather than repeating the same search tranche.
''')

append_once('logs/research_log.md','W05 autonomous iteration — M37 recovery + provider recon', r'''
## 2026-09-12 W05 autonomous iteration — M37 recovery + provider recon
- Consumed run 34650851131 and diagnosed output-root harness mismatch: CLASS emitted `reference__cl.dat` / `active__cl.dat` while the analyzer received touched zero-byte single-underscore placeholders.
- Preregistered recovery at commit 77ab1dc653de2f749a0ff60088b8d67c80391b78; launched corrected workflow at commit 0e38bab4d04a0080239101c7a12715ef4441ee6f.
- Recovery run 34652066337: exact provider pin/build PASS, reference and active exit 0, all four actual TT/P(k) outputs finite, TT response 0.0114841754 and P(k) response 0.0157569608. Classification `M37_K0_PARTIAL_EXECUTABLE_FT_PROVIDER_PROVENANCE_OPEN`; K0 not promoted because authority/provenance remains open; no physical falsification.
- Consumed seven-lane provider reconnaissance run 34650903154: M34/M36/M38/M39/M41/M42/M43 each returned `NO_PROVIDER_GRADE_CANDIDATE_FOUND_IN_FROZEN_SEARCH`, candidate_count=0. Aggregate result: `waves/wave_05_modified_gravity/W05_PARALLEL_PROVIDER_RECON_RESULT_v0.1.json`; no physical inference.
- M32 K0f run 34647841987 attempt 1 failed because the hosted runner received a shutdown signal (exit 143) during corrected stage1, not because of provider/science. Only the failed job/dependents were rerun; scientific criteria unchanged.
''')
