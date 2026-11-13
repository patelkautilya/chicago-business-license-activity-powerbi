# Chicago Business License Activity | 2024–2025

An analyst case study on Chicago license records with **date issued** in 2024 or 2025. The analysis separates initial `ISSUE` applications from `RENEW` and other change applications. The reproducible source, [compact Power BI table](license_activity_month_type_area_2024_2025.csv), and [two-page report preview](previews/chicago_business_license_activity_preview.pdf) are available here.

## Dashboard

- [Interactive Power BI report](https://app.powerbi.com/groups/e6426da3-9b36-4519-acf1-2434daa552ae/reports/a36c17fc-fb49-445b-8e44-dc446cfacf12/19d788469b7aae008dc1?experience=power-bi) — available to accounts with access to the Power BI workspace; the public preview is accessible without sign-in.
- [Activity Overview](previews/activity_overview.png) — total, initial-issue, and renewal KPI cards; monthly trends; application-type mix; year and application-type slicers.
- [License & Community Mix](previews/license_community_mix.png) — ranked top-ten license classes and community areas, with page filters for year and application type. The missing community category is retained.
- [Two-page PDF preview](previews/chicago_business_license_activity_preview.pdf). This PDF was assembled from Power BI's image-based PowerPoint export because direct PDF export was unavailable in the workspace. It is a static preview; use the Power BI report for interaction.

The report sums `license_records` from the grouped table. Its KPI cards abbreviate values to thousands; exact counts are in the validated snapshot below. The second page supports drill-through by application type from a category on the overview page, as well as visual selection and page filtering in Power BI. Public access to the live report is not enabled.

## Question

How did the mix of issued license records vary by month, application type, license class, and community area?

## Source and reproducibility

- Official source: [City of Chicago Business Licenses](https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr), dataset `r5kz-chrr`; [Socrata API](https://data.cityofchicago.org/resource/r5kz-chrr.json). Data owner: Business Affairs and Consumer Protection. The source is updated daily, so this is an extract snapshot.
- Fixed `date_issued` window: **2024-01-01 through 2025-12-31**, inclusive. Extraction time and source-update timestamp are in `validation_summary.json`.
- Run `python build_dataset.py` with Python 3.10+ and internet access, then `python build_report_table.py`. Both use only the standard library. The first downloads a row-level extract without business names or addresses; the second aggregates to month × application type × license description × community area for Power BI. `build_preview_pdf.py` rebuilds the static PDF from the two exported PNGs with `reportlab`.
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
