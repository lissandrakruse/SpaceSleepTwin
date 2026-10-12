"""Last fixed aggregate scenarios, followed by an explicit exploration freeze."""
import json,pathlib,pandas as pd,numpy as np,io,contextlib
from alignment_hera import premission,mission_phase,circular_difference,WINDOWS

def final_tests():
    # Published SEs, NOT SDs; illustrative independent-estimates propagation.
    errors={'mission_SLS':.34,'mission_DLS':.53,'pre_SLS':.33,'pre_DLS':.42}
    independence_se=float(np.sqrt(sum(x*x for x in errors.values())))
    cov_scenarios=[]
    for rho in [0.,.5,.8,1.]:
        var=sum(x*x for x in errors.values())-2*rho*(.34*.33+.53*.42)
        cov_scenarios.append({'assumed_equal_within_group_rho':rho,'approx_se_h':float(np.sqrt(var))})
    state,proxy=premission(24.2)
    t,sls=mission_phase(state,24.2,'SLS')
    rows=[]
    for lux in [13.,30.,60.,100.]:
        t_d,dls=mission_phase(state,24.2,'DLS',dls_evening_lux=lux)
        # Fixed 48h windows, circular means; same initial state and baseline.
        def avg(a):return np.angle(np.mean(np.exp(a*2j*np.pi/24)))*24/(2*np.pi)%24
        contrasts=[]
        for day in WINDOWS:
            s=avg(sls[(t>=(day-1)*24)&(t<(day+1)*24)])
            d=avg(dls[(t_d>=(day-1)*24)&(t_d<(day+1)*24)])
            contrasts.append(float(circular_difference(s,d)))
        rows.append({'dls_final_three_hours_photopic_lux':lux,'mean_SLS_minus_DLS_phase_h':float(np.mean(contrasts))})
    print('Illustrative independent-estimates SE:',independence_se,flush=True)
    print(pd.DataFrame(cov_scenarios).to_string(index=False),flush=True)
    print(pd.DataFrame(rows).round(4).to_string(index=False),flush=True)
    assert abs(rows[0]['mean_SLS_minus_DLS_phase_h']-1.3291069)<1e-5
    return {'fixed_settings':{'tau_h':24.2,'DLS_day_lux':264.,'SLS_lux':122.,
               'premission_routine':'150 lux 07:00–23:00, 21 days','late_lux':[13.,30.,60.,100.]},
      'published_SEs_h':errors,'descriptive_change_contrast_h':.91,
      'approx_SE_independence_h':independence_se,'assumed_correlation_scenarios':cov_scenarios,
      'late_light_scenarios':rows,
      'status':'final fixed aggregate sensitivity; no winning setting selected; covariance unavailable'}

if __name__=='__main__':
    root=pathlib.Path(__file__).resolve().parent;result=final_tests()
    (root/'hera_final_aggregate_tests.json').write_text(json.dumps(result,indent=2))
