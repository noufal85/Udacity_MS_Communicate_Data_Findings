import os
import tempfile
os.environ.setdefault('MPLCONFIGDIR', tempfile.gettempdir() + '/communicate-findings-mpl')
os.environ.setdefault('MPLBACKEND', 'Agg')
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import pytest

from bike_analysis import prepare_trips
from bike_plots import exploratory_figure, explanatory_figure, EXPLORATORY_IDS, EXPLANATORY_IDS


@pytest.fixture
def trips():
    rows = []
    for day in (1, 2, 3):
        for user in ('Subscriber', 'Customer'):
            for hour in (8, 12, 17):
                start = datetime(2019, 2, day, hour)
                duration = 300 + hour * 30 + (600 if user == 'Customer' else 0)
                rows.append({'start_time': str(start), 'end_time': str(start + timedelta(seconds=duration)),
                             'duration_sec': duration, 'user_type': user})
    return prepare_trips(pd.DataFrame(rows))[0]


@pytest.mark.parametrize('chart', ['u_duration', 'u_user_type', 'u_hour', 'u_weekday', 'u_day_type',
                                 'b_scatter', 'b_box', 'b_heatmap', 'b_cluster', 'b_ecdf',
                                 'm_facet', 'm_encoded_scatter'])
def test_exploratory_charts_render_with_labeled_axes(chart, trips, tmp_path):
    fig = exploratory_figure(chart, trips)
    assert any(ax.get_title() for ax in fig.axes) or fig._suptitle is not None
    assert fig.axes[0].get_xlabel() and fig.axes[0].get_ylabel()
    target = tmp_path / (chart + '.png')
    fig.savefig(target)
    assert target.stat().st_size > 1000
    plt.close(fig)


@pytest.mark.parametrize('chart', ['e_composition', 'e_weekday_profile', 'e_duration', 'e_calendar_rates'])
def test_explanatory_charts_render(chart, trips, tmp_path):
    fig = explanatory_figure(chart, trips)
    assert fig.axes[0].get_title() and fig.axes[0].get_xlabel() and fig.axes[0].get_ylabel()
    target = tmp_path / (chart + '.png')
    fig.savefig(target)
    assert target.stat().st_size > 1000
    plt.close(fig)


def test_explanatory_chart_count_is_below_half_exploration():
    assert len(EXPLORATORY_IDS) == 12
    assert 3 <= len(EXPLANATORY_IDS) <= 5
    assert len(EXPLANATORY_IDS) < len(EXPLORATORY_IDS) / 2
