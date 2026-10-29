"""Authored mechanism hypotheses and fictional illustrations, not edge validation."""

EXAMPLES = {
    "Education System Pressure|Teacher Referral Rate|+": (
        "Pressure to meet classroom performance or behavior expectations can make departures from those expectations more likely to trigger referral. This is a proposed institutional response, not proof that referred students have ADHD or that more referrals are always appropriate.",
        "A teacher working under strict behavior expectations refers a student whose interruptions repeatedly disrupt the lesson. The institutional threshold makes referral more likely than it would be in a less pressured setting.",
        "A school emphasizes rapid completion of classroom work. A student who repeatedly falls behind is referred for further attention, showing how expectations can influence which difficulties get escalated.",
    ),
    "Educational Access|Teacher Referral Rate|+": (
        "Access to schooling and relevant support creates opportunities for educators to notice persistent difficulties and arrange referral. The mechanism depends on staff capacity and appropriate procedures, not simply being enrolled.",
        "A child enters a setting where staff can observe learning across regular activities. Persistent difficulties that were previously unseen can now be raised for assessment.",
        "A school makes its referral process available to a family previously disconnected from support. A teacher's concern can reach the next service instead of stopping in the classroom.",
    ),
    "Parental Advocacy|Diagnosis Status|+": (
        "Following up on concerns, supplying relevant observations and navigating referrals can help a child reach a proper assessment. Advocacy can improve the opportunity for diagnosis; it should not determine what conclusion an assessment reaches.",
        "Mira's parent follows up on an unanswered referral and supplies examples from home and school. The assessment proceeds instead of being lost in an administrative gap.",
        "A parent helps arrange an evaluation after persistent concerns were left unresolved. The child's difficulties receive attention rather than remaining outside the assessment process.",
    ),
    "Parental Advocacy|School Support Plan|+": (
        "A parent who documents difficulties and follows up on requests can help a school turn concerns into an organized response. Advocacy supports the planning process, but a plan still depends on needs, procedures and resources.",
        "Mira's parent brings specific examples of unfinished classroom activities and follows up on the request for support. The school can organize a plan around a documented need instead of a vague concern.",
        "A family notices that agreed support has not been recorded and requests a clear written plan. Following up helps an informal intention become an organized response.",
    ),
    "Parental Awareness|Diagnosis Status|+": (
        "Recognizing a persistent difficulty can motivate a family to seek an appropriate evaluation. Awareness opens the assessment pathway without establishing what diagnosis, if any, the child should receive.",
        "Mira's family notices the same difficulty recurring across ordinary activities rather than treating each incident as unrelated. Recognizing the pattern prompts a request for assessment.",
        "A parent realizes that a child's ongoing struggles deserve evaluation rather than another reminder to try harder. Awareness changes whether an assessment is sought.",
    ),
    "Parental Awareness|Parental Advocacy|+": (
        "When a parent recognizes a child's needs, the concern can become a concrete request for support. Awareness may therefore lead to advocacy, although time, confidence and practical barriers affect whether action follows.",
        "Mira's parent notices a recurring problem with classroom instructions and requests a usable way to keep the steps visible. Recognition becomes an action directed at a specific need.",
        "A family understands that unfinished work reflects a persistent difficulty rather than lack of effort. They begin following up with the school instead of repeatedly blaming the child.",
    ),
    "Parental Denial|Parental Awareness|-": (
        "Dismissing persistent difficulties can prevent a parent from recognizing a pattern that needs attention. More denial can therefore reduce awareness of the child's needs, without establishing why the parent is reluctant to acknowledge them.",
        "A parent treats each repeated difficulty as an isolated bad day. The pattern remains unrecognized because the recurring evidence is repeatedly dismissed.",
        "A family insists that a child's struggles cannot reflect a genuine difficulty and disregards reports from school. Rejecting the information prevents a fuller understanding of the child's needs.",
    ),
    "Parental Education|Parental Awareness|+": (
        "Education may help a parent find, understand and evaluate information about a child's difficulties. That is a proposed information-access pathway, not a claim that less formally educated parents cannot recognize or care about their child's needs.",
        "A parent uses information-reading skills to distinguish a persistent pattern from an isolated incident. Better understanding makes the child's difficulty easier to recognize.",
        "A parent finds and interprets a clear explanation of the concerns raised at school. Access to usable knowledge supports awareness instead of leaving the concern unexplained.",
    ),
    "Parental Education|Parental Denial|-": (
        "Relevant knowledge can make a persistent difficulty easier to understand and reduce reliance on dismissive misconceptions. Formal education is only an imperfect proxy for that knowledge, so the mechanism should not become a judgment about families.",
        "A parent learns that a recurring difficulty is not simply a failure to try. Understanding an alternative explanation makes dismissing every incident less likely.",
        "Clear information challenges a family's mistaken belief that a child could stop every difficulty through willpower alone. The misconception loses influence as understanding improves.",
    ),
    "Peer Comparison|Parental Awareness|+": (
        "Seeing how a child manages activities compared with peers can make a persistent difficulty more noticeable. Comparison can prompt attention, but normal differences and different circumstances must not be mistaken for a diagnosis.",
        "During a shared activity, a parent notices that Mira repeatedly loses instructions that other children manage to follow. The contrast prompts closer attention to a recurring difficulty.",
        "A family observes an ongoing difference in completing familiar activities alongside peers. The comparison raises a concern to understand rather than proving that the child has a disorder.",
    ),
    "Provider Availability|Access to Mental Health Care|+": (
        "More usable provider capacity can reduce waiting and travel barriers. That makes obtaining an appointment more feasible, although affordability and service eligibility can still prevent access.",
        "A new assessment service offers appointments within reach of a family that previously faced a long wait. Available capacity changes whether care can actually be obtained.",
        "An adult can book locally after a provider begins accepting new patients. A service that existed only in principle becomes usable.",
    ),
    "Provider Availability|Treatment Access|+": (
        "Treatment requires providers with relevant capacity, not just a recognized need. More available treatment appointments can make starting or continuing care more feasible.",
        "A family has an agreed care need but cannot begin until a suitable provider has capacity. When an appointment becomes available, treatment becomes reachable.",
        "An adult can continue follow-up when an additional local provider begins offering the relevant service. Increased capacity removes a practical interruption to access.",
    ),
    "Provider Referral Pathway|Diagnosis Status|+": (
        "A usable referral pathway connects a concern with a service able to assess it. Clearer routing can increase completed evaluations and accurate recognition, without predetermining their conclusions.",
        "A worker's recurring difficulty is sent to the appropriate assessment service rather than passed between unrelated offices. The concern reaches a place where it can be evaluated.",
        "A family receives a clear referral with the information needed for booking. A previously stalled assessment request can now proceed.",
    ),
    "Provider Referral Pathway|Treatment Access|+": (
        "An effective referral connects someone with an appropriate treatment service and supplies the information needed to proceed. It can remove navigation barriers, though the receiving service must still have capacity.",
        "An adult receives a completed referral to a service that can meet the identified need. The next step is usable rather than an unexplained instruction to find help elsewhere.",
        "A provider sends the necessary care information with a family's referral. Treatment access is less likely to stall because of missing paperwork.",
    ),
    "School Labeling Bias|Teacher Referral Rate|+": (
        "If a school interprets visible behavior through a disciplinary label, it may escalate some children more often. This mechanism concerns biased referral practices, not a legitimate increase in clinical need or accurate recognition.",
        "A student's restlessness is repeatedly labeled defiance without examining the context. The label makes further disciplinary referral more likely.",
        "Similar classroom interruptions are treated more harshly after a child has acquired a negative reputation. The prior label influences escalation instead of the behavior being assessed fairly.",
    ),
    "School Resources|Teacher Referral Rate|+": (
        "Staff time, training and an available referral process can help teachers notice persistent difficulties and act on them. Better resources can increase appropriate referral opportunities, not prove that every referred child has ADHD.",
        "Mira's teacher has time to record recurring missed instructions and a clear way to raise the concern. What previously passed unnoticed becomes an assessment referral.",
        "A school provides trained support staff who help a teacher document persistent difficulties. The available process turns an observation into a usable referral rather than leaving it unresolved.",
    ),
    "School Support Plan|Learning Accommodations|+": (
        "A support plan can assign specific adjustments and responsibilities instead of leaving help as a general intention. Implementation turns the written plan into changes in the learning activity; paperwork alone is not enough.",
        "Mira's plan names a visible sequence of task instructions and who will provide it. The teacher puts that adjustment into the next classroom activity.",
        "A student's plan specifies a less distracting setting for demanding work. Because responsibility is assigned, the adjustment becomes part of the learning day rather than remaining an informal suggestion.",
    ),
    "Self-Diagnosis Behavior|Diagnosis Status|+": (
        "Recognizing a possible condition can motivate someone to seek formal evaluation. The positive pathway is through assessment-seeking, not self-identification automatically becoming a correct diagnosis.",
        "Arun recognizes a possible pattern in longstanding difficulties and arranges an assessment. Self-identification creates a reason to seek evaluation, whose conclusion remains open.",
        "Leena records concerns after considering ADHD as a possibility and brings them to an appropriate assessment. A personal suspicion becomes an evaluated question rather than a confirmed label.",
    ),
    "Self-Diagnosis Behavior|Treatment Access|+": (
        "Self-recognition may encourage someone to look for an assessment and care pathway. The mechanism depends on appropriate evaluation and service availability, not self-prescribing or bypassing assessment.",
        "An adult who recognizes a possible difficulty looks for a legitimate assessment service and learns the available care pathway. Self-recognition begins navigation rather than independent treatment.",
        "A person stops treating recurring difficulties as unrelated incidents and seeks professional help. That action creates an opportunity to reach appropriate care.",
    ),
    "Social Media Awareness|Parental Awareness|+": (
        "A relatable description can make a parent notice a recurring difficulty they had not previously recognized. The mechanism depends on accurate information; a familiar online story is not evidence of a child's diagnosis.",
        "A parent sees an accurate account of persistent attention difficulties and notices a similar pattern at home. The post prompts closer observation rather than a conclusion from a single resemblance.",
        "A family learns that quiet inattention can also deserve attention. Previously overlooked difficulties become something to understand instead of being dismissed because the child is not disruptive.",
    ),
    "Social Media Awareness|Self-Diagnosis Behavior|+": (
        "Recognizable online accounts can give someone a name for experiences they had not connected. That can increase self-identification, but misleading or overly broad content can also produce mistaken conclusions.",
        "Arun encounters an accurate account of persistent organizational difficulties and recognizes a possible pattern. The account prompts self-reflection rather than confirming ADHD.",
        "Leena sees a relatable description and begins considering whether recurring difficulties deserve assessment. Online recognition becomes a starting question, not clinical proof.",
    ),
    "Socioeconomic Status|Access to Mental Health Care|+": (
        "Resources associated with socioeconomic position can make fees, transport, time and navigation easier to manage. Those practical advantages can improve access, without implying that lower-resource families have less need or motivation.",
        "A family can arrange transport and time away from work for an assessment. Practical resources make attending possible where the same requirements would block another family.",
        "An adult has the time and support needed to navigate a complicated booking process. Those advantages make an available service easier to reach.",
    ),
    "Socioeconomic Status|Educational Access|+": (
        "Financial and social resources can affect access to schooling, transport and additional learning support. The proposed mechanism is unequal opportunity, not a difference in a child's worth or ability.",
        "A family can arrange transport to a setting with suitable learning support. Greater practical resources open an educational option that was otherwise out of reach.",
        "A student can attend additional support because the household can manage its cost and schedule. Access changes even though the student's underlying ability has not.",
    ),
    "Socioeconomic Status|Treatment Access|+": (
        "Money, time, transport and help navigating services can remove barriers to treatment. More resources can make care easier to reach, depending on how local services are organized and funded.",
        "A family can manage appointment fees and travel without losing essential income. Those resources make an agreed treatment option practically reachable.",
        "An adult has help arranging follow-up and time available to attend. Fewer logistical barriers make continuing care more feasible.",
    ),
    "Stigma|Access to Mental Health Care|-": (
        "Fear of judgment or shame can discourage someone from contacting or attending a service. Greater stigma can therefore reduce realized access even when appointments exist.",
        "A family avoids booking an available appointment because they fear how others will view seeking help. Social judgment becomes a barrier before the service is reached.",
        "An adult repeatedly postpones contacting care because asking for help feels shameful. The service is available, but stigma prevents its use.",
    ),
    "Stigma|Diagnosis Status|-": (
        "Fear of a label can discourage assessment or the disclosure needed for a fair evaluation. More stigma can therefore reduce opportunities for accurate recognition, rather than reduce the underlying condition.",
        "A family hides recurring concerns because they fear a diagnostic label. Without an assessment, the child's difficulties remain formally unrecognized.",
        "An adult avoids describing longstanding problems during an evaluation for fear of judgment. With less relevant information available, accurate recognition becomes harder.",
    ),
    "Stigma|Self-Diagnosis Behavior|-": (
        "Negative beliefs about a condition can make someone reject even considering it as a possible explanation. Greater stigma may suppress self-recognition and further help-seeking, without changing the underlying difficulties.",
        "Arun recognizes a familiar pattern but immediately dismisses it because the label feels shameful. The possibility is rejected before it can be explored appropriately.",
        "Leena avoids reading reliable information about a concern because of negative beliefs about the condition. Stigma keeps a possible explanation outside consideration.",
    ),
    "Stigma|Treatment Adherence|-": (
        "Fear of being judged for receiving care can make participation harder to maintain. Greater stigma may lead to hidden or missed parts of a plan, although people respond differently to social pressure.",
        "A fictional patient misses an agreed support activity to avoid being seen attending. Fear of others' judgment disrupts participation in the plan.",
        "An adult becomes reluctant to continue visible follow-up because of stigmatizing comments. The social pressure makes consistent participation harder rather than changing the treatment itself.",
    ),
    "Symptom Type|Teacher Referral Rate|+": (
        "Visible or disruptive difficulties may attract a teacher's attention more readily than quiet difficulties. This is a detection mechanism, not a meaningful numeric increase in symptom type or evidence that less visible needs are smaller.",
        "Mira quietly loses instructions, while another student repeatedly interrupts the lesson. The visible interruptions attract a referral first even though both patterns may deserve attention.",
        "A student frequently leaves a seat during shared work and the disruption is immediately noticed. A quieter student's persistent inattention takes longer to be raised for assessment.",
    ),
    "Teacher Referral Rate|Parental Awareness|+": (
        "A teacher can supply observations from school that a family does not see at home. More useful referrals can bring persistent difficulties to a parent's attention, although a referral is a concern to evaluate rather than a diagnosis.",
        "Mira's family sees the teacher's record of repeatedly missed classroom instructions. A pattern outside the home becomes visible to them for the first time.",
        "A teacher raises a recurring participation difficulty with a family who had noticed only occasional incidents. The additional observations help the family recognize a broader pattern.",
    ),
    "Telehealth Access|Access to Mental Health Care|+": (
        "Remote contact can reduce travel and location barriers to suitable services. It can expand practical care access when connectivity, privacy and an appropriate remote service are available.",
        "A family living far from a service can attend an appropriate appointment remotely. Removing the travel requirement makes contact feasible.",
        "An adult who cannot manage a long trip reaches a provider through a suitable remote appointment. Distance is no longer the barrier that stops the visit.",
    ),
    "Telehealth Access|Telehealth Treatment|+": (
        "The equipment, connection and service pathway needed for remote care make remote treatment possible. Access increases the opportunity to use that delivery method, not a guarantee that it suits every need.",
        "A family gains a usable private connection to an available remote service. Follow-up that could not be reached in person becomes possible online.",
        "An adult can join a suitable remote care program after the required connection and service access are arranged. The technical doorway makes the delivery option usable.",
    ),
    "Telehealth Treatment|Treatment Access|+": (
        "Providing suitable treatment remotely can reduce the need for travel and extend the reach of a service. Practical access may improve when remote delivery addresses an actual barrier and remains clinically appropriate.",
        "A remote program offers follow-up to a family who could not repeatedly travel to the provider. Delivering care differently removes the journey that prevented attendance.",
        "An adult can continue an appropriate treatment service after it begins remote delivery. A geographic barrier no longer interrupts access to that service.",
    ),
    "Treatment Access|Behavioral Therapy|+": (
        "Reaching an appropriate service creates the opportunity to start a behavioral intervention. Access removes a practical entry barrier, but does not decide which intervention is suitable or whether someone chooses it.",
        "A family can finally obtain a place in an appropriate behavioral support program. A treatment option they could not previously reach becomes available.",
        "An adult finds a service offering relevant behavioral skills support. Reaching that service opens participation rather than merely adding another name to a waiting list.",
    ),
    "Treatment Access|Digital Therapeutics|+": (
        "A usable care pathway may provide access to a specific evaluated digital intervention. Availability can increase uptake of that option, but ordinary apps are not interchangeable with evaluated treatments.",
        "A service gives a suitable fictional patient access to a defined digital program with appropriate guidance. The option becomes usable through the care pathway rather than through an unsupported app recommendation.",
        "A family can reach an evaluated digital intervention offered by their service. Access changes whether the program is an available option, not whether it is certain to help.",
    ),
    "Treatment Access|Medication Treatment|+": (
        "A reachable treatment service can assess suitability and provide medication treatment when appropriate. Access removes a barrier to that option; it does not imply that everyone who reaches care will receive medication.",
        "A fictional family can reach a qualified service that offers medication assessment and follow-up. Medication becomes a possible treatment option rather than an inaccessible service.",
        "An adult who could not obtain appropriate follow-up reaches a service able to manage medication care. Practical access opens the option without predetermining the treatment decision.",
    ),
    "Treatment Access|School Accommodations|+": (
        "An appropriate care pathway can document needs and connect relevant information with a school's support process. This indirect mechanism may help adjustments become available, but access to treatment alone does not create a school entitlement.",
        "A student's care service supplies relevant information about classroom needs to the school's support process. A previously unclear request for adjustments becomes easier to consider.",
        "A family reaches support that helps describe which learning activities are difficult. The school can use that information when considering practical accommodations.",
    ),
    "Treatment Access|Workplace Support|+": (
        "Care can help a person identify work-related needs and seek practical support through the relevant workplace process. This is a possible mediated pathway, not automatic disclosure, permission or a guaranteed workplace adjustment.",
        "An adult reaches care that helps clarify which work demands cause difficulty. The worker can make a more specific request for practical support if they choose to do so.",
        "A worker obtains relevant documentation through an appropriate care pathway and uses the workplace's support process. Access to care helps make a previously vague request concrete.",
    ),
    "Access to Mental Health Care|Care Coordination|+": (
        "Reaching services creates an opportunity for providers to share a plan and connect their roles. That can increase coordinated care, but only if the services actually communicate rather than working in isolation.",
        "After reaching a service, a family receives a shared plan instead of separate, disconnected instructions. The initial contact makes coordination possible.",
        "An adult enters a care service that connects assessment and follow-up teams. Information can move between them rather than leaving the person to rebuild the plan at every visit.",
    ),
    "Access to Mental Health Care|Diagnosis Status|+": (
        "Access makes an appropriate assessment possible rather than leaving difficulties unevaluated. More opportunity for evaluation can increase the likelihood of an accurate diagnosis, not the likelihood that every person assessed has ADHD.",
        "A family that could not reach an assessment service obtains an appointment. A persistent difficulty can now be evaluated instead of remaining unexplained.",
        "An adult finds a reachable service after repeatedly being unable to obtain an assessment. Access opens the opportunity for a formal explanation; it does not predetermine the result.",
    ),
    "Access to Mental Health Care|Treatment Access|+": (
        "A reachable service can assess needs and connect someone with available treatment options. General care access can therefore remove an entry barrier to treatment, although eligibility, cost and capacity may still limit the next step.",
        "A family reaches a service that can connect them with an appropriate treatment provider. Before that contact, they had no usable route into care.",
        "An adult finds a local service that offers follow-up rather than assessment alone. A previously disconnected treatment pathway becomes reachable.",
    ),
    "Care Coordination|School Support Plan|+": (
        "Sharing relevant observations and agreed actions can help a school turn separate concerns into an organized support plan. Coordination helps the plan reflect the student's needs instead of relying on disconnected accounts.",
        "Mira's school receives a clear summary of the needs already identified by the people supporting her. Staff can use the shared information to organize a consistent plan.",
        "A student's family and school align their accounts of which classroom tasks are difficult. The agreement gives a support plan a clearer practical focus.",
    ),
    "Care Coordination|Treatment Access|+": (
        "Clear handoffs and shared responsibilities can prevent a person from being lost between services. Fewer administrative gaps can make starting or continuing treatment more accessible.",
        "A service sends the next provider the information needed for an agreed referral. The family can proceed instead of repeating the process from the beginning.",
        "An adult receives a named follow-up contact before leaving an assessment service. A clear handoff removes uncertainty about where treatment can begin.",
    ),
    "Clinical Guidelines Evolution|Diagnosis Status|+": (
        "Clearer recognition and assessment guidance can help clinicians identify presentations that an earlier framework overlooked. This is a proposed knowledge-to-practice mechanism, not proof of a particular historical change in diagnosis rates.",
        "A clinician uses a framework that recognizes adult presentations rather than treating ADHD as only a childhood concern. An adult's longstanding difficulties are considered rather than dismissed because of age.",
        "An assessment framework draws attention to less disruptive presentations. A quiet person's persistent attention difficulties are evaluated instead of being overlooked.",
    ),
    "Clinical Guidelines Evolution|Treatment Access|+": (
        "Guidance that identifies appropriate treatment pathways can make referral and service planning clearer. Access may improve when that guidance is adopted and resourced; publishing recommendations alone does not create services.",
        "A service adopts a clearer pathway for adults who need treatment. People who previously received no next step now have an identifiable referral route.",
        "A provider follows an implemented care pathway that names available follow-up options. The person can reach a next service instead of stopping after assessment.",
    ),
    "Cost of Evaluation|Diagnosis Status|-": (
        "A more expensive evaluation can become harder to afford, leading people to postpone or forgo assessment. Fewer completed assessments can mean fewer accurate diagnoses, even when the underlying difficulties have not changed.",
        "A family wants an evaluation but cannot afford the quoted fee. The appointment is postponed, leaving the child's difficulties without a formal assessment.",
        "An adult saves for an assessment but faces a higher cost before booking. The added financial barrier delays the opportunity for diagnosis.",
    ),
    "Diagnosis Status|Behavioral Therapy|+": (
        "A recognized diagnosis can make needs clearer and connect a person with an appropriate behavioral intervention. The arrow concerns entry into a treatment pathway, not an automatic decision that everyone should receive the same therapy.",
        "After a formal assessment identifies ADHD, a family is connected with a behavioral support program. Recognition supplies a route to a service they had not previously reached.",
        "An adult's diagnosis helps a provider direct a referral toward relevant skills-based support. A defined need leads to a more specific treatment option.",
    ),
    "Diagnosis Status|Functional Impairment|-": (
        "Recognition may help someone obtain support that reduces practical barriers. This is a mediated pathway through what happens after diagnosis; a diagnostic label alone does not reduce impairment.",
        "After difficulties are formally recognized, a worker receives clearer written task instructions. The resulting support makes completing work easier; the label itself did not perform the task.",
        "A student's assessment leads to a more usable approach to classroom activities. Daily functioning improves in this fictional case because support changes, not simply because a report has been written.",
    ),
    "Diagnosis Status|Medication Treatment|+": (
        "A diagnosis can establish a basis for considering medication as one treatment option. It may therefore increase entry into medication treatment when appropriate, but it does not make medication necessary or inevitable.",
        "Following a formal assessment, a fictional family considers medication among the available options with a qualified clinician. The diagnosis opens that option rather than prescribing an outcome.",
        "An adult's assessment identifies a condition for which medication can be considered. A treatment option becomes relevant that was not previously part of a defined care plan.",
    ),
    "Diagnosis Status|Quality of Life|+": (
        "Recognition can help explain persistent difficulties and connect someone with useful support. Those changes may improve daily experience, but this is a mediated, context-dependent pathway rather than an effect of a label alone.",
        "A worker's difficulties are recognized and an appropriate support arrangement follows. More manageable days leave room for activities the worker values.",
        "A student receives a clearer explanation and useful support after assessment. In this fictional case, less repeated struggle makes participation in ordinary life more enjoyable.",
    ),
    "Diagnosis Status|School Accommodations|+": (
        "Formal recognition can document a student's needs and help a school consider appropriate adjustments. Whether accommodations follow depends on the school's process and available support, not diagnosis alone.",
        "Mira's assessment identifies persistent difficulties with task organization. Her school uses that documented need to consider a visible sequence of instructions.",
        "A student's difficulties are formally recognized instead of being treated as occasional carelessness. The school has a clearer basis for considering classroom adjustments.",
    ),
    "Diagnosis Status|School Support Plan|+": (
        "A documented diagnosis can help a school identify needs and organize a response. It can support the creation of a plan without guaranteeing eligibility, resources or a particular legal entitlement.",
        "Mira's school receives documentation explaining her persistent classroom difficulties. Staff use it to begin organizing a support plan around those needs.",
        "A student's recognized needs give the school a clearer starting point for planning support. An informal concern can become an organized set of agreed actions.",
    ),
    "Diagnosis Status|Treatment Access|+": (
        "A recognized diagnosis can give services a clearer basis for referral and treatment planning. It can remove an entry barrier, but waiting lists, affordability and available providers may still prevent access.",
        "A family's referral had stalled because the service required an assessment first. Once that requirement is met, the child can enter the treatment pathway rather than remain at the doorway.",
        "An adult receives a formal assessment that identifies the relevant care pathway. A previously unclear request can now be directed to an appropriate treatment service.",
    ),
    "Diagnostic Criteria Variability|Misdiagnosis Rate|+": (
        "Inconsistent criteria or inconsistent application can make similar presentations receive different interpretations. Greater inconsistency can increase opportunities for diagnostic error, though differences do not prove either individual decision is wrong.",
        "Similar difficulties are judged using incompatible assessment approaches. One assessment overlooks information the other requires, creating an opportunity for a mistaken conclusion.",
        "An adult's presentation is assessed without a consistent definition of which symptoms and impairment matter. Shifting standards make the conclusion less dependable.",
    ),
    "Employment Instability|Diagnosis Status|+": (
        "Recurring problems keeping work can make longstanding difficulties more visible and motivate assessment. Employment instability is a possible trigger for help-seeking, not evidence that job problems themselves prove ADHD.",
        "After recurring difficulties maintaining work, Arun seeks an assessment of problems that also occur elsewhere in life. The work disruption brings the need for evaluation into focus.",
        "Leena notices a repeated pattern across changing jobs and requests a broader assessment. Instability prompts evaluation rather than serving as the diagnosis itself.",
    ),
    "Employment Instability|Provider Referral Pathway|+": (
        "Work disruption can prompt a person or supporting service to seek an assessment referral. That creates a possible route into care, although many different causes of employment difficulty must be considered.",
        "A worker experiencing recurring job disruption asks a support service where to obtain an assessment. The practical problem activates a referral route.",
        "An adult's repeated employment difficulties are raised with a provider who arranges further evaluation. A visible work problem becomes a reason for referral, not proof of its cause.",
    ),
    "Family History Awareness|Self-Diagnosis Behavior|+": (
        "Knowing about similar difficulties in a family can make someone recognize a possible pattern in their own experience. It may encourage self-identification or help-seeking, but family history is not a personal diagnosis.",
        "Arun learns that a relative has ADHD and recognizes some familiar difficulties. That awareness prompts self-reflection rather than confirming the same diagnosis.",
        "Leena hears a family member describe longstanding attention problems. The resemblance makes Leena consider seeking an explanation for similar experiences.",
    ),
    "Financial Status|Access to Mental Health Care|+": (
        "More available financial resources can help cover fees, transport and time away from other responsibilities. Removing those practical barriers can make care more reachable, depending on how services are funded.",
        "A family can cover transport and an assessment fee that previously kept care out of reach. The same service becomes usable when the practical costs can be met.",
        "An adult can afford time away from paid work to attend an appointment. Greater financial room removes a barrier that had prevented attendance.",
    ),
    "Gender Bias|Misdiagnosis Rate|+": (
        "Gender stereotypes can cause an assessor to overlook relevant difficulties or interpret the same behavior differently. More reliance on stereotypes can increase diagnostic mistakes; gender itself is not the causal mechanism.",
        "An assessor expects ADHD to look only like obvious restlessness and overlooks a girl's persistent inattention. The stereotype, not her gender, creates the risk of a missed diagnosis.",
        "A person's difficulties are interpreted through assumptions about how someone of that gender should behave. Relevant evidence receives less attention, making an inaccurate conclusion more likely.",
    ),
    "Home Structure Stability|Family Stress|-": (
        "Predictable routines and dependable responsibilities can reduce uncertainty and repeated conflict about everyday tasks. Greater stability may therefore reduce family stress, without removing every source of strain.",
        "A family establishes a dependable sequence for the morning instead of renegotiating every task. Fewer last-minute disputes make the start of the day less stressful.",
        "People at home know who will handle each recurring responsibility. Less uncertainty reduces conflict over work that repeatedly went unfinished.",
    ),
    "Household Stability|Family Stress|-": (
        "A more dependable household situation can reduce recurring uncertainty about daily needs and responsibilities. That can lessen stress arising from instability, while other pressures may remain.",
        "A family no longer has to repeatedly change where everyday activities happen. The more settled arrangement removes a recurring source of worry.",
        "An adult's household responsibilities become dependable rather than changing unexpectedly. Less uncertainty makes ordinary days less strained.",
    ),
    "Household Stability|Nutrition Quality|+": (
        "A dependable household routine can make shopping, food storage and meal preparation easier to maintain. Those practical conditions can support more consistent access to varied meals, but do not determine what every family can afford or prefers.",
        "A family with a settled routine can plan shopping and prepare meals instead of repeatedly improvising around disruptions. More consistent preparation makes varied food easier to provide.",
        "An adult has dependable access to a kitchen and time to prepare food. That stability supports a more regular pattern of meals.",
    ),
    "Institutional Bias|Diagnosis Status|-": (
        "Discriminatory institutional practices can make assessment harder to obtain or make a person's concerns less likely to be taken seriously. In that defined context, greater bias can reduce fair and accurate recognition.",
        "A family's concerns are repeatedly dismissed through a biased institutional process. The child loses opportunities for an appropriate assessment.",
        "An adult encounters a gatekeeping practice that discounts their account without considering the relevant evidence. Access to a fair diagnostic assessment is reduced.",
    ),
    "Institutional Bias|Misdiagnosis Rate|+": (
        "Biased procedures can distort which information is collected or how it is interpreted. That distortion can increase missed or mistaken diagnoses rather than reflecting an inherent difference in the people affected.",
        "A service applies a stereotype instead of examining a person's symptoms and daily difficulties. Important information is missed, making the conclusion less reliable.",
        "A school-related concern is interpreted through a biased process before reaching assessment. The distorted account increases the chance that the real difficulty is misunderstood.",
    ),
    "Misdiagnosis Rate|Diagnosis Status|-": (
        "If Diagnosis Status means accurate ADHD recognition, a wrong or missed explanation can delay that recognition. The negative sign is not meaningful if the target instead counts every recorded diagnosis regardless of accuracy.",
        "A fictional student's persistent difficulties are incorrectly attributed to a different explanation. Appropriate ADHD recognition is delayed because the original interpretation sends assessment in the wrong direction.",
        "An adult receives an incomplete explanation that overlooks relevant ADHD evidence. The mistake leaves the actual difficulty unrecognized rather than accurately diagnosed.",
    ),
    "Neighborhood Quality|Access to Mental Health Care|+": (
        "Here neighborhood quality must mean relevant resources such as nearby services and usable transport. Better local infrastructure can reduce the practical effort needed to reach care; the label alone does not identify which resource matters.",
        "A family lives near a reachable assessment service with usable transport. Attending is possible without the travel barrier faced in a less connected area.",
        "An adult gains a practical route to a nearby provider when local transport improves. Better connection to services makes an appointment easier to attend.",
    ),
    "Online Health Information|Diagnosis Status|+": (
        "Accurate and understandable information can help someone recognize a concern and find an appropriate assessment route. Any diagnosis still depends on evaluation, and misleading information may have the opposite effect.",
        "Arun reads a reliable description of persistent attention difficulties and learns where assessment is available. The information helps turn an unexplained concern into a request for evaluation.",
        "A family finds dependable information explaining when a concern deserves professional assessment. They seek evaluation instead of assuming that reading the page establishes a diagnosis.",
    ),
    "Online Health Information|Self-Diagnosis Behavior|+": (
        "Descriptions of recognizable experiences can lead someone to identify with a possible condition. More exposure may increase self-identification, but accuracy depends on the information and self-identification is not clinical confirmation.",
        "Leena encounters a description of attention difficulties that resembles everyday experience. Leena begins considering ADHD as a possibility rather than treating it as a settled conclusion.",
        "Arun learns a name for a pattern that previously felt unexplained. The information encourages self-recognition and further questions, not a diagnosis from the screen.",
    ),
    "Online Health Information|Treatment Adherence|+": (
        "Clear information about an agreed treatment plan can reduce confusion about its purpose and practical steps. Better understanding may support participation, provided the information is reliable and consistent with professional guidance.",
        "An adult uses reliable information to understand an agreed practice routine. Knowing what each activity is for makes the routine easier to follow consistently.",
        "A family reads clear instructions supplied by the treating service and resolves confusion about follow-up. Fewer misunderstood steps mean fewer missed parts of the plan.",
    ),
    "Genetic Risk|ADHD|+": (
        "Inherited genetic variants can influence brain development and systems involved in attention and impulse regulation. Greater genetic susceptibility can therefore increase the likelihood of ADHD, without determining whether a particular person develops it.",
        "{name} is born with higher inherited susceptibility to ADHD. As everyday demands increase, persistent attention and impulse-control difficulties become noticeable; the inherited susceptibility is a possible contributor, not a certain outcome.",
        "{other} and a sibling grow up in the same household but inherit different combinations of genetic variants. In this fictional example, greater ADHD susceptibility helps explain why one develops persistent difficulties while the other does not.",
    ),
    "ADHD|Symptom Severity|+": (
        "Here ADHD must mean the underlying condition, not the act of receiving a diagnosis. Difficulties regulating attention and impulses are expressed as symptoms; a greater underlying burden can mean more frequent or disruptive symptoms, although this is partly a description of the condition rather than an independent causal mechanism.",
        "{name} wants to follow a {task}, but attention repeatedly shifts before the instructions are complete. This example makes the underlying attention-regulation difficulty visible as persistent symptoms, rather than suggesting that a diagnostic label created them.",
        "During a group activity, {other} repeatedly speaks before others finish despite trying to wait. The difficulty regulating impulses appears as a more frequent symptom, not a deliberate decision to be disruptive.",
    ),
    "ADHD|Symptom Type|+": (
        "ADHD can involve different patterns of inattention, hyperactivity and impulsivity. This arrow describes how an underlying condition is expressed, not a numeric claim that more ADHD produces more of a particular symptom type.",
        "{name} remains quiet during a {task} but repeatedly loses the instructions. The difficulty is visible mainly as inattention, even without obvious restlessness.",
        "{other} often leaves a seat and answers before a turn arrives. This fictional presentation makes hyperactivity and impulsivity more noticeable than quiet distraction.",
    ),
    "ADHD|Executive Function Deficit|+": (
        "ADHD-related difficulties can affect planning, working memory and self-regulation. When those processes are harder to manage, keeping a goal in mind and organizing the steps toward it can also become harder; this does not describe everyone with ADHD.",
        "{name} begins a {task} with a clear goal but loses track of which step comes next. The difficulty is not a missing idea; it is keeping the plan active while working.",
        "{other} gathers everything needed for a project but struggles to decide what to do first. A planning difficulty turns a familiar goal into an unorganized collection of steps.",
    ),
    "Symptom Severity|Functional Impairment|+": (
        "More frequent attention or impulse-control difficulties can interrupt following instructions, organizing work and completing activities. The symptom becomes functional impairment when it prevents someone from doing something they need or want to do.",
        "{name} understands the {task}, but repeatedly loses a place in the instructions and starts again. By the deadline the work is unfinished, so an attention difficulty has become a practical obstacle.",
        "{other} keeps interrupting during a group activity and misses the agreed next step. The group cannot finish the shared task smoothly, showing how a symptom can affect participation rather than just appear on a checklist.",
    ),
    "Executive Function Deficit|Functional Impairment|+": (
        "Difficulties planning, remembering steps and switching between tasks can make ordinary responsibilities harder to complete. The effect concerns daily functioning, not intelligence or willingness to try.",
        "{name} knows what a project needs, but cannot organize the steps before its deadline. The planning difficulty leaves an important responsibility unfinished.",
        "{other} intends to bring the right materials but loses track of the preparation list. Arriving without them prevents participation in an activity that was otherwise within reach.",
    ),
    "Functional Impairment|Quality of Life|-": (
        "When daily activities become harder to complete, they can take time and energy away from relationships, enjoyment and independence. Greater disruption can therefore reduce quality of life, although support and other circumstances can soften that effect.",
        "An unfinished {task} follows {name} into the evening. While friends {social_activity}, {name} stays behind to catch up; the cost is missing something personally meaningful, not just unfinished work.",
        "{other} repeatedly struggles to organize the day and cancels a long-awaited outing to deal with overdue responsibilities. The practical difficulty narrows opportunities for enjoyment and connection.",
    ),
    "Functional Impairment|Employment Instability|+": (
        "Repeated difficulty meeting deadlines, organizing work or maintaining attendance can put employment under strain. This is a proposed route through job demands and workplace responses, not a claim that impairment inevitably causes job loss.",
        "A worker understands the job but repeatedly misses delivery dates because tasks remain unorganized. The employer begins questioning whether the role can continue unchanged.",
        "An employee loses track of changing shifts and misses scheduled work. Recurring attendance problems make keeping the position less secure, even though the employee wants to stay.",
    ),
    "Medication Treatment|Symptom Severity|-": (
        "An effective ADHD medication can support attention and impulse regulation, making some symptoms less frequent or disruptive. Responses vary, so treatment availability or use alone does not guarantee improvement.",
        "In a fictional example of an effective, professionally supervised medication plan, {name} loses the instructions less often during a {task}. More sustained attention means fewer interruptions to the activity.",
        "For {other}, an effective medication plan makes it easier to pause before interrupting a group activity. The reduced frequency of impulsive interruptions illustrates symptom reduction, not a result everyone should expect.",
    ),
    "Medication Treatment|Functional Impairment|-": (
        "If medication reduces difficulties that interfere with an activity, completing that activity may become easier. This is a mediated pathway through symptom management and task demands, not a claim that medication automatically repairs every area of daily life.",
        "With an effective, professionally supervised medication plan, {name} loses a place in a {task} less often. In this fictional case, fewer restarts make finishing the work more manageable.",
        "An adult whose medication plan helps with attention can follow the steps of a work task more consistently. Fewer missed steps reduce a practical difficulty, while other work challenges remain.",
    ),
    "Medication Treatment|Treatment Side Effects|+": (
        "Medication exposure can also bring unwanted effects, such as appetite or sleep difficulties. This positive arrow concerns the possibility of adverse effects alongside treatment; it does not mean every medication user experiences them or that benefit and harm rise proportionally.",
        "In a fictional treatment course, {name} notices a reduced appetite after starting prescribed medication. The new difficulty illustrates a possible unwanted effect, not a reason to change treatment without professional advice.",
        "{other} finds falling asleep more difficult during a medication trial and reports it to the treating clinician. The added sleep difficulty illustrates why tolerability matters as well as intended benefit.",
    ),
    "Behavioral Therapy|Symptom Severity|-": (
        "Behavioral approaches can build routines, practice self-regulation and change the responses surrounding a behavior. Effective strategies may make some disruptive behaviors less frequent, without implying a cure or the same response in every setting.",
        "{name} practices waiting for a cue before speaking during a structured activity. With consistent practice and feedback, interruptions become less frequent in this fictional situation.",
        "{other} learns a short routine for returning to a task after distraction. Repeated practice makes wandering away from the activity less frequent, illustrating one possible benefit rather than a universal result.",
    ),
    "Behavioral Therapy|Functional Impairment|-": (
        "Practical routines and behavioral strategies can make it easier to begin, organize and finish daily activities. Functioning may improve even when some underlying symptoms remain.",
        "{name} uses a practiced routine to divide a {task} into manageable steps. The work gets completed with fewer abandoned starts, even though distraction has not disappeared.",
        "{other} practices preparing materials at a consistent point in the day. Arriving ready for the next activity removes a recurring practical obstacle.",
    ),
    "Sleep Quality|Symptom Severity|-": (
        "Better sleep can support attention and self-regulation, while insufficient or disrupted sleep can add difficulties in those areas. The negative sign assumes that a higher Sleep Quality value means better sleep, not more sleep problems.",
        "After a poorly rested night, {name} repeatedly loses the instructions during a {task}. Following a more restful night, the same activity is easier to stay with in this fictional comparison.",
        "{other} has a run of disrupted nights and becomes more distractible during group activities. When sleep becomes more settled, that added difficulty is less noticeable; the example does not suggest sleep alone explains ADHD.",
    ),
    "Sleep Quality|Executive Function Deficit|-": (
        "Restful sleep can help sustain the attention and working memory needed to plan and keep track of tasks. Better sleep may therefore reduce sleep-related executive difficulties, without eliminating every underlying difficulty.",
        "After fragmented sleep, {name} repeatedly forgets the next step in a familiar {task}. A well-rested day makes holding that sequence in mind easier in this hypothetical comparison.",
        "{other} struggles to organize a busy morning after a restless night. With more settled sleep, planning the same responsibilities requires less effort.",
    ),
    "Family Stress|Sleep Quality|-": (
        "Worry, conflict or unpredictable routines can make settling down and staying asleep harder. More family stress can therefore reduce sleep quality, although sleep problems can also increase stress in the other direction.",
        "An unsettled evening at home leaves {name} worrying after bedtime. Sleep is interrupted by repeated waking rather than becoming a period of rest.",
        "Changes in family routines keep {other} unsure when the evening will end. The uncertainty makes winding down harder and sleep less settled.",
    ),
    "Family Stress|Symptom Severity|+": (
        "Family stress can add competing worries and make self-regulation more demanding. Existing attention or impulse-control difficulties may become more noticeable under that extra load; this is not a claim that families cause ADHD.",
        "During a tense week at home, {name} keeps returning to worries while attempting a {task}. More missed instructions make existing attention difficulties more visible.",
        "{other} arrives at a group activity already upset by conflict at home. Waiting and managing frustration become harder, so impulsive interruptions are more frequent in this fictional situation.",
    ),
    "Family Stress|Chronic Stress Load|+": (
        "Repeated family difficulties can keep a person under strain rather than allowing time to recover between stressful events. Persistent stressors can therefore add to accumulated stress burden.",
        "Arguments and unpredictable responsibilities recur at home for {name}. Each new difficulty arrives before the earlier strain has settled, so stress becomes ongoing rather than occasional.",
        "An adult repeatedly manages family emergencies alongside ordinary responsibilities. The lack of recovery time adds to an already sustained stress burden.",
    ),
    "Chronic Stress Load|Symptom Severity|+": (
        "Sustained stress can compete for attention and make emotional and impulse regulation more demanding. That added burden may amplify existing symptoms rather than create a new diagnosis by itself.",
        "{name} begins a {task} while still preoccupied by ongoing worries. Attention keeps returning to those worries, so instructions are missed more often.",
        "An adult facing prolonged strain finds it harder to pause before reacting to interruptions at work. Existing regulation difficulties become more noticeable under the additional load.",
    ),
    "Chronic Stress Load|Functional Impairment|+": (
        "Sustained strain can leave less attention and energy available for ordinary responsibilities. When that burden repeatedly disrupts activities, practical impairment can increase.",
        "Ongoing worries leave {name} unable to finish a familiar {task} on time. The stress burden has begun interfering with completion, not just changing how the day feels.",
        "An adult managing persistent strain repeatedly postpones essential paperwork. Missed deadlines turn the continuing burden into a practical problem.",
    ),
    "Comorbid Conditions|Functional Impairment|+": (
        "Additional health difficulties can place extra demands on the same activities already affected by ADHD. Their combined burden may make functioning harder, although different conditions interact differently.",
        "{name} struggles with distraction and also has a separate difficulty that interrupts the {task}. Managing both obstacles makes completing the activity harder than managing either alone.",
        "An adult already finding organization difficult must also manage another ongoing health problem. The added appointments and demands make maintaining daily routines more difficult.",
    ),
    "Comorbid Conditions|Misdiagnosis Rate|+": (
        "Overlapping symptoms can make it harder to distinguish ADHD from another condition or recognize both together. If assessment focuses on only one explanation, diagnostic mistakes may become more likely.",
        "{name}'s attention difficulties occur alongside another health concern. If every difficulty is attributed to that concern, ADHD may be overlooked in this fictional assessment.",
        "An adult has distractibility alongside a separate condition with overlapping symptoms. Treating the overlap as proof of only one diagnosis can lead to an incomplete or mistaken explanation.",
    ),
    "Treatment Side Effects|Treatment Adherence|-": (
        "Unwanted treatment effects can make a plan harder or less acceptable to continue. Greater tolerability problems can therefore reduce consistent participation, although an appropriate review may help address them.",
        "A fictional patient finds an unwanted effect increasingly difficult to tolerate and begins missing the agreed treatment routine. The example shows how discomfort can undermine consistency, not advice to change a plan independently.",
        "An adult becomes reluctant to follow a treatment schedule after repeated unwanted effects. The disruption illustrates a barrier to continuing the plan and a reason to discuss concerns with the treating professional.",
    ),
    "Treatment Side Effects|Quality of Life|-": (
        "Unwanted effects can interfere with comfort, enjoyment or ordinary activities. Greater adverse-effect burden can therefore reduce quality of life, even when treatment also has intended benefits.",
        "An unwanted effect makes {name} uncomfortable during a favorite activity. The activity becomes less enjoyable, illustrating a cost distinct from the treatment's intended purpose.",
        "A fictional adult finds an unwanted treatment effect interrupting time with friends. The lost enjoyment shows why quality of life includes tolerability as well as symptom change.",
    ),
    "Digital Therapeutics|Symptom Severity|-": (
        "A specific digital intervention may train attention or provide structured practice that helps a particular symptom-related skill. Evidence for one product or outcome does not establish the same effect for every app or all ADHD symptoms.",
        "{name} completes structured attention practice with an evaluated digital intervention. In this hypothetical case, staying with the practiced activity becomes easier; an ordinary entertainment app is not assumed to do the same.",
        "{other} uses a defined digital program with repeated goal-directed practice. Improvement appears in the practiced attention task, without assuming that every difficulty across daily life has changed.",
    ),
    "Digital Therapeutics|Treatment Adherence|+": (
        "A digital program can make agreed activities easier to remember, schedule or record. If those features reduce practical barriers, participation may become more consistent; access to an app alone is not enough.",
        "{name} uses an agreed program that makes each practice activity easy to find. Fewer forgotten sessions make following the plan more consistent.",
        "An adult uses a digital record to see which agreed activities remain unfinished. The visible routine helps maintain participation instead of relying entirely on memory.",
    ),
    "Care Coordination|Functional Impairment|-": (
        "Coordinated support can reduce conflicting instructions and gaps between the people helping with daily difficulties. A more usable plan can remove practical obstacles, rather than assuming coordination itself changes the underlying condition.",
        "The people supporting {name} agree on the same approach to a difficult {task}. Consistent instructions remove a recurring obstacle created by competing plans.",
        "An adult's support providers share a clear plan instead of giving incompatible next steps. Less time resolving contradictions leaves the person better able to manage ordinary responsibilities.",
    ),
    "Learning Accommodations|Functional Impairment|-": (
        "Adjusting task presentation or the learning environment can reduce the mismatch between a learner's difficulties and an activity's demands. The person may function better without every symptom having to disappear.",
        "Mira receives instructions broken into visible steps rather than having to remember the whole sequence. She can return to the next step after distraction, reducing a practical barrier to finishing.",
        "A student completes a task in a less distracting setting. With fewer competing interruptions, participating in the same learning activity becomes more manageable.",
    ),
    "School Accommodations|Functional Impairment|-": (
        "School adjustments can remove avoidable barriers in how work is presented, organized or completed. Better fit between the task and the student's needs can reduce school-related impairment without being a cure.",
        "A student follows a visible checklist during independent work. The external sequence makes a task manageable even when remembering every step remains difficult.",
        "Mira uses a quieter place for a demanding assignment. Reducing competing interruptions makes completing that activity easier in this fictional example.",
    ),
    "Workplace Accommodations|Functional Impairment|-": (
        "Changes to work instructions, scheduling or the environment can reduce barriers created by a person's difficulties. Functioning can improve because the work fits the person's needs better, not because the underlying condition has vanished.",
        "Arun receives written priorities instead of several changing verbal requests. Keeping the next task visible makes completing work more manageable.",
        "Leena uses a quieter workspace for concentration-heavy work. Fewer competing interruptions reduce a recurring practical obstacle.",
    ),
    "Workplace Support|Functional Impairment|-": (
        "Practical help and clearer expectations can reduce the demands a person must manage without support. That change can lessen work-related impairment while leaving some symptoms unchanged.",
        "Arun and a supervisor agree on clear task priorities. Less time sorting conflicting demands means fewer important tasks are left unfinished.",
        "A worker receives a dependable way to check the next step in a complicated assignment. The available support prevents a small organizational difficulty from repeatedly stopping the work.",
    ),
    "Remote Work Flexibility|Functional Impairment|-": (
        "Flexibility can let a worker arrange tasks and surroundings to reduce a mismatch with their needs. It may reduce some work barriers, although remote work can also introduce distractions and is not helpful for everyone.",
        "Arun schedules concentration-heavy work during a quieter part of the day. Greater control over the setting makes that task easier to complete.",
        "Leena can alternate demanding work with planned breaks instead of following an inflexible sequence. The better fit makes daily responsibilities more manageable in this hypothetical case.",
    ),
    "Performance Pressure|Functional Impairment|+": (
        "Tighter deadlines or more competing demands can expose a gap between available capacity and what an activity requires. Under greater pressure, an existing difficulty may cause more disruption even without a change in the underlying condition.",
        "Arun manages a familiar workload but struggles when several urgent deadlines overlap. The same planning difficulty now leaves more tasks unfinished.",
        "Leena completes an ordinary task reliably until repeated last-minute changes are added. The increased demand turns a manageable difficulty into a practical obstacle.",
    ),
}

