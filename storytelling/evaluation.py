"""Human-rating and comprehension evaluation workflows for graph stories."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from .analysis import THEMES, fact_catalog, story_key
from .data import ROOT
from .director import GenerationError, baseline_story, generate_story, load_story, save_story
from .player import player_html

CONDITIONS = ("explorer", "rule-based", "generated")
RATING_DIMENSIONS = {
    "graph_fidelity": "Graph fidelity",
    "topic_relevance": "Topic relevance",
    "narrative_coherence": "Narrative coherence",
    "clarity": "Clarity",
    "engagement": "Engagement",
}
THEME_QUESTIONS = {
    "Treatment and access": "Which treatment and access relationships differ most?",
    "School and family": "How do school and family pathways differ?",
    "Recognition and bias": "What changes around recognition and bias?",
    "Work and daily life": "What changes around work and daily functioning?",
    "All changes": "What are the most important structural differences?",
}


def evaluation_cases() -> list[dict]:
    """A fixed 24-case suite spanning every snapshot and both comparison axes."""
    themes = list(THEMES)
    specs: list[tuple[str, int, int, int, int]] = []
    for age in (8, 32, 45):
        for start, end in ((1970, 1990), (1990, 2010), (2010, 2026), (1970, 2026)):
            specs.append(("historical", start, age, end, age))
    for year in (1970, 1990, 2010, 2026):
        for start_age, end_age in ((8, 32), (32, 45), (8, 45)):
            specs.append(("age", year, start_age, year, end_age))
    cases = []
    for index, (mode, before_year, before_age, after_year, after_age) in enumerate(specs):
        theme = themes[index % len(themes)]
        cases.append({
            "id": f"case-{index + 1:02d}",
            "mode": mode,
            "before_year": before_year,
            "before_age": before_age,
            "after_year": after_year,
            "after_age": after_age,
            "theme": theme,
            "question": THEME_QUESTIONS[theme],
        })
    return cases


def case_label(case: dict) -> str:
    if case["mode"] == "historical":
        comparison = f"{case['before_year']} → {case['after_year']} · age {case['before_age']}"
    else:
        comparison = f"{case['before_year']} · age {case['before_age']} → age {case['after_age']}"
    return f"{case['id']} · {comparison} · {case['theme']}"


def case_snapshots(case: dict, snapshots: dict) -> tuple[dict, dict]:
    return (
        snapshots[case["before_year"]][case["before_age"]],
        snapshots[case["after_year"]][case["after_age"]],
    )


def assigned_condition(participant_id: str, case_id: str) -> str:
    digest = hashlib.sha256(f"{participant_id.strip()}|{case_id}".encode()).digest()
    return CONDITIONS[int.from_bytes(digest[:4], "big") % len(CONDITIONS)]


def generated_story_path(case: dict, snapshots: dict) -> Path:
    before, after = case_snapshots(case, snapshots)
    key = story_key(before, after, case["theme"], case["question"])
    return ROOT / "evaluation" / "stories" / f"{key}.json"


def load_generated_case(case: dict, snapshots: dict) -> dict | None:
    before, after = case_snapshots(case, snapshots)
    paths = [generated_story_path(case, snapshots), ROOT / "stories" / f"{story_key(before, after, case['theme'], case['question'])}.json"]
    for path in paths:
        if path.exists():
            try:
                story = load_story(path, before, after, case["theme"], case["question"])
            except (ValueError, KeyError, OSError, json.JSONDecodeError):
                continue
            if story["origin"] == "local-qwen":
                return story
    return None


def quiz_for_case(case: dict, snapshots: dict) -> list[dict]:
    before, after = case_snapshots(case, snapshots)
    facts = fact_catalog(before, after, case["theme"], case["question"])
    target = next((fact for fact in facts if fact["kind"] in {"added", "removed"}), facts[0])
    target_edge = (target["after_edges"] or target["before_edges"])[0]
    correct_relationship = f"{target_edge['from']} → {target_edge['to']}"
    distractors = []
    for fact in facts:
        for edge in fact["after_edges"] + fact["before_edges"]:
            label = f"{edge['from']} → {edge['to']}"
            if label != correct_relationship and label not in distractors:
                distractors.append(label)
            if len(distractors) == 3:
                break
        if len(distractors) == 3:
            break
    relation_options = [correct_relationship, *distractors]
    shift = int(hashlib.sha256(case["id"].encode()).hexdigest()[:2], 16) % len(relation_options)
    relation_options = relation_options[shift:] + relation_options[:shift]
    if target["kind"] == "added":
        change_prompt = "Which relationship is included only in the comparison snapshot?"
    elif target["kind"] == "removed":
        change_prompt = "Which relationship is included only in the starting snapshot?"
    else:
        change_prompt = "Which relationship is the highest-ranked difference for this comparison?"
    interpretation_correct = (
        "The snapshots represent different historical models, not proof of a real-world trend."
        if case["mode"] == "historical"
        else "The graphs are separate age scenarios, not one person's development."
    )
    return [
        {"id": "relationship", "prompt": change_prompt, "options": relation_options, "correct": correct_relationship},
        {"id": "absence", "prompt": "What does an absent edge establish?", "options": [
            "Only that the edge is not included in that authored snapshot.",
            "That the relationship did not exist in reality.",
            "That the relationship was clinically disproven.",
            "That the source data are incomplete."
        ], "correct": "Only that the edge is not included in that authored snapshot."},
        {"id": "weight", "prompt": "What does an edge weight represent here?", "options": [
            "An authored model magnitude.",
            "A probability that the outcome will occur.",
            "A measured clinical effect size.",
            "Statistical confidence in the relationship."
        ], "correct": "An authored model magnitude."},
        {"id": "interpretation", "prompt": "Which interpretation is appropriate?", "options": [
            interpretation_correct,
            "The comparison proves that care improved.",
            "Every highlighted pathway is causally equivalent.",
            "A positive sign means the relationship is beneficial."
        ], "correct": interpretation_correct},
    ]


def score_answers(questions: list[dict], answers: dict[str, str]) -> int:
    return sum(answers.get(question["id"]) == question["correct"] for question in questions)


def records_csv(records: list[dict]) -> str:
    if not records:
        return ""
    fields = sorted({key for record in records for key in record if not isinstance(record[key], (dict, list))})
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows({key: record.get(key, "") for key in fields} for record in records)
    return output.getvalue()


def _story_for_condition(condition: str, case: dict, snapshots: dict) -> dict | None:
    before, after = case_snapshots(case, snapshots)
    if condition == "generated":
        return load_generated_case(case, snapshots)
    story = baseline_story(before, after, case["theme"], case["question"])
    story["presentation"] = condition
    return story


def _render_story_ratings(snapshots: dict, cases: list[dict]) -> None:
    st.subheader("Rate 24 generated stories")
    st.caption("Rate graph fidelity—not medical truth—plus relevance, coherence, clarity, and engagement. Results stay in this browser session until downloaded.")
    ratings = st.session_state.setdefault("human_story_ratings", {})
    st.progress(len(ratings) / len(cases), text=f"{len(ratings)} of {len(cases)} stories rated")
    case = st.selectbox("Evaluation case", cases, format_func=case_label, key="rating_case")
    before, after = case_snapshots(case, snapshots)
    session_key = f"evaluation_generated_{case['id']}"
    if session_key not in st.session_state:
        cached = load_generated_case(case, snapshots)
        if cached:
            st.session_state[session_key] = cached
    if st.button("Generate this evaluation story", type="primary", key="generate_evaluation_story"):
        try:
            with st.spinner("Generating and checking the story…"):
                story = generate_story(before, after, case["theme"], case["question"])
                st.session_state[session_key] = story
                try:
                    save_story(story, ROOT / "evaluation" / "stories")
                except OSError:
                    pass
            st.success("Generated story is ready for rating.")
        except (GenerationError, ValueError) as exc:
            st.error(str(exc))
    story = st.session_state.get(session_key)
    if not story:
        st.info("Generate this case with the local model before rating it. Existing saved stories are loaded automatically when available.")
        return
    st.iframe(player_html(story, before, after), height="content")
    existing = ratings.get(case["id"], {})
    with st.form(f"rating_form_{case['id']}"):
        values = {
            key: st.slider(label, 1, 5, int(existing.get(key, 3)), help="1 = poor, 5 = excellent")
            for key, label in RATING_DIMENSIONS.items()
        }
        notes = st.text_area("Reviewer notes", value=existing.get("notes", ""))
        submitted = st.form_submit_button("Save this rating")
    if submitted:
        ratings[case["id"]] = {
            "record_type": "story_rating",
            "case_id": case["id"],
            "story_key": story["key"],
            "story_origin": story["origin"],
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
            **values,
            "notes": notes,
        }
        st.success(f"Saved rating {len(ratings)} of {len(cases)}.")
    if ratings:
        rows = list(ratings.values())
        st.download_button("Download human ratings CSV", records_csv(rows), "story-human-ratings.csv", "text/csv")
        st.download_button("Download human ratings JSON", json.dumps(rows, indent=2), "story-human-ratings.json", "application/json")


def _render_comprehension_study(snapshots: dict, cases: list[dict]) -> None:
    st.subheader("Compare comprehension")
    st.caption("Each participant is assigned reproducibly to the explorer, rule-based story, or generated story. Use a different participant ID for each person.")
    participant_id = st.text_input("Participant ID", key="study_participant", placeholder="P001")
    case = st.selectbox("Study case", cases, format_func=case_label, key="study_case")
    if not participant_id.strip():
        st.info("Enter a participant ID to receive a study condition.")
        return
    condition = assigned_condition(participant_id, case["id"])
    st.metric("Assigned condition", condition.replace("-", " ").title())
    story = _story_for_condition(condition, case, snapshots)
    if story is None:
        st.warning("This generated-story case has not been prepared yet. Generate it in the Story ratings tab before running this participant.")
        return
    before, after = case_snapshots(case, snapshots)
    run_key = f"study_started_{participant_id}_{case['id']}"
    if st.button("Start this study task", type="primary", key=f"start_{participant_id}_{case['id']}"):
        st.session_state[run_key] = time.monotonic()
    if run_key not in st.session_state:
        return
    st.iframe(player_html(story, before, after), height="content")
    questions = quiz_for_case(case, snapshots)
    with st.form(f"quiz_{participant_id}_{case['id']}"):
        answers = {
            question["id"]: st.radio(question["prompt"], question["options"], index=None, key=f"{participant_id}_{case['id']}_{question['id']}")
            for question in questions
        }
        confidence = st.slider("How confident are you?", 1, 5, 3)
        submitted = st.form_submit_button("Submit comprehension answers")
    if submitted:
        if any(answer is None for answer in answers.values()):
            st.error("Answer every question before submitting.")
            return
        result = {
            "record_type": "comprehension",
            "participant_id": participant_id.strip(),
            "case_id": case["id"],
            "condition": condition,
            "score": score_answers(questions, answers),
            "max_score": len(questions),
            "confidence": confidence,
            "duration_seconds": round(time.monotonic() - st.session_state[run_key], 1),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "answers": answers,
        }
        results = st.session_state.setdefault("comprehension_results", [])
        results.append(result)
        del st.session_state[run_key]
        st.success(f"Recorded {result['score']} of {result['max_score']} correct.")
    results = st.session_state.get("comprehension_results", [])
    if results:
        flat = [{**result, "answers": json.dumps(result["answers"], ensure_ascii=False)} for result in results]
        st.download_button("Download comprehension results CSV", records_csv(flat), "comprehension-results.csv", "text/csv")
        st.download_button("Download comprehension results JSON", json.dumps(results, indent=2), "comprehension-results.json", "application/json")


def _render_results_summary(cases: list[dict]) -> None:
    st.subheader("Session results")
    ratings = list(st.session_state.get("human_story_ratings", {}).values())
    results = st.session_state.get("comprehension_results", [])
    if ratings:
        st.write(f"Story ratings collected: {len(ratings)} of {len(cases)}")
        st.dataframe([
            {"Measure": label, "Mean": round(sum(r[key] for r in ratings) / len(ratings), 2)}
            for key, label in RATING_DIMENSIONS.items()
        ], hide_index=True, width="stretch")
    else:
        st.info("No human story ratings have been collected in this session.")
    if results:
        rows = []
        for condition in CONDITIONS:
            subset = [result for result in results if result["condition"] == condition]
            if subset:
                rows.append({
                    "Condition": condition.replace("-", " ").title(),
                    "Participants": len(subset),
                    "Mean score": round(sum(r["score"] for r in subset) / len(subset), 2),
                    "Mean seconds": round(sum(r["duration_seconds"] for r in subset) / len(subset), 1),
                    "Mean confidence": round(sum(r["confidence"] for r in subset) / len(subset), 2),
                })
        st.dataframe(rows, hide_index=True, width="stretch")
    else:
        st.info("No comprehension results have been collected in this session.")


def render_evaluation_lab(snapshots: dict) -> None:
    st.markdown('<div style="font-size:11px;letter-spacing:2px;color:#50828b;font-weight:700">STORY EVALUATION LAB</div>', unsafe_allow_html=True)
    st.title("Test whether the stories help.")
    st.caption("A 24-case protocol for human story ratings and a three-condition comprehension comparison.")
    cases = evaluation_cases()
    ratings_tab, study_tab, results_tab = st.tabs(["Story ratings", "Comprehension study", "Results"])
    with ratings_tab:
        _render_story_ratings(snapshots, cases)
    with study_tab:
        _render_comprehension_study(snapshots, cases)
    with results_tab:
        _render_results_summary(cases)
