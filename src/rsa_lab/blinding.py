# src/rsa_lab/blinding.py
import secrets
from .math_utils import modinv
from .rsa_primitives import RSAKey

def blind_message(m: int, key: RSAKey) -> tuple[int, int]:
    """Return (m_blinded, r) where m_blinded = m * r^e mod n."""
    n, e = key.n, key.e
    while True:
        r = secrets.randbelow(n - 2) + 2  # in [2, n-1]
        if r % key.p != 0 and r % key.q != 0:
            break
    r_e = pow(r, e, n)
    m_blinded = (m * r_e) % n
    return m_blinded, r

def unblind(c: int, r: int, key: RSAKey) -> int:
    rinv = modinv(r, key.n)
    return (c * rinv) % key.n

def exponent_blind(d: int, phi: int) -> int:
    """Return a randomized exponent d' = d + k*phi."""
    k = secrets.randbits(64)  # tunable
    return d + k * phi
