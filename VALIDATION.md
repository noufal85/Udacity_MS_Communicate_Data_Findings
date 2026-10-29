# Validation and evaluator-style checklist

## Observed evidence

- Both notebooks execute from separate fresh kernels and are saved to the supplied starter filenames. Part I has 14 executed code cells and 12 embedded plots; Part II has six executed code cells and four embedded plots. No error outputs are saved.
- Both HTML reports embed every plot as a PNG data URI, include image descriptions, and have descriptive browser titles. Part II hides only setup cells and plotting source in HTML; its notebook retains all code and validation outputs.
- All 30 tests pass. They cover essential validity/duplicate accounting, preservation of optional-metadata cases, February scope, correct calendar exposure, trip denominators, all 16 chart renders, the four-versus-12 count constraint, saved evidence, HTML accessibility/export hygiene and raw-to-clean equality.
- The final CSV reconstructs from the unmodified raw snapshot with matching data and types. CSV loading preserves exact float round trips, so the two notebooks’ summaries agree without weakening a comparison tolerance.
- The official source CSV has 183,412 rows and 14 variables. All rows remain after essential checks, including long durations and missing optional station labels. The analytical table has nine variables.
- Actual figures are inspected for scales, units, tick/category order, legibility and clipping. The HTML reports are checked in a browser, including presentation setup-output removal.
- `pip check` reports no broken requirements. Compatible Matplotlib/Seaborn/parser ranges avoid deprecation noise without blanket warning suppression.

## Available-rubric audit

| Requirement | Evidence |
|---|---|
| Introduction, source, questions and preliminary wrangling | Part I opening; raw hash, schema, missing-field preview, cleaning audit and selected-feature explanation |
| Question–Visualization–Observations framework | Every exploratory plot has an adjacent question and observations; artifact regression checks those associations |
| Histogram and bar/count plots | Five univariate figures covering duration, user type, hour, weekday and day type |
| Scatter, box, heatmap/clustered bar | Five bivariate figures include all those families plus a full-data ECDF |
| Facet and multivariate encodings | Two multivariate figures condition on user/day type, with shared percentage scales or color/marker encodings |
| Template questions, conclusions and reflection | All supplied section questions are answered; no guide notes or placeholders remain |
| Reusable code, intent comments and docstrings | Analysis/plot modules, shared figure helper and documented notebook decisions |
| At least three polished explanatory plots, fewer than half exploration | Four explanatory versus 12 exploratory; exact output and manifest checks |
| Overview, executive summary and aligned key insights | Four stated questions and findings agree with Part I and the stored summary |
| Notebook/HTML exports and data | Both executed `.ipynb`/HTML pairs, embedded figures, raw/clean CSVs, provenance and dependencies |
| Public source and local compressed artifact | Exact remote and ZIP revision are verified at the final handoff; neither is an upload confirmation |

## Corrections exercised during validation

The first raw-to-clean artifact check caught integer-width drift, and cross-notebook execution caught a tiny CSV float-parsing difference. The typed round-trip loader corrects both while preserving strict comparisons. Notebook schema metadata was updated for generated cell IDs. Browser inspection prompted image descriptions, report titles and removal of runtime diagnostics from the explanatory HTML; corresponding tests failed before those corrections and now pass.

## Boundaries and limitations

The linked full rubric did not expose criteria and redirected to the public homepage in the browser. The complete saved document, rendered image checklist and supplied starter tips form the available contract; no review of hidden live rubric criteria is claimed. One-month trip records do not identify unique riders, trip purpose, seasonality, unmet demand or causal effects. No external Udacity grade or submission confirmation is asserted.

The final clean-copy review reruns the tests and notebook/export workflow using the validated interpreter. This verifies the committed artifacts and reproduction path, not an independently provisioned operating system or every possible dependency resolver. Dependency pins are not a full transitive/hash lock.
