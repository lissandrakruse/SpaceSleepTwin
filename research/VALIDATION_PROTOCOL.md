# SpaceSleepTwin: evaluation protocol for future independent data

Status: prospective working protocol written **after** viewing the HERA
aggregate benchmark. It is not a preregistered study and does not convert the
known HERA target into independent validation. Register and freeze a final
protocol before accessing any new evaluation outcomes.

## Scope and proposed contribution

The proposed contribution is a reproducible, auditable integration of a
personal-history latency baseline and a mechanistic circadian component.
This release implements a circadian benchmark, not a completed personalized
digital twin. The study's dynamic-lighting result belongs to its original
authors. Our contribution at this stage is software and a transparent
reconstruction with sensitivity analysis.

Separate two questions:

1. Does a calibrated model predict future phase and difficult nights better
   than appropriate baselines in independent individuals?
2. Do model-guided schedules reduce measured misalignment when applied in
   a controlled comparison?

Question 1 is predictive; question 2 is interventional. A light–sleep
association or a favorable simulation cannot answer question 2.

## Current benchmark interpretation

The current contrast compares model x minima with urinary aMT6s acrophases.
Both conditions use a common assumed starting state. The study's observed
premission group means were different. The published unadjusted mission
contrast and the difference between descriptive pre/post group changes
are distinct quantities. Neither is a reconstruction of individual effects.
Do not select the model version that best matches either known aggregate.

## Before evaluating new records

- Define the eligible population, required records and excluded/missing-data
  rules. Document ethics, consent/access and data licenses.
- Record synchronized light exposure, unit and measurement plane; local
  time/time zone; sleep opportunities; biomarker collection and assay timing;
  medication and operational factors available for adjustment.
- Freeze the phase-marker mapping using an independent calibration source.
  Do not infer aMT6s clock time from x minima without supporting validation.
- Freeze tau, initial-phase estimation, calibration-night requirements and
  model selection using development data only. Never use future observations
  or held-out outcomes to choose these settings.
- Define the number of calibration nights using an evaluation that compares
  the same eligible individuals across candidate lengths.
- Keep evaluation participants or missions independent of model training
  and parameter selection. Within-person forecasts must be chronological.

## Endpoints and comparators

| Component | Endpoint | Comparator | Evaluation |
| --- | --- | --- | --- |
| Circadian phase | Circular phase error, in hours, against a matched validated biomarker | Last measured phase / frozen simple entrainment baseline | Participant-level errors, signed bias, dispersion and drift |
| Sleep latency | Next-night sleep-onset latency | Personal median using only prior calibration nights | MAE as primary, RMSE as secondary; errors aggregated by person |
| Difficult nights | Probability of latency greater than 30 min | Prior-person or development prevalence | Brier score, calibration and precision–recall; freeze threshold |
| Combined model | The same endpoint as its separate comparator | History only, circadian only, fixed hybrid | Prespecified ablation comparisons on the same held-out observations |

Use repeated-measure methods or resampling at the participant/mission level;
individual nights are not independent replication. Report uncertainty based
on observed records. Current sensitivity ranges are not uncertainty intervals.
Determine sample size/power before recruitment or data release, using the
intended clustering and outcome, rather than choosing an unsupported count.

## Failure and decision rules

Retain the personal-history baseline if the hybrid does not improve the
prespecified primary predictive metric with credible uncertainty and
acceptable calibration. Publish negative or inconsistent results.
Model-generated scenarios must stay labeled exploratory when personal
light exposures or biomarker mapping are unavailable.

Improvement thresholds and acceptable circular error must be justified and
frozen before the future evaluation; this document does not invent them from
the favorable known aggregate comparison. A direction match alone is not
validation. Evaluate known schedules with identical inputs before proposing
model-guided intervention schedules.

## Intervention and space transfer

Start with a controlled terrestrial analog comparison, with random allocation
or an explicitly justified alternative, appropriate analysis of carryover and
mission effects, and objective phase outcomes. Evaluate a model-guided schedule
against a defined standard schedule. Do not intentionally use chronic sleep
restriction as a sleep-improvement strategy.

Transfer to space requires preflight calibration plus individual in-flight
measurements and independent evaluation. HERA does not reproduce all flight
conditions. Obtain authorized records (e.g. through LSDA) before making claims
about individual astronauts.

## Reproducibility record

Retain source commit, dependencies, input provenance, access restrictions,
frozen configuration, full predictions and participant-level metrics under
appropriate privacy controls. Public releases should contain code, aggregate
results and authorized data only. The executed HERA notebook has no individual
participant records. Record deviations from this protocol explicitly.


## Source artifacts for existing evidence

[Public cohort-analysis notebook](artigo_spacesleeptwin.ipynb): selected aggregate
outputs only, with participant-level outputs removed. See
[the number-to-source map](EMPIRICAL_FINDINGS.md#number-to-source-map).
The known [HERA benchmark and decomposition](spacesleeptwin_hera_benchmark.ipynb)
remain exploratory development evidence, not future independent evaluation.


## Proposed outcome-specific hypothesis

[H4 addendum](LSDA_H4_ADDENDUM.md) compares incremental prediction gains for
measured phase and latency, conditional on exposure availability. It is a draft
addition to reconcile with the full LSDA request, not a submitted request.
