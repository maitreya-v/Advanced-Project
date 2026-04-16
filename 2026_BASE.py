from pyvis.network import Network
import webbrowser
import os

net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")

# -----------------------------
# NODE POSITIONS (original + new)
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

    # School/Work
    "Teacher Referral Rate": (-100, -420),
    "Classroom Size": (100, -500),
    "Academic Demands": (300, -500),
    "School Resources": (300, -380),
    "Workplace Accommodations": (500, -200),

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

    # New
    "Neurodevelopmental Risk": (-50, 100),

    "Prenatal Stress": (-750, -50),
    "Maternal Nutrition": (-750, -150),
    "Prenatal Substance Exposure": (-750, 50),
    "Birth Complications": (-750, 150),

    "Diet Quality": (-700, -350),
    "Micronutrient Deficiency": (-550, -350),
    "Ultra-Processed Food Intake": (-850, -350),
    "Blood Sugar Instability": (-700, -450),

    "Lead Exposure": (850, -50),
    "Air Pollution": (850, 50),
    "Environmental Toxins": (850, 150),

    "Sleep Quality": (-150, -550),
    "Physical Activity": (0, -600),
    "Screen Time": (150, -550),
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
# ALL EDGES WITH TOOLTIPS + STRENGTH
# Format:
# (source, target, sign, strength, explanation)
# -----------------------------
edges_2026 = [

    # Core ADHD and symptoms
    ("Genetic Risk", "ADHD", "+", 0.92, "Strong inherited contribution to ADHD liability"),
    ("ADHD", "Symptom Severity", "+", 0.96, "ADHD directly increases the severity of core symptoms"),
    ("ADHD", "Symptom Type", "+", 0.91, "ADHD influences whether symptoms appear as inattentive, hyperactive, or combined"),
    ("ADHD", "Comorbid Conditions", "+", 0.72, "ADHD commonly co-occurs with other psychiatric or developmental conditions"),
    ("ADHD", "Functional Impairment", "+", 0.93, "ADHD contributes strongly to impairment in school, work, and daily functioning"),
    ("ADHD", "Quality of Life", "-", 0.80, "ADHD symptoms and impairment can reduce overall quality of life"),
    ("ADHD", "Misdiagnosis Rate", "-", 0.35, "Clearer ADHD presentation can sometimes reduce misdiagnosis by making the disorder easier to identify"),

    # Age
    ("Age", "Symptom Severity", "-", 0.38, "Some symptoms may become less overt or differently expressed with age"),
    ("Age", "Diagnosis Status", "+", 0.52, "Older age can increase the chance that symptoms are eventually recognized"),
    ("Diagnosis Status", "Age at Diagnosis", "-", 1.00, "Earlier diagnosis directly lowers age at diagnosis by definition"),

    # Gender
    ("Gender", "Diagnosis Status", "+", 0.48, "Gender still influences who gets identified and diagnosed"),
    ("Gender", "Symptom Type", "+", 0.44, "Gender can shape which symptom profiles are more visible or emphasized"),

    # Symptoms -> referral -> diagnosis
    ("Symptom Severity", "Diagnosis Status", "+", 0.85, "More severe symptoms make diagnosis more likely"),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.77, "More disruptive or visible symptom types increase school referral"),
    ("Teacher Referral Rate", "Diagnosis Status", "+", 0.82, "Teacher concerns often lead to evaluation and diagnosis"),

    # Family
    ("Parental Awareness", "Diagnosis Status", "+", 0.83, "Parents who recognize symptoms are more likely to seek help"),
    ("Parenting Style", "Symptom Severity", "-", 0.32, "Supportive structure can reduce symptom expression, though not the core condition"),
    ("Family Stress", "Symptom Severity", "+", 0.60, "Stress in the family can worsen symptom expression"),
    ("Family Stress", "Comorbid Conditions", "+", 0.54, "Family stress can contribute to anxiety, mood, or behavioral difficulties"),
    ("Household Stability", "Family Stress", "-", 0.75, "Greater household stability tends to reduce family stress"),

    # School / work context
    ("Classroom Size", "Teacher Referral Rate", "+", 0.40, "Larger classrooms can make attention and behavior difficulties harder to manage"),
    ("Academic Demands", "Functional Impairment", "+", 0.70, "Higher academic demands increase the impact of executive dysfunction"),
    ("Functional Impairment", "Diagnosis Status", "+", 0.76, "Visible impairment pushes families, schools, or clinicians toward diagnosis"),
    ("School Resources", "Diagnosis Status", "+", 0.60, "Better school support systems can help students get identified and assessed"),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.58, "Accommodations can reduce adult functional impairment"),

    # Healthcare
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.88, "Better access makes assessment and diagnosis more likely"),
    ("Provider Availability", "Diagnosis Status", "+", 0.78, "More providers increase the likelihood of timely assessment"),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.62, "Longer waiting times delay or reduce completed diagnoses"),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.74, "High evaluation cost creates a financial barrier to diagnosis"),
    ("Diagnostic Criteria Variability", "Diagnosis Status", "+", 0.45, "Broader or flexible interpretation of criteria can increase diagnosis rates"),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.84, "Inconsistent interpretation of criteria raises misdiagnosis risk"),

    # Social context
    ("Stigma", "Parental Awareness", "-", 0.66, "Stigma can discourage parents from noticing or acting on symptoms"),
    ("Stigma", "Diagnosis Status", "-", 0.72, "Stigma reduces willingness to pursue or accept diagnosis"),
    ("Gender Bias", "Diagnosis Status", "+", 0.63, "Bias can increase diagnosis in stereotyped groups while reducing it in others"),
    ("Cultural Norms", "Stigma", "+", 0.74, "Cultural beliefs shape stigma around ADHD and mental health"),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.84, "Higher socioeconomic status improves access to specialists and care"),
    ("Socioeconomic Status", "Parental Awareness", "+", 0.56, "More resources often increase access to information and advocacy"),
    ("Socioeconomic Status", "Cost of Evaluation", "-", 0.79, "Higher socioeconomic status reduces the effective burden of evaluation cost"),

    # Outcomes
    ("Comorbid Conditions", "Functional Impairment", "+", 0.75, "Comorbid conditions often increase total impairment burden"),
    ("Diagnosis Status", "Functional Impairment", "-", 0.56, "Diagnosis can reduce impairment through treatment and accommodations"),
    ("Functional Impairment", "Quality of Life", "-", 0.89, "Greater impairment strongly lowers quality of life"),
    ("Diagnosis Status", "Quality of Life", "+", 0.52, "Diagnosis may improve quality of life through support and treatment access"),

    # Prenatal / neurodevelopment
    ("Prenatal Stress", "Neurodevelopmental Risk", "+", 0.50, "Maternal stress can affect fetal neurodevelopment"),
    ("Maternal Nutrition", "Neurodevelopmental Risk", "-", 0.42, "Better maternal nutrition supports healthy brain development"),
    ("Prenatal Substance Exposure", "Neurodevelopmental Risk", "+", 0.78, "Prenatal alcohol or smoking exposure can impair neural development"),
    ("Birth Complications", "Neurodevelopmental Risk", "+", 0.58, "Birth complications can increase developmental vulnerability"),
    ("Neurodevelopmental Risk", "ADHD", "+", 0.86, "Higher neurodevelopmental vulnerability increases ADHD likelihood"),

    # Nutrition
    ("Diet Quality", "Micronutrient Deficiency", "-", 0.81, "Better diet quality lowers the chance of micronutrient deficiency"),
    ("Micronutrient Deficiency", "Symptom Severity", "+", 0.46, "Deficiencies may worsen attention, mood, or self-regulation"),
    ("Ultra-Processed Food Intake", "Diet Quality", "-", 0.83, "High ultra-processed food intake tends to reduce overall diet quality"),
    ("Ultra-Processed Food Intake", "Blood Sugar Instability", "+", 0.72, "High sugar and refined foods can increase glucose instability"),
    ("Blood Sugar Instability", "Symptom Severity", "+", 0.34, "Energy swings may worsen attention and behavioral regulation"),

    # Environment
    ("Lead Exposure", "Neurodevelopmental Risk", "+", 0.72, "Lead exposure harms cognitive and neurodevelopmental functioning"),
    ("Air Pollution", "Neurodevelopmental Risk", "+", 0.48, "Air pollution is associated with inflammatory and developmental risk"),
    ("Environmental Toxins", "Neurodevelopmental Risk", "+", 0.58, "Toxin exposure can disrupt developing neural systems"),

    # Lifestyle
    ("Sleep Quality", "Symptom Severity", "-", 0.68, "Better sleep improves attention, regulation, and executive control"),
    ("Physical Activity", "Symptom Severity", "-", 0.50, "Physical activity can help reduce symptom burden"),
    ("Screen Time", "Symptom Severity", "+", 0.40, "Excessive screen time may worsen attention and self-regulation difficulties"),
    ("ADHD", "Sleep Quality", "-", 0.64, "ADHD often disrupts sleep routines and sleep quality"),
    ("ADHD", "Screen Time", "+", 0.42, "ADHD can increase impulsive or reward-seeking media use"),
]

for u, v, sign, strength, explanation in edges_2026:
    add_edge(u, v, sign, strength, explanation)

# -----------------------------
# FINALIZE
# -----------------------------
net.toggle_physics(False)

filename = "2026.html"
net.write_html(filename)

print("Saved:", filename)
webbrowser.open("file://" + os.path.realpath(filename))