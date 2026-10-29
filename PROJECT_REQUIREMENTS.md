# Communicate Data Findings requirements

## Source register

| Source | Authority and intake | Status |
|---|---|---|
| `../Intro.docx` | All 164 paragraphs, template directions, dataset links and 13 rendered pages reviewed; final page contains an image-based checklist | Read in full, including checklist image |
| `../1793229402.tar.gz` | Two starter notebooks, 20 and 11 cells; all source cells reviewed | Safe archive paths; checkpoints excluded |
| Linked Udacity rubric 5115 | Link redirects to homepage in browser; HTTP page has rubric heading but no criteria | Full live rubric unavailable; do not claim it was reviewed |
| Supplied document and starter rubric tips | Explicit plot types, counts, narrative structure, comments, exports and packaging | Controlling available requirements |
| Official Bay Wheels S3 February 2019 archive | Alternative official download after course-hosted CSV returned HTTP 403 | HTTP 200 preflight; record actual acquisition/hash |
| `https://github.com/saiogirala/Ford_Bike_Communicating_Findings` | Advisory README/layout review: source description, separate exploration and explanatory HTML/notebook | Different 2018 scope; findings are not evidence about our 2019 snapshot |
| `https://github.com/wrayz/hw-communicate-data-findings` | Advisory README/layout review: both notebook/HTML pairs, source dictionary and cleaned data | Different dataset; conventions only |
| Official Seaborn documentation via Context7 | Plot types, categorical order, facet/hue encodings | Consult before plotting implementation |

The user authorizes implementation, public GitHub publication, and a local compressed submission. The source repository will be `noufal85/Udacity_MS_Communicate_Data_Findings`. The local ZIP is an additional explicitly requested course-upload artifact, not evidence of an upload or grade. Public peers do not establish Udacity acceptance. Required source attribution and truthful AI-assistance disclosure remain separate from concise code comments explaining the analysis.

## Requirements and verification matrix

| ID | Contract | Implementation | Verification | Status |
|---|---|---|---|---|
| R1 | Use Python, NumPy, pandas, Matplotlib and Seaborn; functional code and reusable functions/comments/docstrings | Both notebooks; analysis/plot helper modules | 30 tests pass; fresh kernels; intent comments and docstrings inspected | Verified |
| R2 | Introduce dataset/source and explicit questions; preliminary wrangling and feature selection | Part I introduction/wrangling | Official raw hash, schema/missingness preview and zero-exclusion audit | Verified |
| R3 | Question–Visualization–Observations throughout exploration; answer template questions, conclusions and reflection | Part I sections | All 12 chart/question/observation associations checked; guide notes removed | Verified |
| R4 | Univariate histogram and bar/count plot | Five univariate plots | Saved PNGs, embedded notebook/HTML figures and labeled axes | Verified |
| R5 | Bivariate scatter, box, heatmap or clustered bar | Five bivariate plots including all named families | Saved manifest, render tests and visual inspection | Verified |
| R6 | Multivariate facet and plot matrix or scatter with multiple encodings | Two multivariate plots | Facets by user type, lines/markers by day type; hour and duration/share axes | Verified |
| R7 | Appropriate scales, transformations, labels, units, ticks, legends, no misleading overplotting/ordinal encodings | All plots | All PNGs inspected; browser HTML review; seeded sample disclosed | Verified |
| R8 | Part II overview/executive summary, 3–5 key questions/insights aligned with Part I | Part II | Four questions; strict shared-summary equality and direct-source cross-check | Verified |
| R9 | At least three polished explanatory plots, fewer than half Part I count | Four explanatory versus 12 exploratory figures | Exact counts in tests/manifest; four is less than six | Verified |
| R10 | Both executed notebooks and HTML or PDF exports | Two notebook/HTML pairs, preserving starter filenames | 14/14 and 6/6 code cells executed; no errors; all 16 images embedded with descriptions | Verified |
| R11 | Data and reproducible dependencies available; total below 1 GB | Raw/clean data, hashes, requirements, README | Raw-to-clean reconstruction; about 58 MB of source/artifacts excluding environment; clean-copy checks | Verified at clean-copy gate |
| R12 | Public dedicated GitHub repo with exact reviewed revision | Public `main` | Public repo/origin created and verified; exact pushed SHA checked at final handoff | Verified at publication gate |
| R13 | Local ZIP with required files; no environments, Git history or secrets | ZIP outside source repo | Integrity, safe paths, exact committed blobs and extracted-copy execution checked at handoff | Verified at packaging gate |
| R14 | Course upload and external assessment | Udacity interface | Not authorized here; local files/publication are not upload confirmation | External step, not claimed |

## Plan and analysis decisions

1. Preserve only the two supplied starter notebooks and acquire the official February 2019 snapshot; record URL, time, archive/CSV hashes and row counts.
2. Write tests before implementing type conversion, exclusion rules, exposure-normalized rate tables and deterministic summaries. Preserve missing optional attributes rather than deleting otherwise usable trips.
3. Explore duration, user type, hour, weekday and day type; then duration/time by user type. Treat rows as trips, not unique riders. Do not infer trip purpose, travel distance, demographics, causation or seasonal patterns from one month.
4. Exclude only invalid essential timestamps/durations/types, audit duplicate rows, and retain long trips. Log-scale duration rather than deleting valid tails. Any scatter subsampling is seeded and labeled; all summaries use the full valid data.
5. Generate 12 exploratory and four explanatory figures, complete all template questions, save fresh-kernel outputs and self-contained HTML exports, inspect actual plots/HTML, and run artifact checks.
6. Review the exact committed state from a clean copy, publish, prepare the user-authorized ZIP, compare every member to that revision, and verify public remote SHA. Full live rubric access remains a documented source limitation, not a silent verification claim.
