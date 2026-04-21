from pyvis.network import Network
import webbrowser, os

net = Network(height="800px", width="100%", directed=True)

# -----------------------------
# Physics Layout
# -----------------------------
net.barnes_hut(
    gravity=-4500,
    central_gravity=0.25,
    spring_length=170,
    spring_strength=0.06,
    damping=0.65
)

# -----------------------------
# Behavior Clusters
# -----------------------------
node_groups = {
    "ADHD": "core",
    "Diagnosis Status": "core",
    "Quality of Life": "core",

    "Genetic Risk": "clinical",
    "Symptom Severity": "clinical",
    "Functional Impairment": "clinical",
    "Symptom Type": "clinical",
    "Misdiagnosis Rate": "clinical",

    "Teacher Referral Rate": "school",
    "School Resources": "school",
    "Classroom Size": "school",
    "School Labeling Bias": "school",
    "Education System Pressure": "school",
    "Academic Competition": "school",
    "Peer Comparison": "school",

    "Parental Awareness": "family",
    "Parental Denial": "family",

    "Access to Mental Health Care": "access",
    "Provider Availability": "access",
    "Cost of Evaluation": "access",
    "Socioeconomic Status": "access",
    "Regional Resource Inequality": "access",

    "Stigma": "bias",
    "Cultural Norms": "bias",

    "Overdiagnosis Pressure": "controversial",
    "Treatment Dependency": "controversial"
}

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
    "school": "School detection / institutional variables",
    "family": "Family response variables",
    "access": "Access / inequality variables",
    "bias": "Social-cultural bias / latent variables",
    "controversial": "Controversial or debated dynamics",
    "factor": "Observed variable"
}

# -----------------------------
# Nodes
# -----------------------------
nodes = [
    "ADHD","Diagnosis Status","Quality of Life",
    "Genetic Risk",
    "Symptom Severity","Functional Impairment","Symptom Type",
    "Teacher Referral Rate","School Resources","Classroom Size",
    "School Labeling Bias","Education System Pressure",
    "Academic Competition","Peer Comparison",
    "Parental Awareness","Parental Denial",
    "Access to Mental Health Care","Provider Availability",
    "Cost of Evaluation","Misdiagnosis Rate",
    "Socioeconomic Status","Regional Resource Inequality",
    "Overdiagnosis Pressure","Treatment Dependency",
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

    ("ADHD","Symptom Severity","+",0.9),
    ("ADHD","Functional Impairment","+",0.85),
    ("ADHD","Symptom Type","+",0.7),

    ("Symptom Severity","Functional Impairment","+",0.8),

    ("Functional Impairment","Teacher Referral Rate","+",0.8),
    ("Symptom Severity","Teacher Referral Rate","+",0.85),
    ("Symptom Type","Misdiagnosis Rate","+",0.6),

    ("School Resources","Teacher Referral Rate","+",0.75),
    ("Classroom Size","Teacher Referral Rate","+",0.6),
    ("School Labeling Bias","Teacher Referral Rate","+",0.75),
    ("Education System Pressure","Teacher Referral Rate","+",0.7),

    ("Peer Comparison","Parental Awareness","+",0.7),
    ("Academic Competition","Functional Impairment","+",0.65),

    ("Teacher Referral Rate","Parental Awareness","+",0.85),
    ("Parental Denial","Parental Awareness","-",0.8),

    ("Parental Awareness","Diagnosis Status","+",0.9),
    ("Access to Mental Health Care","Diagnosis Status","+",0.85),
    ("Cost of Evaluation","Diagnosis Status","-",0.7),

    ("Misdiagnosis Rate","Diagnosis Status","-",0.6),

    ("Overdiagnosis Pressure","Diagnosis Status","+",0.75),

    ("Diagnosis Status","Treatment Dependency","+",0.8),
    ("Treatment Dependency","Functional Impairment","-",0.6),
    ("Functional Impairment","Teacher Referral Rate","+",0.6),

    ("Socioeconomic Status","Access to Mental Health Care","+",0.75),
    ("Regional Resource Inequality","School Resources","-",0.8),

    ("Cultural Norms","Stigma","+",0.7),
    ("Stigma","Diagnosis Status","-",0.65),

    ("Diagnosis Status","Quality of Life","+",0.8),
    ("Functional Impairment","Quality of Life","-",0.85)
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
  "interaction": {
    "hover": true,
    "dragNodes": true,
    "zoomView": true
  },
  "physics": {
    "enabled": true
  }
}
""")

# -----------------------------
# Legend
# -----------------------------
net.add_node(
    "LEGEND",
    label="""
LEGEND

Green Edge → Positive
Red Edge → Negative
Thickness → Causal Power

NODE CLUSTERS:
Blue → Core disorder / outcomes
Green → Clinical symptom pathway
Cyan → School / institutional pathway
Brown → Family response
Purple → Access / inequality
Yellow-Green → Social-cultural bias
Red-Pink → Controversial dynamics
""",
    shape="box",
    color="#f5f5f5",
    physics=False
)

net.add_node(
    "PERSONA",
    label="""
PERSONA 2 (Enhanced)

8-year-old child

• Strong school detection system
• High teacher involvement
• Early intervention pathway

⚠️ Complex Effects:
• School labeling bias
• Education pressure
• Overdiagnosis risk
""",
    shape="box",
    color="#f5f5f5",
    physics=False
)

net.write_html("persona2_clustered.html")
webbrowser.open("persona2_clustered.html")