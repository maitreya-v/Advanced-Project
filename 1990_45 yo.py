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
    "bias": "Social-cultural / structural bias variables",
    "controversial": "Delayed-recognition pathway",
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
    ("Misdiagnosis Rate", 160, 500),

    ("Sleep Quality", 80, -500),
    ("Nutrition Quality", -150, -380),
    ("Chronic Stress Load", 280, -500),

    ("Family Stress", -380, 130),
    ("Home Structure Stability", -500, 320),
    ("Family History Awareness", -620, -20),

    ("Financial Status", 650, -80),
    ("Socioeconomic Status", 780, -120),
    ("Neighborhood Quality", 780, -200),
    ("Provider Availability", 650, 80),
    ("Access to Mental Health Care", 500, 200),
    ("Cost of Evaluation", 500, 480),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Race / Ethnicity", 520, -140),
    ("Institutional Bias", 300, -260),

    ("Self-Diagnosis Behavior", 220, 520),
    ("Clinical Guidelines Evolution", 320, 420),

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
    ("ProviderAvailabilityTypo", "Access to Mental Health Care", "+", 0.01, "Placeholder removed."),
]

edges = [e for e in edges if e[0] != "ProviderAvailabilityTypo"]

edges.extend([
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

    ("Diagnosis Status", "Functional Impairment", "-", 0.36, "Diagnosis can modestly reduce impairment through explanation or support."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.56, "Diagnosis can modestly improve quality of life in midlife.")
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
Purple → Access pathway
Yellow-Green → Social-cultural / structural bias
Red-Pink → Delayed-recognition pathway
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
    label="""AGE 45 GENERAL GRAPH

1990

Delayed-recognition transition model
Provider access and guideline support improve,
but stigma, cost, misdiagnosis,
and structural inequality remain important
""",
    shape="box",
    color="#f5f5f5",
    x=760,
    y=250,
    fixed=True,
    physics=False
)

filename = "1990_age_45_updated.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))