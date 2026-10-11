# First real-data prediction benchmark

Executed 2026-10-11 using the verified Blume2024 paired-endpoint import. This is a descriptive baseline experiment, not a calibrated SpaceSleepTwin or a reproduction of the article's inferential analysis.

## Data and split

44 safely matched visits from 16 participants; four visits excluded (two missing phase endpoints and two unresolved participant-4 condition conflicts). All visits of one participant are held out together in each of 16 folds. Predictions use only the other participants. No tuning, feature selection, removal of unusual values, or train/test overlap. The 96 melatonin profiles are from the same cohort, not additional participants.

Each endpoint has four prespecified predictors: training mean, training median, training mean for the visit's condition, and training median for the condition. The observed phase endpoint is evening-2 minus evening-1 DLMO in minutes. The sleep endpoint is latency to 10 minutes of continuous sleep, not generic sleep onset latency.

## Actual held-out errors

| Predictor | Phase MAE (min) | Phase RMSE (min) | Sleep MAE (min) | Sleep RMSE (min) |
|---|---:|---:|---:|---:|
| Training mean | 31.73 | 40.97 | 11.01 | 27.15 |
| Training median | 31.08 | 40.35 | 7.65 | 26.85 |
| Condition mean | 32.73 | 42.23 | 11.66 | 27.59 |
| Condition median | 32.98 | 41.74 | 7.67 | 26.88 |

MAE averages absolute errors over visits; RMSE is more sensitive to large errors. Participant-macro MAE, which gives each person equal weight despite differing visit counts, is also recorded in results.json. These are descriptive point estimates, without confidence intervals or significance claims. They do not establish equivalence between conditions.

Condition-specific baselines did not improve either MAE or RMSE compared with their corresponding pooled baseline. The observed sleep latency of 174.5 minutes is retained and contributes to the high RMSE. Its removal would require a justified source-quality decision, not a desire to improve scores.

## What this changes for the twin

There is now an auditable real-data benchmark with per-visit held-out predictions. Future models must be compared on the same folds and outcomes against these references. This does not validate the existing browser simulator, and no simulator predictions are included here.

Direct mechanistic calibration remains blocked by unresolved mapping of actual biological clock time, full spectral/melanopic stimulus input, and pre-exposure light history. Photopic lux settings cannot be silently treated as melanopic exposure. Background was always visit 1, so condition predictors mix condition with visit/order. This healthy terrestrial laboratory cohort does not establish astronaut performance or individual one-month forecasting.

Next useful data work is to resolve participant-4 labels against the original laboratory log, reconstruct actual timed light inputs from documented source material, and develop a separately held-out daily-life benchmark using datasets with paired wearable light and sleep diaries. New model selection must use nested participant folds or a new external cohort rather than tuning repeatedly against this benchmark.

## Reproduce

From repository root:

```sh
python analysis/benchmark_blume.py
```

Python standard library only. Input is analysis/blume_experiment/matched_endpoints.csv; its SHA-256 and Python version are saved in results.json. predictions.csv contains all 88 endpoint predictions (44 visits × two endpoints), including each reference prediction.

Source and import provenance: [verified import](../blume_experiment/README.md), [original CC BY 4.0 data](https://doi.org/10.6084/m9.figshare.23578698). Derived data follow the original attribution requirement.
