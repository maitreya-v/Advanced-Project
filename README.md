# Advanced Project — Combined Graph and Storytelling App

This checkout combines GitHub `maitreya-v/Advanced-Project` at `c5b06d3` with the local `Deploy_AP` storytelling application. It preserves the GitHub literature corpus, validation panels, directed route suggestions and graph explorer, alongside local Qwen narration, saved stories, offline exports and evaluation tools.

Read [the reconciliation report](docs/SYNC_REPORT.md), [the directed-path specification](docs/DIRECTED_PATH_STORY_SPEC.md), [the implementation plan](docs/IMPLEMENTATION_PLAN.md), and [the current edge-reasoning format](docs/EDGE_REASONING_SPEC.md). **Path story** implements endpoint selection, bounded route enumeration, concise reasons with fictional examples, and isolated step-by-step playback. Later comparison and study extensions remain in the plan.

## Run the dashboard

Use Python 3.12 or newer. From this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run Dashboard.py
```

Open the local URL printed by Streamlit. **Explore graph** is the default and contains **Snapshot explorer** and **Story paths** tabs. Use the **Workspace** sidebar to open **Path story**, **Story mode** or **Evaluation lab**. On this Mac, `Start Combined Story App.command` uses the existing project environment and port 8502 so the older demo can continue using 8501.

The original GitHub dependency snapshot is preserved in `requirements-research.txt` for reference. The main `requirements.txt` installs the combined dashboard dependencies; optional clustering and CausalChat experiments may need separate environments and their own dependencies.

The explorer attaches the existing snapshot-specific validation reports for 1970, 1990 and 2010. **Path story** combines those review decisions with the contextual literature registry while preserving stable relationship IDs. The older comparison-based Story mode retains its separate literature interface. No snapshot-specific report is available for 2026.

## Understand a selected path through reasons and tiny stories

Choose **Path story** in the Workspace sidebar, or use **Choose nodes and create a story from this graph** in the snapshot explorer. A direct link is `http://127.0.0.1:8502/?workspace=path`. Links from the explorer carry the selected year and age into the story workspace.

The **1. Full graph and endpoints** tab shows the entire selected snapshot. Click a node to set Start; the next node click sets End. The Set Start and Set End buttons let you change either endpoint, and dropdowns provide a keyboard-friendly alternative. Clear selections starts again. No endpoints are preselected in a new session.

Click **Find directed routes** to open **2. Routes and stories**. Choose a route, then click **Generate story for this path** for new local-Qwen writing based on that exact route. Merely selecting nodes does not run the model. Changing endpoints, year/age or filters invalidates old route results until Find directed routes is clicked again.

For the 2026 age-8 Diagnosis Status to Quality of Life example, all eight eligible simple routes within five edges are listed. Direct routes count as valid options; cycles are not repeatedly traversed. Search limits are explicit when discovery is incomplete.

Selecting a route removes every unrelated node and edge from the player. Start, intermediate concepts and End appear in order. Each chapter advances exactly one directed relationship; visited edges remain visible. Next, Back, Replay, Play/Pause and the breadcrumb run inside the player without new model requests. Width continues to represent authored strength; glow marks the current step.

The current format follows the user's revised request: **Cause → Effect · Positive/Negative**, **Reason**, **Example 1**, **Example 2**. Reasons explain a proposed mechanism in one to three sentences; each fictional example is one to three sentences showing a concrete event and consequence. Repeated fox-story and question-writing scenes are removed. Reasons are authored interpretations, not validated causal effects. Original explanations, signs, strengths and review observations remain inspectable separately.

`reasoning_library.py` provides specific reasons and two authored examples for all 124 unique signed relationships across the supplied snapshots. There is no review gate or withheld-example state. Where a label is ambiguous, the reason briefly states the interpretation used for the fictional illustration; the source graph is not silently changed.

An authored explanation is available without Ollama. **Generate story for this path** requests new local-Qwen examples for every selected edge. The model cannot change the reasons, direction or source facts. Fictional responses must not become actual patient claims, promises, dosing or advice. Checks cover exact edge order, two distinct examples, brevity, selected mechanism terms and some overclaims. Failure preserves the current examples without a review gate.

