# Chicago Business License Activity | 2024–2025

An analyst case study in progress on Chicago license records with **date issued** in 2024 or 2025. The analysis separates initial `ISSUE` applications from `RENEW` and other change applications. The reproducible source and [compact Power BI table](license_activity_month_type_area_2024_2025.csv) are published; the interactive report and export are still pending.

## Question

How did the mix of issued license records vary by month, application type, license class, and community area?

## Source and reproducibility

- Official source: [City of Chicago Business Licenses](https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr), dataset `r5kz-chrr`; [Socrata API](https://data.cityofchicago.org/resource/r5kz-chrr.json). Data owner: Business Affairs and Consumer Protection. The source is updated daily, so this is an extract snapshot.
- Fixed `date_issued` window: **2024-01-01 through 2025-12-31**, inclusive. Extraction time and source-update timestamp are in `validation_summary.json`.
- Run `python build_dataset.py` with Python 3.10+ and internet access, then `python build_report_table.py`. Both use only the standard library. The first downloads a row-level extract without business names or addresses; the second aggregates to month × application type × license description × community area for Power BI.
- `license_id` is the unique record key in this extract. The source's `id` field has three duplicates across differing `license_id` values; the script checks `license_id` uniqueness and retains all 64,377 rows. The aggregate table reconciles to the row-level total.

## Validated snapshot

| Measure | Value |
|---|---:|
| License records issued in 2024–2025 | 64,377 |
| 2024 records | 31,441 |
| 2025 records | 32,936 |
| `ISSUE` (initial application) records | 14,026 |
| `RENEW` records | 49,235 |
| Other application-type records | 1,116 |
| Missing community-area name | 5,679 |

An issued license record is **not necessarily a newly opened business**. One account or location may have multiple licenses or application records. The `license_status` field is a current snapshot; it is not a status at issuance. `application_created_date` is absent for 49,323 records, mostly renewals, so a full-population processing-time KPI would be misleading. See `FINDINGS.md` and `validation_summary.json` for detail.

