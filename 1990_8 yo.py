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
    "school": "#17becf",
    "family": "#8c564b",
    "access": "#9467bd",
    "bias": "#bcbd22",
    "controversial": "#ff4d4d",
    "factor": "#dddddd"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical symptom pathway variables",
    "school": "School detection pathway",
    "family": "Family response pathway",
    "access": "Healthcare access / inequality pathway",
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
    "Misdiagnosis Rate": "controversial",

    "Teacher Referral Rate": "school",
    "SchoolResources": "school",
    "School Labeling Bias": "school",
    "Classroom Size": "school",
    "Education System Pressure": "school",

    "Parental Awareness": "family",
    "Parental Denial": "family",
    "Family Stress": "family",
    "Household Stability": "family",

    "Provider Availability": "access",
    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender": "bias",

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
    ("Functional Impairment", -300, 300),
    ("Misdiagnosis Rate", 160, 500),

    ("Parental Awareness", -500, 200),
    ("Parental Denial", -620, 120),
    ("Family Stress", -380, 130),
    ("Household Stability", -500, 320),

    ("Teacher Referral Rate", -100, -420),
    ("Classroom Size", 80, -500),
    ("School Labeling Bias", 100, -340),
    ("SchoolResources", 300, -380),
    ("Education System Pressure", 420, -520),

    ("Provider Availability", 650, 80),
    ("Access to Mental Health Care", 500, 200),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -80),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),

    ("Quality of Life", -500, 450),
]

for node, x, y in positioned_nodes:
    group = node_groups.get(node, "factor")
    net.add_node(
        node,
        label=node if node not in ["ADHD", "SchoolResources"] else ("ADHD (Underlying Disorder)" if node == "ADHD" else "School Resources"),
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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic liability contributes strongly to childhood ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.90, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.84, "Underlying ADHD shapes symptom presentation."),
    ("Age", "Symptom Severity", "+", 0.44, "At age 8, symptoms are visible through school and behavior."),
    ("Gender", "Symptom Type", "+", 0.40, "Gender norms influence which behaviors are noticed."),
    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.72, "Certain symptom styles are likely to trigger school concern."),
    ("Classroom Size", "Teacher Referral Rate", "+", 0.44, "Classroom context can increase teacher concern."),
    ("School Labeling Bias", "Teacher Referral Rate", "+", 0.70, "Behavioral labeling still shapes referrals."),
    ("SchoolResources", "Teacher Referral Rate", "+", 0.46, "In 1990, school resources increasingly support detection."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.52, "Institutional pressure can increase school referrals."),
    ("Teacher Referral Rate", "Parental Awareness", "+", 0.78, "School concerns more reliably increase parent awareness."),
    ("Parental Denial", "Parental Awareness", "-", 0.74, "Denial still reduces parent recognition."),
    ("Family Stress", "Symptom Severity", "+", 0.56, "Stressful homes can amplify symptoms."),
    ("Household Stability", "Family Stress", "-", 0.70, "Stable homes reduce stress."),
    ("Parental Awareness", "Diagnosis Status", "+", 0.62, "Parental awareness meaningfully supports diagnosis by 1990."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.70, "Higher SES improves access to care."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.62, "Provider supply improves access more than in 1970."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.66, "Access meaningfully improves diagnosis likelihood."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.72, "Cost remains a substantial barrier."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.56, "Misdiagnosis reduces accurate identification."),
    ("Cultural Norms", "Stigma", "+", 0.74, "Stigma remains significant, but weaker than in 1970."),
    ("Stigma", "Diagnosis Status", "-", 0.68, "Stigma still suppresses diagnosis."),
    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.56, "Diagnosis can improve support and outcomes.")
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
Green → Clinical variables
Cyan → School detection pathway
Brown → Family pathway
Purple → Access / barriers
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
    label="""AGE 8 GENERAL GRAPH

1990

Transitional detection model
More institutional recognition
than 1970, but stigma,
labeling bias, and cost still matter
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "1990_age_8_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))