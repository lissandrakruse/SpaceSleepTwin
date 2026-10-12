"""Prespecified schedule × metric sensitivity; melEDI is an unvalidated proxy."""
import json,pathlib,io,contextlib
root=pathlib.Path(__file__).resolve().parent
p=root/'spacesleeptwin_hera_benchmark.ipynb';nb=json.loads(p.read_text())
if nb['cells'][-2].get('cell_type')=='markdown' and ''.join(nb['cells'][-2].get('source',[])).startswith('## Sleep-schedule and metric sensitivity'):
    nb['cells']=nb['cells'][:-2]
defs=''.join(nb['cells'][1]['source']).split('primary=compare()')[0].replace('from IPython.display import display','')
# Freeze the modified run function before evaluating the new schedules.
defs=defs.replace('cycle_offset=0, step=1/12):','cycle_offset=0, step=1/12, conventional=False):')
defs=defs.replace('awake = 16. if (day+cycle_offset)%7 < 2 else 19.','awake = 16. if conventional or (day+cycle_offset)%7 < 2 else 19.')
scope={};exec(defs,scope)
code='''# Fixed before evaluating: 45 days, τ=24.2 h, common premission state,
# same six windows; HERA schedule vs seven 23:00–07:00 nights per week.
# Eye-level L1 photopic vs naive eye-level L1 melEDI substitution.
import inspect
# Notebook standalone definition of modified run: needed for reproducibility.
'''+defs[defs.index('def run('):defs.index('def circ_diff(')]+'''
for levels in LIGHTS.values():
    sd,se=levels["SLS"];dd,de=levels["DLS"]
    levels["DAY_ONLY"]=(dd,se);levels["EVENING_ONLY"]=(sd,de)
records=[]
for conventional in [False,True]:
    for location in ["L1_photopic","L1_melEDI_proxy"]:
        phases={c:run(c,tau=24.2,location=location,step=1/120,conventional=conventional)
                for c in ["SLS","DAY_ONLY","EVENING_ONLY","DLS"]}
        contrasts={c:float(circ_diff(phases[c].phase_proxy_h,phases["SLS"].phase_proxy_h).mean()) for c in phases}
        records.append(dict(schedule="conventional_23_07" if conventional else "HERA_variable",
                            metric=location,**contrasts,
                            interaction_h=contrasts["DLS"]-contrasts["DAY_ONLY"]-contrasts["EVENING_ONLY"]))
robustness=pd.DataFrame(records)
display(robustness.round(4))
assert all(abs(r["SLS"])<1e-9 for r in records)
print("Comparison of relative effects is limited to these fixed model settings.")
print("melEDI substitution changes the numeric forcing, not the validated spectral sensitivity of Forger99.")
'''
scope['display']=lambda x:print(x.to_string())
out=io.StringIO()
with contextlib.redirect_stdout(out):exec(code,scope)
print(out.getvalue(),flush=True)
md='''## Sleep-schedule and metric sensitivity (fixed before evaluation)
These tests use τ=24.2 h, 45 days and the six fixed assessment windows. Conventional sleep is 23:00–07:00 every night, with dimming at 20:00. HERA alternates two 8h and five 5h nights. Both use the same assumed premission state. The change therefore combines sleep timing and opportunity duration; it does not isolate bedtime independently of sleep duration.

The spectral sensitivity test substitutes the eye-level L1 melanopic EDI inputs already present in the notebook (SLS 89; DLS day 233, evening 8). Forger99 remains a photopic-input model: this substitution is an unvalidated proxy, not proof of spectral robustness in people. Record all four combinations without choosing a favorable one.
'''
nb['cells'].extend([{'cell_type':'markdown','metadata':{},'source':md.splitlines(keepends=True)},
 {'cell_type':'code','metadata':{},'execution_count':4,'source':code.splitlines(keepends=True),
  'outputs':[{'output_type':'stream','name':'stdout','text':out.getvalue()}]}])
p.write_text(json.dumps(nb,ensure_ascii=False,indent=1))
(root/'hera_robustness.json').write_text(json.dumps({'tau':24.2,'days':45,'status':'exploratory scenarios; melEDI substitution unvalidated','scenarios':scope['records']},indent=2))
