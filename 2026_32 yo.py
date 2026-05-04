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
    "clinical": "Adult ADHD clinical and impairment variables",
    "work": "Adult work and productivity pathway",
    "family": "Adult family and household context",
    "access": "Modern healthcare and digital access pathway",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Lifestyle and environmental burden variables",
    "controversial": "Modern diagnostic discourse and self-recognition pathway",
    "treatment": "2026 adult treatment pathway including medication, therapy, telehealth, digital tools, workplace support, adherence, and side effects",
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
    "Executive Function Deficit": "clinical",
    "Misdiagnosis Rate": "controversial",

    "Employment Instability": "work",
    "Performance Pressure": "work",
    "Workplace Accommodations": "work",
    "Remote Work Flexibility": "work",

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Care Coordination": "access",
    "Telehealth Access": "access",
    "Online Health Information": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Sleep Quality": "environment",
    "Physical Activity": "environment",
    "Screen Time": "environment",
    "Digital Media Exposure": "environment",
    "Chronic Stress Load": "environment",

    "Self-Diagnosis Behavior": "controversial",
    "Social Media Awareness": "controversial",
    "Diagnostic Criteria Variability": "controversial",
    "Treatment Dependency": "controversial",
    "Overdiagnosis Pressure": "controversial",

    "Medication Treatment": "treatment",
    "Behavioral Therapy": "treatment",
    "Treatment Access": "treatment",
    "Treatment Adherence": "treatment",
    "Workplace Support": "treatment",
    "Digital Therapeutics": "treatment",
    "Telehealth Treatment": "treatment",
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
    "Digital Therapeutics": {"x": 480, "y": 300},
    "Telehealth Treatment": {"x": 620, "y": 300},
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
    ("Genetic Risk", "ADHD", "+", 0.90, "Genetic vulnerability contributes to adult ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.88, "Underlying ADHD increases adult symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.82, "ADHD shapes inattentive, hyperactive, or combined presentation."),
    ("ADHD", "Executive Function Deficit", "+", 0.88, "ADHD strongly affects executive functioning."),
    ("ADHD", "Comorbid Conditions", "+", 0.68, "ADHD commonly co-occurs with anxiety, mood, or learning difficulties."),
    ("Age", "Symptom Severity", "-", 0.24, "At age 32, overt hyperactivity may reduce but inattentive impairment can remain."),
    ("Gender", "Symptom Type", "+", 0.34, "Gender norms still influence which adult symptoms are noticed."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.46, "Better nutrition may support regulation and attention."),
    ("Sleep Quality", "Symptom Severity", "-", 0.70, "Better sleep improves attention and regulation."),
    ("Physical Activity", "Symptom Severity", "-", 0.50, "Physical activity may reduce symptom burden."),
    ("Screen Time", "Symptom Severity", "+", 0.34, "Screen exposure may affect attention."),
    ("Digital Media Exposure", "Symptom Severity", "+", 0.36, "Digital media exposure can intensify attention dysregulation."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.68, "Stress amplifies adult symptoms."),

    ("Symptom Severity", "Functional Impairment", "+", 0.84, "Higher symptoms increase occupational and daily impairment."),
    ("Executive Function Deficit", "Functional Impairment", "+", 0.84, "Executive dysfunction creates practical impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.74, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Employment Instability", "+", 0.68, "Impairment can destabilize employment."),
    ("Performance Pressure", "Functional Impairment", "+", 0.34, "Performance demands make executive dysfunction more visible."),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.50, "Workplace accommodations reduce impairment."),
    ("Remote Work Flexibility", "Functional Impairment", "-", 0.42, "Flexible work can reduce adult ADHD-related impairment."),

    ("Family Stress", "Symptom Severity", "+", 0.54, "Adult family stress can intensify symptoms."),
    ("Household Stability", "Family Stress", "-", 0.64, "Stable household context reduces family stress."),

    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.82, "Higher SES improves access to specialists and services."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Income controls access to healthcare."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.50, "Better neighborhood conditions improve resource access."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.84, "More providers improve assessment chances."),
    ("Telehealth Access", "Access to Mental Health Care", "+", 0.72, "Telehealth expands assessment and care access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.52, "Evaluation cost remains a diagnosis barrier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.86, "Access to care strongly affects adult diagnosis."),
    ("Online Health Information", "Self-Diagnosis Behavior", "+", 0.70, "Online information increases adult self-recognition."),
    ("Social Media Awareness", "Self-Diagnosis Behavior", "+", 0.66, "Social media awareness increases self-recognition."),
    ("Self-Diagnosis Behavior", "Diagnosis Status", "+", 0.58, "Self-recognition increases help-seeking."),
    ("Care Coordination", "Functional Impairment", "-", 0.42, "Coordinated care can reduce impairment."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.56, "Structural inequities influence institutions and healthcare pathways."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.50, "Bias increases diagnostic errors."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.36, "Bias suppresses equitable diagnosis access."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.66, "Different interpretations increase misdiagnosis risk."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.64, "Comorbidity can obscure accurate ADHD diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.62, "Misdiagnosis reduces accurate diagnosis."),
    ("Cultural Norms", "Stigma", "+", 0.44, "Cultural norms shape stigma."),
    ("Stigma", "Diagnosis Status", "-", 0.34, "Stigma reduces willingness to seek diagnosis."),
    ("Stigma", "Access to Mental Health Care", "-", 0.30, "Stigma suppresses help-seeking."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.40, "Gender stereotypes still increase diagnostic error."),

    ("Diagnosis Status", "Treatment Access", "+", 0.82, "By 2026, adult diagnosis commonly opens treatment pathways."),
    ("Access to Mental Health Care", "Treatment Access", "+", 0.86, "Mental healthcare access strongly improves treatment availability."),
    ("Provider Availability", "Treatment Access", "+", 0.80, "Provider supply improves adult treatment access."),
    ("Telehealth Access", "Telehealth Treatment", "+", 0.78, "Telehealth directly improves remote treatment availability."),
    ("Telehealth Treatment", "Treatment Access", "+", 0.72, "Telehealth expands practical treatment access."),
    ("Socioeconomic Status", "Treatment Access", "+", 0.74, "Higher SES improves treatment access and continuity."),
    ("Self-Diagnosis Behavior", "Treatment Access", "+", 0.56, "Self-recognition increases treatment seeking."),
    ("Care Coordination", "Treatment Access", "+", 0.66, "Coordinated care improves treatment continuity."),

    ("Treatment Access", "Medication Treatment", "+", 0.80, "Treatment access makes medication more likely."),
    ("Treatment Access", "Behavioral Therapy", "+", 0.74, "Treatment access supports behavioral therapy."),
    ("Treatment Access", "Workplace Support", "+", 0.54, "Treatment access can support workplace accommodations."),
    ("Treatment Access", "Digital Therapeutics", "+", 0.60, "Modern care may include digital ADHD tools."),

    ("Medication Treatment", "Symptom Severity", "-", 0.72, "Medication can reduce adult symptom severity."),
    ("Medication Treatment", "Functional Impairment", "-", 0.50, "Medication may reduce adult impairment."),
    ("Behavioral Therapy", "Symptom Severity", "-", 0.42, "Behavioral therapy can modestly reduce symptom expression."),
    ("Behavioral Therapy", "Functional Impairment", "-", 0.54, "Behavioral therapy reduces practical impairment."),
    ("Workplace Support", "Functional Impairment", "-", 0.50, "Workplace support reduces occupational impairment."),
    ("Digital Therapeutics", "Symptom Severity", "-", 0.34, "Digital tools may modestly improve attention and structure."),
    ("Digital Therapeutics", "Treatment Adherence", "+", 0.36, "Digital tracking and reminders can improve adherence."),

    ("Treatment Adherence", "Medication Treatment", "+", 0.66, "Adherence increases medication benefit."),
    ("Treatment Adherence", "Behavioral Therapy", "+", 0.60, "Participation improves behavioral therapy effect."),
    ("Online Health Information", "Treatment Adherence", "+", 0.38, "Online information can improve understanding and follow-up."),
    ("Treatment Dependency", "Treatment Access", "+", 0.58, "Diagnosis often leads into structured treatment pathways."),
    ("Stigma", "Treatment Adherence", "-", 0.34, "Stigma can reduce treatment continuation."),
    ("Medication Treatment", "Treatment Side Effects", "+", 0.50, "Medication side effects affect tolerability."),
    ("Treatment Side Effects", "Treatment Adherence", "-", 0.48, "Side effects can reduce adherence."),
    ("Treatment Side Effects", "Quality of Life", "-", 0.22, "Side effects can slightly reduce quality of life."),

    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.48, "Overdiagnosis discourse affects diagnosis patterns."),
    ("Diagnosis Status", "Functional Impairment", "-", 0.54, "Diagnosis can reduce impairment through treatment and support."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.70, "Diagnosis can improve quality of life through support and treatment.")
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