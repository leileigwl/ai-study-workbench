# Database MVCC & Isolation Levels — Active Study Workbench

> **Track**: `interview`  
> **Goal**: Master concurrency anomalies, Snapshot Isolation vs Serializable, and write-skew failure diagnosis  
> **Spoiler Rule**: Attempt every draft below *before* consulting `answer_key.md`.

---

## Part 1: Focus Guide & Macro Map

### 1.1 Priority Reading Guide
- **Core (Must Master)**:
  - How MVCC prevents readers from blocking writers and writers from blocking readers
  - Why **Snapshot Isolation (Repeatable Read in Postgres)** prevents dirty/non-repeatable reads yet still fails on **Write Skew**
  - Lock-based 2PL vs SSI (Serializable Snapshot Isolation) tradeoffs
- **Extended (Context Only)**:
  - PostgreSQL `VACUUM` / MySQL InnoDB undo log purging mechanics

### 1.2 Macro Integration & Dependency Map
- **Upstream Inputs**: Concurrent SQL transactions reading & modifying shared rows under a configured isolation level.
- **Core Responsibility**: Decide which version `(xmin, xmax)` or lock set each transaction is legally allowed to observe and mutate without corrupting invariants.
- **Downstream Consumers / Effects**: Misconfigured isolation causes silent financial double-spends, double-bookings, or replica bloat from uncollected dead tuples.

```text
[Concurrent Clients] -> [Transaction Manager (Txn IDs + Snapshots)] -> [Storage Engine Version Chain] -> [Commit / Abort Decision]
```

---

## Part 2: Categorized Blind Retrieval Q&A (Draft -> Scenario Probe -> Audit)

> Write concise keywords under `> **My Draft**:`. Send to your AI coach for point-count scoring and scenario follow-ups.

### Category A: MVCC Internals & Visibility

#### Q1.1 How does MVCC allow long-running analytical `SELECT` queries and high-frequency `UPDATE` transactions to run simultaneously without blocking each other? (`3` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until blind draft + scenario probe are completed)*

### Category B: Anomalies & Write Skew

#### Q1.2 Why can PostgreSQL `REPEATABLE READ` (Snapshot Isolation) still permit double-spending or double-booking across two different rows? (`3` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until blind draft + scenario probe are completed)*

---

## Part 3: Intuition Traps & Anti-Patterns

| Category | Intuition Trap | Real-World / Exam Failure Mode | Reliable Principle |
|---|---|---|---|
| Isolation | "`REPEATABLE READ` stops two concurrent txns from breaking invariants" | Two doctors read each other as "on call" and both go off-call in disjoint rows (**Write Skew**) | Snapshot Isolation only detects *same-row* write-write conflicts; cross-row invariants need `SERIALIZABLE` (SSI) or explicit `SELECT ... FOR UPDATE` / materialized lock row |
| Garbage Collection | "Once old updates commit, version chains cost nothing" | A single forgotten idle-in-transaction reporting query pins the oldest `xmin`, preventing `VACUUM`/undo purge and bloating disk + degrading index scans | Bound analytics transaction timeouts and isolate heavy OLAP reads onto a read replica |

---

## Part 4: Active Production Drill — Incident Root-Cause & Tradeoff Diagnosis

### Case 4.1: Hospital On-Call Roster Double-Drop Incident
> **Scenario**: A clinic requires **at least 1 doctor** on call per shift (`ON_CALL` table: `(doctor_id, shift_id, active)`). Two doctors simultaneously run under Snapshot Isolation: `BEGIN; SELECT count(*) FROM on_call WHERE shift_id=42 AND active=true;` (both get `2`), then Alice updates `doctor_id=Alice SET active=false` and Bob updates `doctor_id=Bob SET active=false`. Both transactions commit cleanly, leaving **0 doctors on call**.

- **Root Cause Hypothesis**: 
- **Immediate Mitigation vs Structural Fix**: 
- **Key Tradeoff Accepted**: 

---

## Part 5: Unit Sign-Off Checklist

- [ ] Can draw an MVCC version chain (`xmin`/`xmax` or undo log) in 60 seconds.
- [ ] Resolved `Q1.1` & `Q1.2` blind and cleared scenario follow-ups.
- [ ] Can immediately diagnose Write Skew vs Lost Update in interview system design reviews.
- [ ] Completed Case 4.1 with at least two valid structural fixes and their latency/retry tradeoffs.
