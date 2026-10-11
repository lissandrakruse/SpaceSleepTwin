"""Exploratory forward-date ablation with strictly prior personal histories."""
import csv,io,json,math,hashlib
from pathlib import Path
from datetime import datetime,timedelta,timezone,date
from statistics import median
from zoneinfo import ZoneInfo
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error

root=Path('analysis/lunar_ucr');out=Path('analysis/lunar_presleep');out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((root/'joined_diaries.csv').open()))
rows.sort(key=lambda r:(r['evening_date'],r['participant_id']))
zone=ZoneInfo('America/Costa_Rica');moon={}
response=json.loads((root/'horizons_response.json').read_text())
for cells in csv.reader(io.StringIO(response['result'].split('$$SOE')[1].split('$$EOE')[0])):
    if not cells or not cells[0].strip():continue
    utc=datetime.strptime(cells[0].strip(),'%Y-%b-%d %H:%M').replace(tzinfo=timezone.utc)
    moon[utc.astimezone(zone)]=(float(cells[4]),float(cells[5]))
prepared=[];excluded=[]
for r in rows:
    previous=[p for p in rows if p['participant_id']==r['participant_id'] and p['evening_date']<r['evening_date']]
    if len(previous)<3:
        excluded.append(dict(participant_id=r['participant_id'],evening_date=r['evening_date'],reason='fewer_than_3_prior_nights'));continue
    bedtime_offsets=[]
    for p in previous:
        midnight=datetime.combine(date.fromisoformat(p['evening_date']),datetime.min.time()).replace(tzinfo=zone)
        bedtime_offsets.append((datetime.fromisoformat(p['bedtime_local'])-midnight).total_seconds()/3600)
    habitual=median(bedtime_offsets)
    midnight=datetime.combine(date.fromisoformat(r['evening_date']),datetime.min.time()).replace(tzinfo=zone)
    end=midnight+timedelta(hours=habitual);start=end-timedelta(hours=3)
    samples=[(t,e,i) for t,(e,i) in moon.items() if start<=t<end]
    if len(samples)!=3:
        excluded.append(dict(participant_id=r['participant_id'],evening_date=r['evening_date'],reason='incomplete_3_hour_ephemeris'));continue
    d=date.fromisoformat(r['evening_date'])
    prepared.append(dict(r,prior_nights=len(previous),habitual_bedtime_hours_after_evening_midnight=habitual,window_start_local=start.isoformat(),window_end_local=end.isoformat(),moon_above_horizon_fraction=sum(e>0 for _,e,_ in samples)/3,mean_positive_moon_elevation_deg=sum(max(e,0) for _,e,_ in samples)/3,illumination_weighted_availability=sum(i/100 if e>0 else 0 for _,e,i in samples)/3,prior_sleepdelay_median=median(float(p['sleepdelay_minutes']) for p in previous),prior_duration_median=median(float(p['sleep_duration_hours']) for p in previous),latest_history_evening=max(p['evening_date'] for p in previous)))
    assert prepared[-1]['latest_history_evening']<r['evening_date']
