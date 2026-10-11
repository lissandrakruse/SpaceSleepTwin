"""Plot two explicitly selected observed profiles; no inferred DLMO overlay."""
import argparse
import csv
from datetime import datetime
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, default=Path("data/dlmo_reference/data"))
parser.add_argument("--output", type=Path, default=Path("research/figures/melatonin_observations.svg"))
args = parser.parse_args()
selected = [("Blume", "first_Visit_1_PB_1.csv"),
            ("Civibe", "civibe_melatonin_FD200_day1.csv")]
fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
for ax, (cohort, name) in zip(axes, selected):
    rows = list(csv.DictReader((args.root/cohort/name).open()))
    times = [datetime.fromisoformat(r["datetime"]) for r in rows]
    hours = [(t-times[0]).total_seconds()/3600 for t in times]
    ax.plot(hours, [float(r["melatonin"]) for r in rows], "o-", color="#226c8b")
    ax.axhline(2.3, color="#a25730", linestyle="--", label="Analysis threshold: 2.3 pg/mL")
    ax.set(xlabel="Hours since first profile sample", ylabel="Melatonin (pg/mL)",
           title=cohort+" example observed profile")
    ax.grid(alpha=0.2)
    ax.legend(fontsize=8)
fig.suptitle("Observed melatonin profiles — not SpaceSleepTwin predictions", fontsize=12)
args.output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output, metadata={"Description": "Two selected raw profiles from Thalji & Spitschan 2026, pinned source bde58d569c3002772262cb57788f5486d11a90e2. Data CC BY 4.0. Relative analysis time only; curves do not represent a cohort average or twin validation."})
print(args.output)
