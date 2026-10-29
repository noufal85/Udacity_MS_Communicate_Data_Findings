"""Populate the supplied exploratory and explanatory notebook sections."""
from pathlib import Path
import json
import nbformat
import pandas as pd
from bike_analysis import prepare_trips, summarize

ROOT = Path(__file__).resolve().parent
data, audit = prepare_trips(pd.read_csv(ROOT/'data/raw/201902-fordgobike-tripdata.csv'))
s = summarize(data)


def md(text):
    return nbformat.v4.new_markdown_cell(text.strip())


def code(text, **metadata):
    return nbformat.v4.new_code_cell(text.strip(), metadata=metadata)


def chart(chart_id, family, question, observations, part='i'):
    function = 'exploratory_figure' if part == 'i' else 'explanatory_figure'
    return [md(f'### Question — {question}'),
            code(f"fig = {function}('{chart_id}', trips)\nshow_chart(fig, '{part}_{chart_id}')", chart_id=chart_id, plot_family=family, alt=question+' '+observations),
            md('**Observations.** '+observations)]


setup = '''from pathlib import Path
import json, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Image
from bike_analysis import prepare_trips, load_clean, summarize, hourly_rates
from bike_plots import exploratory_figure, explanatory_figure

ROOT = Path.cwd()
RAW = ROOT / 'data/raw'
CLEAN = ROOT / 'data/cleaned'
FIGURES = ROOT / 'figures'
EVIDENCE = ROOT / 'evidence'
for folder in (CLEAN, FIGURES, EVIDENCE):
    folder.mkdir(parents=True, exist_ok=True)

def show_chart(fig, name):
    """Embed the saved PNG explicitly so headless execution preserves visible evidence."""
    path = FIGURES / (name + '.png')
    fig.savefig(path, dpi=140, bbox_inches='tight')
    display(Image(filename=str(path)))
    plt.close(fig)

print('pandas', pd.__version__, '| NumPy', np.__version__, '| Seaborn', sns.__version__)
'''

part1 = [
    md('# Part I — When and how long do Ford GoBike trips occur?\n## by Noufal\n\n## Introduction\n\nThis exploration studies all recorded Ford GoBike trips beginning in February 2019 in the San Francisco Bay Area. The official Bay Wheels archive supplies 183,412 trip records; rows describe trips, not unique riders.\n\nThe questions are: How are trip duration and starts distributed? How does duration vary by user type? Do time-of-day patterns differ between Subscriber and Customer trips? How do those patterns change between weekdays and weekends?'),
    md('**Source and scope.** The snapshot comes from `https://s3.amazonaws.com/baywheels-data/201902-fordgobike-tripdata.csv.zip`; the raw CSV, retrieval time and SHA-256 checksums are preserved under `data/raw/`. The course-hosted CSV link returned HTTP 403, so the official archive is used instead. This version has 14 fields and no member age/gender columns; the analysis does not infer demographics, trip purpose, unique users, demand unmet by the system, or annual seasonality.'),
    md('## Preliminary Wrangling'),
    code(setup),
    code('''# Verify the unmodified source snapshot before working on a separate analytical table.
provenance = json.loads((RAW / 'provenance.json').read_text())
raw_path = RAW / '201902-fordgobike-tripdata.csv'
assert hashlib.sha256(raw_path.read_bytes()).hexdigest() == provenance['csv_sha256']
raw = pd.read_csv(raw_path)
print('Raw dimensions:', raw.shape)
raw.info()
display(raw[['duration_sec','start_time','end_time','user_type']].head())
display(raw.isna().sum().rename('Missing source fields').to_frame())

# Essential validity checks do not discard trips for missing optional station labels.
trips, audit = prepare_trips(raw)
print('Cleaning audit:', audit)
assert audit['input_rows'] == audit['duplicate_rows_removed'] + audit['invalid_rows_removed'] + audit['output_rows']
assert trips.duration_min.gt(0).all() and trips.user_type.isin(['Subscriber','Customer']).all()
assert trips.start_date.nunique() == 28
trips.to_csv(CLEAN / 'february_2019_trips.csv', index=False)
(EVIDENCE / 'cleaning_audit.json').write_text(json.dumps(audit,indent=2)+'\\n')
summary = summarize(trips)
(EVIDENCE / 'summary.json').write_text(json.dumps(summary,indent=2)+'\\n')
display(trips.head())
print('Full-data summary:', json.dumps(summary,indent=2))'''),
    md('### What is the structure of your dataset?\n\nThe raw file contains 183,412 trips and 14 fields: duration, start/end timestamps and station coordinates/identifiers, bike identifier, user type and a program flag. The analytical table has nine fields: essential timestamps, duration in seconds/minutes, user type, start hour, ordered weekday, ordered day type and start date. There are no duplicate records or invalid essential fields in this snapshot, so all 183,412 trips remain; 197 trips have missing station names/IDs, which are not needed for this analysis.\n\n### What is/are the main feature(s) of interest in your dataset?\n\nTrip duration and the timing/volume of recorded trip starts are the main outcomes. Duration is measured in minutes, and counts always refer to trips rather than people.\n\n### What features will help support the investigation?\n\nUser type, start hour, weekday and weekday/weekend classification support comparisons. Timestamps are parsed without imposing an unprovided timezone conversion, so hour means the source local clock. Weekdays are ordered Monday–Sunday; February 2019 contains four of each weekday, 20 weekdays and eight weekend days.'),
    md('**Preparation decisions.** The reusable preparation function checks positive duration, valid and increasing timestamps, agreement of recorded duration with elapsed time to within one second, February start dates and the two observed user-type labels. It would exclude invalid essentials or exact duplicate rows with non-overlapping row accounting, but makes zero such exclusions here. Long trips are retained; logarithmic axes handle the tail instead of treating an arbitrary duration cutoff as a cleaning rule. Missing optional station metadata does not justify removing a usable trip.'),
    md('## Univariate Exploration'),
]

