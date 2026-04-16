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

    # School / work
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

    # Neurodevelopment / early-life factors
    "Neurodevelopmental Risk": (-50, 100),
    "Prenatal Stress": (-750, -50),
    "Maternal Nutrition": (-750, -150),
    "Prenatal Substance Exposure": (-750, 50),
    "Birth Complications": (-750, 150),
    "Lead Exposure": (850, -50),

    # Diet / environment / lifestyle
    "Diet Quality": (-700, -350),
    "Micronutrient Deficiency": (-550, -350),
    "Ultra-Processed Food Intake": (-850, -350),
    "Blood Sugar Instability": (-700, -450),
    "Air Pollution": (850, 50),
    "Environmental Toxins": (850, 150),
    "Sleep Quality": (-150, -550),
    "Physical Activity": (0, -600),
    "Screen Time": (150, -550),

    # New for 2010s context
    "Online Health Information": (760, 280),
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
# 2010s CONTEXT EDGES
# Format:
# (source, target, sign, strength, explanation)
# -----------------------------
edges_2010 = [

    # Core ADHD and symptoms
    ("Genetic Risk", "ADHD", "+", 0.91, "Strong inherited contribution to ADHD liability remained well established"),
    ("ADHD", "Symptom Severity", "+", 0.95, "ADHD directly increases the severity of core symptoms"),
    ("ADHD", "Symptom Type", "+", 0.91, "ADHD shapes whether symptoms present as inattentive, hyperactive, or combined"),
    ("ADHD", "Comorbid Conditions", "+", 0.71, "ADHD commonly co-occurred with anxiety, learning, or behavioral conditions"),
    ("ADHD", "Functional Impairment", "+", 0.92, "ADHD strongly affects school, work, and everyday functioning"),
    ("ADHD", "Quality of Life", "-", 0.79, "ADHD symptoms and impairment can reduce overall quality of life"),
    ("ADHD", "Misdiagnosis Rate", "-", 0.28, "Clearer symptom presentation can sometimes reduce misdiagnosis, though not eliminate it"),

    # Age and timing
    ("Age", "Symptom Severity", "-", 0.36, "Some overt hyperactive symptoms may become less visible with age"),
    ("Age", "Diagnosis Status", "+", 0.56, "By the 2010s, recognition increasingly extended beyond very young children"),
    ("Diagnosis Status", "Age at Diagnosis", "-", 1.00, "Earlier diagnosis directly lowers age at diagnosis by definition"),

    # Gender and bias
    ("Gender", "Diagnosis Status", "+", 0.40, "Gender still influenced diagnosis, but less rigidly than in earlier decades"),
    ("Gender", "Symptom Type", "+", 0.42, "Gender affected which symptom patterns were more likely to be noticed"),
    ("Gender Bias", "Teacher Referral Rate", "+", 0.58, "Visible disruptive behavior still fit older stereotypes and shaped referrals"),
    ("Gender Bias", "Misdiagnosis Rate", "+", 0.66, "Bias continued to contribute to over- and under-recognition across groups"),

    # Symptoms -> referral -> diagnosis
    ("Symptom Severity", "Diagnosis Status", "+", 0.84, "More severe symptoms were more likely to lead to assessment"),
    ("Symptom Type", "Teacher Referral Rate", "+", 0.75, "Disruptive or externalizing symptom patterns increased school referral"),
    ("Teacher Referral Rate", "Diagnosis Status", "+", 0.80, "Teacher concern remained a major path to evaluation during the 2010s"),

    # Family influences
    ("Parental Awareness", "Teacher Referral Rate", "+", 0.48, "More aware parents were better able to engage with school concerns"),
    ("Parental Awareness", "Diagnosis Status", "+", 0.82, "Parents who recognized symptoms were more likely to seek evaluation"),
    ("Parenting Style", "Symptom Severity", "-", 0.30, "Supportive structure could reduce behavioral expression without removing ADHD"),
    ("Family Stress", "Symptom Severity", "+", 0.59, "Family stress could worsen attention, regulation, and behavior"),
    ("Family Stress", "Comorbid Conditions", "+", 0.52, "Stressful environments can contribute to co-occurring emotional difficulties"),
    ("Household Stability", "Family Stress", "-", 0.74, "Greater household stability tends to reduce family stress"),

    # School / work context
    ("Classroom Size", "Teacher Referral Rate", "+", 0.39, "Larger classrooms could make attention and behavior issues harder to manage"),
    ("Academic Demands", "Functional Impairment", "+", 0.69, "Rising academic demands made executive dysfunction more visible"),
    ("School Resources", "Teacher Referral Rate", "+", 0.46, "Better school resources supported identification and referral"),
    ("School Resources", "Diagnosis Status", "+", 0.58, "Schools with more support systems could better connect students to evaluation"),
    ("Functional Impairment", "Diagnosis Status", "+", 0.75, "Visible impairment pushed families, schools, or clinicians toward diagnosis"),
    ("Workplace Accommodations", "Functional Impairment", "-", 0.42, "Adult accommodations existed in the 2010s but were less common and less normalized than later"),

    # Healthcare access and diagnostic practice
    ("Access to Mental Health Care", "Diagnosis Status", "+", 0.87, "Access to care strongly affected whether formal diagnosis occurred"),
    ("Provider Availability", "Diagnosis Status", "+", 0.77, "More available providers improved chances of assessment"),
    ("Waiting Time for Assessment", "Diagnosis Status", "-", 0.60, "Long waits delayed or reduced completed diagnoses"),
    ("Cost of Evaluation", "Diagnosis Status", "-", 0.73, "Financial cost remained a substantial barrier to assessment"),
    ("Diagnostic Criteria Variability", "Diagnosis Status", "+", 0.32, "In the 2010s, broader recognition could increase diagnosis rates in some settings"),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+", 0.79, "Differences in interpretation still increased the risk of misdiagnosis"),

    # Social context
    ("Stigma", "Parental Awareness", "-", 0.56, "Stigma still discouraged recognition or help-seeking, though somewhat less than in the 1990s"),
    ("Stigma", "Teacher Referral Rate", "-", 0.28, "Stigma could still suppress referrals or normalize persistent problems"),
    ("Stigma", "Diagnosis Status", "-", 0.60, "Stigma continued to reduce willingness to seek or accept diagnosis"),
    ("Cultural Norms", "Stigma", "+", 0.70, "Cultural beliefs shaped how ADHD and mental health labels were viewed"),
    ("Socioeconomic Status", "Access to Mental Health Care", "+", 0.83, "Higher socioeconomic status improved access to specialists and services"),
    ("Socioeconomic Status", "Parental Awareness", "+", 0.55, "Families with more resources often had more exposure to information and advocacy"),
    ("Socioeconomic Status", "Cost of Evaluation", "-", 0.78, "Higher socioeconomic status reduced the effective burden of evaluation cost"),

    # Online information became important in the 2010s
    ("Online Health Information", "Parental Awareness", "+", 0.74, "Internet access increased public exposure to ADHD information and symptoms"),
    ("Online Health Information", "Diagnosis Status", "+", 0.50, "Online information sometimes pushed families or adults to pursue evaluation"),
    ("Online Health Information", "Stigma", "-", 0.34, "Greater visibility and discussion online could reduce stigma for some people"),

    # Outcomes
    ("Comorbid Conditions", "Functional Impairment", "+", 0.74, "Co-occurring conditions often increased total impairment burden"),
    ("Diagnosis Status", "Functional Impairment", "-", 0.54, "Diagnosis could reduce impairment through treatment, support, and accommodations"),
    ("Functional Impairment", "Quality of Life", "-", 0.88, "Greater impairment strongly lowered quality of life"),
    ("Diagnosis Status", "Quality of Life", "+", 0.50, "Diagnosis could improve quality of life through support and treatment access"),

    # Prenatal / neurodevelopment
    ("Prenatal Stress", "Neurodevelopmental Risk", "+", 0.48, "Maternal stress was increasingly discussed as a developmental risk factor"),
    ("Maternal Nutrition", "Neurodevelopmental Risk", "-", 0.38, "Better maternal nutrition supports healthier early development"),
    ("Prenatal Substance Exposure", "Neurodevelopmental Risk", "+", 0.75, "Prenatal smoking or alcohol exposure increased developmental vulnerability"),
    ("Birth Complications", "Neurodevelopmental Risk", "+", 0.56, "Birth complications could increase risk of later developmental difficulties"),
    ("Lead Exposure", "Neurodevelopmental Risk", "+", 0.70, "Lead exposure remained an important environmental neurodevelopmental risk"),
    ("Air Pollution", "Neurodevelopmental Risk", "+", 0.38, "Air pollution was increasingly discussed as a possible developmental risk factor in the 2010s"),
    ("Environmental Toxins", "Neurodevelopmental Risk", "+", 0.48, "Broader toxin exposure remained relevant in neurodevelopmental risk discussions"),
    ("Neurodevelopmental Risk", "ADHD", "+", 0.84, "Higher developmental vulnerability increased the likelihood of ADHD"),

    # Diet / nutrition
    ("Diet Quality", "Micronutrient Deficiency", "-", 0.72, "Better overall diet quality lowers the chance of micronutrient deficiency"),
    ("Micronutrient Deficiency", "Symptom Severity", "+", 0.34, "Deficiencies were discussed as possibly worsening attention or behavioral regulation"),
    ("Ultra-Processed Food Intake", "Diet Quality", "-", 0.55, "Higher processed food intake generally reflected lower diet quality, though the framing was less central than in 2026"),
    ("Ultra-Processed Food Intake", "Blood Sugar Instability", "+", 0.36, "Highly refined foods could contribute to energy fluctuations, but this link was more tentative"),
    ("Blood Sugar Instability", "Symptom Severity", "+", 0.20, "Possible short-term attention or regulation effects were discussed, though evidence was less central and more contested"),

    # Lifestyle factors that became more salient in the 2010s
    ("Sleep Quality", "Symptom Severity", "-", 0.62, "Better sleep improved attention, regulation, and executive control"),
    ("Physical Activity", "Symptom Severity", "-", 0.46, "Physical activity could help reduce symptom burden"),
    ("Screen Time", "Symptom Severity", "+", 0.38, "Higher screen exposure was increasingly discussed as worsening attention or self-regulation"),
    ("ADHD", "Sleep Quality", "-", 0.60, "ADHD often disrupted sleep routines and sleep quality"),
    ("ADHD", "Screen Time", "+", 0.36, "ADHD could increase impulsive or reward-seeking media use"),
]

for u, v, sign, strength, explanation in edges_2010:
    add_edge(u, v, sign, strength, explanation)

# -----------------------------
# FINALIZE
# -----------------------------
net.toggle_physics(False)

filename = "2010.html"
net.write_html(filename)

print("Saved:", filename)
webbrowser.open("file://" + os.path.realpath(filename))