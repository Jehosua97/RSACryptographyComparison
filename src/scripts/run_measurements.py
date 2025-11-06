# scripts/run_measurements.py
from rsa_lab.rsa_primitives import generate_keypair, rsa_encrypt, rsa_decrypt_secure
from rsa_lab.modexp_vulnerable import modexp_square_multiply
from rsa_lab.modexp_constant import modexp_always_square_mul
from rsa_lab.timing_harness import measure_runtime_ns, summarize, compare_distributions
import secrets

key = generate_keypair(2048)
n = key.n

# Build callable wrappers (same interface) for fair comparison
def vuln_call(m):
    return modexp_square_multiply(m % n, key.d, n)

def const_call(m):
    return modexp_always_square_mul(m % n, key.d, n)

# Random messages (no structured probes)
samples = [secrets.randbelow(n-1) + 1 for _ in range(2000)]

tv = measure_runtime_ns(vuln_call, samples)
tc = measure_runtime_ns(const_call, samples)

print("VULN:", summarize(tv))
print("CONST:", summarize(tc))
print("DIVERGENCE:", compare_distributions(tv, tc))
