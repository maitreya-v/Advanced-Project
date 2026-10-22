# GitHub and local reconciliation

Date: October 15, 2026.

## Result

The combined checkout is `outputs/Advanced-Project` in the working project. It uses the current GitHub Advanced-Project checkout as its base and adds the local storytelling implementation. Its Git remote is `https://github.com/maitreya-v/Advanced-Project.git`.

No commits, branches or pushes were created. This is a content reconciliation across two repository identities, not a Git merge between branches of one repository. The local application points to `maitreya-v/Deploy_AP`; GitHub Advanced-Project is a separate repository.

## Inputs inspected

| Input | State | Treatment |
|---|---|---|
| GitHub Advanced-Project | HEAD `c5b06d3`, “Directed path stories”, October 15, 2026 | Base checkout, including literature and validation artifacts |
| Workspace `outputs/Deploy_AP` | HEAD `748b632`; tracked modifications and untracked storytelling files | Retained intact; local additions copied to combined checkout |
| Desktop `Advanced_Project/outputs/Deploy_AP` | Same shared file contents as workspace app | Inspected; retained intact |
| Workspace-only evaluation cache | `evaluation/stories/f603527a4eca40439d500d82.json` | Included in combined checkout |
| Workspace root README and saved conversation | Prior decisions and local project location | Read as context |
| `sources/` | Empty at inspection | Untouched |

The Desktop and workspace app copies match for every shared relevant file. The workspace has one additional cached evaluation story. Runtime installations, Git internals, operating-system metadata and Python caches are excluded from the application comparison.

## What differed and how it was resolved

| Files / capability | Resolution | Reason |
|---|---|---|
| `Dashboard.py` | Keep GitHub explorer and validation components; add sidebar entries for local Story mode and Evaluation lab | Preserves newer evidence UI and all local storytelling functionality |
| `requirements.txt` | Use focused dashboard dependencies, require Streamlit 1.64 or newer, retain `streamlit-js-eval` | Local story UI and newer validation tabs need a compatible runtime |
| Original GitHub dependency freeze | Preserve as `requirements-research.txt` | Keeps the research environment record without forcing heavyweight experiments into the dashboard installation |
| `.gitignore` | Union patterns; add `.env` exclusion for future untracked local settings | Keeps both projects' temporary-file exclusions |
| `1970.py`, `1990.py`, `2010.py`, `2026_BASE.py`, `base_color.py` | Keep GitHub bytes | Differences were line endings only |
| All twelve `*yo.py` snapshot files and `clusters.json` | Keep GitHub bytes unchanged | Shared graph sources already match; validation source hashes remain meaningful |
| `story_paths.py`, corpus workbook, papers, review reports, validation viewers | Preserve GitHub versions | These newer features are absent from local Deploy_AP |
| `storytelling/`, saved stories, generation/export commands, evaluation suite | Add local versions | These capabilities are absent from GitHub Advanced-Project |
| `tests/` | Union the test suites; adjust local dashboard test to select Story mode explicitly | The merged default remains the newer GitHub explorer |
| Original demo HTML, brief and old launcher | Keep original copies | Existing demonstrations remain available |

Original versions of the three manually reconciled files are backed up under the working project's `work/merge-backups/github/` and `work/merge-backups/local/`.

## Integration boundaries

- Explore graph keeps the existing GitHub snapshot rendering and validation flow.
- The Story paths tab keeps GitHub's bounded changed-route discovery.
- Story mode keeps the local literal-only snapshot loader, stable relationship IDs, local Qwen generation and persistent player.
- Evaluation lab keeps the existing 24-case local protocol.
- Story mode and the explorer currently use different evidence interfaces and snapshot display loaders. The proposed adapter is part of the next implementation plan, not a completed feature of this reconciliation.
- The main dependency file covers the combined dashboard. Optional embedding, clustering and CausalChat experiments are preserved but were not exercised.

## Verification

Executed the combined test suite using the prepared local Python environment:

```text
35 passed, 25 subtests passed
```

Checks cover the explorer at all twelve year/age combinations, validation source checks and panels, corpus counts, directed alternative routes, story grounding, saved stories, exports and evaluation logic. Both comparison modes and every Workspace entry run without test exceptions.

The test suite uses a simulated model for generation tests. Live Qwen inference and visual inspection in a real browser were not repeated during reconciliation. The full suite was run before adding planning documents and the launcher.

## Version control state

The combined checkout retains GitHub's current commit and remote. Additions and integration changes remain uncommitted for review. The original Desktop Deploy_AP checkout and the internal mirrored Deploy_AP checkout were not overwritten.

After reviewing this combined folder, future implementation should target Advanced-Project rather than developing two diverging Deploy_AP copies. Publishing or pushing remains a separate action.
