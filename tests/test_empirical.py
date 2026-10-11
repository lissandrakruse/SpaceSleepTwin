"""Synthetic fixtures verify software only; no human research results."""
import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from analysis.empirical import analyze

class EmpiricalTests(unittest.TestCase):
    def fixture(self):
        return pd.DataFrame([dict(participant_id=f"{p:03}", date=f"2026-01-{d:02}",
            day_medi_lux=100+p*10, prebed_medi_lux=5+d,
            sleep_latency_min=10+p+d) for p in range(12) for d in range(1,5)])

    def run_data(self, data):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"synthetic.csv"
            data.to_csv(path, index=False)
            result = analyze(path, Path(folder)/"out")
            predictions = pd.read_csv(Path(folder)/"out/holdout_predictions.csv")
            json.loads((Path(folder)/"out/metrics.json").read_text())
            return result, predictions

    def test_holdout_and_baseline(self):
        result, predictions = self.run_data(self.fixture())
        self.assertEqual(result["participant_overlap"], 0)
        self.assertEqual(result["train_participants"] + result["test_participants"], 12)
        self.assertEqual(len(result["source_sha256"]), 64)
        self.assertAlmostEqual(result["baseline"]["test_mae_minutes"],
            np.abs(predictions.observed_latency_min-predictions.baseline_latency_min).mean())
        second, _ = self.run_data(self.fixture())
        self.assertEqual(result["test_mae_minutes"], second["test_mae_minutes"])

    def test_duplicates_rejected(self):
        frame = self.fixture()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.run_data(pd.concat([frame,frame.iloc[:1]]))

    def test_studies_not_silently_pooled(self):
        frame = self.fixture()
        frame["study_id"] = ["a","b"]*24
        with self.assertRaisesRegex(ValueError, "harmonization"):
            self.run_data(frame)

    def test_missing_exposure_rejected(self):
        frame = self.fixture()
        frame["prebed_medi_lux"] = np.nan
        with self.assertRaisesRegex(ValueError, "observed training"):
            self.run_data(frame)

if __name__ == "__main__":
    unittest.main()
