"""Conservative full-text judgments for the 1990 graph."""
STATUS_DEFINITIONS = {
    "supported": "Evidence supports the stated direction, sign, and reasoning within the declared scope.",
    "partially_supported": "Evidence supports only part of the claim, a narrower population or outcome, or an association rather than the full causal claim.",
    "contradicted": "Relevant evidence opposes the claimed direction or sign within the declared scope.",
    "mixed_evidence": "Relevant evidence both supports and opposes the same defined claim.",
    "insufficient_evidence": "Available evidence does not establish or refute the causal claim.",
    "not_assessable": "Undefined variable coding or endpoint makes the proposed direction or sign uninterpretable.",
}
def evidence(source_id, excerpt, page, relevance):
    return {"source_id":source_id,"exact_excerpt":excerpt,"location":f"PDF page {page}","relevance":relevance}
E = {
 "age": evidence("AGE_EFFECT", "Results suggest that older children with ADD are significantly more likely than younger ADD children to experience academic and socioemotional difficulties.", 1, "Cross-sectional ages 6-12; supports an age association within childhood, not a longitudinal causal slope."),
 "age_detail": evidence("AGE_EFFECT", "there are increasing negative repercussions associated with ADD in some areas of academic and behavioral functioning.", 5, "Conclusion of the scanned age-effects study; generalizability was limited by exclusion of females."),
 "child_mph": evidence("CHILD_MPH", "Within-subjects analysis of covariance demonstrated significant correlations between the improvement in reaction time on the MFFT and i) GH response (AUCGH, r=.58, p<.001) and 2) prolactin response (AUCPro, r=.40, p<.05)", 1, "Ages 7.0-12.4 in a double-blind drug-placebo design; the outcome is reaction time, narrower than overall symptom severity."),
 "adolescent_mph": evidence("ADOLESCENT_MPH", "Methylphenidate significantly reduced teachers' and parents' ratings of hyperactivity, inattention, and oppositionality.", 1, "Controlled trial supports symptom reduction in ages 12-18, not specifically age eight or adults."),
 "side_effects": evidence("ADOLESCENT_MPH", "Stimulant treatment produced mild side effects and weight reduction.", 1, "Direct treatment adverse-effect evidence in adolescents."),
 "development": evidence("DEVELOPMENT", "The ADD + delinquent boys consistently fared the worst on the assessments of family adversity, verbal intelligence, and reading. Their antisocial behavior began before school age, escalated at school entry, and persisted into adolescence.", 2, "Longitudinal association in boys; does not isolate ADD or family adversity as a single causal exposure."),
}
OVERRIDES = {
 2:("not_assessable","ADHD and Symptom Severity overlap unless the disorder is defined separately from diagnostic symptoms.","Define separate latent and measured constructs.",[]),
 3:("not_assessable","Symptom Type is categorical, so a universal positive sign is undefined.","Use presentation-specific outcomes or an unsigned relation.",[]),
 4:("partially_supported","Children aged 8.6-12.11 showed poorer arithmetic discrepancy and more social withdrawal or uncommunicativeness than younger children, but the study was cross-sectional and did not validate general symptom severity.","Replace the generic positive edge with specific age-by-outcome relationships and note the cross-sectional design.",["age","age_detail"]),
 5:("not_assessable","The supplied studies do not test gender norms, and Symptom Type lacks an ordered scale; several samples included only boys.","Specify a presentation contrast and include evidence with girls.",[]),
 10:("partially_supported","The age-effects and developmental studies connect ADD with academic and socioemotional difficulty, but do not isolate symptom severity as the causal exposure.","Retain as a qualified clinical pathway and add a separately measured severity gradient.",["age","development"]),
 20:("partially_supported","Family adversity was greatest in boys with both ADD and delinquency, while ADD-only boys had normal family scores. This is subgroup association, not family stress causing symptom severity.","Do not generalize the combined subgroup finding to all ADHD; add temporal family-stress evidence.",["development"]),
 39:("partially_supported","Controlled trials enrolled diagnosed children or adolescents and administered methylphenidate, showing a clinical diagnosis-to-treatment pathway without estimating real-world treatment likelihood.","Retain as a care pathway rather than a quantified causal probability.",["child_mph","adolescent_mph"]),
 50:("partially_supported","Methylphenidate improved a reaction-time measure in ages 7-12 and reduced rated symptoms in adolescents. The age-eight and broad symptom-severity claim is only partly covered.","Retain the negative edge, specifying methylphenidate, measured outcome, and age range.",["child_mph","adolescent_mph"]),
 52:("not_assessable","Adherence occurs after medication is prescribed, while the destination is Medication Treatment and the explanation concerns benefit.","Change the destination to treatment exposure or benefit.",[]),
 54:("partially_supported","The adolescent trial directly reports mild side effects and weight reduction, but does not provide age-eight adverse-event evidence.","Retain with drug and adolescent age scope; add child-specific adverse-event evidence.",["side_effects"]),
}
DEFAULT_OBSERVATION="No supplied 1990 paper directly establishes this edge's direction, sign, and stated mechanism for children around age eight."
DEFAULT_ACTION="Retain only as an explicitly unvalidated hypothesis or add directly relevant pediatric evidence."

def build_review(edges):
    rows=[]
    for edge_id,(source,dest,sign,_strength,reasoning) in enumerate(edges,1):
        status,observation,action,keys=OVERRIDES.get(edge_id,("insufficient_evidence",DEFAULT_OBSERVATION,DEFAULT_ACTION,[]))
        rows.append({"edge_id":edge_id,"source":source,"dest":dest,"existing_reasoning":reasoning,"sign":sign,"validation_status":status,"observation_from_validation":observation,"recommended_action":action,"evidence":[E[k] for k in keys]})
    return rows
