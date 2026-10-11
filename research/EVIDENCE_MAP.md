# Evidence map for SpaceSleepTwin — 11 October 2026

This map records external evidence and planned uses. It does not report new SpaceSleepTwin findings.

| Source | Design/data | Contribution | Access and limitation |
|---|---|---|---|
| Rahman et al. 2022, DOI 10.1111/jpi.12826; https://pubmed.ncbi.nlm.nih.gov/35996978/ | 16 participants in four-person HERA crews; 45-day ground analog; dynamic versus static lighting | Direct operational precedent for comparing circadian alignment under lighting schedules | Individual datasets available by request through NASA LSDA; not downloaded. Ground analog is not spaceflight. |
| Thalji & Spitschan 2026, DOI 10.1177/07487304251389994; https://github.com/tscnlab/ThaljiEtAl_JBiolRhythms_2026 | DLMO estimator benchmark using 112 melatonin time series from two source studies | Verify phase-marker extraction and uncertainty; useful R reproducibility example | Repository documents CC BY 4.0 for data/figures and MIT for code. 112 series are not necessarily 112 independent people. Paired light histories must be checked before using for mechanistic model validation. |
| Brown et al. 2022, DOI 10.1371/journal.pbio.3001571 | Expert consensus informed by human studies | Context for melanopic EDI units and daytime/evening/nighttime exposure windows | Not a participant dataset, individual prescription, or astronaut-specific validated protocol. |
| Verhoef et al. 2026 SUNSHINE, DOI 10.1038/s44323-026-00098-w | Two-week monitoring of parents with young infants: light sensors, actigraphy and diaries | Stress-test generalizability to fragmented sleep and caregiving-related light exposure | Individual data not public; academic/noncommercial access on reasonable request. Do not pool with healthy adult cohorts without accounting for caregiving. |
| Akgun et al. 2026, DOI 10.1038/s44323-026-00087-z | Manchester light + wearable sleep, 89 participants | Initial observational data audit already performed | Mapping and coverage recorded in REAL_DATA_SOURCES.md. |
| MeLiDos, https://github.com/MeLiDosProject/melidosData | Multisite wearable-light and diary data | Independent-site evaluation and sensor-position comparison | Preserve site, device, timezone, wear coverage and release identity. UCR partial import audited. |

## Finding that constrains our claims
HERA 2022 found better circadian alignment with dynamic lighting but no difference in self-reported sleep duration or latency between conditions. Therefore, improvements in simulated phase alignment must not be presented as demonstrated improvements in sleep quantity.

Urinary aMT6s acrophase (HERA) and salivary DLMO (dlmoR source studies) are different biomarkers. They require explicit observation models and must not be substituted or combined as the same outcome.

## Research questions
1. Can a reproducible light-history model estimate a measured circadian marker more accurately than a fixed-phase baseline, in held-out participants?
2. Do light exposure timing and regularity add predictive value for sleep timing or duration beyond chronotype and calendar covariates, in held-out participants and a separately held-out site?
3. Under identical operational constraints, do prespecified dynamic schedules reduce predicted phase misalignment versus static schedules across a justified parameter range?

Questions 1 and 2 require compatible real observations. Question 3 remains a simulation experiment until externally validated.

## Analysis safeguards
- Keep sleep latency, sleep duration, sleep onset clock time, DLMO and aMT6s acrophase distinct.
- Use full time-series exposures where possible; threshold totals alone omit timing.
- Account for reverse direction: sleep and behavior can change light exposure.
- Split by person; use an independent site for external assessment only after harmonization.
- Report baseline comparisons, circular timing error where appropriate, uncertainty and null findings.
- Do not convert photopic lux to melanopic EDI without spectral/device information.
- Do not equate repeated nights, series, sites or releases with independent participants.
- Do not describe fitted terrestrial results as astronaut validation.
