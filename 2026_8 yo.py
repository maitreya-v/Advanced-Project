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
    "clinical": "Clinical symptom pathway variables",
    "school": "School support and detection ecosystem",
    "family": "Family awareness and advocacy pathway",
    "access": "Healthcare ecosystem pathway",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and developmental exposure variables",
    "controversial": "Modern diagnostic pressure / discourse pathway",
    "treatment": "2026 childhood treatment pathway including medication, behavioral therapy, school accommodations, digital supports, telehealth, adherence, and side effects",
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
    "Learning Accommodations": "school",

    "Parental Awareness": "family",
    "Parental Advocacy": "family",
    "Family Stress": "family",
    "Parental Education": "family",
    "Peer Comparison": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Care Coordination": "access",
    "Telehealth Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Early Life Nutrition": "environment",
    "Sleep Quality": "environment",
    "Environmental Exposure": "environment",
    "Digital Media Exposure": "environment",

    "Treatment Dependency": "controversial",
    "Overdiagnosis Pressure": "controversial",
    "Social Media Awareness": "controversial",

    "Medication Treatment": "treatment",
    "Behavioral Therapy": "treatment",
    "Treatment Access": "treatment",
    "Treatment Adherence": "treatment",
    "School Accommodations": "treatment",
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
    "School Accommodations": {"x": 120, "y": 300},
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
    net.add_edge(
        u,
        v,
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
    ("Gender", "Symptom Type", "+", 0.36, "Gender norms still influence which childhood behaviors are noticed."),

    ("Early Life Nutrition", "Genetic Risk", "-", 0.16, "Early nutrition can modulate developmental vulnerability."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.58, "Poor nutrition may worsen behavioral regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.68, "Better sleep reduces dysregulation."),
    ("Environmental Exposure", "Symptom Severity", "+", 0.34, "Environmental stressors can worsen symptoms."),
    ("Digital Media Exposure", "Symptom Severity", "+", 0.40, "High digital media exposure can intensify attention dysregulation in 2026."),

    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.76, "Certain symptom patterns are likely to trigger teacher concern."),
    ("School Resources", "Teacher Referral Rate", "+", 0.74, "School resources strongly support detection in 2026."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.54, "Institutional pressure still influences school referral."),
    ("Teacher Referral Rate", "Parental Awareness", "+", 0.88, "Teacher concerns strongly increase parental awareness."),
    ("Peer Comparison", "Parental Awareness", "+", 0.62, "Peer comparison strongly contributes to family noticing."),

    ("Parental Education", "Parental Awareness", "+", 0.66, "More educated parents better recognize childhood issues."),
    ("Parental Awareness", "Parental Advocacy", "+", 0.82, "Awareness readily turns into family advocacy in 2026."),
    ("Parental Advocacy", "Diagnosis Status", "+", 0.82, "Advocacy strongly supports evaluation and diagnosis."),
    ("Parental Advocacy", "School Support Plan", "+", 0.76, "Advocating families are highly likely to secure formal school supports."),
    ("Family Stress", "Symptom Severity", "+", 0.52, "Family stress can amplify visible symptoms."),

    ("Diagnosis Status", "School Support Plan", "+", 0.84, "Diagnosis strongly enables formal school support."),
    ("School Support Plan", "Learning Accommodations", "+", 0.82, "Support planning leads to concrete learning accommodations."),
    ("Learning Accommodations", "Functional Impairment", "-", 0.42, "Accommodations reduce school-related impairment."),

    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.76, "Higher SES improves access to evaluation."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.78, "Affordability strongly controls access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.50, "Better neighborhoods provide more resources."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.86, "Provider supply strongly improves access."),
    ("Telehealth Access", "Access to Mental Health Care", "+", 0.68, "Telehealth expands access to evaluation and care in 2026."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.88, "Access strongly improves diagnosis likelihood."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.72, "Access increasingly leads to coordinated care pathways."),
    ("Care Coordination", "School Support Plan", "+", 0.72, "Coordinated care improves school support planning."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.50, "Cost remains a barrier, though weaker than before."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.58, "Structural inequities still influence institutional behavior."),
    ("Institutional Bias", "Teacher Referral Rate", "+", 0.36, "Bias still affects referral patterns."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.30, "Bias still suppresses equitable diagnosis access."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.40, "Misdiagnosis still reduces accurate identification."),
    ("Cultural Norms", "Stigma", "+", 0.42, "Stigma remains, but much weaker than earlier decades."),
    ("Stigma", "Diagnosis Status", "-", 0.34, "Stigma still suppresses recognition somewhat."),
    ("Social Media Awareness", "Parental Awareness", "+", 0.58, "Online awareness contributes to parent recognition in 2026."),

    ("Diagnosis Status", "Treatment Access", "+", 0.88, "Diagnosis strongly opens structured treatment pathways for children in 2026."),
    ("Access to Mental Health Care", "Treatment Access", "+", 0.88, "Healthcare access strongly controls treatment availability."),
    ("Telehealth Access", "Telehealth Treatment", "+", 0.78, "Telehealth directly increases remote treatment options."),
    ("Telehealth Treatment", "Treatment Access", "+", 0.70, "Telehealth expands practical treatment access."),
    ("Provider Availability", "Treatment Access", "+", 0.84, "Provider supply strongly improves treatment access."),
    ("Care Coordination", "Treatment Access", "+", 0.76, "Coordinated care improves treatment continuity."),
    ("Socioeconomic Status", "Treatment Access", "+", 0.72, "Higher SES improves treatment access and continuity."),

    ("Treatment Access", "Medication Treatment", "+", 0.88, "Treatment access makes medication treatment highly likely when clinically appropriate."),
    ("Treatment Access", "Behavioral Therapy", "+", 0.82, "Treatment access enables behavioral therapy."),
    ("Treatment Access", "School Accommodations", "+", 0.84, "Treatment access supports formal school accommodations."),
    ("Treatment Access", "Digital Therapeutics", "+", 0.62, "Modern treatment access may include app-based or digital ADHD tools."),

    ("Medication Treatment", "Symptom Severity", "-", 0.78, "Medication can substantially reduce childhood symptom burden."),
    ("Behavioral Therapy", "Symptom Severity", "-", 0.50, "Behavioral therapy improves self-regulation and routines."),
    ("Behavioral Therapy", "Functional Impairment", "-", 0.60, "Behavioral therapy reduces practical impairment."),
    ("School Accommodations", "Functional Impairment", "-", 0.68, "School accommodations reduce academic impairment."),
    ("Digital Therapeutics", "Symptom Severity", "-", 0.36, "Digital tools may modestly improve attention and structure."),
    ("Digital Therapeutics", "Treatment Adherence", "+", 0.34, "Digital reminders and tracking can improve adherence."),

    ("Treatment Adherence", "Medication Treatment", "+", 0.72, "Adherence increases real-world medication benefit."),
    ("Treatment Adherence", "Behavioral Therapy", "+", 0.66, "Consistent participation improves therapy effect."),
    ("Treatment Dependency", "Treatment Access", "+", 0.66, "Diagnosis often leads into structured treatment pathways."),
    ("Treatment Dependency", "Functional Impairment", "-", 0.58, "Treatment can meaningfully reduce impairment."),
    ("Stigma", "Treatment Adherence", "-", 0.30, "Stigma can still reduce consistent treatment participation."),
    ("Medication Treatment", "Treatment Side Effects", "+", 0.52, "Medication side effects remain relevant to tolerability."),
    ("Treatment Side Effects", "Treatment Adherence", "-", 0.44, "Side effects can reduce adherence."),
    ("Treatment Side Effects", "Quality of Life", "-", 0.18, "Side effects can slightly reduce quality of life."),

    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.58, "Overdiagnosis discourse is highly visible in 2026."),
    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.82, "Diagnosis can strongly improve support and quality of life.")
]

for edge in edges:
    add_edge(*edge)



if __name__ == "__main__":
    save_graph_with_fuzzy_background(
        net=net,
        positioned_nodes=positioned_nodes,
        group_colors=group_colors,
        html_filename="2026_age_8_graph.html",
        svg_filename="2026_age_8_regions.svg"
    )