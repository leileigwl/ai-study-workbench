# Database MVCC & Isolation Levels — Separated Answer Key

> **Track**: `interview`  
> **Spoiler Guard**: Keep closed until blind drafts in `workbench.md` are graded.

---

### Q1.1 How does MVCC allow long-running analytical `SELECT` queries and high-frequency `UPDATE` transactions to run simultaneously without blocking each other?
- **Core Scoring Points (`3`)**:
  1. **Versioned Row Copies**: Writers append new row versions (or undo log records) tagged with transaction visibility bounds (`xmin`/`xmax`) instead of mutating bytes in place.
  2. **Consistent Read Snapshots**: Each transaction captures an active-transaction snapshot (`xid` watermark) at start (or statement start) so readers only see committed versions visible at that instant.
  3. **Non-Blocking Separation**: Readers never acquire shared read locks that block writers, and writers only contend with other writers on the same row.
- **Scenario Probes (Use if missed)**:
  - *Missing Point 1 or 2*: `"Suppose Txn 100 begins a 10-minute report, and at minute 2 Txn 105 commits an update changing a balance from 500 to 0. How does Txn 100 still read 500 without holding a table lock?"`
  - *Missing Point 3*: `"Why can an interactive checkout `UPDATE` still stall behind another `UPDATE` on the exact same inventory row even under MVCC?"`

### Q1.2 Why can PostgreSQL `REPEATABLE READ` (Snapshot Isolation) still permit double-spending or double-booking across two different rows?
- **Core Scoring Points (`3`)**:
  1. **Disjoint Write Sets**: First-Committer-Wins only aborts transactions whose modified **rows overlap**; updating two distinct rows commits both cleanly.
  2. **Shared Stale Snapshot Premise**: Both transactions evaluate a read predicate (`count(*) >= 2`) against the **same pre-commit snapshot**, neither seeing the other's uncommitted intent.
  3. **Write Skew Remedy**: Cross-row invariants require **SSI (`SERIALIZABLE`)** conflict tracking (SIREAD predicate locks), **explicit locking (`SELECT ... FOR UPDATE`)**, or consolidating the invariant onto one locked parent row.
- **Scenario Probes (Use if missed)**:
  - *Missing Point 1*: `"Postgres runs First-Committer-Wins under Repeatable Read. If Alice updates row A and Bob updates row B, why does Postgres let both commit?"`
  - *Missing Point 3*: `"If upgrading the whole database to `SERIALIZABLE` causes 8% retry aborts under peak load, how could you preserve correctness inside `REPEATABLE READ`?"`
