"""Clean reference implementation shown only AFTER all tests pass."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    """Result returned by TokenBucketLimiter.allow()."""

    allowed: bool
    remaining_tokens: float
    retry_after: float


@dataclass
class _BucketState:
    tokens: float
    last_ts: float


class TokenBucketLimiter:
    """Per-key lazy-refill token bucket rate limiter."""

    def __init__(self, capacity: float, refill_rate: float) -> None:
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("capacity and refill_rate must be positive")
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self._buckets: dict[str, _BucketState] = {}

    def allow(self, key: str, cost: float = 1.0, now: float | None = None) -> Decision:
        """Evaluate whether a request consuming `cost` tokens is allowed."""
        if cost <= 0:
            raise ValueError("cost must be positive")

        ts = time.monotonic() if now is None else float(now)
        state = self._buckets.get(key)
        if state is None:
            state = _BucketState(tokens=self.capacity, last_ts=ts)
            self._buckets[key] = state
        else:
            elapsed = max(0.0, ts - state.last_ts)
            state.tokens = min(self.capacity, state.tokens + elapsed * self.refill_rate)
            state.last_ts = ts

        if cost > self.capacity or state.tokens < cost:
            deficit = cost - state.tokens
            return Decision(
                allowed=False,
                remaining_tokens=state.tokens,
                retry_after=deficit / self.refill_rate,
            )

        state.tokens -= cost
        return Decision(allowed=True, remaining_tokens=state.tokens, retry_after=0.0)
