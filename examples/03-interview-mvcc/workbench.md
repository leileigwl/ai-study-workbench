# Interview Prep: Database MVCC & Write Skew — Practice Workbench

> **Domain**: `interview`  
> **Source Material**: *System Design Handbook: Isolation Levels & Concurrency Anomalies*  
> **Spoiler Lock**: Practice here *before* unlocking standard answers from `answer_key.md`.

---

## Part 1: High-Yield Guide & Big Picture

### 1.1 Priority Reading Focus
- **Must Master**:
  - Why MVCC lets long reads and fast writes run side by side without blocking
  - Why `REPEATABLE READ` (Snapshot Isolation) still allows **Write Skew** across two different rows
- **Good Context**:
  - Background dead-tuple cleanup mechanics

### 1.2 Big-Picture Map
```text
[Concurrent Clients] ---> [Snapshot ID per Txn] ---> [Version Chain] ---> [Commit or Conflict Abort]
```

---

## Part 2: Blind Check Questions (Practice -> Follow-Up -> Unlock to Memorize)

> Write rough keywords under `> **My Try**:` first. Once cleared, your coach unlocks concise answers under `> **Verified Answer to Memorize**:`.

### Topic A: Snapshot Reads & Concurrency Bugs

#### Q1.1 How does MVCC allow a 5-minute analytical `SELECT` and fast `UPDATE` writes to run at the same time without blocking each other? (`3` points)
- > **My Try**: 
- > **Verified Answer to Memorize**: *(Locked until blind try + follow-up probe are completed)*

#### Q1.2 Why can two concurrent transactions under PostgreSQL `REPEATABLE READ` leave a shift with ZERO doctors on call even when code checks `count >= 2` first? (`3` points)
- > **My Try**: 
- > **Verified Answer to Memorize**: *(Locked until blind try + follow-up probe are completed)*

---

## Part 3: Common Misconception Traps

| Area | Classic Misconception | How It Fails in Practice | Grounded Truth |
|---|---|---|---|
| Isolation | "`REPEATABLE READ` blocks all concurrent invariant bugs" | Two transactions read `count=2` and update *different* rows (`doctor=A`, `doctor=B`) — both commit! | Snapshot Isolation catches **same-row** conflicts only; cross-row rules need `SERIALIZABLE` (SSI) or locking a parent row (`SELECT ... FOR UPDATE`) |
| Cleanup | "Old versions cost nothing once committed" | A long idle transaction pins old versions, blocking vacuum and bloating tables | Bound idle transaction timeouts and route heavy analytics to replicas |

---

## Part 4: Incident / Exam Vignette Drill

### Case 4.1: Coupon Budget Overdraft Under Concurrency
> **Scenario**: Promo code allows at most \$100 total rewards per user by checking `SUM(amount)` in `REWARDS` before inserting a new reward row. Under `REPEATABLE READ`, two parallel clicks read `SUM=80` and both insert `30` (`140` total).

- **Root-Cause Diagnosis**: 
- **Fix + One Tradeoff**: 

---

## Part 5: Answer-Grounded Mock Simulation & Sign-Off

- **Mock Simulation Brief**: Once Parts 2–4 are memorized, say: *"Run Step 4 Mock Simulation."* Your coach will interview you closed-book on `Q1.1`, `Q1.2`, and Case 4.1 against `answer_key.md`.
- [ ] Explained Part 1's big picture in 60 seconds without notes.
- [ ] Unlocked and memorized all Part 2 verified standard answers.
- [ ] Completed Case 4.1.
- [ ] Passed closed-book Mock Simulation using `answer_key.md` as the live rubric.
