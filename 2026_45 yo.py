from pyvis.network import Network
from graph_background_utils import save_graph_with_fuzzy_background
import json
import webbrowser
import os

net = Network(height="800px", width="100%", directed=True, bgcolor="#ffffff")

net.barnes_hut(
    gravity=-9000,
    central_gravity=0.1,
    spring_length=220,
    spring_strength=0.01,
    damping=0.4
)

# keep nodes fixed, but allow panning + zooming of the whole graph
net.set_options("""
var options = {
  "interaction": {
    "dragNodes": false,
    "dragView": true,
    "zoomView": true
  },
  "physics": {
    "enabled": false
  }
}
""")

# ---------------------------------------------------
# Domain colors
# ---------------------------------------------------
group_colors = {
    "core": "#B5EAD7",
    "clinical": "#FFD1DC",
    "school": "#FFDAC1",
    "family": "#AEC6CF",
    "access": "#CBAACB",
    "bias": "#F3E5AB",
    "environment": "#C7CEEA",
    "controversial": "#D5E1DF",
    "work": "#FFB7B2",
    "factor": "#D3D3D3",
    "unknown": "#D3D3D3"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical-cognitive pathway variables",
    "environment": "Environmental burden variables",
    "family": "Family-context variables",
    "access": "Healthcare ecosystem pathway",
    "bias": "Social-cultural / structural bias variables",
    "controversial": "Modern recognition / correction pathway",
    "factor": "Observed variable"
}

node_groups = {
    "ADHD": "core",
    "Diagnosis Status": "core",
    "Quality of Life": "core",

    "Genetic Risk": "clinical",
    "Executive Function Deficit": "clinical",
    "Symptom Severity": "clinical",
    "Functional Impairment": "clinical",
    "Misdiagnosis Rate": "controversial",

    "Sleep Quality": "environment",
    "Nutrition Quality": "environment",
    "Digital Distraction Environment": "environment",
    "Chronic Stress Load": "environment",

    "Family Stress": "family",
    "Home Structure Stability": "family",
    "Family History Awareness": "family",

    "Financial Status": "access",
    "Socioeconomic Status": "access",
    "Provider Availability": "access",
    "Access to Mental Health Care": "access",
    "Waiting Time for Assessment": "access",
    "Cost of Evaluation": "access",
    "Clinical Guidelines Evolution": "access",
    "Care Coordination": "access",
    "Telehealth Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Self-Diagnosis Behavior": "controversial",
    "Retrospective Recognition": "controversial",
    "Diagnosis Feedback Loop": "controversial",
    "Social Media Awareness": "controversial",
    "Overdiagnosis Pressure": "controversial",

    "Age": "factor"
}

# ---------------------------------------------------
# Read positions from JSON
# ---------------------------------------------------
with open("clusters.json", "r", encoding="utf-8") as f:
    node_positions = json.load(f)

positioned_nodes = []
graph_nodes = list(node_groups.keys())

for node in graph_nodes:
    if node in node_positions:
        x = node_positions[node]["x"]
        y = node_positions[node]["y"]
        # color = node_positions[node]["color"]   local domain color
        color = group_colors.get(node_positions[node]["domain"]) #manual domain color
        domain = node_positions[node].get("domain", "unknown")
        local_domain = node_positions[node].get("local_domain", "unknown")
        confidence = node_positions[node].get("confidence", 0.0)

        positioned_nodes.append((node, x, y, color, domain, local_domain, confidence))
    else:
        print(f"Warning: '{node}' not found in clusters.json")

# ---------------------------------------------------
# Add nodes
# background regions carry most of the grouping info
# node borders show local domain
# ---------------------------------------------------
for node, x, y, col, domain, local_domain, confidence in positioned_nodes:
    group = node_groups.get(node, "factor")
    desc = group_descriptions.get(group, "No description available")

    net.add_node(
        node,
        label="ADHD (Underlying Disorder)" if node == "ADHD" else node,
        color={
            "background": "#e6e6e6",
            "border": col,
            "highlight": {
                "background": "#f2f2f2",
                "border": col
            }
        },
        borderWidth=3,
        size=45 if node == "ADHD" else 40 if node == "Diagnosis Status" else 30 if node == "Quality of Life" else 25,
        x=x,
        y=y,
        fixed=True,
        physics=False,
        font={"size": 18 if node in ["ADHD", "Diagnosis Status"] else 13, "color": "black"},
        title=(
            f"Node: {node}\n"
            f"Manual Domain: {domain.upper()}\n"
            f"Local Domain: {local_domain.upper()}\n"
            f"Confidence: {confidence:.2f}\n"
            f"Description: {desc}"
        )
    )

