"""Trip-level preparation and calendar-exposure summaries for February 2019."""
import numpy as np
import pandas as pd

USER_TYPES = ['Subscriber', 'Customer']
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAY_TYPES = ['Weekday', 'Weekend']


def prepare_trips(raw):
    """Keep valid essential trip fields; missing station labels do not remove trips."""
    frame = raw.drop_duplicates().copy()
    duplicates = len(raw) - len(frame)
    frame['start_time'] = pd.to_datetime(frame.start_time, errors='coerce')
    frame['end_time'] = pd.to_datetime(frame.end_time, errors='coerce')
    frame['duration_sec'] = pd.to_numeric(frame.duration_sec, errors='coerce')
    elapsed = (frame.end_time - frame.start_time).dt.total_seconds()
    # Recorded integer seconds may differ from timestamp precision by less than one second.
    valid = (frame.duration_sec.gt(0) & frame.start_time.notna() & frame.end_time.notna()
             & elapsed.gt(0) & elapsed.sub(frame.duration_sec).abs().le(1)
             & frame.user_type.isin(USER_TYPES)
             & frame.start_time.ge('2019-02-01') & frame.start_time.lt('2019-03-01'))
    result = frame.loc[valid, ['start_time', 'end_time', 'duration_sec', 'user_type']].copy()
    result['duration_min'] = result.duration_sec / 60
    result['start_hour'] = result.start_time.dt.hour
    result['start_weekday'] = pd.Categorical(result.start_time.dt.day_name(), WEEKDAYS, ordered=True)
    result['day_type'] = pd.Categorical(np.where(result.start_time.dt.dayofweek.lt(5), 'Weekday', 'Weekend'), DAY_TYPES, ordered=True)
    result['start_date'] = result.start_time.dt.normalize()
    audit = {'input_rows': len(raw), 'duplicate_rows_removed': duplicates,
             'invalid_rows_removed': int((~valid).sum()), 'output_rows': len(result)}
    return result.reset_index(drop=True), audit


def load_clean(path):
    frame = pd.read_csv(path, parse_dates=['start_time', 'end_time', 'start_date'],
                        dtype={'start_hour': 'int32'}, float_precision='round_trip')
    frame['start_weekday'] = pd.Categorical(frame.start_weekday, WEEKDAYS, ordered=True)
    frame['day_type'] = pd.Categorical(frame.day_type, DAY_TYPES, ordered=True)
    return frame


def hourly_rates(trips):
    """Include zero cells and use all calendar days, not days observed within a user group."""
    keys = ['user_type', 'day_type', 'start_hour']
    index = pd.MultiIndex.from_product([USER_TYPES, DAY_TYPES, range(24)], names=keys)
    counts = trips.groupby(keys, observed=True).size().reindex(index, fill_value=0).rename('trips').reset_index()
    counts['calendar_days'] = counts.day_type.map({'Weekday': 20, 'Weekend': 8})
    counts['trips_per_day'] = counts.trips / counts.calendar_days
    totals = counts.groupby(['user_type', 'day_type']).trips.transform('sum')
    counts['within_type_day_percent'] = counts.trips.div(totals.replace(0, np.nan)).fillna(0) * 100
    return counts


def weekday_rates(trips):
    index = pd.MultiIndex.from_product([USER_TYPES, WEEKDAYS], names=['user_type', 'start_weekday'])
    counts = trips.groupby(['user_type', 'start_weekday'], observed=True).size().reindex(index, fill_value=0).rename('trips').reset_index()
    counts['calendar_days'] = 4
    counts['trips_per_day'] = counts.trips / counts.calendar_days
    return counts


def summarize(trips):
    medians = trips.groupby('user_type', observed=True).duration_min.median()
    rates = hourly_rates(trips)
    result = {'trips': len(trips), 'subscriber_share_percent': float(trips.user_type.eq('Subscriber').mean() * 100),
              'subscriber_median_minutes': float(medians.get('Subscriber', np.nan)),
              'customer_median_minutes': float(medians.get('Customer', np.nan)),
              'median_minutes': float(trips.duration_min.median()),
              'p95_minutes': float(trips.duration_min.quantile(.95)),
              'maximum_minutes': float(trips.duration_min.max())}
    for user in USER_TYPES:
        for day in DAY_TYPES:
            subset = rates.loc[rates.user_type.eq(user) & rates.day_type.eq(day)]
            result[f'{user.lower()}_{day.lower()}_peak_hour'] = int(subset.loc[subset.trips.idxmax(), 'start_hour'])
            result[f'{user.lower()}_{day.lower()}_trips_per_day'] = float(subset.trips_per_day.sum())
    return result
