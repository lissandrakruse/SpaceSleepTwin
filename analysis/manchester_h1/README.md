# Manchester H1 — first retrospective measured-light benchmark

Executed 2026-10-11 after publishing [the dated plan](PLAN_2026-10-11.md), commit 42663ae65f43cd4f9e3dab19c736505210bc709b. Tables had already been inspected for schema and source-quality issues before that record. This is not an independent-cohort preregistration or causal confirmation of H1.

## Source and eligible data

Source https://github.com/altugdidikoglu/light-sleep-inreallife pinned ef570332cd6bd04cafea40a66f5a70e6f2206505. Input SHA-256 matches [existing import audit](../manchester_import_audit.json). Source Rmd defines presleep3hr by zero-inflated log → mean → inverse transform of measured MEDI during three hours ending at observed Fitbit startTime. TAT250 is minutes above 250 melanopic lux. log1p(presleep3hr) here is an additional specified feature transform, not an assertion that the source value is arithmetic mean lux.

528 diary rows, 542 light rows; exact one-to-one Id/yday4 join: 440 nights from 88 people. All joined exposure values are finite/nonnegative. 197 joined nights lack three previous personal diary observations; 243 eligible nights from 77 people remain. Personal history uses earlier valid diary nights even if they lack matched light. Four chronological blocks initialize training then evaluate three future blocks: 185 test nights from 62 people, with identical evaluation keys for every model. The first training block has 58 nights from 16 people; subsequent training sets expand. Dates use UTC-to-Europe/London conversion and a 04:00 boundary.

Published target hoursToSleep is converted to minutes. It is not reconstructed from datetimeSleep. Source-quality check: 165/528 records disagree with sleepTime-gobedTime. Some datetimeSleep differences appear in seconds despite a minutes-valued latency, while others conflict more broadly. No silent repair is made. Clarification of preprocessing/definitions is necessary before biological interpretation.

## Actual held-out metrics

| Model | MAE (min) | RMSE (min) | Median absolute error (min) | Participant-macro MAE (min) |
|---|---:|---:|---:|---:|
| Personal-history median | 9.6514 | 17.9949 | 5.00 | 9.8454 |
| History + training residual median | 9.6514 | 17.9949 | 5.00 | 9.8454 |
| History + pre-sleep light | 9.6514 | 17.9949 | 5.00 | 9.8454 |
| History + daytime exposure | 9.6514 | 17.9949 | 5.00 | 9.8454 |
| History + both exposures (primary) | 9.6514 | 17.9949 | 5.00 | 9.8454 |
| Both exposures, log-outcome sensitivity | 9.6650 | 18.0363 | 5.00 | 9.8517 |

All standardized light coefficients and residual intercepts are zero in all folds under fixed QuantileRegressor(quantile=0.5,alpha=0.05). Models therefore collapse to the history reference. Training residual medians are also zero. Log sensitivity differs slightly because median-of-log and log-of-median differ for even historical sample sizes, followed by inverse transformation; it is not a learned light effect.

The joint-minus-history fixed-prediction bootstrap interval is [0,0] because predictions are identical. This is a degenerate model-comparison result, not evidence of zero biological uncertainty or equivalence of light exposure. It cannot give a meaningful biological minimum detectable effect. No hyperparameters were changed after seeing this result.

95.45% of reported diary-minute values are multiples of five; 57.58% multiples of ten; 37.88% multiples of fifteen. These overlapping descriptive frequencies do not prove a formal recording resolution or a minimum achievable error. Zero and unusual reported latencies are retained; no negative predictions occur.

## Interpretation and limits

No added predictive gain from the measured-light features under this fixed median residual model. Do not compare 9.65 minutes here with the UCR 8.57-minute reference as if they were the same cohort, task or measurement. H1 as a biological/causal hypothesis remains unconfirmed.

The pre-sleep window is defined using already observed Fitbit sleep onset. Consequently this is retrospective exposure-conditioned prediction with future-date evaluation, not an operational pre-bedtime forecast. Full-day TAT250 availability before bedtime is also not established. Raw timed light reconstruction with a previously known window endpoint is required for prospective deployment.

Bootstrap: 2,000 paired participant resamples of fixed prediction errors, seed 20261011; no model refitting or cross-person calendar dependence accounted for. Source tables and individual predictions are not redistributed while exact reuse terms for this release remain unresolved. Aggregate results and code are provided. No astronaut validation, DLMO estimation or mechanistic calibration is performed.

## Reproduce

Python dependencies pyreadr, pandas, numpy, scikit-learn; solver uses scipy/HiGHS. From repository root:

```sh
python analysis/test_manchester_h1.py --raw /path/to/source-tables --private-output /path/outside/public-repository
```

The script validates source hashes, join uniqueness, prior-history chronology, minimum training sizes, strictly forward train/test dates and identical test keys. Full aggregate diagnostics, exposure coefficients and source discrepancies are in results.json. No subject-level output is written inside the public repository by default; an explicit private output directory is required.

## Further work

First resolve diary target inconsistencies and verify exact reuse terms. Any tuning of quantile regularization or alternate model should have a new recorded protocol, nested temporal selection and an independent validation cohort. Forger99 photopic inputs must not simply be relabeled as melanopic EDI: its light response requires a documented reformulation and calibration. The observed zero coefficients cannot determine whether there is sufficient information for that mechanistic calibration.
