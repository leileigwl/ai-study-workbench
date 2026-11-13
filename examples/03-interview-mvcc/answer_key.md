# Interview Prep: Database MVCC & Write Skew — Extracted Standard Answers & Mock Rubric

> **Domain**: `interview`  
> Extracted from source material. Used by the AI coach to grade `workbench.md` and run Step 4 Mock Simulations.

---

### Q1.1 How does MVCC allow a 5-minute `SELECT` and fast `UPDATE`s without blocking?
- **Standard Answer Key Points (`3`)**:
  1. **Append Versions Instead of Overwriting**: Updates create a new version stamped with visibility bounds (`xmin`/`xmax` or undo log).
  2. **Consistent Read Watermark**: Readers keep a frozen snapshot ID taken when starting, ignoring newer commits.
  3. **Readers Never Block Writers**: No shared read locks needed; writers only contend on the *same* row.
- **Follow-Up Probes if Missed (Never spoil directly)**:
  - *If missing Point 2*: `"Transaction A starts a slow report at 10:00. Transaction B commits a balance update at 10:02. Without a table lock, how does A still read the 10:00 balance?"`

### Q1.2 Why can PostgreSQL `REPEATABLE READ` leave ZERO doctors on call?
- **Standard Answer Key Points (`3`)**:
  1. **Disjoint Rows Written**: First-Committer-Wins only aborts same-row collisions; Alice and Bob touched separate rows.
  2. **Shared Stale Snapshot**: Both ran `count >= 2` against the same pre-commit snapshot.
  3. **Cross-Row Remedy**: Needs `SERIALIZABLE` (SSI conflict tracking) or locking a parent `SHIFT` row (`SELECT ... FOR UPDATE`).
- **Follow-Up Probes if Missed**:
  - *If missing Point 3*: `"Say `SERIALIZABLE` retries spike error rates under peak load—how can you prevent the bug inside `REPEATABLE READ`?"`
