# Findings and limits

## Validation

The fixed `date_issued` window has **64,377 records**, matching the official Socrata count query. All `license_id` values are distinct; the source's separate `id` field has three duplicated values, each attached to different `license_id` records. An independent Socrata aggregation by application type matches the downloaded extract. The compact 20,615-row report table sums to the same 64,377 records. Hashes and the source-update timestamp are recorded in `validation_summary.json` and the report-table build output.

## Observations

1. **Most records are renewals.** `RENEW` accounts for 49,235 records (76.48%); `ISSUE` accounts for 14,026 (21.79%). The remaining 1,116 are change applications (`C_LOC`, `C_SBA`, `C_EXPA`, `C_CAPA`). The City's field definitions distinguish initial issuance from subsequent renewals.
2. **Total records rose while initial issues were nearly flat.** All types combined increased from 31,441 in 2024 to 32,936 in 2025 (**4.75%**). `ISSUE` moved from 7,036 to 6,990 (**−0.65%**); `RENEW` rose from 23,837 to 25,398 (**6.55%**). These are counts by issue date, not business formation or survival rates.
3. **Geographic coverage is incomplete.** The community-area name is missing on 5,679 records (8.82%); ward is missing on 5,606. Any map or community comparison must show the missing category and must not be framed as an exposure-adjusted rate.
4. **The largest license class is Limited Business License.** It has 18,638 issued records in the report window, followed by Retail Food Establishment (12,012) and Regulated Business License (8,920). These are license-class records, not unique firms.
5. **The missing community-area bucket leads the ranked view.** Among named areas, Near North Side has 5,172 records, followed by Loop (4,418) and Near West Side (3,571). The rankings count licenses and cannot establish relative business intensity without a denominator.

## Interpretation limits

- License records are not unique businesses, operating locations, or jobs. A firm can have multiple license classes, sites, renewals, or change applications. `ISSUE` identifies an initial license application record, not necessarily a newly opened enterprise.
- The source is revised daily. `license_status` reflects the extract's later state, so 2024 and 2025 status percentages do not have equal time at risk. This case will not treat cancellation/revocation as a comparable cohort outcome.
- `application_created_date` is missing on 49,323 records. It is present for 13,940 of 14,026 `ISSUE` records, but extreme multi-year lags occur. Processing-time analysis would need narrower validation and should not be generalized to all records.
- Monthly totals are affected by differing business days, holidays, and licensing cycles. The data alone do not explain why activity changed.

Source: [Chicago Business Licenses](https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr), City of Chicago Data Portal.
