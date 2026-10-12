"""Premission anchoring and assumed-prior alignment sensitivity, not individual validation."""
import numpy as np, pandas as pd
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks
import json, pathlib, io, contextlib

TARGET=(2.75,5.65)
PRE={'SLS':4.24,'DLS':3.69}
MISSION={'SLS':6.22,'DLS':4.76}
WINDOWS=[5,12,19,26,33,43]

def circular_difference(a,b): return (np.asarray(a)-b+12)%24-12
def circular_mean(a): return np.angle(np.mean(np.exp(np.asarray(a)*2j*np.pi/24)))*24/(2*np.pi)%24
def metrics(phases,target=TARGET):
    start,end=target; width=(end-start)%24
    if width<=0 or width>=12: raise ValueError('Target width must be in (0,12) hours')
    center=(start+width/2)%24
    return {'mean_distance_to_center_h':float(np.mean(np.abs(circular_difference(phases,center)))),
            'fraction_in_window':float(np.mean((np.asarray(phases)-start)%24<=width))}

def model_rhs(t,y,tau,I):
    x,xc,n=y;alpha=.05*np.sqrt(I/9500) if I>0 else 0.
    B=33.75*(1-n)*alpha*(1-.4*x)*(1-.4*xc)
    return [np.pi/12*(xc+B),np.pi/12*(.23*(xc-4*xc**3/3)-x*((24/(.99669*tau))**2+.55*B)),60*(alpha*(1-n)-.0075*n)]

def evolve(start,end,state,tau,I,step=1/120):
    grid=np.linspace(start,end,int(np.ceil((end-start)/step))+1)
    sol=solve_ivp(lambda t,y:model_rhs(t,y,tau,I),(start,end),state,t_eval=grid,
                  rtol=1e-8,atol=1e-10,max_step=.25)
    assert sol.success,sol.message
    return sol.t,sol.y

def minima(times,x,step=1/120):
    times=np.asarray(times);x=np.asarray(x)
    idx,_=find_peaks(-x,distance=int(18/step));result=[]
    for i in idx:
        if not 0<i<len(x)-1:continue
        a,b,c=x[i-1:i+2];delta=np.clip(.5*(a-c)/(a-2*b+c),-1,1)
        t=times[i]+delta*(times[i+1]-times[i])
        result.append(t)
    return np.asarray(result)

def premission(tau=24.2):
    state=np.array([1.,0.,.5]);ts=[];xs=[]
    for day in range(-21,0):
        for begin,end,I in [(0,16,150.),(16,24,0.)]:
            t,y=evolve(day*24+begin,day*24+end,state,tau,I);state=y[:,-1]
            if day>=-7:ts.extend(t[:-1]);xs.extend(y[0,:-1])
    phase=circular_mean((minima(ts,xs)+7)%24)
    return state,phase

def mission_phase(state,tau,condition,initial_shift=0.):
    # Rotate oscillator state by an assumed initial-phase error; photoreceptor n unchanged.
    angle=initial_shift*np.pi/12;c,s=np.cos(angle),np.sin(angle)
    state=np.array([c*state[0]-s*state[1],s*state[0]+c*state[1],state[2]])
    ts=[];xs=[];day_lux,evening_lux={'SLS':(122.,122.),'DLS':(264.,13.)}[condition]
    for day in range(45):
        awake=16 if day%7<2 else 19
        for begin,end,I in [(0,awake-3,day_lux),(awake-3,awake,evening_lux),(awake,24,0.)]:
            t,y=evolve(day*24+begin,day*24+end,state,tau,I);state=y[:,-1]
            ts.extend(t[:-1]);xs.extend(y[0,:-1])
    times=minima(ts,xs)
    return times,(times+7)%24

def anchored_forecast(tau=24.2,anchors=PRE,initial_shift=0.,target=TARGET):
    state,pre_proxy=premission(tau);out={}
    for condition in ['SLS','DLS']:
        # Offsets use PRE ONLY. MISSION is never used to fit any parameter.
        offset=float(circular_difference(anchors[condition],pre_proxy))
        times,proxy=mission_phase(state,tau,condition,initial_shift)
        mapped=(proxy+offset)%24
        window_means=[circular_mean(mapped[(times>=(d-1)*24)&(times<(d+1)*24)]) for d in WINDOWS]
        out[condition]={'offset_h':offset,'premission_proxy_h':pre_proxy,
          'mapped_premission_h':float((pre_proxy+offset)%24),
          'mean_window_phase_h':float(circular_mean(window_means)),
          'window_phases_h':list(map(float,window_means)),
          'daily_phases_h':list(map(float,mapped)),**metrics(mapped,target)}
    return out

