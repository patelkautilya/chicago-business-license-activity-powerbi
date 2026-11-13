"""Build a fixed 2024-2025 Chicago business-license issuance panel.

Uses only Python's standard library. Source: City of Chicago, dataset r5kz-chrr.
"""
from __future__ import annotations

import csv
import hashlib
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError


ROOT = Path(__file__).resolve().parent
API = "https://data.cityofchicago.org/resource/r5kz-chrr.json"
META = "https://data.cityofchicago.org/api/views/r5kz-chrr.json"
WHERE = "date_issued >= '2024-01-01T00:00:00' AND date_issued < '2026-01-01T00:00:00'"
FIELDS = ["id", "license_id", "date_issued", "application_type", "license_description",
          "community_area_name", "ward", "application_created_date", "license_status"]
OUTPUT = ROOT / "chicago_business_licenses_issued_2024_2025.csv"


def get_json(url: str, params: dict | None = None):
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={"User-Agent": "analyst-portfolio-data-validation/1.0"})
    for attempt in range(5):
        try:
            with urlopen(req, timeout=90) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 4:
                raise
            time.sleep(2 ** attempt)


def date_part(value: str) -> str:
    return value[:10] if value else ""


def main() -> None:
    metadata = get_json(META)
    expected = int(get_json(API, {"$select": "count(*) as n", "$where": WHERE})[0]["n"])
    rows: list[dict] = []
    offset = 0
    while offset < expected:
        batch = get_json(API, {"$select": ",".join(FIELDS), "$where": WHERE,
                               "$order": "license_id", "$limit": 5000, "$offset": offset})
        if not batch:
            raise ValueError(f"Pagination stopped at {offset} of {expected}")
        rows.extend(batch)
        offset += len(batch)
        print(f"Downloaded {offset:,} / {expected:,}")
    if len(rows) != expected:
        raise ValueError(f"Expected {expected:,} rows, received {len(rows):,}")
    ids = [r.get("id", "") for r in rows]
    license_ids = [r.get("license_id", "") for r in rows]
    if len(set(license_ids)) != len(license_ids) or "" in license_ids:
        raise ValueError("Missing or duplicate LICENSE ID values")

    years = Counter()
    months = Counter()
    types = Counter()
    statuses = Counter()
    missing = Counter()
    elapsed = []
    for row in rows:
        issued = date_part(row.get("date_issued", ""))
        if not issued or issued < "2024-01-01" or issued >= "2026-01-01":
            raise ValueError(f"Unexpected issue date: {issued}")
        year, month = issued[:4], issued[:7]
        years[year] += 1
        months[month] += 1
        types[row.get("application_type") or "(missing)"] += 1
        statuses[row.get("license_status") or "(missing)"] += 1
        for field in FIELDS:
            if not row.get(field):
                missing[field] += 1
        created = date_part(row.get("application_created_date", ""))
        if created:
            days = (datetime.fromisoformat(issued) - datetime.fromisoformat(created)).days
            elapsed.append(days)
        row["issue_month"] = month
        row["issue_year"] = year
        row["application_created_date"] = created
        row["date_issued"] = issued

    # Separate aggregate query guards against a partial or shifted local extract.
    remote_types = get_json(API, {"$select": "application_type,count(*) as n", "$where": WHERE,
                                  "$group": "application_type", "$order": "application_type"})
    remote_counts = {r.get("application_type") or "(missing)": int(r["n"]) for r in remote_types}
    if remote_counts != dict(types):
        raise ValueError("Application-type totals disagree with independent source aggregation")

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS + ["issue_month", "issue_year"])
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in writer.fieldnames})
    sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    summary = {
        "source": "https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr",
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_rows_updated_at_unix": metadata.get("rowsUpdatedAt"),
        "issue_date_start": "2024-01-01", "issue_date_end": "2025-12-31",
        "records": len(rows), "unique_license_ids": len(set(license_ids)),
        "unique_id_field_values": len(set(ids)), "duplicate_id_field_rows": len(ids) - len(set(ids)),
        "years": dict(sorted(years.items())), "months": dict(sorted(months.items())),
        "application_types": dict(types.most_common()), "license_statuses": dict(statuses.most_common()),
        "missing_fields": dict(missing),
        "application_to_issue_days": {"nonmissing": len(elapsed), "negative": sum(x < 0 for x in elapsed),
                                      "max": max(elapsed) if elapsed else None},
        "independent_application_type_counts_match": True,
        "curated_csv_sha256": sha,
    }
    (ROOT / "validation_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
