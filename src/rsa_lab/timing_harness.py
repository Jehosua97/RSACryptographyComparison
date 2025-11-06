# src/rsa_lab/timing_harness.py
import time, statistics, math
import numpy as np
from typing import Callable

def measure_runtime_ns(fn: Callable[[int], int], samples: list[int]) -> list[int]:
    times = []
    for x in samples:
        t0 = time.perf_counter_ns()
        _ = fn(x)
        t1 = time.perf_counter_ns()
        times.append(t1 - t0)
    return times

def summarize(times: list[int]) -> dict:
    return {
        "n": len(times),
        "mean_ns": statistics.mean(times),
        "stdev_ns": statistics.pstdev(times),
        "min_ns": min(times),
        "max_ns": max(times),
    }

def compare_distributions(a: list[int], b: list[int]) -> dict:
    # JS divergence on normalized histograms (coarse, stable)
    hist_a, edges = np.histogram(a, bins="auto", density=True)
    hist_b, _ = np.histogram(b, bins=edges, density=True)
    pa = hist_a / (hist_a.sum() + 1e-12)
    pb = hist_b / (hist_b.sum() + 1e-12)
    m = 0.5 * (pa + pb)
    def kl(p, q):
        p = np.clip(p, 1e-12, 1); q = np.clip(q, 1e-12, 1)
        return float(np.sum(p * np.log(p / q)))
    js = 0.5 * kl(pa, m) + 0.5 * kl(pb, m)
    return {"js_divergence": js}
