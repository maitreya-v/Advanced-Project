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
 19:("not_assessable","Diagnosis Status is ambiguous between any and accurate diagnosis, while Misdiagnosis Rate is aggregate.","Define accurate diagnosis as the outcome.",[]),
 20:("not_assessable","Race / Ethnicity and Institutional Bias are not ordered variables with a universal positive sign.","Specify a population contrast and measured institutional outcome.",[]),
 22:("not_assessable","Race / Ethnicity is categorical; a negative sign needs a named comparison and access measure.","Specify the population contrast and setting.",[]),
 38:("not_assessable","Adherence occurs after prescription; the explanation concerns effect while the destination is treatment itself.","Model adherence as a modifier of exposure or benefit.",[]),
}
DEFAULT_OBSERVATION="The four supplied papers study children or adolescents and do not establish this causal claim for adults around age 45. Pediatric findings are not transferred as midlife evidence."
DEFAULT_ACTION="Retain only as an explicitly unvalidated hypothesis or add directly relevant midlife adult evidence."

def build_review(edges):
    rows=[]
    for edge_id,(source,dest,sign,_strength,reasoning) in enumerate(edges,1):
        status,observation,action,keys=OVERRIDES.get(edge_id,("insufficient_evidence",DEFAULT_OBSERVATION,DEFAULT_ACTION,[]))
        rows.append({"edge_id":edge_id,"source":source,"dest":dest,"existing_reasoning":reasoning,"sign":sign,"validation_status":status,"observation_from_validation":observation,"recommended_action":action,"evidence":[E[k] for k in keys]})
    return rows
