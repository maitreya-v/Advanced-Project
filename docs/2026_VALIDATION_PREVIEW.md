# 2026 validation in Dashboard.py

The local `main` ref at `d935c3f` contains the 2026 age-8, age-32 and age-45
validation reports. These artifacts were missing from `codex/all-project-work`.
They have been copied from that ref and integrated into the existing dashboard.

## Test the original layout with 2026 evidence

```powershell
.\.venv\Scripts\python.exe -m streamlit run Dashboard.py
```

Open <http://localhost:8501>. In **Explore graph**, select **2026**, then each age
(**8**, **32**, **45**). Click an edge to open **Validation**. Check status,
decision, reference pagination, and **Open supplied PDF**. The Info, Edges,
Groups and Legend tabs and the strength slider still use the existing dashboard.

`Dashboard.py` uses its existing validation loader for all four years.
`dashboard_validation.py` includes 2026 in its supported years, and
`dashboard_corpus.py` uses UTF-8 when reading reports and deduplicates the 159 PDF
copies into 158 documents for the year-level reviewed count, matching `main`.
The temporary launcher and support module were removed. Graph source files and
validation decisions remain unchanged.

## Imported material

- `validation_2026_age8/`: 68 edges.
- `validation_2026_age32/`: 74 edges.
- `validation_2026_age45/`: 70 edges.
- `2026 ADHD Papers/`: 159 PDFs, kept byte-for-byte from `main`.
- `paper_reviews/2026/` and `validation_2026_utils.py`: provenance and rebuild sources.

Standalone graphs, reports and workbooks link directly to `../2026 ADHD Papers/`.
No symlinks, Windows junctions or local Git exclusions are needed. Keep the corpus
folder beside the report folders. Dashboard PDF links continue to resolve through
the existing reference renderer. Report rebuilding accepts Git checkout newline
conversions while retaining source-text and PDF integrity checks.

`scripts/import_2026_validation.py` records the original import from the local
`main` ref and refuses to overwrite differing files. It is not needed after a
checkout; the portable artifacts are committed directly. Do not re-import the
older reports over the rebuilt portable reports.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_dashboard_2026_support.py -v
```

The three integration tests cover all 212 edges, preserved layout and styling,
graph rendering with a strength filter, hashes for all 159 source PDFs,
deduplicated corpus counts, and simulated edge clicks into page-linked validation
panels for each age.

The portability checks additionally copy the artifacts and PDF corpus into a
fresh directory tree without any symlinks or junctions, resolve every standalone
page-linked PDF URL, compare workbook paths, and verify the selected quotations
against the source PDFs. Install `requirements-dev.txt`, then run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_2026_portability.py -v
```

## Next phase

After user testing, implement a separate **Dashboard 2.0** file with compact year,
age and strength controls above the left graph and the existing Snapshot tabs in
the lower right. The upper-right workspace is deferred. This phase does not
change the dashboard layout.