part1 += chart('u_duration','histogram','How is trip duration distributed?',
    f'Durations are strongly right-skewed: the median is {s["median_minutes"]:.2f} minutes, the 95th percentile is {s["p95_minutes"]:.2f} minutes, and the maximum is {s["maximum_minutes"]:.1f} minutes. Log-spaced bins and a log x-axis expose the main mass while keeping the full tail visible; 96.3% of trips last at most 30 minutes.')
part1 += chart('u_user_type','bar','Which user type accounts for most trips?',
    f'Subscriber trips account for {s["subscriber_share_percent"]:.2f}% of recorded trips (163,544 versus 19,868 Customer trips). This is a trip composition, not a population share of unique people, and the imbalance motivates normalized group comparisons later.')
part1 += chart('u_hour','count','At what hours do most trips start?',
    'The largest raw hourly count occurs at 17:00 (21,864 trips), followed by 08:00 (21,056). The pooled distribution has morning/evening concentrations, but it does not show whether both user types have the same pattern.')
part1 += chart('u_weekday','count','How does recorded volume vary by weekday?',
    'Thursday has the most trips (35,197), while Saturday has the fewest (15,405). Each weekday occurs four times in February 2019, so these weekday totals have equal calendar exposure; they still combine two differently sized user groups.')
part1 += chart('u_day_type','bar','How do raw weekday and weekend totals compare?',
    'There are 152,484 weekday trips and 30,928 weekend trips, but the month contains 20 weekdays versus eight weekend days. The raw totals alone therefore overstate a typical-day contrast; later comparisons divide by the appropriate calendar-day count.')
part1 += [md('### Discuss the distributions and transformations\n\nDuration has a long right tail; a log-scale histogram retains long trips without allowing the central mass to collapse into one narrow band. User type is imbalanced, and hourly starts concentrate around 08:00 and 17:00.\n\n### Were there unusual distributions or changes to tidy the data?\n\nDuration units were converted from seconds to minutes, dates were parsed, and calendar features were derived with ordered categories. No duration outlier was deleted, no missing station label was guessed, and no demographic category was created. Calendar exposure, not a data-quality defect, explains part of the weekday/weekend total difference.'), md('## Bivariate Exploration')]

part1 += chart('b_scatter','scatter','Does start hour alone explain duration?',
    'The seeded sample of 4,000 trips shows broad duration dispersion at similar start hours, with a dense short-trip band and a sparse long-duration tail. Alpha blending and a log y-axis reduce overplotting, but this sampled diagnostic does not replace the complete-data summaries or establish an hour-to-duration causal effect.')
