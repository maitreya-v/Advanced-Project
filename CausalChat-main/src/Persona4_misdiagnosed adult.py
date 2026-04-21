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
"Misdiagnosis Rate":"mediator",

"Diagnostic Criteria Variability":"confounder",

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
("ADHD","Comorbid Conditions","+",0.8),

("Symptom Severity","Comorbid Conditions","+",0.75),
("Comorbid Conditions","Functional Impairment","+",0.8),

("Diagnostic Criteria Variability","Misdiagnosis Rate","+",0.9),
("Comorbid Conditions","Misdiagnosis Rate","+",0.85),

("Misdiagnosis Rate","Diagnosis Status","-",0.75),

("Functional Impairment","Access to Mental Health Care","+",0.75),
("Access to Mental Health Care","Diagnosis Status","+",0.8),

("Diagnosis Status","Quality of Life","+",0.7),
("Functional Impairment","Quality of Life","-",0.9),

("Stigma","Access to Mental Health Care","-",0.7)
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
PERSONA 4

28-year-old adult
ADHD with high comorbidity burden
Diagnostic ambiguity present
High misdiagnosis probability
Delayed correct diagnosis
""",
shape="box",
color="#f5f5f5",
physics=False
)

# -----------------------------
# Save Graph
# -----------------------------

filename="adhd_persona4_causal_network.html"

net.write_html(filename)

print("Graph saved:",filename)

webbrowser.open("file://" + os.path.realpath(filename))