EXAMPLES.update({
    "Early Life Nutrition|Genetic Risk|-": (
        "This example follows the source's developmental-vulnerability interpretation of the arrow, not a change in inherited DNA. Adequate early nutrition is imagined as avoiding an added nutrition-related developmental burden while genetic susceptibility stays unchanged.",
        "{name} is assumed to have inherited ADHD susceptibility. In this hypothetical example, adequate early nourishment avoids adding a nutrition-related developmental difficulty; the inherited susceptibility itself does not change.",
        "{other} has the same assumed inherited susceptibility across two imagined childhood situations. A nutrition-related deficiency adds a developmental challenge in one situation, while adequate nourishment avoids that extra challenge in the other.",
    ),
    "Age|Symptom Severity|+": (
        "The positive sign is illustrated through increasing demands at a life stage, which can make an existing difficulty more noticeable. It does not mean that every symptom biologically increases with age.",
        "A child manages a loosely structured activity but struggles when growing older brings longer classroom tasks. The added demand makes existing attention difficulties more visible.",
        "An adult takes on more competing responsibilities at a later life stage. Persistent attention difficulties become more disruptive under that workload, rather than age itself creating ADHD.",
    ),
    "Age|Symptom Severity|-": (
        "This example follows the source's interpretation that overt restlessness can become less visible as someone grows older. Other attention difficulties may remain, so the story does not imply that aging removes ADHD.",
        "A child who often leaves a seat later experiences restlessness more internally. Visible movement becomes less frequent in this fictional account while attention difficulties remain.",
        "An adult looks back on being constantly in motion as a child but now shows less obvious hyperactivity. Planning and concentration can still be difficult despite the quieter presentation.",
    ),
    "Age|Functional Impairment|+": (
        "The source's proposed pathway is accumulated difficulties meeting growing responsibilities over time. The example attributes the added impairment to that burden, not to age alone.",
        "Arun's unresolved organizational difficulties become harder to manage as work and household responsibilities accumulate. More commitments are missed even though the original difficulty is familiar.",
        "Leena could manage an earlier routine but struggles when later responsibilities require coordinating more activities. The larger practical burden exposes difficulties that used to be manageable.",
    ),
    "ADHD|Comorbid Conditions|+": (
        "This arrow is illustrated as additional difficulties occurring alongside ADHD, not proof that ADHD directly causes a second disorder. The example makes the combined burden visible while leaving the reason for co-occurrence open.",
        "{name} has persistent attention difficulties and also experiences a separate ongoing health concern. Both affect the same day, illustrating co-occurrence rather than establishing that one caused the other.",
        "An adult managing ADHD also has an independently identified difficulty. The additional concern complicates daily life without being treated as an inevitable consequence of ADHD.",
    ),
    "Gender|Symptom Type|+": (
        "The source's example concerns which presentations people notice through gender expectations, rather than an increase in a numeric gender variable. Those expectations can shape descriptions of symptoms without proving a biological cause.",
        "A quiet student's repeated inattention is described as daydreaming, while another student's visible restlessness attracts attention. Expectations influence the presentation observers record, not the child's underlying worth or ability.",
        "An observer expects a particular gender to be disruptive and notices movement more readily than quiet missed instructions. The resulting description reflects selective attention to symptom presentation.",
    ),
    "Gender Bias|Diagnosis Status|+": (
        "The positive direction is illustrated for a group favored by an assessor's stereotype of ADHD. Greater attention to that group's difficulties can increase recorded recognition while disadvantaging people who do not fit the stereotype.",
        "An assessor expects ADHD to look like a restless boy and sends a matching presentation for assessment sooner. The stereotype increases recognition in that favored case rather than making the process fairer.",
        "A provider takes one person's concerns more seriously because the presentation matches a gender expectation. That person reaches diagnostic assessment while an equally relevant concern elsewhere is overlooked.",
    ),
    "Race / Ethnicity|Access to Mental Health Care|-": (
        "This example interprets the arrow through discriminatory processes and structural barriers affecting a group, not an inherent biological effect of identity. Those barriers can make the same service harder to reach.",
        "A family encounters discriminatory gatekeeping when requesting an available appointment. The institutional barrier reduces their access; their identity does not create a lower need for care.",
        "A person's community has fewer reachable services because of unequal resource distribution. The resulting travel barrier illustrates reduced access through social conditions rather than biology.",
    ),
    "Race / Ethnicity|Institutional Bias|+": (
        "The illustrated mechanism is an institution treating a perceived group identity unfairly. The arrow refers to exposure to biased practices, not identity itself generating prejudice or being an increasing numeric cause.",
        "An institution applies a stereotype to a family's concerns instead of considering the relevant information. Their perceived identity changes how the institution responds.",
        "A person encounters a different gatekeeping standard because staff make assumptions about their ethnic background. The extra biased treatment comes from the institution's practice.",
    ),
    "Institutional Bias|Teacher Referral Rate|+": (
        "The positive direction is illustrated as over-referral of a targeted group through biased disciplinary expectations. It does not imply that bias increases every kind of referral or identifies genuine clinical need.",
        "A school interprets a targeted student's restlessness more harshly than similar behavior elsewhere. The biased interpretation makes disciplinary escalation more frequent.",
        "A negative institutional expectation causes ordinary classroom incidents involving one group to be recorded and referred more often. The increased referral reflects unequal treatment rather than greater underlying need.",
    ),
    "Classroom Size|Teacher Referral Rate|+": (
        "The source's positive pathway is illustrated through classroom-management pressure making visible disruption more likely to trigger referral. This scenario does not establish that larger classes always improve detection.",
        "A teacher managing a crowded room has little capacity to resolve a recurring disruption during the lesson. The difficulty is escalated through a referral rather than handled within the activity.",
        "In a large class, repeated interruptions affect many simultaneous tasks. A teacher raises the disruptive pattern for further attention because its classroom impact has become harder to manage.",
    ),
    "Cultural Norms|Stigma|+": (
        "For this illustration, the relevant norms are beliefs that shame people for seeking mental health support. Stronger endorsement of those particular beliefs can increase stigma; not all cultural norms have that effect.",
        "A child repeatedly hears that asking for mental health support is a personal weakness. The belief makes seeking help feel shameful rather than ordinary.",
        "An adult's social circle mocks people who receive care. Repeated exposure to that norm adds fear of judgment around getting support.",
    ),
    "Overdiagnosis Pressure|Diagnosis Status|+": (
        "Here the example interprets pressure as pushing toward a recorded diagnosis, rather than concern about excessive diagnosis. A lower threshold for assigning a label can increase recorded diagnoses without establishing their accuracy.",
        "A service is pressured to assign a label quickly before gathering a complete account. A diagnosis is recorded sooner, but the shortcut does not make it accurate.",
        "A persistent demand for a particular explanation influences an assessment process. More labels are recorded under that pressure rather than because the evidence has become stronger.",
    ),
    "Treatment Dependency|Treatment Access|+": (
        "This illustration interprets dependency as needing continuing care, not addiction. Recognizing an ongoing need can motivate arranging follow-up and seeking a usable treatment pathway.",
        "An adult who needs continuing support arranges follow-up before the current care period ends. The ongoing need prompts active navigation toward the next service.",
        "A family recognizes that support will be needed beyond an initial appointment and seeks an available continuing-care program. The recognized need becomes a reason to obtain access.",
    ),
    "Treatment Dependency|Functional Impairment|-": (
        "The source's example concerns effective ongoing support reducing practical difficulty, not dependency itself being beneficial. Here dependency means relying on that support to maintain functioning, rather than addiction.",
        "An adult relies on an effective support routine to organize daily work. Continuing that support makes responsibilities more manageable than trying to manage without it.",
        "A student's usable support plan remains in place across learning activities. The continuing help removes recurring practical barriers even though underlying difficulties remain.",
    ),
    "Treatment Adherence|Medication Treatment|+": (
        "The target is illustrated as receiving medication treatment consistently according to an agreed plan, not increasing the dose. Fewer missed parts of the plan can mean more consistent treatment exposure.",
        "An adult follows the professionally agreed medication routine more consistently instead of repeatedly forgetting it. Treatment exposure becomes more regular without any independent dose change.",
        "A fictional patient's agreed care routine becomes easier to remember with an organized schedule. Fewer missed steps make medication treatment more consistent rather than stronger in amount.",
    ),
    "Treatment Adherence|Behavioral Therapy|+": (
        "The arrow is illustrated as consistent participation in behavioral treatment, including agreed practice. Following the plan more regularly creates more opportunities to use the intervention, without guaranteeing its effectiveness.",
        "A student regularly practices an agreed pause-before-speaking routine instead of using it only occasionally. More consistent participation gives the behavioral approach more opportunities to be applied.",
        "An adult follows through on planned skills sessions and between-session activities. The therapy becomes a continuing part of the routine rather than an interrupted series of visits.",
    ),
    "Nutrition Quality|Symptom Severity|-": (
        "This hypothetical example concerns removing hunger or a nutrition-related difficulty that adds to trouble concentrating. It does not claim that a general diet change treats the underlying ADHD condition.",
        "A hungry student finds it difficult to stay with a classroom activity. After eating an adequate meal in this fictional situation, that added distraction eases while underlying attention difficulties may remain.",
        "An adult's irregular meals add fatigue and distraction during work. More dependable nourishment removes that extra burden in this imagined example, rather than removing ADHD itself.",
    ),
    "Physical Activity|Symptom Severity|-": (
        "The example illustrates an activity break helping a particular person settle into a following task. It is a hypothetical context-specific benefit, not a promise that exercise treats every ADHD symptom.",
        "After a movement break, a fictional student returns to a classroom task feeling less restless. Fewer interruptions make that particular activity easier to stay with.",
        "An adult takes a planned active break before returning to demanding work. In this imagined situation, some immediate restlessness eases without assuming the underlying condition has disappeared.",
    ),
    "Digital Media Exposure|Symptom Severity|+": (
        "Frequent alerts and rapid switching between digital activities can interrupt sustained attention during a task. This illustrates a possible distraction pathway, not proof that digital media causes ADHD.",
        "Notifications repeatedly draw a student's attention away from an assignment. Each return requires finding the place again, making distraction more frequent during the activity.",
        "An adult alternates between a work task and a stream of digital updates. Repeated switching adds missed details and interruptions to existing attention difficulties.",
    ),
    "Screen Time|Symptom Severity|+": (
        "For this example, screen time means distracting use that competes with an ongoing activity. The possible effect comes from interruptions and competing attention, not every use of a screen or a demonstrated cause of ADHD.",
        "A student keeps checking a screen while trying to follow homework instructions. The competing activity makes losing the next step more frequent.",
        "An adult leaves distracting video content running beside a demanding task. Attention repeatedly shifts away, adding interruptions to the work rather than creating a new diagnosis.",
    ),
    "Environmental Exposure|Symptom Severity|+": (
        "The broad environment label is illustrated here as distracting surroundings rather than an unspecified chemical exposure. More competing noise and interruptions can add difficulty sustaining attention during a particular task.",
        "A student works beside frequent noise and movement and repeatedly misses the next instruction. The competing surroundings make an existing attention difficulty more visible.",
        "An adult tries to finish a task in a setting with repeated interruptions. The environment adds distraction that was less noticeable in a quieter setting.",
    ),
})

