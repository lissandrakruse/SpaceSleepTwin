# Manchester competition v2 — final model selection

Recorded 2026-10-11 before any holdout evaluation performed in this workspace.

## Frozen selection authorized by the researcher

1. Personal-history model — primary reference under MAE.
2. Quantile model with Process S proxies — secondary candidate; evaluate both MAE and RMSE without changing the primary metric after seeing holdout results.
3. Nested combination of history and quantile S — secondary candidate; combination weight must be selected using development data / inner validation only.

Primary endpoint: diary latency in minutes. Primary metric: MAE. RMSE is secondary. Do not select models, weights, hyperparameters or preprocessing using holdout outcomes. Report all three once, whether favorable or unfavorable. Do not rerun final evaluation to tune results. Keep data_manchester/ and individual predictions (including oof_predictions.csv) out of the public repository; strip record-level notebook outputs before publication.

## Provenance and execution status

This selection is based on the researcher's supplied v2 summary, not independently verified notebook outputs. The reported development MAE/RMSE are history 9.66/17.13, quantile S 9.85/15.73, nested combination 9.86/16.46 minutes.

manchester_competition_v2.ipynb was not found in the current workspace, default branch repository tree, or exact filename search of accessible stored files. The holdout has NOT been opened by this assistant. No EVALUATE_HOLDOUT flag has been changed and no final holdout score is available.

Before execution: obtain the exact executed notebook and its existing private data/split manifest; verify the holdout membership and preprocessing, feature availability at prediction time, history construction, and development-only nested weight selection. Record notebook/config/split SHA-256 before enabling EVALUATE_HOLDOUT=True. Use the original holdout definition, never reconstruct a new split as a substitute. Create an execution marker before accessing holdout outcomes and preserve final aggregate output and environment versions. Interpret Process S inputs as proxies, not validated mechanistic Process S states.

This document records model selection only; it is not a claim of completed notebook review, executable FINAL_MODELS mutation, or opened holdout.
