"""Participant-held-out descriptive benchmark; not a calibrated digital twin."""
import argparse, csv, hashlib, json, math, platform
from pathlib import Path
from statistics import mean, median


def run(source, output):
    raw = source.read_bytes()
    rows = list(csv.DictReader(raw.decode().splitlines()))
    kept = [r for r in rows if r['phase_alignment_status'] == 'matched']
    keys = [(r['participant_id'], r['visit']) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate participant/visit')
    participants = sorted({r['participant_id'] for r in kept})
    targets = ['observed_phase_shift_minutes', 'sleep_latency_to_10min_continuous_sleep_minutes']
    predictions, metrics = [], {}
    for target in targets:
        records = []
        for participant in participants:
            train = [r for r in kept if r['participant_id'] != participant]
            test = [r for r in kept if r['participant_id'] == participant]
            assert not {r['participant_id'] for r in train} & {r['participant_id'] for r in test}
            values = [float(r[target]) for r in train]
            if not all(math.isfinite(v) for v in values):
                raise ValueError('Nonfinite endpoint')
            for r in test:
                condition_values = [float(t[target]) for t in train if t['condition'] == r['condition']]
                if not condition_values:
                    raise ValueError('Unseen condition')
                record = dict(target=target, participant_id=participant, visit=r['visit'], condition=r['condition'], observed_minutes=float(r[target]), train_mean_minutes=mean(values), train_median_minutes=median(values), condition_mean_minutes=mean(condition_values), condition_median_minutes=median(condition_values))
                records.append(record)
        metrics[target] = {}
        for model in ['train_mean', 'train_median', 'condition_mean', 'condition_median']:
            errors = [float(r[model + '_minutes']) - r['observed_minutes'] for r in records]
            participant_mae = [mean(abs(float(r[model + '_minutes']) - r['observed_minutes']) for r in records if r['participant_id'] == p) for p in participants]
            metrics[target][model] = {'mae_minutes': mean(map(abs, errors)), 'rmse_minutes': math.sqrt(mean(e*e for e in errors)), 'participant_macro_mae_minutes': mean(participant_mae)}
        predictions.extend(records)
    summary = {'source_sha256': hashlib.sha256(raw).hexdigest(), 'python': platform.python_version(), 'input_visits': len(rows), 'included_visits': len(kept), 'participants': len(participants), 'excluded_visits': [{'participant_id': r['participant_id'], 'visit': r['visit'], 'reason': r['phase_alignment_status']} for r in rows if r not in kept], 'validation': 'Leave one participant out; all visits from that participant withheld. No hyperparameter selection.', 'models': 'Training mean/median and training condition mean/median only. No twin or mechanistic model predictions.', 'metrics': metrics, 'limitations': ['Small repeated-measures terrestrial laboratory cohort, not astronaut validation.', 'Condition predictors cannot separate spectral effects from visit/order or protocol effects; background always visit 1.', 'Photopic stimulus settings are not melanopic daily light exposure.', 'Sleep endpoint is latency to 10 minutes of continuous sleep.', 'No outliers removed; zero latency retained.', 'All four nonmatched visits excluded for both endpoints to keep one common comparison cohort.', 'Leave-one-participant-out errors assess new participants in this study, not new studies or personal longitudinal forecasting.']}
    output.mkdir(parents=True, exist_ok=True)
    with (output/'predictions.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(predictions[0])); writer.writeheader(); writer.writerows(predictions)
    (output/'results.json').write_text(json.dumps(summary, indent=2)+'\n')
    return summary

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--input', type=Path, default=Path('analysis/blume_experiment/matched_endpoints.csv')); p.add_argument('--output', type=Path, default=Path('analysis/blume_benchmark'))
    args = p.parse_args(); print(json.dumps(run(args.input, args.output), indent=2))
