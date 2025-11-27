import secrets

from rsa_lab.rsa_primitives import generate_keypair, rsa_encrypt
from rsa_lab.modexp_vulnerable import modexp_vuln
from rsa_lab.modexp_constant import modexp_always
from rsa_lab.analysis import timing_experiment, power_experiment


def main() -> None:
    print("=== Side-Channel Educational Demo ===")

    # 1) Key pequeña para que sea rápido en vivo
    print("1) Generating a small RSA key (512 bits) just for the demo...")
    key = generate_keypair(512)
    print(f"   - n bits: {key.n.bit_length()}")
    print(f"   - e: {key.e}")

    # 2) Demo de cifrado/descifrado
    print("\n2) Encrypting and decrypting one sample message...")
    m = 42
    c = rsa_encrypt(m, key)
    print(f"   Plaintext m = {m}")
    print(f"   Ciphertext c = pow(m, e, n) = {c}")
    print("   Decrypting in two ways: vulnerable and constant-time style...")

    m_v = modexp_vuln(c, key.d, key.n)
    m_c = modexp_always(c, key.d, key.n)

    print(f"   Result vulnerable  = {m_v}")
    print(f"   Result constant    = {m_c}")
    print("   (Both should match original m)")

    # 3) Timing mini-experiment
    print("\n3) Now running a small timing experiment (quick version)...")
    timing_experiment(samples=80, key_bits=512)

    # 4) SPA sintético mini-experiment
    print("\n4) Now running a small synthetic power SPA experiment (quick version)...")
    power_experiment(noise=1.0, traces=60, key_bits=512)

    print("\nDemo finished. Use these outputs and plots in your presentation slides.")


if __name__ == "__main__":
    main()
