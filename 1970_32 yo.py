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
    "environment": "#17becf",
    "controversial": "#ff4d4d",
    "factor": "#dddddd"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical impairment variables",
    "work": "Institutional / performance-pressure pathway",
    "family": "Family and household context variables",
    "access": "Healthcare access / economic barriers",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and chronic burden variables",
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

    "Family Stress": "family",
    "Household Stability": "family",

    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Educational Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender Bias": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Sleep Quality": "environment",
    "Chronic Stress Load": "environment",

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

    ("Nutrition Quality", -200, -350),
    ("Sleep Quality", 80, -520),
    ("Chronic Stress Load", 250, -500),

    ("Family Stress", -380, 130),
    ("Household Stability", -500, 320),

    ("Employment Instability", 120, -420),
    ("Performance Pressure", 320, -500),

    ("Access to Mental Health Care", 500, 200),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -80),
    ("Financial Status", 780, -120),
    ("Neighborhood Quality", 780, -200),
    ("Educational Access", 500, -350),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Gender Bias", 220, -300),
    ("Race / Ethnicity", 520, -140),
    ("Institutional Bias", 300, -260),

    ("Diagnostic Criteria Variability", 300, 420),
    ("Misdiagnosis Rate", 180, 500),

    ("Quality of Life", -500, 450),
]

for node, x, y in positioned_nodes:
    group = node_groups.get(node, "factor")
    net.add_node(
        node,
        label="ADHD (Underlying Disorder)" if node == "ADHD" else node,
        color=group_colors[group],
        size=45 if node == "ADHD" else 40 if node == "Diagnosis Status" else 30 if node == "Quality of Life" else 25,
        x=x,
        y=y,
        fixed=True,
        physics=False,
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
    ("ADHD", "Symptom Type", "+", 0.78, "Underlying ADHD shapes symptom presentation."),
    ("ADHD", "Comorbid Conditions", "+", 0.44, "Untreated ADHD can co-occur with other difficulties that complicate recognition."),

    ("Nutrition Quality", "Symptom Severity", "-", 0.50, "Poor nutrition worsens cognitive regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.60, "Sleep disruption affects functioning and regulation."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Stress amplifies symptoms."),

    ("Age", "Symptom Severity", "+", 0.28, "At age 32, sustained adult role demands can make symptoms more visible."),
    ("Gender", "Symptom Type", "+", 0.32, "Gender norms affect which adult symptoms are noticed or dismissed."),
    ("Symptom Severity", "Functional Impairment", "+", 0.82, "Higher severity increases occupational and daily impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.72, "Comorbid burden increases impairment."),
    ("Functional Impairment", "Employment Instability", "+", 0.72, "Impairment can destabilize employment in adulthood."),
    ("Performance Pressure", "Functional Impairment", "+", 0.32, "Work and performance pressure can worsen visible dysfunction."),

    ("Family Stress", "SymptomSeverity2", "+", 0.01, "Placeholder removed."),
]

edges = [e for e in edges if e[0] != "Family Stress"]

edges.extend([
    ("Family Stress", "Symptom Severity", "+", 0.54, "Adult family stress can intensify symptom burden."),
    ("Household Stability", "Family Stress", "-", 0.62, "Stable household context reduces stress."),

    ("Socioeconomic Status", "Educational Access", "+", 0.68, "Higher SES improves educational and cognitive support opportunities."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Income controls access to mental healthcare."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.44, "Better neighborhood conditions improve resource access."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.72, "Higher SES improves healthcare access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.76, "Cost is a major adult diagnosis barrier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.40, "Access helps diagnosis, but adult ADHD recognition remains weak in 1970."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.68, "Structural inequities influence institutions and healthcare pathways."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.60, "Bias increases diagnostic errors."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.58, "Bias suppresses fair diagnosis access."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.86, "Inconsistent diagnostic framing increases misdiagnosis."),
    ("Comorbid Conditions", "Misdiagnosis Rate", "+", 0.76, "Comorbidity obscures accurate diagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.82, "Misdiagnosis reduces correct diagnosis status."),

    ("Cultural Norms", "Stigma", "+", 0.82, "1970 cultural norms strongly reinforce stigma."),
    ("Stigma", "Access to Mental Health Care", "-", 0.70, "Stigma suppresses help-seeking and care access."),
    ("Gender Bias", "Diagnosis Status", "+", 0.34, "Gender bias shapes who is recognized or dismissed."),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.48, "Gender stereotypes increase diagnostic error."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.28, "Diagnosis can modestly reduce impairment through explanation or limited treatment."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Impairment lowers adult quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.46, "Diagnosis can modestly improve quality of life.")
])

for edge in edges:
    add_edge(*edge)

net.add_node(
    "LEGEND_NODE",
    label="""LEGEND

Green Edge → Positive Effect
Red Edge → Negative Effect
Edge Thickness → Causal Strength

Blue → Core disorder / outcomes
Green → Clinical variables
Cyan → Work / environment pathway
Brown → Family context
Purple → Access / barriers
Yellow-Green → Social-cultural / structural bias
Red-Pink → Diagnostic ambiguity
""",
    shape="box",
    color="#f5f5f5",
    x=760,
    y=470,
    fixed=True,
    physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 32 GENERAL GRAPH

1970

Underrecognition model
Impairment, instability, stigma,
economic barriers, and structural bias dominate
""",
    shape="box",
    color="#f5f5f5",
    x=760,
    y=250,
    fixed=True,
    physics=False
)

filename = "1970_age_32_updated.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))