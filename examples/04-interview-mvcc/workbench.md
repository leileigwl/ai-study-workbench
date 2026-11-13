# Interview Prep: Database MVCC & Write Skew — Active Study Workbench

> **Track**: `interview`  
> **What you'll master**: Explain snapshot isolation cleanly and diagnose subtle double-spending / double-booking bugs in system design rounds  
> **Rule**: Write rough keywords under `> **My Try**:` *before* opening `answer_key.md`.

---

## Part 1: What Matters Most & Big Picture

### 1.1 Priority Guide
- **Must Master**:
  - Why MVCC lets long reads and fast writes run side by side without blocking each other
  - Why `REPEATABLE READ` (Snapshot Isolation) still allows **Write Skew** across two separate rows
- **Good Context**:
  - Background vacuum / undo log cleanup internals

### 1.2 How It All Connects
```text
[Concurrent Requests] ---> [Snapshot ID per Transaction] ---> [Row Version History] ---> [Commit or Conflict Abort]
```

---

## Part 2: Blind Check Questions (Try First -> Follow-Up -> Final Note)

> Write rough bullet keywords under `> **My Try**:` without peeking at `answer_key.md`.

### Topic A: Snapshot Reads & Concurrency Bugs

#### Q1.1 How does MVCC allow a 5-minute analytical `SELECT` and thousands of `UPDATE` writes to run at the exact same time without blocking each other? (`3` points)
- > **My Try**: 
- > **Coach Feedback & Final Note**: *(Unlocked after your try + follow-up)*

#### Q1.2 Why can two concurrent transactions under PostgreSQL `REPEATABLE READ` (Snapshot Isolation) leave a hospital shift with ZERO doctors on call even though code checks `count >= 2` first? (`3` points)
- > **My Try**: 
- > **Coach Feedback & Final Note**: *(Unlocked after your try + follow-up)*

---

## Part 3: Common Mistakes (Quick Trap Check)

| Area | Classic Misconception | How It Fails in Interviews / Prod | Exact Right Answer |
|---|---|---|---|
| Isolation | "`REPEATABLE READ` stops concurrent transactions from breaking business rules" | Two doctors read `count=2` from the same snapshot and both update *different* rows (`doctor=Alice`, `doctor=Bob`) — both commit! | Snapshot Isolation only blocks **same-row** conflicts; cross-row rules need `SERIALIZABLE` (SSI) or explicit `SELECT ... FOR UPDATE` / locking a shared shift row |
| Cleanup | "Dead row versions are harmless" | One idle transaction left open for hours pins old versions, blocking cleanup and slowing every scan | Set idle-transaction timeouts and isolate heavy analytics onto replicas |

---

## Part 4: Realistic Failure / Exam Twist Case

### Case 4.1: Coupon Budget Overdraft Under Load
> **Scenario**: A promo rule says a user's campaign wallet (`total <= 100`) checks active rows in `REWARDS` (`SUM(amount)`) before inserting a new reward row. Under `REPEATABLE READ`, two parallel requests both read `SUM=80`, and each inserts `30` — leaving `140`.

- **Your Root-Cause Diagnosis**: 
- **Fix + One Tradeoff**: 

---

## Part 5: Honest Sign-Off Checklist

- [ ] Can explain MVCC read snapshots and Write Skew in plain language in 60 seconds.
- [ ] Answered `Q1.1` & `Q1.2` blind and resolved all follow-up scenarios.
- [ ] Solved Case 4.1 with two valid fixes (`SERIALIZABLE` vs. locking a parent wallet row) and stated the latency/retry tradeoff.
