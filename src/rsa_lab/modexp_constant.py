# src/rsa_lab/modexp_constant.py
def modexp_always_square_mul(m: int, d: int, n: int) -> int:
    """Square-and-multiply-always: constant sequence of operations per bit."""
    r = 1
    x = m % n
    for bit in bin(d)[2:]:
        # Always do both ops, then select
        r_sq = (r * r) % n
        r_mul = (r_sq * x) % n
        # Select without branching
        is_one = 1 if bit == '1' else 0
        r = (r_mul * is_one + r_sq * (1 - is_one)) % n
    return r
