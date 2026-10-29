# Ford GoBike — Communicate Data Findings

Two completed Udacity notebooks investigate when February 2019 Ford GoBike trips occur and how their durations differ by user type. Both notebooks contain real saved outputs; both HTML reports embed their figures.

## Deliverables

| Report | Executable notebook | HTML export |
|---|---|---|
| Part I: exploration | [Notebook](Part_I_exploration_template.ipynb) | [HTML](Part_I_exploration_template.html) |
| Part II: explanation | [Notebook](Part_II_explanatory_template.ipynb) | [HTML](Part_II_explanatory_template.html) |

GitHub displays HTML source rather than rendering a report. Download the repository and open the HTML files locally. Part II hides setup diagnostics and plotting code in its HTML only; the executable notebook retains the source and validation outputs.

The exploration has **12 figures**: five univariate, five bivariate and two multivariate. The explanatory report selects **four polished figures**, fewer than half of 12. Every exploration figure has a question and observations; the notebooks include the supplied template questions, conclusions, intent comments and reusable functions.

## Findings

- All **183,412 trips** pass the essential validity checks; there are no exact duplicates. The raw source has 14 columns, and the analytical table has nine.
- Subscriber trips account for **89.2%** of records. That is not a share of unique riders.
- Customer trips have a **13.2-minute median**, versus **8.2 minutes** for Subscriber trips.
- Calendar-adjusted Subscriber volume averages about **6,913 trips per weekday** and **3,162 per weekend day**. Customer volume averages about **712** and **704**, respectively.
- Within-group hourly profiles differ by user type and day type; one month of observational records cannot establish trip purpose, causality or annual seasonality.

Long durations remain in the analysis. Log axes make the duration tail visible; boxplots omit outlier markers without deleting those rows. Only the raw hour/duration scatter uses a disclosed, seeded 4,000-trip sample; summaries use the full valid dataset.

## Reproduce

Validated with Python 3.13.5. From the repository directory:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python run_project.py
python -m pytest -q
```

`run_project.py` executes each notebook in a new kernel, saves it, and exports its HTML. No API key, network data download or global kernel registration is needed for a normal rerun: the source snapshot is included and hash-verified. The local Jupyter kernel needs permission to open local sockets. Matplotlib and its parser dependency are constrained for compatibility with Seaborn 0.13, rather than hiding upstream deprecation warnings.

`build_notebooks.py` is an authoring helper that regenerates notebook sources and clears their outputs. It is **not** the normal reproduction command. If you deliberately edit the analysis with that helper, rerun the entire project and tests before treating the artifacts as complete.

## Data and source attribution

The dataset is the official Bay Wheels archive of February 2019 Ford GoBike trips:

`https://s3.amazonaws.com/baywheels-data/201902-fordgobike-tripdata.csv.zip`

The supplied course-hosted CSV returned HTTP 403 during acquisition. The official archive provides the same requested month and a 14-column snapshot without member age/gender fields. We do not reconstruct or infer those absent attributes. `data/raw/provenance.json` records the actual URL, UTC retrieval time, archive hash and unmodified CSV hash.

`DATA_SOURCES.md` documents variables, denominators and provider terms. Provider rights remain with the original source; no provider affiliation or endorsement is claimed. Starter notebook sections originate with the supplied Udacity assignment. Implementation and validation were developed with AI assistance; the submitting student should review and understand the work and follow applicable course disclosure rules.

## Validation and submission

The 30 tests cover preparation, exposure denominators, all 16 plot renders, chart counts, saved notebook execution, image descriptions, embedded HTML figures, export hygiene and exact raw-to-clean reconstruction. `VALIDATION.md` records the observed checks and source limitations.

The user-requested public GitHub repository is the source deliverable. The saved course directions additionally require a ZIP for local-development submissions, so a local archive is prepared separately as described in `SUBMISSION.md`. Neither publication nor archive preparation proves a course upload or grade.

The linked full rubric redirected to Udacity’s homepage, so compliance is checked against the complete supplied document, its image-based final checklist, and the starter rubric tips. No claim is made that inaccessible live rubric criteria or the submission interface were inspected.
