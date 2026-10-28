"""Explicit, corpus-limited judgments for every existing 2026 edge.

Rules are keyed by constructs rather than edge numbers because the three
personas order shared edges differently. No unmatched edge receives a default
decision: a changed/new construct requires an explicit review.
"""
import ast
import hashlib
import json
from pathlib import Path
from review_evidence import E, CORPUS, SOURCE_NOTES

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
STATUS_DEFINITIONS = {
    'supported': 'Evidence supports the stated direction, sign, and reasoning within the declared scope.',
    'partially_supported': 'Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.',
    'contradicted': 'Relevant evidence opposes the claimed direction or sign within the declared scope.',
    'mixed_evidence': 'Relevant evidence both supports and opposes the same defined claim.',
    'insufficient_evidence': 'Available evidence does not establish or refute the causal claim.',
    'not_assessable': 'Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.',
}
RULES = {}


def rule(source, dest, status, observation, action, keys=(), ages=(8, 32, 45)):
    for age in ages:
        pair = (age, source, dest)
        if pair in RULES:
            raise ValueError(f'Duplicate review: {pair}')
        RULES[pair] = (status, observation, action, keys)


S, P, I, N = 'supported', 'partially_supported', 'insufficient_evidence', 'not_assessable'

rule('Genetic Risk', 'ADHD', S,
     'The biological review synthesizes twin and genomic evidence for inherited ADHD liability across children, adolescents and adults. This supports the broad inherited-liability pathway; it does not validate a deterministic variant or the original strength.',
     'Retain as aggregate inherited liability; keep the numeric strength explicitly unvalidated.', ['genetics'])
rule('ADHD', 'Symptom Severity', N,
     'The latent disorder and the symptoms used to recognize it are not operationally separated. A signed cause-to-severity edge risks restating the disorder definition.',
     'Define underlying liability independently of the measured symptom scale before interpreting this as causal.', ['lifespan'])
for source in ['ADHD', 'Gender']:
    rule(source, 'Symptom Type', N,
         'Symptom Type is an unordered category, so a universal positive sign has no defined interpretation. Sex differences, gender norms, presentation and recognition are separate constructs.',
         'Use an unsigned association or specify a presentation contrast and a defined sex/gender measure.')
rule('Age', 'Symptom Severity', N,
     'Visibility of symptoms at age eight does not define an increasing severity slope with age. No comparison age or symptom-domain coding is supplied.',
     'Replace the universal plus sign with a defined age comparison or domain-specific developmental function.', ['lifespan'], ages=(8,))
rule('Age', 'Symptom Severity', P,
     'The editorial describes hyperactivity/impulsivity declining from childhood to adulthood while inattention is more stable. This supports a domain-specific developmental pattern, not a uniform negative effect on all symptoms at 32.',
     'Specify hyperactivity/impulsivity and the comparison ages; model persistent inattention separately.', ['trajectory', 'lifespan'], ages=(32,))
rule('Age', 'Functional Impairment', I,
     'Lifespan accounts emphasize fluctuating symptoms and variable relationships with impairment. They do not establish that moving to age 45 increases impairment through cumulative untreated difficulties.',
     'Model duration of untreated impairment and context separately from chronological age; require longitudinal evidence.', ['lifespan', 'adult_phenotype'], ages=(45,))
rule('Early Life Nutrition', 'Genetic Risk', N,
     'Inherited genetic liability is fixed before postnatal nutrition. Maternal diet may relate to expression or developmental risk, but the genetic trio study finds substantial confounding and no robust causal diet pathway; it does not show nutrition reducing inherited risk.',
     'Change the destination to a defined developmental or symptom outcome; distinguish inherited genotype from environmental expression.', ['genetic_trio'], ages=(8,))
rule('Nutrition Quality', 'Symptom Severity', P,
     'The carbohydrate review reports associations of poorer carbohydrate quality with symptom burden, with heterogeneous intervention results and limited certainty. Probiotic RCTs do not demonstrate a clear core-symptom benefit. These are different nutritional exposures and do not validate a uniform diet effect.',
     'Specify the dietary exposure and outcome; label causality and exact-age benefit uncertain.', ['diet', 'probiotics'], ages=(8,))
rule('Nutrition Quality', 'Symptom Severity', P,
     'A small adult study links lower B12/vitamin D levels to greater symptoms. This supports an adult association with specific biomarkers, not evidence that changing overall diet reduces symptoms. Mixed-age carbohydrate evidence is also heterogeneous.',
     'Describe a biomarker association or specify an adult nutritional intervention; do not claim an exact-age causal benefit.', ['adult_vitamins', 'diet'], ages=(32,45))
rule('Sleep Quality', 'Symptom Severity', P,
     'Pediatric sleep-management literature describes insomnia as potentially worsening symptoms, but the selected study is qualitative. Longitudinal genetic work also finds ADHD symptoms preceding sleep difficulties. Broad clinical consistency does not establish this one-way causal effect at eight.',
     'Define insomnia/sleep quality and show bidirectional uncertainty; seek an age-relevant sleep-intervention symptom endpoint.', ['sleep_child', 'sleep_direction'], ages=(8,))
