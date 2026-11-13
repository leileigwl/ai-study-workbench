[English](workbench.md) | [简体中文](workbench.zh-CN.md)

# Token Bucket Rate Limiter — Practice Workbench

> **Domain**: `coding`  
> **Source Material**: *API Gateway Rate Limiting Module*  
> **Spoiler Lock**: Practice here *before* unlocking standard answers from `answer_key.md` or reading `solution.py`.

---

## Part 1: High-Yield Guide & Big Picture

### 1.1 Priority Reading Focus
- **Must Master**:
  - Computing refilled tokens **on demand when a request arrives** instead of spawning background timer threads
  - Protecting against **clock jumps** and **burst overflow above capacity**
- **Good Context**:
  - Multi-node Redis + Lua coordination later

### 1.2 Big-Picture Map
```text
[API Client] ---> [TokenBucketLimiter.allow()] ---> (Allowed) ---> [Backend Service]
                             |
                        (Rejected: 429 + retry_after)
```

---

## Part 2: Blind Check Questions (Practice -> Follow-Up -> Unlock to Memorize)

> Write rough keywords under `> **My Try**:` first. Once cleared, your coach unlocks concise answers under `> **Verified Answer to Memorize**:`.

### Topic A: Time, Memory & Concurrency

#### Q1.1 Why do real rate limiters calculate tokens lazily on request arrival instead of running a background timer every 100ms for every user? (`3` points)
- > **My Try**: 
- > **Verified Answer to Memorize**: *(Locked until blind try + follow-up probe are completed)*

#### Q1.2 What breaks if you use wall-clock time (`time.time()`) instead of a monotonic clock, or never evict idle user keys? (`2` points)
- > **My Try**: 
- > **Verified Answer to Memorize**: *(Locked until blind try + follow-up probe are completed)*

---

## Part 3: Common Misconception Traps

| Area | Tempting Mistake | How It Fails in Practice | Grounded Truth |
|---|---|---|---|
| Refill | Spawn a background timer thread adding tokens every tick | Wastes CPU scanning idle users and blocks shared locks | **Lazy math**: store `(tokens, last_ts)` and refill on request arrival |
| Cap Limit | `tokens += elapsed * rate` with no ceiling | Idle users build millions of tokens overnight and flood your DB | Always clamp `min(capacity, ...)` |
| Wall Clock | Subtract `time.time() - last_ts` directly | Backward NTP jump makes elapsed negative | Use `time.monotonic()` or clamp `max(0.0, elapsed)` |

---

## Part 4: 4-Step Plain-Language Code Drill

### Drill 4.1: `TokenBucketLimiter.allow(key, cost, now)`

#### Input / Output Examples
```json
[
  {
    "config": {"capacity": 5.0, "refill_rate": 2.0},
    "call": {"key": "alice", "cost": 3.0, "now": 10.0},
    "expected": {"allowed": true, "remaining_tokens": 2.0, "retry_after": 0.0}
  },
  {
    "config": {"capacity": 5.0, "refill_rate": 2.0},
    "call": {"key": "alice", "cost": 4.0, "now": 10.5},
    "expected": {"allowed": false, "remaining_tokens": 3.0, "retry_after": 0.5}
  }
]
```

#### Already Handled For You
- Signature: `allow(self, key: str, cost: float = 1.0, now: float | None = None) -> Decision(allowed, remaining_tokens, retry_after)`
- New `key` starts full (`tokens = capacity`).

#### Your 4 Plain-Language Steps (No raw syntax needed)
1. **What to store**: 
2. **Main step / loop**: 
3. **Edge cases to guard**: 
4. **What to return**: 

---

## Part 5: Answer-Grounded Mock Simulation & Sign-Off

- **Mock Simulation Brief**: Once your 4 steps pass `test_exercise.py` and Part 2 answers are memorized, tell your coach: *"Run Step 4 Mock Simulation."* Your coach acts as a staff engineer grilling edge cases (1M keys, backward clock drift, cost > capacity) strictly against `answer_key.md`.
- [ ] Explained Part 1's big picture in 60 seconds without notes.
- [ ] Unlocked and memorized all Part 2 verified standard answers.
- [ ] Passed 100% of `test_exercise.py` from 4 plain-language steps and reviewed `solution.py`.
- [ ] Passed closed-book Mock Simulation using `answer_key.md` as the live rubric.
