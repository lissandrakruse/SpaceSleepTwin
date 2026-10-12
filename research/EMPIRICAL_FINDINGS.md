# Empirical findings: two Earth cohorts

Source: researcher-supplied executed `artigo_spacesleeptwin.ipynb`, 74 original cells.
A [public reproduction copy](artigo_spacesleeptwin.ipynb) includes an added
sanitization notice and selected aggregate outputs; participant-level outputs
and figures have been removed. The underlying analysis was not rerun.
This update transcribes aggregate outputs, not a fresh participant-data analysis.
No participant records are published. Full study-population sizes may differ
from the following analytical subsets.

| Subset | Adults | Nights | Final-night holdout | Events >30 min | History AUC | History Brier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Manchester | 88 | 440 | 80 | 13 | 0.7623 | 0.1302 |
| MeLiDos | 145 | 1,003 | 144 | 18 | 0.8223 | 0.0781 |

MeLiDos includes eight analyzed sites in six countries; Costa Rica/UCR was
excluded because its diaries had already been analyzed. Development uses
person-grouped validation. Personal history includes only prior nights.
Final-night holdout requires at least three available nights.

## Predictive findings

| Holdout latency model | Manchester MAE (min) | MeLiDos MAE (min) |
| --- | ---: | ---: |
| Personal median history | 11.94 | 12.13 |
| Quantile + sleep-pressure features | 11.51 | 12.88 |
| Nested history/quantile blend | 11.57 | 12.59 |
| Quantile + prospective prebed light | Not the same prospective feature | 12.87 |

Original H1's MeLiDos feature is mean light in the three hours before bed:
12.87 versus 12.88 min is not a meaningful predictive gain. It does not rule
out physiological evening-light effects.

No consistent superiority over history was demonstrated. Some models were
numerically better on specific metrics: MeLiDos secondary LightGBM MAE 12.05;
logistic AUC 0.8250 versus history 0.8223, but Brier 0.0824 versus 0.0781.
Manchester quantile minus history MAE was −0.429 min, with descriptive paired
95% interval [−1.979, 1.002]. AUC is discrimination, not percent accuracy.
Few held-out events and multiple model comparisons constrain inference.

## Exploratory light association

Pooled standardized quantile-regression coefficients for daytime bright-duration
`log_tat` were −2.81 min/SD (Manchester), −1.07 min/SD (MeLiDos).
This is a log-transformed feature, not a coefficient per lux or raw minute.
Coefficients have no reported confidence intervals and were examined after
both holdouts were opened. Association does not establish causality.

## Provenance and limitations

Manchester development was exploratory. Its notebook reports one holdout
evaluation with v3 choices fixed but no preceding seal commit. MeLiDos principal
comparisons were specified before inspecting its outcomes. Cross-cohort transfer
and pooled associations are post-holdout exploratory analyses. Bootstrap intervals
are descriptive without multiplicity correction. Diary constructs and sensors differ.

HERA latency/wakefulness comparisons use cohort summaries, not joined individual
records. Published HERA dynamic light improved circadian alignment without a
statistically significant latency difference. The separate
[phase benchmark](HERA_BENCHMARK.md) is already executed: default −1.329 h
versus aggregate urinary aMT6s contrast −1.46 h, using distinct phase markers.

Working hypothesis: history and sleep pressure may dominate same-night latency
prediction, while lighting may mainly support circadian alignment. None of these
results validates predictions or benefits in astronauts.

The HERA article directs individual-data requests to [NASA LSDA](https://lsda.jsc.nasa.gov/).
The [prospective plan](VALIDATION_PROTOCOL.md) is not a registered study or an
approved request. Authorized individual records and independent evaluation
are needed for transfer to spaceflight.

## Sources

- Guidolin C et al. (2024). Protocol for a prospective, multicentre,
  cross-sectional cohort study to assess personal light exposure.
  BMC Public Health 24:3285. https://doi.org/10.1186/s12889-024-20206-4
- Forger DB, Jewett ME, Kronauer RE (1999). A simpler model of the human
  circadian pacemaker. J Biol Rhythms 14(6):532–537.
  https://doi.org/10.1177/074873099129000867
- HERA: https://doi.org/10.1111/jpi.12826
- Manchester data: https://doi.org/10.48420/23786238
- Researcher notebook: https://www.kaggle.com/code/lissandrakruse/notebookddc2625012


## Number-to-source map

The public copy begins with one added notice cell. Cell numbers below are
one-based in that copy. Retained aggregate outputs are from the supplied run.

| Website quantity | Source location |
| --- | --- |
| Manchester analyzed 88 adults/440 nights and 80 held-out nights | Part A §2, public cell 9 code; cohort-size audit in supplied original output |
| MeLiDos 145 adults/1,003 nights, 8 sites | Part B §2, public cell 44 code; six countries listed in Part C cohort-comparison markdown |
| Manchester AUC/Brier and 13 events | Part A §10, public cell 31 retained aggregate output |
| MeLiDos AUC/Brier, 18 events, holdout 144, H1 MAE | Part B §6, public cell 55 retained aggregate outputs |
| Cohort comparison and history MAE | Part B §7, public cell 57 retained aggregate outputs |
| Daytime-light coefficients −2.81/−1.07 | Part C §3, public cell 70 retained aggregate output |

Local raw files and participant predictions generated by notebook execution
are not part of this public copy and should not be uploaded automatically.
