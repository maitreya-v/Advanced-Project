from pyvis.network import Network
import webbrowser
import os

net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")

# -----------------------------
# NODE POSITIONS
# -----------------------------
node_positions = {

    "ADHD": (0, 0),
    "Diagnosis Status": (0, 350),

    # Individual
    "Age": (-500, -200),
    "Gender": (-380, -200),
    "Genetic Risk": (-300, -80),
    "Symptom Severity": (-200, -200),
    "Symptom Type": (-200, -80),
    "Comorbid Conditions": (-100, -300),

    # Family
    "Parental Awareness": (-500, 200),
    "Parenting Style": (-500, 80),
    "Family Stress": (-380, 130),
    "Household Stability": (-500, 320),

    # School
    "Teacher Referral Rate": (-100, -420),
    "Classroom Size": (100, -500),
    "Academic Demands": (300, -500),
    "School Resources": (300, -380),

    # Healthcare
    "Access to Mental Health Care": (500, 200),
    "Provider Availability": (650, 80),
    "Diagnostic Criteria Variability": (300, 420),
    "Waiting Time for Assessment": (500, 350),
    "Cost of Evaluation": (500, 480),

    # Social
    "Stigma": (400, -300),
    "Gender Bias": (200, -300),
    "Cultural Norms": (550, -380),
    "Socioeconomic Status": (650, -80),

    # Outcomes
    "Age at Diagnosis": (0, 500),
    "Misdiagnosis Rate": (200, 480),
    "Functional Impairment": (-300, 300),
    "Quality of Life": (-500, 450),

    # Environmental / early-life factors
    "Lead Exposure": (850, -50),
    "Prenatal Stress": (-750, -50),
    "Maternal Nutrition": (-750, -150),
    "Prenatal Substance Exposure": (-750, 50),
    "Birth Complications": (-750, 150),
}

