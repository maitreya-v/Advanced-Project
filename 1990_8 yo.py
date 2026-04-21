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

# ---------------------------------------------------
# Cluster colors
# ---------------------------------------------------
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
    "school": "School detection pathway",
    "family": "Family response pathway",
    "access": "Healthcare access / economic barriers",
    "bias": "Social-cultural / structural bias variables",
    "environment": "Environmental and developmental exposure variables",
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
    "School Labeling Bias": "school",
    "Classroom Size": "school",
    "School Resources": "school",
    "Education System Pressure": "school",

    "Parental Awareness": "family",
    "Parental Denial": "family",
    "Family Stress": "family",
    "Household Stability": "family",
    "Parental Education": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Financial Status": "access",
    "Neighborhood Quality": "access",
    "Educational Access": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",
    "Gender": "bias",
    "Race / Ethnicity": "bias",
    "Institutional Bias": "bias",

    "Nutrition Quality": "environment",
    "Early Life Nutrition": "environment",
    "Sleep Quality": "environment",
    "Environmental Exposure": "environment",

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
    ("Parental Denial", -620, 120),
    ("Family Stress", -380, 130),
    ("Household Stability", -500, 320),
    ("Parental Education", -650, 250),

    ("Teacher Referral Rate", -100, -420),
    ("Classroom Size", 80, -500),
    ("School Labeling Bias", 100, -340),
    ("School Resources", 260, -380),
    ("Education System Pressure", 420, -520),

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
    ("Educational Access", 500, -350),

    ("Stigma", 400, -300),
    ("Cultural Norms", 550, -380),
    ("Race / Ethnicity", 520, -150),
    ("Institutional Bias", 300, -250),

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
    ("Gender", "Symptom Type", "+", 0.40, "Gender norms influence which childhood behaviors are noticed."),

    ("Early Life Nutrition", "Genetic Risk", "-", 0.20, "Poor early nutrition can increase developmental vulnerability."),
    ("Nutrition Quality", "Symptom Severity", "-", 0.54, "Poor nutrition may worsen behavioral regulation."),
    ("Sleep Quality", "Symptom Severity", "-", 0.64, "Better sleep reduces behavioral dysregulation."),
    ("Environmental Exposure", "Symptom Severity", "+", 0.42, "Environmental stressors can worsen symptoms."),

    ("Symptom Severity", "Functional Impairment", "+", 0.84, "More severe symptoms increase impairment."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.72, "Certain symptom patterns are more likely to trigger teacher concern."),
    ("Classroom Size", "Teacher Referral Rate", "+", 0.44, "Classroom context can increase teacher concern."),
    ("School Labeling Bias", "Teacher Referral Rate", "+", 0.70, "Behavioral labeling still strongly shapes referrals."),
    ("School Resources", "Teacher Referral Rate", "+", 0.46, "In 1990, school resources increasingly support detection."),
    ("Education System Pressure", "Teacher Referral Rate", "+", 0.52, "Institutional pressure can increase school referrals."),

    ("Teacher Referral Rate", "Parental Awareness", "+", 0.78, "School concerns more reliably increase parent awareness."),
    ("Parental Denial", "Parental Awareness", "-", 0.74, "Denial still reduces recognition of child difficulties."),
    ("Parental Education", "Parental Awareness", "+", 0.60, "More educated parents better recognize childhood issues."),
    ("Parental Education", "Parental Denial", "-", 0.44, "Education reduces denial probability."),
    ("Family Stress", "Symptom Severity", "+", 0.56, "Stressful homes can amplify visible symptoms."),
    ("Household Stability", "Family Stress", "-", 0.70, "Stable homes reduce stress."),
    ("Household Stability", "Nutrition Quality", "+", 0.60, "Stable homes support better nutrition."),
    ("Family Stress", "Sleep Quality", "-", 0.56, "Stress disrupts sleep patterns."),

    ("Parental Awareness", "Diagnosis Status", "+", 0.64, "Parental awareness meaningfully supports diagnosis by 1990."),
    ("Socioeconomic Status", "Educational Access", "+", 0.72, "Higher SES improves educational access."),
    ("Educational Access", "Teacher Referral Rate", "+", 0.40, "Better systems may detect issues earlier."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.70, "Higher SES improves access to care."),
    ("Financial Status", "Access to Mental Health Care", "+", 0.78, "Affordability strongly controls access."),
    ("Neighborhood Quality", "Access to Mental Health Care", "+", 0.46, "Better neighborhoods provide more resources."),
    ("Provider Availability", "Access to Mental Health Care", "+", 0.62, "Provider supply improves access more than in 1970."),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.72, "Cost remains a substantial barrier to evaluation."),
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.66, "Access meaningfully improves diagnosis likelihood."),

    ("Race / Ethnicity", "Institutional Bias", "+", 0.68, "Structural inequities influence institutional behavior."),
    ("Institutional Bias", "Teacher Referral Rate", "+", 0.60, "Bias affects referral and labeling patterns."),
    ("Institutional Bias", "Diagnosis Status", "-", 0.54, "Bias suppresses fair diagnosis access."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.56, "Misdiagnosis reduces accurate identification."),

    ("Cultural Norms", "Stigma", "+", 0.74, "Stigma remains significant, but weaker than in 1970."),
    ("Stigma", "Diagnosis Status", "-", 0.68, "Stigma still suppresses recognition and diagnosis."),

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
Cyan → School / environment pathway
Brown → Family pathway
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
    label="""AGE 8 GENERAL GRAPH

1990

Transitional school-detection model
More institutional recognition than 1970,
but stigma, labeling bias, and inequality
still matter structurally
""",
    shape="box",
    color="#f5f5f5",
    x=760,
    y=250,
    fixed=True,
    physics=False
)

filename = "1990_age_8_updated.html"
net.write_html(filename)
print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))