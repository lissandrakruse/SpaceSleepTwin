# HERA benchmark: exploratory aggregate comparison

The browser implements the Forger99 oscillator already used by the research
notebook. It replaces the earlier phenomenological phase-update calculation.
The numerical phase proxy is the time of each minimum of x; it is not a
predicted urinary melatonin concentration or peak time.

## Published inputs

Rahman et al., *J Pineal Research* (2022), DOI
[10.1111/jpi.12826](https://doi.org/10.1111/jpi.12826),
[article and Table 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC11316501/).

The 45-day HERA protocol used two 23:00–07:00 and five 02:00–07:00 sleep
opportunities per weekly cycle. Dynamic lighting dimmed three hours before
bedtime. Collection windows lasted 48 hours from mission days 5, 12, 19, 26,
33 and 43. Published aggregate urinary aMT6s acrophases were SLS 6.22 h and
DLS 4.76 h: DLS−SLS = −1.46 h.

| Assumed eye-level environment | SLS photopic lux | DLS day lux | DLS final 3h lux |
| --- | ---: | ---: | ---: |
| Level 1 | 122 | 264 | 13 |
| Level 2 | 143 | 80 | 4 |

## Reconstruction assumptions

- The same initial oscillator state is used for both conditions.
- Both follow an assumed 21-day premission routine: 150 photopic lux from
  07:00 to 23:00, zero during sleep. This is not observed HERA premission light.
- The weekly cycle begins with two long-sleep nights. All seven cycle offsets
  are explored in the notebook rather than choosing the best match.
- A person remains in the selected habitat level throughout wakefulness.
- Final-hour lighting and spectra are summarized; sleep means zero eye exposure.
- The six window contrasts are averaged equally. This does not reproduce the
  published mixed-model estimator or participants' individual exposures.

Photopic lux is the engine's native input. The notebook's naive melanopic-EDI
substitution is an explicitly experimental sensitivity scenario and is not
offered as a validated browser input.

## Executed results

At τ=24.2 h and Level 1, the Python benchmark gives approximately −1.329 h;
the browser RK4 implementation reproduces that contrast. Its discrepancy
from −1.46 h is approximately 7.9 minutes. This compares **different markers**,
not individual prediction errors. Parameters were not optimized against this
known target; nevertheless, the target is not an unseen validation set.

Cycle-offset scenarios: −1.335 to −1.327 h. Intrinsic-period scenarios:
τ=23.8 h → −0.690 h; τ=24.6 h → −1.133 h on the notebook 5-minute
output grid, and −1.142 h on a refined 30-second grid matching the browser.
Level 2 → −1.113 h.
At τ=24.6 h, some minima occur near abrupt light-switch boundaries; finer
output sampling reduces interpolation error. The default τ=24.2 h contrast
remains −1.329 h.
These are sensitivity scenarios, not confidence intervals.

The Python notebook uses adaptive SciPy integration. The browser uses RK4
with a 30-second maximum step and exact light-switch boundaries. Phase minima
use parabolic interpolation and comparisons use circular differences. Tests
check Python/browser agreement, step refinement and identical-light controls.

## Interpretation and next work

The model reproduces the direction and approximates the magnitude of a
published space-analog aggregate contrast under a simplified reconstruction.
It does not establish individual astronaut accuracy, improvements in sleep,
causality for the twin, or a validated connection from x-minimum to aMT6s.
Population baseline phase differences and biomarker timing remain unresolved.

Audit the supplementary light protocol, establish a biomarker mapping and
obtain individual exposure/phase records before making stronger claims.
The source article directs individual-data requests to NASA LSDA.
Prediction and intervention benefit need separate evaluation designs.

## Reproduction

Open [the executed notebook](spacesleeptwin_hera_benchmark.ipynb) in Kaggle or
Jupyter with numpy, pandas, scipy and matplotlib. It contains no participant
records. For browser engine checks: `node tests/test_simulator.cjs` from the
repository root. The existing illustrative engine in `research/forger99.py`
remains available; the browser HERA reconstruction is in `simulator.js`.

Model: Forger, Jewett & Kronauer (1999),
[A Simpler Model of the Human Circadian Pacemaker](https://doi.org/10.1177/074873099129000867).


## Factorial input decomposition (executed, exploratory)

At Level 1, τ=24.2 h, with identical initial states and a 30-second output grid:

| Schedule | Day / final three waking hours (photopic lux) | Mean proxy contrast vs SLS (h) |
| --- | --- | ---: |
| SLS | 122 / 122 | 0.0000 |
| Daytime change only | 264 / 122 | −0.5369 |
| Evening dimming only | 122 / 13 | −1.0455 |
| Full DLS | 264 / 13 | −1.3291 |

Full minus the isolated contrasts is +0.2533 h: the oscillator is nonlinear.
These partial schedules are model counterfactuals, not HERA intervention arms.
They do not decompose the observed causal effect. No percentage attribution
or optimal schedule is inferred. All arms keep sleep exposure at zero.
At Level 2, dynamic daytime light is *lower* than standard; the day-only change
produces +0.4842 h at τ=24.2 h. Predefined sensitivity uses both levels and
τ=23.8/24.2/24.6 h, with full results in hera_decomposition.json.

The model receives photopic lux, not the published dynamic spectral response.
It cannot quantify the spectrum's contribution. Comparing vertical photopic
and horizontal melanopic measurements confounds geometry and spectrum.
Underestimation of the physiological contrast is a possibility, not a result.

Reproduce with the appended cell in spacesleeptwin_hera_benchmark.ipynb.
The script decompose_hera.py generates its aggregate outputs from the notebook
functions; execute it on a clean benchmark copy to avoid duplicate appended cells.


## Fixed schedule and input-metric sensitivity

At Level 1 and τ=24.2 h, the four configurations were fixed before execution:

| Schedule | Input | Day-only Δh | Evening-only Δh | Full Δh |
| --- | --- | ---: | ---: | ---: |
| HERA_variable | L1_photopic | -0.5369 | -1.0455 | -1.3291 |
| HERA_variable | L1_melEDI_proxy | -0.6777 | -1.0832 | -1.4326 |
| conventional_23_07 | L1_photopic | -0.4947 | -1.0151 | -1.3929 |
| conventional_23_07 | L1_melEDI_proxy | -0.6395 | -1.0595 | -1.5340 |

Evening dimming retains the larger isolated phase contrast in these settings.
This is conditional model robustness, not general dominance across τ, location,
or human cohorts. Conventional sleep changes timing and duration together.
melEDI substitution is an unvalidated numerical input sensitivity, not a
physiologically validated spectral comparison. No optimum is established.
See robustness_hera.py and hera_robustness.json; the notebook includes executed
outputs. The proposed H4 request addendum is LSDA_H4_ADDENDUM.md.
