# NASA/JPL lunar ephemerides × real UCR sleep diaries

Executed 2026-10-11. Actual join: 267 diary records, 39 participants, 83 evening dates, 2025-06-16 through 2025-09-06. This is a terrestrial Costa Rica dataset with computed NASA astronomical covariates, not astronaut sleep data.

## Sources and timing

Sleep data: Sancho-Salas, von-Breymann, Zauner & Spitschan (2025), MeLiDos UCR, CC BY 4.0, DOI https://doi.org/10.5281/zenodo.17289456. Source repository https://github.com/MeLiDosProject/Sancho-SalasEtAl_Dataset_2025 pinned to ed90d9ac91b9fa81c0869dafbe6efb3c8d9faed3, file data/imported/continuous/sleepdiaries.RData. Exact file SHA-256 in join_audit.json.

Source metadata data/Metadata_Melidos_UCR.xlsx specifies campus coordinates 9.9372 N, 84.0509 W and Costa Rica timezone. These coordinates proxy the study city, not individual overnight residence. Site altitude was not established and is set to 0 km for this preliminary query.

Pyreadr exposes the imported datetimes as naive UTC values. A direct raw-diary check for UCR_S001 confirms 2025-06-16 21:20 local → 2025-06-17 03:20 in the imported file. Convert UTC to America/Costa_Rica before assigning an evening. Bedtimes before local noon are assigned to the preceding evening; later bedtimes use the same date. This rule is explicit and does not establish a universally correct biological-night definition.

NASA/JPL Horizons observer ephemerides: https://ssd-api.jpl.nasa.gov/doc/horizons.html. Moon target 301, geodetic observer at campus proxy. Quantities 4,10,24: azimuth/elevation, illuminated disk percent, observer phase angle. UTC hourly ephemerides are converted to local time. Features use disk illumination at 18:00 and the count of positive geometric elevations at six hourly samples, 18:00–23:00. The count is not exact visible hours, and this fixed civil-time window is not the paper's first six hours after astronomical dusk. Disk illumination is not personal lux. Clouds, buildings, windows and indoor exposure are unknown.

Raw API response, query settings, SHA-256 and returned API signature are saved. The API actually returned signature version 1.2, while the currently displayed API documentation lists 1.3; the returned signature is retained without replacing it.

## Same-fold exploratory prediction comparison

Fixed StandardScaler + Ridge(alpha=10), with standardization fitted only on training rows. Baseline predictors: reported workday, weekday sine/cosine and elapsed calendar days. Added predictors: illuminated disk percent and above-horizon sample count. No hyperparameter tuning, clipping or outlier removal.

Participant holdout excludes all records from each test person, but may share dates between training and test. A second evaluation uses four consecutive blocks of unique evening dates: the first initializes training, and each of the other three is predicted using strictly earlier dates only. These later-date tests contain 209 records and may include previously observed participants. Neither evaluation is external validation.

| Evaluation | Outcome | MAE without lunar | MAE with lunar |
|---|---|---:|---:|
| Participant holdout, 267 records | Diary sleep delay (minutes) | 10.99 | 11.32 |
| Participant holdout, 267 records | Diary sleep duration (hours) | 1.0066 | 1.0064 |
| Later calendar dates, 209 records | Diary sleep delay (minutes) | 15.40 | 15.51 |
| Later calendar dates, 209 records | Diary sleep duration (hours) | 1.0598 | 1.0691 |

**No consistent predictive improvement.** The tiny duration difference in participant holdout does not persist in later dates. No confidence interval, significance or causal effect is claimed. Do not promote lunar covariates into the simulator as an established improvement.

Diary sleep delay differs from Blume's latency to ten minutes of continuous sleep. These errors cannot be compared directly with the Blume results. The six-person light-glasses subset has not been merged, so this test does not control measured personal light exposure. Month, recruitment timing and person characteristics can be associated with lunar covariates. Each person contributed about one week, which is insufficient to estimate a personal lunar cycle reliably.

## Reproduce

From repository root, with Python, pyreadr, numpy and scikit-learn installed:

```sh
python analysis/cross_lunar_ucr.py --input /path/to/sleepdiaries.RData
python analysis/evaluate_lunar_ucr.py
```

The cached raw Horizons response is used if present. Delete only that cache to request fresh ephemerides. Inspect the pinned source and audit before using a different source file or date range. Current join integrity checks passed: 267 unique participant/evening keys, 39 participants, physically valid lunar ranges, and the source-verified local date conversion. Model assertions enforce participant separation and strictly forward calendar splits.

Research motivation: Casiraghi et al. (2021), https://doi.org/10.1126/sciadv.abe0465. This analysis is not a reproduction of that study and uses a different evening window. Next improvements require actual individual light exposure and better dusk-aligned lunar availability, followed by an independent cohort. The existing SpaceSleepTwin browser model remains uncalibrated.
