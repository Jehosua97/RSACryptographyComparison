# src/rsa_lab/math_utils.py
from typing import Tuple

def ct_select(a: int, b: int, sel: int) -> int:
    """Constant-time select: returns a if sel == 0 else b."""
    mask = -int(bool(sel))  # 0 -> 0x0, 1 -> 0x...FF
    return (a & ~mask) | (b & mask)

def egcd(a: int, b: int) -> Tuple[int, int, int]:
    """Extended GCD: returns (g, x, y) with ax + by = g = gcd(a,b)."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, n: int) -> int:
    g, x, _ = egcd(a, n)
    if g != 1:
        raise ValueError("No inverse")
    return x % n
