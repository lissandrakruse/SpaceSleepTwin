# Mechanistic circadian model (SpaceSleepTwin v2 research engine)

This module implements the **Forger99** three-state limit-cycle model, with Process L and Process P, based on Forger, Jewett & Kronauer (1999). It is distinct from the simplified phase oscillator used by the browser visualization. The browser has **not yet been connected** to this Python engine.

## Scientific sources
- Forger, Jewett & Kronauer (1999): https://doi.org/10.1177/074873099129000867
- Model implementation and parameter documentation: https://arcascope.github.io/circadian/api/models.html
- Jewett, Forger & Kronauer (1999): https://doi.org/10.1177/074873049901400608

## Run
```bash
pip install numpy pandas scipy
python research/forger99.py --days 45 --tau 24.2 --out scenarios.csv
```

Outputs x, xc, n, photopic lux and simulation time for three lighting profiles. **Do not interpret x directly as measured sleep, DLMO, or a validated phase shift.** Model initialization and entrainment require burn-in and reference-phase estimation before such outputs are inferred.

## Planned experiment
A: fixed lighting; B: predefined dynamic schedule; C: optimized individual schedule (not implemented).
Use identical constraints and individual parameters, with training and holdout subjects separated. Optimization must use a prespecified objective and respect visual safety and operational lighting needs.

## Hypothesis
Personalized model-predictive lighting could reduce estimated circadian misalignment compared with static and standardized dynamic schedules. This is a **hypothesis**, not an established improvement in astronaut sleep.

## Limitations
Light inputs are illustrative photopic lux, not spectral/melanopic exposure. No astronaut data are used; the model has not been calibrated or independently validated. Do not use this prototype to prescribe astronaut lighting.
