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
    "school": "School support and detection pathway",
    "family": "Family advocacy pathway",
    "access": "Healthcare access pathway",
    "bias": "Social-cultural bias / stigma variables",
    "controversial": "Modern treatment and diagnostic pressure pathway",
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

    "Teacher Referral Rate": "school",
    "School Resources": "school",
    "Education System Pressure": "school",
    "School Support Plan": "school",

    "Parental Awareness": "family",
    "Parental Advocacy": "family",
    "Family Stress": "family",

    "Provider Availability": "access",
    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",

    "Treatment Dependency": "controversial",
    "Overdiagnosis Pressure": "controversial",
    "Misdiagnosis Rate": "controversial",

    "Age": "factor"
}

positioned_nodes = [
    ("ADHD", 0, 0),
    ("Diagnosis Status", 0, 350),

    ("Age", -500, -200),
    ("Genetic Risk", -300, -80),
    ("Symptom Severity", -200, -200),
    ("Symptom Type", -200, -80),
    ("Functional Impairment", -300, 300),

    ("Parental Awareness", -500, 200),
    ("Parental Advocacy", -620, 120),
    ("Family Stress", -380, 130),

    ("Teacher Referral Rate", -100, -420),
    ("School Resources", 220, -380),
    ("Education System Pressure", 420, -520),
    ("School Support Plan", 120, 520),

    ("Provider Availability", 650, 80),
    ("Access to Mental Health Care", 500, 200),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -80),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),

    ("Treatment Dependency", -120, 500),
    ("Overdiagnosis Pressure", 320, 520),
    ("Misdiagnosis Rate", 200, 480),

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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic liability contributes strongly to childhood ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.90, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.84, "Underlying ADHD shapes visible symptom presentation."),
    ("Age", "Symptom Severity", "+", 0.44, "At age 8, symptoms remain highly visible through school functioning."),
    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase daily impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.74, "Certain symptom styles are likely to trigger school concern."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.56, "Institutional pressure can increase school referral."),
    ("School Resources", "Teacher Referral Rate", "+", 0.64, "By 2010, school resources strongly support detection."),
    ("Teacher Referral Rate", "Parental Awareness", "+", 0.84, "Teacher concern strongly raises parental awareness."),
    ("Parental Awareness", "Parental Advocacy", "+", 0.74, "Awareness increasingly leads to active parent advocacy."),
    ("Parental Advocacy", "Diagnosis Status", "+", 0.72, "Advocacy strongly supports evaluation and diagnosis."),
    ("Family Stress", "Symptom Severity", "+", 0.54, "Family stress can amplify symptoms."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.74, "Higher SES improves access to evaluation."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.78, "Provider supply strongly improves access."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.82, "Access strongly improves diagnosis likelihood."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.62, "Cost still remains a barrier."),
    ("Diagnosis Status", "School Support Plan", "+", 0.74, "Diagnosis can lead to formalized school support structures."),
    ("Diagnosis Status", "Treatment Dependency", "+", 0.58, "Diagnosis increasingly leads into treatment pathways."),
    ("Treatment Dependency", "Functional Impairment", "-", 0.48, "Treatment can meaningfully reduce impairment."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.46, "Misdiagnosis still reduces accurate identification."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Overdiagnosis discourse is visible by 2010."),
    ("Cultural Norms", "Stigma", "+", 0.58, "Stigma remains, but weaker than in 1990."),
    ("Stigma", "Diagnosis Status", "-", 0.46, "Stigma still suppresses recognition somewhat."),
    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.74, "Diagnosis can strongly improve support and quality of life.")
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
Cyan → School support / detection pathway
Brown → Family advocacy pathway
Purple → Access pathway
Yellow-Green → Social-cultural bias
Red-Pink → Modern treatment / pressure pathway
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 8 GENERAL GRAPH

2010

Formal diagnosis-and-support model
Clearer school-family-provider pathway
Structured support now matters
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "2010_age_8_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))