rule('Sleep Quality', 'Symptom Severity', I,
     'The directly relevant supplied sleep studies are pediatric; they do not establish adult sleep improvement causing symptom reduction at 32. Shared sleep/ADHD biology is not an adult intervention result.',
     'Add an adult ADHD sleep-intervention study with a symptom endpoint.', ['sleep_direction'], ages=(32,))
rule('Sleep Quality', 'Executive Function Deficit', I,
     'The corpus sleep studies emphasize children, sleep problems, or internalizing symptoms. They do not test improved sleep reducing executive deficits in adults near 45.',
     'Add an adult sleep-intervention study measuring executive function rather than transferring pediatric sleep associations.', ['sleep_direction'], ages=(45,))
rule('Environmental Exposure', 'Symptom Severity', P,
     'Prenatal exposure reviews provide narrower associations with offspring ADHD risk. Familial confounding remains. Risk of a later diagnosis and severity caused by current environmental stressors are different endpoints.',
     'Specify the exposure, developmental window and symptom outcome; retain only a qualified environmental association.', ['smoking'], ages=(8,))
for source in ['Screen Time', 'Digital Media Exposure']:
    rule(source, 'Symptom Severity', I,
         'The corpus includes adolescent problematic-use associations and pediatric screen-time group comparisons. Neither establishes a generic exposure causing symptoms for this persona. Problematic use, therapeutic video games and exposure hours are distinct constructs.',
         'Use an age-relevant prospective or experimental design with a defined digital exposure; do not transfer adolescent or university samples.', ['media_youth', 'screens'])
rule('Physical Activity', 'Symptom Severity', I,
     'The exercise reviews mainly concern children/adolescents, with benefits depending on cognitive domain and intervention. The reviewed evidence does not establish symptom reduction specifically in adult ADHD at this age.',
     'Add adult ADHD exercise trials measuring core symptoms; do not transfer pediatric executive-function effects.', ['exercise_limits'], ages=(32,45))
rule('Symptom Severity', 'Functional Impairment', P,
     'Pediatric evidence describes symptom-related academic, peer and daily-function difficulties. This is consistent with the pathway, but impairment also helps define clinical ADHD and the cross-sectional models do not isolate a causal severity gradient.',
     'Retain a qualified association with separately measured symptom and impairment scales.', ['child_impairment', 'family_direction'], ages=(8,))
rule('Symptom Severity', 'Functional Impairment', P,
     'Adult syntheses describe practical impairment associated with ADHD symptoms, but symptoms, functioning and quality of life can change differently. No universal causal severity gradient or exact-age strength is established.',
     'Separate symptoms from function, specify the functional domain, and label the pathway as qualified.', ['adult_ef', 'adult_phenotype', 'function_qol_distinct'], ages=(32,45))
rule('ADHD', 'Executive Function Deficit', P,
     'The adult self-regulation review links ADHD to executive and motivational difficulties, while biological literature emphasizes heterogeneity. This supports an associated phenotype, not a universal executive deficit caused by ADHD.',
     'Specify the executive domain and measurement; avoid assuming every adult with ADHD has the same deficit.', ['adult_ef'], ages=(32,45))
rule('Executive Function Deficit', 'Functional Impairment', P,
     'Executive/self-regulatory difficulties are implicated in procrastination and adult functioning. Most underlying evidence is cross-sectional, so the precise causal path and persona-specific magnitude remain unestablished.',
     'Retain as a qualified domain-specific pathway; obtain longitudinal executive-function and real-life outcome measures.', ['adult_ef', 'adult_cbt_function'], ages=(32,45))
rule('ADHD', 'Comorbid Conditions', P,
     'Adult case-control and cohort studies show elevated anxiety and other co-occurring conditions. Shared liability, selection and reverse pathways prevent interpreting co-occurrence as ADHD causing every comorbidity.',
     'Use a co-occurrence association or condition-specific causal model.', ['adult_comorbidity', 'adult_phenotype'], ages=(32,45))
rule('Comorbid Conditions', 'Functional Impairment', I,
     'The adult cohort documents both comorbid conditions and impairment, without isolating the causal contribution of a defined comorbidity to impairment for this age.',
     'Specify a condition and functional endpoint and compare ADHD with versus without that condition longitudinally.', ['adult_phenotype'], ages=(32,))
rule('Functional Impairment', 'Employment Instability', P,
     'Adult occupational burden and workplace maladjustment are described in the supplied work studies. They are related to employment difficulty but do not isolate impairment causing later job instability.',
     'Specify turnover, unemployment or contract stability as the outcome; seek longitudinal temporal evidence.', ['work_adjustment', 'adult_med_function'], ages=(32,45))
rule('Performance Pressure', 'Functional Impairment', I,
     'Workplace adjustment evidence does not manipulate or measure the graph’s performance-pressure mechanism as a cause of functional impairment.',
     'Define workload or performance demand and test its relationship with independently measured function.', ['work_adjustment'], ages=(32,))
