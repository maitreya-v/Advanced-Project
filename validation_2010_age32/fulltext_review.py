"""Conservative full-text judgments for the 2010 age-32 graph."""

STATUS_DEFINITIONS = {
    "supported": "Evidence supports the stated direction, sign, and reasoning within the declared scope.",
    "partially_supported": "Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.",
    "contradicted": "Relevant evidence opposes the claimed direction or sign within the declared scope.",
    "mixed_evidence": "Relevant evidence both supports and opposes the same defined claim.",
    "insufficient_evidence": "Available evidence does not establish or refute the causal claim.",
    "not_assessable": "Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.",
}

def evidence(source_id, excerpt, page, relevance):
    return {"source_id": source_id, "exact_excerpt": excerpt, "location": f"PDF page {page}", "relevance": relevance}

E = {
    "genetic": evidence("GWAS_META", "Although twin and family studies have shown attention-deficit/hyperactivity disorder (ADHD) to be highly heritable, genetic variants influencing the trait at a genome-wide significant level have yet to be identified.", 1, "Supports inherited liability while cautioning that individual genome-wide significant variants were not identified."),
    "adult_course": evidence("ADULT_CBT", "Adult individuals with attention-deficit hyperactivity disorder (ADHD) have been suffering from this neurobiological and highly heritable disorder chronically since childhood.", 1, "Supports persistence into adulthood and inherited liability, but does not provide an age-32-specific estimate."),
    "adult_outcomes": evidence("ADULT_CBT", "Resulting from their longstanding neuropsychological impairments, such as attentional problems, emotional instability, and disinhibition, they are familiar to a multiplicity of negative life outcomes and under-achievement.", 1, "Supports a relationship between longstanding impairment and adverse adult outcomes without isolating a single causal edge."),
    "adult_comorbidity": evidence("ADULT_CBT", "Furthermore, a large part of this population suffers from psychiatric comorbidity.", 1, "Supports adult co-occurrence, not ADHD causing each comorbid condition."),
    "age_persistence": evidence("AGE_SEX", "Although they may no longer meet the full symptom criterion, young adults with a history of lifetime DSM-IV-like ADHD maintain higher levels of ADHD symptoms compared to the general population.", 1, "Supports symptom persistence with attenuation in young adults, but not a causal estimate at age 32."),
    "female_detection": evidence("AGE_SEX", "Lower male:female ratios than reported in some clinic-based studies suggest that females are under-diagnosed in the community.", 1, "Supports unequal detection by sex, but does not directly measure gender bias causing diagnostic errors at age 32."),
    "adult_medication": evidence("CPG_REVIEW", "The NICE guidelines recommend medication treatment as the first-line intervention for children, adolescents, and young adults with severe ADHD as well as for adults with ADHD", 5, "Supports medication as recommended adult treatment, not the probability that diagnosis or access causes its use."),
    "adult_package": evidence("CPG_REVIEW", "Medication treatment should always form part of a comprehensive care package that includes psychological and educational components.", 5, "Supports combined adult care pathways without identifying access effects."),
    "adult_cbt": evidence("ADULT_CBT", "At the end of the therapy programme, the CBT group showed significantly greater improvement on measures of knowledge about ADHD, self-efficacy, and self-esteem than the control group.", 5, "Supports specific CBT-related adult outcomes; it does not directly establish a generic symptom-severity effect."),
    "adult_cbt_guideline": evidence("CPG_REVIEW", "for adults, cognitive behavioral therapies.", 8, "Identifies CBT among recommended adult psychosocial interventions."),
    "stigma": evidence("STIGMA_SCALE", "The Surgeon General identifies stigma surrounding mental illness and its treatment as a potent barrier to help-seeking.", 1, "Supports a general help-seeking barrier; the study sample itself was adolescents aged 11-19."),
    "side_effects": evidence("NONMEDICAL_STIMULANT", "common side effects of the drugs include headache, stomach upset, nausea, loss of appetite, trouble sleeping, weight loss, dry mouth, nervousness, mood swings, dizziness, fast heart beat, and heart palpitations", 2, "Supports stimulant adverse effects, although the paper studies nonmedical college use rather than prescribed treatment at age 32."),
}

