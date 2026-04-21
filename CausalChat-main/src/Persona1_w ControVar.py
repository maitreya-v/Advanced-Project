from pyvis.network import Network
import webbrowser, os

net = Network(height="800px", width="100%", directed=True)

# -----------------------------
# Physics Layout
# -----------------------------
net.barnes_hut(
    gravity=-4000,
    central_gravity=0.3,
    spring_length=180,
    spring_strength=0.05,
    damping=0.6
)

# -----------------------------
# Behavior Clusters
# -----------------------------
node_groups = {
    "ADHD": "core",
    "Diagnosis Status": "core",
    "Quality of Life": "core",

    "Genetic Risk": "clinical",
    "Executive Function Deficit": "clinical",
    "Symptom Severity": "clinical",
    "Functional Impairment": "clinical",

    "Nutrition Quality": "environment",
    "Sleep Quality": "environment",
    "Screen Time Exposure": "environment",
    "Early Childhood Exposure": "environment",
    "Digital Distraction Environment": "environment",

    "Parental Mental Health": "family",
    "Family History Awareness": "family",
    "Home Structure Stability": "family",

    "Financial Status": "access",
    "Race / Ethnicity": "access",
    "Neighborhood Quality": "access",
    "Access to Mental Health Care": "access",
    "Cost of Evaluation": "access",
    "Clinical Guidelines Evolution": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",

    "Social Media Awareness": "controversial",
    "Self-Diagnosis Behavior": "controversial",
    "Overdiagnosis Pressure": "controversial",
    "Diagnosis Feedback Loop": "controversial"
}

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
    "environment": "Environmental exposure variables",
    "family": "Family-context variables",
    "access": "Socioeconomic / healthcare access variables",
    "bias": "Social-cultural bias / latent variables",
    "controversial": "Controversial or debated dynamics",
    "factor": "Observed variable"
}

# -----------------------------
# Nodes
# -----------------------------
nodes = [
    "ADHD","Diagnosis Status","Quality of Life",
    "Genetic Risk","Executive Function Deficit",
    "Nutrition Quality","Sleep Quality","Screen Time Exposure",
    "Early Childhood Exposure","Digital Distraction Environment",
    "Parental Mental Health","Family History Awareness",
    "Home Structure Stability",
    "Symptom Severity","Functional Impairment",
    "Financial Status","Race / Ethnicity","Neighborhood Quality",
    "Access to Mental Health Care","Cost of Evaluation",
    "Clinical Guidelines Evolution",
    "Social Media Awareness","Self-Diagnosis Behavior",
    "Overdiagnosis Pressure","Diagnosis Feedback Loop",
    "Stigma","Cultural Norms"
]

# -----------------------------
# Add Nodes
# -----------------------------
for node in nodes:
    group = node_groups.get(node, "factor")
    net.add_node(
        node,
        label=node,
        color=group_colors.get(group, "#dddddd"),
        size=45 if node == "ADHD" else 40 if node == "Diagnosis Status" else 30 if node == "Quality of Life" else 25,
        title=f"""
Node: {node}

Cluster: {group.upper()}

Description:
{group_descriptions.get(group, "Observed variable")}
"""
    )

# -----------------------------
# Edges
# -----------------------------
edges = [
    ("Genetic Risk","ADHD","+",0.85),
    ("ADHD","Executive Function Deficit","+",0.9),

    ("Nutrition Quality","Symptom Severity","-",0.6),
    ("Sleep Quality","Executive Function Deficit","-",0.7),
    ("Screen Time Exposure","Symptom Severity","+",0.7),
    ("Digital Distraction Environment","Screen Time Exposure","+",0.8),

    ("Parental Mental Health","Home Structure Stability","-",0.7),
    ("Home Structure Stability","Symptom Severity","-",0.6),

    ("Executive Function Deficit","Functional Impairment","+",0.8),
    ("Symptom Severity","Functional Impairment","+",0.85),

    ("Financial Status","Access to Mental Health Care","+",0.8),
    ("Race / Ethnicity","Access to Mental Health Care","-",0.6),

    ("Access to Mental Health Care","Diagnosis Status","+",0.85),
    ("Cost of Evaluation","Diagnosis Status","-",0.7),

    ("Social Media Awareness","Self-Diagnosis Behavior","+",0.7),
    ("Self-Diagnosis Behavior","Diagnosis Status","+",0.6),
    ("Overdiagnosis Pressure","Diagnosis Status","+",0.75),

    ("Diagnosis Status","Diagnosis Feedback Loop","+",0.7),
    ("Diagnosis Feedback Loop","Self-Diagnosis Behavior","+",0.6),

    ("Diagnosis Status","Functional Impairment","-",0.6),
    ("Functional Impairment","Quality of Life","-",0.9),
    ("Diagnosis Status","Quality of Life","+",0.8),

    ("Cultural Norms","Stigma","+",0.7),
    ("Stigma","Diagnosis Status","-",0.75)
]

for u, v, s, p in edges:
    net.add_edge(
        u, v,
        color="green" if s == "+" else "red",
        width=p * 8,
        arrows="to",
        title=f"{u} → {v}\nEffect: {s}\nPower: {p}"
    )

net.set_options("""
{
  "physics": {"enabled": true},
  "interaction": {"hover": true, "dragNodes": true, "zoomView": true}
}
""")

# -----------------------------
# Legend
# -----------------------------
net.add_node(
    "LEGEND",
    label="""
LEGEND

Green Edge → Positive Effect
Red Edge → Negative Effect
Edge Thickness → Causal Power

NODE CLUSTERS:
Blue → Core disorder / outcomes
Green → Clinical-cognitive pathway
Cyan → Environmental exposure
Brown → Family context
Purple → Socioeconomic / access
Yellow-Green → Social-cultural bias
Red-Pink → Controversial dynamics
""",
    shape="box",
    color="#f5f5f5",
    physics=False,
    x=-900,
    y=-600
)

net.add_node(
    "PERSONA_DESC",
    label="""
PERSONA 1: Undiagnosed Adult

• 45-year-old individual
• High stigma & cultural resistance
• Low financial status
• Limited healthcare access

KEY DYNAMICS:
• Underdiagnosis despite symptoms
• Self-diagnosis influence
• Cost and access barriers
""",
    shape="box",
    color="#f5f5f5",
    physics=False,
    x=900,
    y=-600
)

net.write_html("persona1_clustered.html")
webbrowser.open("persona1_clustered.html")