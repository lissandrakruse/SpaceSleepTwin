"""Download and audit licensed melatonin profiles at a fixed upstream commit.

Standard library only. This is an import audit, not a DLMO estimator.
"""
import argparse
import concurrent.futures
import csv
from datetime import datetime
import hashlib
import io
import json
import math
from pathlib import Path
import urllib.request

REPOSITORY = "tscnlab/ThaljiEtAl_JBiolRhythms_2026"
COMMIT = "bde58d569c3002772262cb57788f5486d11a90e2"
DLMOR_COMMIT = "3f9ff3277b8e9ecbd4ca68e1efeb857ab483d180"


def download(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise


def audit(path):
    raw = path.read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if reader.fieldnames != ["datetime", "melatonin"]:
        raise ValueError(f"Unexpected columns: {path}")
    rows = list(reader)
    times = [datetime.fromisoformat(row["datetime"]) for row in rows]
    values = [float(row["melatonin"]) for row in rows]
    intervals = [(b-a).total_seconds()/60 for a,b in zip(times,times[1:])]
    return {
        "profile": path.name, "cohort": path.parent.name,
        "sha256": hashlib.sha256(raw).hexdigest(), "rows": len(rows),
        "nonfinite_values": sum(not math.isfinite(v) for v in values),
        "negative_values": sum(v < 0 for v in values),
        "duplicate_timestamps": len(times)-len(set(times)),
        "strictly_increasing_timestamps": all(v > 0 for v in intervals),
        "span_hours": (times[-1]-times[0]).total_seconds()/3600,
        "minimum_interval_minutes": min(intervals) if intervals else None,
        "maximum_interval_minutes": max(intervals) if intervals else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("data/dlmo_reference"))
    parser.add_argument("--output", type=Path, default=Path("analysis/dlmo_import_audit.json"))
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    if not args.offline:
        tree = json.loads(download(f"https://api.github.com/repos/{REPOSITORY}/git/trees/{COMMIT}?recursive=1"))
        if tree.get("truncated"):
            raise ValueError("Incomplete upstream tree")
        files = [x["path"] for x in tree["tree"] if x["type"] == "blob" and
                 (x["path"].startswith("data/") and x["path"].endswith(".csv") or
                  x["path"] in {"LICENSE.md", "README.md", "renv.lock"})]
        def fetch(name):
            target = args.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(download(f"https://raw.githubusercontent.com/{REPOSITORY}/{COMMIT}/{name}"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(fetch, files))
    profiles = [audit(p) for p in sorted((args.root/"data").glob("*/*.csv"))]
    if not profiles:
        raise ValueError("No melatonin profiles found")
    counts = {}
    for profile in profiles:
        counts[profile["cohort"]] = counts.get(profile["cohort"], 0)+1
    result = {
        "source_repository": REPOSITORY, "source_commit": COMMIT,
        "data_license": "CC BY 4.0", "dlmor_article_ref": "v0.1.1",
        "dlmor_source_commit": DLMOR_COMMIT,
        "status": "raw import audited; DLMO estimation is a separate R step",
        "profile_files": len(profiles), "cohort_profile_counts": counts,
        "measurement_rows": sum(p["rows"] for p in profiles),
        "caveats": [
            "File counts are profiles, not independent participants.",
            "Raw inventory is not the paper's selected analytic sample.",
            "Do not interpret profile timestamps as original local biological clock times without provenance verification.",
            "No matched continuous light/sleep histories are established by this import.",
        ], "profiles": profiles,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({k: result[k] for k in ["profile_files", "cohort_profile_counts", "measurement_rows"]}))


if __name__ == "__main__":
    main()
