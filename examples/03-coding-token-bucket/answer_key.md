# Token Bucket Rate Limiter — Separated Answer Key (For Your AI Coach)

> **Track**: `coding`  
> Keep closed while practicing `workbench.md`. Q-IDs match 1:1.

---

### Q1.1 Why do real rate limiters compute new tokens using timestamp math on arrival instead of a background timer?
- **Key Points (`3`)**:
  1. **Zero Idle CPU**: Only active keys do math (`elapsed * rate`), keeping cost $O(1)$ per request.
  2. **No Lock Contention**: Avoids periodically scanning millions of buckets under a global lock.
  3. **Smooth Continuous Refill**: Eliminates artificial burst waves aligned to coarse timer ticks.
- **Follow-Up Prompts if Missed**:
  - *If missing Point 1*: `"You have 500,000 signed-up users, only 2,000 active right now. What happens to your server every 100ms if a background thread loops through all 500,000 buckets?"`

### Q1.2 What goes wrong with wall-clock time or never evicting inactive keys?
- **Key Points (`2`)**:
  1. **NTP Backward Jump**: Negative `elapsed` subtracts tokens instead of adding them.
  2. **Unbounded Memory Leak**: Random/one-time keys accumulate forever until OOM crash.
- **Follow-Up Prompts if Missed**:
  - *If missing Point 2*: `"An attacker blasts 5 million requests from randomized IP keys, and each gets blocked nicely. Why does the gateway still crash 15 minutes later?"`
