# Token Bucket Rate Limiter — Active Study Workbench

> **Track**: `coding`  
> **Goal**: Master lazy-refill rate limiting & concurrency invariants without memorizing boilerplate syntax  
> **Spoiler Rule**: Attempt every draft below *before* consulting `answer_key.md`.

---

## Part 1: Focus Guide & Macro Map

### 1.1 Priority Reading Guide
- **Core (High-Yield / Must Master)**:
  - Why token refill should be computed **lazily on request arrival** rather than via background cron/timer threads
  - Clock source choice (`monotonic` vs wall-clock `time.time()`)
  - Burst capacity clamping (`min(capacity, ...)`) vs leaky-bucket strict pacing
- **Extended (Context Only)**:
  - Distributed Redis + Lua atomic script extension for multi-node gateways

### 1.2 Macro Integration & Dependency Map
- **Upstream Inputs**: Incoming API gateway requests `(client_id, cost, now_seconds)`.
- **Core Responsibility**: Decide deterministically in $O(1)$ time & memory whether a request is admitted (`allowed=True`) or rejected (`retry_after > 0`).
- **Downstream Consumers / Effects**: If this component allows unchecked bursts or underflows tokens, downstream databases suffer cascading exhaustion or false-positive `429` outages.

```text
[API Client] -> [Gateway Auth] -> [TokenBucketLimiter.allow()] -> (Allowed) -> [Upstream Service]
                                              |
                                         (Rejected: HTTP 429 + Retry-After)
```

---

## Part 2: Categorized Blind Retrieval Q&A (Draft -> Scenario Probe -> Audit)

> Write concise keywords under `> **My Draft**:`. Send to your AI coach for scoring and failure-scenario follow-ups.

### Category A: Time, Memory & Concurrency Invariants

#### Q1.1 Why does production rate limiting use lazy timestamp calculation instead of spawning a background timer that adds tokens every 100ms? (`3` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until draft + scenario probe are completed)*

#### Q1.2 What breaks in a rate limiter if you read `time.time()` (wall clock) instead of a monotonic clock, or if you track per-key buckets without a TTL/eviction policy? (`2` core points)
- > **My Draft**: 
- > **Follow-up & Audited Answer**: *(Locked until draft + scenario probe are completed)*

---

## Part 3: Intuition Traps & Anti-Patterns

| Category | Intuition Trap | Real-World Failure Mode | Reliable Principle |
|---|---|---|---|
| Refill Mechanism | Spawn a background thread ticking every `dt` to top up every user's tokens | With 1M active tenants, timer scheduling overhead & lock contention stall the process | **Lazy O(1) refill**: store `(tokens, last_ts)` and compute elapsed refill only when `allow()` is called |
| Clamping | `tokens += elapsed * refill_rate` without capping | Idle users accumulate millions of tokens overnight, unleashing a massive thundering herd at 9 AM | Always clamp `tokens = min(capacity, tokens + elapsed * refill_rate)` |
| Wall Clock | Use Unix epoch `time.time()` for `elapsed = now - last_ts` | NTP clock jump backwards makes `elapsed < 0`, permanently draining tokens or causing negative sleep | Use **monotonic clock** (`time.monotonic()`), or guard `max(0.0, now - last_ts)` |
| Cost Validation | Only check `if tokens >= 1` for variable-cost endpoints | Heavy batch requests (`cost=10`) succeed with `tokens=1`, causing negative balance debt | Check `tokens >= cost` and validate `cost > 0` (reject or treat `cost > capacity` cleanly) |

---

## Part 4: Active Production Drill — 4-Slot Pseudocode Compilation

### Drill 4.1: `TokenBucketLimiter.allow(key, cost, now)`

#### Input / Output Examples (Plain Data)
```json
[
  {
    "config": {"capacity": 5.0, "refill_rate_per_sec": 2.0},
    "call": {"key": "user_1", "cost": 3.0, "now": 10.0},
    "expected_output": {"allowed": true, "remaining_tokens": 2.0, "retry_after": 0.0}
  },
  {
    "config": {"capacity": 5.0, "refill_rate_per_sec": 2.0},
    "call": {"key": "user_1", "cost": 4.0, "now": 10.5},
    "note": "0.5s elapsed -> +1.0 token (2.0 + 1.0 = 3.0 available < 4.0 needed)",
    "expected_output": {"allowed": false, "remaining_tokens": 3.0, "retry_after": 0.5}
  }
]
```

#### Stripped Interface Contract
- Implement inside `exercise.py`:
  - `Decision(allowed: bool, remaining_tokens: float, retry_after: float)` (already imported)
  - `TokenBucketLimiter(capacity: float, refill_rate: float)`
  - Method: `allow(self, key: str, cost: float = 1.0, now: float | None = None) -> Decision`
- When a `key` is seen for the very first time, it starts full (`tokens = capacity`, `last_ts = now`).
- Wait: if `now is None`, default to `time.monotonic()`.

#### 4-Slot Native-Language Pseudocode (Submit to AI Coach to Compile 1:1 into `exercise.py`)
- **Slot 1 — State & Containers**: 
- **Slot 2 — Core Step / Transition**: 
- **Slot 3 — Boundary & Error Guards**: 
- **Slot 4 — Return / Side-Effect Contract**: 

---

## Part 5: Unit Sign-Off Checklist

- [ ] Can explain lazy token refill vs background ticker and Token Bucket vs Leaky Bucket in 60 seconds.
- [ ] Answered `Q1.1` & `Q1.2` blind and cleared scenario follow-ups.
- [ ] Compiled 4-slot pseudocode into `exercise.py` and passed 100% of `test_exercise.py`.
- [ ] Reviewed `solution.py` idioms (e.g., `max(0.0, now - state.last_ts)` and `min(capacity, ...)`).
