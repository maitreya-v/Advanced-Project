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
    "environment": "Environmental and lifestyle burden variables",
    "family": "Family-context variables",
    "access": "Socioeconomic / healthcare access variables",
    "bias": "Social-cultural / structural bias variables",
    "controversial": "Delayed adult recognition pathway",
    "treatment": "2010 midlife treatment pathway with improved adult recognition but weaker effect than childhood pathways",
    "work": "Workplace and adult functioning pathway",
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
    "Comorbid Conditions": "clinical",
    "Misdiagnosis Rate": "controversial",

    "Sleep Quality": "environment",
    "Nutrition Quality": "environment",
    "Physical Activity": "environment",
    "Screen Time": "environment",
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
    "Online Health Information": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",
    "Gender Bias": "bias",

    "Self-Diagnosis Behavior": "controversial",
    "Clinical Guidelines Evolution": "controversial",
    "Diagnostic Criteria Variability": "controversial",

    "Workplace Accommodations": "work",
    "Employment Instability": "work",

    "Medication Treatment": "treatment",
    "Behavioral Therapy": "treatment",
    "Treatment Access": "treatment",
    "Treatment Adherence": "treatment",
    "Workplace Support": "treatment",
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
    "Workplace Support": {"x": 120, "y": 300},
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

    EDGE_COLORS = {
        "+": "rgba(111, 191, 159, 0.85)",  # pastel teal-green
        "-": "rgba(217, 140, 140, 0.85)"   # dusty rose
    }

    net.add_edge(
        u,
        v,
        color=EDGE_COLORS[sign],
        width=max(2, strength * 6),
        arrows="to",
        title=f"Effect: {'Positive' if sign == '+' else 'Negative'}\nWhy: {explanation}\nStrength: {strength:.2f}"
    )

