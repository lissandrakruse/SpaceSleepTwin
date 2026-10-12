# Hypothetical premission outdoor-light sensitivity

This test was specified after viewing the original known-aggregate benchmark,
before running these profiles. It is not preregistered or independent human
validation. All profiles are retained; none is selected as the participants'
actual exposure or as a new calibrated model.

## Fixed assumptions

Tau 24.2 h; 21 assumed premission days; 150 photopic lux from 07:00 to 23:00;
darkness during sleep. Add 5,000-lux pulses centered at 13:00, lasting 0, 1, 2
or 4 h daily. The pulse intervals are 12:30–13:30, 12:00–14:00 and 11:00–15:00.
These hypothetical profiles are not observed HERA premission records. The
5,000-lux value is a fixed scenario input, not a measurement or lighting recommendation.

Use the same mission schedules and six assessment windows. As before, fit
separate circular marker offsets from the premission means only. Each profile
changes both the incoming oscillator state and the fitted marker offset.
This tests calibration sensitivity, not a uniquely identified outdoor-light mechanism.

## Executed results

Positive changes indicate delay from each group's own published premission mean.

| Assumed intense-light hours/day | Standard delay (h) | Dynamic delay (h) | Difference between changes (h) |
| --- | ---: | ---: | ---: |
| 0 | 1.5552 | 0.2261 | 1.3291 |
| 1 | 1.8183 | 0.4949 | 1.3234 |
| 2 | 1.9905 | 0.6710 | 1.3196 |
| 4 | 2.3037 | 0.9921 | 1.3116 |
| Published descriptive change | 1.98 | 1.07 | 0.91 |

## Interpretation

Increasing assumed premission bright-light duration moves both modeled drifts
in the direction of the observed delays. Two hours nearly matches standard
drift but leaves dynamic drift too small. Four hours nearly matches dynamic
drift but overshoots standard. Both reduce the aggregate phase discrepancy
relative to the original 150-lux routine.

The differential benefit changes very little, remaining 1.31–1.33 h, around
0.40–0.42 h larger than the descriptive observed 0.91 h. The profiles therefore
do not jointly reproduce both group drifts and the difference between them.
A common-delay mechanism alone cannot explain the residual difference in
the groups' modeled-versus-observed changes. This does not identify which
alternative mechanism is responsible.

Do not infer real outdoor exposure by choosing the closest known-target profile.
Two groups' aggregate drifts do not prove a single common missing mechanism;
baseline and mission averages have uncertainty and come from repeated-measure
group analyses, not paired individual change estimates supplied here.

The result strengthens the need to request actual premission light histories
for calibration. It does not validate a personalized twin or causal exposure effect.

## Reproduction

Run premission_profiles.py, or the appended cell in
spacesleeptwin_hera_benchmark.ipynb, after the alignment definitions.
All four profiles and signed group errors are in hera_premission_profiles.json.
No mission mean is used to fit parameters or choose a profile.

The expanded Monte Carlo continues to use the original premission assumption
and identical probability distributions. It does not silently switch to a
profile selected from these results.
