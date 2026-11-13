# Token Bucket Rate Limiter — Extracted Standard Answers & Mock Rubric

> **Domain**: `coding`  
> Extracted from source material. Used by the AI coach to grade `workbench.md` and run Step 4 Mock Simulations.

---

### Q1.1 Why do real rate limiters compute tokens lazily on request arrival instead of a background timer?
- **Standard Answer Key Points (`3`)**:
  1. **Zero Idle CPU**: Only active keys execute arithmetic (`elapsed * rate`), keeping cost $O(1)$ per request.
  2. **No Lock Contention**: Avoids periodically scanning millions of buckets under locks.
  3. **Smooth Continuous Refill**: Eliminates traffic bursts aligned to coarse timer ticks.
- **Follow-Up Probes if Missed (Never spoil directly)**:
  - *If missing Point 1*: `"You have 500,000 signed-up users and 2,000 active right now. What happens every 100ms if a background thread loops over all 500,000 buckets?"`

### Q1.2 What breaks with wall-clock time or never evicting inactive keys?
- **Standard Answer Key Points (`2`)**:
  1. **NTP Backward Jump**: Negative elapsed delta drains tokens instead of adding them.
  2. **Unbounded Memory Leak**: One-time keys accumulate forever until an OOM crash.
- **Follow-Up Probes if Missed**:
  - *If missing Point 2*: `"An attacker blasts 5 million requests from randomized IP keys, and each gets blocked cleanly. Why does the gateway still crash 15 minutes later?"`
