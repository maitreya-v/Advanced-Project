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
             x=0, y=0,
             font={"size": 18, "color": "black", "bold": True})

net.add_node("Diagnosis Status",
             label="Diagnosis Status",
             color="#ff7f0e",
             size=45,
             x=0, y=350,
             font={"size": 18, "color": "black", "bold": True})

# -----------------------------
# ALL Other Variables
# -----------------------------

positioned_nodes = [

    # Individual — top-left cluster
    ("Age",                     -500, -200),
    ("Gender",                  -380, -200),
    ("Genetic Risk",            -300,  -80),
    ("Symptom Severity",        -200, -200),
    ("Symptom Type",            -200,  -80),
    ("Comorbid Conditions",     -100, -300),

    # Family — left
    ("Parental Awareness",      -500,  200),
    ("Parenting Style",         -500,   80),
    ("Family Stress",           -380,  130),
    ("Household Stability",     -500,  320),

    # School/Work — top-center
    ("Teacher Referral Rate",   -100, -420),
    ("Classroom Size",           100, -500),
    ("Academic Demands",         300, -500),
    ("School Resources",         300, -380),
    ("Workplace Accommodations", 500, -200),

    # Healthcare — right
    ("Access to Mental Health Care",   500,  200),
    ("Provider Availability",          650,   80),
    ("Diagnostic Criteria Variability",300,  420),
    ("Waiting Time for Assessment",    500,  350),
    ("Cost of Evaluation",             500,  480),

    # Social — top-right
    ("Stigma",                   400, -300),
    ("Gender Bias",              200, -300),
    ("Cultural Norms",           550, -380),
    ("Socioeconomic Status",     650,  -80),

    # Outcomes — bottom
    ("Age at Diagnosis",           0,  500),
    ("Misdiagnosis Rate",         200,  480),
    ("Functional Impairment",    -300,  300),
    ("Quality of Life",          -500,  450),

    # Treatment — lower-right
    ("Medication Treatment",      260,  180),
    ("Treatment Access",          720,  220),
    ("Treatment Adherence",       260,  300),
    ("Treatment Side Effects",    720,  320),
]

for node, x, y in positioned_nodes:
    net.add_node(node,
                 label=node,
                 color="#dddddd",
                 size=25,
                 x=x, y=y,
                 font={"size": 13})

# -----------------------------
# EDGE HELPER
# -----------------------------
def add_edge(u, v, sign, strength, explanation):
    color = "green" if sign == "+" else "red"
    effect_text = "Positive" if sign == "+" else "Negative"
    tooltip = (
        f"Effect: {effect_text}\n"
        f"Why: {explanation}\n"
        f"Strength: {strength:.2f}"
    )

    net.add_edge(
        u,
        v,
        label=sign,
        color=color,
        title=tooltip,
        arrows="to"
    )

# -----------------------------
# Causal Edges
# -----------------------------

