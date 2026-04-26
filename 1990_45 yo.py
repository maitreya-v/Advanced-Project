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
    "treatment": "#E2C2FF",
    "work": "#FFB7B2",
    "factor": "#D3D3D3",
    "unknown": "#D3D3D3"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical-cognitive pathway variables",
    "environment": "Environmental burden variables",
    "family": "Family-context variables",
    "access": "Socioeconomic / healthcare access variables",
    "bias": "Social-cultural / structural bias variables",
    "controversial": "Delayed-recognition pathway",
    "treatment": "1990 midlife treatment pathway, stronger than 1970 but still limited by delayed recognition and stigma",
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
    "Chronic Stress Load": "environment",

    "Family Stress": "family",
    "Home Structure Stability": "family",
    "Family History Awareness": "family",

    "Financial Status": "access",
    "Socioeconomic Status": "access",
    "Neighborhood Quality": "access",
    "Provider Availability": "access",
    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Self-Diagnosis Behavior": "controversial",
    "Clinical Guidelines Evolution": "controversial",

    "Medication Treatment": "treatment",
    "Behavioral Therapy": "treatment",
    "Treatment Access": "treatment",
    "Treatment Adherence": "treatment",
    "School Accommodations": "treatment",
    "Treatment Side Effects": "treatment",

    "Age": "factor"
}

with open("clusters.json", "r", encoding="utf-8") as f:
    node_positions = json.load(f)

fallback_positions = {
    "Medication Treatment": {"x": 260, "y": 180},
    "Behavioral Therapy": {"x": 120, "y": 180},
    "Treatment Access": {"x": 760, "y": 220},
    "Treatment Adherence": {"x": 260, "y": 300},
    "School Accommodations": {"x": 120, "y": 300},
    "Treatment Side Effects": {"x": 760, "y": 320}
}

positioned_nodes = []
graph_nodes = list(node_groups.keys())

for node in graph_nodes:
    if node in node_positions:
        x = node_positions[node]["x"]
        y = node_positions[node]["y"]
        domain = node_positions[node].get("domain", node_groups.get(node, "unknown"))
        local_domain = node_positions[node].get("local_domain", "unknown")
        confidence = node_positions[node].get("confidence", 0.0)
        color = group_colors.get(domain, group_colors.get(node_groups.get(node, "unknown")))
        positioned_nodes.append((node, x, y, color, domain, local_domain, confidence))
    elif node in fallback_positions:
        x = fallback_positions[node]["x"]
        y = fallback_positions[node]["y"]
        domain = node_groups.get(node, "treatment")
        local_domain = domain
        confidence = 0.85
        color = group_colors.get(domain)
        positioned_nodes.append((node, x, y, color, domain, local_domain, confidence))
    else:
        print(f"Warning: '{node}' not found in clusters.json")

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
        u,
        v,
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

    ("Nutrition Quality", "Symptom Severity", "-", 0.50, "Long-term nutrition impacts cognition."),
    ("Sleep Quality", "Executive Function Deficit", "-", 0.64, "Sleep affects executive functioning."),
    ("Chronic Stress Load", "Functional Impairment", "+", 0.70, "Accumulated stress worsens outcomes."),

    ("Home Structure Stability", "Family Stress", "-", 0.68, "Stable home structure reduces stress."),
    ("Family Stress", "Chronic Stress Load", "+", 0.72, "Family stress contributes to accumulated burden."),
    ("Family History Awareness", "Self-Diagnosis Behavior", "+", 0.22, "Family history somewhat supports self-recognition by 1990."),

    ("Financial Status", "Access to Mental Health Care", "+", 0.78, "Income strongly controls access."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.72, "Socioeconomic position shapes access to care."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.46, "Better neighborhood conditions improve resource access."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.64, "Provider supply improves access more than in 1970."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.78, "High evaluation cost still strongly suppresses diagnosis."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.54, "Access helps diagnosis, though adult recognition remains incomplete."),
    ("Clinical Guidelines Evolution", "Diagnosis Status", "+", 0.30, "Guideline evolution makes delayed adult recognition somewhat more plausible."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.70, "Misdiagnosis still reduces correct diagnosis status."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.66, "Structural inequities influence institutional and healthcare pathways."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.58, "Bias suppresses diagnosis in midlife."),
    ("Race / Ethnicity", "Access to Mental Health Care", "-", 0.58, "Structural inequity persists in access pathways."),

    ("Cultural Norms", "Stigma", "+", 0.78, "1990 norms still reinforce stigma, though less than in 1970."),
    ("Stigma", "Diagnosis Status", "-", 0.74, "Stigma still suppresses adult diagnosis."),
    ("Stigma", "Self-Diagnosis Behavior", "-", 0.56, "Stigma discourages self-recognition and help-seeking."),

    ("Diagnosis Status", "Medication Treatment", "+", 0.38, "By 1990, diagnosis can lead to treatment in midlife, but the pathway remains delayed and limited."),
    ("Diagnosis Status", "Behavioral Therapy", "+", 0.30, "Diagnosis can connect midlife adults to behavioral support, but less commonly than children."),
    ("Access to Mental Health Care", "Treatment Access", "+", 0.54, "Mental healthcare access supports treatment availability."),
    ("Provider Availability", "Treatment Access", "+", 0.52, "Provider supply increases the chance of accessing treatment."),
    ("Socioeconomic Status", "Treatment Access", "+", 0.56, "Higher SES improves treatment access."),
    ("Self-Diagnosis Behavior", "Treatment Access", "+", 0.26, "Self-recognition can increase help-seeking, but the pathway is still weak."),
    ("Clinical Guidelines Evolution", "Treatment Access", "+", 0.28, "Evolving clinical guidelines modestly improve treatment access."),
    ("Treatment Access", "Medication Treatment", "+", 0.42, "Treatment access can lead to medication, but midlife adult ADHD remains underrecognized."),
    ("Treatment Access", "Behavioral Therapy", "+", 0.36, "Treatment access may enable behavioral support."),
    ("Behavioral Therapy", "Functional Impairment", "-", 0.28, "Behavioral support may modestly reduce cumulative impairment."),
    ("Medication Treatment", "Symptom Severity", "-", 0.32, "Medication may reduce symptoms, but treatment effects are constrained by delayed recognition."),
    ("Medication Treatment", "Functional Impairment", "-", 0.24, "Medication may slightly reduce midlife impairment."),
    ("Treatment Adherence", "Medication Treatment", "+", 0.36, "Adherence strengthens medication effect."),
    ("Stigma", "Treatment Adherence", "-", 0.50, "Stigma reduces continued treatment engagement."),
    ("Medication Treatment", "Treatment Side Effects", "+", 0.40, "Medication can introduce side effects."),
    ("Treatment Side Effects", "Treatment Adherence", "-", 0.46, "Side effects can reduce adherence."),
    ("Treatment Side Effects", "Quality of Life", "-", 0.24, "Side effects can slightly reduce quality of life."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.36, "Diagnosis can modestly reduce impairment through explanation or support."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.56, "Diagnosis can modestly improve quality of life in midlife.")
]

for edge in edges:
    add_edge(*edge)


if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="1990_age_45_graph.html",
        svg_filename="1990_age_45_regions.svg"
    )