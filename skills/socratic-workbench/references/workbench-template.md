# Standardized Workbench & Separated Answer-Key Schema

Every study unit MUST consist of two separate files in the same unit directory:
- `workbench.md` — The learner's active workspace (0% spoilers).
- `answer_key.md` — Reference rubric, Q-ID-matched scoring points, and keyword memory anchors (consulted by the AI coach during grading, or reviewed by the learner only after recall).

---

## `workbench.md` — Mandatory 5-Part Structure

```markdown
# Unit XX: <Topic Title> — Active Study Workbench

> **Goal & Timebox**: <User goal, e.g., System design mastery / Certification exam / Applied book notes>
> **Track**: `coding` | `interview` | `book`
> **Rule**: Attempt every question and draft in this file *before* checking `answer_key.md`.

---

## Part 1: Focus Guide & Macro System Map

### 1.1 Priority Reading Guide
- **Core (High-Yield / Must Master)**:
  - ...
- **Extended (Read for Mental Context)**:
  - ...

### 1.2 Macro Integration & Dependency Map
<!-- Show where this unit sits in the broader system, knowledge graph, or problem domain. -->
- **Upstream Inputs**: ...
- **This Unit's Core Responsibility**: ...
- **Downstream Consumers / Effects**: ...
- **Key Integration Snippet / Visual Flow** (15–25 lines max, or Mermaid diagram):
  ```text
  [Upstream] -> [Core Mechanism] -> [Downstream]
  ```

---

## Part 2: Categorized Blind Retrieval Q&A (Draft -> Scenario Probe -> Audit)

> **Instructions**: Write keywords or rough reasoning under `> My Draft:`. Do NOT look at `answer_key.md`. Send your drafts to your AI coach for scoring and failure-scenario follow-ups.

### Category A: <Theme Name>

#### Q1.1 <Question text> (`N` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until draft + scenario probe are completed)*

---

## Part 3: Intuition Traps & Anti-Patterns (Quick Audit Table)

| Category | Intuition Trap (Common Mistake) | Real-World / Exam Failure Mode | Reliable Principle / Practice |
|---|---|---|---|
| ... | ... | ... | ... |

---

## Part 4: Active Production Drill (Track-Specific)

<!-- Replace with the matching Track A / B / C drill block from references/track-*.md -->
<!-- Track A: Input/Output JSON examples + Stripped Interface Contract + 4-Slot Native-Language Pseudocode -->
<!-- Track B: Tradeoff Matrix / Incident Root-Cause Diagnosis Draft -->
<!-- Track C: Real-World Case Transfer + Concept Synthesis Brief -->

---

## Part 5: Unit Sign-Off Checklist

- [ ] Can explain the core mechanism from Part 1 in 60 seconds without notes.
- [ ] Completed all Part 2 questions (including follow-up probes) with 100% key-point coverage.
- [ ] Can spot every Part 3 intuition trap when given a buggy design or flawed argument.
- [ ] Passed Part 4 active drill verification (`tests` 100% pass / Feynman teach-back approved).
```

---

## `answer_key.md` — Mandatory Paired Structure

```markdown
# Unit XX: <Topic Title> — Separated Answer Key (AI Grading Rubric)

> **Spoiler Guard**: Do NOT open while filling `workbench.md`. Q-IDs match `workbench.md` 1:1.

---

### Q1.1 <Question text>
- **Core Scoring Points (`N`)**:
  1. **<Bold Keyword Anchor 1>**: <Concise explanation of the invariant / mechanism>.
  2. **<Bold Keyword Anchor 2>**: <Concise explanation of the tradeoff / failure boundary>.
- **Recommended Follow-up Scenario Probe (if missed)**:
  - *If missing Point 1*: "<Concrete incident/scenario question that forces the learner to discover Point 1>"
  - *If missing Point 2*: "<Concrete edge-case question>"
```
