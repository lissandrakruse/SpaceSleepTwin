"""Exploratory nested participant validation of prior-visit personalization."""
import csv, hashlib, json, math
from pathlib import Path
from statistics import median, mean

TARGETS = ['observed_phase_shift_minutes', 'sleep_latency_to_10min_continuous_sleep_minutes']
WEIGHTS = [0, .1, .25, .5, .75, 1]


def examples(rows, target):
    result = []
    for r in rows:
        previous = [t for t in rows if t['participant_id'] == r['participant_id'] and int(t['visit']) < int(r['visit'])]
        if previous:
            result.append((r, median(float(t[target]) for t in previous)))
    return result


def predict(base, history, weight):
    return (1-weight)*base + weight*history


def run(source, out):
    raw = source.read_bytes()
    rows = [r for r in csv.DictReader(raw.decode().splitlines()) if r['phase_alignment_status'] == 'matched']
    if len({(r['participant_id'],r['visit']) for r in rows}) != len(rows):
        raise ValueError('Duplicate visits')
    people = sorted({r['participant_id'] for r in rows})
    records = []
    metrics = {}
    for target in TARGETS:
        ex = examples(rows, target)
        for person in people:
            train = [r for r in rows if r['participant_id'] != person]
            test = [(r,h) for r,h in ex if r['participant_id'] == person]
            if not test:
                continue
            scores = {w: [] for w in WEIGHTS}
            for inner_person in sorted({r['participant_id'] for r in train}):
                inner_train = [r for r in train if r['participant_id'] != inner_person]
                inner_test = [(r,h) for r,h in examples(train,target) if r['participant_id'] == inner_person]
                if not inner_test:
                    continue
                base = median(float(r[target]) for r in inner_train)
                for w in WEIGHTS:
                    scores[w].append(mean(abs(predict(base,h,w)-float(r[target])) for r,h in inner_test))
            weight = min(WEIGHTS, key=lambda w: (mean(scores[w]), w))
            base = median(float(r[target]) for r in train)
            for r,h in test:
                records.append({'target':target,'participant_id':person,'visit':r['visit'],'observed_minutes':float(r[target]),'prior_visit_median_minutes':h,'baseline_minutes':base,'history_only_minutes':h,'nested_personalized_minutes':predict(base,h,weight),'selected_weight':weight})
        these = [r for r in records if r['target'] == target]
        metrics[target] = {}
        for model in ['baseline','history_only','nested_personalized']:
            errors = [r[model+'_minutes']-r['observed_minutes'] for r in these]
            byperson = [mean(abs(r[model+'_minutes']-r['observed_minutes']) for r in these if r['participant_id']==p) for p in sorted({r['participant_id'] for r in these})]
            metrics[target][model] = {'mae_minutes':mean(map(abs,errors)),'rmse_minutes':math.sqrt(mean(e*e for e in errors)),'participant_macro_mae_minutes':mean(byperson)}
    report = {'source_sha256':hashlib.sha256(raw).hexdigest(),'eligible_visits_per_endpoint':len(records)//2,'eligible_participants':len({r['participant_id'] for r in records}),'weights':WEIGHTS,'selection':'Inner leave-one-participant-out macro MAE; ties choose smaller history weight. Outer participant never used for weight selection or population median. Only strictly earlier matched visits used as personal history.','metrics':metrics,'limitations':['Exploratory analysis on a cohort already inspected; requires independent confirmation.','Different task from first benchmark: repeat-visit forecasting for people with a previous measured outcome. Compare only the same eligible visits here.','No sleep outlier removal, zero retained; excluded source conflicts remain excluded.','Not a mechanistic twin, astronaut validation, causal light effect, or demonstrated daily-life forecast.']}
    out.mkdir(parents=True,exist_ok=True)
    with (out/'predictions.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0])); w.writeheader(); w.writerows(records)
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return records, report

if __name__=='__main__':
    _,result=run(Path('analysis/blume_experiment/matched_endpoints.csv'),Path('analysis/blume_personalization'))
    print(json.dumps(result,indent=2))