SOURCES = {
    "genetics": {"title": "Genome-wide analyses of ADHD identify 27 risk loci", "url": "https://www.nature.com/articles/s41588-022-01285-8", "scope": "Genetic association evidence; not an individual prediction or validation of this graph weight."},
    "gene_environment": {"title": "NHGRI: Gene–environment interaction", "url": "https://www.genome.gov/genetics-glossary/Gene-Environment-Interaction", "scope": "Conceptual distinction between genetic liability and environmental influences; not evidence for a nutrition-to-genetic-risk edge."},
    "adhd": {"title": "NIMH: Attention-deficit/hyperactivity disorder", "url": "https://www.nimh.nih.gov/health/topics/attention-deficit-hyperactivity-disorder-adhd", "scope": "Clinical background on symptoms and functioning; not independent causal estimates for these graph concepts."},
    "medication": {"title": "MTA: A randomized trial of ADHD treatment strategies", "url": "https://pubmed.ncbi.nlm.nih.gov/10591283/", "scope": "Pediatric treatment-trial context; not a guarantee of response, an adult-treatment estimate or validation of a snapshot weight."},
    "sleep": {"title": "Hiscock et al.: Behavioral sleep intervention trial", "url": "https://www.bmj.com/content/350/bmj.h68", "scope": "A pediatric sleep-intervention trial; does not establish every sleep mechanism or an adult effect."},
    "media": {"title": "Ra et al.: Digital media use and subsequent ADHD symptoms", "url": "https://pubmed.ncbi.nlm.nih.gov/30027248/", "scope": "Observational adolescent association; the authors do not establish causation."},
    "quality_of_life": {"title": "Children's ADHD symptoms and health-related quality of life", "url": "https://pubmed.ncbi.nlm.nih.gov/40657667/", "scope": "Longitudinal associations in children; not proof of a single impairment-to-quality-of-life causal effect."},
}

CONTEXT = {
    "Genetic Risk|ADHD|+": ["genetics"],
    "Early Life Nutrition|Genetic Risk|-": ["gene_environment"],
    "ADHD|Symptom Severity|+": ["adhd"],
    "ADHD|Symptom Type|+": ["adhd"],
    "ADHD|Executive Function Deficit|+": ["adhd"],
    "Symptom Severity|Functional Impairment|+": ["adhd"],
    "Functional Impairment|Quality of Life|-": ["quality_of_life"],
    "Medication Treatment|Symptom Severity|-": ["medication"],
    "Medication Treatment|Functional Impairment|-": ["medication"],
    "Behavioral Therapy|Symptom Severity|-": ["medication"],
    "Behavioral Therapy|Functional Impairment|-": ["medication"],
    "Sleep Quality|Symptom Severity|-": ["sleep"],
    "Sleep Quality|Executive Function Deficit|-": ["sleep"],
    "Digital Media Exposure|Symptom Severity|+": ["media"],
    "Screen Time|Symptom Severity|+": ["media"],
}
