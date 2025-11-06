# src/rsa_lab/power_simulator.py
import numpy as np

def hamming_weight(x: int) -> int:
    return x.bit_count()

def simulate_trace_square_multiply(m: int, d: int, n: int, noise_std: float = 1.0) -> np.ndarray:
    # Returns a synthetic trace vector (not aligned to real clocks)
    rng = np.random.default_rng()
    r = 1
    x = m % n
    trace = []
    for bit in bin(d)[2:]:
        r = (r * r) % n
        trace.append(hamming_weight(r) + rng.normal(0, noise_std))  # square “cost”
        if bit == '1':
            r = (r * x) % n
            trace.append(hamming_weight(r) + rng.normal(0, noise_std))  # multiply “cost”
    return np.array(trace)

def simulate_trace_always(m: int, d: int, n: int, noise_std: float = 1.0) -> np.ndarray:
    rng = np.random.default_rng()
    r = 1
    x = m % n
    trace = []
    for _ in bin(d)[2:]:
        r_sq = (r * r) % n
        trace.append(hamming_weight(r_sq) + rng.normal(0, noise_std)) # square
        r_mul = (r_sq * x) % n
        trace.append(hamming_weight(r_mul) + rng.normal(0, noise_std)) # multiply
        # selection is abstracted, no branching visible in synthetic trace
        r = r_mul  # or r_sq; selection hidden in simulator
    return np.array(trace)
