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
    "access": "Healthcare ecosystem pathway",
    "bias": "Social-cultural bias / latent variables",
    "controversial": "Modern recognition / correction pathway",
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
    "Provider Availability": "access",
    "Access to Mental Health Care": "access",
    "Waiting Time for Assessment": "access",
    "Cost of Evaluation": "access",
    "Clinical Guidelines Evolution": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Race / Ethnicity": "bias",

    "Self-Diagnosis Behavior": "controversial",
    "Retrospective Recognition": "controversial",
    "Diagnosis Feedback Loop": "controversial",
    "Social Media Awareness": "controversial",
    "Overdiagnosis Pressure": "controversial",

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
    ("Provider Availability", 650, 80),
    ("Access to Mental Health Care", 500, 200),
    ("Waiting Time for Assessment", 500, 350),
    ("Cost of Evaluation", 500, 480),
    ("Clinical Guidelines Evolution", 320, 420),
    ("Care Coordination", 650, 320),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Race / Ethnicity", 520, -140),

    ("Self-Diagnosis Behavior", 220, 520),
    ("Retrospective Recognition", 60, 560),
    ("DiagnosisFeedbackLoop", 320, 560),
    ("Social Media Awareness", 320, -120),
    ("Overdiagnosis Pressure", 500, 560),

    ("Quality of Life", -500, 450),
]

for node, x, y in positioned_nodes:
    group = node_groups.get(node, "factor")
    label = node
    if node == "ADHD":
        label = "ADHD (Underlying Disorder)"
    elif node == "DiagnosisFeedbackLoop":
        label = "Diagnosis Feedback Loop"

    net.add_node(
        node,
        label=label,
        color=group_colors[group],
        size=45 if node == "ADHD" else 40 if node == "Diagnosis Status" else 30 if node == "Quality of Life" else 25,
        x=x, y=y,
        fixed=True, physics=False,
        font={"size": 18 if node in ["ADHD", "Diagnosis Status"] else 13, "color": "black"},
        title=f"Node: {label}\nCluster: {group.upper()}\nDescription: {group_descriptions[group]}"
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

    ("Sleep Quality", "Executive Function Deficit", "-", 0.64, "Better sleep can modestly reduce executive dysfunction."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.50, "Better nutrition may modestly reduce symptom severity."),
    ("Digital Distraction Environment", "Chronic Stress Load", "+", 0.58, "Digital distraction is a strong contextual factor by 2026."),
    ("Chronic Stress Load", "Symptom Severity", "+", 0.66, "Accumulated life stress can worsen symptoms in midlife."),

    ("Home Structure Stability", "Family Stress", "-", 0.68, "Stable home structure reduces stress."),
    ("Family Stress", "Chronic Stress Load", "+", 0.72, "Family stress contributes to chronic stress accumulation."),
    ("Family History Awareness", "Retrospective Recognition", "+", 0.54, "Family history strongly supports later-life recognition by 2026."),

    ("Financial Status", "Access to Mental Health Care", "+", 0.76, "Financial resources strongly affect access to care."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.82, "More providers reduce waiting time in 2026."),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.34, "Long waits still reduce diagnosis, but less sharply than before."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.46, "Cost still suppresses diagnosis, but less absolutely than before."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.86, "Access strongly helps diagnosis in 2026."),
    ("Clinical Guidelines Evolution", "Diagnosis Status", "+", 0.78, "Guideline evolution makes delayed adult recognition highly plausible."),
    ("Care Coordination", "Diagnosis Status", "+", 0.62, "Care coordination strengthens successful diagnosis completion."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.50, "Misdiagnosis still reduces correct diagnosis status."),
    ("Race / Ethnicity", "Access to Mental Health Care", "-", 0.50, "Structural inequities still reduce access for some groups."),

    ("Social Media Awareness", "Self-Diagnosis Behavior", "+", 0.62, "Online awareness strongly supports self-recognition by 2026."),
    ("Retrospective Recognition", "Self-Diagnosis Behavior", "+", 0.66, "Later-life reinterpretation of lifelong patterns strongly supports self-recognition."),
    ("Self-Diagnosis Behavior", "Diagnosis Status", "+", 0.54, "Self-recognition can meaningfully push toward evaluation."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Overdiagnosis discourse is clearly present in 2026."),
    ("Diagnosis Status", "DiagnosisFeedbackLoop", "+", 0.56, "Diagnosis strongly influences reinterpretation of lifelong patterns."),
    ("DiagnosisFeedbackLoop", "Retrospective Recognition", "+", 0.46, "Feedback effects on recognition are substantial."),
    ("DiagnosisFeedbackLoop", "Self-Diagnosis Behavior", "+", 0.42, "Diagnosis history reinforces self-understanding and future help-seeking."),

    ("Cultural Norms", "Stigma", "+", 0.38, "Stigma remains present, but much weaker than in earlier decades."),
    ("Stigma", "Diagnosis Status", "-", 0.30, "Stigma still suppresses adult diagnosis somewhat."),
    ("Stigma", "Self-DiagnosisBehavior", "-", 0.01, "Placeholder removed."),
]

edges = [e for e in edges if e[0] != "Stigma" or e[1] != "Self-DiagnosisBehavior"]

edges.extend([
    ("Stigma", "Self-DiagnosisBehavior2", "+", 0.01, "Placeholder removed.")
])
edges = [e for e in edges if e[0] != "Stigma"]

# re-add correct stigma edges
edges.extend([
    ("Stigma", "Self-Diagnosis Behavior", "-", 0.24, "Stigma still discourages self-recognition somewhat."),
    ("Diagnosis Status", "Functional Impairment", "-", 0.60, "Diagnosis can meaningfully reduce impairment through treatment or support."),
    ("Functional Impairment", "Quality of Life", "-", 0.90, "Cumulative impairment strongly lowers quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.82, "Diagnosis can strongly improve quality of life in midlife.")
])

# deduplicate manually if needed
seen = set()
clean_edges = []
for e in edges:
    key = (e[0], e[1], e[2])
    if key not in seen:
        clean_edges.append(e)
        seen.add(key)

for edge in clean_edges:
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
Purple → Healthcare ecosystem
Yellow-Green → Social-cultural bias
Red-Pink → Modern recognition / correction pathway
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 45 GENERAL GRAPH

2026

Diagnosis-correction ecosystem model
Retrospective recognition, digital awareness,
care coordination, and feedback loops
become structurally central
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "2026_age_45_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))