# -----------------------------
# ADD NODES
# -----------------------------
for node, (x, y) in node_positions.items():

    if node == "ADHD":
        color = "#1f77b4"
        size = 45
    elif node == "Diagnosis Status":
        color = "#ff7f0e"
        size = 45
    else:
        color = "#dddddd"
        size = 25

    net.add_node(
        node,
        label=node,
        x=x,
        y=y,
        fixed=True,
        physics=False,
        color=color,
        size=size,
        font={"size": 13}
    )

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
# 1990s CONTEXT EDGES
# Format:
# (source, target, sign, strength, explanation)
# -----------------------------
edges_1990 = [

    # Core etiology / early risk
    ("Genetic Risk", "ADHD", "+", 0.90, "Strong inherited contribution to ADHD risk"),
    ("Prenatal Stress", "ADHD", "+", 0.45, "Maternal stress may affect early child neurobehavioral development"),
    ("Maternal Nutrition", "ADHD", "-", 0.35, "Better maternal nutrition may reduce developmental vulnerability"),
    ("Prenatal Substance Exposure", "ADHD", "+", 0.70, "Prenatal smoking or alcohol exposure can increase developmental risk"),
    ("Birth Complications", "ADHD", "+", 0.50, "Birth complications may contribute to later attention or behavioral problems"),
    ("Lead Exposure", "ADHD", "+", 0.65, "Lead exposure was an important environmental developmental risk factor"),

    # ADHD effects
    ("ADHD", "Symptom Severity", "+", 0.95, "ADHD directly increases severity of attention and behavioral symptoms"),
    ("ADHD", "Symptom Type", "+", 0.90, "ADHD influences whether symptoms appear as inattentive, hyperactive, or mixed"),
    ("ADHD", "Comorbid Conditions", "+", 0.70, "ADHD often co-occurs with other behavioral or emotional conditions"),
    ("ADHD", "Functional Impairment", "+", 0.92, "ADHD contributes to impairment in academic and daily functioning"),
    ("ADHD", "Quality of Life", "-", 0.78, "ADHD can reduce quality of life through impairment and stress"),

    # Age and timing
    ("Age", "Symptom Severity", "-", 0.35, "Some symptoms may appear less intense or differently expressed with age"),
    ("Age", "Diagnosis Status", "+", 0.50, "Older children had more time to be noticed and evaluated"),
    ("Diagnosis Status", "Age at Diagnosis", "-", 1.00, "Being diagnosed earlier lowers age at diagnosis by definition"),

    # Gender and bias
    ("Gender", "Diagnosis Status", "+", 0.55, "Boys were more likely to be diagnosed in the 1990s context"),
    ("Gender", "Symptom Type", "+", 0.45, "Gender influenced which symptom patterns were more likely to be noticed"),
    ("Gender Bias", "Teacher Referral Rate", "+", 0.72, "Boys fitting the dominant ADHD stereotype were more likely to be referred"),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.62, "Bias increased under-recognition in some groups and over-recognition in others"),

    # Symptoms to school referral to diagnosis
    ("Symptom Severity", "Diagnosis Status", "+", 0.82, "More severe symptoms increased likelihood of evaluation and diagnosis"),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.78, "Disruptive or visible symptom patterns increased school referral"),
    ("Teacher Referral Rate", "Diagnosis Status", "+", 0.88, "Teacher concern was a major pathway into evaluation in the 1990s"),

    # Family influences
    ("Parental Awareness", "Teacher Referral Rate", "+", 0.52, "Aware parents were more likely to respond to school concerns and pursue referrals"),
    ("Parental Awareness", "Diagnosis Status", "+", 0.80, "Parents who recognized symptoms were more likely to seek assessment"),
    ("Parenting Style", "Symptom Severity", "-", 0.30, "Supportive structure could reduce behavioral expression, though it does not remove ADHD"),
    ("Family Stress", "Symptom Severity", "+", 0.58, "Stressful home environments could worsen symptom expression"),
    ("Family Stress", "Comorbid Conditions", "+", 0.50, "Family stress can contribute to emotional and behavioral co-occurring issues"),
    ("Household Stability", "Family Stress", "-", 0.72, "More stable homes tend to reduce overall family stress"),

    # School context
    ("Classroom Size", "Teacher Referral Rate", "+", 0.40, "Larger classrooms could make disruptive behavior stand out more or become harder to manage"),
    ("Academic Demands", "Functional Impairment", "+", 0.68, "Higher academic demands made ADHD-related difficulties more visible"),
    ("School Resources", "Teacher Referral Rate", "+", 0.45, "Schools with more support systems could identify and refer students more effectively"),
    ("School Resources", "Diagnosis Status", "+", 0.55, "Better school resources supported the path from concern to formal diagnosis"),

    # Healthcare access
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.85, "Better access made formal diagnosis more likely"),
    ("Provider Availability", "Diagnosis Status", "+", 0.75, "More available providers increased chances of assessment"),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.60, "Long waits reduced or delayed completed diagnosis"),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.70, "Higher costs created a barrier to evaluation"),

    # Diagnostic inconsistency in 1990s
    ("Diagnostic Criteria Variability", "Diagnosis Status", "-", 0.58, "Inconsistent interpretation of criteria reduced diagnostic consistency"),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.82, "More variability in criteria interpretation increased misdiagnosis risk"),

    # Social context
    ("Stigma", "Parental Awareness", "-", 0.65, "Stigma discouraged parents from recognizing or acting on symptoms"),
    ("Stigma", "Teacher Referral Rate", "-", 0.42, "Stigma could reduce referrals by normalizing or dismissing concerns"),
    ("Stigma", "Diagnosis Status", "-", 0.70, "Stigma reduced willingness to pursue or accept diagnosis"),
    ("Cultural Norms", "Stigma", "+", 0.72, "Cultural expectations shaped stigma around child behavior and mental health labels"),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.82, "Higher socioeconomic status improved access to specialists and services"),
    ("Socioeconomic Status", "Parental Awareness", "+", 0.52, "Families with more resources often had more exposure to information and advocacy"),
    ("Socioeconomic Status", "Cost of Evaluation", "-", 0.76, "Higher socioeconomic status reduced the effective burden of evaluation cost"),

    # Outcomes
    ("Comorbid Conditions", "Functional Impairment", "+", 0.73, "Additional conditions often increased overall impairment"),
    ("Functional Impairment", "Diagnosis Status", "+", 0.72, "Visible impairment pushed families and schools toward diagnosis"),
    ("Diagnosis Status", "Functional Impairment", "-", 0.50, "Diagnosis could reduce impairment through treatment or support"),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Greater impairment strongly reduced quality of life"),
    ("Diagnosis Status", "Quality of Life", "+", 0.48, "Diagnosis could improve quality of life through recognition and intervention"),
]

for u, v, sign, strength, explanation in edges_1990:
    add_edge(u, v, sign, strength, explanation)

# -----------------------------
# FINALIZE
# -----------------------------
net.toggle_physics(False)

filename = "1990.html"
net.write_html(filename)

print("Saved:", filename)
webbrowser.open("file://" + os.path.realpath(filename))