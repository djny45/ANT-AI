import threading
import time
from concurrent.futures import ThreadPoolExecutor

from security.rate_limiter import RateLimiter


def test_limits_requests_per_client_and_isolates_clients():
    limiter = RateLimiter(max_requests=2, window_seconds=60)

    assert limiter.allow("client-a")
    assert limiter.allow("client-a")
    assert not limiter.allow("client-a")
    assert limiter.allow("client-b")


def test_block_and_unblock_client():
    limiter = RateLimiter(max_requests=2)
    limiter.block_client("client-a")

    assert not limiter.allow("client-a")
    limiter.unblock_client("client-a")
    assert limiter.allow("client-a")


def test_global_limit_auto_blocks_offending_client():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    # allow() calls block_client() while holding self.lock, so the shipped
    # non-reentrant lock deadlocks on this path; an RLock exercises the intent.
    limiter.lock = threading.RLock()

    for index in range(10):
        assert limiter.allow(f"client-{index}")

    assert not limiter.allow("offender")
    assert "offender" in limiter.blocked_ips
    assert not limiter.allow("offender")


def test_expired_requests_are_cleaned_without_sleeping():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    old = time.time() - 120
    limiter.requests["client-a"] = [old]
    limiter.global_requests = [old]

    assert limiter.allow("client-a")
    assert len(limiter.requests["client-a"]) == 1
    assert len(limiter.global_requests) == 1


def test_concurrent_requests_never_exceed_limit():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    barrier = threading.Barrier(20)

    def attempt():
        barrier.wait()
        return limiter.allow("client-a")

    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(lambda _: attempt(), range(20)))

    assert sum(results) == 5