def add_edge(u, v, sign, strength, explanation):
    net.add_edge(
        u, v,
        # label=sign,
        color="green" if sign == "+" else "red",
        width=max(2, strength * 6),
        arrows="to",
        title=f"Effect: {'Positive' if sign == '+' else 'Negative'}\nWhy: {explanation}\nStrength: {strength:.2f}"
    )

edges = [
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic vulnerability contributes strongly to lifelong ADHD."),
    ("ADHD", "Executive Function Deficit", "+", 0.90, "Underlying ADHD strongly affects executive functioning."),
    ("Executive Function Deficit", "Functional Impairment", "+", 0.84, "Executive dysfunction increases cumulative impairment."),
    ("Symptom Severity", "Functional Impairment", "+", 0.84, "Greater symptom burden worsens daily functioning."),
    ("Age", "Functional Impairment", "+", 0.40, "By age 45, long-term untreated difficulties can compound impairment."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.52, "Long-term nutrition still impacts cognition and regulation."),
    ("Sleep Quality", "Executive Function Deficit", "-", 0.64, "Sleep affects executive functioning."),
    ("Digital Distraction Environment", "Chronic Stress Load", "+", 0.58, "Digital distraction is a strong contextual factor by 2026."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Accumulated life stress can worsen symptoms in midlife."),

    ("Home Structure Stability", "Family Stress", "-", 0.68, "Stable home structure reduces stress."),
    ("Family Stress", "Chronic Stress Load", "+", 0.72, "Family stress contributes to chronic stress accumulation."),
    ("Family History Awareness", "Retrospective Recognition", "+", 0.54, "Family history strongly supports later-life recognition by 2026."),

    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Financial resources strongly affect access to care."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.74, "Socioeconomic position still shapes access."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.82, "More providers reduce waiting time in 2026."),
    ("Telehealth Access", "Access to Mental Health Care", "+", 0.70, "Telehealth expands access to evaluation and follow-up."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.34, "Long waits still reduce diagnosis, but less sharply than before."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.46, "Cost still suppresses diagnosis, but less absolutely than before."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.86, "Access strongly helps diagnosis in 2026."),
    ("Clinical Guidelines Evolution", "Diagnosis Status", "+", 0.78, "Guideline evolution makes delayed adult recognition highly plausible."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.72, "Access increasingly leads to coordinated care."),
    ("Care Coordination", "Diagnosis Status", "+", 0.36, "Coordination improves successful diagnosis completion."),
    ("Care Coordination", "Quality of Life", "+", 0.34, "Coordinated care can improve stability and quality of life."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.50, "Misdiagnosis still reduces correct diagnosis status."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.52, "Structural inequities still influence institutions."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.34, "Bias still creates some diagnostic error."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.24, "Bias still suppresses equitable access to diagnosis."),

    ("Social Media Awareness", "Self-Diagnosis Behavior", "+", 0.62, "Online awareness strongly supports self-recognition by 2026."),
    ("Retrospective Recognition", "Self-Diagnosis Behavior", "+", 0.66, "Later-life reinterpretation of lifelong patterns strongly supports self-recognition."),
    ("Self-Diagnosis Behavior", "Diagnosis Status", "+", 0.54, "Self-recognition can meaningfully push toward evaluation."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Overdiagnosis discourse is clearly present in 2026."),
    ("Diagnosis Status", "Diagnosis Feedback Loop", "+", 0.56, "Diagnosis strongly influences reinterpretation of lifelong patterns."),
    ("Diagnosis Feedback Loop", "Retrospective Recognition", "+", 0.46, "Feedback effects on recognition are substantial."),
    ("Diagnosis Feedback Loop", "Self-Diagnosis Behavior", "+", 0.42, "Diagnosis history reinforces self-understanding and future help-seeking."),

    ("Cultural Norms", "Stigma", "+", 0.38, "Stigma remains present, but much weaker than in earlier decades."),
    ("Stigma", "Diagnosis Status", "-", 0.30, "Stigma still suppresses adult diagnosis somewhat."),
    ("Stigma", "Self-Diagnosis Behavior", "-", 0.24, "Stigma still discourages self-recognition somewhat."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.60, "Diagnosis can meaningfully reduce impairment through treatment or support."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.82, "Diagnosis can strongly improve quality of life in midlife.")
]

for edge in edges:
    add_edge(*edge)

if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="2026_age_45_graph.html",
        svg_filename="2026_age_45_regions.svg"
    )