def execute_alignment(n_draws=24,seed=20261011):
    # Frozen example uncertainty assumptions, NOT fitted from HERA aggregate means.
    if n_draws<2:raise ValueError('At least two draws required')
    primary=anchored_forecast();rows=[]
    for condition,result in primary.items():
        rows.append({'condition':condition,'pre_anchor_h':PRE[condition],
           'prediction_h':result['mean_window_phase_h'],'observed_h':MISSION[condition],
           'absolute_circular_error_h':float(abs(circular_difference(result['mean_window_phase_h'],MISSION[condition]))),
           'predicted_mean_inside':metrics([result['mean_window_phase_h']])['fraction_in_window']==1,
           'observed_mean_inside':metrics([MISSION[condition]])['fraction_in_window']==1,
           'daily_fraction_inside':result['fraction_in_window'],
           'daily_mean_distance_h':result['mean_distance_to_center_h']})
    print('Aggregate premission-anchored evaluation (conditional offsets per group):')
    print(pd.DataFrame(rows).round(4).to_string(index=False),flush=True)
    # Shared-offset alternative: pooled premission anchor; phase groups no longer both fit.
    shared_anchor=float(circular_mean(list(PRE.values())))
    common=anchored_forecast(anchors={'SLS':shared_anchor,'DLS':shared_anchor})
    print('Common-offset alternative, mission phase predictions:',{c:round(r['mean_window_phase_h'],4) for c,r in common.items()},flush=True)
    rng=np.random.default_rng(seed);draws=[]
    for k in range(n_draws):
        tau=rng.normal(24.2,.15)
        while not 23.8<=tau<=24.6:tau=rng.normal(24.2,.15)
        shift=rng.normal(0.,.25)
        while abs(shift)>1:shift=rng.normal(0.,.25)
        # Same hypothetical person, same sampled state and anchor for both strategies.
        r=anchored_forecast(tau,{'SLS':shared_anchor,'DLS':shared_anchor},shift)
        draws.append({'tau_h':float(tau),'initial_shift_h':float(shift),
          'SLS_distance_h':r['SLS']['mean_distance_to_center_h'],
          'DLS_distance_h':r['DLS']['mean_distance_to_center_h'],
          'SLS_fraction':r['SLS']['fraction_in_window'],'DLS_fraction':r['DLS']['fraction_in_window']})
        if (k+1)%6==0:print(f'Assumed-prior draws completed: {k+1}/{n_draws}',flush=True)
    mc=pd.DataFrame(draws);difference=mc.SLS_distance_h-mc.DLS_distance_h
    result={'status':'known aggregate benchmark and assumed-prior sensitivity, not individual posterior',
      'target_h':TARGET,'center_h':4.2,'primary':rows,'calibration':primary,
      'shared_offset_predictions':{c:r['mean_window_phase_h'] for c,r in common.items()},
      'uncertainty_assumptions':{'tau':'Normal(24.2,0.15), truncated to [23.8,24.6]',
         'initial_phase_error':'Normal(0,0.25 h), truncated to [-1,1] h',
         'shared_hypothetical_premission_anchor_h':shared_anchor,'seed':seed,'draws':n_draws},
      'assumption_conditional_probability_DLS_closer':float(np.mean(difference>1e-6)),
      'tie_fraction':float(np.mean(abs(difference)<=1e-6)),
      'distance_gain_quantiles_h':list(map(float,np.quantile(difference,[.05,.5,.95]))),
      'mean_daily_fraction':{'SLS':float(mc.SLS_fraction.mean()),'DLS':float(mc.DLS_fraction.mean())},
      'synthetic_draws':draws}
    print('Assumption-conditional probability DLS closer:',result['assumption_conditional_probability_DLS_closer'],flush=True)
    print('Synthetic-draw mean daily fractions:',result['mean_daily_fraction'],flush=True)
    # Checks for both early and late penalties, wraparound, and independent calibration.
    assert abs(metrics([3.2])['mean_distance_to_center_h']-metrics([5.2])['mean_distance_to_center_h'])<1e-9
    assert metrics([23.5],(23.,1.))['fraction_in_window']==1
    assert metrics([2.],(23.,1.))['fraction_in_window']==0
    assert all(abs(circular_difference(primary[c]['mapped_premission_h'],PRE[c]))<1e-9 for c in PRE)
    print('Circular target and premission-calibration checks passed.',flush=True)
    return result

if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parent
    result=execute_alignment()
    (root/'hera_alignment.json').write_text(json.dumps(result,indent=2))
    nb_path=root/'spacesleeptwin_hera_benchmark.ipynb';nb=json.loads(nb_path.read_text())
    if nb['cells'][-2].get('cell_type')=='markdown' and ''.join(nb['cells'][-2].get('source',[])).startswith('## Absolute alignment'):
        nb['cells']=nb['cells'][:-2]
    source=pathlib.Path(__file__).read_text().split("if __name__=='__main__':")[0]
    source+='\nalignment_results=execute_alignment()\n'
    # Retain actual aggregate results, not a second Monte Carlo execution.
    display=json.dumps({k:result[k] for k in ['primary','shared_offset_predictions','uncertainty_assumptions',
      'assumption_conditional_probability_DLS_closer','mean_daily_fraction','distance_gain_quantiles_h']},indent=2)
    md='''## Absolute alignment: premission anchoring and assumed uncertainty
Target aMT6s window: 02:45–05:39; center 04:12. Mapping is fitted using only published premission means (SLS 4.24 h; DLS 3.69 h), then evaluated against known mission means. The assumed model premission routine is not observed exposure. Separate group offsets absorb group phase differences and do not establish a universal biological marker mapping. A shared-offset alternative is also reported.

Daily metrics are model fractions and distances, not measured daily biomarkers or a reproduction of the study's individual alignment percentages. Greater advance is not automatically better alignment. A constant-offset mapping between x-min and aMT6s is an unvalidated assumption.

Uncertainty uses 24 matched, synthetic Monte Carlo draws from explicitly assumed distributions of tau and initial phase error. The common 3.965 h starting anchor represents a hypothetical subject, not either HERA group or an individual astronaut. The probability is conditional on these assumptions, not a calibrated patient/astronaut posterior. Finite Monte Carlo sampling and uncertainty about model structure remain. Individual premission measures and exposure are needed to estimate actual calibration uncertainty.
'''
    nb['cells'].extend([{'cell_type':'markdown','metadata':{},'source':md.splitlines(keepends=True)},
      {'cell_type':'code','metadata':{},'execution_count':5,'source':source.splitlines(keepends=True),
       'outputs':[{'output_type':'stream','name':'stdout','text':display+'\n'}]}])
    nb_path.write_text(json.dumps(nb,ensure_ascii=False,indent=1))
