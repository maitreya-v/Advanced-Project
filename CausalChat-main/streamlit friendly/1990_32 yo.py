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
    "work": "Institutional / work-function pathway",
    "family": "Family and household context variables",
    "access": "Healthcare access pathway",
    "bias": "Social-cultural bias / stigma variables",
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
    "Comorbid Conditions": "clinical",

    "Employment Instability": "work",
    "Performance Pressure": "work",
    "Provider Referral Pathway": "work",

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",
    "Gender": "bias",

    "Diagnostic Criteria Variability": "controversial",
    "Misdiagnosis Rate": "controversial",

    "Age": "factor"
}

positioned_nodes = [
    ("ADHD", 0, 0),
    ("Diagnosis Status", 0, 350),

    ("Age", -500, -200),
    ("Gender", -380, -200),
    ("Genetic Risk", -300, -80),
    ("Symptom Severity", -200, -200),
    ("Symptom Type", -200, -80),
    ("Comorbid Conditions", -100, -300),
    ("Functional Impairment", -300, 300),

    ("Family Stress", -380, 130),
    ("Household Stability", -500, 320),

    ("Employment Instability", 80, -420),
    ("Performance Pressure", 320, -500),
    ("Provider Referral Pathway", 180, 520),

    ("Access to Mental Health Care", 500, 200),
    ("Provider Availability", 650, 80),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -80),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Gender Bias", 220, -300),

    ("Diagnostic Criteria Variability", 300, 420),
    ("Misdiagnosis Rate", 120, 480),

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
    ("ADHD", "Comorbid Conditions", "+", 0.52, "ADHD frequently co-occurs with other difficulties that complicate recognition."),
    ("Age", "Symptom Severity", "+", 0.30, "At age 32, work and adult role demands increase symptom visibility."),
    ("Gender", "Symptom Type", "+", 0.34, "Gender norms affect how adult symptoms are interpreted."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.76, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Employment Instability", "+", 0.70, "Impairment can destabilize employment."),
    ("Performance Pressure", "Functional Impairment", "+", 0.28, "Performance pressure worsens visible dysfunction."),
    ("Employment Instability", "Provider Referral Pathway", "+", 0.34, "Occupational difficulties begin to increase referral toward assessment in 1990."),
    ("Family Stress", "Symptom Severity", "+", 0.56, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.62, "Stable household context reduces stress."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.76, "Higher SES improves healthcare access."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.62, "Provider supply improves access more than in 1970."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.72, "Cost remains a substantial diagnosis barrier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.56, "Access meaningfully improves diagnosis, though adult ADHD is still underrecognized."),
    ("Provider Referral Pathway", "Diagnosis Status", "+", 0.44, "Referral from observed adult impairment becomes somewhat more plausible by 1990."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.82, "Inconsistent diagnostic framing increases misdiagnosis."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.76, "Comorbidity obscures accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.80, "Misdiagnosis reduces correct diagnosis status."),
    ("Cultural Norms", "Stigma", "+", 0.76, "1990 norms still reinforce stigma, though less than in 1970."),
    ("Stigma", "Access to Mental Health Care", "-", 0.64, "Stigma suppresses help-seeking and care access."),
    ("Gender Bias", "Diagnosis Status", "+", 0.38, "Gender bias shapes who is recognized."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.50, "Gender stereotypes increase diagnostic error."),
    ("Diagnosis Status", "Functional Impairment", "-", 0.38, "Diagnosis can modestly reduce impairment through treatment or understanding."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.56, "Diagnosis can improve functioning and quality of life.")
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
Cyan → Work / referral pathway
Brown → Family context
Purple → Access pathway
Yellow-Green → Social-cultural bias
Red-Pink → Diagnostic ambiguity
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 32 GENERAL GRAPH

1990

Transitional adult-recognition model
Provider access and referral improve,
but misdiagnosis and stigma
remain structurally important
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "1990_age_32_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))