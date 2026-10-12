# Proposed H4 addendum for a NASA LSDA research-data request

Status: ready-to-incorporate draft; not sent, registered or approved. The full
previous request and its three original hypotheses were not located, so H4 is
a proposed label to reconcile with the complete document. Do not replace the
prior hypotheses or imply that this addendum has already been incorporated.

## Proposed hypothesis

**H4 — Outcome-specific predictive value of late-wake light exposure.**
Conditional on the availability of synchronized individual exposure records,
late-wake light exposure will add more out-of-sample predictive information
for independently measured circadian phase than for same-night self-reported
sleep-onset latency, after accounting for personal history and sleep timing.

This is a prospective hypothesis for secondary analysis, not an established
finding in astronauts. The Earth-cohort result was a negligible incremental
predictive gain for one prebed-light feature in one tested latency model; it
does not prove that evening light never predicts latency. The mechanistic
phase result supplies rationale, not individual empirical confirmation.

## Requested feasibility information and records

Please confirm whether HERA lighting-study records can be linked, under
applicable access and ethics conditions, using pseudonymous participant and
mission identifiers. Specifically, we request availability information for:

- Calibrated, time-stamped personal light exposure, if collected: units,
  spectra or melanopic EDI, sensor position, wearing/nonwear flags and calibration.
- If only habitat measurements exist, time-stamped lighting schedules,
  spatial photometry and participant location/activity records, if available.
  Ambient input reconstruction must be distinguished from personal measurement.
- Original sleep diaries, actual and scheduled bed/wake timing, latency
  definitions and quality flags; relevant caffeine/medication records if authorized.
- Original urinary aMT6s sampling times, concentrations, sample volumes,
  assay methods and phase estimates with uncertainty, plus premission records.
- Collection-day, mission, intervention order, protocol changes and missingness
  metadata sufficient to align exposure windows and outcomes.

The published HERA study characterizes lighting by environment; it does not
by itself establish that a calibrated individual light series exists. If only
group lighting schedules are available, H4's individual-exposure comparison
may not be identifiable; report that limitation rather than substituting
group assignment for measured personal exposure.

## Evaluation plan to finalize before outcome access

1. Specify eligible participants/windows and data coverage requirements.
   Anchor late-wake exposure to the last three hours before the scheduled or
   actual attempt to sleep, with the choice fixed beforehand; do not anchor
   it to a future observed sleep-onset time for prospective latency prediction.
2. Use actual biomarker assessment windows as phase targets. Never treat
   interpolated daily aMT6s values as independently measured daily phase.
   For a phase forecast, fix the prediction origin and use only preceding
   exposure; a candidate is late-wake exposure accumulated over the seven
   days before the collection window. Any concurrent-window analysis is an
   association analysis and must be labeled separately.
3. Define simple endpoint-specific baselines using only prior measured phase
   or prior personal latency and available sleep-timing/history information.
   Add the same prespecified late-wake exposure feature family, without
   optimizing exposure windows against held-out outcomes.
4. Compare incremental predictive gains on held-out participants or missions
   and chronological future windows. Phase uses circular MAE; latency uses
   MAE. Do not compare raw hour and minute errors or p-values across outcomes.
   A candidate common scale is relative error reduction against each
   endpoint's own baseline, with a prespecified treatment of near-zero baseline
   error and an uncertainty interval for the difference in gains.
5. Preserve participant/mission clustering and account for the different
   outcome sampling rates. Restrict model complexity to the actual available
   sample. Lighting condition and mission may be confounded; group-level
   comparisons cannot establish independent individual dose effects.
6. Report null, reversed or unidentifiable results. Determine the final
   estimator and feasibility before a registered evaluation plan is frozen.

No new data have been received. No communication was sent through this addendum.
Spaceflight transfer requires authorized in-flight records and separate evaluation.

## Rationale from model sensitivity

The notebook tests HERA-variable and fixed 23:00–07:00 sleep schedules at
τ=24.2 h, with photopic input and a naive melanopic-EDI substitution. Late-wake
dimming has the larger isolated phase contrast in those four configurations.
The EDI substitution is not a validated spectral model; changing the sleep
schedule also changes sleep opportunity. These simulations motivate H4 but
cannot validate it.

Sources: [published HERA study](https://doi.org/10.1111/jpi.12826),
[NASA LSDA](https://lsda.jsc.nasa.gov/),
[executed benchmark](spacesleeptwin_hera_benchmark.ipynb),
[prospective plan](VALIDATION_PROTOCOL.md).
