# Interview Prep: Database MVCC & Write Skew — Separated Answer Key (For Your AI Coach)

> **Track**: `interview`  
> Keep closed while practicing `workbench.md`. Q-IDs match 1:1.

---

### Q1.1 How does MVCC allow a 5-minute analytical `SELECT` and fast `UPDATE` writes without blocking each other?
- **Key Points (`3`)**:
  1. **Append Versions Instead of Overwriting**: Updates create a new version stamped with transaction visibility metadata (`xmin`/`xmax` or undo log).
  2. **Consistent Read Watermark**: Readers keep a frozen snapshot ID taken when they started, ignoring newer commits.
  3. **Readers Don't Block Writers**: No shared read locks needed; writers only contend with writers modifying the *same* row.
- **Follow-Up Prompts if Missed**:
  - *If missing Point 2*: `"Transaction A starts a slow report at 10:00. Transaction B updates a price at 10:02 and commits. Without locking the table, how does Transaction A still see the 10:00 price?"`

### Q1.2 Why can PostgreSQL `REPEATABLE READ` still leave ZERO doctors on call?
- **Key Points (`3`)**:
  1. **Disjoint Rows Written**: First-Committer-Wins only aborts overlapping *same-row* writes; Alice and Bob updated different rows.
  2. **Shared Stale Snapshot**: Both evaluated `count >= 2` on the same snapshot before either committed.
  3. **Cross-Row Fix**: Requires `SERIALIZABLE` (SSI predicate conflict tracking) or locking a single parent `SHIFT` row (`SELECT ... FOR UPDATE`).
- **Follow-Up Prompts if Missed**:
  - *If missing Point 3*: `"Say upgrading the whole database to `SERIALIZABLE` spikes retry errors under heavy load. How can you fix this specific bug while keeping `REPEATABLE READ`?"`
