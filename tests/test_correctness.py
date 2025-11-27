from rsa_lab.rsa_primitives import generate_keypair, rsa_encrypt
from rsa_lab.modexp_constant import modexp_always
import secrets

def test_roundtrip():
    key = generate_keypair(512)
    m = secrets.randbelow(key.n-1)+1
    c = rsa_encrypt(m, key)
    m2 = modexp_always(c, key.d, key.n)
    assert m == m2
