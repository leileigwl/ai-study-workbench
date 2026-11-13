# The Socratic Workbench Methodology: Learning Anything with AI Without the Illusion of Competence

## 1. The Core Problem: Why Conventional AI Study Fails

When learners use LLMs (ChatGPT, Claude, Gemini, Cursor) to study codebases, exams, or books, three predictable failure modes emerge:

1. **Premature Answer Spoiling**: Ask "Explain this concept" or "Quiz me", and the AI dumps clean summaries or hints right below the question. Passive recognition feels like mastery — **the Illusion of Competence** — yet collapses under closed-book interviews or production incidents.
2. **Syntax Overwhelm vs. Silent AI Patching**: In coding drills, either learners waste hours fighting forgotten syntax boilerplate, or they accept 60 lines of AI-generated code and learn zero invariants because the AI quietly handles edge cases the learner never thought of.
3. **Model Drift on Lightweight / Flash Models**: Switching to faster, cheaper models causes prompt fatigue — the AI reverts to flattery, auto-fixes logic bugs, and skips Socratic probing unless constrained by explicit file separation and a deterministic state machine.

---

## 2. How `socratic-workbench` Fixes It (5-Part Architecture)

| Failure Mode | Cognitive Mechanism Violated | Socratic Workbench Countermeasure |
|---|---|---|
| Reading smooth AI explanations feels like learning | **Generation Effect & Active Recall** | **Dual-File Separation** (`workbench.md` vs `answer_key.md`): questions display only `(N core points)` with empty draft slots |
| Seeing a full answer right after a weak guess triggers "I basically knew that" | **Calibration & Productive Struggle** | **3-Step Scenario Probing**: AI scores `Matched: X / Y`, hides missed bullets, and invents a concrete failure incident forcing you to reason out the gap |
| Hand-writing boilerplate syntax slows systems learning; full AI coding kills logic ownership | **Desirable Difficulty (Logic vs Syntax)** | **4-Slot Native-Language Pseudocode + 1:1 Literal Compile**: you own Containers, Step, Guards, Return in plain language; AI translates literally with zero silent fixes and lets `tests` act as objective judge |
| Lightweight/Flash models ignore soft prompts | **Deterministic Guardrails** | Explicit **Hard Refusals & 4-Check State Gate** backed by external files (`answer_key.md`, `test_*`, `init_workbench.py --check`) |

---

## 3. The "1 + 3" Domain Model

One universal 5-step workflow (**Diagnose -> Macro Map & Traps -> Dual-File Blind Workbench -> Active Drill & Socratic Probe -> Spaced Sign-Off**) feeds three specialized adapters:

- **Track A (`coding`)**: Macro system boundaries -> Intuition Traps -> 4-Slot Native-Language Pseudocode -> 1:1 Literal Compilation -> Deterministic Test Counterexamples -> Post-Pass Idiom Anatomy.
- **Track B (`interview`)**: Syllabus clustering -> Point-Counted Blind Q&A -> Incident Failure Probing -> Bold-Keyword Memory Card Locking.
- **Track C (`book`)**: Causal mental-model mapping -> Cognitive/Intuition Trap Table -> Cross-Context Case Transfer -> 60-Second Jargon-Free Feynman Teach-Back.

---

## 4. Recommended 4-Step Daily Loop

1. **Skim Source + Anchor Macro Map (Part 1 & Part 3)**: Identify high-yield invariants and how they fail in the wild before touching drills.
2. **Blind Retrieval Without Peeking (Part 2)**: Fill concise keywords under `> My Draft:` in `workbench.md`. Submit to AI for `Matched: X / Y` scoring + failure scenario probing; only unlock bold memory anchors after resolving probes.
3. **Active Production Drill (Part 4)**: Write 4-slot pseudocode (Track A), incident diagnosis (Track B), or unfamiliar case transfer (Track C). Let objective tests or rubric criteria break your blind spots via counterexamples.
4. **Honest Sign-Off & Spaced Re-Check (Part 5)**: Mark questions that needed $\ge 2$ follow-up hints for a 24h / 72h cold-recall re-test.
