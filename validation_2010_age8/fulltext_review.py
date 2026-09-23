"""Conservative full-text judgments for the 2010 age-eight graph.

The review is intentionally explicit: each graph edge starts as insufficient
evidence, and only the overrides below receive another status.
"""

STATUS_DEFINITIONS = {
    "supported": "Evidence supports the stated direction, sign, and reasoning within the declared scope.",
    "partially_supported": "Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.",
    "contradicted": "Relevant evidence opposes the claimed direction or sign within the declared scope.",
    "mixed_evidence": "Relevant evidence both supports and opposes the same defined claim.",
    "insufficient_evidence": "Available evidence does not establish or refute the causal claim.",
    "not_assessable": "Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.",
}


def evidence(source_id, excerpt, page, relevance):
    return {
        "source_id": source_id,
        "exact_excerpt": excerpt,
        "location": f"PDF page {page}",
        "relevance": relevance,
    }


E = {
    "genetic": evidence(
        "GWAS_META",
        "Although twin and family studies have shown attention-deficit/hyperactivity disorder (ADHD) to be highly heritable, genetic variants influencing the trait at a genome-wide significant level have yet to be identified.",
        1,
        "Supports substantial inherited liability while cautioning that this GWAS did not identify individual genome-wide significant variants.",
    ),
    "age_sex": evidence(
        "AGE_SEX",
        "Overall prevalence of current DSM-IV-like ADHD was 9.2% with a male:female ratio of 2.28:1. The prevalence of DSM-IV-like ADHD was highest in children. Gender differences in DSM-IV-like ADHD subtype prevalences were highest in adolescents.",
        1,
        "Shows age and sex differences in prevalence and subtype patterns, not the graph's proposed social-norm mechanism.",
    ),
    "female_detection": evidence(
        "AGE_SEX",
        "Lower male:female ratios than reported in some clinic-based studies suggest that females are under-diagnosed in the community.",
        1,
        "Supports unequal detection by sex but does not isolate teacher referral or institutional bias.",
    ),
    "sleep": evidence(
        "SLEEP_BEHAVIOR",
        "shorter sleep duration in 7- to 8 year olds (as measured by actigraphy) was associated with increased caregiver reports of inattentive/hyperactive problem behavior.",
        2,
        "Directly relevant to age eight, but observational wording supports association rather than a fully identified causal effect.",
    ),
    "sleep_direction": evidence(
        "SLEEP_BEHAVIOR",
        "There is some evidence of a causal relationship between sleep disruption and difficulties regulating behavior, emotion, and attention. However, such associations have rarely been experimentally evaluated, because the majority of sleep studies have used correlational designs.",
        2,
        "The review itself states both the plausible direction and the causal limitation.",
    ),
    "exposure": evidence(
        "ORGANOCHLORINE",
        "These results support an association between low-level prenatal organochlorine exposure and ADHD-like behaviors in childhood.",
        1,
        "Supports a specific prenatal exposure association, narrower than the graph's generic environmental-stressor claim.",
    ),
    "guidelines": evidence(
        "CPG_REVIEW",
        "The CPGs all recommend: a structured approach to diagnosis and treatment; attention to psychiatric comorbidity and other ADHD-related conflicts during an individual's lifespan; consideration of medication (usually stimulants) and psychosocial therapies; and follow-up and monitoring of patient response.",
        2,
        "Supports diagnosis-linked consideration of medication and psychosocial care, but does not estimate the graph's causal probabilities.",
    ),
    "med_effect": evidence(
        "PHARM_REVIEW",
        "The effectiveness of three doses of methylphenidate (0.15, 0.3, and 0.6 mg kg-1, administered twice daily) compared to placebo was investigated by Pearson et al. [2003] in a double-blind, placebo-controlled crossover study.",
        2,
        "Identifies controlled efficacy evidence in a narrower developmental-disorder population.",
    ),
    "med_side": evidence(
        "PHARM_REVIEW",
        "significant adverse events such as severe social withdrawal, increased crying, drowsiness, and irritability were noted, especially at the higher dose (0.6 mg kg-1) of methylphenidate",
        2,
        "Directly supports medication causing adverse effects, although the population and drug are specific.",
    ),
    "behavior": evidence(
        "CPG_REVIEW",
        "consideration of medication (usually stimulants) and psychosocial therapies; and follow-up and monitoring of patient response.",
        2,
        "Supports psychosocial therapy as recommended care, not a quantified effect on every symptom or impairment outcome.",
    ),
    "impairment": evidence(
        "ODD_REVIEW",
        "Attention-deficit/hyperactivity disorder (ADHD) is a highly prevalent disorder with significant functional impairment.",
        1,
        "Links ADHD and impairment, but does not independently estimate symptom-severity-to-impairment causation.",
    ),
    "qol": evidence(
        "ECZEMA_SLEEP",
        "ADHD affects more than 5% of all children and causes severe psychosocial maladaptation, impairment of quality of life and economic burden on social services.",
        1,
        "Supports an adverse relation between ADHD-related impairment and quality of life, but not the graph's separate diagnosis benefit.",
    ),
    "stigma": evidence(
        "STIGMA_SCALE",
        "The Surgeon General identifies stigma surrounding mental illness and its treatment as a potent barrier to help-seeking.",
        1,
        "Supports a general help-seeking barrier; it does not isolate ADHD diagnosis or treatment adherence in eight-year-olds.",
    ),
}


