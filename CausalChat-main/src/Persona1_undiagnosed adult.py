from pyvis.network import Network
import webbrowser
import os

# -----------------------------
# Create Network
# -----------------------------

net = Network(
    height="800px",
    width="100%",
    directed=True,
    bgcolor="#ffffff",
    font_color="black"
)

# -----------------------------
# Physics Layout (Interactive)
# -----------------------------

net.barnes_hut(
    gravity=-9000,
    central_gravity=0.12,
    spring_length=220,
    spring_strength=0.02,
    damping=0.4
)

# -----------------------------
# Node Categories
# -----------------------------

node_types = {

"ADHD":"root",
"Diagnosis Status":"outcome",

"Symptom Severity":"mediator",
"Functional Impairment":"mediator",
"Comorbid Conditions":"mediator",

"Socioeconomic Status":"confounder",

"Cultural Norms":"latent",
"Stigma":"latent"
}

colors = {
"root":"#1f77b4",
"outcome":"#ff7f0e",
"mediator":"#2ca02c",
"confounder":"#9467bd",
"latent":"#ffd92f",
"factor":"#dddddd"
}

# -----------------------------
# All Nodes
# -----------------------------

nodes = [

"ADHD","Diagnosis Status","Age","Gender","Genetic Risk",
"Symptom Severity","Symptom Type","Comorbid Conditions",

"Parental Awareness","Parenting Style","Family Stress",
"Household Stability","Teacher Referral Rate","Classroom Size",

"Academic Demands","School Resources","Workplace Accommodations",

"Access to Mental Health Care","Provider Availability",
"Diagnostic Criteria Variability","Waiting Time for Assessment",
"Cost of Evaluation","Stigma","Gender Bias","Cultural Norms",
"Socioeconomic Status","Age at Diagnosis","Misdiagnosis Rate",
"Functional Impairment","Quality of Life"
]

# -----------------------------
# Reference Node Positions (from base causal network)
# -----------------------------

node_positions = {

"ADHD": (0, 0),
"Diagnosis Status": (0, -220),

"Genetic Risk": (0, 180),

"Symptom Severity": (-120, -80),
"Symptom Type": (-200, 0),
"Functional Impairment": (0, -60),
"Comorbid Conditions": (120, 40),

"Age": (80, -150),
"Gender": (-80, -150),

"Socioeconomic Status": (220, -20),
"Cost of Evaluation": (180, -100),
"Access to Mental Health Care": (160, 40),

"Stigma": (200, 80),
"Cultural Norms": (320, 80),

"Workplace Accommodations": (100, 120),

"Quality of Life": (-60, -180)
}

# -----------------------------
# Add Nodes Using Reference Layout
# -----------------------------

for node in nodes:

    ntype = node_types.get(node, "factor")

    x, y = node_positions.get(node, (0, 0))

    net.add_node(
        node,
        label=node,
        color=colors[ntype],
        size=40 if ntype in ["root","outcome"] else 25,
        title=f"Node type: {ntype}",
        x=x,
        y=y,
        physics=False
    )

# -----------------------------
# Causal Edges with Causal Power
# -----------------------------

edges = [

("Genetic Risk","ADHD","+",0.85),

("ADHD","Symptom Severity","+",0.9),
("ADHD","Symptom Type","+",0.7),
("ADHD","Functional Impairment","+",0.9),
("ADHD","Comorbid Conditions","+",0.7),

("Symptom Severity","Functional Impairment","+",0.8),
("Symptom Type","Functional Impairment","+",0.6),

("Age","Diagnosis Status","-",0.4),

("Socioeconomic Status","Access to Mental Health Care","+",0.75),
("Socioeconomic Status","Cost of Evaluation","-",0.6),

("Access to Mental Health Care","Diagnosis Status","+",0.85),
("Cost of Evaluation","Diagnosis Status","-",0.65),

("Cultural Norms","Stigma","+",0.7),
("Stigma","Diagnosis Status","-",0.75),

("Workplace Accommodations","Functional Impairment","-",0.5),

("Functional Impairment","Comorbid Conditions","+",0.65),
("Comorbid Conditions","Diagnosis Status","+",0.75),

("Diagnosis Status","Functional Impairment","-",0.6),

("Functional Impairment","Quality of Life","-",0.9),
("Diagnosis Status","Quality of Life","+",0.8)

]

for u,v,sign,power in edges:

    color = "green" if sign=="+" else "red"

    net.add_edge(
        u,
        v,
        color=color,
        width=power*8,
        arrows="to",
        title=f"""
Causal Relationship

{u} → {v}

Effect: {"Positive" if sign=="+" else "Negative"}
Causal Power: {power}
"""
    )

# -----------------------------
# Interaction Settings
# -----------------------------

net.set_options("""
{
  "interaction": {
    "dragNodes": true,
    "dragView": true,
    "zoomView": true,
    "hover": true
  },
  "physics": {
    "enabled": false
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

Green Edge → Positive Effect
Red Edge → Negative Effect

Blue Node → Root Cause
Orange Node → Outcome
Green Node → Mediator
Purple Node → Confounder
Yellow Node → Latent Variable
""",
shape="box",
color="#f5f5f5",
physics=False
)

# -----------------------------
# Persona Description
# -----------------------------

net.add_node(
"Persona",
label="""
PERSONA 1

45-year-old male
Hyperactive ADHD presentation
Low socioeconomic status
High stigma
Limited access to healthcare
Undiagnosed ADHD
""",
shape="box",
color="#f5f5f5",
physics=False
)

# -----------------------------
# Save Graph
# -----------------------------

filename="adhd_persona1_causal_network.html"

net.write_html(filename)

print("Graph saved:",filename)

webbrowser.open("file://" + os.path.realpath(filename))