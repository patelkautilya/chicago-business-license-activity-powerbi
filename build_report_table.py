"""Create a compact, non-identifying Power BI table from the validated extract."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "chicago_business_licenses_issued_2024_2025.csv"
OUTPUT = ROOT / "license_activity_month_type_area_2024_2025.csv"
SUMMARY = ROOT / "validation_summary.json"
FIELDS = ["issue_month", "issue_year", "application_type", "license_description",
          "community_area_name", "license_records"]


def main() -> None:
    validation = json.loads(SUMMARY.read_text(encoding="utf-8"))
    counts: Counter[tuple[str, ...]] = Counter()
    raw_count = 0
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["issue_month"], row["issue_year"], row["application_type"],
                   row["license_description"], row["community_area_name"] or "(missing)")
            counts[key] += 1
            raw_count += 1
    if raw_count != validation["records"] or sum(counts.values()) != raw_count:
        raise ValueError("Report table failed to reconcile to the validated extract")
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDS)
        for key, value in sorted(counts.items()):
            writer.writerow([*key, value])
    print(json.dumps({"source_records": raw_count, "report_rows": len(counts),
                      "total_license_records": sum(counts.values()),
                      "report_csv_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
