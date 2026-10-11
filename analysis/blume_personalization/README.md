# Exploratory prior-visit personalization — no improvement

Executed 2026-10-11. Using the verified Blume2024 matched import, test whether a person's earlier measured outcome improves prediction of their later laboratory visit.

28 eligible later visits from 15 people have at least one strictly earlier matched visit. The other 16 matched visits are first available observations and are ineligible for this task; they have not been deleted from the original 44-visit benchmark. All source conflicts and missing phase endpoints remain excluded. No unusual sleep observation is removed.

## Validation

Outer leave-one-participant-out validation excludes the evaluated person from population training and weight selection. That person's strictly earlier measured outcomes are allowed as history, because the task is prediction of a subsequent visit for a known person. There is no use of the current or future outcome as a feature.

The predictor combines the training population median with the person's median of previous visits. Candidate history weights are 0, 0.1, 0.25, 0.5, 0.75, 1. Inner participant folds select the weight by participant-macro MAE; ties favor smaller weights. The inner procedure repeats population fitting and constructs history from earlier visits only. No outer outcome selects the weight. This analysis is exploratory because the cohort was already inspected before the method was designed.

## Actual errors on the same eligible visits

| Predictor | Phase MAE (min) | Phase RMSE (min) | Sleep MAE (min) | Sleep RMSE (min) |
|---|---:|---:|---:|---:|
| Population median | 31.45 | 38.11 | 4.59 | 10.09 |
| Prior personal history only | 41.11 | 56.57 | 9.76 | 32.21 |
| Weight selected in inner folds | 33.99 | 41.37 | 9.94 | 32.33 |

Personal history did not improve either outcome. Retain the population reference for this comparison. Small cohort size and unusual earlier observations can make personalization unstable; these results do not prove that personalization generally fails.

The 4.59-minute sleep MAE is **not** an improvement over the previous 7.65-minute result: the earlier benchmark included all 44 matched visits, while this task uses 28 later visits. In particular, the observed 174.5-minute first-visit latency is used as personal history rather than evaluated as a later-visit target. It remains in the source and can worsen subsequent predictions. Comparisons across these two target populations would be misleading.

This experiment does not calibrate the browser simulator or validate a mechanistic twin. No causal lighting claim, astronaut performance, or daily-life forecasting is established. An independent, temporally aligned wearable-light and sleep dataset remains necessary to assess such models.

## Reproduce and audit

From repository root:

```sh
python analysis/personalize_blume.py
```

Python standard library only. `predictions.csv` contains observed outcomes, history, population references, selected weights, and personalized predictions. `results.json` records input SHA-256, metrics, and limitations. A mutation check confirmed that changing a held-out participant's final visit outcome does not change their prior-visit features, selected weights, or predictions for any of their visits.

Source: [verified import and CC BY 4.0 attribution](../blume_experiment/README.md). [Original 44-visit benchmark](../blume_benchmark/README.md) remains unchanged.
