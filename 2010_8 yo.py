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
    "clinical": "Clinical symptom pathway variables",
    "school": "School support and detection pathway",
    "family": "Family advocacy pathway",
    "access": "Healthcare access pathway",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and developmental exposure variables",
    "controversial": "Modern treatment and diagnostic pressure pathway",
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
    "Misdiagnosis Rate": "controversial",

    "Teacher Referral Rate": "school",
    "School Resources": "school",
    "Education System Pressure": "school",
    "School Support Plan": "school",

    "Parental Awareness": "family",
    "Parental Advocacy": "family",
    "Family Stress": "family",
    "Parental Education": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Early Life Nutrition": "environment",
    "Sleep Quality": "environment",
    "Environmental Exposure": "environment",

    "Treatment Dependency": "controversial",
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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic liability contributes strongly to childhood ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.90, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.84, "Underlying ADHD shapes visible behavioral presentation."),

    ("Age", "Symptom Severity", "+", 0.44, "At age 8, symptoms are highly visible through behavior and school functioning."),
    ("Gender", "Symptom Type", "+", 0.38, "Gender norms influence which childhood behaviors are noticed."),

    ("Early Life Nutrition", "Genetic Risk", "-", 0.18, "Early nutrition can modulate developmental vulnerability."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.56, "Poor nutrition may worsen behavioral regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.66, "Better sleep reduces dysregulation."),
    ("Environmental Exposure", "Symptom Severity", "+", 0.40, "Environmental stressors can worsen symptoms."),

    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.74, "Certain symptom patterns are likely to trigger teacher concern."),
    ("School Resources", "Teacher Referral Rate", "+", 0.64, "By 2010, school resources strongly support detection."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.56, "Institutional pressure can increase school referral."),
    ("Teacher Referral Rate", "Parental Awareness", "+", 0.84, "Teacher concern strongly raises parental awareness."),

    ("ParentalEducationTypo", "Parental Awareness", "+", 0.01, "Placeholder removed."),
]
edges = [e for e in edges if e[0] != "ParentalEducationTypo"]

edges.extend([
    ("Parental Education", "Parental Awareness", "+", 0.64, "More educated parents better recognize childhood issues."),
    ("Parental Awareness", "Parental Advocacy", "+", 0.74, "Awareness increasingly leads to active parent advocacy."),
    ("Parental Advocacy", "Diagnosis Status", "+", 0.72, "Advocacy strongly supports evaluation and diagnosis."),
    ("Family Stress", "Symptom Severity", "+", 0.54, "Family stress can amplify visible symptoms."),
    ("Family Stress", "Sleep Quality", "-", 0.56, "Stress disrupts sleep patterns."),
    ("Parental Advocacy", "School Support Plan", "+", 0.66, "Advocating families are more likely to secure formal school supports."),

    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.74, "Higher SES improves access to evaluation."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.78, "Affordability strongly controls access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.48, "Better neighborhoods provide more resources."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.78, "Provider supply strongly improves access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.62, "Cost still remains a barrier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.82, "Access strongly improves diagnosis likelihood."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.60, "Access increasingly leads to coordinated care in 2010."),
    ("Care Coordination", "School Support Plan", "+", 0.58, "Care coordination improves school support planning."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.62, "Structural inequities influence institutional behavior."),
    ("Institutional Bias", "Teacher Referral Rate", "+", 0.46, "Bias still affects referral patterns."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.44, "Bias suppresses equitable diagnosis access."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.46, "Misdiagnosis still reduces accurate identification."),
    ("Cultural Norms", "Stigma", "+", 0.58, "Stigma remains, but weaker than in 1990."),
    ("Stigma", "Diagnosis Status", "-", 0.46, "Stigma still suppresses recognition somewhat."),

    ("Diagnosis Status", "School Support Plan", "+", 0.74, "Diagnosis can lead to formalized school support structures."),
    ("Diagnosis Status", "Treatment Dependency", "+", 0.58, "Diagnosis increasingly leads into treatment pathways."),
    ("Treatment Dependency", "Functional Impairment", "-", 0.48, "Treatment can meaningfully reduce impairment."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Overdiagnosis discourse is visible by 2010."),

    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.74, "Diagnosis can strongly improve support and quality of life.")
])

for edge in edges:
    add_edge(*edge)

if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="2010_age_8_graph.html",
        svg_filename="2010_age_8_regions.svg"
    )