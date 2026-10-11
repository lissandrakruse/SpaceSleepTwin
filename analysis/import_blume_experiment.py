"""Join licensed, observed phase and sleep endpoints within the same experiment.

This is a provenance/harmonization step, not model calibration or new DLMO fitting.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import urllib.request
import zipfile

URL = "https://ndownloader.figshare.com/files/41362323"
ZIP_SHA256 = "1a89e9ff338e7e0e36f9d01970a7b898a608bdf0f2e6d1fdd8ae2e96731a78da"
CONDITIONS = {"BKG": "background", "B": "blue_dim", "blue": "blue_dim",
              "Y": "yellow_bright", "yellow": "yellow_bright"}
SETTINGS = {"background": 93.5, "blue_dim": 67.0, "yellow_bright": 123.5}


def key(row):
    condition = row.get("Condition", row.get("condition"))
    return int(row["PB_No"]), int(row.get("Visit", row.get("visit"))), CONDITIONS[condition]


def indexed(rows):
    result = {}
    for row in rows:
        k = key(row)
        if k in result:
            raise ValueError(f"Duplicate participant/visit/condition: {k}")
        result[k] = row
    return result


def number(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("Nonfinite endpoint")
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path)
    parser.add_argument("--profiles", type=Path, default=Path("data/dlmo_reference/data/Blume"))
    parser.add_argument("--output", type=Path, default=Path("analysis/blume_experiment"))
    args = parser.parse_args()
    raw = args.zip.read_bytes() if args.zip else urllib.request.urlopen(URL, timeout=30).read()
    if hashlib.sha256(raw).hexdigest() != ZIP_SHA256:
        raise ValueError("Source ZIP changed; review provenance before importing")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        def read(name):
            return list(csv.DictReader(io.StringIO(archive.read("Data/"+name).decode("utf-8-sig"))))
        phase = indexed(read("dlmo_data.csv"))
        sleep = indexed(read("SLatency_data.csv"))
        melatonin = read("melatonin_data.csv")
    phase_only = set(phase)-set(sleep)
    conflicts = {k for k in sleep if k not in phase and any(
        p[0] == k[0] and p[2] == k[2] for p in phase_only)}
    joined = []
    for k, row in sorted(sleep.items()):
        pb, visit, condition = k
        ref = phase.get(k)
        latency = number(row["LATcont10"])
        if latency < 0:
            raise ValueError("Negative latency")
        joined.append({
            "study_id": "Blume2024", "participant_id": f"blume2024_{pb}",
            "visit": visit, "condition": condition,
            "reported_stimulus_setting_photopic_lux": SETTINGS[condition],
            "exposure_duration_minutes": 60,
            "exposure_start_after_habitual_bedtime_minutes": 30,
            "phase_reference_present": ref is not None,
            "phase_alignment_status": "matched" if ref else (
                "visit_condition_conflict" if k in conflicts else "missing_phase_endpoint"),
            "observed_phase_shift_minutes": number(ref["shift"]) if ref else "",
            "source_dlmo_time": ref["DLMO_time"] if ref else "",
            "sleep_latency_to_10min_continuous_sleep_minutes": latency,
        })
    groups = defaultdict(list)
    for row in melatonin:
        groups[key(row)].append(row)
    if not set(phase).issubset(groups):
        raise ValueError("Phase records lack original melatonin visit/condition coverage")
    mapping = []
    for k, group in sorted(groups.items()):
        pb, visit, condition = k
        group.sort(key=lambda row: int(row["Number"]))
        if [int(row["Number"]) for row in group] != list(range(1, 34)):
            raise ValueError("Unexpected melatonin sampling sequence")
        for prefix, segment in [("first", group[:14]), ("second", group[-14:])]:
            name = f"{prefix}_Visit_{visit}_PB_{pb}.csv"
            path = args.profiles/name
            profile_raw = path.read_bytes()
            rows = list(csv.DictReader(io.StringIO(profile_raw.decode())))
            values = [number(row["melatonin"]) for row in rows]
            if len(values) != 14 or any(abs(a-number(b["Value"])) > 1e-9 for a,b in zip(values, segment)):
                raise ValueError(f"Profile does not reproduce original observations: {name}")
            mapping.append({"profile": name, "participant_id": f"blume2024_{pb}",
                            "visit": visit, "condition": condition, "evening": prefix,
                            "original_sample_numbers": "1-14" if prefix == "first" else "20-33",
                            "sha256": hashlib.sha256(profile_raw).hexdigest()})
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, rows in [("matched_endpoints.csv", joined), ("profile_provenance.csv", mapping)]:
        with (args.output/filename).open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    audit = {
        "source_doi": "10.6084/m9.figshare.23578698", "source_file_id": 41362323,
        "zip_sha256": ZIP_SHA256, "license": "CC BY 4.0",
        "article": "10.1038/s41562-023-01791-7",
        "endpoint_dictionary_code_revision": "e9bc03f89244b7b00e1cd9ec63b3091b09d75018",
        "participant_count": len({k[0] for k in sleep}), "sleep_visit_records": len(sleep),
        "phase_shift_visit_records": len(phase),
        "matched_phase_sleep_visit_records": len(set(phase)&set(sleep)),
        "visit_condition_conflicts": [list(k) for k in sorted(conflicts)],
        "unmatched_phase_visit_keys": [list(k) for k in sorted(phase_only)],
        "raw_melatonin_measurements": len(melatonin), "verified_profile_files": len(mapping),
        "sleep_records_by_condition": dict(Counter(k[2] for k in sleep)),
        "phase_records_by_condition": dict(Counter(k[2] for k in phase)),
        "missing_phase_keys": [list(k) for k in sorted(set(sleep)-set(phase))],
        "interpretation": [
            "These are repeated visits of 16 people, not 48 independent participants.",
            "The 96 Blume profile files are the same observations already counted in the dlmoR inventory; do not add them as another cohort.",
            "Phase shift values are original study endpoints, not estimates newly produced by SpaceSleepTwin.",
            "Positive phase shift is delay; negative is advance, in minutes (author analysis dictionary).",
            "Sleep endpoint is latency to 10 minutes of continuous sleep, not generic diary sleep onset latency.",
            "Photopic values describe reported stimulus settings, not daily mean exposure or melanopic EDI.",
            "Melanopsin excitation was matched across conditions; background was constant and blue/yellow modulated.",
            "Missing phase endpoints remain explicit. No fitting, predictive validation, or causal reanalysis has been performed.",
            "Participant 4 has swapped blue/yellow visit labels between melatonin/phase and sleep tables; those two sleep visits are not linked to a phase endpoint pending original-record verification.",
        ],
    }
    (args.output/"import_audit.json").write_text(json.dumps(audit, indent=2)+"\n")
    print(json.dumps({k: audit[k] for k in ["participant_count", "sleep_visit_records", "phase_shift_visit_records", "verified_profile_files"]}))


if __name__ == "__main__":
    main()
