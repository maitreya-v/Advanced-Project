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
    "work": "Workplace and adult-support ecosystem",
    "family": "Family and household context variables",
    "access": "Healthcare ecosystem pathway",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and chronic burden variables",
    "controversial": "Modern discourse / recognition pathway",
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
    "Career Friction": "work",
    "Remote Work Flexibility": "work",
    "Support Ecosystem": "work",
    "Productivity Tooling": "work",

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Waiting Time for Assessment": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Care Coordination": "access",
    "Telehealth Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Sleep Quality": "environment",
    "Chronic Stress Load": "environment",
    "Digital Overload": "environment",

    "Diagnostic Criteria Variability": "controversial",
    "Misdiagnosis Rate": "controversial",
    "Self-Recognition": "controversial",
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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic vulnerability contributes to adult ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.86, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.80, "Underlying ADHD shapes symptom presentation."),
    ("ADHD", "Comorbid Conditions", "+", 0.60, "ADHD frequently co-occurs with other difficulties that complicate recognition."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.56, "Poor nutrition worsens cognitive regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.66, "Sleep disruption affects functioning and regulation."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Stress amplifies symptoms."),
    ("Digital Overload", "Symptom Severity", "+", 0.46, "Digital overload can intensify attention dysregulation in 2026."),

    ("Age", "Symptom Severity", "+", 0.34, "At age 32, work and life demands can make symptoms highly visible."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.78, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Career Friction", "+", 0.76, "Impairment often contributes to recurring career friction."),
    ("Career Friction", "Self-Recognition", "+", 0.58, "Repeated work difficulties strongly support self-recognition by 2026."),
    ("Remote Work Flexibility", "Functional Impairment", "-", 0.26, "Flexible work can partially buffer impairment in modern contexts."),
    ("Productivity Tooling", "Functional Impairment", "-", 0.22, "Modern productivity tools can modestly reduce impairment burden."),

    ("Family Stress", "Symptom Severity", "+", 0.56, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.60, "Stable household context reduces stress."),

    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.78, "Higher SES improves healthcare access."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Income strongly affects evaluation and treatment access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.50, "Better neighborhood conditions improve care access."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.82, "More providers reduce waiting time in 2026."),
    ("Telehealth Access", "Access to Mental Health Care", "+", 0.72, "Telehealth expands access to evaluation and support."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.34, "Long waits still reduce diagnosis, but less sharply than before."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.46, "Cost remains a barrier, though less absolute than earlier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.86, "Access strongly improves adult diagnosis in 2026."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.72, "Access increasingly leads to coordinated care pathways."),
    ("Care Coordination", "Support Ecosystem", "+", 0.76, "Coordinated care helps build a broader support ecosystem."),
    ("Diagnosis Status", "Support Ecosystem", "+", 0.72, "Diagnosis can connect adults to broader support structures."),

    ("Social Media Awareness", "Self-Recognition", "+", 0.62, "Online awareness strongly supports adult self-recognition."),
    ("Self-Recognition", "Diagnosis Status", "+", 0.60, "Self-recognition can strongly push adults toward evaluation."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.64, "Diagnostic inconsistency still creates misdiagnosis risk."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.66, "Comorbidity continues to obscure accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.56, "Misdiagnosis reduces correct diagnosis status."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Modern overdiagnosis discourse is clearly present in 2026."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.52, "Structural inequities still influence institutions."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.34, "Bias still creates some diagnostic error."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.24, "Bias still suppresses equitable access to diagnosis."),
    ("Cultural Norms", "Stigma", "+", 0.40, "Stigma remains present, but much weaker than earlier decades."),
    ("Stigma", "Access to Mental Health Care", "-", 0.30, "Stigma still suppresses help-seeking somewhat."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.30, "Gender stereotypes still create some diagnostic error."),

    ("Diagnosis Status", "Workplace Accommodations", "+", 0.70, "Diagnosis strongly enables workplace accommodations."),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.50, "Accommodations can meaningfully reduce impairment."),
    ("Support Ecosystem", "Quality of Life", "+", 0.66, "Support systems improve functioning and quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.82, "Diagnosis can strongly improve functioning and quality of life."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life.")
]

for edge in edges:
    add_edge(*edge)

if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="2026_age_32_graph.html",
        svg_filename="2026_age_32_regions.svg"
    )