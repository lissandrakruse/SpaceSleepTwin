"""SpaceSleepTwin empirical analysis: authorized participant-level daily light/sleep CSV.
Usage: python analysis/empirical.py observations.csv --out results
Expected columns: participant_id,date,day_medi_lux,prebed_medi_lux,sleep_latency_min
Optional: sleep_duration_h,study_id. Each row is a participant-day.
This is an observational association analysis, NOT astronaut or circadian-phase validation.
"""
import argparse
import json
import hashlib
import platform
from importlib.metadata import version
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

FEATURES = ["day_medi_lux", "prebed_medi_lux"]
REQUIRED = ["participant_id", "date", "sleep_latency_min"] + FEATURES

def analyze(input_csv, out_dir):
    df = pd.read_csv(input_csv, dtype={"participant_id": "string"})
    input_rows = len(df)
    if "study_id" in df and df["study_id"].dropna().nunique() > 1:
        raise ValueError("Analyze each study separately until harmonization is documented.")
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for c in FEATURES + ["sleep_latency_min"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=["participant_id", "date", "sleep_latency_min"])
    df = df[(df["sleep_latency_min"] >= 0) & (df["sleep_latency_min"] <= 300)]
    for c in FEATURES:
        df.loc[df[c] < 0, c] = np.nan
    if df.duplicated(subset=["participant_id", "date"]).any():
        raise ValueError("Duplicate participant-days: resolve records before analysis.")
    if df["participant_id"].nunique() < 6:
        raise ValueError("At least six distinct participants are required for a grouped holdout.")
    if len(df) < 12:
        raise ValueError("At least 12 valid participant-days are required.")
    X = np.log1p(df[FEATURES])
    y = df["sleep_latency_min"]
    groups = df["participant_id"].astype(str)
    split = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=42)
    train, test = next(split.split(X, y, groups))
    model = Pipeline([("impute", SimpleImputer(strategy="median")),
                      ("scale", StandardScaler()), ("ridge", Ridge(alpha=10.0))])
    if any(X.iloc[train][c].notna().sum() == 0 for c in FEATURES):
        raise ValueError("Each exposure feature needs observed training values.")
    model.fit(X.iloc[train], y.iloc[train])
    pred = model.predict(X.iloc[test])
    baseline = np.full(len(test), float(y.iloc[train].mean()))
    baseline_mae = float(mean_absolute_error(y.iloc[test], baseline))
    model_mae = float(mean_absolute_error(y.iloc[test], pred))
    result = {
        "status": "observational model; NOT a validated circadian digital twin",
        "source_file": Path(input_csv).name,
        "source_sha256": hashlib.sha256(Path(input_csv).read_bytes()).hexdigest(),
        "environment": {"python": platform.python_version(), **{p: version(p) for p in ["numpy", "pandas", "scikit-learn"]}},
        "quality": {"input_rows": input_rows, "excluded_rows": input_rows - len(df),
                    "missing_exposure_values": {c: int(df[c].isna().sum()) for c in FEATURES}},
        "baseline": {"method": "training mean latency", "test_mae_minutes": baseline_mae,
                     "model_mae_improvement_minutes": baseline_mae - model_mae},
        "participant_overlap": int(len(set(groups.iloc[train]) & set(groups.iloc[test]))),
        "n_participants": int(groups.nunique()),
        "n_participant_days": int(len(df)),
        "train_participants": int(groups.iloc[train].nunique()),
        "test_participants": int(groups.iloc[test].nunique()),
        "test_mae_minutes": float(mean_absolute_error(y.iloc[test], pred)),
        "test_rmse_minutes": float(np.sqrt(mean_squared_error(y.iloc[test], pred))),
        "test_r2": float(r2_score(y.iloc[test], pred)) if len(test) > 1 and y.iloc[test].nunique() > 1 else None,
        "split": "grouped by participant, random_state=42",
        "features": FEATURES,
        "target": "self-reported sleep latency in minutes",
        "warnings": [
            "Observational association is not causation.",
            "This does not estimate DLMO or circadian phase.",
            "Participant-day records are not independent people.",
            "No astronaut or spaceflight validation is implied.",
            "Different devices and studies must not be pooled without harmonization."
        ]
    }
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    pd.DataFrame({"participant_id": groups.iloc[test].to_numpy(),
                  "date": df["date"].iloc[test].dt.strftime("%Y-%m-%d").to_numpy(),
                  "observed_latency_min": y.iloc[test].to_numpy(),
                  "predicted_latency_min": pred,
                  "baseline_latency_min": baseline,
                  "residual_min": y.iloc[test].to_numpy() - pred}).to_csv(output / "holdout_predictions.csv", index=False)
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input_csv")
    p.add_argument("--out", default="results")
    args = p.parse_args()
    print(json.dumps(analyze(args.input_csv, args.out), indent=2))
