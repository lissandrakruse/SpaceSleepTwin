"""Audit Manchester published tables without redistributing participant records.
Install: pip install pyreadr pandas
Run: python analysis/import_manchester.py --raw /private/data --out audit.json
No predictive model is fitted. Downloads are pinned to an upstream commit.
"""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
import pyreadr

COMMIT = "ef570332cd6bd04cafea40a66f5a70e6f2206505"
FILES = ["light_daily_data.RData", "sleep_diary.RData", "sleep_fitbit.RData", "baseline_data.RData"]

def audit(raw, out):
    raw = Path(raw)
    raw.mkdir(parents=True, exist_ok=True)
    tables, checksums = {}, {}
    for name in FILES:
        content = urlopen(f"https://raw.githubusercontent.com/altugdidikoglu/light-sleep-inreallife/{COMMIT}/data/{name}", timeout=60).read()
        path = raw/name
        path.write_bytes(content)
        checksums[name] = hashlib.sha256(content).hexdigest()
        objects = pyreadr.read_r(str(path))
        if len(objects) != 1:
            raise ValueError(f"Expected one table in {name}")
        tables[name.removesuffix(".RData")] = next(iter(objects.values()))
    light = tables["light_daily_data"]
    report = {
        "status": "import and alignment audit only; no validated predictions",
        "source": "https://github.com/altugdidikoglu/light-sleep-inreallife",
        "upstream_commit": COMMIT,
        "tables": {k: {"rows": len(v), "participants": int(v.Id.nunique()), "columns": list(v.columns)} for k,v in tables.items()},
        "files_sha256": checksums,
        "warnings": [
            "TAT250 is minutes above 250 melanopic lux, not average daylight lux.",
            "presleep3hr uses observed Fitbit startTime; it is not a prospective bedtime feature.",
            "Id and yday4 reproduce the upstream join; verify dates and timezone before new analyses.",
            "Consumer wearable staging is not polysomnography.",
            "Confirm reuse and redistribution terms for the exact source release.",
            "No astronaut, DLMO or circadian-phase validation."
        ]
    }
    for label, name in [("fitbit", "sleep_fitbit"), ("diary", "sleep_diary")]:
        joined = light.merge(tables[name], on=["Id", "yday4"], validate="one_to_one")
        report[f"light_{label}_matched_rows"] = len(joined)
        report[f"light_{label}_matched_participants"] = int(joined.Id.nunique())
    Path(out).write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, help="Local directory outside the public repository")
    parser.add_argument("--out", default="manchester_import_audit.json")
    args = parser.parse_args()
    report = audit(args.raw, args.out)
    print(json.dumps({k:v for k,v in report.items() if "matched" in k}, indent=2))