for source in ['Workplace Accommodations', 'Workplace Support']:
    rule(source, 'Functional Impairment', P,
         'Among Japanese workers aged 20–59, workplace adjustments were associated with better adaptation, including high ADHD-trait groups. Cross-sectional selection, trait-based ascertainment and the narrower workplace endpoint limit causal interpretation.',
         'Retain a qualified workplace-adaptation association; specify the adjustment and avoid generalizing to all impairment.', ['work_adjustment'], ages=(32,45))
rule('Remote Work Flexibility', 'Functional Impairment', I,
     'Flexible hours and other workplace adjustments are not the same exposure as remote work. No reviewed source directly tests remote work reducing adult ADHD impairment.',
     'Separate flexible scheduling from remote location and add direct outcome evidence.', ['work_adjustment'], ages=(32,45))
rule('Family Stress', 'Symptom Severity', I,
     'The family studies describe stress associated with child impairment or adult relationship difficulties. They do not establish family stress as the cause of this persona’s core symptom severity.',
     'Model reciprocal pathways and obtain age-relevant longitudinal stress-to-symptom evidence.', ['family_direction'], ages=(8,))
rule('Family Stress', 'Symptom Severity', I,
     'Adult relationship accounts describe burdens associated with ADHD; they do not test family stress causing later core symptom worsening at 32.',
     'Add an adult longitudinal study distinguishing family stress from symptoms and comorbidity.', ['adult_relationship'], ages=(32,))
for source,dest in [('Household Stability','Family Stress'), ('Home Structure Stability','Family Stress'), ('Family Stress','Chronic Stress Load'), ('Chronic Stress Load','Symptom Severity'), ('Chronic Stress Load','Functional Impairment')]:
    rule(source,dest,I,
         'The reviewed corpus does not directly test this specified household/chronic-stress causal pathway in adult ADHD. General relationship or burden accounts do not establish its direction or sign.',
         'Define the exposure, time window and independent endpoint; add adult longitudinal evidence.', ['adult_relationship'], ages=(32,45))
rule('Symptom Type', 'Teacher Referral Rate', N,
     'An unordered symptom category cannot have a universal positive effect. Referral rate also needs a denominator and a specified presentation comparison.',
     'Specify inattentive versus hyperactive/combined presentation and a defined teacher-referral outcome.', ages=(8,))
for source in ['School Resources','Education System Pressure']:
    rule(source,'Teacher Referral Rate',I,
         'Teacher-literacy and school-readiness studies concern knowledge or observed diagnoses; they do not estimate the effect of school resources or institutional pressure on referral rates.',
         'Define the school exposure and measure actual referrals before assigning a causal sign.', ['teacher_literacy'], ages=(8,))
rule('Teacher Referral Rate','Parental Awareness',P,
     'Parent focus groups describe recognition based partly on teacher reports. This supports a qualitative recognition pathway, without a quantified effect of teacher referral rate or proof that it is strong at eight.',
     'Retain teacher communication as a qualified awareness pathway; distinguish reports, referrals and their frequencies.', ['teacher_notice'], ages=(8,))
rule('Peer Comparison','Parental Awareness',I,
     'The corpus does not directly establish peer comparison causing parents to recognize ADHD in children near eight.',
     'Add a recognition study measuring peer-comparison exposure rather than relying on assumed noticing.', ages=(8,))
rule('Parental Education','Parental Awareness',I,
     'The preterm-preschool recognition study found low knowledge despite frequent university education; no independent multivariable predictor remained significant. It does not establish the proposed age-eight education effect.',
     'Separate educational attainment from ADHD-specific knowledge and use age-relevant adjusted estimates.', ['recognition'], ages=(8,))
rule('Parental Awareness','Parental Advocacy',P,
     'The START pilot increased ADHD knowledge and engagement-related measures alongside service uptake. It is an uncontrolled multicomponent intervention, so awareness alone is not an identified cause of advocacy.',
     'Retain as a proposed engagement pathway with multicomponent and causal uncertainty.', ['start_knowledge'], ages=(8,))
rule('Parental Advocacy','Diagnosis Status',I,
     'The START pilot enrolled children already diagnosed with ADHD, so its treatment-engagement gains cannot establish advocacy causing an initial diagnosis.',
     'Add a pre-diagnosis study of advocacy and completed assessment, accounting for access.', ['start_knowledge'], ages=(8,))
for source in ['Parental Advocacy','Diagnosis Status','Care Coordination']:
    rule(source,'School Support Plan',P,
         'A newly diagnosed pediatric engagement pilot increased school accommodations and involved navigation and advocacy. It supports a related school-service pathway but does not isolate this source construct as the cause of a formal support plan.',
         'Specify the school-plan endpoint and local eligibility process; qualify the pathway and remove claims of strong causal likelihood.', ['start_school'], ages=(8,))
rule('School Support Plan','Learning Accommodations',P,
     'The engagement literature includes IEP/504 school services and increased accommodations. This is consistent with a planning-to-service pathway, but the corpus does not separately test formal plan implementation causing specific accommodations.',
     'Define the plan and actual implemented accommodation rather than assuming plan receipt guarantees delivery.', ['start_school'], ages=(8,))