# edge_id: (status, observation, recommended action, evidence keys)
OVERRIDES = {
    1: ("partially_supported", "The corpus consistently describes ADHD as highly heritable. The large GWAS found no genome-wide significant individual variant, so the broad liability claim is supported more strongly than any specific genetic mechanism.", "Retain the positive edge, define Genetic Risk as aggregate inherited liability, and avoid implying a known single variant.", ["genetic"]),
    2: ("not_assessable", "ADHD and Symptom Severity overlap unless ADHD is defined as a latent liability separate from the symptoms used to diagnose it.", "Define a latent disorder construct and a separate severity measure before assigning a signed causal edge.", []),
    3: ("not_assessable", "Symptom Type is categorical and has no ordered scale, so a universal positive sign is undefined.", "Use category-specific outcomes or an unsigned relationship.", []),
    4: ("not_assessable", "The supplied age analysis shows prevalence and symptom patterns varying with age, but 'age eight is highly visible' is not a positive slope from age to severity.", "Replace the plus sign with an age-specific function or explicit comparison.", ["age_sex"]),
    5: ("not_assessable", "The evidence shows sex differences in subtype prevalence and possible underdiagnosis of females, but Symptom Type is unordered and the proposed gender-norm mechanism was not tested.", "Specify sex or gender, a presentation contrast, and the proposed detection mechanism.", ["age_sex", "female_detection"]),
    6: ("not_assessable", "Inherited liability is not an ordered outcome that better nutrition can simply reduce; no paper tests nutrition changing genetic risk.", "Model nutrition as a possible modifier of expression, not as a cause of inherited liability.", []),
    8: ("partially_supported", "At ages 7-8, shorter objectively measured sleep was associated with more inattentive/hyperactive behavior. The paper emphasizes that most evidence is correlational.", "Retain a qualified negative pathway from sleep duration or quality to behavior and label causal direction uncertain.", ["sleep", "sleep_direction"]),
    9: ("partially_supported", "A cohort study found prenatal organochlorine exposure associated with ADHD-like behaviors. This supports one specified exposure, not generic environmental stressors.", "Replace Environmental Exposure with the measured prenatal contaminant construct or keep the generic edge explicitly provisional.", ["exposure"]),
    10: ("partially_supported", "The corpus consistently links ADHD symptoms with functional impairment, but the supplied wording does not identify an independent causal severity gradient.", "Retain as a clinically coherent pathway while distinguishing definitional association from causal effect.", ["impairment"]),
    11: ("not_assessable", "Symptom Type has no ordered coding, and no supplied study estimates teacher referral rates by presentation.", "Define a specific presentation contrast and a referral denominator.", []),
    29: ("not_assessable", "Race / Ethnicity is categorical and Institutional Bias has no directional scale; a universal plus sign is uninterpretable.", "Specify the population contrast and measured institutional outcome.", []),
    32: ("not_assessable", "Diagnosis Status is ambiguous between any diagnosis and accurate diagnosis, while Misdiagnosis Rate is an aggregate rate.", "Define accurate diagnosis as the outcome before assigning a negative effect.", []),
    35: ("partially_supported", "Guidelines connect structured diagnosis with consideration of medication, but recommendations do not establish how often diagnosis causes medication use.", "Retain as a care pathway and describe it as treatment consideration rather than inevitable treatment.", ["guidelines"]),
    36: ("partially_supported", "Guidelines connect diagnosis and treatment with consideration of psychosocial therapies, without isolating diagnosis as the causal driver of uptake.", "Retain as a recommended care pathway with access and preference modifiers.", ["guidelines", "behavior"]),
    45: ("partially_supported", "The pharmacotherapy review describes controlled methylphenidate efficacy studies, including children, but the quoted evidence is from a narrower developmental-disorder population and does not justify the graph's generic magnitude.", "Retain the negative edge, identify medication and population, and remove the unvalidated strength claim.", ["med_effect"]),
    46: ("partially_supported", "Clinical guidelines recommend psychosocial therapies, but the corpus excerpt does not establish a uniform reduction in core symptom severity across behavioral interventions.", "Specify the intervention and outcome; retain only as a qualified treatment hypothesis.", ["behavior"]),
    47: ("partially_supported", "Psychosocial treatment is recommended and functional outcomes are clinically central, but this corpus does not directly estimate a generic therapy-to-impairment effect.", "Specify the behavioral program and functional endpoint.", ["behavior", "impairment"]),
    49: ("not_assessable", "Adherence occurs after medication is prescribed; the explanation concerns benefit while the destination is Medication Treatment itself.", "Change the destination to treatment exposure or benefit and define adherence temporally.", []),
    50: ("not_assessable", "Participation may modify therapy dose or outcome, but the current destination is receipt of Behavioral Therapy rather than its effect.", "Model participation as a modifier of therapy exposure or outcome.", []),
    51: ("partially_supported", "The stigma paper describes stigma as a barrier to help-seeking. That is related to participation but does not directly measure adherence among treated eight-year-olds.", "Retain only as a broader engagement barrier unless direct adherence evidence is added.", ["stigma"]),
    52: ("supported", "The pharmacotherapy review reports treatment-emergent adverse effects with methylphenidate, directly supporting medication preceding side effects.", "Retain the positive edge; specify that adverse-effect type and risk depend on drug, dose, and population.", ["med_side"]),
    53: ("insufficient_evidence", "The corpus documents adverse effects but the reviewed passages do not estimate whether those effects cause treatment discontinuation or lower adherence.", "Add direct discontinuation or adherence evidence before retaining this causal explanation.", ["med_side"]),
    54: ("insufficient_evidence", "Adverse effects are documented, but their separate causal effect on quality of life is not estimated in the supplied studies.", "Obtain a study measuring adverse effects and quality of life longitudinally.", ["med_side"]),
    56: ("not_assessable", "Overdiagnosis Pressure is not operationalized, and visible public discourse does not itself define a positive causal exposure.", "Define a measurable pressure construct and distinguish diagnostic scrutiny from actual overdiagnosis.", []),
    57: ("partially_supported", "The corpus links ADHD-related psychosocial maladaptation and impairment with poorer quality of life, but does not isolate functional impairment as a causal exposure.", "Retain as a qualified clinical pathway and seek longitudinal evidence separating symptoms, impairment, and quality of life.", ["qol"]),
    58: ("insufficient_evidence", "The evidence documents impaired quality of life among diagnosed or treated children; it does not show that receiving a diagnosis itself improves quality of life.", "Model mediated pathways through effective support and treatment rather than a direct diagnosis benefit.", ["qol"]),
}


DEFAULT_OBSERVATION = "No supplied 2010 paper directly establishes this edge's direction, sign, and stated mechanism for children aged approximately eight. Related context is not treated as causal validation."
DEFAULT_ACTION = "Retain only as an explicitly unvalidated hypothesis or add directly relevant evidence with a defined exposure, outcome, and temporal direction."


def build_review(edges):
    rows = []
    for edge_id, (source, dest, sign, _strength, reasoning) in enumerate(edges, 1):
        status, observation, action, keys = OVERRIDES.get(
            edge_id,
            ("insufficient_evidence", DEFAULT_OBSERVATION, DEFAULT_ACTION, []),
        )
        rows.append({
            "edge_id": edge_id,
            "source": source,
            "dest": dest,
            "existing_reasoning": reasoning,
            "sign": sign,
            "validation_status": status,
            "observation_from_validation": observation,
            "recommended_action": action,
            "evidence": [E[key] for key in keys],
        })
    return rows
