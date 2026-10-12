"""Expand the same assumed-prior calculation; binomial interval is MC-only."""
import pathlib,json,pandas as pd,numpy as np
from alignment_hera import execute_alignment

def wilson_interval(k,n,z=1.96):
    p=k/n;denom=1+z*z/n
    center=(p+z*z/(2*n))/denom
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/denom
    return [float(max(0,center-half)),float(min(1,center+half))]

if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parent
    result=execute_alignment(n_draws=256,seed=20261011)
    a=pd.DataFrame(result['synthetic_draws']);diff=a.SLS_distance_h-a.DLS_distance_h
    counts={'DLS':int((diff>1e-6).sum()),'SLS':int((diff< -1e-6).sum()),'tie':int((abs(diff)<=1e-6).sum())}
    result['sampling_only_fractions']={k:{'count':v,'fraction':v/256,
       'wilson_95_interval':wilson_interval(v,256)} for k,v in counts.items()}
    print('Monte Carlo sampling only:',result['sampling_only_fractions'],flush=True)
    (root/'hera_alignment_256.json').write_text(json.dumps(result,indent=2))
    p=root/'spacesleeptwin_hera_benchmark.ipynb';nb=json.loads(p.read_text())
    if nb['cells'][-2].get('cell_type')=='markdown' and ''.join(nb['cells'][-2].get('source',[])).startswith('## Expanded Monte Carlo'):
        nb['cells']=nb['cells'][:-2]
    code='''# Same explicitly assumed distributions and seed as the 24-draw example.
expanded_alignment=execute_alignment(n_draws=256,seed=20261011)
def wilson_interval(k,n,z=1.96):
    p=k/n;denom=1+z*z/n
    center=(p+z*z/(2*n))/denom
    half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/denom
    return [max(0,center-half),min(1,center+half)]
draws=pd.DataFrame(expanded_alignment["synthetic_draws"])
diff=draws.SLS_distance_h-draws.DLS_distance_h
counts={"DLS":int((diff>1e-6).sum()),"SLS":int((diff< -1e-6).sum()),"tie":int((abs(diff)<=1e-6).sum())}
display(pd.DataFrame([{ "strategy":k,"count":v,"fraction":v/256,
 "sampling_only_95_interval":wilson_interval(v,256)} for k,v in counts.items()]))
'''
    md='''## Expanded Monte Carlo: 256 draws
This repeats the same assumed Normal distributions, bounds, common hypothetical premission anchor and seed. Only the numerical sampling precision increases. The intervals quantify finite Monte Carlo sampling conditional on the fixed assumptions; they do not quantify individual physiological calibration, model validity or a clinical success probability. The draws still use the original 150-lux premission assumption, not a selected outdoor-light profile.
'''
    nb['cells'].extend([{'cell_type':'markdown','metadata':{},'source':md.splitlines(keepends=True)},
      {'cell_type':'code','metadata':{},'execution_count':7,'source':code.splitlines(keepends=True),
       'outputs':[{'output_type':'stream','name':'stdout','text':json.dumps(result['sampling_only_fractions'],indent=2)+'\n'}]}])
    p.write_text(json.dumps(nb,ensure_ascii=False,indent=1))