for source in ['Learning Accommodations','School Accommodations']:
    rule(source,'Functional Impairment',I,
         'The corpus reports accommodation uptake and school social-skills trials, but not a direct effect of the graph’s learning accommodations on academic impairment. Social-skills training has a different endpoint and negligible overall effect.',
         'Specify an accommodation and academic functional outcome and add a relevant controlled evaluation.', ['start_school','school_social_null'], ages=(8,))
for source in ['Socioeconomic Status','Financial Status']:
    rule(source,'Access to Mental Health Care',P,
         'Pediatric parent focus groups report financial/time resources as barriers to behavioral care. This supports a resource-access association, but it does not isolate a general socioeconomic effect on initial evaluation or compare decades.',
         'Specify affordability, insurance and service type; avoid strong universal or temporal claims.', ['parent_barriers'], ages=(8,))
    rule(source,'Access to Mental Health Care',P,
         'The mixed-age adherence review reports cost/insurance barriers and links lower socioeconomic resources to treatment discontinuation. This supports a related financial barrier, not a measured effect on initial adult assessment access.',
         'Separate ongoing treatment continuity from evaluation access; specify an adult affordability endpoint.', ['adherence_ses'], ages=(32,45))
rule('Neighborhood Quality','Access to Mental Health Care',I,
     'Geographic diagnosis and treatment variation does not directly measure neighborhood quality causing access. The Danish study leaves most regional variation unexplained and is pediatric.',
     'Define neighborhood resources and measure individual service access with age-relevant adjustment.', ['capacity_null'], ages=(8,))
rule('Neighborhood Quality','Access to Mental Health Care',I,
     'No reviewed adult study isolates a defined neighborhood-quality exposure causing access to ADHD evaluation or services.',
     'Add an adult geographic access study separating deprivation, supply, cost and clinical need.', ages=(32,45))
rule('Provider Availability','Access to Mental Health Care',I,
     'Service barriers and shortages are discussed, but direct provider-supply effects on access are not established. The Danish child study found no significant association of specialist capacity with recorded diagnosis or medication prevalence; those outcomes also differ from access.',
     'Retain as a hypothesis; measure actual appointment availability and access rather than treating provider counts as causal.', ['parent_barriers','capacity_null'], ages=(8,))
rule('Provider Availability','Access to Mental Health Care',I,
     'Provider relationships and continuity affect ongoing treatment, but the reviewed adult evidence does not isolate provider supply causing initial access.',
     'Measure appointment capacity, waiting time and completed adult assessment directly.', ['adherence_access'], ages=(32,45))
for source,dest in [('Telehealth Access','Access to Mental Health Care'),('Telehealth Access','Telehealth Treatment'),('Telehealth Treatment','Treatment Access')]:
    rule(source,dest,I,
         'The supplied digital registry review identifies ongoing videoconferencing trials and the pediatric co-design paper identifies needs. Neither supplies completed evidence that telehealth availability increased access or actual treatment use for this persona.',
         'Add a completed age-relevant telehealth service evaluation; distinguish availability, uptake and clinical benefit.', ['digital_planned'])
rule('Access to Mental Health Care','Diagnosis Status',P,
     'Parent reports describe practical barriers to care and diagnostic recognition, consistent with an evaluation pathway. No controlled probability that healthcare access causes correct diagnosis is supplied.',
     'Specify completed assessment and accurate diagnosis; preserve uncertainty and the distinction between access and ascertainment.', ['parent_barriers','teacher_notice'], ages=(8,))
rule('Access to Mental Health Care','Diagnosis Status',I,
     'Mixed-age treatment-continuity evidence does not establish healthcare access causing initial accurate adult diagnosis at this age.',
     'Add an adult diagnostic-service study measuring completed evaluations and diagnostic accuracy.', ['adherence_access'], ages=(32,45))
rule('Access to Mental Health Care','Care Coordination',I,
     'Accessible services do not automatically imply coordination. Parent studies instead report fragmented communication; no direct access-to-coordination effect is identified.',
     'Measure coordination separately from service access and define its temporal ordering.', ['parent_barriers'], ages=(8,))
rule('Cost of Evaluation','Diagnosis Status',I,
     'The corpus describes general financial/treatment barriers, but does not isolate evaluation cost causing a lower rate of accurate diagnosis. Claims that this barrier weakened over time are not tested.',
     'Obtain an evaluation-fee or insurance study with a diagnostic-completion endpoint.', ['parent_barriers'], ages=(8,))
rule('Cost of Evaluation','Diagnosis Status',I,
     'The mixed-age adherence review measures medication and treatment cost barriers, not the separate effect of adult evaluation cost on initial diagnosis.',
     'Add an adult evaluation-cost study rather than transferring medication-continuity findings.', ['adherence_ses'], ages=(32,45))
for dest in ['Institutional Bias','Access to Mental Health Care']:
    rule('Race / Ethnicity',dest,N,
         'Race/ethnicity is categorical, with no ordered coding or reference population. Structural inequity can be studied, but a universal plus/minus slope from an unordered category is undefined.',
         'Specify a social/structural exposure or population contrast with a defined comparator; avoid biological interpretation.', ['race_prevalence'] if dest=='Institutional Bias' else ())