Download a standalone player or JSON record, or save for replay. The `edge-examples-v5` cache includes a rationale-library hash so old review-gated records cannot reappear. Earlier saved character, edge-reasoning and comparison stories remain exportable, but are not reused as current explanations. The full suite passes 73 tests, including 703 subtests.

## Generate new stories for free

Install [Ollama](https://ollama.com/download) from its official website. Download the local model and start the local service if it is not already running:

```sh
ollama pull qwen3:8b
OLLAMA_NO_CLOUD=1 ollama serve
```

Qwen3 8B's compressed weights are approximately 5.2 GB; runtime memory is larger and depends on context length. The prototype was exercised on an Apple M5 with 16 GB memory. The included four-scene example took about 85 seconds to generate locally. Performance varies with load and hardware.

Select a comparison and focus, optionally enter a question, and click **Generate a new story**. Each click performs live inference and creates one story with up to four scenes. Change the question or comparison to direct the next story; the saved example does not limit what can be generated. Generation is on demand, not automatically triggered by every filter adjustment. Identical inputs may produce the same story because inference uses reproducible settings.

The app sends graph data only to the local Ollama service. It has no cloud-model fallback and requires no API key. Failure leaves the current story intact. **Use rule-based story** produces a clearly labeled deterministic alternative without any model.

Ollama must run on the same machine as the Streamlit server. A remotely hosted Streamlit app cannot reach a visitor's laptop through `localhost`. For a public demo, generate stories locally and include their JSON files in `stories/`; visitors can play them without live inference. Always-on live generation needs model-serving hardware.

The local endpoint defaults to `http://127.0.0.1:11434`. `OLLAMA_BASE_URL` can select another HTTP loopback port. Remote URLs, redirects and cloud model names are rejected. The CLI also supports the smaller local `qwen3:4b` model after downloading it.

## Saved project deliverables

- [Standalone ADHD story demo](docs/ADHD-story-demo.html) — the original saved offline demonstration.
- [Professor brief](docs/ADHD%20Graph%20Storytelling%20Brief.docx) — the original one-page project brief.
- [Edge-reasoning demo](docs/edge-reasoning-demo.html) and [character-story demo](docs/character-story-demo.html) — saved examples of earlier story formats.

The current application and tests are included alongside these deliverables. Python environments, downloaded model weights, runtime logs and local backup folders remain outside the repository.

## Save and share

- **Download standalone story** exports a self-contained HTML file containing the graph library, source graph records, evidence and scene player. It works offline and needs no Python or Ollama.
- **Download story + evidence** exports the JSON storyboard and its provenance.
- **Save for demo playback** saves the current story into this project's `stories/` directory. Include that file when deploying. On a read-only host, use the downloads instead.

You can also generate demo stories from a terminal:

```sh
python generate_story.py --from-year 2010 --to-year 2026 --age 8
python generate_story.py --from-year 2026 --to-year 2026 --age 8 --to-age 32 --theme "Work and daily life"
python generate_story.py --baseline --theme "School and family"
```

Rebuild a standalone HTML demo from a checked saved story:

```sh
python export_saved_story.py stories/STORY_KEY.json ADHD-story-demo.html
```

Saved stories are keyed by source fingerprints, comparison, theme, question and story format version. When a story is loaded, the app rebuilds its evidence from the current source records and checks references and numerical literals again. Editing source snapshots invalidates the saved story; regenerate it after a source change. The dashboard reloads graph data on a rerun when a source file's timestamp or size changes.

## How it works

1. `storytelling/data.py` reads literal node/edge records from the existing `*yo.py` scripts with Python's AST parser. It does not execute those scripts. Layout comes from `clusters.json` and fallback positions.
2. `storytelling/analysis.py` identifies additions, removals, sign changes, strength changes and short replacement paths. Comparisons hold either age or year constant.
3. Candidate facts receive a transparent editorial score: relevance (40), novelty (25), absolute weight change (20), and connection to selected outcome nodes (15). The question uses keyword matching; it is not a semantic search engine. Baseline selection penalizes repeated node coverage.
4. `storytelling/director.py` gives local Qwen a bounded tool loop (`get_ranked_changes`, `inspect_fact`) and requests a structured storyboard. There are at most two tool rounds, one final generation and one validation-repair attempt. Qwen chooses the ordering and writes captions; graph calculations remain deterministic.
5. Pydantic checks the format. Additional checks reject unknown or repeated facts, mismatched graph entities, unsupported numerical literals, off-focus scene sets, ambiguous age-comparison language, and some overstated claims. The app does not claim to prove semantic correctness of arbitrary generated prose. Review model-written narration before research publication.
6. `storytelling/player.html` plays the complete sequence inside one iframe. Scene navigation does not rerun Streamlit or call the model. Node positions are stable, width continues to represent model strength, and opacity/shadows direct attention. Dashed comparison edges belong to the other snapshot, not the currently selected graph.

Every story now has deterministic opening and closing chapters. The opening states the comparison scope; the closing summarizes the selected change types and citation coverage. These chapters are computed from checked graph facts rather than generated prose.

## Evidence labels and citations

`storytelling/evidence.json` attaches reviewed literature context to stable edge IDs. The initial registry covers 13 treatment, telehealth, digital-therapeutic and school-support relationships using a pediatric clinical guideline and three randomized trials. Every evidence panel shows one of three scopes:

- directly relevant trial evidence, with any population or outcome limitation stated;
- guideline or indirect context that does not test the exact edge; or
- not yet reviewed.

These labels are deliberately not GRADE ratings. A citation never validates an authored direction, sign or weight. Evidence updates do not change graph fingerprints or silently invalidate an otherwise grounded saved story.

## Evaluation lab

Choose **Evaluation lab** in the sidebar to use the fixed 24-case study suite.

- **Story ratings** generates or loads each local-Qwen story and collects 1–5 human ratings for graph fidelity, topic relevance, narrative coherence, clarity and engagement. Download results before ending the browser session.
- **Comprehension study** reproducibly assigns an anonymous participant ID to the graph explorer, rule-based story or generated story. It records four-question comprehension score, completion time and confidence.
- **Results** summarizes the current session by rating dimension and study condition.

The protocol and safeguards are documented in `evaluation/README.md`. Generated evaluation stories can be cached under `evaluation/stories/`; human results are not written automatically. Prepare generated cases before recruiting participants, use anonymous IDs, and do not fabricate ratings for unfinished cases.

## Interpretation and validation

These are **authored model snapshots**, not validated longitudinal observations. The prototype does not estimate causal effects or validate ADHD claims. Some edges now have literature context, but the attached sources do not independently verify the graph's directions or weights.

- Strengths are authored magnitudes, not probabilities, measured effect sizes or statistical confidence.
- The `confidence` values in `clusters.json` concern agreement among nearby node categories in the layout. They are not used as scientific confidence or narrative ranking weights.
- A missing edge means absent from a particular snapshot; it does not prove disappearance in reality.
- A direct edge and a longer path are not necessarily causally equivalent.
- Different ages are separate scenarios; the app does not present them as one person's life history.
- Rankings are prototype editorial choices. Expert relevance rankings and user comprehension should be used to tune them.

The GitHub validation reports are retained unchanged, including source-hash checks. They do not assess the numeric strengths, and 2026 has no matching snapshot-specific review report. The local story registry remains literature context rather than validation of a complete route.

## Checks

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Tests cover real snapshot differences, path restructuring, negative signs, comparison axes, evidence attachment, deterministic bookends, the 24-case evaluation suite, comprehension scoring, safe literal loading, cache invalidation, rejected unsupported statements, local-only connections, tool execution and escaped standalone exports. `cluster.py` is an optional, separate layout-generation utility; its embedding/UMAP dependencies are not required to run the dashboard.

## Licensing

Qwen3 is released under Apache 2.0; Ollama and the bundled graph library have their own upstream licenses. This change does not assign a new license to the original repository.
