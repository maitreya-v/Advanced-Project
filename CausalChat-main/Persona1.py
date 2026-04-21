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
    bgcolor="#ffffff"
)



# Stable physics (minimal wobble)
net.barnes_hut(
    gravity=-9000,
    central_gravity=0.1,
    spring_length=220,
    spring_strength=0.01,
    damping=0.4
)

# -----------------------------
# Main Nodes
# -----------------------------

net.add_node("ADHD",
             label="ADHD (Underlying Disorder)",
             color="#1f77b4",
             size=45,
             font={"size": 18, "color": "black", "bold": True})

net.add_node("Diagnosis Status",
             label="Diagnosis Status",
             color="#ff7f0e",
             size=45,
             font={"size": 18, "color": "black", "bold": True})

# -----------------------------
# ALL Other Variables
# -----------------------------

all_nodes = [

# Individual
"Age", "Gender", "Genetic Risk", "Symptom Severity",
"Symptom Type", "Comorbid Conditions",

# Family
"Parental Awareness", "Parenting Style",
"Family Stress", "Household Stability",

# School/Work
"Teacher Referral Rate", "Classroom Size",
"Academic Demands", "School Resources",
"Workplace Accommodations",

# Healthcare
"Access to Mental Health Care",
"Provider Availability",
"Diagnostic Criteria Variability",
"Waiting Time for Assessment",
"Cost of Evaluation",

# Social
"Stigma", "Gender Bias",
"Cultural Norms", "Socioeconomic Status",

# Outcomes
"Age at Diagnosis",
"Misdiagnosis Rate",
"Functional Impairment",
"Quality of Life"
]

for node in all_nodes:
    net.add_node(node,
                 label=node,
                 color="#dddddd",
                 size=25,
                 font={"size": 13})

# -----------------------------
# Causal Edges
# -----------------------------

edges = [

# -------------------------
# Core Biological Structure
# -------------------------
("Genetic Risk", "ADHD", "+"),
("ADHD", "Symptom Severity", "+"),
("ADHD", "Symptom Type", "+"),
("ADHD", "Functional Impairment", "+"),
("ADHD", "Comorbid Conditions", "+"),

# -------------------------
# Symptom Expression
# -------------------------
("Symptom Severity", "Functional Impairment", "+"),
("Symptom Type", "Functional Impairment", "+"),

# -------------------------
# Age (adult missed childhood detection)
# -------------------------
("Age", "Diagnosis Status", "-"),

# -------------------------
# Socioeconomic Barriers
# -------------------------
("Socioeconomic Status", "Access to Mental Health Care", "+"),  
# (Low SES → less access; sign reflects higher SES increases access)

("Socioeconomic Status", "Cost of Evaluation", "-"),
# (Higher SES reduces cost burden)

("Access to Mental Health Care", "Diagnosis Status", "+"),
("Cost of Evaluation", "Diagnosis Status", "-"),

# -------------------------
# Stigma & Cultural Suppression
# -------------------------
("Cultural Norms", "Stigma", "+"),
("Stigma", "Diagnosis Status", "-"),

# -------------------------
# Workplace Context
# -------------------------
("Workplace Accommodations", "Functional Impairment", "-"),

# -------------------------
# Impairment-Driven Detection (Crisis pathway)
# -------------------------
("Functional Impairment", "Comorbid Conditions", "+"),
("Comorbid Conditions", "Diagnosis Status", "+"),

# -------------------------
# Outcomes
# -------------------------
("Diagnosis Status", "Functional Impairment", "-"),
("Functional Impairment", "Quality of Life", "-"),
("Diagnosis Status", "Quality of Life", "+"),

]

for u, v, sign in edges:
    color = "green" if sign == "+" else "red"
    net.add_edge(u, v, label=sign, color=color, arrows="to")

# -----------------------------
# Freeze Layout (optional)
# -----------------------------
net.toggle_physics(False)

# -----------------------------
# Save + Open
# -----------------------------
filename = "adhd_persona1_causal network.html"


net.add_node(
    "LEGEND_NODE",
    label="LEGEND:\n\nGreen Edge (+): Positive Effect\nRed Edge (-): Negative Effect\nArrow: Causal Direction",
    shape="box",
    color="#f5f5f5",
    size=30,
    font={
        "size": 14,
        "color": "black",
        "face": "Arial"
    },
    physics=False
)

net.add_node(
    "Persona",
    label="PERSONA:\n\n45-year-old male, hyperactive presentation, low SES, high stigma, limited access, undiagnosed",
    shape="box",
    color="#f5f5f5",
    size=30,
    font={
        "size": 14,
        "color": "black",
        "face": "Arial"
    },
    physics=False
)
net.write_html(filename)

print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))