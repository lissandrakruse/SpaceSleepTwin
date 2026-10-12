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
τ=23.8 h → −0.690 h; τ=24.6 h → −1.133 h. Level 2 → −1.113 h.
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
