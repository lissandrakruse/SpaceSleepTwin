"""Fixed exploratory ridge ablation: same folds, with/without NASA lunar covariates."""
import csv,json,math
from datetime import date
from pathlib import Path
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.model_selection import LeaveOneGroupOut

root=Path('analysis/lunar_ucr')
rows=list(csv.DictReader((root/'joined_diaries.csv').open()))
if not all(math.isfinite(float(r[t])) for r in rows for t in ['sleepdelay_minutes','sleep_duration_hours']):
    raise ValueError('Missing or nonfinite endpoint; needs explicit exclusion audit')
days=[date.fromisoformat(r['evening_date']) for r in rows]; first=min(days)
X=np.array([[int(r['daytype']=='a work day'),math.sin(2*math.pi*d.weekday()/7),math.cos(2*math.pi*d.weekday()/7),(d-first).days] for r,d in zip(rows,days)])
L=np.array([[float(r['lunar_illuminated_percent_at_18h']),float(r['moon_above_horizon_hour_samples'])] for r in rows])
groups=np.array([r['participant_id'] for r in rows]); unique_dates=sorted(set(days)); blocks=np.array_split(unique_dates,4)
splits={'participant_held_out':list(LeaveOneGroupOut().split(X,groups=groups)), 'forward_calendar_blocks':[(np.array([i for i,d in enumerate(days) if d<block[0]]),np.array([i for i,d in enumerate(days) if d in block])) for block in blocks[1:]]}
records=[];metrics={}
for validation,folds in splits.items():
    metrics[validation]={}
    for target in ['sleepdelay_minutes','sleep_duration_hours']:
        y=np.array([float(r[target]) for r in rows]); bucket={}
        for model,features in [('calendar_workday',X),('calendar_workday_plus_lunar',np.column_stack((X,L)))]:
            truth=[]; predictions=[]
            for fold,(train,test) in enumerate(folds):
                if validation=='participant_held_out': assert not set(groups[train])&set(groups[test])
                else: assert max(days[i] for i in train)<min(days[i] for i in test)
                m=make_pipeline(StandardScaler(),Ridge(alpha=10.0));m.fit(features[train],y[train]);pred=m.predict(features[test])
                for i,p in zip(test,pred):
                    records.append(dict(validation=validation,target=target,model=model,fold=fold,participant_id=rows[i]['participant_id'],evening_date=rows[i]['evening_date'],observed=y[i],predicted=p))
                truth.extend(y[test]);predictions.extend(pred)
            bucket[model]={'n_predictions':len(truth),'mae':mean_absolute_error(truth,predictions),'rmse':float(np.sqrt(mean_squared_error(truth,predictions)))}
        metrics[validation][target]=bucket
report={'estimator':'StandardScaler fit on training rows only + Ridge(alpha=10), fixed alpha, no tuning','baseline_features':['workday','weekday sine','weekday cosine','elapsed calendar days'],'added_lunar_features':['illuminated disk percent at 18h local','count of positive geometric elevations at hourly 18h–23h local'],'metrics':metrics,'interpretation':'Exploratory ablation, not causal or external validation. Calendar-block evaluation tests later dates, may include previously observed people. Participant holdout can share dates across train/test and is insufficient alone for lunar claims. No negative prediction clipping or removal of long sleep delays. Sleep duration errors in hours; delay errors in minutes.'}
(root/'model_results.json').write_text(json.dumps(report,indent=2)+'\n')
with (root/'model_predictions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
print(json.dumps(report,indent=2))
