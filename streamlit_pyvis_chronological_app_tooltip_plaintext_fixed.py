# Import Streamlit.
import streamlit as st
# Import the HTML component renderer for PyVis output.
import streamlit.components.v1 as components
# Import PyVis.
from pyvis.network import Network

# Set the page configuration.
st.set_page_config(page_title="Chronological Causal Graph Explorer", layout="wide")

# Store the exact snapshot data from the uploaded yearly graph files.
YEAR_DATA = {
    "1970": {
        "period_label": "1970s",
        "positions": {
            "ADHD": [
                0,
                0
            ],
            "Diagnosis Status": [
                0,
                350
            ],
            "Age": [
                -500,
                -200
            ],
            "Gender": [
                -380,
                -200
            ],
            "Genetic Risk": [
                -300,
                -80
            ],
            "Symptom Severity": [
                -200,
                -200
            ],
            "Symptom Type": [
                -200,
                -80
            ],
            "Comorbid Conditions": [
                -100,
                -300
            ],
            "Parental Awareness": [
                -500,
                200
            ],
            "Parenting Style": [
                -500,
                80
            ],
            "Family Stress": [
                -380,
                130
            ],
            "Household Stability": [
                -500,
                320
            ],
            "Teacher Referral Rate": [
                -100,
                -420
            ],
            "Classroom Size": [
                100,
                -500
            ],
            "Academic Demands": [
                300,
                -500
            ],
            "School Resources": [
                300,
                -380
            ],
            "Workplace Accommodations": [
                500,
                -200
            ],
            "Access to Mental Health Care": [
                500,
                200
            ],
            "Provider Availability": [
                650,
                80
            ],
            "Diagnostic Criteria Variability": [
                300,
                420
            ],
            "Waiting Time for Assessment": [
                500,
                350
            ],
            "Cost of Evaluation": [
                500,
                480
            ],
            "Stigma": [
                400,
                -300
            ],
            "Gender Bias": [
                200,
                -300
            ],
            "Cultural Norms": [
                550,
                -380
            ],
            "Socioeconomic Status": [
                650,
                -80
            ],
            "Age at Diagnosis": [
                0,
                500
            ],
            "Misdiagnosis Rate": [
                200,
                480
            ],
            "Functional Impairment": [
                -300,
                300
            ],
            "Quality of Life": [
                -500,
                450
            ]
        },
        "edges": [
            [
                "Genetic Risk",
                "ADHD",
                "+",
                0.9,
                "Genetic vulnerability strongly increases the likelihood of underlying ADHD."
            ],
            [
                "Comorbid Conditions",
                "ADHD",
                "+",
                0.45,
                "Co-occurring conditions can increase the chance that ADHD-related patterns are recognized or reinforced."
            ],
            [
                "ADHD",
                "Symptom Severity",
                "+",
                0.92,
                "Underlying ADHD directly increases the intensity of symptoms."
            ],
            [
                "ADHD",
                "Symptom Type",
                "+",
                0.88,
                "Underlying ADHD influences the type or presentation of symptoms."
            ],
            [
                "Age",
                "Symptom Severity",
                "+",
                0.4,
                "In this graph, age is assumed to increase the visible severity of symptoms."
            ],
            [
                "Gender",
                "Symptom Type",
                "+",
                0.42,
                "Gender can influence which kinds of symptoms are more likely to be noticed or expressed."
            ],
            [
                "Symptom Severity",
                "Functional Impairment",
                "+",
                0.86,
                "More severe symptoms tend to increase day-to-day impairment."
            ],
            [
                "Comorbid Conditions",
                "Functional Impairment",
                "+",
                0.7,
                "Additional conditions increase the overall functional burden."
            ],
            [
                "Functional Impairment",
                "Quality of Life",
                "-",
                0.88,
                "More impairment reduces overall quality of life."
            ],
            [
                "Symptom Severity",
                "Teacher Referral Rate",
                "+",
                0.8,
                "More severe symptoms make teacher referral more likely."
            ],
            [
                "Symptom Type",
                "Teacher Referral Rate",
                "+",
                0.76,
                "More noticeable symptom types increase teacher referral."
            ],
            [
                "Classroom Size",
                "Teacher Referral Rate",
                "+",
                0.38,
                "Larger classrooms may make attention and behavior issues harder to manage, increasing referrals."
            ],
            [
                "Academic Demands",
                "Teacher Referral Rate",
                "+",
                0.6,
                "Higher academic demands make difficulties more visible to teachers."
            ],
            [
                "School Resources",
                "Teacher Referral Rate",
                "+",
                0.5,
                "More school resources can increase identification and referral."
            ],
            [
                "Parenting Style",
                "Symptom Severity",
                "+",
                0.45,
                "Parenting style can worsen or amplify the visible severity of symptoms in this model."
            ],
            [
                "Family Stress",
                "Symptom Severity",
                "+",
                0.62,
                "Higher family stress can worsen symptom expression."
            ],
            [
                "Household Stability",
                "Family Stress",
                "-",
                0.74,
                "Greater household stability reduces family stress."
            ],
            [
                "Parental Awareness",
                "Diagnosis Status",
                "+",
                0.78,
                "More parental awareness increases the likelihood of diagnosis."
            ],
            [
                "Teacher Referral Rate",
                "Age at Diagnosis",
                "-",
                0.72,
                "Higher referral rates can lead to earlier diagnosis, lowering age at diagnosis."
            ],
            [
                "Access to Mental Health Care",
                "Age at Diagnosis",
                "-",
                0.82,
                "Better access to care can lead to earlier diagnosis."
            ],
            [
                "Provider Availability",
                "Waiting Time for Assessment",
                "-",
                0.76,
                "More providers reduce waiting time for assessment."
            ],
            [
                "Waiting Time for Assessment",
                "Age at Diagnosis",
                "+",
                0.84,
                "Longer waits delay diagnosis and increase age at diagnosis."
            ],
            [
                "Cost of Evaluation",
                "Age at Diagnosis",
                "+",
                0.7,
                "Higher cost can delay diagnosis and increase age at diagnosis."
            ],
            [
                "Age at Diagnosis",
                "Diagnosis Status",
                "+",
                0.55,
                "In this graph, reaching the point of diagnosis is linked to age at diagnosis."
            ],
            [
                "Diagnostic Criteria Variability",
                "Misdiagnosis Rate",
                "+",
                0.82,
                "More variability in criteria increases the chance of misdiagnosis."
            ],
            [
                "Misdiagnosis Rate",
                "Diagnosis Status",
                "-",
                0.78,
                "Higher misdiagnosis reduces accurate diagnosis status."
            ],
            [
                "Cultural Norms",
                "Stigma",
                "+",
                0.72,
                "Cultural norms can increase stigma around ADHD-related behaviors."
            ],
            [
                "Stigma",
                "Parental Awareness",
                "-",
                0.68,
                "More stigma can reduce parental recognition or acknowledgment."
            ],
            [
                "Gender Bias",
                "Teacher Referral Rate",
                "+",
                0.74,
                "Gender bias can increase referral for some groups based on stereotypes."
            ],
            [
                "Gender Bias",
                "Diagnosis Status",
                "+",
                0.6,
                "Gender bias can affect who is more likely to receive a diagnosis."
            ],
            [
                "Socioeconomic Status",
                "Access to Mental Health Care",
                "+",
                0.8,
                "Higher socioeconomic status improves access to mental health care."
            ],
            [
                "Socioeconomic Status",
                "Cost of Evaluation",
                "-",
                0.76,
                "Higher socioeconomic status reduces the effective burden of evaluation cost."
            ]
        ]
    },
    "1990": {
        "period_label": "1990s",
        "positions": {
            "ADHD": [
                0,
                0
            ],
            "Diagnosis Status": [
                0,
                350
            ],
            "Age": [
                -500,
                -200
            ],
            "Gender": [
                -380,
                -200
            ],
            "Genetic Risk": [
                -300,
                -80
            ],
            "Symptom Severity": [
                -200,
                -200
            ],
            "Symptom Type": [
                -200,
                -80
            ],
            "Comorbid Conditions": [
                -100,
                -300
            ],
            "Parental Awareness": [
                -500,
                200
            ],
            "Parenting Style": [
                -500,
                80
            ],
            "Family Stress": [
                -380,
                130
            ],
            "Household Stability": [
                -500,
                320
            ],
            "Teacher Referral Rate": [
                -100,
                -420
            ],
            "Classroom Size": [
                100,
                -500
            ],
            "Academic Demands": [
                300,
                -500
            ],
            "School Resources": [
                300,
                -380
            ],
            "Access to Mental Health Care": [
                500,
                200
            ],
            "Provider Availability": [
                650,
                80
            ],
            "Diagnostic Criteria Variability": [
                300,
                420
            ],
            "Waiting Time for Assessment": [
                500,
                350
            ],
            "Cost of Evaluation": [
                500,
                480
            ],
            "Stigma": [
                400,
                -300
            ],
            "Gender Bias": [
                200,
                -300
            ],
            "Cultural Norms": [
                550,
                -380
            ],
            "Socioeconomic Status": [
                650,
                -80
            ],
            "Age at Diagnosis": [
                0,
                500
            ],
            "Misdiagnosis Rate": [
                200,
                480
            ],
            "Functional Impairment": [
                -300,
                300
            ],
            "Quality of Life": [
                -500,
                450
            ],
            "Lead Exposure": [
                850,
                -50
            ],
            "Prenatal Stress": [
                -750,
                -50
            ],
            "Maternal Nutrition": [
                -750,
                -150
            ],
            "Prenatal Substance Exposure": [
                -750,
                50
            ],
            "Birth Complications": [
                -750,
                150
            ]
        },
        "edges": [
            [
                "Genetic Risk",
                "ADHD",
                "+",
                0.9,
                "Strong inherited contribution to ADHD risk"
            ],
            [
                "Prenatal Stress",
                "ADHD",
                "+",
                0.45,
                "Maternal stress may affect early child neurobehavioral development"
            ],
            [
                "Maternal Nutrition",
                "ADHD",
                "-",
                0.35,
                "Better maternal nutrition may reduce developmental vulnerability"
            ],
            [
                "Prenatal Substance Exposure",
                "ADHD",
                "+",
                0.7,
                "Prenatal smoking or alcohol exposure can increase developmental risk"
            ],
            [
                "Birth Complications",
                "ADHD",
                "+",
                0.5,
                "Birth complications may contribute to later attention or behavioral problems"
            ],
            [
                "Lead Exposure",
                "ADHD",
                "+",
                0.65,
                "Lead exposure was an important environmental developmental risk factor"
            ],
            [
                "ADHD",
                "Symptom Severity",
                "+",
                0.95,
                "ADHD directly increases severity of attention and behavioral symptoms"
            ],
            [
                "ADHD",
                "Symptom Type",
                "+",
                0.9,
                "ADHD influences whether symptoms appear as inattentive, hyperactive, or mixed"
            ],
            [
                "ADHD",
                "Comorbid Conditions",
                "+",
                0.7,
                "ADHD often co-occurs with other behavioral or emotional conditions"
            ],
            [
                "ADHD",
                "Functional Impairment",
                "+",
                0.92,
                "ADHD contributes to impairment in academic and daily functioning"
            ],
            [
                "ADHD",
                "Quality of Life",
                "-",
                0.78,
                "ADHD can reduce quality of life through impairment and stress"
            ],
            [
                "Age",
                "Symptom Severity",
                "-",
                0.35,
                "Some symptoms may appear less intense or differently expressed with age"
            ],
            [
                "Age",
                "Diagnosis Status",
                "+",
                0.5,
                "Older children had more time to be noticed and evaluated"
            ],
            [
                "Diagnosis Status",
                "Age at Diagnosis",
                "-",
                1.0,
                "Being diagnosed earlier lowers age at diagnosis by definition"
            ],
            [
                "Gender",
                "Diagnosis Status",
                "+",
                0.55,
                "Boys were more likely to be diagnosed in the 1990s context"
            ],
            [
                "Gender",
                "Symptom Type",
                "+",
                0.45,
                "Gender influenced which symptom patterns were more likely to be noticed"
            ],
            [
                "Gender Bias",
                "Teacher Referral Rate",
                "+",
                0.72,
                "Boys fitting the dominant ADHD stereotype were more likely to be referred"
            ],
            [
                "Gender Bias",
                "Misdiagnosis Rate",
                "+",
                0.62,
                "Bias increased under-recognition in some groups and over-recognition in others"
            ],
            [
                "Symptom Severity",
                "Diagnosis Status",
                "+",
                0.82,
                "More severe symptoms increased likelihood of evaluation and diagnosis"
            ],
            [
                "Symptom Type",
                "Teacher Referral Rate",
                "+",
                0.78,
                "Disruptive or visible symptom patterns increased school referral"
            ],
            [
                "Teacher Referral Rate",
                "Diagnosis Status",
                "+",
                0.88,
                "Teacher concern was a major pathway into evaluation in the 1990s"
            ],
            [
                "Parental Awareness",
                "Teacher Referral Rate",
                "+",
                0.52,
                "Aware parents were more likely to respond to school concerns and pursue referrals"
            ],
            [
                "Parental Awareness",
                "Diagnosis Status",
                "+",
                0.8,
                "Parents who recognized symptoms were more likely to seek assessment"
            ],
            [
                "Parenting Style",
                "Symptom Severity",
                "-",
                0.3,
                "Supportive structure could reduce behavioral expression, though it does not remove ADHD"
            ],
            [
                "Family Stress",
                "Symptom Severity",
                "+",
                0.58,
                "Stressful home environments could worsen symptom expression"
            ],
            [
                "Family Stress",
                "Comorbid Conditions",
                "+",
                0.5,
                "Family stress can contribute to emotional and behavioral co-occurring issues"
            ],
            [
                "Household Stability",
                "Family Stress",
                "-",
                0.72,
                "More stable homes tend to reduce overall family stress"
            ],
            [
                "Classroom Size",
                "Teacher Referral Rate",
                "+",
                0.4,
                "Larger classrooms could make disruptive behavior stand out more or become harder to manage"
            ],
            [
                "Academic Demands",
                "Functional Impairment",
                "+",
                0.68,
                "Higher academic demands made ADHD-related difficulties more visible"
            ],
            [
                "School Resources",
                "Teacher Referral Rate",
                "+",
                0.45,
                "Schools with more support systems could identify and refer students more effectively"
            ],
            [
                "School Resources",
                "Diagnosis Status",
                "+",
                0.55,
                "Better school resources supported the path from concern to formal diagnosis"
            ],
            [
                "Access to Mental Health Care",
                "Diagnosis Status",
                "+",
                0.85,
                "Better access made formal diagnosis more likely"
            ],
            [
                "Provider Availability",
                "Diagnosis Status",
                "+",
                0.75,
                "More available providers increased chances of assessment"
            ],
            [
                "Waiting Time for Assessment",
                "Diagnosis Status",
                "-",
                0.6,
                "Long waits reduced or delayed completed diagnosis"
            ],
            [
                "Cost of Evaluation",
                "Diagnosis Status",
                "-",
                0.7,
                "Higher costs created a barrier to evaluation"
            ],
            [
                "Diagnostic Criteria Variability",
                "Diagnosis Status",
                "-",
                0.58,
                "Inconsistent interpretation of criteria reduced diagnostic consistency"
            ],
            [
                "Diagnostic Criteria Variability",
                "Misdiagnosis Rate",
                "+",
                0.82,
                "More variability in criteria interpretation increased misdiagnosis risk"
            ],
            [
                "Stigma",
                "Parental Awareness",
                "-",
                0.65,
                "Stigma discouraged parents from recognizing or acting on symptoms"
            ],
            [
                "Stigma",
                "Teacher Referral Rate",
                "-",
                0.42,
                "Stigma could reduce referrals by normalizing or dismissing concerns"
            ],
            [
                "Stigma",
                "Diagnosis Status",
                "-",
                0.7,
                "Stigma reduced willingness to pursue or accept diagnosis"
            ],
            [
                "Cultural Norms",
                "Stigma",
                "+",
                0.72,
                "Cultural expectations shaped stigma around child behavior and mental health labels"
            ],
            [
                "Socioeconomic Status",
                "Access to Mental Health Care",
                "+",
                0.82,
                "Higher socioeconomic status improved access to specialists and services"
            ],
            [
                "Socioeconomic Status",
                "Parental Awareness",
                "+",
                0.52,
                "Families with more resources often had more exposure to information and advocacy"
            ],
            [
                "Socioeconomic Status",
                "Cost of Evaluation",
                "-",
                0.76,
                "Higher socioeconomic status reduced the effective burden of evaluation cost"
            ],
            [
                "Comorbid Conditions",
                "Functional Impairment",
                "+",
                0.73,
                "Additional conditions often increased overall impairment"
            ],
            [
                "Functional Impairment",
                "Diagnosis Status",
                "+",
                0.72,
                "Visible impairment pushed families and schools toward diagnosis"
            ],
            [
                "Diagnosis Status",
                "Functional Impairment",
                "-",
                0.5,
                "Diagnosis could reduce impairment through treatment or support"
            ],
            [
                "Functional Impairment",
                "Quality of Life",
                "-",
                0.88,
                "Greater impairment strongly reduced quality of life"
            ],
            [
                "Diagnosis Status",
                "Quality of Life",
                "+",
                0.48,
                "Diagnosis could improve quality of life through recognition and intervention"
            ]
        ]
    },
    "2010": {
        "period_label": "2010s",
        "positions": {
            "ADHD": [
                0,
                0
            ],
            "Diagnosis Status": [
                0,
                350
            ],
            "Age": [
                -500,
                -200
            ],
            "Gender": [
                -380,
                -200
            ],
            "Genetic Risk": [
                -300,
                -80
            ],
            "Symptom Severity": [
                -200,
                -200
            ],
            "Symptom Type": [
                -200,
                -80
            ],
            "Comorbid Conditions": [
                -100,
                -300
            ],
            "Parental Awareness": [
                -500,
                200
            ],
            "Parenting Style": [
                -500,
                80
            ],
            "Family Stress": [
                -380,
                130
            ],
            "Household Stability": [
                -500,
                320
            ],
            "Teacher Referral Rate": [
                -100,
                -420
            ],
            "Classroom Size": [
                100,
                -500
            ],
            "Academic Demands": [
                300,
                -500
            ],
            "School Resources": [
                300,
                -380
            ],
            "Workplace Accommodations": [
                500,
                -200
            ],
            "Access to Mental Health Care": [
                500,
                200
            ],
            "Provider Availability": [
                650,
                80
            ],
            "Diagnostic Criteria Variability": [
                300,
                420
            ],
            "Waiting Time for Assessment": [
                500,
                350
            ],
            "Cost of Evaluation": [
                500,
                480
            ],
            "Stigma": [
                400,
                -300
            ],
            "Gender Bias": [
                200,
                -300
            ],
            "Cultural Norms": [
                550,
                -380
            ],
            "Socioeconomic Status": [
                650,
                -80
            ],
            "Age at Diagnosis": [
                0,
                500
            ],
            "Misdiagnosis Rate": [
                200,
                480
            ],
            "Functional Impairment": [
                -300,
                300
            ],
            "Quality of Life": [
                -500,
                450
            ],
            "Neurodevelopmental Risk": [
                -50,
                100
            ],
            "Prenatal Stress": [
                -750,
                -50
            ],
            "Maternal Nutrition": [
                -750,
                -150
            ],
            "Prenatal Substance Exposure": [
                -750,
                50
            ],
            "Birth Complications": [
                -750,
                150
            ],
            "Lead Exposure": [
                850,
                -50
            ],
            "Diet Quality": [
                -700,
                -350
            ],
            "Micronutrient Deficiency": [
                -550,
                -350
            ],
            "Ultra-Processed Food Intake": [
                -850,
                -350
            ],
            "Blood Sugar Instability": [
                -700,
                -450
            ],
            "Air Pollution": [
                850,
                50
            ],
            "Environmental Toxins": [
                850,
                150
            ],
            "Sleep Quality": [
                -150,
                -550
            ],
            "Physical Activity": [
                0,
                -600
            ],
            "Screen Time": [
                150,
                -550
            ],
            "Online Health Information": [
                760,
                280
            ]
        },
        "edges": [
            [
                "Genetic Risk",
                "ADHD",
                "+",
                0.91,
                "Strong inherited contribution to ADHD liability remained well established"
            ],
            [
                "ADHD",
                "Symptom Severity",
                "+",
                0.95,
                "ADHD directly increases the severity of core symptoms"
            ],
            [
                "ADHD",
                "Symptom Type",
                "+",
                0.91,
                "ADHD shapes whether symptoms present as inattentive, hyperactive, or combined"
            ],
            [
                "ADHD",
                "Comorbid Conditions",
                "+",
                0.71,
                "ADHD commonly co-occurred with anxiety, learning, or behavioral conditions"
            ],
            [
                "ADHD",
                "Functional Impairment",
                "+",
                0.92,
                "ADHD strongly affects school, work, and everyday functioning"
            ],
            [
                "ADHD",
                "Quality of Life",
                "-",
                0.79,
                "ADHD symptoms and impairment can reduce overall quality of life"
            ],
            [
                "ADHD",
                "Misdiagnosis Rate",
                "-",
                0.28,
                "Clearer symptom presentation can sometimes reduce misdiagnosis, though not eliminate it"
            ],
            [
                "Age",
                "Symptom Severity",
                "-",
                0.36,
                "Some overt hyperactive symptoms may become less visible with age"
            ],
            [
                "Age",
                "Diagnosis Status",
                "+",
                0.56,
                "By the 2010s, recognition increasingly extended beyond very young children"
            ],
            [
                "Diagnosis Status",
                "Age at Diagnosis",
                "-",
                1.0,
                "Earlier diagnosis directly lowers age at diagnosis by definition"
            ],
            [
                "Gender",
                "Diagnosis Status",
                "+",
                0.4,
                "Gender still influenced diagnosis, but less rigidly than in earlier decades"
            ],
            [
                "Gender",
                "Symptom Type",
                "+",
                0.42,
                "Gender affected which symptom patterns were more likely to be noticed"
            ],
            [
                "Gender Bias",
                "Teacher Referral Rate",
                "+",
                0.58,
                "Visible disruptive behavior still fit older stereotypes and shaped referrals"
            ],
            [
                "Gender Bias",
                "Misdiagnosis Rate",
                "+",
                0.66,
                "Bias continued to contribute to over- and under-recognition across groups"
            ],
            [
                "Symptom Severity",
                "Diagnosis Status",
                "+",
                0.84,
                "More severe symptoms were more likely to lead to assessment"
            ],
            [
                "Symptom Type",
                "Teacher Referral Rate",
                "+",
                0.75,
                "Disruptive or externalizing symptom patterns increased school referral"
            ],
            [
                "Teacher Referral Rate",
                "Diagnosis Status",
                "+",
                0.8,
                "Teacher concern remained a major path to evaluation during the 2010s"
            ],
            [
                "Parental Awareness",
                "Teacher Referral Rate",
                "+",
                0.48,
                "More aware parents were better able to engage with school concerns"
            ],
            [
                "Parental Awareness",
                "Diagnosis Status",
                "+",
                0.82,
                "Parents who recognized symptoms were more likely to seek evaluation"
            ],
            [
                "Parenting Style",
                "Symptom Severity",
                "-",
                0.3,
                "Supportive structure could reduce behavioral expression without removing ADHD"
            ],
            [
                "Family Stress",
                "Symptom Severity",
                "+",
                0.59,
                "Family stress could worsen attention, regulation, and behavior"
            ],
            [
                "Family Stress",
                "Comorbid Conditions",
                "+",
                0.52,
                "Stressful environments can contribute to co-occurring emotional difficulties"
            ],
            [
                "Household Stability",
                "Family Stress",
                "-",
                0.74,
                "Greater household stability tends to reduce family stress"
            ],
            [
                "Classroom Size",
                "Teacher Referral Rate",
                "+",
                0.39,
                "Larger classrooms could make attention and behavior issues harder to manage"
            ],
            [
                "Academic Demands",
                "Functional Impairment",
                "+",
                0.69,
                "Rising academic demands made executive dysfunction more visible"
            ],
            [
                "School Resources",
                "Teacher Referral Rate",
                "+",
                0.46,
                "Better school resources supported identification and referral"
            ],
            [
                "School Resources",
                "Diagnosis Status",
                "+",
                0.58,
                "Schools with more support systems could better connect students to evaluation"
            ],
            [
                "Functional Impairment",
                "Diagnosis Status",
                "+",
                0.75,
                "Visible impairment pushed families, schools, or clinicians toward diagnosis"
            ],
            [
                "Workplace Accommodations",
                "Functional Impairment",
                "-",
                0.42,
                "Adult accommodations existed in the 2010s but were less common and less normalized than later"
            ],
            [
                "Access to Mental Health Care",
                "Diagnosis Status",
                "+",
                0.87,
                "Access to care strongly affected whether formal diagnosis occurred"
            ],
            [
                "Provider Availability",
                "Diagnosis Status",
                "+",
                0.77,
                "More available providers improved chances of assessment"
            ],
            [
                "Waiting Time for Assessment",
                "Diagnosis Status",
                "-",
                0.6,
                "Long waits delayed or reduced completed diagnoses"
            ],
            [
                "Cost of Evaluation",
                "Diagnosis Status",
                "-",
                0.73,
                "Financial cost remained a substantial barrier to assessment"
            ],
            [
                "Diagnostic Criteria Variability",
                "Diagnosis Status",
                "+",
                0.32,
                "In the 2010s, broader recognition could increase diagnosis rates in some settings"
            ],
            [
                "Diagnostic Criteria Variability",
                "Misdiagnosis Rate",
                "+",
                0.79,
                "Differences in interpretation still increased the risk of misdiagnosis"
            ],
            [
                "Stigma",
                "Parental Awareness",
                "-",
                0.56,
                "Stigma still discouraged recognition or help-seeking, though somewhat less than in the 1990s"
            ],
            [
                "Stigma",
                "Teacher Referral Rate",
                "-",
                0.28,
                "Stigma could still suppress referrals or normalize persistent problems"
            ],
            [
                "Stigma",
                "Diagnosis Status",
                "-",
                0.6,
                "Stigma continued to reduce willingness to seek or accept diagnosis"
            ],
            [
                "Cultural Norms",
                "Stigma",
                "+",
                0.7,
                "Cultural beliefs shaped how ADHD and mental health labels were viewed"
            ],
            [
                "Socioeconomic Status",
                "Access to Mental Health Care",
                "+",
                0.83,
                "Higher socioeconomic status improved access to specialists and services"
            ],
            [
                "Socioeconomic Status",
                "Parental Awareness",
                "+",
                0.55,
                "Families with more resources often had more exposure to information and advocacy"
            ],
            [
                "Socioeconomic Status",
                "Cost of Evaluation",
                "-",
                0.78,
                "Higher socioeconomic status reduced the effective burden of evaluation cost"
            ],
            [
                "Online Health Information",
                "Parental Awareness",
                "+",
                0.74,
                "Internet access increased public exposure to ADHD information and symptoms"
            ],
            [
                "Online Health Information",
                "Diagnosis Status",
                "+",
                0.5,
                "Online information sometimes pushed families or adults to pursue evaluation"
            ],
            [
                "Online Health Information",
                "Stigma",
                "-",
                0.34,
                "Greater visibility and discussion online could reduce stigma for some people"
            ],
            [
                "Comorbid Conditions",
                "Functional Impairment",
                "+",
                0.74,
                "Co-occurring conditions often increased total impairment burden"
            ],
            [
                "Diagnosis Status",
                "Functional Impairment",
                "-",
                0.54,
                "Diagnosis could reduce impairment through treatment, support, and accommodations"
            ],
            [
                "Functional Impairment",
                "Quality of Life",
                "-",
                0.88,
                "Greater impairment strongly lowered quality of life"
            ],
            [
                "Diagnosis Status",
                "Quality of Life",
                "+",
                0.5,
                "Diagnosis could improve quality of life through support and treatment access"
            ],
            [
                "Prenatal Stress",
                "Neurodevelopmental Risk",
                "+",
                0.48,
                "Maternal stress was increasingly discussed as a developmental risk factor"
            ],
            [
                "Maternal Nutrition",
                "Neurodevelopmental Risk",
                "-",
                0.38,
                "Better maternal nutrition supports healthier early development"
            ],
            [
                "Prenatal Substance Exposure",
                "Neurodevelopmental Risk",
                "+",
                0.75,
                "Prenatal smoking or alcohol exposure increased developmental vulnerability"
            ],
            [
                "Birth Complications",
                "Neurodevelopmental Risk",
                "+",
                0.56,
                "Birth complications could increase risk of later developmental difficulties"
            ],
            [
                "Lead Exposure",
                "Neurodevelopmental Risk",
                "+",
                0.7,
                "Lead exposure remained an important environmental neurodevelopmental risk"
            ],
            [
                "Air Pollution",
                "Neurodevelopmental Risk",
                "+",
                0.38,
                "Air pollution was increasingly discussed as a possible developmental risk factor in the 2010s"
            ],
            [
                "Environmental Toxins",
                "Neurodevelopmental Risk",
                "+",
                0.48,
                "Broader toxin exposure remained relevant in neurodevelopmental risk discussions"
            ],
            [
                "Neurodevelopmental Risk",
                "ADHD",
                "+",
                0.84,
                "Higher developmental vulnerability increased the likelihood of ADHD"
            ],
            [
                "Diet Quality",
                "Micronutrient Deficiency",
                "-",
                0.72,
                "Better overall diet quality lowers the chance of micronutrient deficiency"
            ],
            [
                "Micronutrient Deficiency",
                "Symptom Severity",
                "+",
                0.34,
                "Deficiencies were discussed as possibly worsening attention or behavioral regulation"
            ],
            [
                "Ultra-Processed Food Intake",
                "Diet Quality",
                "-",
                0.55,
                "Higher processed food intake generally reflected lower diet quality, though the framing was less central than in 2026"
            ],
            [
                "Ultra-Processed Food Intake",
                "Blood Sugar Instability",
                "+",
                0.36,
                "Highly refined foods could contribute to energy fluctuations, but this link was more tentative"
            ],
            [
                "Blood Sugar Instability",
                "Symptom Severity",
                "+",
                0.2,
                "Possible short-term attention or regulation effects were discussed, though evidence was less central and more contested"
            ],
            [
                "Sleep Quality",
                "Symptom Severity",
                "-",
                0.62,
                "Better sleep improved attention, regulation, and executive control"
            ],
            [
                "Physical Activity",
                "Symptom Severity",
                "-",
                0.46,
                "Physical activity could help reduce symptom burden"
            ],
            [
                "Screen Time",
                "Symptom Severity",
                "+",
                0.38,
                "Higher screen exposure was increasingly discussed as worsening attention or self-regulation"
            ],
            [
                "ADHD",
                "Sleep Quality",
                "-",
                0.6,
                "ADHD often disrupted sleep routines and sleep quality"
            ],
            [
                "ADHD",
                "Screen Time",
                "+",
                0.36,
                "ADHD could increase impulsive or reward-seeking media use"
            ]
        ]
    },
    "2026": {
        "period_label": "2026",
        "positions": {
            "ADHD": [
                0,
                0
            ],
            "Diagnosis Status": [
                0,
                350
            ],
            "Age": [
                -500,
                -200
            ],
            "Gender": [
                -380,
                -200
            ],
            "Genetic Risk": [
                -300,
                -80
            ],
            "Symptom Severity": [
                -200,
                -200
            ],
            "Symptom Type": [
                -200,
                -80
            ],
            "Comorbid Conditions": [
                -100,
                -300
            ],
            "Parental Awareness": [
                -500,
                200
            ],
            "Parenting Style": [
                -500,
                80
            ],
            "Family Stress": [
                -380,
                130
            ],
            "Household Stability": [
                -500,
                320
            ],
            "Teacher Referral Rate": [
                -100,
                -420
            ],
            "Classroom Size": [
                100,
                -500
            ],
            "Academic Demands": [
                300,
                -500
            ],
            "School Resources": [
                300,
                -380
            ],
            "Workplace Accommodations": [
                500,
                -200
            ],
            "Access to Mental Health Care": [
                500,
                200
            ],
            "Provider Availability": [
                650,
                80
            ],
            "Diagnostic Criteria Variability": [
                300,
                420
            ],
            "Waiting Time for Assessment": [
                500,
                350
            ],
            "Cost of Evaluation": [
                500,
                480
            ],
            "Stigma": [
                400,
                -300
            ],
            "Gender Bias": [
                200,
                -300
            ],
            "Cultural Norms": [
                550,
                -380
            ],
            "Socioeconomic Status": [
                650,
                -80
            ],
            "Age at Diagnosis": [
                0,
                500
            ],
            "Misdiagnosis Rate": [
                200,
                480
            ],
            "Functional Impairment": [
                -300,
                300
            ],
            "Quality of Life": [
                -500,
                450
            ],
            "Neurodevelopmental Risk": [
                -50,
                100
            ],
            "Prenatal Stress": [
                -750,
                -50
            ],
            "Maternal Nutrition": [
                -750,
                -150
            ],
            "Prenatal Substance Exposure": [
                -750,
                50
            ],
            "Birth Complications": [
                -750,
                150
            ],
            "Diet Quality": [
                -700,
                -350
            ],
            "Micronutrient Deficiency": [
                -550,
                -350
            ],
            "Ultra-Processed Food Intake": [
                -850,
                -350
            ],
            "Blood Sugar Instability": [
                -700,
                -450
            ],
            "Lead Exposure": [
                850,
                -50
            ],
            "Air Pollution": [
                850,
                50
            ],
            "Environmental Toxins": [
                850,
                150
            ],
            "Sleep Quality": [
                -150,
                -550
            ],
            "Physical Activity": [
                0,
                -600
            ],
            "Screen Time": [
                150,
                -550
            ]
        },
        "edges": [
            [
                "Genetic Risk",
                "ADHD",
                "+",
                0.92,
                "Strong inherited contribution to ADHD liability"
            ],
            [
                "ADHD",
                "Symptom Severity",
                "+",
                0.96,
                "ADHD directly increases the severity of core symptoms"
            ],
            [
                "ADHD",
                "Symptom Type",
                "+",
                0.91,
                "ADHD influences whether symptoms appear as inattentive, hyperactive, or combined"
            ],
            [
                "ADHD",
                "Comorbid Conditions",
                "+",
                0.72,
                "ADHD commonly co-occurs with other psychiatric or developmental conditions"
            ],
            [
                "ADHD",
                "Functional Impairment",
                "+",
                0.93,
                "ADHD contributes strongly to impairment in school, work, and daily functioning"
            ],
            [
                "ADHD",
                "Quality of Life",
                "-",
                0.8,
                "ADHD symptoms and impairment can reduce overall quality of life"
            ],
            [
                "ADHD",
                "Misdiagnosis Rate",
                "-",
                0.35,
                "Clearer ADHD presentation can sometimes reduce misdiagnosis by making the disorder easier to identify"
            ],
            [
                "Age",
                "Symptom Severity",
                "-",
                0.38,
                "Some symptoms may become less overt or differently expressed with age"
            ],
            [
                "Age",
                "Diagnosis Status",
                "+",
                0.52,
                "Older age can increase the chance that symptoms are eventually recognized"
            ],
            [
                "Diagnosis Status",
                "Age at Diagnosis",
                "-",
                1.0,
                "Earlier diagnosis directly lowers age at diagnosis by definition"
            ],
            [
                "Gender",
                "Diagnosis Status",
                "+",
                0.48,
                "Gender still influences who gets identified and diagnosed"
            ],
            [
                "Gender",
                "Symptom Type",
                "+",
                0.44,
                "Gender can shape which symptom profiles are more visible or emphasized"
            ],
            [
                "Symptom Severity",
                "Diagnosis Status",
                "+",
                0.85,
                "More severe symptoms make diagnosis more likely"
            ],
            [
                "Symptom Type",
                "Teacher Referral Rate",
                "+",
                0.77,
                "More disruptive or visible symptom types increase school referral"
            ],
            [
                "Teacher Referral Rate",
                "Diagnosis Status",
                "+",
                0.82,
                "Teacher concerns often lead to evaluation and diagnosis"
            ],
            [
                "Parental Awareness",
                "Diagnosis Status",
                "+",
                0.83,
                "Parents who recognize symptoms are more likely to seek help"
            ],
            [
                "Parenting Style",
                "Symptom Severity",
                "-",
                0.32,
                "Supportive structure can reduce symptom expression, though not the core condition"
            ],
            [
                "Family Stress",
                "Symptom Severity",
                "+",
                0.6,
                "Stress in the family can worsen symptom expression"
            ],
            [
                "Family Stress",
                "Comorbid Conditions",
                "+",
                0.54,
                "Family stress can contribute to anxiety, mood, or behavioral difficulties"
            ],
            [
                "Household Stability",
                "Family Stress",
                "-",
                0.75,
                "Greater household stability tends to reduce family stress"
            ],
            [
                "Classroom Size",
                "Teacher Referral Rate",
                "+",
                0.4,
                "Larger classrooms can make attention and behavior difficulties harder to manage"
            ],
            [
                "Academic Demands",
                "Functional Impairment",
                "+",
                0.7,
                "Higher academic demands increase the impact of executive dysfunction"
            ],
            [
                "Functional Impairment",
                "Diagnosis Status",
                "+",
                0.76,
                "Visible impairment pushes families, schools, or clinicians toward diagnosis"
            ],
            [
                "School Resources",
                "Diagnosis Status",
                "+",
                0.6,
                "Better school support systems can help students get identified and assessed"
            ],
            [
                "Workplace Accommodations",
                "Functional Impairment",
                "-",
                0.58,
                "Accommodations can reduce adult functional impairment"
            ],
            [
                "Access to Mental Health Care",
                "Diagnosis Status",
                "+",
                0.88,
                "Better access makes assessment and diagnosis more likely"
            ],
            [
                "Provider Availability",
                "Diagnosis Status",
                "+",
                0.78,
                "More providers increase the likelihood of timely assessment"
            ],
            [
                "Waiting Time for Assessment",
                "Diagnosis Status",
                "-",
                0.62,
                "Longer waiting times delay or reduce completed diagnoses"
            ],
            [
                "Cost of Evaluation",
                "Diagnosis Status",
                "-",
                0.74,
                "High evaluation cost creates a financial barrier to diagnosis"
            ],
            [
                "Diagnostic Criteria Variability",
                "Diagnosis Status",
                "+",
                0.45,
                "Broader or flexible interpretation of criteria can increase diagnosis rates"
            ],
            [
                "Diagnostic Criteria Variability",
                "Misdiagnosis Rate",
                "+",
                0.84,
                "Inconsistent interpretation of criteria raises misdiagnosis risk"
            ],
            [
                "Stigma",
                "Parental Awareness",
                "-",
                0.66,
                "Stigma can discourage parents from noticing or acting on symptoms"
            ],
            [
                "Stigma",
                "Diagnosis Status",
                "-",
                0.72,
                "Stigma reduces willingness to pursue or accept diagnosis"
            ],
            [
                "Gender Bias",
                "Diagnosis Status",
                "+",
                0.63,
                "Bias can increase diagnosis in stereotyped groups while reducing it in others"
            ],
            [
                "Cultural Norms",
                "Stigma",
                "+",
                0.74,
                "Cultural beliefs shape stigma around ADHD and mental health"
            ],
            [
                "Socioeconomic Status",
                "Access to Mental Health Care",
                "+",
                0.84,
                "Higher socioeconomic status improves access to specialists and care"
            ],
            [
                "Socioeconomic Status",
                "Parental Awareness",
                "+",
                0.56,
                "More resources often increase access to information and advocacy"
            ],
            [
                "Socioeconomic Status",
                "Cost of Evaluation",
                "-",
                0.79,
                "Higher socioeconomic status reduces the effective burden of evaluation cost"
            ],
            [
                "Comorbid Conditions",
                "Functional Impairment",
                "+",
                0.75,
                "Comorbid conditions often increase total impairment burden"
            ],
            [
                "Diagnosis Status",
                "Functional Impairment",
                "-",
                0.56,
                "Diagnosis can reduce impairment through treatment and accommodations"
            ],
            [
                "Functional Impairment",
                "Quality of Life",
                "-",
                0.89,
                "Greater impairment strongly lowers quality of life"
            ],
            [
                "Diagnosis Status",
                "Quality of Life",
                "+",
                0.52,
                "Diagnosis may improve quality of life through support and treatment access"
            ],
            [
                "Prenatal Stress",
                "Neurodevelopmental Risk",
                "+",
                0.5,
                "Maternal stress can affect fetal neurodevelopment"
            ],
            [
                "Maternal Nutrition",
                "Neurodevelopmental Risk",
                "-",
                0.42,
                "Better maternal nutrition supports healthy brain development"
            ],
            [
                "Prenatal Substance Exposure",
                "Neurodevelopmental Risk",
                "+",
                0.78,
                "Prenatal alcohol or smoking exposure can impair neural development"
            ],
            [
                "Birth Complications",
                "Neurodevelopmental Risk",
                "+",
                0.58,
                "Birth complications can increase developmental vulnerability"
            ],
            [
                "Neurodevelopmental Risk",
                "ADHD",
                "+",
                0.86,
                "Higher neurodevelopmental vulnerability increases ADHD likelihood"
            ],
            [
                "Diet Quality",
                "Micronutrient Deficiency",
                "-",
                0.81,
                "Better diet quality lowers the chance of micronutrient deficiency"
            ],
            [
                "Micronutrient Deficiency",
                "Symptom Severity",
                "+",
                0.46,
                "Deficiencies may worsen attention, mood, or self-regulation"
            ],
            [
                "Ultra-Processed Food Intake",
                "Diet Quality",
                "-",
                0.83,
                "High ultra-processed food intake tends to reduce overall diet quality"
            ],
            [
                "Ultra-Processed Food Intake",
                "Blood Sugar Instability",
                "+",
                0.72,
                "High sugar and refined foods can increase glucose instability"
            ],
            [
                "Blood Sugar Instability",
                "Symptom Severity",
                "+",
                0.34,
                "Energy swings may worsen attention and behavioral regulation"
            ],
            [
                "Lead Exposure",
                "Neurodevelopmental Risk",
                "+",
                0.72,
                "Lead exposure harms cognitive and neurodevelopmental functioning"
            ],
            [
                "Air Pollution",
                "Neurodevelopmental Risk",
                "+",
                0.48,
                "Air pollution is associated with inflammatory and developmental risk"
            ],
            [
                "Environmental Toxins",
                "Neurodevelopmental Risk",
                "+",
                0.58,
                "Toxin exposure can disrupt developing neural systems"
            ],
            [
                "Sleep Quality",
                "Symptom Severity",
                "-",
                0.68,
                "Better sleep improves attention, regulation, and executive control"
            ],
            [
                "Physical Activity",
                "Symptom Severity",
                "-",
                0.5,
                "Physical activity can help reduce symptom burden"
            ],
            [
                "Screen Time",
                "Symptom Severity",
                "+",
                0.4,
                "Excessive screen time may worsen attention and self-regulation difficulties"
            ],
            [
                "ADHD",
                "Sleep Quality",
                "-",
                0.64,
                "ADHD often disrupts sleep routines and sleep quality"
            ],
            [
                "ADHD",
                "Screen Time",
                "+",
                0.42,
                "ADHD can increase impulsive or reward-seeking media use"
            ]
        ]
    }
}