with (out/'features.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(prepared[0]));w.writeheader();w.writerows(prepared)
days=[date.fromisoformat(r['evening_date']) for r in prepared];first=min(days);blocks=np.array_split(sorted(set(days)),4)
folds=[(np.array([i for i,d in enumerate(days) if d<b[0]]),np.array([i for i,d in enumerate(days) if d in b])) for b in blocks[1:]]
records=[];metrics={}
for target,history in [('sleepdelay_minutes','prior_sleepdelay_median'),('sleep_duration_hours','prior_duration_median')]:
    y=np.array([float(r[target]) for r in prepared]);h=np.array([float(r[history]) for r in prepared])
    X=np.array([[int(r['daytype']=='a work day'),math.sin(2*math.pi*d.weekday()/7),math.cos(2*math.pi*d.weekday()/7),(d-first).days,float(r['habitual_bedtime_hours_after_evening_midnight']),float(r[history])] for r,d in zip(prepared,days)])
    L=np.array([[float(r['illumination_weighted_availability']),float(r['mean_positive_moon_elevation_deg'])] for r in prepared])
    metrics[target]={}
    for model in ['personal_history_only','history_calendar','history_calendar_plus_presleep_lunar']:
        truth=[];preds=[]
        for fold,(train,test) in enumerate(folds):
            assert max(days[i] for i in train)<min(days[i] for i in test)
            if model=='personal_history_only':prediction=h[test]
            else:
                features=X if model=='history_calendar' else np.column_stack((X,L))
                estimator=make_pipeline(StandardScaler(),Ridge(alpha=10));estimator.fit(features[train],y[train]-h[train]);prediction=h[test]+estimator.predict(features[test])
            for i,p in zip(test,prediction):
                records.append(dict(target=target,model=model,fold=fold,participant_id=prepared[i]['participant_id'],evening_date=prepared[i]['evening_date'],observed=y[i],predicted=p))
            truth.extend(y[test]);preds.extend(prediction)
        metrics[target][model]={'n_predictions':len(truth),'mae':mean_absolute_error(truth,preds),'rmse':float(np.sqrt(mean_squared_error(truth,preds)))}
with (out/'predictions.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
report={'window_hours':3,'minimum_prior_nights':3,'eligible_nights':len(prepared),'eligible_participants':len({r['participant_id'] for r in prepared}),'evaluated_participants':len({r['participant_id'] for r in records}),'excluded':excluded,'join_sha256':hashlib.sha256((root/'joined_diaries.csv').read_bytes()).hexdigest(),'ephemeris_sha256':hashlib.sha256((root/'horizons_response.json').read_bytes()).hexdigest(),'model':'Prior personal outcome median plus residual Ridge(alpha=10) with train-only StandardScaler; no tuning. Calendar controls, habitual bedtime and prior outcome median; add two fixed pre-sleep lunar features.','validation':'Four chronological date blocks; first used only to initialize training. Every prediction has >=3 strictly earlier personal nights; historical outcomes can come from earlier evaluation dates, representing updated operational history. All models evaluated on identical nights.','metrics':metrics,'limitations':['Three-hour window and three-history minimum are fixed exploratory choices after inspecting this cohort. Independent confirmation required.','Hourly geometric elevation and illuminated disk fraction are availability proxies, not measured moonlight; no sunlight/dusk gate, clouds, indoor exposure or individual location.','City campus coordinates and 0 km altitude assumed.','No individual z-score, no lunar/artificial-light interaction; actual personal artificial light has not been established.','Known-person subsequent-night task, not new-person prediction or individual lunar periodicity.','Conditional bootstrap intervals do not capture model refitting or cross-person calendar dependence; no significance or proof of no lunar effect.']}
# Paired participant-cluster bootstrap of existing held-out errors, without refitting.
# This does not capture model-fitting or calendar-block dependence uncertainty.
rng=np.random.default_rng(20261011); uncertainty={}
for target in metrics:
    lookup={(r['model'],r['participant_id'],r['evening_date']):r for r in records if r['target']==target}
    people=sorted({r['participant_id'] for r in records if r['target']==target})
    uncertainty[target]={}
    for reference in ['history_calendar','personal_history_only']:
        totals=[]
        for person in people:
            these=[r for r in records if r['target']==target and r['model']=='history_calendar_plus_presleep_lunar' and r['participant_id']==person]
            differences=[abs(r['predicted']-r['observed'])-abs(lookup[(reference,person,r['evening_date'])]['predicted']-r['observed']) for r in these]
            totals.append((sum(differences),len(differences)))
        sums=np.array([t[0] for t in totals]);counts=np.array([t[1] for t in totals]);draws=rng.integers(0,len(people),size=(2000,len(people)))
        boot=sums[draws].sum(axis=1)/counts[draws].sum(axis=1)
        uncertainty[target][reference]={'mae_difference_lunar_minus_reference':float(sums.sum()/counts.sum()),'paired_cluster_bootstrap_95_percentile_interval':[float(x) for x in np.quantile(boot,[.025,.975])]}
report['uncertainty']=uncertainty
report['bootstrap']='2000 resamples of test participants, seed 20261011; paired fixed predictions; negative difference favors lunar. Conditional descriptive interval, not a significance test; ignores refitting and temporal dependence between people.'
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps({k:v for k,v in report.items() if k!='excluded'},indent=2))
