# SpaceSleepTwin source-to-model mapping

These sources support development of an exploratory circadian/sleep digital-twin prototype. Inclusion as a source does not imply calibration or validation.

| Source | Role in the twin | Current integration | What it cannot establish |
|---|---|---|---|
| Manchester, Akgun et al. 2026, https://doi.org/10.1038/s44323-026-00087-z | Measured melanopic exposure and sleep outcomes for observational evaluation | Four published tables imported and audited locally; aggregate audit committed | No fitted predictive calibration, circadian biomarker or astronaut validation |
| MeLiDos, https://github.com/MeLiDosProject/melidosData | Independent-site evaluation; sensor position, exposure timing and sleep diaries | Costa Rica diary and eye-level light tables inspected; pairing/harmonization pending | Not all sites imported; different sensor positions are not interchangeable |
| Forger, Jewett & Kronauer 1999, https://doi.org/10.1177/074873099129000867 | Mechanistic circadian model basis | Python engine exists; browser uses a separate simplified oscillator | No validation merely from implementing equations; photopic input is not melanopic EDI |
| Brown et al. 2022, https://doi.org/10.1371/journal.pbio.3001571 | Context for melanopic exposure metrics and time windows | Literature reference for scenario design | Consensus targets are not fitted coefficients or personalized prescriptions |
| Rahman et al. HERA 2022, https://doi.org/10.1111/jpi.12826 | Ground-analog benchmark for dynamic versus static lighting and phase alignment | Published findings included; participant records require LSDA request | Not astronaut validation; better phase alignment did not imply longer sleep or shorter latency |
| Thalji & Spitschan 2026, https://doi.org/10.1177/07487304251389994 ; https://github.com/tscnlab/ThaljiEtAl_JBiolRhythms_2026 | DLMO extraction methods, uncertainty and melatonin-series benchmark | Source located; no SpaceSleepTwin marker calculation performed | Melatonin alone cannot validate response to light without compatible paired exposure |
| SUNSHINE 2026, https://doi.org/10.1038/s44323-026-00098-w | Generalizability and fragmented-sleep context | Literature source only; data require academic/noncommercial request | Not a downloaded open cohort or a controlled lighting intervention |

## Observation and simulation contract
Each future result must declare source DOI/URL, exact version/checksum, participant/study identifier, outcome definition, units, timezone, sensor position, missingness and whether it is measured or simulated.

Measured sleep timing, sleep duration, sleep latency, salivary DLMO and urinary aMT6s acrophase are different outcomes. Forger clock states are model states, not observed sleep or hormone measurements.

Current source support advances the prototype's evidence base. Calling it a calibrated personal digital twin requires individual parameter estimation, held-out evaluation and observed-versus-predicted comparisons. Spaceflight transfer requires appropriate mission data.

Related records: [evidence map](EVIDENCE_MAP.md), [real-data inventory](../analysis/REAL_DATA_SOURCES.md), [Manchester import audit](../analysis/manchester_import_audit.json), [Costa Rica import audit](../analysis/ucr_import_audit.json).
