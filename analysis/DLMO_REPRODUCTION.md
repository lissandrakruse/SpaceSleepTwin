# Open melatonin baseline reproduction

Source: Thalji & Spitschan (2026), https://doi.org/10.1177/07487304251389994.
Data/code repository: https://github.com/tscnlab/ThaljiEtAl_JBiolRhythms_2026.
Source commit: bde58d569c3002772262cb57788f5486d11a90e2.
Data: CC BY 4.0; upstream code: MIT.

## Completed import audit

The raw repository contains 120 profile CSV files: 96 Blume and 24 Civibe, totaling 1,889 measurement rows. All 120 downloaded files matched their upstream Git blob hashes. The initial audit found no nonfinite or negative melatonin concentrations, duplicate timestamps within a profile, or nonincreasing timestamp sequences.

These are profile files, not 120 independent participants. The raw inventory is not the article's selected analytic sample. The article reports that eight of the 96 Blume profiles did not yield estimates in either method (ambiguous baseline/rise or a profile entirely above/below the threshold), leaving 88 Blume plus 24 Civibe profiles in its 112-profile benchmark. This is an external benchmark to check against our output, not a count of successful estimates from our own run. Repeated conditions, visits, and days must be modeled as repeated observations; do not split their records randomly as independent people.

The article repository README calls the package version v0.1.1. Its renv.lock records RemoteRef v0.1.1 and RemoteSha 3f9ff3277b8e9ecbd4ca68e1efeb857ab483d180, although the package Version field is 0.1.0. The current upstream main inspected during this work identifies itself as 0.2.0. Use the recorded source SHA rather than silently switching versions.

## Reproduce

From the SpaceSleepTwin root:

```sh
python3 analysis/import_dlmo_reference.py
Rscript -e 'install.packages("renv"); renv::restore(lockfile="data/dlmo_reference/renv.lock", prompt=FALSE)'
Rscript analysis/estimate_dlmo_reference.R
```

The workflow .github/workflows/dlmo-reference.yml performs these steps using R 4.4.3, the version recorded in the upstream lockfile. Downloaded data stay outside committed project source. The workflow publishes an artifact with its audit, baseline estimates, status counts, and session information.

The R runner saves each completed profile separately and processes independent curves on up to four available CPU cores. It uses the pinned dlmoR hockey-stick implementation, threshold 2.3 pg/mL, and fine-grid estimation. This is baseline extraction from observed melatonin curves. It retains every profile, including estimation errors and warnings.

## Executed preliminary pilot

The corrected single-profile coarse-grid pilot completed successfully on 2026-10-11: https://github.com/lissandrakruse/SpaceSleepTwin/actions/runs/38149555486. Its actual output and R session are in dlmo_pilot/. For first_Visit_1_PB_1.csv, the estimate is 1.55 hours on the imported analysis axis, with threshold 2.3 pg/mL. The displayed 01:33:00 is not established as original participant-local clock time. This pilot demonstrates execution on one real curve; it is not full-sample reproduction or validation of a biological prediction.

A prior 120-profile coarse batch exported no successful estimates: 106 errors arose when the pinned package called scale_y_continuous without ggplot2 attached; 14 other errors require method/profile review. The runner now attaches ggplot2 as the author's analysis scripts do. Failure records are retained in dlmo_attempts/. Do not label all these curves biologically invalid or claim a reproduced 112-profile benchmark. Fine-grid extraction is a separate verification step.

The original [Blume experiment import](blume_experiment/README.md) also verifies the provenance of all 96 Blume curves and safely aligns 44 observed phase/sleep visit records, keeping missing values and source conflicts explicit.

## Interpretation and outstanding work

Import success is verified locally; one coarse-grid extraction pilot is verified from its successful workflow and downloaded output. Expanded and fine-grid outputs require their own outcome checks.

Profile timestamps are analysis coordinates. In particular, some Blume files use a common date and start near midnight. Do not treat those values as original participant-local DLMO clock times without examining timestamp transformations in the original source studies. Parsing using UTC does not resolve this provenance question.

Next evaluate failure patterns, confirm the paper's profile inclusion rules, and compare results with its derived baseline tables. Then run threshold and sampling sensitivity analyses. Successful curve fitting is not an independent validation of a circadian prediction.

This import does not establish matched continuous light exposure and sleep histories. SpaceSleepTwin has not been calibrated against these profiles; terrestrial data alone do not establish performance in astronauts.
