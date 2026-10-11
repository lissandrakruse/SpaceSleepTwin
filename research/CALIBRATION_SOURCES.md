# Calibration and validation sources

Reviewed: 2026-10-11.

## Current status

SpaceSleepTwin is a research prototype. Its simulator has not been calibrated or validated against participant-level observations. Import audits in analysis/ establish data availability and structure, not predictive accuracy.

## Verified sources and their roles

### Open melatonin reference data and reproducible R analysis

Thalji & Spitschan (2026), dlmoR:
https://doi.org/10.1177/07487304251389994
https://github.com/tscnlab/ThaljiEtAl_JBiolRhythms_2026

The repository supplies input melatonin time series, analysis scripts, derived summaries, and a versioned R environment via renv.lock. Data and figures are CC BY 4.0; code is MIT. It reuses observations from Blume et al. (2024) and Heinrichs & Spitschan (2025). Full large simulation outputs are separately archived at https://doi.org/10.5281/zenodo.18371010.

Use: reproduce DLMO extraction and quantify sensitivity to sampling, thresholds, and noise. DLMO is the onset of melatonin under dim light, a circadian phase marker.

Limit: melatonin curves alone do not establish that matched continuous light exposure and sleep records are available for end-to-end twin validation. Inspect the original protocols and participant linkage before combining records.

### Independent model implementation

Arcascope circadian documentation:
https://arcascope.github.io/circadian/api/models.html
https://github.com/Arcascope/circadian

Provides Forger99 and other models, configurable parameters and initial conditions, equilibration, and phase-marker extraction. Its Forger99 uses parameter values from Serkh & Forger (2014), rather than automatically reproducing the original 1999 parameterization. Default conversion places DLMO seven hours before the core-body-temperature minimum.

Use: numerical comparison of research/forger99.py against an independent implementation, with pinned versions, identical inputs, parameter sets, initialization, and time units.

Limit: agreement between implementations verifies software behavior; it does not validate predictions in humans. The default phase-marker offset is a model assumption, not an individually measured constant. Do not substitute melanopic EDI for the model's light input without justified adaptation.

### Human validation design using matched wearable and melatonin observations

Cheng et al., Sleep 44(2), zsaa180:
https://doi.org/10.1093/sleep/zsaa180

Study of 45 fixed night-shift workers compared model predictions from wrist actigraphy and photometry against laboratory DLMO. It also compared predictions with average sleep timing as a simpler reference.

Use: a precedent for validating circadian predictions against an observed biological marker and comparing against a practical baseline.

Limit: published results are external evidence, not SpaceSleepTwin performance. Public downloadable participant-level observations and reuse terms have not been confirmed in this review.

Additional candidate:
Light-based methods for predicting circadian phase in delayed sleep–wake phase disorder:
https://doi.org/10.1038/s41598-021-89924-8
Participant-level access and licensing still need verification before ingestion.

## Proposed evaluation plan (not yet executed)

1. Reproduce DLMO extraction on a licensed open melatonin dataset, retaining units, collection conditions, provenance, and measurement uncertainty.
2. Compare Forger99 implementations under identical light schedules and parameters. Evaluate initialization and equilibration sensitivity.
3. For empirical sleep outcomes, use the audited Manchester/UCR sources after temporal alignment and variable harmonization. Fit on training participants and evaluate on held-out participants against a training-only baseline.
4. For circadian phase validation, obtain linked light histories and observed DLMO from the same participants. Sleep onset and wearable REM latency must not be relabeled as DLMO.
5. Report circular phase errors in hours (wrapped around the 24-hour clock), median and mean absolute errors, bias, uncertainty, and failure rates. Include held-out participants and, where possible, a separate cohort.
6. Treat transfer to spaceflight as a separate validation problem. Terrestrial performance alone does not establish astronaut performance.

## Related project records

- ../analysis/REAL_DATA_SOURCES.md
- ../analysis/manchester_import_audit.json
- ../analysis/ucr_import_audit.json
- EVIDENCE_MAP.md
- TWIN_SOURCES.md
