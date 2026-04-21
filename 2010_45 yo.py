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
    "access": "Healthcare access pathway",
    "bias": "Social-cultural / structural bias variables",
    "controversial": "Retrospective recognition pathway",
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
    "Digital Distraction Environment": "environment",
    "Chronic Stress Load": "environment",

    "Family Stress": "family",
    "Home Structure Stability": "family",
    "Family History Awareness": "family",

    "Financial Status": "access",
    "Socioeconomic Status": "access",
    "Provider Availability": "access",
    "Access to Mental Health Care": "access",
    "Waiting Time for Assessment": "access",
    "Cost of Evaluation": "access",
    "Clinical Guidelines Evolution": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Self-Diagnosis Behavior": "controversial",
    "Retrospective Recognition": "controversial",
    "Diagnosis Feedback Loop": "controversial",
    "Social Media Awareness": "controversial",

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
    ("Misdiagnosis Rate", 140, 500),

    ("Sleep Quality", 80, -500),
    ("Nutrition Quality", -100, -420),
    ("Digital Distraction Environment", 300, -380),
    ("Chronic Stress Load", 280, -500),

    ("Family Stress", -380, 130),
    ("Home Structure Stability", -500, 320),
    ("Family History Awareness", -620, -20),

    ("Financial Status", 650, -80),
    ("Socioeconomic Status", 780, -130),
    ("Provider Availability", 650, 80),
    ("Access to Mental Health Care", 500, 200),
    ("Waiting Time for Assessment", 500, 350),
    ("Cost of Evaluation", 500, 480),
    ("Clinical Guidelines Evolution", 320, 420),
    ("Care Coordination", 650, 320),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Race / Ethnicity", 520, -140),
    ("Institutional Bias", 300, -240),

    ("Self-Diagnosis Behavior", 220, 520),
    ("Retrospective Recognition", 60, 560),
    ("Diagnosis Feedback Loop", 320, 560),
    ("Social Media Awareness", 320, -120),

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
    ("Digital Distraction Environment", "Chronic Stress Load", "+", 0.34, "Modern distraction environments begin to contribute to stress by 2010."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Accumulated life stress can worsen symptoms in midlife."),

    ("Home Structure Stability", "Family Stress", "-", 0.68, "Stable home structure reduces stress."),
    ("Family Stress", "Chronic Stress Load", "+", 0.72, "Family stress contributes to chronic stress accumulation."),
    ("Family History Awareness", "Retrospective Recognition", "+", 0.42, "Family history can meaningfully support later-life recognition by 2010."),

    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Financial resources strongly affect access to care."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.74, "Socioeconomic position shapes access to care."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.74, "More providers reduce waiting time."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.46, "Long waits still reduce diagnosis, though less sharply."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.60, "Cost still suppresses diagnosis, though less absolutely than before."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.76, "Access strongly helps diagnosis in 2010."),
    ("Clinical Guidelines Evolution", "Diagnosis Status", "+", 0.60, "Guideline evolution makes delayed adult recognition much more plausible."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.58, "Access increasingly leads to coordinated care in 2010."),
    ("Care Coordination", "Diagnosis Status", "+", 0.36, "Care coordination helps diagnosis completion."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.60, "Misdiagnosis still reduces correct diagnosis status."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.58, "Structural inequities influence institutional behavior."),
    ("Institutional Bias", "Misdiagnosis Rate", "+", 0.44, "Bias still increases some diagnostic error."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.36, "Bias still suppresses equitable access to diagnosis."),
    ("Social Media Awareness", "Self-Diagnosis Behavior", "+", 0.34, "Online awareness begins to support self-recognition by 2010."),
    ("Retrospective Recognition", "Self-Diagnosis Behavior", "+", 0.50, "Retrospective interpretation of lifelong patterns increasingly supports self-recognition."),
    ("Self-Diagnosis Behavior", "Diagnosis Status", "+", 0.36, "Self-recognition can meaningfully push toward evaluation."),
    ("Diagnosis Status", "Diagnosis Feedback Loop", "+", 0.42, "Diagnosis can influence later reinterpretation of lifelong patterns."),
    ("Diagnosis Feedback Loop", "Retrospective Recognition", "+", 0.30, "Feedback effects increasingly reinforce later-life understanding."),

    ("Cultural Norms", "Stigma", "+", 0.56, "Stigma remains present, but weaker than in 1990."),
    ("Stigma", "Diagnosis Status", "-", 0.50, "Stigma still suppresses adult diagnosis, though less strongly."),
    ("Stigma", "Self-Diagnosis Behavior", "-", 0.38, "Stigma still discourages self-recognition and help-seeking."),

    ("Diagnosis Status", "Functional Impairment", "-", 0.50, "Diagnosis can meaningfully reduce impairment through treatment or support."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.70, "Diagnosis can meaningfully improve quality of life in midlife.")
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
Green → Clinical-cognitive pathway
Cyan → Environmental burden
Brown → Family context
Purple → Access / care pathway
Yellow-Green → Social-cultural / structural bias
Red-Pink → Retrospective recognition pathway
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

2010

Retrospective-recognition model
Guideline support, access,
self-recognition, and coordinated care
become structurally meaningful
""",
    shape="box",
    color="#f5f5f5",
    x=760,
    y=250,
    fixed=True,
    physics=False
)

filename = "2010_age_45_updated.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))