"""Direct lunar ablation on exactly the prior pre-sleep evaluation nights."""
import csv,json,hashlib
from pathlib import Path
from datetime import date
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error,mean_squared_error
root=Path('analysis/lunar_presleep');out=Path('analysis/lunar_direct');out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((root/'features.csv').open()));days=[date.fromisoformat(r['evening_date']) for r in rows];blocks=np.array_split(sorted(set(days)),4)
folds=[(np.array([i for i,d in enumerate(days) if d<b[0]]),np.array([i for i,d in enumerate(days) if d in b])) for b in blocks[1:]]
L=np.array([[float(r['illumination_weighted_availability']),float(r['mean_positive_moon_elevation_deg'])] for r in rows]);records=[];metrics={};uncertainty={};rng=np.random.default_rng(20261011)
for target,history in [('sleepdelay_minutes','prior_sleepdelay_median'),('sleep_duration_hours','prior_duration_median')]:
 y=np.array([float(r[target]) for r in rows]);h=np.array([float(r[history]) for r in rows]);metrics[target]={}
 for model in ['history_only','history_bias_correction','history_plus_lunar']:
  truth=[];preds=[]
  for fold,(train,test) in enumerate(folds):
   assert max(days[i] for i in train)<min(days[i] for i in test)
   if model=='history_only':p=h[test]
   elif model=='history_bias_correction':p=h[test]+np.mean(y[train]-h[train])
   else:
    m=make_pipeline(StandardScaler(),Ridge(alpha=10));m.fit(L[train],y[train]-h[train]);p=h[test]+m.predict(L[test])
   for i,pred in zip(test,p):records.append(dict(target=target,model=model,fold=fold,participant_id=rows[i]['participant_id'],evening_date=rows[i]['evening_date'],observed=y[i],predicted=pred))
   truth.extend(y[test]);preds.extend(p)
  metrics[target][model]={'n_predictions':len(truth),'mae':mean_absolute_error(truth,preds),'rmse':float(np.sqrt(mean_squared_error(truth,preds)))}
 lookup={(r['model'],r['participant_id'],r['evening_date']):r for r in records if r['target']==target};people=sorted({r['participant_id'] for r in records if r['target']==target});uncertainty[target]={}
 for reference in ['history_only','history_bias_correction']:
  totals=[]
  for person in people:
   these=[r for r in records if r['target']==target and r['model']=='history_plus_lunar' and r['participant_id']==person]
   diffs=[abs(r['predicted']-r['observed'])-abs(lookup[(reference,person,r['evening_date'])]['predicted']-r['observed']) for r in these];totals.append((sum(diffs),len(diffs)))
  sums=np.array([v[0] for v in totals]);counts=np.array([v[1] for v in totals]);draws=rng.integers(0,len(people),size=(2000,len(people)));boot=sums[draws].sum(axis=1)/counts[draws].sum(axis=1)
  uncertainty[target][reference]={'mae_difference_lunar_minus_reference':float(sums.sum()/counts.sum()),'paired_participant_bootstrap_95_percentile_interval':[float(v) for v in np.quantile(boot,[.025,.975])]}
previous=list(csv.DictReader((root/'predictions.csv').open()))
for target in metrics:
 expected={(r['participant_id'],r['evening_date']) for r in previous if r['target']==target}
 for model in metrics[target]:
  actual={(r['participant_id'],r['evening_date']) for r in records if r['target']==target and r['model']==model};assert actual==expected and len(actual)==115
report={'feature_source_sha256':hashlib.sha256((root/'features.csv').read_bytes()).hexdigest(),'protocol':'Same 115 nights / 30 people and forward date folds as pre-sleep test. Fixed prior median history; residual bias correction or residual Ridge(alpha=10) on two lunar features only. StandardScaler fit on training rows only, no tuning.','metrics':metrics,'uncertainty':uncertainty,'bootstrap':'2000 paired fixed-prediction participant resamples, seed 20261011. Conditional descriptive intervals; no refitting or cross-person temporal dependence modeled.','limitations':['Sequential exploratory analysis of an already inspected cohort; independent replication required.','Lunar features are geometric proxies without darkness, cloud or indoor exposure adjustment.','No causal attribution or astronaut validation.','Adding a feature is not itself regularization; ridge penalty provides regularization.','Short test histories do not diagnose coefficient instability; training information and dependence matter.']}
with (out/'predictions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
