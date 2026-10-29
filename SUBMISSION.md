# Local compressed submission

The user requested a public GitHub repository and a local ZIP. The saved course directions specify ZIP submission for local development; public publication alone is not treated as a course upload.

The local package is named `Udacity_MS_Communicate_Data_Findings_submission.zip` and is stored beside the repository directory. It contains one project folder with:

- Both completed notebooks with saved outputs.
- Both HTML exports, with figures embedded for local viewing.
- Raw/clean datasets, provenance, cleaning audit, summary and chart manifest.
- Required analysis/plot modules, notebook runner, authoring helper and tests.
- README, dataset/source definitions, validation notes and dependency specifications.

Git history, environments, caches, checkpoints, secrets and unrelated assignment files are excluded. The package is generated from the reviewed committed tree, so it does not collect arbitrary untracked files.

To recreate it from the repository directory after committing the reviewed revision:

```bash
git archive --format=zip --prefix=Udacity_MS_Communicate_Data_Findings/ --output=../Udacity_MS_Communicate_Data_Findings_submission.zip HEAD
python -m zipfile -t ../Udacity_MS_Communicate_Data_Findings_submission.zip
```

The source commit is recorded in the ZIP comment. At handoff, every file is checked byte-for-byte against its committed blob, paths and archive integrity are validated, and an extracted copy is tested and executed using the validated project environment. This ZIP is a generated local artifact, not a file nested inside the public source repository.

Upload it through the course interface and verify that interface’s confirmation. If the live interface imposes additional size/naming rules or accepts a repository link instead, follow its explicit instructions. No course upload or grade is claimed here.
