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
"Teacher Referral Rate":"mediator",
"Parental Awareness":"mediator",
"Functional Impairment":"mediator",

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

for node in nodes:

    ntype = node_types.get(node,"factor")

    net.add_node(
        node,
        label=node,
        color=colors[ntype],
        size=40 if ntype in ["root","outcome"] else 25,
        title=f"Node type: {ntype}"
    )

# -----------------------------
# Causal Edges with Causal Power
# -----------------------------

edges = [

("Genetic Risk","ADHD","+",0.85),

("ADHD","Symptom Severity","+",0.9),
("ADHD","Symptom Type","+",0.75),
("ADHD","Functional Impairment","+",0.75),

("Symptom Severity","Teacher Referral Rate","+",0.85),
("Teacher Referral Rate","Parental Awareness","+",0.8),

("Parental Awareness","Diagnosis Status","+",0.9),

("School Resources","Teacher Referral Rate","+",0.8),
("Classroom Size","Teacher Referral Rate","+",0.6),
("Academic Demands","Functional Impairment","+",0.65),

("Access to Mental Health Care","Diagnosis Status","+",0.85),
("Provider Availability","Diagnosis Status","+",0.75),

("Diagnosis Status","Functional Impairment","-",0.75),
("Diagnosis Status","Quality of Life","+",0.85),

("Functional Impairment","Quality of Life","-",0.8)
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
PERSONA 2

8-year-old child
Combined ADHD presentation
Strong parental awareness
Supportive school environment
Teacher referral pathway active
Early diagnosis and intervention
""",
shape="box",
color="#f5f5f5",
physics=False
)

# -----------------------------
# Save Graph
# -----------------------------

filename="adhd_persona2_causal_network.html"

net.write_html(filename)

print("Graph saved:",filename)

webbrowser.open("file://" + os.path.realpath(filename))