# SpaceSleepTwin — Mission Control

Interactive **English-language research prototype** for exploring circadian lighting schedules in simulated spaceflight.

**[Open the website after GitHub Pages is enabled](https://lissandrakruse.github.io/SpaceSleepTwin/)**

## Features
- Futuristic mission-control UI and eye visualization
- Dynamic, static and late-bright-light LED scenarios
- Mission durations from 7 to 180 days
- Adjustable intrinsic circadian period
- Simulated phase plot and CSV export
- References and explicit scientific limitations

## Scientific limitations
This is a simplified phenomenological circadian oscillator for exploratory scenario comparison. It is **not** the full Jewett–Forger–Kronauer model and has **not** been calibrated or validated using astronaut observations. Lighting profiles use illustrative photopic lux, **not** CIE S 026 melanopic EDI. It is not medical guidance, an official NASA product, or evidence of astronaut health outcomes.

## Evidence and real-data development
The source-to-component map is documented in [research/TWIN_SOURCES.md](research/TWIN_SOURCES.md). It includes Manchester and MeLiDos measurements, the Forger99 research engine, Brown et al. exposure guidance, HERA lighting research, dlmoR melatonin methods, and SUNSHINE context.

Manchester and Costa Rica tables have been downloaded and inspected locally; aggregate import audits are in analysis/. They have not calibrated the browser simulator. HERA and SUNSHINE participant records require access requests. See [research/EVIDENCE_MAP.md](research/EVIDENCE_MAP.md) for findings and limitations.

## Open melatonin reproduction

The [DLMO reproduction record](analysis/DLMO_REPRODUCTION.md) documents a pinned import of 120 raw melatonin profiles (1,889 measurements), file integrity checks, the article's analytic exclusions, and the original R environment. The [workflow](.github/workflows/dlmo-reference.yml) extracts baseline estimates with the article's dlmoR source and preserves per-profile errors and session information. See [execution results](https://github.com/lissandrakruse/SpaceSleepTwin/actions/workflows/dlmo-reference.yml) for actual run status; successful extraction does not validate the twin.

[Two selected observed profiles](research/figures/melatonin_observations.svg) illustrate the raw data on a relative time axis.

The [original Blume experiment audit](analysis/blume_experiment/README.md) verifies that the 96 Blume curves match original observed measurements and links phase-shift and sleep endpoints within 44 visits from the same study. Missing endpoints and two conflicting visit labels remain explicit. This is the same cohort already in the melatonin inventory, not an increase in independent participants. Both [coarse](analysis/dlmo_pilot/baseline_estimates.csv) and [fine-grid](analysis/dlmo_fine_pilot/baseline_estimates.csv) extraction have executed successfully on one real profile, with their actual R sessions recorded. Full-cohort reproduction and validation of the twin remain separate work.

## Key references
1. Brown TM et al. (2022), *PLOS Biology*. https://doi.org/10.1371/journal.pbio.3001571
2. CIE S 026/E:2018. https://cie.co.at/publications/cie-system-metrology-optical-radiation-iprgc-influenced-responses-light-0
3. Jewett ME, Forger DB, Kronauer RE (1999). Revised limit cycle oscillator model. https://pubmed.ncbi.nlm.nih.gov/?term=Jewett+Forger+Kronauer+1999+circadian
4. NASA Human Research Program: https://www.nasa.gov/hrp/

## Publishing with GitHub Pages
Repository Settings → Pages → Build and deployment → Deploy from a branch → **main** / **/(root)** → Save.

## Researcher
Lissandra Kruse Fuganti · Applied Computing · UEPG, Brazil.
