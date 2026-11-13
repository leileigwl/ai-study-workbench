# Track B Adapter: Exams, Interviews & Concept Mastery

> **Ideal for**: Technical interviews, system design reviews, cloud/security certifications, bar/medical/finance exams, or dense conceptual courses where precision under questioning matters.

---

## Design Philosophy: Point-Counted Blind Recall + Scenario Stress Testing

Passive flashcards invite premature peeking and shallow memorization of isolated definitions. Track B groups questions by architectural/syllabus theme, reveals only how many scoring points exist (`(4 core points)`), hides every rubric bullet inside `answer_key.md`, and probes missing points using real-world failure incidents.

---

## Part 2 & Part 4 Structure in `workbench.md`

1. **Part 2 — Theme-Clustered Blind Questions**:
   - Group questions by syllabus/system pillar (e.g., *Isolation & Concurrency*, *Recovery & Failure Modes*).
   - Mark every question with `(N core points)`.
   - Never expose hints or keywords inline.
2. **Part 4 — Incident Root-Cause / Tradeoff Matrix Drill**:
   - Present 1–2 concrete production incidents or exam case vignettes (e.g., *"At 2,000 QPS, read queries see phantom billing rows even under Repeatable Read..."*).
   - Ask the learner to diagnose root cause, propose a fix, and justify one tradeoff.

---

## Grading Protocol (3-Step Anti-Spoiler Audit)

When the learner submits `> My Draft:` notes:

1. **Audit Against `answer_key.md`**:
   - Match learner keywords/concepts against numbered points in `answer_key.md`.
   - Report: `Matched: X / Y core points` and briefly confirm which ideas hit.
   - **NEVER** list the missed concepts directly.
2. **Design Concrete Failure/Exam Probes for Missed Points**:
   - Use the pre-built probes in `answer_key.md` or craft an edge-case question that breaks the learner's partial answer.
   - Example: If they missed *clock skew* in distributed locking, ask: *"Your lease TTL is 10s, NTP drifts 4s between nodes, and GC pauses 8s — why do two workers now think they both hold the lock?"*
3. **Lock Bold-Keyword Memory Card**:
   - Once the learner resolves the probes (or explicitly says `"reveal after attempt"`), write a structured **bold-keyword summary** into `> Follow-up & Audited Answer:` inside `workbench.md` so Part 2 becomes a personalized, high-retention exam cheat sheet.
