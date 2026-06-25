# © 2026 Raj Kumar. All rights reserved. Credential Fortress is an educational, simulation-only toolkit. Unauthorized use is prohibited.

import csv
from pathlib import Path
from datetime import datetime, timezone

METRICS_FILE = Path("reports/metrics.csv")

def init_metrics() -> None:
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not METRICS_FILE.exists():
        with open(METRICS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Scenario", "Wordlist_Size", "Simulated_Hash_Rate", "Estimated_Crack_Time_Secs", "Run_Duration_Secs"])

def record_metric(scenario: str, wordlist_size: int, hash_rate: int, crack_time: float, run_duration: float) -> None:
    """Records local-only metrics about the simulation run."""
    init_metrics()
    with open(METRICS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            scenario,
            wordlist_size,
            hash_rate,
            f"{crack_time:.2f}",
            f"{run_duration:.4f}"
        ])
