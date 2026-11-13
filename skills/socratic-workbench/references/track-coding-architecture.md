# Track A Adapter: Code & System Architecture

> **Ideal for**: Learners whose syntax is rusty or who code daily with AI, yet need rock-solid mental ownership of **system boundaries, invariants, concurrency/edge cases, and architectural tradeoffs** for engineering work and technical interviews.

---

## Design Philosophy: Logic Ownership Without Syntax Friction

Most AI-assisted coding creates fake fluency: the learner accepts 50 lines of generated code, reads it once ("looks right"), and forgets every invariant three days later. Track A separates **design logic** (owned 100% by the human) from **language syntax** (compiled deterministically by AI + unit tests).

---

## Part 4 Format: 4-Slot Native-Language Pseudocode Drill

For every coding/algorithm/component drill in `workbench.md`:

1. **Concrete Input / Output Examples (JSON / Plain Data)**:
   Show 2–3 intuitive examples so the learner never guesses framework boilerplate.
2. **Stripped Interface Contract**:
   Tell the learner exact field names, method signatures, and state types already handled by the wrapper.
3. **Neutral 4-Slot Pseudocode Form** (learner fills in plain English, Chinese, or any native language):
   - **Slot 1 — State & Containers**: What persistent/local variables, maps, queues, or counters do you keep?
   - **Slot 2 — Core Step / Transition**: What happens step-by-step on each call or loop iteration?
   - **Slot 3 — Boundary & Error Guards**: What happens on zero/negative inputs, empty state, clock jumps, overflow, or failure?
   - **Slot 4 — Return / Side-Effect Contract**: What exact structure or boolean/result do you return or mutate?

---

## Grading Protocol (4 Mandatory Steps)

When the learner submits their 4-slot pseudocode:

1. **Literal 1:1 Compilation (Zero Silent Fixes)**:
   - Translate the learner's exact 4 slots into the target exercise file (`exercise.py`, `exercise.ts`, etc.).
   - Wrap only the pre-declared function/class signature and return struct.
   - **NEVER** add an `if`, clamp, lock, or boundary guard the learner did not specify.
2. **Run Deterministic Verification**:
   - Execute the real test suite (e.g., `pytest`, `unittest`, `vitest`, `go test`) via shell command.
3. **If ANY Test Fails (`FAILED`) — Counterexample Probing Only**:
   - Output exact pass/fail count first (e.g., `Passed: 5 / 8 tests`).
   - Extract the **first failing test's concrete input + observed actual output vs expected output**.
   - Ask ONE targeted question: *"Given input X, your Step 2 produced A instead of B. Which slot rule needs updating?"*
   - **FORBIDDEN**: Showing the corrected code, naming the exact `if` statement, or flattering.
4. **When 100% Pass (`PASSED`) — Post-Pass Idiom Anatomy**:
   - Compare the compiled implementation against the clean reference `solution.*`.
   - Highlight **1–2 concise engineering idioms or standard-library patterns** (e.g., `min(cap, tokens + elapsed * rate)` instead of loops, `collections.Counter`, monotonic clock vs wall clock) so the learner absorbs readable design taste without memorizing raw syntax.
