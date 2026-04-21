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
# Individual → ADHD
# -------------------------
("Genetic Risk", "ADHD", "+"),

# -------------------------
# ADHD → Symptoms & Impairment
# -------------------------
("ADHD", "Symptom Severity", "+"),
("ADHD", "Symptom Type", "+"),
("ADHD", "Comorbid Conditions", "+"),
("ADHD", "Functional Impairment", "+"),
("ADHD", "Quality of Life", "-"),
("ADHD", "Misdiagnosis Rate", "-"),

# -------------------------
# Age Effects
# -------------------------
("Age", "Symptom Severity", "-"),
("Age", "Diagnosis Status", "+"),

# -------------------------
# Gender Effects
# -------------------------
("Gender", "Diagnosis Status", "+"),
("Gender", "Symptom Type", "+"),

# -------------------------
# Symptoms → Detection
# -------------------------
("Symptom Severity", "Diagnosis Status", "+"),
("Symptom Type", "Teacher Referral Rate", "+"),
("Teacher Referral Rate", "Diagnosis Status", "+"),

# -------------------------
# Family & Home Environment
# -------------------------
("Parental Awareness", "Diagnosis Status", "+"),
("Parenting Style", "Symptom Severity", "-"),
("Family Stress", "Symptom Severity", "+"),
("Family Stress", "Comorbid Conditions", "+"),
("Household Stability", "Family Stress", "-"),

# -------------------------
# School & Workplace
# -------------------------
("Classroom Size", "Teacher Referral Rate", "+"),
("Academic Demands", "Functional Impairment", "+"),
("Functional Impairment", "Diagnosis Status", "+"),
("School Resources", "Diagnosis Status", "+"),
("Workplace Accommodations", "Functional Impairment", "-"),

# -------------------------
# Health Care Access
# -------------------------
("Access to Mental Health Care", "Diagnosis Status", "+"),
("Provider Availability", "Diagnosis Status", "+"),
("Waiting Time for Assessment", "Diagnosis Status", "-"),
("Cost of Evaluation", "Diagnosis Status", "-"),
("Diagnostic Criteria Variability", "Diagnosis Status", "+"),
("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+"),

# -------------------------
# Social & Cultural
# -------------------------
("Stigma", "Parental Awareness", "-"),
("Stigma", "Diagnosis Status", "-"),
("Gender Bias", "Diagnosis Status", "+"),
("Cultural Norms", "Stigma", "+"),
("Socioeconomic Status", "Access to Mental Health Care", "+"),
("Socioeconomic Status", "Parental Awareness", "+"),
("Socioeconomic Status", "Cost of Evaluation", "-"),

# -------------------------
# Comorbidity & Outcomes
# -------------------------
("Comorbid Conditions", "Functional Impairment", "+"),
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
filename = "adhd_full_causal_network.html"


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
net.write_html(filename)

print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))