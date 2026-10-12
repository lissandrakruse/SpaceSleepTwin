"""Factorial light-input decomposition; not a causal decomposition of HERA data."""
import json, pathlib, io, contextlib, base64
import matplotlib
matplotlib.use('Agg')
root=pathlib.Path(__file__).resolve().parent
nb=json.loads((root/'spacesleeptwin_hera_benchmark.ipynb').read_text())
if nb['cells'][-2].get('cell_type')=='markdown' and ''.join(nb['cells'][-2].get('source',[])).startswith('## Factorial decomposition'):
    nb['cells']=nb['cells'][:-2]
defs=''.join(nb['cells'][1]['source']).split('primary=compare()')[0].replace('from IPython.display import display','')
scope={}
exec(defs,scope)
code='''# Four schedules with identical initial state and sleep timing.
# Sleep exposure remains zero; "evening" means the last 3h awake.
for levels in LIGHTS.values():
    standard_day, standard_evening = levels["SLS"]
    dynamic_day, dynamic_evening = levels["DLS"]
    levels["DAY_ONLY"] = (dynamic_day, standard_evening)
    levels["EVENING_ONLY"] = (standard_day, dynamic_evening)

def decompose(tau=24.2, location="L1_photopic", step=1/120):
    phases={c:run(c,tau=tau,location=location,step=step) for c in ["SLS","DAY_ONLY","EVENING_ONLY","DLS"]}
    result=phases["SLS"][["mission_day"]].copy()
    for c in phases:
        result[c]=circ_diff(phases[c].phase_proxy_h,phases["SLS"].phase_proxy_h)
    result["interaction_h"]=result.DLS-result.DAY_ONLY-result.EVENING_ONLY
    return result

factorial=decompose()
display(factorial.round(4))
means=factorial.drop(columns="mission_day").mean()
display(means.round(4))
checks=[]
for location in ["L1_photopic","L2_photopic"]:
    for tau in [23.8,24.2,24.6]:
        values=decompose(tau=tau,location=location).drop(columns="mission_day").mean()
        checks.append(dict(location=location,tau=tau,**values.to_dict()))
factorial_sensitivity=pd.DataFrame(checks)
display(factorial_sensitivity.round(4))
assert np.max(np.abs(factorial.SLS))<1e-9
assert np.allclose(factorial.DLS,factorial.DAY_ONLY+factorial.EVENING_ONLY+factorial.interaction_h)
fig,ax=plt.subplots(figsize=(8,4))
ax.bar(["Day only","Evening only","Full dynamic","Interaction"],
       means[["DAY_ONLY","EVENING_ONLY","DLS","interaction_h"]],color=["#6495ed","#e9a445","#22a6a6","#888888"])
ax.axhline(0,color="black",lw=.8)
ax.set(ylabel="Phase-proxy contrast vs SLS (hours)",title="HERA input decomposition: model counterfactuals")
fig.tight_layout();plt.show()
print("Negative = earlier phase. The interaction is full minus the two partial contrasts.")
print("No percent attribution: the oscillator is nonlinear, and these scenarios were not observed HERA arms.")
'''
scope['display']=lambda x:print(x.to_string() if hasattr(x,'to_string') else str(x))
buf=io.StringIO()
with contextlib.redirect_stdout(buf):exec(code,scope)
print(buf.getvalue(),flush=True)
out=io.BytesIO();scope['plt'].gcf().savefig(out,format='png',dpi=140)
markdown='''## Factorial decomposition of light inputs (exploratory)
Four counterfactual schedules hold sleep timing, initial phase and all model parameters constant. The partial schedules are not HERA treatment arms: they isolate changes in this model, not causal effects in the observed participants. Day-only changes the early waking input; evening-only changes the last three waking hours. Sleep remains dark in every arm.

Primary contrasts use 48h windows and a refined 30-second output grid. The interaction is Δ(full)−Δ(day-only)−Δ(evening-only); it describes nonadditivity in the oscillator. Do not treat partial effects as additive percentages. Sensitivity spans the predefined two habitat levels and three intrinsic periods.

The model receives photopic lux and cannot represent the published spectral change. Photopic eye-level and melanopic horizontal measurements cannot be directly compared as a matched spectral ratio. Whether omission underestimates the physiological contrast has not been demonstrated here.
'''
nb['cells'].extend([{'cell_type':'markdown','metadata':{},'source':markdown.splitlines(keepends=True)},
 {'cell_type':'code','metadata':{},'execution_count':3,'source':code.splitlines(keepends=True),
  'outputs':[{'output_type':'stream','name':'stdout','text':buf.getvalue()},
   {'output_type':'display_data','metadata':{},'data':{'image/png':base64.b64encode(out.getvalue()).decode(),'text/plain':['Factorial light-input decomposition']}}]}])
(root/'spacesleeptwin_hera_benchmark.ipynb').write_text(json.dumps(nb,ensure_ascii=False,indent=1))
payload={'status':'exploratory model counterfactuals','tau':24.2,'location':'L1_photopic','output_grid_hours':1/120,
         'means':scope['means'].to_dict(),'windows':scope['factorial'].to_dict(orient='records'),
         'sensitivity':scope['factorial_sensitivity'].to_dict(orient='records')}
(root/'hera_decomposition.json').write_text(json.dumps(payload,indent=2))
