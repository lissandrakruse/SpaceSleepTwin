# Absolute phase and alignment: known-aggregate test

Target: aMT6s acrophase 02:45–05:39, centered at 04:12, as defined in the
[HERA article](https://doi.org/10.1111/jpi.12826). This is a study criterion,
not a universal clinical prescription or an optimum for every sleep schedule.

## Calibration and evaluation are separate

Under the assumed 21-day premission light/sleep routine, compute the oscillator
x-minimum phase over its last seven days. Fit an additive circular offset using
only the published premission group means: SLS 4.24 h and DLS 3.69 h.
Mission means 6.22 h and 4.76 h are used only for assessment, never fitting.
Tau remains 24.2 h; light inputs and windows remain fixed.

| Group | Premission anchor (h) | Predicted mission mean (h) | Published mean (h) | Circular error (h) | Mean inside target? |
| --- | ---: | ---: | ---: | ---: | --- |
| SLS | 4.24 | 5.7952 | 6.22 | 0.4248 | Model no / observed no |
| DLS | 3.69 | 3.9161 | 4.76 | 0.8439 | Model yes / observed yes |

The group-anchored method reproduces mean in/out classification but errors
are approximately 25 and 51 minutes. It does not reproduce absolute phase
with the apparent accuracy suggested by the earlier contrast-only comparison.
Predicted daily fractions inside the window are 44.4%/100.0%; these are
model days, not observed participant-day fractions and not a reproduction of
the publication's alignment percentages.

Separate offsets absorb the baseline group difference; they do not identify
a universal biomarker mapping. A shared-offset alternative using pooled
premission mean 3.965 h predicts SLS 5.5202 h and DLS 4.1911 h: both means
are inside the target. This alternative fails the observed mean SLS category.
Report both rather than selecting the favorable calibration method.

The mapping is an assumed constant offset between x minimum and urinary
acrophase; its physiological validity and constancy across conditions remain
untested. Actual premission exposure and individual marker records are absent.
Both published premission and mission aggregates were already known: this is
not independent validation or preregistration.

## Alignment metrics

The notebook calculates mean absolute circular distance to the target center
and fraction of modeled daily minima inside the target interval. Distances
penalize both advances and delays away from the center. Circular membership
also works for target intervals crossing midnight. An alternative target can
be supplied to the functions, but must be defined independently before
comparing schedules; it cannot be optimized against mission outcomes.

## Uncertainty: implemented sensitivity, not individualized calibration

Use matched synthetic draws for the same hypothetical subject across SLS/DLS:

- Tau: Normal(24.2 h, 0.15 h), rejection-truncated to [23.8,24.6] h.
- Initial phase perturbation: Normal(0,0.25 h), rejection-truncated to ±1 h,
  implemented as an oscillator-state rotation in nominal-hour coordinates.
- Shared premission anchor: 3.965 h. Both strategies receive the same draw.
- 24 draws, fixed seed 20261011. This small Monte Carlo example is not a
  clinical probability, calibrated posterior, confidence interval or guarantee.

All 24 draws favored DLS by mean distance to center under these assumptions.
That is a conditional model result, not certainty about a person or astronaut.
Mean simulated daily fractions were SLS 79.2%, DLS 100%; they use a different
starting anchor than the primary separate-group calculation.
Do not mix the two sets of fractions or compare them to observed group percentages.

Aggregate means cannot jointly identify tau, phase/state, biomarker offset,
measurement error and their covariance. Individual premission observations
and measured exposure are needed to fit those distributions. The functions
accept anchors and phase perturbations but do not infer an individual's posterior.
Model-structure, spectral and exposure-reconstruction uncertainty are not
covered by this assumed-prior Monte Carlo exercise.

## Reproduce

Execute alignment_hera.py or the appended cell of
[the benchmark notebook](spacesleeptwin_hera_benchmark.ipynb).
Results are in hera_alignment.json, including explicitly synthetic draws.
Tests check equal early/late penalties, midnight crossing and exact fitting
of the premission anchors without using mission means.

## Research implication

The correct objective is alignment, not maximum advance. This test exposes
calibration dependence and absolute-phase errors. A personalized lighting
decision requires an independently validated marker mapping and individual
calibration; the present prototype does not establish those requirements.


## Expanded numerical sampling: 256 draws

The same assumed distributions, seed and original premission routine were
rerun with 256 draws. DLS was closer in 256/256; conditional
fraction 1.0000, marginal 95% Wilson sampling interval
[0.9852, 1.0000]. This describes finite Monte Carlo uncertainty only.
It is not individual calibration uncertainty or a clinical confidence interval.
SLS/tie counts and their separate marginal intervals are retained in
hera_alignment_256.json. The first 24 draws are consistent with the earlier
example; increasing their number does not validate the assumptions.

The separate [premission profile test](HERA_PREMISSION.md) increases both
modeled group drifts but does not remove the differential mismatch. No
profile was chosen to replace the original Monte Carlo setting.
