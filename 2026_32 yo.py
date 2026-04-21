from pyvis.network import Network
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

group_colors = {
    "core": "#1f77b4",
    "clinical": "#2ca02c",
    "work": "#17becf",
    "family": "#8c564b",
    "access": "#9467bd",
    "bias": "#bcbd22",
    "controversial": "#ff4d4d",
    "factor": "#dddddd"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical impairment variables",
    "work": "Workplace and adult-support ecosystem",
    "family": "Family and household context variables",
    "access": "Healthcare ecosystem pathway",
    "bias": "Social-cultural bias / stigma variables",
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

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Waiting Time for Assessment": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",

    "Diagnostic Criteria Variability": "controversial",
    "Misdiagnosis Rate": "controversial",
    "Self-Recognition": "controversial",
    "Social Media Awareness": "controversial",
    "Overdiagnosis Pressure": "controversial",

    "Age": "factor"
}

positioned_nodes = [
    ("ADHD", 0, 0),
    ("Diagnosis Status", 0, 350),

    ("Age", -500, -200),
    ("Genetic Risk", -300, -80),
    ("Symptom Severity", -200, -200),
    ("Symptom Type", -200, -80),
    ("Comorbid Conditions", -100, -300),
    ("Functional Impairment", -300, 300),

    ("Family Stress", -380, 130),
    ("Household Stability", -500, 320),

    ("Workplace Accommodations", 520, -220),
    ("Career Friction", 120, -420),
    ("Remote Work Flexibility", 300, -500),
    ("Support Ecosystem", 120, 520),

    ("Access to Mental Health Care", 500, 200),
    ("Provider Availability", 650, 80),
    ("Waiting Time for Assessment", 500, 350),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -80),
    ("Care Coordination", 650, 320),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Gender Bias", 220, -300),

    ("Diagnostic Criteria Variability", 300, 420),
    ("Misdiagnosis Rate", 140, 500),
    ("Self-Recognition", 320, 560),
    ("Social Media Awareness", 320, -120),
    ("Overdiagnosis Pressure", 500, 560),

    ("Quality of Life", -500, 450),
]

for node, x, y in positioned_nodes:
    group = node_groups.get(node, "factor")
    net.add_node(
        node,
        label=node if node != "ADHD" else "ADHD (Underlying Disorder)",
        color=group_colors[group],
        size=45 if node == "ADHD" else 40 if node == "Diagnosis Status" else 30 if node == "Quality of Life" else 25,
        x=x, y=y,
        fixed=True, physics=False,
        font={"size": 18 if node in ["ADHD", "Diagnosis Status"] else 13, "color": "black"},
        title=f"Node: {node}\nCluster: {group.upper()}\nDescription: {group_descriptions[group]}"
    )

def add_edge(u, v, sign, strength, explanation):
    net.add_edge(
        u, v,
        label=sign,
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
    ("Age", "Symptom Severity", "+", 0.34, "At age 32, work and life demands can make symptoms highly visible."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.78, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Career Friction", "+", 0.76, "Impairment often contributes to recurring career friction."),
    ("Career Friction", "Self-Recognition", "+", 0.58, "Repeated work difficulties strongly support self-recognition by 2026."),
    ("Remote Work Flexibility", "Functional Impairment", "-", 0.26, "Flexible work can partially buffer impairment in modern contexts."),
    ("Family Stress", "Symptom Severity", "+", 0.56, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.60, "Stable household context reduces stress."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.78, "Higher SES improves healthcare access."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.82, "More providers reduce waiting time in 2026."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.34, "Long waits still reduce diagnosis, but less sharply than before."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.46, "Cost remains a barrier, though less absolute than earlier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.86, "Access strongly improves adult diagnosis in 2026."),
    ("Social Media Awareness", "Self-Recognition", "+", 0.62, "Online awareness strongly supports adult self-recognition."),
    ("Self-Recognition", "Diagnosis Status", "+", 0.60, "Self-recognition can strongly push adults toward evaluation."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.64, "Diagnostic inconsistency still creates misdiagnosis risk."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.66, "Comorbidity continues to obscure accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.56, "Misdiagnosis reduces correct diagnosis status."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Modern overdiagnosis discourse is clearly present in 2026."),
    ("Diagnosis Status", "Workplace Accommodations", "+", 0.70, "Diagnosis strongly enables workplace accommodations."),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.50, "Accommodations can meaningfully reduce impairment."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.72, "Access increasingly leads to coordinated care pathways."),
    ("Care Coordination", "Support Ecosystem", "+", 0.76, "Coordinated care helps build a broader support ecosystem."),
    ("Diagnosis Status", "Support Ecosystem", "+", 0.72, "Diagnosis can connect adults to broader support structures."),
    ("Support Ecosystem", "Quality of Life", "+", 0.66, "Support systems improve functioning and quality of life."),
    ("Cultural Norms", "Stigma", "+", 0.40, "Stigma remains present, but much weaker than in earlier decades."),
    ("Stigma", "Access to Mental Health Care", "-", 0.30, "Stigma still suppresses help-seeking somewhat."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.30, "Gender stereotypes still create some diagnostic error."),
    ("Diagnosis Status", "Quality of Life", "+", 0.82, "Diagnosis can strongly improve functioning and quality of life."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life.")
]

for edge in edges:
    add_edge(*edge)

net.add_node(
    "LEGEND_NODE",
    label="""LEGEND

Green Edge → Positive Effect
Red Edge → Negative Effect
Edge Thickness → Causal Strength

Blue → Core disorder / outcomes
Green → Clinical impairment variables
Cyan → Workplace / support ecosystem
Brown → Family context
Purple → Healthcare ecosystem
Yellow-Green → Social-cultural bias
Red-Pink → Modern recognition / discourse
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 32 GENERAL GRAPH

2026

Coordinated adult-support model
Self-recognition, diagnosis, workplace support,
care coordination, and broader support
all become structurally central
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "2026_age_32_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))