for dest in ['Teacher Referral Rate','Diagnosis Status','Misdiagnosis Rate']:
    rule('Institutional Bias',dest,I,
         'Observed diagnosis disparities do not by themselves identify institutional bias as the cause, its direction on referrals, or its effect on diagnostic error. No bias intervention or independently measured bias estimate for this edge is established.',
         'Operationalize the institutional process and outcome, specify the comparison population, and distinguish diagnosis frequency from diagnostic accuracy.', ['school_disparity','race_prevalence'] if dest!='Misdiagnosis Rate' else (), ages=(8,))
    rule('Institutional Bias',dest,I,
         'No reviewed adult source isolates independently measured institutional bias causing this diagnostic outcome. Pediatric disparities cannot establish an adult mechanism.',
         'Define the institutional process and comparator and add adult diagnostic pathway/accuracy evidence.', ages=(32,45))
rule('Misdiagnosis Rate','Diagnosis Status',N,
     'An aggregate error rate and individual diagnosis status are different levels of measurement. Diagnosis Status is also ambiguous between any label and a correct diagnosis.',
     'Define an individual accurate-diagnosis endpoint and avoid mixing it with an aggregate misdiagnosis rate.')
for source in ['Diagnostic Criteria Variability','Gender Bias']:
    rule(source,'Misdiagnosis Rate',I,
         'The corpus discusses diagnostic complexity and heterogeneous recognition, but supplies no independently measured effect of this exposure on diagnostic error for this adult age.',
         'Specify the criteria variation or bias measure and compare against a defensible diagnostic reference standard.', ['lifespan'], ages=(32,45))
rule('Comorbid Conditions','Misdiagnosis Rate',P,
     'Adult sources describe overlapping symptoms and diagnostic complexity. This supports a potential diagnostic-obscuring mechanism, not an observed increase in error rates for every comorbidity.',
     'Name the overlapping condition and distinguish screening difficulty from verified misdiagnosis.', ['comorbidity_overlap'], ages=(32,))
rule('Cultural Norms','Stigma',I,
     'Stigma is described as a barrier, but the corpus does not measure a defined cultural-norm exposure causing stigma or prove that stigma is weaker than in earlier decades.',
     'Define the norm, community and stigma scale; require comparable longitudinal data for temporal claims.', ['adherence_stigma'])
rule('Stigma','Diagnosis Status',P,
     'Parent focus groups report hesitancy, misconceptions and stigma in recognition and care-seeking. This is qualitative support for a barrier, not an isolated effect on accurate diagnostic probability.',
     'Describe a qualified recognition/help-seeking pathway rather than a quantified causal diagnosis effect.', ['parent_barriers','teacher_notice'], ages=(8,))
rule('Stigma','Diagnosis Status',I,
     'Adult/mixed-age adherence barriers do not directly establish stigma causing lower initial adult diagnosis. Diagnosis and continuation of an existing treatment are separate endpoints.',
     'Add an adult pre-diagnosis help-seeking study with measured stigma and diagnostic follow-through.', ['adherence_stigma'], ages=(32,45))
for dest in ['Access to Mental Health Care','Self-Diagnosis Behavior']:
    rule('Stigma',dest,I,
         'The supplied synthesis discusses stigma in ongoing engagement, but does not establish its causal effect on initial adult care access or self-recognition.',
         'Distinguish self-recognition, help-seeking, appointment access and adherence, and measure the proposed endpoint.', ['adherence_stigma'], ages=(32,45))
for source,dest in [('Social Media Awareness','Parental Awareness'),('Online Health Information','Self-Diagnosis Behavior'),('Social Media Awareness','Self-Diagnosis Behavior'),('Self-Diagnosis Behavior','Diagnosis Status'),('Self-Diagnosis Behavior','Treatment Access'),('Online Health Information','Treatment Adherence')]:
    rule(source,dest,I,
         'The video-quality audit measures content and the review protocol proposes future evidence synthesis. They do not measure the claimed downstream change in awareness, correct diagnosis, service uptake or adherence. Exposure to online information cannot be assumed beneficial.',
         'Add a completed audience/outcome study with the proposed age group and endpoint; distinguish recognition from validated diagnosis.', ['video_quality'])
rule('Family History Awareness','Self-Diagnosis Behavior',I,
     'The preschool study relates family history to parents’ symptom recognition, and the adherence review discusses treatment familiarity. Neither directly tests an adult’s family-history awareness causing self-recognition at 45.',
     'Add adult recognition data with a measured awareness exposure.', ['recognition'], ages=(45,))
rule('Care Coordination','Functional Impairment',I,
     'Engagement and continuity findings do not isolate coordination causing reduced adult functional impairment at 32.',
     'Add a coordinated-care comparison with functional outcomes and a defined coordination intervention.', ['adherence_access'], ages=(32,))
rule('Employment Instability','Diagnosis Status',I,
     'Occupational difficulties are documented but no reviewed study isolates unstable employment causing completed adult diagnosis at 45.',
     'Measure the assessment trigger, subsequent help-seeking and diagnostic outcome longitudinally.', ['work_adjustment'], ages=(45,))
