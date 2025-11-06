# Toy RSA timing attack demonstration (educational only).
# [Unverified] This is a simplified simulation to show the principle.

import time, random, math
from statistics import mean
import pandas as pd

# --- tiny RSA key (insecure) ---
def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    r = int(n**0.5)
    for i in range(3, r+1, 2):
        if n % i == 0: return False
    return True

def gen_small_prime(start=100, end=400):
    while True:
        p = random.randrange(start, end)
        if is_prime(p):
            return p

p = gen_small_prime(100,500)
q = gen_small_prime(100,500)
while q == p:
    q = gen_small_prime(100,500)
N = p * q
phi = (p-1)*(q-1)
e = 65537
def egcd(a,b):
    if b==0: return (a,1,0)
    g,x1,y1 = egcd(b,a%b)
    return (g, y1, x1 - (a//b)*y1)
g, x, y = egcd(e, phi)
if g != 1:
    for cand in range(3, 1000, 2):
        g, x, y = egcd(cand, phi)
        if g==1:
            e = cand
            break
d = x % phi
d_bits = list(map(int, bin(d)[2:]))

print(f"Demo RSA modulus N = {N}, key exponent d (bits) length = {len(d_bits)}")

# --- vulnerable exponentiation but *targeted* leak ---
EXTRA_DELAY_PER_MULTIPLY = 0.0008  # seconds (tweak to make signal visible)

def vulnerable_modexp_targeted(m, d_bits, N, target_bit_index):
    """Simulated exponentiation that adds extra delay only when processing target_bit_index
    AND when that bit==1 AND the chosen input m is odd. This models an attacker-crafted input
    that makes timing sensitive to one step (toy model)."""
    start = time.perf_counter()
    R = 1
    for i, bit in enumerate(d_bits):
        R = (R * R) % N
        if bit == 1:
            R = (R * m) % N
            if i == target_bit_index and (m & 1) == 1:
                t0 = time.perf_counter()
                cnt = 0
                while time.perf_counter() - t0 < EXTRA_DELAY_PER_MULTIPLY:
                    cnt += 1
    elapsed = time.perf_counter() - start
    return R, elapsed

def targeted_oracle(m, target_bit_index):
    _, elapsed = vulnerable_modexp_targeted(m, d_bits, N, target_bit_index)
    return elapsed

def recover_bits_targeted(num_samples=120):
    recovered = []
    rows = []
    for idx in range(len(d_bits)):
        odd = [targeted_oracle(random.randrange(2, N-1) | 1, idx) for _ in range(num_samples)]
        even = [targeted_oracle(random.randrange(2, N-1) & ~1, idx) for _ in range(num_samples)]
        avg_odd = mean(odd)
        avg_even = mean(even)
        guessed = 1 if (avg_odd - avg_even) > (EXTRA_DELAY_PER_MULTIPLY/4) else 0
        recovered.append(guessed)
        rows.append({"bit_index": idx, "avg_odd": avg_odd, "avg_even": avg_even, "delta": avg_odd-avg_even, "guessed": guessed, "true": d_bits[idx]})
        print(f"bit {idx:02d}: avg_odd={avg_odd:.6f}, avg_even={avg_even:.6f}, delta={avg_odd-avg_even:.6f}, guessed={guessed}, true={d_bits[idx]}")
    return recovered, pd.DataFrame(rows)

recovered_bits, df2 = recover_bits_targeted(num_samples=120)
print("\nTrue:", "".join(map(str, d_bits)))
print("Recovered:", "".join(map(str, recovered_bits)))

# If you want a table show, use pandas display or print df2
print(df2.head(10))