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
    "clinical": "Clinical impairment variables",
    "work": "Workplace support and adult-function pathway",
    "family": "Family and household context variables",
    "access": "Healthcare access pathway",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and chronic burden variables",
    "controversial": "Diagnostic ambiguity / modern adult diagnosis pathway",
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

    "Workplace Accommodations": "work",
    "Performance Pressure": "work",
    "Career Friction": "work",
    "Remote Collaboration Demands": "work",

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Waiting Time for Assessment": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Sleep Quality": "environment",
    "Chronic Stress Load": "environment",

    "Diagnostic Criteria Variability": "controversial",
    "Misdiagnosis Rate": "controversial",
    "Self-Recognition": "controversial",

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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic vulnerability contributes to adult ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.86, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.80, "Underlying ADHD shapes symptom presentation."),
    ("ADHD", "Comorbid Conditions", "+", 0.58, "ADHD frequently co-occurs with other difficulties that complicate recognition."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.54, "Poor nutrition worsens cognitive regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.64, "Sleep disruption affects functioning and regulation."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Stress amplifies symptoms."),

    ("Age", "Symptom Severity", "+", 0.32, "At age 32, work and life demands can make symptoms more visible."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.78, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Career Friction", "+", 0.74, "Impairment often contributes to persistent career friction."),
    ("Performance Pressure", "Functional Impairment", "+", 0.24, "Performance demands worsen visible dysfunction."),
    ("Remote Collaboration Demands", "Functional Impairment", "+", 0.10, "Emerging digital work demands begin to add cognitive load by 2010."),
    ("Career Friction", "Self-Recognition", "+", 0.44, "Repeated work difficulties increasingly support adult self-recognition by 2010."),

    ("Family Stress", "Symptom Severity", "+", 0.56, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.62, "Stable household context reduces stress."),

    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.78, "Higher SES improves healthcare access."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Income strongly affects evaluation and treatment access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.48, "Better neighborhood conditions improve care access."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.74, "More providers reduce waiting time."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.46, "Long waits still reduce diagnosis, though less sharply."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.56, "Cost remains a barrier, though less absolute than before."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.76, "Access strongly improves adult diagnosis in 2010."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.60, "Access increasingly leads to coordinated care pathways."),
    ("Care Coordination", "Workplace Accommodations", "+", 0.46, "Coordinated care can help secure workplace support."),

    ("Self-Recognition", "Diagnosis Status", "+", 0.42, "Self-recognition can meaningfully push adults toward evaluation."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.72, "Diagnostic inconsistency still creates misdiagnosis risk."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.70, "Comorbidity continues to obscure accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.66, "Misdiagnosis reduces correct diagnosis status."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.60, "Structural inequities influence institutional behavior."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.46, "Bias still increases some diagnostic error."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.38, "Bias still suppresses equitable access to diagnosis."),
    ("Cultural Norms", "Stigma", "+", 0.54, "Stigma remains present, but weaker than in earlier decades."),
    ("Stigma", "Access to Mental Health Care", "-", 0.46, "Stigma still suppresses help-seeking, but less strongly."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.40, "Gender stereotypes continue to increase diagnostic error."),

    ("Diagnosis Status", "Workplace Accommodations", "+", 0.56, "Diagnosis increasingly enables workplace accommodations by 2010."),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.42, "Accommodations can meaningfully reduce impairment."),
    ("Diagnosis Status", "Quality of Life", "+", 0.72, "Diagnosis can meaningfully improve functioning and quality of life."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life.")
]

for edge in edges:
    add_edge(*edge)

if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="2010_age_32_graph.html",
        svg_filename="2010_age_32_regions.svg"
    )