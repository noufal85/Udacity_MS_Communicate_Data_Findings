"""Exploratory and presentation figures with consistent trip-level definitions."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from bike_analysis import USER_TYPES, WEEKDAYS, DAY_TYPES, hourly_rates, weekday_rates

EXPLORATORY_IDS = ['u_duration', 'u_user_type', 'u_hour', 'u_weekday', 'u_day_type',
                   'b_scatter', 'b_box', 'b_heatmap', 'b_cluster', 'b_ecdf',
                   'm_facet', 'm_encoded_scatter']
EXPLANATORY_IDS = ['e_composition', 'e_weekday_profile', 'e_duration', 'e_calendar_rates']
COLORS = {'Subscriber': '#176b87', 'Customer': '#d87436'}
DAY_COLORS = {'Weekday': '#176b87', 'Weekend': '#a24f8d'}


def exploratory_figure(chart, trips):
    """Use complete data except the explicitly seeded 4,000-trip scatter sample."""
    sns.set_theme(style='whitegrid', context='notebook')
    if chart == 'm_facet':
        rates = hourly_rates(trips)
        grid = sns.relplot(data=rates, x='start_hour', y='within_type_day_percent', col='user_type',
                           col_order=USER_TYPES, hue='day_type', hue_order=DAY_TYPES, palette=DAY_COLORS,
                           kind='line', estimator=None, errorbar=None, height=3.6, aspect=1.15)
        grid.set_axis_labels('Start hour (local clock)', 'Trips within user/day-type group (%)')
        grid.set_titles('{col_name}')
        grid.set(xlim=(-.5, 23.5), xticks=range(0, 24, 4))
        grid.figure.subplots_adjust(top=.78)
        grid.figure.suptitle('Hourly profiles by user type and day type')
        grid._legend.set_title('Day type')
        return grid.figure

    fig, ax = plt.subplots(figsize=(9, 5))
    if chart == 'u_duration':
        bins = np.geomspace(trips.duration_min.min(), trips.duration_min.max() * 1.001, 45)
        sns.histplot(data=trips, x='duration_min', bins=bins, color=COLORS['Subscriber'], ax=ax)
        ax.set_xscale('log')
        ax.set(title='Trip duration: full range in log-spaced bins', xlabel='Duration (minutes, log scale)', ylabel='Trips')
    elif chart == 'u_user_type':
        counts = trips.user_type.value_counts().reindex(USER_TYPES, fill_value=0)
        ax.bar(counts.index, counts.values, color=[COLORS[u] for u in USER_TYPES])
        ax.set(title='Recorded trips by user type', xlabel='User type', ylabel='Trips')
    elif chart == 'u_hour':
        counts = trips.start_hour.value_counts().reindex(range(24), fill_value=0)
        ax.bar(counts.index, counts.values, color=COLORS['Subscriber'])
        ax.set(title='Trip starts across the local-clock day', xlabel='Start hour (local clock)', ylabel='Trips', xticks=range(0,24,2))
    elif chart == 'u_weekday':
        counts = trips.start_weekday.value_counts().reindex(WEEKDAYS, fill_value=0)
        ax.bar(counts.index, counts.values, color=COLORS['Subscriber'])
        ax.set(title='Trips by weekday: four of each weekday in this month', xlabel='Start weekday', ylabel='Trips')
        ax.tick_params(axis='x', rotation=20)
    elif chart == 'u_day_type':
        counts = trips.day_type.value_counts().reindex(DAY_TYPES, fill_value=0)
        ax.bar(counts.index, counts.values, color=[DAY_COLORS[d] for d in DAY_TYPES])
        ax.set(title='Raw trip totals: 20 weekdays versus 8 weekend days', xlabel='Day type', ylabel='Trips (not exposure-normalized)')
    elif chart == 'b_scatter':
        sample = trips.sample(min(4000, len(trips)), random_state=42)
        ax.scatter(sample.start_hour, sample.duration_min, s=7, alpha=.15, color=COLORS['Subscriber'])
        ax.set_yscale('log')
        ax.set(title=f'Hour and duration: seeded sample of {len(sample):,} trips', xlabel='Start hour (local clock)', ylabel='Duration (minutes, log scale)', xticks=range(0,24,2))
    elif chart == 'b_box':
        sns.boxplot(data=trips, x='user_type', y='duration_min', order=USER_TYPES,
                    color='#b9d7e2', showfliers=False, ax=ax)
        ax.set_yscale('log')
        ax.set(title='Duration by user type: outlier markers omitted, rows retained', xlabel='User type', ylabel='Duration (minutes, log scale)')
    elif chart == 'b_heatmap':
        counts = trips.groupby(['start_weekday', 'start_hour'], observed=True).size().unstack(fill_value=0)
        counts = counts.reindex(index=WEEKDAYS, columns=range(24), fill_value=0) / 4
        sns.heatmap(counts, cmap='YlGnBu', ax=ax, cbar_kws={'label': 'Mean trips per occurrence of weekday'})
        ax.set(title='Mean trip starts by weekday and hour', xlabel='Start hour (local clock)', ylabel='Start weekday')
    elif chart == 'b_cluster':
        sns.barplot(data=weekday_rates(trips), x='start_weekday', y='trips_per_day', hue='user_type',
                    order=WEEKDAYS, hue_order=USER_TYPES, palette=COLORS, errorbar=None, ax=ax)
        ax.set(title='Daily trip rate by weekday and user type', xlabel='Start weekday', ylabel='Mean trips per occurrence of weekday')
        ax.legend(title='User type'); ax.tick_params(axis='x', rotation=20)
    elif chart == 'b_ecdf':
        sns.ecdfplot(data=trips, x='duration_min', hue='user_type', hue_order=USER_TYPES, palette=COLORS, ax=ax)
        ax.set_xscale('log')
        ax.set(title='Cumulative duration distributions use every valid trip', xlabel='Duration (minutes, log scale)', ylabel='Cumulative proportion of trips')
    elif chart == 'm_encoded_scatter':
        medians = trips.groupby(['user_type', 'day_type', 'start_hour'], observed=True).duration_min.median().reset_index()
        sns.scatterplot(data=medians, x='start_hour', y='duration_min', hue='user_type', hue_order=USER_TYPES,
                        style='day_type', style_order=DAY_TYPES, palette=COLORS, s=65, alpha=.8, ax=ax)
        ax.set(title='Median duration by hour, user type and day type', xlabel='Start hour (local clock)', ylabel='Median duration (minutes)', xticks=range(0,24,2))
        ax.legend(loc='upper right', fontsize=8)
    else:
        raise ValueError(f'Unknown exploratory chart: {chart}')
    fig.tight_layout()
    return fig


def explanatory_figure(chart, trips):
    """Recast the explored results with consistent units and restrained annotations."""
    sns.set_theme(style='whitegrid', context='notebook', font_scale=1.05)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    if chart == 'e_composition':
        counts = trips.user_type.value_counts().reindex(USER_TYPES, fill_value=0)
        shares = counts / len(trips) * 100
        bars = ax.bar(USER_TYPES, shares, color=[COLORS[u] for u in USER_TYPES], width=.6)
        for bar, count, share in zip(bars, counts, shares):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, f'{share:.1f}%\n{count:,} trips', ha='center')
        ax.set(title=f'Subscribers account for {shares.iloc[0]:.1f}% of February trips', xlabel='User type', ylabel='Share of recorded trips (%)', ylim=(0,110))
        ax.set_yticks(range(0,101,20))
    elif chart == 'e_weekday_profile':
        rates = hourly_rates(trips).query("day_type == 'Weekday'")
        sns.lineplot(data=rates, x='start_hour', y='within_type_day_percent', hue='user_type',
                     hue_order=USER_TYPES, palette=COLORS, estimator=None, errorbar=None, marker='o', ax=ax)
        ax.set(title='Weekday timing differs even after adjusting for group size', xlabel='Start hour (local clock)', ylabel='Share of each user type’s weekday trips (%)', xticks=range(0,24,2), xlim=(-.5,23.5))
        ax.legend(title='User type')
    elif chart == 'e_duration':
        sns.boxplot(data=trips, x='user_type', y='duration_min', hue='user_type', order=USER_TYPES,
                    hue_order=USER_TYPES, palette=COLORS, legend=False, showfliers=False, width=.5, ax=ax)
        ax.set_yscale('log')
        for index, user in enumerate(USER_TYPES):
            median = trips.loc[trips.user_type.eq(user), 'duration_min'].median()
            ax.text(index+.3, median, f'{median:.1f} min\nmedian', va='center', fontsize=10)
        ax.set(title='Customer trips have a longer typical duration', xlabel='User type', ylabel='Duration (minutes, log scale)')
        fig.text(.5,.015,'Boxes: middle 50%; whiskers: 1.5×IQR. Outlier markers omitted, not removed from summaries.', ha='center', fontsize=9)
    elif chart == 'e_calendar_rates':
        rates = hourly_rates(trips).groupby(['user_type','day_type'], sort=False).trips_per_day.sum().reset_index()
        sns.barplot(data=rates, x='user_type', y='trips_per_day', hue='day_type', order=USER_TYPES,
                    hue_order=DAY_TYPES, palette=DAY_COLORS, errorbar=None, ax=ax)
        for container in ax.containers:
            ax.bar_label(container, fmt='%.0f', padding=3, fontsize=9)
        ax.set(title='Daily volume: a larger weekday–weekend gap for Subscriber trips', xlabel='User type', ylabel='Mean recorded trips per calendar day')
        ax.legend(title='Day type (20 weekdays; 8 weekend days)')
        ax.margins(y=.18)
    else:
        raise ValueError(f'Unknown explanatory chart: {chart}')
    sns.despine(ax=ax)
    fig.tight_layout(rect=(0,.045,1,1))
    return fig
