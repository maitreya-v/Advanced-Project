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
    "environment": "#17becf",
    "family": "#8c564b",
    "access": "#9467bd",
    "bias": "#bcbd22",
    "controversial": "#ff4d4d",
    "factor": "#dddddd"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical-cognitive pathway variables",
    "environment": "Environmental burden variables",
    "family": "Family-context variables",
    "access": "Socioeconomic / healthcare access variables",
    "bias": "Social-cultural bias / latent variables",
    "controversial": "Historically weak or minimal pathway",
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

    "Sleep Quality": "environment",
    "Nutrition Quality": "environment",
    "Chronic Stress Load": "environment",

    "Family Stress": "family",
    "Home Structure Stability": "family",
    "Family History Awareness": "family",

    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Race / Ethnicity": "bias",

    "Self-Diagnosis Behavior": "controversial",
    "Clinical Guidelines Evolution": "controversial",

    "Age": "factor"
}

positioned_nodes = [
    ("ADHD", 0, 0),
    ("Diagnosis Status", 0, 350),

    ("Age", -500, -200),
    ("Genetic Risk", -300, -80),
    ("Executive Function Deficit", -200, -200),
    ("Symptom Severity", -120, -80),
    ("Functional Impairment", -300, 300),

    ("Sleep Quality", 80, -500),
    ("Nutrition Quality", -100, -420),
    ("Chronic Stress Load", 280, -500),

    ("Family Stress", -380, 130),
    ("Home Structure Stability", -500, 320),
    ("Family History Awareness", -620, -20),

    ("Financial Status", 650, -80),
    ("Neighborhood Quality", 680, -220),
    ("Access to Mental Health Care", 500, 200),
    ("Cost of Evaluation", 500, 480),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Race / Ethnicity", 520, -140),

    ("Self-Diagnosis Behavior", 220, 520),
    ("Clinical Guidelines Evolution", 320, 420),

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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic vulnerability contributes strongly to lifelong ADHD."),
    ("ADHD", "Executive Function Deficit", "+", 0.90, "Underlying ADHD strongly affects executive functioning."),
    ("Executive Function Deficit", "Functional Impairment", "+", 0.84, "Executive dysfunction increases cumulative impairment."),
    ("SymptomSeverity", "Functional Impairment", "+", 0.01, "Placeholder removed."),
]

edges = [e for e in edges if e[0] != "SymptomSeverity"]

edges.extend([
    ("Symptom Severity", "Functional Impairment", "+", 0.84, "Greater symptom burden worsens daily functioning."),
    ("Age", "Functional Impairment", "+", 0.40, "By age 45, long-term untreated difficulties can compound impairment."),

    ("Sleep Quality", "Executive Function Deficit", "-", 0.62, "Better sleep can modestly reduce executive dysfunction."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.48, "Better nutrition may modestly reduce symptom severity."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.68, "Accumulated life stress can worsen symptoms in midlife."),

    ("Home Structure Stability", "Family Stress", "-", 0.68, "Stable home structure reduces stress."),
    ("Family Stress", "Chronic Stress Load", "+", 0.72, "Family stress contributes to chronic stress accumulation."),
    ("Family History Awareness", "Self-Diagnosis Behavior", "+", 0.12, "Family history only weakly supports self-recognition in 1970."),

    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Financial resources strongly affect access to care."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.46, "Better neighborhood conditions modestly improve care access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.80, "High evaluation cost strongly suppresses diagnosis."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.40, "Access helps diagnosis, but adult recognition remains weak."),
    ("Clinical Guidelines Evolution", "Diagnosis Status", "+", 0.10, "Guideline support for adult ADHD is minimal in 1970."),
    ("Race / Ethnicity", "Access to Mental Health Care", "-", 0.60, "Structural inequities reduce access for some groups."),

    ("Cultural Norms", "Stigma", "+", 0.86, "1970 norms strongly reinforce stigma toward adult cognitive and behavioral differences."),
    ("Stigma", "Diagnosis Status", "-", 0.84, "High stigma suppresses adult diagnosis."),
    ("Stigma", "Self-Diagnosis Behavior", "-", 0.68, "Stigma discourages self-recognition and help-seeking."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.28, "Diagnosis can modestly reduce impairment through explanation or limited treatment."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.46, "Diagnosis can modestly improve quality of life in midlife.")
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
Green → Clinical-cognitive pathway
Cyan → Environmental burden
Brown → Family context
Purple → Access / barriers
Yellow-Green → Social-cultural bias
Red-Pink → Historically weak pathway
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 45 GENERAL GRAPH

1970

Chronic underdiagnosis model
Stigma, cost, low access,
and accumulated burden dominate
Modern recognition pathways are minimal
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "1970_age_45_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))