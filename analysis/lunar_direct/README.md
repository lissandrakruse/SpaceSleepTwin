# Direct history + lunar ablation

Executed 2026-10-11 on exactly the same 115 future nights from 30 participants as [the pre-sleep test](../lunar_presleep/README.md). No calendar predictors are used in the new lunar model.

Three comparisons: (1) strictly prior personal median; (2) same median plus mean training residual, an intercept-only bias correction; (3) same median plus residual Ridge(alpha=10) using illumination-weighted geometric lunar availability and mean positive elevation in the historical-bedtime three-hour window. StandardScaler is fitted on training rows only. The bias-correction comparator distinguishes lunar-feature value from the intercept adjustment that regression also adds.

All models use the same four chronological blocks, with the first for initial training and the remaining three for evaluation using strictly earlier training dates. Personal histories update using available earlier nights only. Model assertions verified exact equality of all evaluated participant/date keys with the preceding test: 115 per endpoint/model, 690 predictions total. No tuning, calendar covariates, clipping or removal of unusual observations.

| Model | Delay MAE (min) | Delay RMSE (min) | Duration MAE (h) | Duration RMSE (h) |
|---|---:|---:|---:|---:|
| Personal history only | 8.57 | 13.77 | 1.3051 | 1.6620 |
| History + bias correction | 8.86 | 13.91 | 1.2934 | 1.6364 |
| History + lunar residual regression | 8.91 | 13.93 | 1.2960 | 1.6383 |

**No added lunar benefit over the bias-corrected comparator on either MAE or RMSE.** The small duration improvement relative to uncorrected history is also achieved, slightly more strongly, without lunar features. Do not attribute it to lunar light.

Paired MAE differences for lunar minus bias correction: +0.0411 minutes (95% conditional participant-bootstrap interval -0.1120 to +0.1983) and +0.00258 hours (-0.00714 to +0.01155). Lunar minus uncorrected history: +0.3356 minutes (+0.2166 to +0.4561) and -0.00910 hours (-0.05228 to +0.03179). Bootstrap uses 2,000 participant resamples of fixed paired predictions, seed 20261011. It does not refit models, model calendar dependence across people, account for sequential exploratory analyses, or constitute confirmatory inference. A causal claim would not follow even from an interval excluding zero.

Calendar degradation alone cannot diagnose overfitting or insufficient observations per parameter: that diagnosis needs training behavior, model sensitivity and dependence-aware uncertainty. Adding a lunar feature does not itself regularize regression; the ridge penalty does. Predictive error does not establish how much variance is biologically explained by routine.

Source attribution and pinned NASA/UCR provenance: [original join](../lunar_ucr/README.md). The source is CC BY 4.0 UCR terrestrial sleep diaries, with NASA/JPL computed ephemerides. No lunar/cloud/indoor exposure interaction, causal effect, astronaut validation or simulator calibration is established. Features still lack a daylight gate, cloud cover and individual location. Longer histories and independent validation remain necessary. Cloud fraction cannot simply be converted into measured lunar light attenuation without a justified radiative model and indoor-exposure information.

Reproduce from repository root, with numpy and scikit-learn installed:

```sh
python analysis/evaluate_history_lunar.py
```

Input: analysis/lunar_presleep/features.csv. Source SHA-256, full metrics and conditional intervals in results.json; all predictions in predictions.csv. Earlier benchmarks remain unchanged.
