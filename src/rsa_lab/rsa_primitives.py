# src/rsa_lab/rsa_primitives.py
import secrets
from dataclasses import dataclass
from .math_utils import egcd, modinv

def _random_prime(bits: int) -> int:
    # Very small Miller–Rabin for demo; replace with a vetted prime lib in real life.
    from random import randrange
    from math import log2
    def is_probable_prime(n: int) -> bool:
        if n < 2 or any(n % p == 0 for p in (2,3,5,7,11,13,17,19,23,29)):
            return n in (2,3,5,7,11,13,17,19,23,29)
        # Miller-Rabin bases sufficient for 64-bit; for >1024 bits add bases or use library.
        d, s = n - 1, 0
        while d % 2 == 0:
            d //= 2; s += 1
        for a in (2,325,9375,28178,450775,9780504,1795265022):
            if a % n == 0: 
                continue
            x = pow(a, d, n)
            if x in (1, n - 1): 
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True

    while True:
        cand = secrets.randbits(bits) | 1 | (1 << (bits - 1))
        if is_probable_prime(cand):
            return cand

@dataclass
class RSAKey:
    n: int
    e: int
    d: int
    p: int
    q: int
    dp: int
    dq: int
    qinv: int  # q^{-1} mod p

def generate_keypair(bits: int = 2048, e: int = 65537) -> RSAKey:
    half = bits // 2
    while True:
        p = _random_prime(half)
        q = _random_prime(bits - half)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if egcd(e, phi)[0] == 1:
            break
    d = modinv(e, phi)
    return RSAKey(
        n=p*q, e=e, d=d,
        p=p, q=q,
        dp=d % (p - 1),
        dq=d % (q - 1),
        qinv=modinv(q, p)
    )
