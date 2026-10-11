# Matched observations from the original Blume experiment

Blume et al. (2024): https://doi.org/10.1038/s41562-023-01791-7.
Data: https://doi.org/10.6084/m9.figshare.23578698 (CC BY 4.0).
Laboratory log: https://doi.org/10.6084/m9.figshare.23578695 (CC BY 4.0).
Author analysis code: https://github.com/ChristineBlume/Effects-of-calibrated-blue-yellow-changes-in-light-on-the-human-circadian-clock, revision e9bc03f89244b7b00e1cd9ec63b3091b09d75018.

## Completed, verified work

- Original public archive downloaded and pinned by file ID and SHA256.
- 1,584 original melatonin measurements from 16 participants and 48 visits inspected.
- All 96 Blume profiles already imported from the dlmoR study match the original measurements, value for value: first profiles use samples 1–14; second profiles use samples 20–33.
- Original endpoint tables contain 46 phase-shift records and 48 sleep-latency records.
- Exactly 44 records align on participant, visit, and condition across both endpoint tables. The join is one-to-one and missing/conflicting records stay explicit.

The 96 profiles are the same observations already in the 120-profile dlmoR inventory. This archive enriches their provenance and outcomes; it is not another independent cohort.

## Endpoint definitions

The author's R analysis dictionary defines phase shift as evening-2 minus evening-1 DLMO in minutes: positive is delay and negative is advance. These values are observed-study derived endpoints, not newly fitted SpaceSleepTwin estimates.

The sleep endpoint is latency to **10 minutes of continuous sleep**, in minutes. It must not be relabeled as generic diary sleep onset latency in analysis/empirical.py.

The reported photopic stimulus settings and exposure timing are protocol metadata, not daily mean personal exposure or melanopic EDI. The source study matched melanopsin excitation across its conditions. It did not find conclusive evidence of differences between the three conditions; do not describe its results as proof that a particular light colour improves sleep.

## Unresolved source discrepancy

For anonymized participant 4, the phase/melatonin tables label visit 2 yellow and visit 3 blue, while the sleep table labels visit 2 blue and visit 3 yellow. Both sleep visits remain flagged as visit_condition_conflict and receive no matched phase value. The two other unmatched sleep visits lack a phase endpoint in the source table. No visit or condition has been corrected by assumption.

Consult original logs and study documentation before resolving this discrepancy. Do not join only on participant, ignore visits, or automatically swap labels.

## Reproduce

From the project root, after importing the dlmoR profiles:

```sh
python3 analysis/import_blume_experiment.py
```

Outputs:
- matched_endpoints.csv: all 48 sleep visits, including 44 phase matches, two missing phase endpoints, and two conflicts.
- profile_provenance.csv: 96 verified melatonin profile mappings.
- import_audit.json: source hashes, counts, and limits.

Next: resolve timestamp provenance and protocol histories, then evaluate circadian predictions against phase shifts using held-out participants. These tables have not calibrated or validated the simulator.
