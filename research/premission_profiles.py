"""Fixed hypothetical outdoor-light profiles; known-target sensitivity, not fitting."""
import numpy as np,pandas as pd,json,pathlib,io,contextlib
from alignment_hera import evolve,minima,circular_mean,circular_difference,mission_phase,PRE,MISSION,WINDOWS

def outdoor_premission(hours,tau=24.2,lux=5000.,center_clock=13.):
    if hours not in [0,1,2,4]:raise ValueError('Fixed durations are 0,1,2,4 hours')
    # Wake begins at 07:00; daylight pulse centered at 13:00.
    midpoint=center_clock-7;begin=midpoint-hours/2;end=midpoint+hours/2
    segments=[(0,16,150.),(16,24,0.)] if hours==0 else [(0,begin,150.),(begin,end,lux),(end,16,150.),(16,24,0.)]
    state=np.array([1.,0.,.5]);ts=[];xs=[]
    for day in range(-21,0):
        for a,b,I in segments:
            t,y=evolve(day*24+a,day*24+b,state,tau,I);state=y[:,-1]
            if day>=-7:ts.extend(t[:-1]);xs.extend(y[0,:-1])
    return state,circular_mean((minima(ts,xs)+7)%24)

def execute_profiles():
    rows=[]
    for hours in [0,1,2,4]:
        state,proxy=outdoor_premission(hours)
        shifts={};errors={};means={}
        for condition in ['SLS','DLS']:
            offset=float(circular_difference(PRE[condition],proxy))
            t,phase=mission_phase(state,24.2,condition)
            mapped=(phase+offset)%24
            windows=[circular_mean(mapped[(t>=(d-1)*24)&(t<(d+1)*24)]) for d in WINDOWS]
            means[condition]=float(circular_mean(windows))
            shifts[condition]=float(circular_difference(means[condition],PRE[condition]))
            errors[condition]=float(circular_difference(means[condition],MISSION[condition]))
        contrast=shifts['SLS']-shifts['DLS']
        rows.append({'outdoor_hours':hours,'premission_proxy_h':float(proxy),
          'SLS_prediction_h':means['SLS'],'DLS_prediction_h':means['DLS'],
          'SLS_delay_h':shifts['SLS'],'DLS_delay_h':shifts['DLS'],
          'benefit_change_contrast_h':contrast,'observed_change_contrast_h':.91,
          'SLS_signed_error_h':errors['SLS'],'DLS_signed_error_h':errors['DLS'],
          'mean_absolute_group_error_h':float(np.mean(np.abs(list(errors.values()))))})
    print(pd.DataFrame(rows).round(4).to_string(index=False),flush=True)
    return {'status':'hypothetical premission sensitivity; all known-target scenarios retained',
      'fixed_settings':{'tau_h':24.2,'warmup_days':21,'baseline_lux':150.,'outdoor_lux':5000.,
                       'pulse_center_clock_h':13.,'pulse_durations_h':[0,1,2,4]},'profiles':rows}

if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parent
    result=execute_profiles();(root/'hera_premission_profiles.json').write_text(json.dumps(result,indent=2))
    p=root/'spacesleeptwin_hera_benchmark.ipynb';nb=json.loads(p.read_text())
    if nb['cells'][-2].get('cell_type')=='markdown' and ''.join(nb['cells'][-2].get('source',[])).startswith('## Hypothetical premission'):
        nb['cells']=nb['cells'][:-2]
    source=pathlib.Path(__file__).read_text().split("if __name__=='__main__':")[0]
    source=source.replace('from alignment_hera import evolve,minima,circular_mean,circular_difference,mission_phase,PRE,MISSION,WINDOWS',
      '# Reuse alignment definitions from the preceding notebook cell.')
    source+='\npremission_profile_results=execute_profiles()\n'
    md='''## Hypothetical premission outdoor-light test
Fixed before execution, after the original known-target benchmark: 21 premission days, 150 photopic lux 07:00–23:00, darkness during sleep, plus 0/1/2/4 h at 5,000 lux centered at 13:00. τ=24.2 h. These pulses are hypothetical; real HERA premission exposures were not reconstructed. All results are retained; do not choose the best matching profile as a validated estimate of exposure.

Group marker offsets are fitted separately to premission means only. Thus the experiment changes both the starting oscillator state and inferred marker offset. It is a calibration sensitivity, not identification of a causal outdoor-light effect. Evaluate both absolute group drifts and their difference (observed 1.98, 1.07, and 0.91 h). Both groups' observed delays do not identify a single common omitted mechanism by themselves.
'''
    nb['cells'].extend([{'cell_type':'markdown','metadata':{},'source':md.splitlines(keepends=True)},
      {'cell_type':'code','metadata':{},'execution_count':6,'source':source.splitlines(keepends=True),
       'outputs':[{'output_type':'stream','name':'stdout','text':pd.DataFrame(result['profiles']).round(4).to_string(index=False)+'\n'}]}])
    p.write_text(json.dumps(nb,ensure_ascii=False,indent=1))