part1 += chart('b_box','box','How does typical duration differ by user type?',
    f'Customer trips have a median duration of {s["customer_median_minutes"]:.1f} minutes versus {s["subscriber_median_minutes"]:.2f} minutes for Subscriber trips. The boxplots summarize all rows; markers beyond the 1.5×IQR whiskers are omitted from this display only, with the full tail already examined above.')
part1 += chart('b_heatmap','heatmap','When are average weekday/hour volumes largest?',
    'The calendar-adjusted heatmap highlights morning and late-afternoon concentrations on working weekdays, while weekend starts concentrate more around daytime hours. Each cell is the number of trips at that hour divided by the four occurrences of its weekday, not a probability of riding or a count of unique riders.')
part1 += chart('b_cluster','clustered_bar','Does the weekday pattern differ by user type?',
    'Subscriber trips dominate absolute daily volume and show a larger weekday–weekend contrast. Customer daily volumes are much smaller, so a common absolute y-axis is useful for scale but insufficient for comparing within-group hourly shapes; the multivariate section addresses that limitation.')
part1 += chart('b_ecdf','ecdf','Is the duration difference visible across the full distributions?',
    'The complete-data ECDF places the Customer distribution to the right of the Subscriber distribution across much of the central range, consistent with the longer Customer median. Both retain long tails; logarithmic duration coordinates preserve positive values and avoid discarding extremes.')
part1 += [md('### How did the features of interest vary with other features?\n\nDuration differs by user type, and starts vary with hour and weekday. The same pooled hourly profile can hide differences between user groups, while unequal weekday/weekend exposure can distort raw-count comparisons.\n\n### Were there relationships between supporting features?\n\nThe relative Subscriber/Customer mix varies across weekdays, and time-of-day patterns differ between weekdays and weekends. These associations motivate conditioning on both user type and day type, with normalized shares to separate timing from group size.'), md('## Multivariate Exploration')]
part1 += chart('m_facet','facet','How do hourly profiles change jointly with user type and day type?',
    'Each panel conditions on user type and each line on day type; every line sums to 100% over hours, so the y-axis compares timing rather than absolute traffic. Subscriber peaks shift from 08:00 on weekdays to 14:00 on weekends, while Customer peaks shift from 17:00 to 13:00; this is consistent with differing schedules, not recorded proof of trip purpose.')
part1 += chart('m_encoded_scatter','multi_encoding_scatter','How does median duration vary by hour, user type and day type?',
    'Color identifies user type and marker shape identifies day type, exposing conditional medians that a pooled duration plot hides. Customer medians are 16.05 minutes on weekends and 12.40 on weekdays, while Subscriber medians remain close to 8.1 minutes; individual hour/user/day cells range from five to 18,558 trips, so sparse early-hour medians should not be overinterpreted.')
part1 += [md('### Did features strengthen each other when conditioning jointly?\n\nYes: conditioning on user type and day type separates changes in hourly shape from large differences in group volume. Calendar-adjusted daily Subscriber volume is about 6,913 trips on weekdays versus 3,162 on weekend days, whereas Customer volume is about 712 versus 704.\n\n### Were there surprising interactions?\n\nThe Customer weekend duration shift contrasts with the nearly unchanged Subscriber medians. Sparse early-hour groups can produce unstable medians, and one month of observational trip records cannot distinguish user preference, pricing, weather, network supply or trip purpose. The evidence supports conditional description, not a behavioral or causal attribution.'),
    md('## Conclusions\n\n- Subscriber trips make up 89.2% of the 183,412 recorded trips; this is not a unique-rider statistic.\n- Typical Customer trips are longer: 13.2 minutes versus 8.2 minutes for Subscriber trips.\n- Within-group weekday timing differs, and both groups shift toward daytime peaks on weekends.\n- Subscriber weekday volume remains much higher after calendar-day adjustment; Customer daily volumes are similar across day types.\n\nThe exploration progressed from single-variable distributions to group comparisons and multivariate conditioning. I retained the full duration range, separated counts from exposure-normalized rates and normalized timing shares, and used a seeded sample only for the overplotted raw scatter. Further work would compare additional months and check station availability or weather before discussing seasonality or explanations for trip patterns; this month alone does not identify those effects.')]

