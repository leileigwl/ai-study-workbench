# Token Bucket Rate Limiter — Active Study Workbench

> **Track**: `coding`  
> **What you'll master**: Design a real-world API rate limiter without memorizing Python boilerplate  
> **Rule**: Write your plain-language steps below *before* opening `answer_key.md` or `solution.py`.

---

## Part 1: What Matters Most & Big Picture

### 1.1 Priority Guide
- **Must Master**:
  - Computing refilled tokens **on demand when a request arrives** instead of spawning background timer threads
  - Protecting against **clock jumps** and **burst overflow above capacity**
- **Good Context**:
  - Multi-server Redis + Lua coordination later in distributed setups

### 1.2 How It All Connects
```text
[API Client] ---> [TokenBucketLimiter.allow()] ---> (Allowed) ---> [Backend Service]
                             |
                        (Rejected: 429 + retry_after)
```

---

## Part 2: Blind Check Questions (Try First -> Follow-Up -> Final Note)

> Jot rough keywords under `> **My Try**:`. Don't peek at `answer_key.md`.

### Topic A: Time, Memory & Concurrency

#### Q1.1 Why do real rate limiters compute new tokens using timestamp math when a request arrives, instead of running a background timer every 100ms to top up every user? (`3` points)
- > **My Try**: 
- > **Coach Feedback & Final Note**: *(Unlocked after your try + follow-up)*

#### Q1.2 What goes wrong if you use wall-clock time (`time.time()`) instead of a monotonic clock, or never evict old inactive keys? (`2` points)
- > **My Try**: 
- > **Coach Feedback & Final Note**: *(Unlocked after your try + follow-up)*

---

## Part 3: Common Mistakes (Quick Trap Check)

| Area | Tempting Mistake | How It Breaks | Reliable Way |
|---|---|---|---|
| Refill | Spawn a background timer thread adding tokens every tick | Wastes CPU on idle users and locks shared maps | **Lazy math**: store `(tokens, last_ts)` and refill only on request arrival |
| Cap Limit | `tokens += elapsed * rate` with no ceiling | Idle users build millions of tokens overnight and flood your DB | Always cap with `min(capacity, ...)` |
| Wall Clock | Subtract `time.time() - last_ts` directly | NTP clock sync backward produces negative elapsed time | Use `time.monotonic()` or clamp `max(0.0, elapsed)` |

---

## Part 4: Plain-Language Code Drill (4-Step Logic -> Real Tests)

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

#### Already Handled For You (Ignore Boilerplate)
- Class & return wrapper live in `exercise.py`: `Decision(allowed, remaining_tokens, retry_after)`.
- Method signature: `allow(self, key: str, cost: float = 1.0, now: float | None = None) -> Decision`.
- Brand-new `key` starts full (`tokens = capacity`).

#### Your 4 Plain-Language Steps (Chinese or English — NO need to write raw syntax)
1. **What to store**: 
2. **Main step / loop**: 
3. **Edge cases to guard**: 
4. **What to return**: 

---

## Part 5: Honest Sign-Off Checklist

- [ ] Can explain lazy token refill vs. background timer threads in 60 seconds.
- [ ] Cleared `Q1.1` & `Q1.2` blind with coach follow-ups.
- [ ] Had my 4 plain-language steps compiled 1:1 into `exercise.py` and passed `test_exercise.py`.
- [ ] Reviewed `solution.py` for 1–2 clean idioms I can reuse.
