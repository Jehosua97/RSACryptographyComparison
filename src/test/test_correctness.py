# tests/test_correctness.py
from rsa_lab.rsa_primitives import generate_keypair, rsa_encrypt, rsa_decrypt_secure
import secrets

def test_encrypt_decrypt_roundtrip():
    key = generate_keypair(1024)
    for _ in range(20):
        m = secrets.randbelow(key.n - 1) + 1
        c = rsa_encrypt(m, key)
        m2 = rsa_decrypt_secure(c, key, use_blinding=True, use_crt=True)
        assert m == m2
