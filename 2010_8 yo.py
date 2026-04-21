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
    "environment": "#17becf",
    "controversial": "#ff4d4d",
    "factor": "#dddddd"
}

group_descriptions = {
    "core": "Core disorder / final outcomes",
    "clinical": "Clinical symptom pathway variables",
    "school": "School support and detection pathway",
    "family": "Family advocacy pathway",
    "access": "Healthcare access pathway",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and developmental exposure variables",
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
    "Misdiagnosis Rate": "controversial",

    "Teacher Referral Rate": "school",
    "School Resources": "school",
    "Education System Pressure": "school",
    "School Support Plan": "school",

    "Parental Awareness": "family",
    "Parental Advocacy": "family",
    "Family Stress": "family",
    "Parental Education": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Care Coordination": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Early Life Nutrition": "environment",
    "Sleep Quality": "environment",
    "Environmental Exposure": "environment",

    "Treatment Dependency": "controversial",
    "Overdiagnosis Pressure": "controversial",

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
    ("Misdiagnosis Rate", 180, 500),

    ("Parental Awareness", -500, 200),
    ("Parental Advocacy", -620, 120),
    ("Family Stress", -380, 130),
    ("Parental Education", -650, 250),

    ("Teacher Referral Rate", -100, -420),
    ("School Resources", 220, -380),
    ("Education System Pressure", 420, -520),
    ("School Support Plan", 120, 520),

    ("Early Life Nutrition", -450, -350),
    ("Nutrition Quality", -200, -350),
    ("Sleep Quality", 20, -520),
    ("Environmental Exposure", 220, -450),

    ("Access to Mental Health Care", 500, 200),
    ("Provider Availability", 650, 80),
    ("Cost of Evaluation", 500, 480),
    ("Socioeconomic Status", 650, -50),
    ("Financial Status", 780, -120),
    ("Neighborhood Quality", 780, -250),
    ("Care Coordination", 650, 320),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Race / Ethnicity", 520, -150),
    ("Institutional Bias", 300, -250),

    ("Treatment Dependency", -120, 500),
    ("Overdiagnosis Pressure", 320, 560),

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
    ("Genetic Risk", "ADHD", "+", 0.88, "Genetic liability contributes strongly to childhood ADHD."),
    ("ADHD", "Symptom Severity", "+", 0.90, "Underlying ADHD increases symptom severity."),
    ("ADHD", "Symptom Type", "+", 0.84, "Underlying ADHD shapes visible behavioral presentation."),

    ("Age", "Symptom Severity", "+", 0.44, "At age 8, symptoms are highly visible through behavior and school functioning."),
    ("Gender", "Symptom Type", "+", 0.38, "Gender norms influence which childhood behaviors are noticed."),

    ("Early Life Nutrition", "Genetic Risk", "-", 0.18, "Early nutrition can modulate developmental vulnerability."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.56, "Poor nutrition may worsen behavioral regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.66, "Better sleep reduces dysregulation."),
    ("Environmental Exposure", "Symptom Severity", "+", 0.40, "Environmental stressors can worsen symptoms."),

    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.74, "Certain symptom patterns are likely to trigger teacher concern."),
    ("School Resources", "Teacher Referral Rate", "+", 0.64, "By 2010, school resources strongly support detection."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.56, "Institutional pressure can increase school referral."),
    ("Teacher Referral Rate", "Parental Awareness", "+", 0.84, "Teacher concern strongly raises parental awareness."),

    ("ParentalEducationTypo", "Parental Awareness", "+", 0.01, "Placeholder removed."),
]
edges = [e for e in edges if e[0] != "ParentalEducationTypo"]

edges.extend([
    ("Parental Education", "Parental Awareness", "+", 0.64, "More educated parents better recognize childhood issues."),
    ("Parental Awareness", "Parental Advocacy", "+", 0.74, "Awareness increasingly leads to active parent advocacy."),
    ("Parental Advocacy", "Diagnosis Status", "+", 0.72, "Advocacy strongly supports evaluation and diagnosis."),
    ("Family Stress", "Symptom Severity", "+", 0.54, "Family stress can amplify visible symptoms."),
    ("Family Stress", "Sleep Quality", "-", 0.56, "Stress disrupts sleep patterns."),
    ("Parental Advocacy", "School Support Plan", "+", 0.66, "Advocating families are more likely to secure formal school supports."),

    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.74, "Higher SES improves access to evaluation."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.78, "Affordability strongly controls access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.48, "Better neighborhoods provide more resources."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.78, "Provider supply strongly improves access."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.62, "Cost still remains a barrier."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.82, "Access strongly improves diagnosis likelihood."),
    ("Access to Mental Health Care", "Care Coordination", "+", 0.60, "Access increasingly leads to coordinated care in 2010."),
    ("Care Coordination", "School Support Plan", "+", 0.58, "Care coordination improves school support planning."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.62, "Structural inequities influence institutional behavior."),
    ("Institutional Bias", "Teacher Referral Rate", "+", 0.46, "Bias still affects referral patterns."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.44, "Bias suppresses equitable diagnosis access."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.46, "Misdiagnosis still reduces accurate identification."),
    ("Cultural Norms", "Stigma", "+", 0.58, "Stigma remains, but weaker than in 1990."),
    ("Stigma", "Diagnosis Status", "-", 0.46, "Stigma still suppresses recognition somewhat."),

    ("Diagnosis Status", "School Support Plan", "+", 0.74, "Diagnosis can lead to formalized school support structures."),
    ("Diagnosis Status", "Treatment Dependency", "+", 0.58, "Diagnosis increasingly leads into treatment pathways."),
    ("Treatment Dependency", "Functional Impairment", "-", 0.48, "Treatment can meaningfully reduce impairment."),
    ("Overdiagnosis Pressure", "Diagnosis Status", "+", 0.42, "Overdiagnosis discourse is visible by 2010."),

    ("Functional Impairment", "Quality of Life", "-", 0.86, "Impairment reduces quality of life."),
    ("Diagnosis Status", "Quality of Life", "+", 0.74, "Diagnosis can strongly improve support and quality of life.")
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
Cyan → School / environment pathway
Brown → Family advocacy pathway
Purple → Access / care pathway
Yellow-Green → Social-cultural / structural bias
Red-Pink → Modern diagnostic pressure
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
    label="""AGE 8 GENERAL GRAPH

2010

Formal diagnosis-and-support model
Clear school-family-provider pathway,
stronger advocacy, treatment,
and coordinated support
""",
    shape="box",
    color="#f5f5f5",
    x=760,
    y=250,
    fixed=True,
    physics=False
)

filename = "2010_age_8_updated.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))