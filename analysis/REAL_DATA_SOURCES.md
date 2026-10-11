# Real data sources and import status (11 October 2026)

## Completed Manchester audit
Source: https://github.com/altugdidikoglu/light-sleep-inreallife
Article: https://doi.org/10.1038/s44323-026-00087-z
Pinned upstream commit: ef570332cd6bd04cafea40a66f5a70e6f2206505.

Four actual RData tables were downloaded and read with pyreadr. Counts: baseline 89 people; light 542 rows; Fitbit sleep 547 rows; sleep diary 528 rows. One-to-one upstream-key joins produce 454 light/Fitbit records from 88 people and 440 light/diary records from 88 people. These are alignment counts, not final analysis sample sizes.

Reproduce:
```bash
pip install pyreadr pandas
python analysis/import_manchester.py --raw /private/local/manchester --out audit.json
```

Only code and aggregate audit metadata are stored here. Exact GitHub data-release reuse/redistribution terms require confirmation; the related Figshare cognitive-study archive (10.48420/28911977) is CC BY 4.0, but that alone does not establish the license of all added sleep files.

### Mapping decisions
- TAT250 is minutes above 250 melanopic lux. Never map it to day_medi_lux.
- presleep3hr is a geometric-type mean computed using LightLogR zero-inflated transforms, over the three hours preceding observed Fitbit startTime. Do not relabel it as an arithmetic mean or an independently defined bedtime window.
- yday4 is the upstream day key. Verify full dates, year and local Europe/London timezone before constructing new windows.
- REM latency is not sleep-onset latency.
- The generic empirical.py input is therefore not yet populated from these tables.
- No circadian phase, DLMO or astronaut validation has occurred.

## Additional cohorts
| Source | Available measurements | Access/status | Intended role |
|---|---|---|---|
| MeLiDos / melidosData: https://github.com/MeLiDosProject/melidosData | Personal light, sleep diaries, chronotype, wear logs; project reports 191 people across 9 sites and 7 countries, 1480 participant-days | Public site repositories; inspect each license and version | External validation after harmonization |
| Costa Rica UCR: https://github.com/MeLiDosProject/Sancho-SalasEtAl_Dataset_2025 | Eye/chest/wrist light, morning sleep diary and questionnaires; repository describes 39 included people | CC BY 4.0; located, full analysis pending | Latin American validation cohort |
| Tuebingen MPI: https://github.com/MeLiDosProject/GuidolinEtAl_Dataset_2025 | Light, actigraphy and sleep diary; 26 included people | CC BY 4.0; located, not imported | Separate validation; protocol differences documented upstream |
| MESA: https://sleepdata.org/datasets/mesa | Actigraphy light/activity, PSG and covariates | Data-access request/approval required; not obtained | Larger observational comparison; light units need harmonization |
| NASA LSDA/NLSP: https://www.nasa.gov/hrp/nlsp/ | Human mission/analog studies including sleep and light records | Locate exact study and request restricted data; not obtained | Later spaceflight transfer assessment |

Do not sum releases or site counts into a unique total without checking participant overlap. Independent study evaluation must preserve site identity and account for devices, season, timezone, wear coverage and outcome definitions. Consumer wearable stages and diaries are distinct from PSG.
