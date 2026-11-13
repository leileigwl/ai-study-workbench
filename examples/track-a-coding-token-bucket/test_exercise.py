"""Deterministic test suite for TokenBucketLimiter (set TARGET_MODULE=solution to verify reference)."""

from __future__ import annotations

import importlib
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
TARGET_MODULE = os.environ.get("TARGET_MODULE", "exercise")
mod = importlib.import_module(TARGET_MODULE)
TokenBucketLimiter = mod.TokenBucketLimiter


class TestTokenBucketLimiter(unittest.TestCase):
    """Covers lazy refill, burst clamping, partial deficit retry_after, backward clock, and key isolation."""

    def test_first_request_starts_full_and_consumes(self) -> None:
        limiter = TokenBucketLimiter(capacity=5.0, refill_rate=2.0)
        res = limiter.allow("alice", cost=3.0, now=10.0)
        self.assertTrue(res.allowed)
        self.assertAlmostEqual(res.remaining_tokens, 2.0)
        self.assertAlmostEqual(res.retry_after, 0.0)

    def test_reject_computes_exact_retry_after_without_draining_tokens(self) -> None:
        limiter = TokenBucketLimiter(capacity=5.0, refill_rate=2.0)
        limiter.allow("alice", cost=3.0, now=10.0)
        res = limiter.allow("alice", cost=4.0, now=10.5)
        self.assertFalse(res.allowed)
        self.assertAlmostEqual(res.remaining_tokens, 3.0)
        self.assertAlmostEqual(res.retry_after, 0.5)

    def test_idle_refill_never_exceeds_capacity(self) -> None:
        limiter = TokenBucketLimiter(capacity=5.0, refill_rate=2.0)
        limiter.allow("alice", cost=4.0, now=10.0)
        res = limiter.allow("alice", cost=1.0, now=9999.0)
        self.assertTrue(res.allowed)
        self.assertAlmostEqual(res.remaining_tokens, 4.0)

    def test_backward_clock_tick_is_clamped_safe(self) -> None:
        limiter = TokenBucketLimiter(capacity=5.0, refill_rate=2.0)
        limiter.allow("alice", cost=2.0, now=20.0)
        res = limiter.allow("alice", cost=1.0, now=15.0)
        self.assertTrue(res.allowed)
        self.assertAlmostEqual(res.remaining_tokens, 2.0)

    def test_keys_are_isolated(self) -> None:
        limiter = TokenBucketLimiter(capacity=2.0, refill_rate=1.0)
        self.assertTrue(limiter.allow("alice", cost=2.0, now=1.0).allowed)
        self.assertFalse(limiter.allow("alice", cost=1.0, now=1.0).allowed)
        self.assertTrue(limiter.allow("bob", cost=2.0, now=1.0).allowed)

    def test_invalid_non_positive_cost_raises(self) -> None:
        limiter = TokenBucketLimiter(capacity=2.0, refill_rate=1.0)
        with self.assertRaises(ValueError):
            limiter.allow("alice", cost=0.0, now=1.0)


if __name__ == "__main__":
    unittest.main()
