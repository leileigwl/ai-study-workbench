# Domain Guide: Codebases, Algorithms & System Design (`coding`)

Use when the learner shares a repository, architecture guide, coding lesson, or backend/frontend design doc—especially when syntax is rusty and they want solid ownership of **logic, invariants, and tradeoffs**.

## Vocabulary Adaptation
Refer to items naturally as **system invariants, data structures, edge guards, failure boundaries, and architectural tradeoffs**.

## 4-Step Source-Driven Flow
1. **Extract from the Codebase/Doc**: Map upstream/downstream boundaries, common bugs/anti-patterns, and reference answers into `answer_key.md`.
2. **Blind Workbook (`workbench.md`) + 4-Slot Plain-Language Drill**:
   - Conceptual checks show `(N points)` and blank `> My Try:` slots.
   - Code drills show 2–3 Input/Output JSON samples + the stripped interface signature and ask ONLY for **4 plain-language steps** (What to store / Main steps / Edge guards / What to return).
   - **Compile 1:1 literally** into `exercise.*` (zero silent boundary fixes), run real tests, and respond to failures with ONLY exact pass count + the first failing input vs. expected output.
3. **Unlock for Memorization**: Once probes and tests pass 100%, unlock concise **Verified Answers to Memorize** in Part 2 and highlight **1–2 clean engineering idioms** from `solution.*`.
4. **Answer-Grounded Mock Simulation**: Switch into a staff-engineer design review or production incident interview—probe what breaks under 10x traffic, clock drift, partial failures, or concurrency using the extracted `answer_key.md` invariants as your rubric.