edges = [

    # Biological causes
    ("Genetic Risk", "ADHD", "+", 0.90, "Genetic vulnerability strongly increases the likelihood of underlying ADHD."),
    ("Comorbid Conditions", "ADHD", "+", 0.45, "Co-occurring conditions can increase the chance that ADHD-related patterns are recognized or reinforced."),

    # ADHD producing symptoms
    ("ADHD", "Symptom Severity", "+", 0.92, "Underlying ADHD directly increases the intensity of symptoms."),
    ("ADHD", "Symptom Type", "+", 0.88, "Underlying ADHD influences the type or presentation of symptoms."),

    # Individual differences
    ("Age", "Symptom Severity", "+", 0.40, "In this graph, age is assumed to increase the visible severity of symptoms."),
    ("Gender", "Symptom Type", "+", 0.42, "Gender can influence which kinds of symptoms are more likely to be noticed or expressed."),

    # Functional outcomes
    ("Symptom Severity", "Functional Impairment", "+", 0.86, "More severe symptoms tend to increase day-to-day impairment."),
    ("Comorbid Conditions", "Functional Impairment", "+", 0.70, "Additional conditions increase the overall functional burden."),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "More impairment reduces overall quality of life."),

    # School detection
    ("Symptom Severity", "Teacher Referral Rate", "+", 0.80, "More severe symptoms make teacher referral more likely."),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.76, "More noticeable symptom types increase teacher referral."),
    ("Classroom Size", "Teacher Referral Rate", "+", 0.38, "Larger classrooms may make attention and behavior issues harder to manage, increasing referrals."),
    ("Academic Demands", "Teacher Referral Rate", "+", 0.60, "Higher academic demands make difficulties more visible to teachers."),
    ("School Resources", "Teacher Referral Rate", "+", 0.50, "More school resources can increase identification and referral."),

    # Family influences
    ("Parenting Style", "Symptom Severity", "+", 0.45, "Parenting style can worsen or amplify the visible severity of symptoms in this model."),
    ("Family Stress", "Symptom Severity", "+", 0.62, "Higher family stress can worsen symptom expression."),
    ("Household Stability", "Family Stress", "-", 0.74, "Greater household stability reduces family stress."),
    ("Parental Awareness", "Diagnosis Status", "+", 0.78, "More parental awareness increases the likelihood of diagnosis."),

    # Healthcare system
    ("Teacher Referral Rate", "Age at Diagnosis", "-", 0.72, "Higher referral rates can lead to earlier diagnosis, lowering age at diagnosis."),
    ("Access to Mental Health Care", "Age at Diagnosis", "-", 0.82, "Better access to care can lead to earlier diagnosis."),
    ("Provider Availability", "Waiting Time for Assessment", "-", 0.76, "More providers reduce waiting time for assessment."),
    ("Waiting Time for Assessment", "Age at Diagnosis", "+", 0.84, "Longer waits delay diagnosis and increase age at diagnosis."),
    ("Cost of Evaluation", "Age at Diagnosis", "+", 0.70, "Higher cost can delay diagnosis and increase age at diagnosis."),

    # Diagnostic process
    ("Age at Diagnosis", "Diagnosis Status", "+", 0.55, "In this graph, reaching the point of diagnosis is linked to age at diagnosis."),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.82, "More variability in criteria increases the chance of misdiagnosis."),
    ("Misdiagnosis Rate", "Diagnosis Status", "-", 0.78, "Higher misdiagnosis reduces accurate diagnosis status."),

    # Social context
    ("Cultural Norms", "Stigma", "+", 0.72, "Cultural norms can increase stigma around ADHD-related behaviors."),
    ("Stigma", "Parental Awareness", "-", 0.68, "More stigma can reduce parental recognition or acknowledgment."),
    ("Gender Bias", "Teacher Referral Rate", "+", 0.74, "Gender bias can increase referral for some groups based on stereotypes."),
    ("Gender Bias", "Diagnosis Status", "+", 0.60, "Gender bias can affect who is more likely to receive a diagnosis."),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.80, "Higher socioeconomic status improves access to mental health care."),
    ("Socioeconomic Status", "Cost of Evaluation", "-", 0.76, "Higher socioeconomic status reduces the effective burden of evaluation cost."),

        # Treatment layer
    ("Diagnosis Status", "Medication Treatment", "+", 0.58, "In the 1970s, receiving a diagnosis could lead to medication treatment, but treatment pathways were less standardized."),
    ("Access to Mental Health Care", "Treatment Access", "+", 0.72, "Better access to care increased the chance that treatment could actually be obtained."),
    ("Socioeconomic Status", "Treatment Access", "+", 0.68, "Families with more resources were better able to reach and sustain treatment."),
    ("Treatment Access", "Medication Treatment", "+", 0.74, "When treatment access was available, medication use became more likely."),
    ("Stigma", "Treatment Adherence", "-", 0.52, "Stigma could reduce willingness to continue or consistently follow treatment."),
    ("Medication Treatment", "Symptom Severity", "-", 0.48, "Medication could reduce visible ADHD symptom burden in some diagnosed children."),
    ("Medication Treatment", "Functional Impairment", "-", 0.34, "Treatment could reduce some school and daily-life impairment, though benefits were less consistently structured than later decades."),
    ("Treatment Adherence", "Medication Treatment", "+", 0.46, "More consistent adherence increased the real-world effect of medication treatment."),
    ("Medication Treatment", "Treatment Side Effects", "+", 0.42, "Medication could introduce side effects that affected comfort or continued use."),
    ("Treatment Side Effects", "Treatment Adherence", "-", 0.40, "Side effects could reduce willingness to stay on treatment."),
    ("Treatment Side Effects", "Quality of Life", "-", 0.18, "Side effects could slightly reduce quality of life for some patients."),
]

for u, v, sign, strength, explanation in edges:
    add_edge(u, v, sign, strength, explanation)

# -----------------------------
# Freeze Layout
# -----------------------------
net.toggle_physics(False)

# -----------------------------
# Save + Open
# -----------------------------
filename = "1970.html"


net.add_node(
    "LEGEND_NODE",
    label="LEGEND:\n\nGreen Edge (+): Positive Effect\nRed Edge (-): Negative Effect\nArrow: Causal Direction",
    shape="box",
    color="#f5f5f5",
    size=30,
    x=700, y=500,
    font={
        "size": 14,
        "color": "black",
        "face": "Arial"
    },
    fixed=True,
    physics=False
)

# net.add_node(
#     "Persona",
#     label="CHRONOLOGICAL HYPOTHESIS:\n\n1970s",
#     shape="box",
#     color="#f5f5f5",
#     size=30,
#     x=700, y=300,
#     font={
#         "size": 14,
#         "color": "black",
#         "face": "Arial"
#     },
#     fixed=True,
#     physics=False
# )
net.write_html(filename)

print("Graph saved as:", filename)
webbrowser.open("file://" + os.path.realpath(filename))