for dest in ['Diagnosis Status','Treatment Access']:
    rule('Clinical Guidelines Evolution',dest,I,
         'The pharmacological synthesis can inform future guidance, but does not compare guideline changes with subsequent adult recognition or treatment access. Publication of evidence is not an implementation effect.',
         'Specify a guideline change, implementation setting and before/after recognition or access outcome.', ['med_efficacy_adult'], ages=(45,))
rule('Diagnosis Status','Treatment Access',P,
     'Pediatric recommendations and newly diagnosed engagement studies support entry to treatment pathways. They do not isolate diagnosis alone as the cause of service access or establish the graph’s strong probability.',
     'Retain as a qualified care pathway mediated by eligibility, affordability, preferences and actual service availability.', ['child_care','start_knowledge'], ages=(8,))
rule('Diagnosis Status','Treatment Access',P,
     'Adult medication and CBT studies concern clinically identified ADHD populations and describe appropriate treatment. This supports clinical pathway context, not a causal estimate of how diagnosis changes access.',
     'Describe a treatment-eligibility pathway with measured barriers; do not treat diagnosis as guaranteed access.', ['med_efficacy_adult','adult_cbt_symptoms'], ages=(32,45))
rule('Access to Mental Health Care','Treatment Access',P,
     'Pediatric parent reports describe financial, time and provider-coordination barriers to obtaining treatment. The related access constructs are not independently separated in the graph.',
     'Define evaluation access and actual treatment availability separately; use a qualified service pathway.', ['parent_barriers'], ages=(8,))
rule('Access to Mental Health Care','Treatment Access',P,
     'The mixed-age review links healthcare access/provider communication to treatment continuity. This supports a related care pathway but not an isolated adult causal access effect.',
     'Distinguish initial availability, treatment initiation and continuity; qualify the age-specific causal claim.', ['adherence_access'], ages=(32,45))
rule('Provider Availability','Treatment Access',P,
     'Parents describe availability and coordination as treatment barriers. This supports a qualitative service relationship but not a provider-count causal estimate; Danish capacity associations were null for different prevalence outcomes.',
     'Define actual appointment/treatment capacity; avoid a universal strong supply effect.', ['parent_barriers','capacity_null'], ages=(8,))
rule('Provider Availability','Treatment Access',I,
     'The adult/mixed-age review addresses provider communication and continuity, not an independently measured supply-to-access effect.',
     'Add adult appointment-capacity and treatment-initiation data.', ['adherence_access'], ages=(32,45))
rule('Care Coordination','Treatment Access',P,
     'Pediatric focus groups identify coordination barriers, and a navigation/engagement pilot increased service use. These findings support a qualified pathway but do not isolate coordination from other intervention components.',
     'Define coordination, service initiation and continuity separately; retain a qualified multicomponent interpretation.', ['parent_barriers','start_knowledge'], ages=(8,))
rule('Care Coordination','Treatment Access',P,
     'The adherence review describes continuity problems when providers change and the importance of provider communication. It supports a related ongoing-care pathway, not a controlled effect on initial access at this age.',
     'Specify continuity or treatment persistence as the outcome and label causal effects uncertain.', ['adherence_access'], ages=(32,45))
rule('Socioeconomic Status','Treatment Access',P,
     'Cost/insurance and family-resource barriers are described in pediatric focus groups and the mixed-age adherence review. The Danish study also shows that aggregate socioeconomic medication patterns need not have a universally positive sign.',
     'Specify individual affordability and distinguish access from medication prevalence or continuity.', ['parent_barriers','adherence_ses','ses_diagnosis_null'], ages=(8,))
rule('Socioeconomic Status','Treatment Access',P,
     'The mixed-age review links socioeconomic and insurance barriers with discontinuation. This supports a qualified relationship with continuity, but not a universal effect on initial treatment availability.',
     'Specify income/insurance and initiation versus persistence; avoid an unvalidated exact-age strength.', ['adherence_ses'], ages=(32,45))
for dest in ['Medication Treatment','Behavioral Therapy']:
    rule('Treatment Access',dest,P,
         'Pediatric recommendations include medication and behavioral care, while engagement work reports uptake after a multicomponent intervention. Available treatment can enable uptake, but access is not sufficient and no causal probability is identified.',
         'Retain as a qualified option/uptake pathway that includes clinical indication and preferences.', ['child_care','start_knowledge'], ages=(8,))
    rule('Treatment Access',dest,P,
         'Adult RCT/meta-analytic evidence establishes treatments used in diagnosed ADHD populations, not access as an experimentally isolated determinant of uptake.',
         'Describe access as enabling a treatment option; separately measure offered treatment and actual initiation.', ['med_efficacy_adult'] if dest=='Medication Treatment' else ['adult_cbt_symptoms'], ages=(32,45))
rule('Treatment Access','School Accommodations',P,
     'School-service receipt rose in the START pilot, but a multicomponent engagement intervention is not the same as generic treatment access and does not establish school eligibility requirements.',
     'Specify the school-service process and local access requirements; keep the pathway qualified.', ['start_school'], ages=(8,))
