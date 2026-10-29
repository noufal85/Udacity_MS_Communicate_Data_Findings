import pandas as pd
import pytest
from datetime import datetime, timedelta

from bike_analysis import prepare_trips, hourly_rates, weekday_rates, summarize


def row(start='2019-02-01 08:00:00', duration=600, user='Subscriber'):
    timestamp = datetime.fromisoformat(start)
    return {'start_time': str(timestamp), 'end_time': str(timestamp + timedelta(seconds=600)),
            'duration_sec': duration, 'user_type': user, 'bike_id': 1, 'start_station_name': None}


def test_preparation_preserves_raw_and_optional_missing_attributes():
    raw = pd.DataFrame([row()])
    clean, audit = prepare_trips(raw)
    assert raw.start_time.dtype == object
    assert len(clean) == 1 and clean.duration_min.iloc[0] == 10
    assert clean.start_weekday.iloc[0] == 'Friday' and clean.day_type.iloc[0] == 'Weekday'
    assert audit['input_rows'] == audit['output_rows'] == 1


def test_invalid_essentials_and_duplicates_have_nonoverlapping_accounting():
    valid = row()
    bad_time = row(); bad_time['start_time'] = 'invalid'
    mismatch = row(duration=50)
    raw = pd.DataFrame([valid, valid, bad_time, mismatch, row(user='Unknown')])
    clean, audit = prepare_trips(raw)
    assert len(clean) == 1
    assert audit['duplicate_rows_removed'] == 1 and audit['invalid_rows_removed'] == 3
    assert sum([audit['duplicate_rows_removed'], audit['invalid_rows_removed'], audit['output_rows']]) == len(raw)


def test_out_of_period_trip_is_not_silently_used():
    clean, audit = prepare_trips(pd.DataFrame([row('2019-03-01 08:00:00')]))
    assert clean.empty and audit['invalid_rows_removed'] == 1


def test_calendar_exposure_is_not_observed_group_days():
    raw = pd.DataFrame([row(), row('2019-02-02 08:00:00', user='Customer')])
    trips, _ = prepare_trips(raw)
    hourly = hourly_rates(trips)
    assert len(hourly) == 96
    selected = hourly.query("user_type == 'Subscriber' and day_type == 'Weekday' and start_hour == 8").iloc[0]
    assert selected.calendar_days == 20 and selected.trips_per_day == pytest.approx(1/20)
    assert selected.within_type_day_percent == 100
    assert hourly.trips.sum() == len(trips)
    assert weekday_rates(trips).calendar_days.eq(4).all()


def test_summary_uses_trip_denominators_not_unique_riders():
    trips, _ = prepare_trips(pd.DataFrame([row(), row('2019-02-02 08:00:00', user='Customer')]))
    summary = summarize(trips)
    assert summary['trips'] == 2 and summary['subscriber_share_percent'] == 50
    assert summary['customer_median_minutes'] == summary['subscriber_median_minutes'] == 10
