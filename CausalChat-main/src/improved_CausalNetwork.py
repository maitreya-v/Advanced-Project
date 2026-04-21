from pyvis.network import Network
import webbrowser
import os

net = Network(
    height="900px",
    width="100%",
    directed=True,
    bgcolor="#ffffff",
    font_color="black"
)

# -----------------------------
# Physics Settings
# -----------------------------

net.barnes_hut(
    gravity=-8000,
    central_gravity=0.2,
    spring_length=240,
    spring_strength=0.02
)
net.add_node(
    "ADHD",
    label="ADHD (Underlying Disorder)",
    color="#1f77b4",
    size=45,
    x=0,
    y=0,
    physics=False
)

net.add_node(
    "Diagnosis Status",
    label="Diagnosis Status",
    color="#ff7f0e",
    size=45,
    x=0,
    y=-250,
    physics=False
)


# -----------------------------
# Node Categories
# -----------------------------

node_types = {

    "ADHD":"root",
    "Diagnosis Status":"outcome",

    "Symptom Severity":"mediator",
    "Functional Impairment":"mediator",
    "Teacher Referral Rate":"mediator",

    "Socioeconomic Status":"confounder",
    "Gender":"confounder",

    "Cultural Norms":"latent"
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
# Fixed Node Positions (REFERENCE LAYOUT)
# -----------------------------

node_positions = {

# ROOT
"ADHD": (0,0),

# BIOLOGICAL
"Genetic Risk": (-300,-150),
"Age": (-150,-150),
"Gender": (150,-150),

# SYMPTOMS
"Symptom Severity": (-250,120),
"Symptom Type": (-350,120),
"Comorbid Conditions": (250,120),

# FUNCTIONAL
"Functional Impairment": (0,200),
"Misdiagnosis Rate": (350,120),

# FAMILY
"Parental Awareness": (-450,250),
"Parenting Style": (-550,220),
"Family Stress": (-300,250),
"Household Stability": (-450,320),

# SCHOOL
"Teacher Referral Rate": (-350,360),
"Classroom Size": (-450,450),
"School Resources": (-200,420),
"Academic Demands": (200,220),

# WORK
"Workplace Accommodations": (320,260),

# HEALTHCARE
"Access to Mental Health Care": (350,350),
"Provider Availability": (520,350),
"Diagnostic Criteria Variability": (150,300),
"Waiting Time for Assessment": (300,420),
"Cost of Evaluation": (200,500),

# SOCIAL
"Stigma": (-100,350),
"Gender Bias": (100,420),
"Cultural Norms": (-150,450),
"Socioeconomic Status": (450,450),

# DIAGNOSIS
"Diagnosis Status": (0,520),
"Age at Diagnosis": (-50,600),

# OUTCOME
"Quality of Life": (0,700)
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

    x,y = node_positions.get(node,(0,0))

    net.add_node(
        node,
        label=node,
        color=colors[ntype],
        size=40 if ntype in ["root","outcome"] else 25,
        title=f"Node type: {ntype}",
        x=x,
        y=y,
        physics=True
    )

# -----------------------------
# Edges With Weights
# -----------------------------

edges = [

("Genetic Risk","ADHD","+",0.85),

("ADHD","Symptom Severity","+",0.9),
("ADHD","Symptom Type","+",0.65),
("ADHD","Comorbid Conditions","+",0.6),
("ADHD","Functional Impairment","+",0.9),
("ADHD","Quality of Life","-",0.75),
("ADHD","Misdiagnosis Rate","-",0.4),

("Age","Diagnosis Status","+",0.35),
("Gender","Diagnosis Status","+",0.3),

("Symptom Severity","Diagnosis Status","+",0.9),
("Symptom Type","Teacher Referral Rate","+",0.65),
("Teacher Referral Rate","Diagnosis Status","+",0.8),

("Parental Awareness","Diagnosis Status","+",0.65),
("Parenting Style","Symptom Severity","-",0.3),
("Family Stress","Symptom Severity","+",0.55),
("Household Stability","Family Stress","-",0.6),

("Classroom Size","Teacher Referral Rate","+",0.5),
("Academic Demands","Functional Impairment","+",0.55),

("Access to Mental Health Care","Diagnosis Status","+",0.9),
("Provider Availability","Diagnosis Status","+",0.8),
("Waiting Time for Assessment","Diagnosis Status","-",0.6),
("Cost of Evaluation","Diagnosis Status","-",0.55),

("Stigma","Diagnosis Status","-",0.65),
("Socioeconomic Status","Access to Mental Health Care","+",0.75),

("Functional Impairment","Quality of Life","-",0.9),
("Diagnosis Status","Quality of Life","+",0.75)

]

for u,v,sign,power in edges:

    color = "green" if sign=="+" else "red"

    net.add_edge(
        u,
        v,
        color=color,
        width=power*8,
        value=power,
        arrows="to",
        title=f"""
Causal Relationship

Direction: {u} → {v}
Effect: {"Positive" if sign=="+" else "Negative"}
Causal Power: {power:.2f}
"""
    )

# -----------------------------
# Enable Node Interaction
# -----------------------------

net.set_options("""
{
  "layout": {
    "improvedLayout": true
  },
  "physics": {
    "enabled": false
  },
  "interaction": {
    "dragNodes": true,
    "dragView": true,
    "zoomView": true,
    "hover": true
  }
}
""")

# -----------------------------
# Legend
# -----------------------------

net.add_node(
    "Legend",
    label="""
Legend

Green Edge (+) : Positive Effect
Red Edge (-)   : Negative Effect

Blue Node      : Root Cause
Orange Node    : Outcome
Green Node     : Mediator
Purple Node    : Confounder
Yellow Node    : Latent Factor
""",
    shape="box",
    physics=False,
    color="#f5f5f5",
    x=-900,
    y=-600
)
# -----------------------------
# Save Graph
# -----------------------------

filename = "adhd_causal_network_meeting_ready.html"

net.write_html(filename)

print("Graph saved:",filename)

webbrowser.open("file://" + os.path.realpath(filename))