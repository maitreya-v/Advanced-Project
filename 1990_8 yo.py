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
    "school": "School detection pathway",
    "family": "Family response pathway",
    "access": "Healthcare access / economic barriers",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and developmental exposure variables",
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
    "Misdiagnosis Rate": "controversial",

    "Teacher Referral Rate": "school",
    "School Labeling Bias": "school",
    "Classroom Size": "school",
    "School Resources": "school",
    "Education System Pressure": "school",

    "Parental Awareness": "family",
    "Parental Denial": "family",
    "Family Stress": "family",
    "Household Stability": "family",
    "Parental Education": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Educational Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Early Life Nutrition": "environment",
    "Sleep Quality": "environment",
    "Environmental Exposure": "environment",

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
    ("Gender", "Symptom Type", "+", 0.40, "Gender norms influence which childhood behaviors are noticed."),

    ("Early Life Nutrition", "Genetic Risk", "-", 0.20, "Poor early nutrition can increase developmental vulnerability."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.54, "Poor nutrition may worsen behavioral regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.64, "Better sleep reduces behavioral dysregulation."),
    ("Environmental Exposure", "Symptom Severity", "+", 0.42, "Environmental stressors can worsen symptoms."),

    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.72, "Certain symptom patterns are more likely to trigger teacher concern."),
    ("Classroom Size", "Teacher Referral Rate", "+", 0.44, "Classroom context can increase teacher concern."),
    ("School Labeling Bias", "Teacher Referral Rate", "+", 0.70, "Behavioral labeling still strongly shapes referrals."),
    ("School Resources", "Teacher Referral Rate", "+", 0.46, "In 1990, school resources increasingly support detection."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.52, "Institutional pressure can increase school referrals."),

    ("Teacher Referral Rate", "Parental Awareness", "+", 0.78, "School concerns more reliably increase parent awareness."),
    ("Parental Denial", "Parental Awareness", "-", 0.74, "Denial still reduces recognition of child difficulties."),
    ("Parental Education", "Parental Awareness", "+", 0.60, "More educated parents better recognize childhood issues."),
    ("Parental Education", "Parental Denial", "-", 0.44, "Education reduces denial probability."),
    ("Family Stress", "Symptom Severity", "+", 0.56, "Stressful homes can amplify visible symptoms."),
    ("Household Stability", "Family Stress", "-", 0.70, "Stable homes reduce stress."),
    ("Household Stability", "Nutrition Quality", "+", 0.60, "Stable homes support better nutrition."),
    ("Family Stress", "Sleep Quality", "-", 0.56, "Stress disrupts sleep patterns."),

    ("Parental Awareness", "Diagnosis Status", "+", 0.64, "Parental awareness meaningfully supports diagnosis by 1990."),
    ("Socioeconomic Status", "Educational Access", "+", 0.72, "Higher SES improves educational access."),
    ("Educational Access", "Teacher Referral Rate", "+", 0.40, "Better systems may detect issues earlier."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.70, "Higher SES improves access to care."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.78, "Affordability strongly controls access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.46, "Better neighborhoods provide more resources."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.62, "Provider supply improves access more than in 1970."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.72, "Cost remains a substantial barrier to evaluation."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.66, "Access meaningfully improves diagnosis likelihood."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.68, "Structural inequities influence institutional behavior."),
    ("Institutional Bias", "Teacher Referral Rate", "+", 0.60, "Bias affects referral and labeling patterns."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.54, "Bias suppresses fair diagnosis access."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.56, "Misdiagnosis reduces accurate identification."),

    ("Cultural Norms", "Stigma", "+", 0.74, "Stigma remains significant, but weaker than in 1970."),
    ("Stigma", "Diagnosis Status", "-", 0.68, "Stigma still suppresses recognition and diagnosis."),

    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.56, "Diagnosis can improve support and outcomes.")
]

for edge in edges:
    add_edge(*edge)

if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="1990_age_8_graph.html",
        svg_filename="1990_age_8_regions.svg"
    )