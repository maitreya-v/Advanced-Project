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
    "factor": "#dddddd"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical symptom pathway variables",
    "school": "School / disciplinary pathway",
    "family": "Family response pathway",
    "access": "Healthcare access / economic barriers",
    "bias": "Social-cultural bias / stigma variables",
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
    "School Labeling Bias": "school",
    "Classroom Size": "school",

    "Parental Awareness": "family",
    "Parental Denial": "family",
    "Family Stress": "family",
    "Household Stability": "family",

    "Cost of Evaluation": "access",
    "Access to Mental Health Care": "access",
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

    ("Parental Awareness", -500, 200),
    ("Parental Denial", -620, 120),
    ("Family Stress", -380, 130),
    ("Household Stability", -500, 320),

    ("Teacher Referral Rate", -100, -420),
    ("Classroom Size", 120, -500),
    ("School Labeling Bias", 160, -340),

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
    ("ADHD", "Symptom Type", "+", 0.82, "Underlying ADHD shapes visible behavioral presentation."),
    ("Age", "Symptom Severity", "+", 0.42, "At age 8, symptoms are highly visible in daily behavior."),
    ("Gender", "Symptom Type", "+", 0.38, "Gender norms influence which childhood behaviors are noticed."),
    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.62, "Certain symptom patterns are more likely to trigger teacher concern."),
    ("Classroom Size", "Teacher Referral Rate", "+", 0.40, "Large classrooms can increase disciplinary attention."),
    ("School Labeling Bias", "Teacher Referral Rate", "+", 0.80, "Behavior is often interpreted through discipline and labeling."),
    ("Teacher Referral Rate", "Parental Awareness", "+", 0.60, "School concern can raise parental awareness."),
    ("Parental Denial", "Parental Awareness", "-", 0.82, "Denial reduces recognition of problems."),
    ("Family Stress", "Symptom Severity", "+", 0.54, "Stressful homes can amplify visible symptoms."),
    ("Household Stability", "Family Stress", "-", 0.70, "Stable homes reduce stress."),
    ("Parental Awareness", "Diagnosis Status", "+", 0.42, "Awareness can support diagnosis, though formal systems are weak."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.64, "Higher SES improves access to scarce care."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.40, "Access helps diagnosis, but the child mental health system is limited."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.78, "Cost is a major barrier to evaluation."),
    ("Cultural Norms", "Stigma", "+", 0.84, "1970 norms strongly reinforce stigma around behavior differences."),
    ("Stigma", "Diagnosis Status", "-", 0.82, "Stigma suppresses recognition and formal diagnosis."),
    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.38, "Diagnosis can modestly improve support and understanding.")
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
Cyan → School / disciplinary pathway
Brown → Family pathway
Purple → Access / barriers
Yellow-Green → Social-cultural bias
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=470,
    fixed=True, physics=False
)

net.add_node(
    "PERSONA_DESC",
    label="""AGE 8 GENERAL GRAPH

1970

Discipline / labeling model
Sparse formal care structure
High stigma, high denial,
and weak institutional support
""",
    shape="box",
    color="#f5f5f5",
    x=760, y=250,
    fixed=True, physics=False
)

filename = "1970_age_8_structural.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))