rule('Treatment Access','Workplace Support',I,
     'Workplace adjustment associations do not test whether healthcare treatment access leads to employer accommodations.',
     'Model employer disclosure, eligibility and accommodation delivery separately and add direct pathway evidence.', ['work_adjustment'], ages=(32,45))
rule('Treatment Access','Digital Therapeutics',P,
     'Completed pediatric digital-therapy trials establish that some digital interventions are available treatment options. They do not identify a generic access-to-adoption effect.',
     'Name the evaluated intervention and distinguish availability, adoption and efficacy.', ['digital_child'], ages=(8,))
rule('Treatment Access','Digital Therapeutics',I,
     'The completed digital efficacy syntheses are pediatric, while the registry review describes ongoing adult studies. Neither establishes adult treatment access causing digital-therapy uptake.',
     'Add a completed adult adoption/service study and define which digital treatment is offered.', ['digital_planned'], ages=(32,45))
rule('Medication Treatment','Symptom Severity',P,
     'Double-blind RCT synthesis supports symptom efficacy for specified medications in children/adolescents aged five and older. Drug/dose heterogeneity and broad age bands prevent a universal age-eight magnitude.',
     'Retain a qualified negative pathway for specified agents; do not treat the original strength as an effect estimate.', ['med_efficacy_child'], ages=(8,))
rule('Medication Treatment','Symptom Severity',P,
     'Adult double-blind RCT synthesis supports drug/dose-specific symptom efficacy. It does not provide a separate age-32 or age-45 effect or establish the graph’s numerical strength.',
     'Retain a qualified negative pathway with drug, outcome and age-band scope explicit.', ['med_efficacy_adult'], ages=(32,45))
rule('Medication Treatment','Functional Impairment',I,
     'Adult symptom efficacy cannot substitute for real-world functioning. The supplied stimulant observational study found no adjusted employment benefit and greater social limitations in treated participants; confounding prevents interpreting those associations as harm.',
     'Add functional-outcome RCTs or robust longitudinal analyses; do not infer impairment reduction from symptom efficacy alone.', ['adult_med_function','adult_med_social'], ages=(32,45))
rule('Behavioral Therapy','Symptom Severity',P,
     'A small nonrandomized Chinese parent-training study found symptom reductions; this is narrower than generic behavioral therapy, with parental ratings and limited generalizability.',
     'Specify parent training and outcome raters; preserve study-design and age-range qualifications.', ['parent_training'], ages=(8,))
rule('Behavioral Therapy','Functional Impairment',P,
     'Pediatric guidance supports behavioral treatment, and specific parent-training results improve behavioral symptoms. Functional impairment is a separate endpoint, so this supports a recommended clinical pathway rather than a demonstrated generic functional effect.',
     'Specify the program and measured daily/school functional endpoint; keep benefit provisional.', ['child_care','parent_training'], ages=(8,))
rule('Behavioral Therapy','Symptom Severity',P,
     'Fourteen adult CBT RCTs show symptom improvement. This supports ADHD-specific CBT, not every behavioral therapy or a separate exact-age benefit.',
     'Name adult ADHD CBT and distinguish symptom efficacy from functional or quality-of-life outcomes.', ['adult_cbt_symptoms'], ages=(32,))
rule('Behavioral Therapy','Functional Impairment',P,
     'Adult CBT meta-analysis reports functional improvement, including occupational domains. Mixed study designs, risk of bias, outcome heterogeneity and absence of an exact-age analysis limit the generic behavioral-therapy claim.',
     'Specify adult ADHD CBT and the functional endpoint; qualify certainty and preserve the distinction from quality of life.', ['adult_cbt_function','function_qol_distinct'], ages=(32,45))
rule('Digital Therapeutics','Symptom Severity',P,
     'Pediatric randomized video-game/digital-therapy syntheses support some symptom gains, but effects vary by modality, study quality and clinical relevance. Not all digital tools or screen use are equivalent.',
     'Name the intervention, child age range and outcome; characterize gains as qualified and do not validate the original weight.', ['digital_child','digital_bias'], ages=(8,))
rule('Digital Therapeutics','Symptom Severity',I,
     'The completed efficacy syntheses reviewed are pediatric. Ongoing adult digital trials and general adherence tools do not establish core symptom benefit at this adult age.',
     'Add completed adult digital-therapy symptom trials and define the modality.', ['digital_planned'], ages=(32,45))
rule('Digital Therapeutics','Treatment Adherence',P,
     'The mixed-age adherence synthesis links specific mobile reminders and monitoring programs with improved adherence. Such tools are narrower than digital therapeutics as a whole and the review does not provide an isolated exact-age effect.',
     'Rename the exposure as reminder/monitoring support and specify medication adherence and the relevant age range.', ['adherence_digital'])
for dest in ['Medication Treatment','Behavioral Therapy']:
    rule('Treatment Adherence',dest,N,
         'The reasoning describes better treatment benefit or effect, but the destination represents receipt of treatment. Adherence follows prescription/enrollment and can alter exposure, so the current direction and endpoint are ambiguous.',
         'Change the endpoint to delivered dose, treatment exposure or clinical response and define the time ordering.')
