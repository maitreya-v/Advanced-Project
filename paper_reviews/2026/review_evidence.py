"""Manually selected passages; quotations must match normalized PDF-page text.

The source PDFs are the evidence authority. These selections are not generated
from keyword matches and do not assert that every paper supports a graph edge.
"""
import json
from pathlib import Path
import unicodedata

BASE = Path(__file__).resolve().parent
CORPUS = {r['source_id']: r for r in json.loads((BASE / 'extracted_papers.json').read_text())}

SOURCE_NOTES = {
    1: ('The effectiveness and feasibility of the new Forest parenting programme for Chinese children with attention-deficit/hyperactivity disorder and their families', 'Nonrandomized Chinese parent-training trial, 30 families; parent-reported outcomes, not a universal behavioral-therapy effect.'),
    4: (None, 'Adult CBT meta-analysis, 70 studies including 38 RCTs; functioning and quality of life are distinct endpoints; no isolated age-32 or age-45 estimate.'),
    7: (None, 'Umbrella review of prenatal smoking and offspring ADHD risk; familial confounding remains, and diagnosis risk differs from current symptom severity.'),
    18: (None, 'Meta-analysis of 14 adult CBT RCTs; intervention-specific results, without a separate age-32 or age-45 effect.'),
    21: (None, 'Ten pediatric video-game RCTs; small inattention benefit judged not clinically meaningful; not generic digital tools or adult evidence.'),
    26: (None, 'Qualitative diagnostic-reassessment interviews; not a controlled effect of diagnosis or guidelines.'),
    33: (None, 'Systematic review of ADHD and procrastination; predominantly cross-sectional evidence precludes causal inference.'),
    39: (None, 'Qualitative parent/carer sleep-management study; contextual sleep evidence, not a sleep intervention efficacy trial.'),
    43: ('Pharmacological interventions for ADHD: a systematic review and dose–effect network meta-analysis', 'Double-blind medication RCT network meta-analysis; separate under-18 and adult analyses, ages five and older. Efficacy and adverse-event discontinuation depend on drug and dose; no separate exact-age effect.'),
    44: (None, 'Linked UK school/health cohort; school readiness at 4–5 and later diagnoses; observed disparities do not identify a causal institutional-bias mechanism.'),
    45: (None, 'Cross-sectional survey of 1,000 Japanese workers aged 20–59, including high ADHD-trait groups; accommodations are associated with adaptation, not randomized effects. Flexible hours are not evidence for remote work.'),
    47: (None, 'Youth racial/ethnic prevalence meta-analysis; ascertainment and sample affect differences. Categories have no universal signed ordering.'),
    48: ('A multi-stakeholder preliminary needs assessment to inform the co-design of a digital telerehabilitation tool for children and adolescents with ADHD', 'Qualitative co-design needs assessment, not an efficacy or access-effect trial.'),
    49: (None, 'Danish register cross-sectional study, ages 4–17. Specialist capacity and waiting times were not significantly associated with diagnosis or medication prevalence; prevalence is not direct access measurement.'),
    55: (None, 'Editorial synthesis of heterogeneous developmental trajectories; not a monotonic effect of age or an exact-age causal estimate.'),
    56: ('Do Children and Adolescents with Attention Deficit Hyperactivity Disorder Use Screens More? A Systematic Review and Meta-Analysis', 'Pediatric screen-time group comparisons, low/very-low certainty; do not identify exposure causing ADHD symptoms.'),
    59: (None, 'Systematic review of caregiver stigma, primarily correlational evidence; caregiver distress and child symptom causation are distinct.'),
    62: (None, 'Open-ended survey of adults with ADHD about relationships; qualitative accounts do not establish stress causing ADHD severity.'),
    63: (None, 'Cross-sectional parental recognition study in preterm preschool children; no independent predictor remained significant in the multivariable model; not age-eight parental education evidence.'),
    64: (None, 'Representative Australian vignette survey measures stigmatizing attitudes; does not estimate cultural norms causing stigma or downstream diagnostic rates.'),
    65: (None, 'Lifespan clinical perspective emphasizes fluctuating trajectories and impairment requirements; not evidence that diagnosis itself improves outcomes.'),
    67: ('Emerging Digital Interventions for ADHD: An Overview of Ongoing Clinical Trials', 'Registry review of 35 ongoing trials; planned videoconferencing interventions are not completed evidence of telehealth access or treatment efficacy.'),
    68: (None, 'Uncontrolled psychoeducation feasibility study of a child’s social network, online or in person; not a controlled school-plan pathway.'),
    74: ('A comprehensive overview of the biological foundations of ADHD', 'Lifespan biological narrative review; supports aggregate genetic liability, not deterministic genes or validated edge weights.'),
    75: (None, 'Pediatric school-based social-skills meta-analysis; overall effect negligible. Social-skills training differs from learning accommodations and academic impairment.'),
    80: (None, '58-study adult case-control anxiety meta-analysis; co-occurrence is not proof ADHD causes another disorder.'),
    86: ('Multimodal Digital Therapeutics Enhanced by Task Design and AI for Attention-Deficit/Hyperactivity Disorder Core Symptoms and Executive Functions in Children and Adolescents: Systematic Review and Network Meta-Analysis of Randomized Controlled Trials', 'Pediatric digital-therapy network meta-analysis, ages 4–17; heterogeneous interventions and substantial risk of bias; no adult efficacy estimate.'),
    89: (None, 'Cross-sectional family study, mean child age 9.6; structural mediation models do not establish causal direction. Child impairment and parental stress are different outcomes.'),
    90: (None, 'Adult 4–8-year follow-up of CBT plus medication/psychoeducation; substantial attrition and no added CBT quality-of-life benefit. Treatment outcome is not diagnosis-only benefit.'),
    92: (None, 'Systematic review of 52 heterogeneous adherence studies across children, adolescents and adults; specific reminder and monitoring interventions differ from broad digital therapeutics; no exact-age effect.'),
    93: ('Age at Diagnosis and Clinical and Genetic Profiles Among Adults With Attention-Deficit/Hyperactivity Disorder', 'Cross-sectional All of Us adult cohort, mean ages 34.8 and 43.8; diagnosis timing is not randomized and group differences do not show diagnostic benefit.'),
    94: (None, 'Pediatric longitudinal sleep-apnea meta-analysis; OSA and generic sleep quality are different constructs.'),
    95: (None, 'Cross-sectional family quality-of-life study; caregiver/family quality of life is not the child’s own quality of life.'),
    99: ('Problematic Social Media Use and ADHD Symptoms in Adolescents', 'Five-wave adolescent ABCD cohort, mean baseline age 12.1; small prospective bidirectional associations. Not age-eight or adult evidence, and problematic use differs from exposure hours.'),
    100: (None, 'Carbohydrate-quality review of 48 studies; mixed ages/designs, confounding and heterogeneous interventions; no generic diet or exact-age causal estimate.'),
    101: (None, 'Nine pediatric probiotic RCTs; no clear core-symptom benefit. Probiotics are not interchangeable with overall diet quality.'),
    103: (None, 'Review restricted to adults 50 and older; cannot be transferred directly to age 45.'),
    104: (None, 'Retrospective cross-sectional adult stimulant study; no adjusted employment benefit, greater social limitations in treated participants. Confounding by indication precludes interpreting this as treatment harm.'),
    107: ('Quality assessment of ADHD-related short videos on Chinese social media: A cross-sectional study', 'Cross-sectional audit of 228 videos measures content quality, not changes in viewer awareness, help-seeking, diagnosis or adherence.'),
    126: (None, 'Scoping review of pharmacist roles; heterogeneous service evidence does not establish generic capacity-to-access effects.'),
    133: ('Socioeconomic burden of attention-deficit/hyperactivity disorder in adults in Japan', 'Cross-sectional socioeconomic burden analysis; unemployment costs do not isolate impairment causing employment instability.'),
    138: (None, 'Dietary inflammatory index observational/Mendelian-randomization study; diet measures and directions differ from a generic nutrition-quality claim.'),
    142: (None, 'Family rare-variant and laboratory study; not population-wide deterministic ADHD causation.'),
    143: (None, 'Maternal dietary-pattern genetic trio study; nonreplication and genetic confounding prevent a robust causal diet pathway; nutrition does not change inherited genotype.'),
    147: (None, 'Pediatric longitudinal sleep/genetic study; ADHD symptoms predicted later sleep traits, not evidence for adult sleep-to-executive-function causation.'),
    149: ('Evaluation of the relationship between vitamin levels and symptom severity in adults with attention-deficit/hyperactivity disorder', 'Small adult cross-sectional biomarker study, 35 ADHD/36 controls. Serum vitamins are not a dietary intervention, and association cannot establish nutrition causing symptom reduction.'),
    152: (None, 'Uncontrolled START community-worker pilot, ages 6–12, 18 families; increased treatment/school-service uptake, without isolating advocacy or care coordination as causes.'),
    153: (None, 'Qualitative parent focus groups about pediatric treatment barriers; not causal effect sizes, adult evidence, or proof barriers weakened over time.'),
    156: ('What Predicts Attention-Deficit/Hyperactivity Disorder Literacy in Primary Schoolteachers?', 'Indian teacher-literacy cross-sectional study; knowledge and school characteristics do not directly measure referral rates.'),
    157: (None, 'Exercise review with effects especially in children/adolescents and no significant hyperactivity/impulsivity benefit; not an exact-age adult efficacy result.'),
}

