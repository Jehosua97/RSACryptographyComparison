# tests/test_constant_time.py
from rsa_lab.timing_harness import measure_runtime_ns, summarize
from rsa_lab.rsa_primitives import generate_keypair
from rsa_lab.modexp_constant import modexp_always_square_mul
import secrets

def test_low_variance_vs_input_variation():
    key = generate_keypair(1024)
    n, d = key.n, key.d
    def const_call(m): return modexp_always_square_mul(m % n, d, n)
    samples = [secrets.randbelow(n-1) + 1 for _ in range(400)]
    times = measure_runtime_ns(const_call, samples)
    s = summarize(times)
    # Heuristic: stdev relative to mean is modest (not a proof of const-time)
    assert s["stdev_ns"] / s["mean_ns"] < 0.25
