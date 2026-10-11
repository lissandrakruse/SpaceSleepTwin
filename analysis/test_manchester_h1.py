"""Manchester retrospective H1 benchmark; published plan precedes execution."""
import argparse,csv,hashlib,json,math
from pathlib import Path
from statistics import median
import numpy as np
import pandas as pd
import pyreadr
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import QuantileRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error


def run(raw,out,private):
 audit=json.loads(Path('analysis/manchester_import_audit.json').read_text());tables={};checks={}
 for name in ['light_daily_data.RData','sleep_diary.RData']:
  p=raw/name;sha=hashlib.sha256(p.read_bytes()).hexdigest()
  if sha!=audit['files_sha256'][name]:raise ValueError('Source hash changed '+name)
  checks[name]=sha;tables[name]=next(iter(pyreadr.read_r(str(p)).values()))
 light=tables['light_daily_data.RData'];diary=tables['sleep_diary.RData'].copy();diary['target']=diary.hoursToSleep*60
 diary['local_bedtime']=pd.to_datetime(diary.datetimeGobed,utc=True).dt.tz_convert('Europe/London');diary['night']=(diary.local_bedtime-pd.Timedelta(hours=4)).dt.date
 if diary.duplicated(['Id','night']).any():raise ValueError('Duplicate study night')
 valid_diary=diary[np.isfinite(diary.target)&(diary.target>=0)].copy();joined=light.merge(valid_diary,on=['Id','yday4'],validate='one_to_one');prepared=[];missing=0;short=0
 for _,r in joined.iterrows():
  if not all(np.isfinite(r[k]) and r[k]>=0 for k in ['presleep3hr','TAT250']):missing+=1;continue
  previous=valid_diary[(valid_diary.Id==r.Id)&(valid_diary.night<r.night)]
  if len(previous)<3:short+=1;continue
  assert previous.night.max()<r.night
  prepared.append(dict(person=str(r.Id),night=str(r.night),observed=float(r.target),history=float(previous.target.median()),history_log=float(np.median(np.log1p(previous.target))),presleep_log=float(np.log1p(r.presleep3hr)),daytime=float(r.TAT250),prior_nights=len(previous)))
 rows=sorted(prepared,key=lambda r:(r['night'],r['person']));dates=np.array([r['night'] for r in rows]);people=np.array([r['person'] for r in rows]);blocks=np.array_split(sorted(set(dates)),4)
 folds=[(np.where(dates<b[0])[0],np.where(np.isin(dates,b))[0]) for b in blocks[1:]]
 y=np.array([r['observed'] for r in rows]);h=np.array([r['history'] for r in rows]);hl=np.array([r['history_log'] for r in rows]);X=np.array([[r['presleep_log'],r['daytime']] for r in rows]);records=[];metrics={};fold_details=[];fit_diagnostics=[]
 for f,(train,test) in enumerate(folds):
  if len(train)<20 or len(set(people[train]))<5:raise ValueError('Insufficient initial training under fixed plan')
  assert max(dates[train])<min(dates[test])
  fold_details.append(dict(fold=f,train_nights=len(train),train_people=len(set(people[train])),test_nights=len(test),test_people=len(set(people[test])),latest_training_date=max(dates[train]),first_test_date=min(dates[test])))
 for model in ['personal_history','history_residual_median','presleep_light','daytime_light','joint_light','joint_light_log_outcome']:
  for fold,(train,test) in enumerate(folds):
   if model=='personal_history':prediction=h[test]
   elif model=='history_residual_median':prediction=h[test]+np.median(y[train]-h[train])
   else:
    features=X[:,[0]] if model=='presleep_light' else X[:,[1]] if model=='daytime_light' else X
    log=model=='joint_light_log_outcome';residual=np.log1p(y)-hl if log else y-h
    m=make_pipeline(StandardScaler(),QuantileRegressor(quantile=.5,alpha=.05,solver='highs'));m.fit(features[train],residual[train]);fit_diagnostics.append(dict(model=model,fold=fold,intercept=float(m[-1].intercept_),standardized_feature_coefficients=[float(v) for v in m[-1].coef_]));pred=m.predict(features[test]);prediction=np.expm1(hl[test]+pred) if log else h[test]+pred
   for i,p in zip(test,prediction):records.append(dict(model=model,fold=fold,participant_id=people[i],night=dates[i],observed=y[i],predicted=float(p)))
  rs=[r for r in records if r['model']==model];errors=np.array([r['predicted']-r['observed'] for r in rs]);macro=[np.mean([abs(r['predicted']-r['observed']) for r in rs if r['participant_id']==p]) for p in sorted({r['participant_id'] for r in rs})]
  metrics[model]={'test_nights':len(rs),'test_people':len(macro),'mae_minutes':float(np.mean(abs(errors))),'rmse_minutes':float(np.sqrt(np.mean(errors**2))),'median_absolute_error_minutes':float(np.median(abs(errors))),'participant_macro_mae_minutes':float(np.mean(macro)),'negative_predictions':sum(r['predicted']<0 for r in rs)}
 baseline_keys={(r['participant_id'],r['night']) for r in records if r['model']=='personal_history'}
 for model in metrics:assert {(r['participant_id'],r['night']) for r in records if r['model']==model}==baseline_keys
 uncertainty={};lookup={(r['model'],r['participant_id'],r['night']):r for r in records};testpeople=sorted({p for p,_ in baseline_keys});rng=np.random.default_rng(20261011)
 for reference in ['personal_history','history_residual_median']:
  sums=[];counts=[]
  for p in testpeople:
   rs=[r for r in records if r['model']=='joint_light' and r['participant_id']==p];d=[abs(r['predicted']-r['observed'])-abs(lookup[(reference,p,r['night'])]['predicted']-r['observed']) for r in rs];sums.append(sum(d));counts.append(len(d))
  sums=np.array(sums);counts=np.array(counts);draws=rng.integers(0,len(testpeople),size=(2000,len(testpeople)));boot=sums[draws].sum(axis=1)/counts[draws].sum(axis=1)
  uncertainty[reference]={'mae_difference_joint_minus_reference_minutes':float(sums.sum()/counts.sum()),'paired_participant_95_percentile_interval_minutes':[float(v) for v in np.quantile(boot,[.025,.975])]}
 values=valid_diary.target.to_numpy();discrepancy=~np.isclose(diary.hoursToSleep,diary.sleepTime-diary.gobedTime,atol=1e-6)
 report={'plan_commit':'42663ae65f43cd4f9e3dab19c736505210bc709b','source_commit':audit['upstream_commit'],'source_hashes':checks,'diary_rows':len(diary),'light_rows':len(light),'joined_rows':len(joined),'joined_people':int(joined.Id.nunique()),'invalid_diary_rows':len(diary)-len(valid_diary),'excluded_missing_light':missing,'excluded_short_history':short,'eligible_nights':len(rows),'eligible_people':len(set(people)),'folds':fold_details,'metrics':metrics,'fit_diagnostics':fit_diagnostics,'joint_light_paired_uncertainty':uncertainty,'latency_clock_field_disagreement_rows':int(discrepancy.sum()),'diary_reported_minutes':{'unique_values':sorted(set(float(v) for v in values)),'fraction_at_multiple_5':float(np.mean(np.isclose(values/5,np.round(values/5)))),'fraction_at_multiple_10':float(np.mean(np.isclose(values/10,np.round(values/10)))),'fraction_at_multiple_15':float(np.mean(np.isclose(values/15,np.round(values/15))))},'interpretation':'Retrospective exposure-conditioned evaluation of reported latency, not deployable pre-bedtime prediction, causal H1 confirmation, or astronaut validation. presleep3hr ends at observed Fitbit sleep onset.','bootstrap':'2000 fixed-prediction participant cluster resamples; conditional intervals ignore refitting and between-person calendar dependence.','software':{'numpy':np.__version__,'pandas':pd.__version__}}
 out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');private.mkdir(parents=True,exist_ok=True)
 with (private/'predictions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--raw',type=Path,required=True);p.add_argument('--output',type=Path,default=Path('analysis/manchester_h1'));p.add_argument('--private-output',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.raw,a.output,a.private_output),indent=2))
