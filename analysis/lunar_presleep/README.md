# Three-hour pre-sleep lunar availability — exploratory forward-date test

Executed 2026-10-11 using the verified UCR diary / NASA-JPL ephemeris join. Source attribution, pinned commit, campus coordinates and timezone evidence: [original lunar join](../lunar_ucr/README.md). These are terrestrial UCR sleep observations and computed NASA astronomical covariates.

## Protocol

For each night, require at least three strictly earlier personal diary nights. Estimate habitual bedtime from the median of their bedtime offsets relative to their assigned evening midnight; this avoids treating 01:00 as earlier than 23:00. Estimate personal outcome reference from the median of strictly earlier sleep observations. Current and future nights cannot contribute to either history calculation. No individual z-score is computed.

Construct a fixed three-hour window ending at that habitual bedtime, using the cached hourly Moon ephemerides. Include geometric elevation and illuminated disk fraction only. The window length and minimum history were fixed before running this particular test; the design remains exploratory because previous analyses of the same cohort were known.

150 eligible nights from 39 people; 117 initial nights lack three earlier observations and are excluded from this task only. Four consecutive blocks of eligible evening dates: first initializes training, remaining three are predicted using strictly earlier dates. Evaluate 115 nights from 30 people. Historical observations from earlier evaluation nights are available for subsequent predictions, representing updated operational history; the model itself is refit at calendar-block boundaries only.

Compare three models on exactly the same nights: personal-history median; historical reference plus calendar residual regression; same regression with lunar covariates. Residual model is StandardScaler + Ridge(alpha=10), fitted on training rows only, with no tuning. Calendar model uses workday, weekday sine/cosine, elapsed days, habitual bedtime and personal outcome median. Lunar model adds illumination-weighted above-horizon availability and mean positive elevation in the three-hour window.

## Held-out errors

| Predictor | Sleep delay MAE (min) | Sleep delay RMSE (min) | Duration MAE (h) | Duration RMSE (h) |
|---|---:|---:|---:|---:|
| Personal history only | 8.57 | 13.77 | 1.3051 | 1.6620 |
| History + calendar | 9.71 | 13.24 | 1.3124 | 1.6276 |
| History + calendar + pre-sleep lunar | 9.14 | 12.90 | 1.3071 | 1.6218 |

Adding lunar covariates modestly reduces error versus the same calendar/history model, but does not outperform personal history alone on MAE. RMSE favors the lunar model in this sample. Do not choose the scoring metric after inspecting which model wins; both are reported.

For lunar-minus-calendar/history paired MAE differences, participant-cluster bootstrap 95% percentile intervals are -1.285 to +0.029 minutes (sleep delay) and -0.0167 to +0.0070 hours (duration). Both span zero. Bootstrap uses 2,000 fixed-prediction participant resamples, seed 20261011. These are conditional descriptive intervals: they do not refit models, account for cross-person calendar dependence, correct repeated exploratory testing, or establish statistical significance.

The 115-night evaluation population differs from the earlier 209-night and 267-night tests. Reductions across these studies cannot be attributed to the new feature. Compare only the matched rows and models in this report.

## Limits and next steps

This measures potential geometric availability, not visible light reaching the eye. It lacks a dusk/daylight gate, clouds, buildings, indoor behavior and individual location. Campus coordinates proxy the study city; elevation is assumed 0 km. Hourly samples do not measure exact rise/set times. No artificial-light interaction is fitted: the imported light logger measures total light, whose artificial component cannot be silently inferred. Only six participants have the previously imported glasses subset.

Each person contributes approximately a week, so this does not establish personal lunar periodicity. No astronaut validation or calibration of the browser simulator is claimed. Longer longitudinal observations and measured personal exposure remain necessary. The sensible next lunar feature improvement is a darkness gate based on local Sun elevation, with evaluation kept on the same nights; independent confirmation is required before adopting lunar inputs into the twin.

## Reproduce and verification

From repository root, with numpy/scikit-learn installed:

```sh
python analysis/evaluate_presleep_lunar.py
```

Source hashes, all exclusions, model settings, paired uncertainty estimates and limitations are in results.json. features.csv contains every eligible history and window; predictions.csv contains all 690 predictions (115 nights × two endpoints × three models). Assertions enforce history dates before target dates and model-training dates before evaluation blocks. Feature checks independently reconstructed the habitual bedtime from prior rows and confirmed identical evaluated keys across models.
