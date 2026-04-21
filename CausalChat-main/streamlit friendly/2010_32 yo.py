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
    "work": "Workplace support and adult-function pathway",
    "family": "Family and household context variables",
    "access": "Healthcare access pathway",
    "bias": "Social-cultural bias / stigma variables",
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

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Waiting Time for Assessment": "access",
    "Socioeconomic Status": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",

    "Diagnostic Criteria Variability": "controversial",
    "Misdiagnosis Rate": "controversial",
    "Self-Recognition": "controversial",

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
    ("Performance Pressure", 280, -500),
    ("Career Friction", 120, -420),

    ("Access to Mental Health Care", 500, 200),
    ("Provider Availability", 650, 80),
    ("Waiting Time for Assessment", 500, 350),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -80),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Gender Bias", 220, -300),

    ("Diagnostic Criteria Variability", 300, 420),
    ("Misdiagnosis Rate", 140, 500),
    ("Self-Recognition", 320, 560),

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
    ("ADHD", "Comorbid Conditions", "+", 0.58, "ADHD frequently co-occurs with other difficulties that complicate recognition."),
    ("Age", "Symptom Severity", "+", 0.32, "At age 32, work and life demands can make symptoms more visible."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.78, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Career Friction", "+", 0.74, "Impairment often contributes to persistent career friction."),
    ("Performance Pressure", "Functional Impairment", "+", 0.24, "Performance demands worsen visible dysfunction."),
    ("Career Friction", "Self-Recognition", "+", 0.44, "Repeated work difficulties increasingly support adult self-recognition by 2010."),
    ("Family Stress", "Symptom Severity", "+", 0.56, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.62, "Stable household context reduces stress."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.78, "Higher SES improves healthcare access."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.74, "More providers reduce waiting time."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.46, "Long waits still reduce diagnosis, though less sharply."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.56, "Cost remains a barrier, though less absolute than before."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.76, "Access strongly improves adult diagnosis in 2010."),
    ("Self-Recognition", "Diagnosis Status", "+", 0.42, "Self-recognition can meaningfully push adults toward evaluation."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.72, "Diagnostic inconsistency still creates misdiagnosis risk."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.70, "Comorbidity continues to obscure accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.66, "Misdiagnosis reduces correct diagnosis status."),
    ("Diagnosis Status", "Workplace Accommodations", "+", 0.56, "Diagnosis increasingly enables workplace accommodations by 2010."),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.42, "Accommodations can meaningfully reduce impairment."),
    ("Cultural Norms", "Stigma", "+", 0.54, "Stigma remains present, but weaker than in earlier decades."),
    ("Stigma", "Access to Mental Health Care", "-", 0.46, "Stigma still suppresses help-seeking, but less strongly."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.40, "Gender stereotypes continue to increase diagnostic error."),
    ("Diagnosis Status", "Quality of Life", "+", 0.72, "Diagnosis can meaningfully improve functioning and quality of life."),
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
Cyan → Workplace support pathway
Brown → Family context
Purple → Access pathway
Yellow-Green → Social-cultural bias
Red-Pink → Modern adult diagnosis / ambiguity
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 32 GENERAL GRAPH

2010

Formal adult-diagnosis model
Career friction, self-recognition,
access, and workplace support
all become structurally meaningful
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "2010_age_32_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))