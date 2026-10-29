# Data source and analytical definitions

Source: official Bay Wheels/Ford GoBike system-data archive, February 2019, containing 183,412 trips beginning during that month. The downloaded CSV is 33,995,020 bytes and is retained unchanged under `data/raw/`. Exact acquisition details and checksums are in `provenance.json` in that directory.

- Provider data page: https://www.lyft.com/bikes/bay-wheels/system-data
- Provider data terms: https://baywheels.com/data-license-agreement
- Actual download: https://s3.amazonaws.com/baywheels-data/201902-fordgobike-tripdata.csv.zip

The provider describes a limited license for data research and analysis with conditions on reuse and redistribution. This repository supplies the source snapshot to support this non-commercial analytical project, not as a stand-alone data product; consult and comply with the provider’s terms before other reuse. No affiliation, endorsement or access to private rider identities is claimed.

## Analytical table

| Variable | Type | Meaning and units |
|---|---|---|
| `start_time` | datetime | Trip start, source local clock; no invented timezone conversion |
| `end_time` | datetime | Trip end, source local clock |
| `duration_sec` | integer | Source recorded duration, seconds |
| `user_type` | string | Source trip category: Subscriber or Customer |
| `duration_min` | float | Recorded duration divided by 60, minutes |
| `start_hour` | integer | Source-clock hour of start, 0–23 |
| `start_weekday` | ordered category | Monday through Sunday |
| `day_type` | ordered category | Weekday or Weekend |
| `start_date` | datetime | Calendar date of trip start, normalized to midnight |

A row is a trip. Bike IDs are not rider IDs, and there is no unique-rider count in the analysis. Derived calendar features are explanatory variables, not additional source defects or evidence of trip purpose.

## Preparation and denominators

- Exact duplicate records and invalid essential fields would be excluded with non-overlapping accounting. In this snapshot both exclusion counts are zero.
- Essential checks require positive duration, increasing valid timestamps, February 2019 starts, known user types and duration/timestamp agreement within one second to respect the integer-second field’s precision.
- The 197 records with missing station metadata remain because location fields are not used in these analyses. No age/gender fields are present in this official snapshot.
- February 2019 has 20 weekdays, eight weekend days and four instances of each named weekday. Rate tables include zero hour/group cells and use those full calendar denominators, not only days when a group happened to have trips.
- Hourly timing shares divide each user/day-type group by its own total and sum to 100% across its 24 hours. They are not per-person rates, and should not be confused with absolute trip volumes.
- Full-data statistics retain the long duration tail. Only the raw hour-duration scatter is sampled, using a fixed seed; it is explicitly labeled.

The analysis is deliberately specific to this month. Reusing the helpers for another month requires changing and testing the calendar definitions, not merely replacing the CSV.
