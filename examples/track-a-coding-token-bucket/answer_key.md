# Token Bucket Rate Limiter — Separated Answer Key

> **Track**: `coding`  
> **Spoiler Guard**: Keep closed until blind drafts in `workbench.md` are graded.

---

### Q1.1 Why does production rate limiting use lazy timestamp calculation instead of spawning a background timer that adds tokens every 100ms?
- **Core Scoring Points (`3`)**:
  1. **Zero Idle CPU / Timer Churn**: Only active keys execute arithmetic (`elapsed * refill_rate`) at request arrival, giving $O(1)$ per-request cost regardless of total user count.
  2. **No Lock Contention Against Tickers**: Avoids scanning millions of buckets periodically under mutex locks.
  3. **Precision Without Tick Quantization**: Continuous float/microsecond time delta eliminates burst spikes aligned to coarse timer intervals.
- **Scenario Probes (Use if missed)**:
  - *Missing Point 1 or 2*: `"Your SaaS gateway now has 500,000 registered workspaces, though only 3,000 are active per minute. What happens to your single ticker thread every 100ms?"`
  - *Missing Point 3*: `"Why do requests arriving 1ms after a 1-second refill tick all succeed at once if tokens only increment on timer ticks?"`

### Q1.2 What breaks in a rate limiter if you read `time.time()` (wall clock) instead of a monotonic clock, or if you track per-key buckets without a TTL/eviction policy?
- **Core Scoring Points (`2`)**:
  1. **Non-Monotonic Clock Jumps (NTP Skew)**: Wall-clock adjustment backwards produces negative `elapsed`, shrinking available tokens or generating huge `retry_after` lockouts.
  2. **Unbounded Memory Leak**: Storing a `(tokens, last_ts)` entry forever per distinct IP/user causes steady OOM under high-cardinality traffic or DDoS.
- **Scenario Probes (Use if missed)**:
  - *Missing Point 1*: `"At 02:00 UTC, NTP steps the host clock backward by 3 seconds. What is `now - last_ts` for the next request, and what happens to `tokens`?"`
  - *Missing Point 2*: `"An attacker sends 10 million requests using randomized `X-Forwarded-For` client IDs. Even though 99% never return, why does your gateway crash 20 minutes later?"`
