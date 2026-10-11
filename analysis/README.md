# Empirical calibration track (v0.6)

The browser simulation is still a **simplified, unvalidated phase oscillator**. This independent Python module begins an evidence-based observational analysis of light exposure versus sleep latency; it does **not** replace the circadian phase simulator with validated predictions.

## Primary open dataset
Didikoglu, Lucas & Brown (2023), University of Manchester Figshare, 59 adults with 30-second melanopic equivalent daylight illuminance and sleep diaries. CC BY 4.0. Dataset: https://doi.org/10.48420/23786238 ; paper: https://doi.org/10.1073/pnas.2301608120 .

The original data require inspection and participant-day aggregation. **Do not rename columns blindly or assume that the raw files match the model input schema.** Record transformations and exclusions in a reproducible notebook before analysis.

## Input schema
An authorized, de-identified participant-day CSV containing:
- participant_id: stable pseudonymous ID
- date: ISO date
- day_medi_lux: measured average daytime melanopic EDI in lux
- prebed_medi_lux: measured average melanopic EDI over a consistently defined pre-bedtime window
- sleep_latency_min: reported time to fall asleep, in minutes

Example command:
```bash
pip install -r analysis/requirements.txt
python analysis/empirical.py participant_day_data.csv --out results
```

Do not commit restricted or participant-level records to the public repository. Outputs should be checked for disclosure risk.

## Primary preregisterable hypothesis
H1: Greater melanopic EDI during the three hours preceding bedtime is associated with longer sleep onset latency, after adjustment for daytime exposure and prespecified covariates. The baseline Ridge model is **predictive**, not a causal or fully adjusted test of H1.

## Planned inferential model
A mixed-effects regression with participant random intercepts, time-of-day and season adjustment, age, chronotype, and other justified covariates. Split model development and evaluation by participant, then by independent study if possible. Report missingness, calibration, confidence intervals, and sensitivity analyses.

## Next research phases
1. Inspect raw Manchester Figshare files, obtain documented mappings and process the melanopic EDI and sleep diaries.
2. Add an independent open cohort with compatible exposure definitions.
3. Validate sleep latency predictions and only then investigate a separately measured circadian phase outcome.
4. Compare transfer to HERA/ISS only with appropriate, authorized data.

**No real participant dataset has yet been ingested or validated in this repository.**