# Define the node colors to match the original graphs.
CORE_NODE_COLORS = {
    "ADHD": "#1f77b4",
    "Diagnosis Status": "#ff7f0e",
}

# Define a helper that formats an edge tooltip.
def build_edge_tooltip(sign, strength, explanation):
    # Choose the effect text from the sign.
    effect_text = "Positive" if sign == "+" else "Negative"

    # Normalize explanation text safely.
    clean_explanation = str(explanation).replace("\r\n", "\n").replace("\r", "\n").strip()

    # Return plain text tooltip only.
    return (
        f"Effect: {effect_text}\n"
        f"Why: {clean_explanation}\n"
        f"Strength: {strength:.2f}"
    )

# Define a helper that builds the network HTML for one year snapshot.
def build_network_html(selected_year):
    # Read the selected year's data.
    year_snapshot = YEAR_DATA[str(selected_year)]
    # Extract node positions.
    node_positions = year_snapshot["positions"]
    # Extract edges.
    edges = year_snapshot["edges"]

    # Create the network.
    net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")

    # Use stable, fixed rendering.
    net.set_options(
        """
        var options = {
          "layout": {
            "improvedLayout": false
          },
          "physics": {
            "enabled": false
          },
          "interaction": {
            "dragNodes": false,
            "dragView": true,
            "zoomView": true,
            "hover": true,
            "navigationButtons": true
          },
          "edges": {
            "smooth": false,
            "font": {
              "size": 12,
              "align": "top"
            }
          }
        }
        """
    )

    # Add all nodes from the selected snapshot.
    for node_name, coordinates in node_positions.items():
        # Read x and y.
        x_pos, y_pos = coordinates
        # Choose the original color.
        node_color = CORE_NODE_COLORS.get(node_name, "#dddddd")
        # Choose the original size.
        node_size = 45 if node_name in CORE_NODE_COLORS else 25
        # Choose the original font size.
        font_size = 18 if node_name in CORE_NODE_COLORS else 13
        # Add the node.
        net.add_node(
            node_name,
            label=node_name,
            x=x_pos,
            y=y_pos,
            fixed=True,
            physics=False,
            color=node_color,
            size=node_size,
            font={"size": font_size, "color": "black"},
            title=node_name,
        )

    # Add all edges from the selected snapshot.
    for source, target, sign, strength, explanation in edges:
        # Choose the edge color by sign.
        edge_color = "green" if sign == "+" else "red"
        # Add the edge with the uploaded tooltip content.
        net.add_edge(
            source,
            target,
            label=sign,
            color=edge_color,
            arrows="to",
            title=build_edge_tooltip(sign, strength, explanation),
        )

    # Place a clean period label to the right of the graph.
    max_x = max(coords[0] for coords in node_positions.values())
    period_x = max_x + 250

    # Add the period label box.
    net.add_node(
        "PERIOD_NODE",
        label=f"CHRONOLOGICAL SNAPSHOT\n\n{year_snapshot['period_label']}",
        shape="box",
        color="#f5f5f5",
        size=32,
        x=period_x,
        y=320,
        fixed=True,
        physics=False,
        font={"size": 18, "color": "black", "face": "Arial"},
    )

    # Generate the HTML.
    graph_html = net.generate_html(notebook=False)
    # Improve the default tooltip box styling for readability.
    graph_html = graph_html.replace(
        "</head>",
        """
<style>
div.vis-tooltip {
    white-space: pre-line !important;
    max-width: 340px !important;
    padding: 10px 12px !important;
    border-radius: 8px !important;
    border: 1px solid #d9d9d9 !important;
    background: #ffffff !important;
    color: #111111 !important;
    font-size: 13px !important;
    line-height: 1.5 !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12) !important;
    font-family: Arial, sans-serif !important;
}
</style>
</head>
""",
        1,
    )
    # Return the final HTML.
    return graph_html

