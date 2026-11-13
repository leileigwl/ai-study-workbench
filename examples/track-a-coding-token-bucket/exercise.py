"""Starter exercise stub for Track A showcase: Token Bucket Rate Limiter."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    """Result returned by TokenBucketLimiter.allow()."""

    allowed: bool
    remaining_tokens: float
    retry_after: float


class TokenBucketLimiter:
    """Per-key lazy-refill token bucket rate limiter."""

    def __init__(self, capacity: float, refill_rate: float) -> None:
        if capacity <= 0 or refill_rate <= 0:
            raise ValueError("capacity and refill_rate must be positive")
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        # Learners/AI compile Slot 1 state structures below:

    def allow(self, key: str, cost: float = 1.0, now: float | None = None) -> Decision:
        """Evaluate whether a request for `key` consuming `cost` tokens is allowed."""
        _ = now if now is not None else time.monotonic()
        raise NotImplementedError("Compile your 4-slot pseudocode from workbench.md here.")