E = {}


def ev(key, number, page, quote, relevance):
    quote = unicodedata.normalize('NFKC', quote).replace('\u00ad', '')
    source_id = f'PDF_{number:03}'
    text = CORPUS[source_id]['pages'][page - 1]
    if quote not in text:
        raise ValueError(f'Unverified quotation {key}: {source_id}, page {page}')
    E[key] = {'source_id': source_id, 'exact_excerpt': quote,
              'location': f'PDF page {page} (one-based file page)', 'relevance': relevance}


ev('genetics', 74, 14, 'For ADHD, twin studies conducted across various European countries estimate a weighted average heritability of 76%, a value consistent across children, adolescents, and adults', 'Supports inherited liability across the lifespan; heritability is not the original numeric edge strength.')
ev('genetic_trio', 143, 1, 'Collectively, these genetic results indicate a potential pathway by which genetic confounding can inﬂate observed associations between maternal dietary pattern in pregnancy and offspring ADHD, and do not provide any robust evidence consistent with a causal pathway between the two.', 'Does not support early nutrition reducing inherited genetic risk; distinguishes confounding from environmental modification.')
ev('diet', 100, 1, 'Conclusions: Poorer carbohydrate quality may be associated with greater ADHD-related symptom burden, whereas total carbohydrate intake showed inconsistent associations.', 'Qualified diet-quality association; narrower exposure and heterogeneous ages/designs, without a generic causal nutrition effect.')
ev('probiotics', 101, 1, 'Current 8–12-week RCT evidence does not demonstrate a clear benefit of probiotic supplementation for ADHD core symptomrelated measures.', 'Limits treatment overgeneralization; does not refute all nutritional interventions.')
ev('adult_vitamins', 149, 1, 'These findings indicate that lower serum vitamin B12 and 25-hydroxyvitamin D levels are associated with greater ADHD symptom severity in adults.', 'Adult biomarker association is narrower than diet quality and cannot establish benefit from changing diet.')
ev('sleep_child', 39, 1, 'Many children with ADHD have chronic insomnia, which is associated with negative outcomes for the child and family and can worsen ADHD symptoms.', 'Pediatric sleep context in a qualitative study; not a controlled sleep-to-symptom estimate.')
ev('sleep_direction', 147, 1, 'Latent growth curve modeling revealed that ADHD symptoms signiﬁcantly impacted sleep traits with a lag effect.', 'Documents a reverse temporal pathway; cautions against assuming sleep is always upstream.')
ev('smoking', 7, 1, 'Further analyses indicated substantial heterogeneity and potential confounding by familial factors.', 'Prenatal smoking risk associations do not validate generic contemporary environmental stressors causing symptom severity.')
ev('media_youth', 99, 1, 'The analytic sample consisted of 11 286 youths with a mean (SD) age at year 2 of 12.1 (0.67)', 'Makes the adolescent population explicit; cannot be transferred directly to age eight or adult personas.')
ev('screens', 56, 2, 'Conclusions: Children and adolescents with ADHD spent more time during weekdays using screens and were therefore more likely to exhibit excessive screen and computer use.', 'ADHD group screen-use difference does not identify exposure causing symptoms.')
ev('child_impairment', 89, 2, 'ADHD is associated with significant functional impairments, including difficulties in peer relationships, academic underachievement, and challenges in daily activities', 'Clinical association supports a qualified symptom/impairment pathway, not an isolated causal severity gradient.')
ev('family_direction', 89, 2, 'Functional impairment, parental ADHD, and family functioning, rather than child ADHD symptoms, are key determinants of parental stress in families of children with ADHD.', 'Cross-sectional results concern impairment and parental stress; they do not establish family stress causing child severity.')
ev('recognition', 63, 1, 'The overall model predicting general ADHD knowledge was significant (p = 0.020) in multivariable linear regression, but no single independent predictor re­ mained significant.', 'Preterm-preschool recognition study does not establish parental education causing recognition at age eight.')
ev('parent_barriers', 153, 1, 'Parents reported barriers that can be conceptualized as (1) misconceptions and stigma; (2) availability of financial and time-related resources; and (3) treatment messaging and provider coordination.', 'Qualitative pediatric barriers support qualified resource, stigma, and coordination pathways, not causal effect sizes or adult transfer.')
ev('teacher_notice', 153, 5, 'These observations were based on witnessing their child’s behavior or reports from others (such as their child’s teacher).', 'Qualitative accounts support teacher reports contributing to recognition, not a measured effect of referral frequency.')
ev('start_knowledge', 152, 1, 'From pre- to post-intervention, median number of outpatient treatments increased from 1.0 (IQR = 1.5) to 2.0 (IQR = 0.5; p = .0034), ADHD knowledge increased (p < .0001)', 'An uncontrolled multicomponent pilot connects knowledge/engagement and service uptake but cannot isolate a causal awareness-to-advocacy effect.')
ev('start_school', 152, 5, 'a statistically significant increase in receipt of school accommodations (from 38% to 88%, p = .0047).', 'Uncontrolled pilot reports school-service uptake, not evidence for all diagnosed children or an isolated coordination effect.')
ev('school_disparity', 44, 1, 'Male and White British heritage individuals were more likely to have received a diagnosis for ADHD than females and those of South Asian heritage or other ethnicities', 'Specific observed diagnosis disparity; does not identify a universal signed racial effect or prove institutional bias.')
ev('race_prevalence', 47, 2, 'The study demonstrates that the type of sample and method for assessing ADHD diagnosis are important to consider.', 'Diagnostic prevalence differences depend on ascertainment and cannot by themselves validate institutional mechanisms.')
ev('capacity_null', 49, 1, 'Neither waiting times nor specialist capacity was significantly associated with either outcome.', 'Pediatric counter-context to universal supply claims; outcomes are recorded diagnoses and medication prevalence, not direct access.')
ev('ses_diagnosis_null', 49, 1, 'Municipal socioeconomic status was weakly and inversely correlated with medication use (ρ = −0.20, p = 0.049), but not diagnoses.', 'Context-dependent aggregate prevalence does not establish positive individual SES-to-access causation.')
ev('school_social_null', 75, 1, 'the overall meta-analytic effect size was negligible (ES = 0.09).', 'School social-skills programs do not establish generic learning-accommodation effectiveness; the outcome differs.')
ev('parent_training', 1, 1, 'compared with the control group, the intervention group showed significant reductions in inattention, hyperactivity/impulsivity, and oppositional defiant scores after the NFPP intervention.', 'Nonrandomized parent-training evidence is pediatric and intervention-specific.')
ev('child_care', 153, 1, 'The American Academy of Pediatrics (AAP) recommends behavioral therapy as first-line evidence-based treatment for young children with ADHD, and in combination with medications for children ages 6 years and older.', 'Recommendation describes an appropriate care pathway, not a causal probability of uptake after access or diagnosis.')
ev('digital_child', 21, 1, 'Conclusion: Findings indicate that video game interventions show statistically significant but not clinically meaningful benefits on attention and may be therapeutic when added to other evidence-based therapies.', 'Qualifies pediatric digital-treatment support and its clinical relevance; not adult efficacy or generic screen exposure.')
ev('digital_bias', 86, 1, 'a high risk in 40.6% of the studies, mainly due to inadequate reporting of randomization or blinding.', 'Digital-treatment results need qualification for study quality and modality heterogeneity.')
ev('digital_planned', 67, 1, 'Of 149 identified trials, 35 ongoing studies met inclusion criteria.', 'Planned digital/telehealth trials do not establish completed access or clinical-effect evidence.')
ev('adult_cbt_symptoms', 18, 1, 'Analysis of 14 RCTs selected from 949 identified records showed significant benefits of CBT for core ADHD symptoms (SMD = −0.45, P < 0.00001)', 'Supports adult ADHD-specific CBT effects, not every behavioral intervention or an exact-age estimate.')
ev('adult_cbt_function', 4, 1, 'CBT produced moderate effects on global functioning at post-treatment (SMD = 0.47) that increased at follow-up (SMD = 0.67).', 'Adult CBT functional benefit; meta-analysis mixes designs and does not isolate age 32 or 45.')
ev('function_qol_distinct', 4, 1, 'The dissociation between symptom change, QoL, and functioning suggests that functional gains may not be fully explained by symptom reduction alone, although the mechanisms underlying these effects remain unclear.', 'Functional impairment and quality of life are related but distinct; symptom or function improvement cannot automatically prove a direct QoL edge.')
ev('adult_qol_null', 90, 1, 'No significant between-group differences were found in the proportion of participants achieving clinically meaningful QoL improvements over time.', 'Long-term CBT follow-up found no between-group QoL benefit; this does not test diagnosis alone.')
ev('adult_comorbidity', 80, 1, 'The average effect size (Hedges’s g) of anxiety scores in those with ADHD relative to controls was 0.77 (SE = 0.066); a medium effect.', 'Adult anxiety co-occurrence; causal direction from ADHD is not established.')
ev('adult_ef', 33, 1, 'Findings were also consistent with the involvement of executive functioning deficits, emotion dysregulation, and motivational processes, although evidence was primarily based on cross-sectional designs.', 'Executive/self-regulatory difficulties have associated functional consequences; does not prove universal ADHD-to-deficit causation.')
ev('adult_phenotype', 93, 1, 'both groups showed substantial clinical burden.', 'Adult groups around the two persona ages have comorbidity/impairment; cross-sectional diagnosis-age groups do not identify diagnostic benefits or cumulative age effects.')
ev('work_adjustment', 45, 1, 'workplace adjustments equivalent to reasonable accommodations are associated with a lower risk of workplace maladjustment and improved workplace adaptation among employees with high ASD or ADHD trait levels', 'Supports qualified adult workplace-support association, not randomized effects, general functional recovery or remote-work benefit.')
ev('adult_med_function', 104, 1, 'No significant differences were found in the employment outcomes between the two groups in adjusted models.', 'No demonstrated adjusted employment benefit in this adult observational study; not proof of medication inefficacy for all functional outcomes.')
ev('adult_med_social', 104, 1, 'Stimulant-treated adults had higher odds of social limitations (OR = 3.16 [1.50, 6.69])', 'Confounding by indication is possible; this association cannot be treated as causal medication harm.')
ev('adherence_ses', 92, 13, 'Low socioeconomic status households or uninsured households were more likely to discontinue treatment due to cost concerns.', 'Mixed-age review links financial resources to continuity; initial evaluation access remains a distinct outcome.')
ev('adherence_access', 92, 12, 'Access to healthcare services and communication with providers significantly influenced adherence', 'Mixed-age synthesis relates provider communication/access to adherence, not proof that generic access creates coordination or diagnosis.')
ev('adherence_digital', 92, 1, 'digital interventions and mobile-based reminders, psychoeducational and behavioral approaches, multimodal and long-term interventions, and consent-based strategies were all linked to improved adherence.', 'Supports specified reminder/monitoring interventions; mixed ages and designs prevent universal age-specific digital-therapy effects.')
ev('adherence_stigma', 92, 1, 'addressing barriers such as stigma, system fragmentation, and cultural mismatch', 'Stigma appears as an engagement barrier; not a controlled exact-age effect or proof all cultural norms increase stigma.')
ev('side_adherence', 92, 10, 'Adverse effects and side effects emerged as a major adherence barrier, with the majority of patients missing doses or stopping medication to avoid physical or mental distress', 'Mixed-age review describes adverse effects as an adherence barrier.')
ev('med_efficacy_child', 43, 1, 'In children and adolescents, methylphenidate, amphetamines, and guanfacine showed increasing median efficacy', 'Randomized medication evidence supports symptom reduction for specified agents and age bands.')
ev('med_efficacy_adult', 43, 1, 'In adults, amphetamines showed a plateau above approximatively 50 mg/day, whereas methylphenidate', 'Adult RCT synthesis supports drug/dose-specific efficacy; not the graph strength or an exact-age dose recommendation.')
ev('med_adverse', 43, 1, 'Dose-dependent increases in discontinuation probability due to adverse events were observed for amphetamines', 'Controlled treatment-emergent adverse-event evidence supports the medication-to-side-effects direction across pediatric/adult groups.')
ev('trajectory', 55, 1, 'hyperactivity/impulsivity typically declines from childhood into adulthood and is more strongly linked to externalizing and risk-taking outcomes, whereas inattention is relatively more stable', 'Editorial discusses domain-specific age trajectories, not an exact-age slope.')
ev('lifespan', 65, 1, 'Longitudinal evidence demonstrates that ADHD trajectories are heterogeneous and non-­linear, with fluctuating symptom ex­ pression and variable relationships to functional impairment.', 'Prevents a universal monotonic age-to-impairment slope or treating diagnosis as a fixed causal exposure.')
ev('video_quality', 107, 1, 'A total of 228 eligible videos were analyzed.', 'Video-quality audit cannot estimate awareness, self-diagnosis, formal diagnosis, or treatment adherence effects.')
ev('exercise_limits', 157, 1, 'Exercise yielded a small-to-moderate improvement in inhibitory control but showed no significant effects on hyperactivity/ impulsivity or inhibition-related N2 and P3 components.', 'Domain-specific exercise effects, especially pediatric; not a demonstrated adult core-symptom effect.')
ev('adult_relationship', 62, 1, 'Adults with ADHD (N = 355) answered an open‐ended survey question asking if and how their ADHD had negatively impacted their romantic relationships.', 'Relationship accounts concern consequences and lived experience, not family stress causing core symptoms.')
ev('teacher_literacy', 156, 1, 'The study found that 98.7% of teachers had a low level of knowledge related to ADHD.', 'Teacher knowledge is relevant context but does not measure school resources causing actual referral rates.')
ev('comorbidity_overlap', 104, 1, 'its symptoms frequently overlap with other conditions, such as anxiety, depression, and mood disorders, further complicating its diagnosis', 'Review context for diagnostic overlap, not a measured comorbidity-to-misdiagnosis rate.')
ev('child_qol', 75, 1, 'Students with ADHD often experience difficulties in academic, behavioral, and social domains, which can negatively impact their overall quality of life', 'Clinical background linking functional difficulties and quality of life; not an isolated age-eight causal effect.')


if __name__ == '__main__':
    print(f'{len(E)} verified quotations from {len({e["source_id"] for e in E.values()})} supplied documents')