part2 = [
    md('# Part II — Different trip rhythms within one bike-share system\n## by Noufal'),
    md('## Investigation Overview\n\nThis report communicates four descriptive findings from the preceding Ford GoBike exploration. Its audience is a bike-share service analyst comparing recorded trip patterns, not estimating causal effects or counting unique customers.\n\n## Dataset Overview and Executive Summary\n\nThe official Bay Wheels February 2019 archive contains 183,412 trips and 14 raw fields. All trips pass the essential validity checks; the nine-column analytical dataset preserves long durations and does not remove trips for missing optional station labels. Source URL, retrieval timestamp and checksums are included with the raw data.\n\nFour questions organize the report:\n1. Who accounts for most recorded trips? Subscriber trips represent 89.2% of the total.\n2. Do weekday timing patterns differ after accounting for group size? Within-group profiles retain distinct timing, with Subscriber morning/evening peaks.\n3. How does typical duration differ? Customer trips have a 13.2-minute median versus 8.2 minutes for Subscriber trips.\n4. Is the weekday–weekend volume gap merely unequal calendar exposure? Subscriber daily volume still falls substantially on weekends; Customer daily volume is similar.\n\nThese are the same findings summarized in Part I. Four polished figures are selected from 12 exploratory figures, fewer than half the exploratory count.'),
    code(setup,tags=['report_setup']),
    code('''# Load the same stored analytical table rather than applying a different cleaning rule.
trips = load_clean(CLEAN / 'february_2019_trips.csv')
saved_summary = json.loads((EVIDENCE / 'summary.json').read_text())
summary = summarize(trips)
assert summary == saved_summary
print('Verified shared analysis population:', len(trips), 'trips; February 2019')
print('Median durations (minutes):', summary['subscriber_median_minutes'], summary['customer_median_minutes'])''',tags=['report_setup']),
]
part2 += chart('e_composition','bar','Who accounts for most recorded trips?',
    'Subscriber trips account for 89.2% of February records, versus 10.8% for Customer trips. Percentages and trip counts are annotated to establish the scale imbalance; they describe trip categories rather than distinct people.', part='ii')
part2 += chart('e_weekday_profile','line','Do weekday timing patterns differ after adjusting for group size?',
    'Each line divides hourly weekday trips by all weekday trips within its user type, removing the dominance of the larger Subscriber group from the timing comparison. Subscriber trips show pronounced morning and late-afternoon concentrations; Customer trips peak at 17:00, but trip purpose is not recorded.', part='ii')
part2 += chart('e_duration','box','How does typical duration differ by user type?',
    'The Customer median is 13.2 minutes, compared with 8.2 minutes for Subscriber trips. Log coordinates make the central distributions readable; omitted outlier markers are a display choice only, and every valid trip contributes to the boxes and medians.', part='ii')
part2 += chart('e_calendar_rates','clustered_bar','Does the weekday–weekend volume difference survive exposure adjustment?',
    'Dividing by 20 weekdays and eight weekend days yields about 6,913 versus 3,162 daily Subscriber trips, compared with about 712 versus 704 Customer trips. The larger Subscriber gap is therefore not solely an artifact of more weekdays in the month; these remain recorded trip volumes, not per-person usage rates.', part='ii')
part2 += [md('## Takeaways and limits\n\nUser-type composition, trip duration and temporal profiles tell complementary stories; no single pooled plot captures all three. All figures use the same valid trip population, consistent colors and explicit denominators. One month cannot establish seasonal demand, unique-rider behavior, causality or the purpose of any trip; a broader study should add time periods and contextual service data.\n\nThe accompanying HTML is the presentation report, with plotting code hidden and all figures embedded; the notebook retains the executable source for review.')]

for name,cells in [('Part_I_exploration_template',part1),('Part_II_explanatory_template',part2)]:
    path=ROOT/(name+'.ipynb')
    notebook=nbformat.read(path,4)
    notebook.cells=cells
    notebook.nbformat_minor=5
    notebook.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
    nbformat.write(notebook,path)

manifest={}
for name,cells in [('Part I',part1),('Part II',part2)]:
    manifest[name]=[{'chart_id':c.metadata['chart_id'],'family':c.metadata['plot_family']} for c in cells if c.metadata.get('chart_id')]
(ROOT/'evidence').mkdir(exist_ok=True)
(ROOT/'evidence/plot_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built both notebooks:',len(part1),'and',len(part2),'cells')