# edge_id: status, observation, recommendation, evidence keys
OVERRIDES = {
    1: ("partially_supported", "Adult and genetic reviews describe ADHD as highly heritable and persistent from childhood. The graph's generic liability claim is better supported than any specific variant mechanism.", "Retain the positive edge, define Genetic Risk as aggregate inherited liability, and avoid implying a known single variant.", ["genetic", "adult_course"]),
    2: ("not_assessable", "ADHD and Symptom Severity overlap unless ADHD is defined as a latent liability separate from diagnostic symptoms.", "Define separate latent and measured constructs before assigning a signed causal edge.", []),
    3: ("not_assessable", "Symptom Type is categorical and has no ordered scale, so a universal positive sign is undefined.", "Use subtype-specific outcomes or an unsigned relationship.", []),
    4: ("partially_supported", "The adult review reports frequent psychiatric comorbidity, but co-occurrence does not establish ADHD as its cause.", "Represent this as an association or specify a comorbid outcome and causal mechanism.", ["adult_comorbidity"]),
    5: ("partially_supported", "Young adults with lifetime ADHD may fall below full symptom criteria while retaining elevated symptoms. This is consistent with attenuation and persistence, but does not estimate an age-to-severity effect at 32.", "Retain a qualified developmental trajectory rather than a fixed negative linear edge.", ["age_persistence"]),
    6: ("not_assessable", "Sex differences and possible female underdiagnosis are documented, but Symptom Type is unordered and the proposed social-norm mechanism was not tested.", "Specify sex or gender and a particular symptom-presentation contrast.", ["female_detection"]),
    12: ("partially_supported", "The adult review links longstanding neuropsychological impairments with negative life outcomes and underachievement, but does not isolate a symptom-severity gradient.", "Retain as a clinically coherent pathway while labeling the causal magnitude unvalidated.", ["adult_outcomes"]),
    13: ("partially_supported", "Psychiatric comorbidity is common in adult ADHD, but the supplied evidence does not separately estimate its effect on functional impairment.", "Specify the comorbid condition and functional endpoint.", ["adult_comorbidity", "adult_outcomes"]),
    14: ("partially_supported", "The adult review describes underachievement and negative life outcomes, consistent with employment difficulty, but does not directly estimate employment instability caused by impairment.", "Retain only as a qualified occupational pathway and add employment-specific longitudinal evidence.", ["adult_outcomes"]),
    29: ("not_assessable", "Race / Ethnicity is categorical and Institutional Bias lacks an ordered scale, making a universal plus sign uninterpretable.", "Specify a population contrast and measured institutional outcome.", []),
    34: ("not_assessable", "Diagnosis Status is ambiguous between any diagnosis and accurate diagnosis, while Misdiagnosis Rate is an aggregate measure.", "Define accurate diagnosis as the outcome before assigning a negative effect.", []),
    36: ("partially_supported", "Stigma is described as a barrier to help-seeking, which can precede diagnosis, but the cited statement is general and the study sample was adolescent.", "Retain as a provisional help-seeking pathway and add direct adult ADHD diagnostic evidence.", ["stigma"]),
    37: ("partially_supported", "The corpus explicitly describes stigma as a barrier to help-seeking, but does not measure adult mental-health-care access at age 32.", "Retain a qualified negative pathway limited to help-seeking.", ["stigma"]),
    38: ("partially_supported", "Community data suggest females are underdiagnosed. This is compatible with gender-linked diagnostic error but does not identify stereotypes as the cause or quantify misdiagnosis.", "Replace the broad bias edge with a measured sex difference in detection or add mechanism-specific evidence.", ["female_detection"]),
    39: ("partially_supported", "Clinical guidelines recommend medication for adults with ADHD. A recommendation supports diagnosis-linked consideration, not an estimate that diagnosis causes medication uptake.", "Retain as a recommended care pathway, with clinical eligibility and preference modifiers.", ["adult_medication"]),
    40: ("partially_supported", "Adult CBT is recommended and adult outcome studies are discussed, supporting a diagnosis-linked therapy pathway without estimating uptake caused by diagnosis.", "Retain as a care pathway and specify CBT or skills-based treatment.", ["adult_cbt_guideline", "adult_cbt"]),
    50: ("partially_supported", "Medication is recommended for adults, but the supplied passages do not provide an age-32-specific controlled symptom effect.", "Retain the negative edge with a medication-specific adult efficacy source before assigning magnitude.", ["adult_medication"]),
    51: ("partially_supported", "Adult CBT produced improvements in knowledge, self-efficacy, and self-esteem, but that does not directly establish reduced core symptom severity.", "Specify the CBT program and measured outcome rather than a generic symptom reduction.", ["adult_cbt"]),
    52: ("partially_supported", "Adult CBT evidence reports improvements in therapy-relevant functioning, but the supplied excerpt does not establish a general reduction in functional impairment.", "Specify the functional endpoint and intervention.", ["adult_cbt", "adult_outcomes"]),
    54: ("not_assessable", "Adherence occurs after medication is prescribed; the explanation concerns benefit while the destination is Medication Treatment itself.", "Change the destination to treatment exposure or benefit and define adherence temporally.", []),
    55: ("not_assessable", "Participation may modify therapy dose or outcomes, but the destination is receipt of Behavioral Therapy rather than its effect.", "Model participation as a modifier of therapy exposure or outcome.", []),
    56: ("partially_supported", "Stigma is described as a help-seeking barrier, but treatment continuation among adults was not measured.", "Retain only as a broader engagement hypothesis unless adult adherence evidence is added.", ["stigma"]),
    57: ("partially_supported", "Stimulant medication guides list multiple adverse effects. The supporting paper concerns nonmedical college use, so it does not fully validate therapeutic treatment at age 32.", "Retain the positive edge, specifying drug, dose, and treatment context.", ["side_effects"]),
    58: ("insufficient_evidence", "The corpus documents adverse effects but does not show that they cause lower adherence in treated adults.", "Add direct discontinuation or adherence evidence.", ["side_effects"]),
    59: ("insufficient_evidence", "The corpus documents adverse effects but does not estimate their independent impact on adult quality of life.", "Add longitudinal evidence connecting adverse effects to quality of life.", ["side_effects"]),
    61: ("partially_supported", "The adult review connects longstanding neuropsychological impairment with negative life outcomes, but does not directly measure quality of life as the destination.", "Retain as a qualified pathway and add an adult quality-of-life measure.", ["adult_outcomes"]),
    62: ("insufficient_evidence", "No supplied study shows that receiving an adult diagnosis itself improves quality of life; any benefit would likely be mediated through effective care and support.", "Replace the direct edge with explicit treatment and support mediators.", []),
}

DEFAULT_OBSERVATION = "No supplied paper directly establishes this edge's direction, sign, and stated mechanism for adults around age 32. Pediatric or adjacent evidence is not transferred as adult causal proof."
DEFAULT_ACTION = "Retain only as an explicitly unvalidated hypothesis or add adult evidence with a defined exposure, outcome, and temporal direction."

def build_review(edges):
    rows = []
    for edge_id, (source, dest, sign, _strength, reasoning) in enumerate(edges, 1):
        status, observation, action, keys = OVERRIDES.get(edge_id, ("insufficient_evidence", DEFAULT_OBSERVATION, DEFAULT_ACTION, []))
        rows.append({"edge_id": edge_id, "source": source, "dest": dest, "existing_reasoning": reasoning, "sign": sign, "validation_status": status, "observation_from_validation": observation, "recommended_action": action, "evidence": [E[key] for key in keys]})
    return rows