edges = [
    ("Genetic Risk", "ADHD", "+", 0.90, "Genetic vulnerability contributes strongly to lifelong ADHD."),
    ("ADHD", "Executive Function Deficit", "+", 0.90, "Underlying ADHD strongly affects executive functioning."),
    ("ADHD", "Comorbid Conditions", "+", 0.66, "ADHD commonly co-occurs with anxiety, mood, or other conditions."),
    ("Executive Function Deficit", "Functional Impairment", "+", 0.84, "Executive dysfunction increases cumulative impairment."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Greater symptom burden worsens daily functioning."),
    ("Age", "Functional Impairment", "+", 0.36, "By age 45, cumulative untreated difficulties can compound impairment."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.46, "Long-term nutrition may support cognitive regulation."),
    ("Sleep Quality", "Executive Function Deficit", "-", 0.66, "Sleep affects executive functioning."),
    ("Physical Activity", "Symptom Severity", "-", 0.42, "Physical activity may reduce symptom burden."),
    ("Screen Time", "Symptom Severity", "+", 0.30, "Screen exposure is increasingly discussed as affecting attention."),
    ("Chronic Stress Load", "Functional Impairment", "+", 0.70, "Accumulated stress worsens outcomes."),

    ("Home Structure Stability", "Family Stress", "-", 0.66, "Stable home structure reduces stress."),
    ("Family Stress", "Chronic Stress Load", "+", 0.72, "Family stress contributes to accumulated burden."),
    ("Family History Awareness", "Self-Diagnosis Behavior", "+", 0.42, "Family history increasingly supports self-recognition by 2010."),

    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Income strongly controls access."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.78, "Socioeconomic position shapes access to care."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.48, "Better neighborhood conditions improve resource access."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.76, "Provider supply improves access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.70, "Evaluation cost still suppresses diagnosis."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.72, "Access helps adult diagnosis."),
    ("Online Health Information", "Self-Diagnosis Behavior", "+", 0.66, "Online information increases self-recognition."),
    ("Online Health Information", "Diagnosis Status", "+", 0.50, "Online information can lead adults to seek evaluation."),
    ("Self-Diagnosis Behavior", "Diagnosis Status", "+", 0.48, "Self-recognition increases diagnosis-seeking."),
    ("Clinical Guidelines Evolution", "Diagnosis Status", "+", 0.52, "Guideline evolution improves adult ADHD recognition."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.68, "Diagnostic variation still contributes to misdiagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.66, "Misdiagnosis reduces correct diagnosis status."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.62, "Structural inequities influence institutional and healthcare pathways."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.50, "Bias suppresses fair diagnosis."),
    ("Race / Ethnicity", "Access to Mental Health Care", "-", 0.50, "Structural inequity persists in access pathways."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.44, "Gender stereotypes still contribute to diagnostic error."),
    ("Cultural Norms", "Stigma", "+", 0.62, "Cultural beliefs shape stigma."),
    ("Stigma", "Diagnosis Status", "-", 0.56, "Stigma suppresses adult diagnosis."),
    ("Stigma", "Self-Diagnosis Behavior", "-", 0.44, "Stigma discourages self-recognition and help-seeking."),

    ("Functional Impairment", "Employment Instability", "+", 0.68, "Impairment can destabilize employment."),
    ("Employment Instability", "Diagnosis Status", "+", 0.38, "Work problems can trigger assessment-seeking."),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.46, "Workplace accommodations can reduce impairment."),

    ("Diagnosis Status", "Medication Treatment", "+", 0.56, "By 2010, midlife adult diagnosis can lead to medication treatment."),
    ("Diagnosis Status", "Behavioral Therapy", "+", 0.48, "Diagnosis can connect midlife adults to behavioral support."),
    ("Access to Mental Health Care", "Treatment Access", "+", 0.72, "Healthcare access supports treatment availability."),
    ("Provider Availability", "Treatment Access", "+", 0.68, "Provider availability improves treatment access."),
    ("Socioeconomic Status", "Treatment Access", "+", 0.70, "Higher SES improves treatment access and continuity."),
    ("Online Health Information", "Treatment Adherence", "+", 0.32, "Online information can improve treatment understanding."),
    ("Self-Diagnosis Behavior", "Treatment Access", "+", 0.46, "Self-recognition increases treatment-seeking."),
    ("Clinical Guidelines Evolution", "Treatment Access", "+", 0.44, "Guideline evolution improves adult treatment pathways."),
    ("Care Coordination", "Treatment Access", "+", 0.54, "Care coordination supports treatment continuity."),
    ("Treatment Access", "Medication Treatment", "+", 0.62, "Treatment access can lead to medication."),
    ("Treatment Access", "Behavioral Therapy", "+", 0.56, "Treatment access can enable behavioral support."),
    ("Treatment Access", "Workplace Support", "+", 0.40, "Treatment access can support workplace accommodations."),
    ("Medication Treatment", "Symptom Severity", "-", 0.52, "Medication can reduce symptoms, but cumulative midlife burden remains."),
    ("Medication Treatment", "Functional Impairment", "-", 0.38, "Medication can modestly reduce midlife impairment."),
    ("Behavioral Therapy", "Functional Impairment", "-", 0.40, "Behavioral therapy can reduce practical impairment."),
    ("Workplace Support", "Functional Impairment", "-", 0.42, "Workplace support reduces occupational impairment."),
    ("Treatment Adherence", "Medication Treatment", "+", 0.50, "Adherence strengthens medication effect."),
    ("Treatment Adherence", "Behavioral Therapy", "+", 0.48, "Participation improves behavioral therapy impact."),
    ("Stigma", "Treatment Adherence", "-", 0.48, "Stigma reduces continued treatment engagement."),
    ("Medication Treatment", "Treatment Side Effects", "+", 0.46, "Medication can introduce side effects."),
    ("Treatment Side Effects", "Treatment Adherence", "-", 0.48, "Side effects can reduce adherence."),
    ("Treatment Side Effects", "Quality of Life", "-", 0.24, "Side effects can slightly reduce quality of life."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.44, "Diagnosis can reduce impairment through support and treatment."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.60, "Diagnosis can improve quality of life in midlife.")
]

for edge in edges:
    add_edge(*edge)



if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="2010_age_45_graph.html",
        svg_filename="2010_age_45_regions.svg"
    )