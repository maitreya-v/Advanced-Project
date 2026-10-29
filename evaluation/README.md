# Story evaluation protocol

The dashboard's **Evaluation lab** contains a fixed 24-case suite covering every graph snapshot, historical comparisons, age-scenario comparisons, and all five story focuses.

## Study A: human story ratings

Generate each case with the local model, then have a reviewer score it from 1–5 on:

- graph fidelity;
- topic relevance;
- narrative coherence;
- clarity; and
- engagement.

Graph fidelity means agreement with the authored graph and attached scene evidence. It does not mean that the graph is clinically valid. Reviewers should use the notes field for specific errors. Download the CSV or JSON before closing the browser session.

Recommended minimum: all 24 stories, with at least two independent reviewers per story. Report the mean and range for every dimension, the number of rejected generations, and common error categories. Do not invent missing human scores.

## Study B: comprehension comparison

Assign each participant a unique ID. The app reproducibly assigns that participant and case to one of three conditions:

1. graph explorer;
2. rule-based story; or
3. generated story.

Participants answer four questions about a graph difference, missing-edge interpretation, weight interpretation, and the comparison axis. The app records score, completion time, and self-reported confidence.

Use prepared generated stories before recruiting participants. Keep instructions, device, and available time consistent across conditions. Analyze mean comprehension score first; time and confidence are secondary outcomes. With a small class sample, present the results as exploratory rather than statistically conclusive.

## Privacy and storage

Use anonymous participant IDs. Ratings and comprehension results remain in the current browser session and are only written when the user downloads them. Do not enter names, email addresses, diagnoses, or other health information.