for dest in ['Treatment Access','Functional Impairment']:
    rule('Treatment Dependency',dest,N,
         'Treatment Dependency is undefined, while the reasoning refers to diagnosis opening pathways or treatment improving function. Neither defines dependency or establishes its signed effect.',
         'Replace the source with diagnosis, treatment exposure or a defined dependency construct matching the intended mechanism.')
rule('Stigma','Treatment Adherence',P,
     'The mixed-age review describes stigma as an engagement barrier. This supports the qualitative mechanism, with heterogeneous measures and no isolated exact-age causal estimate.',
     'Retain as a qualified engagement barrier with a specified stigma and adherence measure.', ['adherence_stigma'])
rule('Medication Treatment','Treatment Side Effects',S,
     'The randomized medication synthesis reports treatment-emergent adverse-event discontinuation across pediatric and adult medication groups. This supports medications causing possible side effects; type and risk depend on drug and dose.',
     'Retain the positive pathway as possible treatment-emergent adverse effects; do not imply every patient experiences them or validate the original strength.', ['med_adverse'])
rule('Treatment Side Effects','Treatment Adherence',P,
     'The adherence review identifies adverse effects as a major barrier, and medication RCTs measure adverse-event discontinuation. This supports a tolerability-to-persistence pathway but not a universal exact-age adherence effect.',
     'Specify adverse-event-related discontinuation or measured persistence and retain dose/drug qualifications.', ['side_adherence','med_adverse'])
rule('Treatment Side Effects','Quality of Life',I,
     'Adverse effects and quality of life are documented separately. The corpus does not isolate adverse effects as the cause of a net quality-of-life decrement for this persona.',
     'Add longitudinal adverse-event and quality-of-life measurements that separate symptom benefits from treatment burden.', ['med_adverse'])
rule('Overdiagnosis Pressure','Diagnosis Status',N,
     'Visible discourse about overdiagnosis does not operationalize a pressure exposure. More diagnoses, greater awareness, improved detection and inappropriate diagnosis are different processes.',
     'Define a measurable diagnostic-pressure construct and distinguish ascertainment from diagnostic error.')
rule('Functional Impairment','Quality of Life',P,
     'Pediatric school literature describes functional difficulties affecting quality of life, but does not isolate a causal effect on the child’s own quality of life at eight. Caregiver/family quality of life cannot substitute for the child endpoint.',
     'Use the child’s validated quality-of-life measure and test function separately from symptoms and caregiver burden.', ['child_qol'], ages=(8,))
rule('Functional Impairment','Quality of Life',P,
     'Adult functional difficulties and quality of life are clinically related, but CBT evidence shows they can change differently. No independent causal impairment-to-quality-of-life effect at the persona age is established.',
     'Retain a qualified clinical association and measure functioning and quality of life separately.', ['function_qol_distinct'], ages=(32,45))
rule('Diagnosis Status','Quality of Life',I,
     'Treatment, navigation and support may help some outcomes, but the corpus does not isolate receiving a diagnosis itself as a cause of better child quality of life.',
     'Model the mediated support/treatment pathways and add diagnosis-specific longitudinal evidence.', ['start_knowledge'], ages=(8,))
for dest in ['Quality of Life','Functional Impairment']:
    rule('Diagnosis Status',dest,I,
         'Adult CBT/medication studies concern treatment and diagnosed groups, not diagnosis alone. Improvement after care cannot identify diagnosis as the cause; the long-term follow-up also found no added CBT quality-of-life benefit.',
         'Represent mediated care pathways explicitly and evaluate diagnosis timing separately from treatment and baseline severity.', ['adult_cbt_function','adult_qol_null','adult_phenotype'], ages=(32,45))


def compile_reviews():
    reviews = {}
    for age in (8,32,45):
        path = ROOT / f'2026_{age} yo.py'
        tree = ast.parse(path.read_text())
        edges = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'edges' for t in n.targets))
        rows = []
        for edge_id, (source, dest, sign, strength, reasoning) in enumerate(edges,1):
            status, observation, action, keys = RULES[(age,source,dest)]
            rows.append(dict(edge_id=edge_id,source=source,dest=dest,existing_reasoning=reasoning,
                             sign=sign,validation_status=status,observation_from_validation=observation,
                             recommended_action=action,evidence=[E[key] for key in keys]))
        reviews[str(age)] = {'graph_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                             'original_edges':edges,'edges':rows}
    result = {'status_definitions':STATUS_DEFINITIONS, 'excerpts':E, 'reviews':reviews,
              'corpus_sha256':hashlib.sha256((BASE / 'extracted_papers.json').read_bytes()).hexdigest(),
              'source_notes':{f'PDF_{n:03}': {'title':title or CORPUS[f'PDF_{n:03}']['metadata_title'],
                                           'evidence_scope':note} for n,(title,note) in SOURCE_NOTES.items()}}
    (BASE / 'reviewed_decisions.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print('Compiled explicit reviews:', {age:len(review['edges']) for age,review in reviews.items()})


if __name__ == '__main__':
    compile_reviews()