# Show the page title.
st.title("Chronological Causal Graph Explorer")
# Show a short description.
st.caption("Use the slider to switch between fixed yearly snapshots. Node positions stay fixed within each snapshot for easier comparison.")

# Create the sidebar controls.
st.sidebar.header("Controls")
# Show the year selector.
selected_year = st.sidebar.select_slider(
    "Choose a year",
    options=[1970, 1990, 2010, 2026],
    value=1970,
)
# Show a small note.
st.sidebar.info("Hover over an edge to see the explanation and strength.")

# Build the selected graph.
graph_html = build_network_html(selected_year)

# Create the layout.
left_col, right_col = st.columns([4.8, 1.2])

# Render the graph.
with left_col:
    # Show the graph title.
    st.subheader(f"Graph for {YEAR_DATA[str(selected_year)]['period_label']}")
    # Render the HTML.
    components.html(graph_html, height=930, scrolling=True)

# Render the readable legend and summary.
with right_col:
    # Show the legend title.
    st.subheader("Legend")
    # Render the legend items.
    st.markdown(
        """
        <div style="background:#f7f7f7;padding:14px 16px;border-radius:12px;line-height:1.6;">
        <b>Green edge (+)</b>: positive effect<br>
        <b>Red edge (-)</b>: negative effect<br>
        <b>Arrow direction</b>: source influences target<br>
        <b>Hover an edge</b>: see explanation and strength
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Add spacing.
    st.markdown("")

    # Read the current snapshot.
    current_snapshot = YEAR_DATA[str(selected_year)]

    # Show quick stats.
    st.subheader("Snapshot")
    st.write(f"Year: {current_snapshot['period_label']}")
    st.write(f"Nodes: {len(current_snapshot['positions'])}")
    st.write(f"Edges: {len(current_snapshot['edges'])}")

    # Add spacing.
    st.markdown("")

    # Show visible variables.
    st.subheader("Variables")
    for node_name in current_snapshot["positions"]:
        if node_name not in ("ADHD", "Diagnosis Status"):
            st.write(f"• {node_name}")
