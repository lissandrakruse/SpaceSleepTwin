# Final aggregate sensitivities and interpretation freeze

These two fixed tests were specified after seeing the known HERA aggregates, before their execution. They are exploratory, not preregistered validation. No exposure or physiological setting is selected by agreement with the target.

## Published uncertainty

The descriptive difference of changes is (6.22−4.24)−(4.76−3.69)=0.91 h. Published mean SEs are respectively 0.34, 0.33, 0.53 and 0.42 h. Assuming all four estimates independent gives sqrt(sum(SE²))=0.8257 h. This is an approximate **standard error**, not a confidence interval. The model's 1.3291 h is compatible under that approximation; the central-value difference alone does not demonstrate overestimation or validate the model.

Covariance is unavailable. Assuming independent groups and the same illustrative within-group pre/mission correlation, SE is 0.8257 h at rho=0, 0.5891 at 0.5, 0.3823 at 0.8 and 0.1105 at 1. These are assumptions, not estimated correlations or a covariance-aware statistical test. We cannot assert compatibility for the unknown actual covariance. Differences of reported aggregate means are not supplied paired participant change estimates.

## Same 256 assumed-prior draws

Mean standard-minus-dynamic phase contrast: **1.3124 h**; between-draw SD 0.0927 h; finite-sampling MC SE 0.0058 h; assumed-prior 5/50/95 percentiles 1.1590/1.3332/1.4175 h. The same seed 20261011, truncated Normal tau and initial perturbation, common starting anchor and original 150-lux routine are retained. Contrast is the mean of circular phase differences over the same six assessment windows; the shared marker offset cancels. No participant posterior is inferred. Nonlinearity alone does not guarantee a smaller population mean; its sign depends on the curvature and chosen distribution.

## Fixed late-light sensitivity

All scenarios use tau=24.2 h, standard 122 lux, dynamic daytime 264 lux, original premission routine and unchanged HERA sleep schedule. Only dynamic light in the final three waking hours changes. Lux is photopic; scenarios are not measured personal exposure.

| Dynamic final-three-hour lux | Standard-minus-dynamic phase contrast (h) |
| ---: | ---: |
| 13 | 1.3291 |
| 30 | 1.1213 |
| 60 | 0.8731 |
| 100 | 0.6393 |

This quantifies exposure sensitivity. The 60-lux result approaching 0.91 h is not evidence that participants experienced 60 lux, and is not a new fitted benchmark. All results are retained.

## Freeze and next evidence

Aggregate-based calibration is closed at this revision. No further tuning to these known means is planned. Individual accuracy requires authorized LSDA records: calibrated personal light and premission histories, sleep diaries, timed aMT6s samples and uncertainty, participant linkage and assessment metadata. The full request remains an unsubmitted draft; H4 has been incorporated by the researcher. Archive the analysis and predefine individual-data validation before accessing those records.

Reproduce with alignment_hera.py / monte_carlo_256.py and final_aggregate_tests.py, or the executed notebook. Outputs: hera_alignment_256.json and hera_final_aggregate_tests.json. The nightly lux scenarios are fixed, not crossed with a newly fitted tau distribution.
