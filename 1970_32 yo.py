from pyvis.network import Network
from graph_background_utils import save_graph_with_fuzzy_background
import json
import matplotlib
matplotlib.use("Agg")
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
    "clinical": "Clinical impairment variables",
    "work": "Institutional / performance-pressure pathway",
    "family": "Family and household context variables",
    "access": "Healthcare access / economic barriers",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and chronic burden variables",
    "controversial": "Diagnostic ambiguity pathway",
    "factor": "Observed variable"
}

node_groups = {
    "ADHD": "core",
    "Diagnosis Status": "core",
    "Quality of Life": "core",

    "Genetic Risk": "clinical",
    "Symptom Severity": "clinical",
    "Symptom Type": "clinical",
    "Functional Impairment": "clinical",
    "Comorbid Conditions": "clinical",

    "Employment Instability": "work",
    "Performance Pressure": "work",

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Educational Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Sleep Quality": "environment",
    "Chronic Stress Load": "environment",

    "Diagnostic Criteria Variability": "controversial",
    "Misdiagnosis Rate": "controversial",

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

# ---------------------------------------------------
# Add edges
# ---------------------------------------------------
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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic vulnerability contributes to adult ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.86, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.78, "Underlying ADHD shapes symptom presentation."),
    ("ADHD", "Comorbid Conditions", "+", 0.44, "Untreated ADHD can co-occur with other difficulties that complicate recognition."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.50, "Poor nutrition worsens cognitive regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.60, "Sleep disruption affects functioning and regulation."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Stress amplifies symptoms."),

    ("Age", "Symptom Severity", "+", 0.28, "At age 32, sustained adult role demands can make symptoms more visible."),
    ("Gender", "Symptom Type", "+", 0.32, "Gender norms affect which adult symptoms are noticed or dismissed."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.72, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Employment Instability", "+", 0.72, "Impairment can destabilize employment in adulthood."),
    ("Performance Pressure", "Functional Impairment", "+", 0.32, "Work and performance pressure can worsen visible dysfunction."),

    ("Family Stress", "SymptomSeverity2", "+", 0.01, "Placeholder removed."),
]

edges = [e for e in edges if e[0] != "Family Stress"]

edges.extend([
    ("Family Stress", "Symptom Severity", "+", 0.54, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.62, "Stable household context reduces stress."),

    ("Socioeconomic Status", "Educational Access", "+", 0.68, "Higher SES improves educational and cognitive support opportunities."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Income controls access to mental healthcare."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.44, "Better neighborhood conditions improve resource access."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.72, "Higher SES improves healthcare access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.76, "Cost is a major adult diagnosis barrier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.40, "Access helps diagnosis, but adult ADHD recognition remains weak in 1970."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.68, "Structural inequities influence institutions and healthcare pathways."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.60, "Bias increases diagnostic errors."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.58, "Bias suppresses fair diagnosis access."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.86, "Inconsistent diagnostic framing increases misdiagnosis."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.76, "Comorbidity obscures accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.82, "Misdiagnosis reduces correct diagnosis status."),

    ("Cultural Norms", "Stigma", "+", 0.82, "1970 cultural norms strongly reinforce stigma."),
    ("Stigma", "Access to Mental Health Care", "-", 0.70, "Stigma suppresses help-seeking and care access."),
    ("Gender Bias", "Diagnosis Status", "+", 0.34, "Gender bias shapes who is recognized or dismissed."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.48, "Gender stereotypes increase diagnostic error."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.28, "Diagnosis can modestly reduce impairment through explanation or limited treatment."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.46, "Diagnosis can modestly improve quality of life.")
])

for edge in edges:
    add_edge(*edge)

if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="1970_age_32_graph.html",
        svg_filename="1970_age_32_regions.svg"
    )